#!/usr/bin/env python3
"""Build standalone skills and a self-contained plugin; MCP is opt-in."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile


SKILL_INCLUDED = ("SKILL.md", "requirements.txt", "agents", "references", "scripts")
EXCLUDED_PARTS = {"__pycache__", ".venv", "dist", "tests"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mcp-url",
        help="Optional connector endpoint; omit for a self-contained plugin with no MCP dependency",
    )
    parser.add_argument("--output-dir", type=Path, help="Package destination")
    args = parser.parse_args()
    mcp_url = _validate_mcp_url(args.mcp_url) if args.mcp_url else None

    root = Path(__file__).resolve().parent.parent
    output_dir = (args.output_dir or root / "dist").expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    skill_files = _skill_files(root)

    openai_zip = output_dir / "shared-url-to-markdown-openai.zip"
    _write_zip(openai_zip, ((path, path.relative_to(root)) for path in skill_files))
    print(openai_zip)

    claude_zip = output_dir / "shared-url-to-markdown-claude.zip"
    _write_zip(
        claude_zip,
        (
            (path, Path("shared-url-to-markdown") / path.relative_to(root))
            for path in skill_files
        ),
    )
    print(claude_zip)

    plugin_zip = output_dir / "shared-url-to-markdown-plugin.zip"
    _build_plugin(root, plugin_zip, mcp_url)
    print(plugin_zip)
    return 0


def _skill_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in SKILL_INCLUDED:
        candidate = root / name
        if candidate.is_file():
            files.append(candidate)
        elif candidate.is_dir():
            files.extend(path for path in candidate.rglob("*") if path.is_file())
    files = [
        path for path in files
        if not EXCLUDED_PARTS.intersection(path.relative_to(root).parts)
        and path.suffix not in {".pyc", ".pyo"}
        and path.name != "package_skill.py"
    ]
    return sorted(files)


def _write_zip(destination: Path, entries) -> None:
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for source, archive_path in entries:
            archive.write(source, archive_path.as_posix())


def _validate_mcp_url(value: str) -> str:
    parsed = urlsplit(value.rstrip("/"))
    local_http = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}
    if (parsed.scheme != "https" and not local_http) or not parsed.netloc:
        raise SystemExit("--mcp-url must be HTTPS, except for localhost testing")
    if parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise SystemExit("--mcp-url must not contain credentials, a query, or a fragment")
    if parsed.path.rstrip("/") != "/mcp":
        raise SystemExit("--mcp-url must end in /mcp")
    return value.rstrip("/")


def _build_plugin(root: Path, destination: Path, mcp_url: str | None = None) -> None:
    plugin_source = root / "plugins" / "shared-url-to-markdown"
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary) / "shared-url-to-markdown"
        shutil.copytree(plugin_source, stage)
        skill_stage = stage / "skills" / "shared-url-to-markdown"
        skill_stage.mkdir(parents=True, exist_ok=True)
        for source in _skill_files(root):
            relative = source.relative_to(root)
            target = skill_stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        if mcp_url:
            config = {"mcpServers": {"shared-url-to-markdown": {"type": "http", "url": mcp_url}}}
            (stage / ".mcp.json").write_text(
                json.dumps(config, indent=2) + "\n", encoding="utf-8"
            )
            manifest_path = stage / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["mcpServers"] = "./.mcp.json"
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        files = sorted(path for path in stage.rglob("*") if path.is_file())
        _write_zip(
            destination,
            ((path, Path("shared-url-to-markdown") / path.relative_to(stage)) for path in files),
        )


if __name__ == "__main__":
    raise SystemExit(main())
