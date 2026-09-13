from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHATGPT_URL = "https://chatgpt.com/share/11111111-2222-4333-8444-555555555555"


class CliSnapshotTests(unittest.TestCase):
    def test_exports_complete_snapshot_without_network(self) -> None:
        payload = {
            "title": "Offline snapshot",
            "linear_conversation": [
                {
                    "id": "u1",
                    "author": {"role": "user"},
                    "content": {"parts": ["hello"]},
                },
                {
                    "id": "a1",
                    "author": {"role": "assistant"},
                    "content": {"parts": ["world"]},
                },
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            snapshot = directory / "snapshot.json"
            snapshot.write_text(json.dumps(payload), encoding="utf-8")
            output = directory / "export.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "export_shared_chat.py"),
                    CHATGPT_URL,
                    "--snapshot",
                    str(snapshot),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
            )
            rendered = output.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Completeness: verified", result.stdout)
        self.assertIn("## User\n\nhello", rendered)
        self.assertIn("## Assistant\n\nworld", rendered)

    def test_rejects_snapshot_with_browser_mode(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "export_shared_chat.py"),
                CHATGPT_URL,
                "--snapshot",
                "-",
                "--mode",
                "browser",
            ],
            input="{}",
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot be combined", result.stderr)


if __name__ == "__main__":
    unittest.main()
