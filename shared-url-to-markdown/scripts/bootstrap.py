#!/usr/bin/env python3
"""Create an isolated runtime for the exporter."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Install exporter dependencies into .venv")
    parser.add_argument("--skip-browser", action="store_true", help="Do not download Chromium")
    args = parser.parse_args()

    if sys.version_info < (3, 10):
        print("Python 3.10 or newer is required.", file=sys.stderr)
        return 1

    root = Path(__file__).resolve().parent.parent
    venv = root / ".venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    subprocess.run(
        [str(python), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(root / "requirements.txt")],
        check=True,
    )
    if not args.skip_browser:
        environment = os.environ.copy()
        environment["PLAYWRIGHT_BROWSERS_PATH"] = str(venv / "playwright-browsers")
        subprocess.run(
            [str(python), "-m", "playwright", "install", "chromium"],
            check=True,
            env=environment,
        )
    print("Skill runtime is ready.")
    print(f'Run: "{python}" "{root / "scripts/export_shared_chat.py"}" URL')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
