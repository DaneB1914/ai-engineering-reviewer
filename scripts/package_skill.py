"""Create a deterministic, allowlisted skill ZIP. Never include repository extras."""

from pathlib import Path
import zipfile

from validate import ROOT, contained_file, validate_skill

PACKAGE_FILES = ("SKILL.md", "LICENSE", "agents/openai.yaml")


def package(root=ROOT, destination=None):
    root = Path(root).resolve()
    meta = validate_skill(root)
    # Resolve and read all inputs before creating the output archive.
    files = [(relative, contained_file(root, relative).read_bytes()) for relative in PACKAGE_FILES]
    destination = Path(destination) if destination else root / "dist" / f"{meta['name']}.zip"
    if destination.resolve() in {contained_file(root, relative) for relative in PACKAGE_FILES}:
        raise ValueError("archive must not overwrite a package source file")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, content in files:
            info = zipfile.ZipInfo(f"{meta['name']}/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            # Normalize checkout line endings so Windows/Linux archives match.
            archive.writestr(info, content.replace(b"\r\n", b"\n"))
    return destination


if __name__ == "__main__":
    print(package())
