"""Regression checks for invalid metadata, file boundaries, and package contents."""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from package_skill import PACKAGE_FILES, package
from validate import ROOT, contained_file, load_yaml, validate_cases, validate_links, validate_skill


class ToolingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "ai-engineering-reviewer"
        self.root.mkdir()
        for relative in PACKAGE_FILES:
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)

    def edit_skill(self, before, after):
        file = self.root / "SKILL.md"
        file.write_text(file.read_text(encoding="utf-8").replace(before, after), encoding="utf-8")

    def test_valid_skill(self):
        self.assertEqual(validate_skill(self.root)["name"], self.root.name)

    def test_missing_frontmatter_fails(self):
        (self.root / "SKILL.md").write_text("# No metadata\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_skill(self.root)

    def test_invalid_names_fail(self):
        for name in ("Bad_Name", "-review", "review--code", "r" * 65):
            with self.subTest(name=name):
                text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
                (self.root / "SKILL.md").write_text(text.replace("name: ai-engineering-reviewer", f"name: {name}"), encoding="utf-8")
                with self.assertRaises(ValueError):
                    validate_skill(self.root)

    def test_directory_mismatch_fails(self):
        self.edit_skill("name: ai-engineering-reviewer", "name: another-reviewer")
        with self.assertRaises(ValueError):
            validate_skill(self.root)

    def test_blank_description_fails(self):
        text = (self.root / "SKILL.md").read_text(encoding="utf-8")
        line = next(line for line in text.splitlines() if line.startswith("description:"))
        self.edit_skill(line, 'description: " "')
        with self.assertRaises(ValueError):
            validate_skill(self.root)

    def test_duplicate_yaml_keys_fail(self):
        with self.assertRaises(ValueError):
            load_yaml("name: first\nname: second\n")

    def test_missing_link_fails(self):
        (self.root / "README.md").write_text("[missing](missing.md)", encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_links(self.root)

    def test_links_allow_fragments_and_external_urls(self):
        (self.root / "README.md").write_text("[skill](SKILL.md#purpose) [web](https://example.com/a) [anchor](#here)", encoding="utf-8")
        validate_links(self.root)

    def test_path_escape_fails_even_for_existing_file(self):
        (self.root.parent / "private.md").write_text("outside", encoding="utf-8")
        with self.assertRaises(ValueError):
            contained_file(self.root, "../private.md")

    def test_missing_eval_fixture_fails(self):
        shutil.copytree(ROOT / "evals", self.root / "evals")
        cases = json.loads((self.root / "evals/cases.json").read_text(encoding="utf-8"))
        cases[0]["files"] = ["missing.js"]
        (self.root / "evals/cases.json").write_text(json.dumps(cases), encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_cases(self.root)

    def test_duplicate_eval_ids_fail(self):
        shutil.copytree(ROOT / "evals", self.root / "evals")
        cases = json.loads((self.root / "evals/cases.json").read_text(encoding="utf-8"))
        cases.append(cases[0])
        (self.root / "evals/cases.json").write_text(json.dumps(cases), encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_cases(self.root)

    def test_package_is_allowlisted(self):
        (self.root / ".env").write_text("TEST_ONLY=not-a-real-secret", encoding="utf-8")
        (self.root / "unrelated.txt").write_text("exclude me", encoding="utf-8")
        with zipfile.ZipFile(package(self.root)) as archive:
            self.assertEqual(archive.namelist(), [f"{self.root.name}/{file}" for file in PACKAGE_FILES])
            for file in PACKAGE_FILES:
                self.assertEqual(archive.read(f"{self.root.name}/{file}"), (self.root / file).read_bytes().replace(b"\r\n", b"\n"))

    def test_package_is_deterministic_across_line_endings(self):
        first = package(self.root).read_bytes()
        for relative in PACKAGE_FILES:
            file = self.root / relative
            file.write_bytes(file.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertEqual(first, package(self.root).read_bytes())

    def test_package_cannot_overwrite_source(self):
        before = (self.root / "SKILL.md").read_bytes()
        with self.assertRaises(ValueError):
            package(self.root, self.root / "SKILL.md")
        self.assertEqual(before, (self.root / "SKILL.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
