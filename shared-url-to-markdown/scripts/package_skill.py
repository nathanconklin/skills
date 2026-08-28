#!/usr/bin/env python3
"""Build a hosted-skill ZIP with SKILL.md at the archive root."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


INCLUDED = ("SKILL.md", "requirements.txt", "agents", "references", "scripts")
EXCLUDED_PARTS = {"__pycache__", ".venv", "dist", "tests"}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    destination = root / "dist" / "shared-url-to-markdown.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for name in INCLUDED:
        candidate = root / name
        if candidate.is_file():
            files.append(candidate)
        elif candidate.is_dir():
            files.extend(path for path in candidate.rglob("*") if path.is_file())
    files = [
        path for path in files
        if not EXCLUDED_PARTS.intersection(path.relative_to(root).parts)
        and path.suffix not in {".pyc", ".pyo"}
    ]
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, path.relative_to(root).as_posix())
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
