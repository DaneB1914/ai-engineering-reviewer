"""Validate this repository's skill, YAML, local file links, and eval manifest.

This is a packaging check, not a model-quality or full Markdown validator.
"""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently discarding a value."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(text):
    return yaml.load(text, Loader=UniqueLoader)


def contained_file(root, relative):
    root = Path(root).resolve()
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise ValueError(f"missing file or path outside repository: {relative}")
    return candidate


def validate_skill(root):
    root = Path(root)
    text = contained_file(root, "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", text, re.S)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter and have a body")
    meta = load_yaml(match[1])
    if not isinstance(meta, dict):
        raise ValueError("skill frontmatter must be a mapping")
    name = meta.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError("invalid skill name")
    if root.name != name:
        raise ValueError("skill name must match its directory")
    description = meta.get("description")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        raise ValueError("description must contain 1-1024 characters")
    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    if set(meta) - allowed:
        raise ValueError("unsupported skill frontmatter fields")
    if not match[2].strip():
        raise ValueError("skill body cannot be empty")
    return meta


def markdown_targets(text):
    # Check inline file links outside fenced examples. Anchors and remote URLs
    # are intentionally out of scope; all repository links use inline syntax.
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield from re.findall(r"\]\(([^\s)]+)\)", line)


def validate_links(root):
    root = Path(root).resolve()
    for file in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", "dist"} for part in file.relative_to(root).parts):
            continue
        for target in markdown_targets(file.read_text(encoding="utf-8")):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            relative = file.parent.relative_to(root) / unquote(parsed.path)
            contained_file(root, relative)


def validate_cases(root):
    root = Path(root)
    cases = json.loads(contained_file(root, "evals/cases.json").read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        raise ValueError("eval cases must be a nonempty list")
    ids = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("each eval case must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in ids:
            raise ValueError("eval IDs must be nonempty and unique")
        ids.add(case_id)
        if case.get("mode") not in {"QUICK", "STANDARD", "DEEP", "SECURITY", "ARCHITECTURE"}:
            raise ValueError(f"invalid eval mode: {case_id}")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError(f"missing prompt: {case_id}")
        for key in ("files", "checks"):
            values = case.get(key)
            if not isinstance(values, list) or not values or not all(isinstance(v, str) and v.strip() for v in values):
                raise ValueError(f"invalid {key}: {case_id}")
        for file in case["files"]:
            contained_file(root / "evals", file)
    return cases


def validate(root=ROOT):
    meta = validate_skill(root)
    validate_links(root)
    for pattern in ("*.yaml", "*.yml"):
        for file in Path(root).rglob(pattern):
            if not any(part in {".git", ".venv", "dist"} for part in file.relative_to(root).parts):
                load_yaml(file.read_text(encoding="utf-8"))
    cases = validate_cases(root)
    print(f"Validated {meta['name']}: metadata, YAML, local file links, {len(cases)} eval cases.")


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, OSError, yaml.YAMLError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
