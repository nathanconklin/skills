from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_default_plugin_exports_snapshot_without_packages_or_network(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            built = subprocess.run(
                [sys.executable, str(ROOT / "scripts/package_skill.py"),
                 "--output-dir", str(destination)],
                capture_output=True, text=True,
            )
            self.assertEqual(built.returncode, 0, built.stderr)
            with ZipFile(destination / "shared-url-to-markdown-plugin.zip") as archive:
                names = archive.namelist()
                prefix = "shared-url-to-markdown/"
                self.assertNotIn(prefix + ".mcp.json", names)
                manifest = json.loads(archive.read(prefix + ".codex-plugin/plugin.json"))
                self.assertNotIn("mcpServers", manifest)
                self.assertFalse(any("/service/" in name or "/.venv/" in name for name in names))
                for name in names:
                    self.assertTrue((destination / name).resolve().is_relative_to(destination.resolve()))
                archive.extractall(destination)

            script = destination / prefix / "skills/shared-url-to-markdown/scripts/export_shared_chat.py"
            payload = {
                "title": "Self-contained package",
                "linear_conversation": [
                    {"id": "u1", "author": {"role": "user"},
                     "content": {"parts": ["A question"]}},
                    {"id": "a1", "author": {"role": "assistant"},
                     "content": {"parts": ["An answer\n\n```python\nprint(42)\n```"]}},
                ],
            }
            snapshot = destination / "snapshot.json"
            snapshot.write_text(json.dumps(payload), encoding="utf-8")
            output = destination / "export.md"
            # -S prevents third-party site-packages from loading; the audit hook
            # fails if the packaged exporter tries to open any network connection.
            runner = (
                "import runpy, sys\n"
                "from pathlib import Path\n"
                "def deny_network(event, args):\n"
                "    if event in ('socket.connect', 'socket.getaddrinfo'):\n"
                "        raise RuntimeError('Network unavailable in this test')\n"
                "sys.addaudithook(deny_network)\n"
                "sys.argv = sys.argv[1:]\n"
                "sys.path.insert(0, str(Path(sys.argv[0]).parent))\n"
                "runpy.run_path(sys.argv[0], run_name='__main__')\n"
            )
            exported = subprocess.run(
                [sys.executable, "-S", "-B", "-c", runner, str(script),
                 "https://chatgpt.com/share/11111111-2222-4333-8444-555555555555",
                 "--snapshot", str(snapshot), "--output", str(output)],
                cwd=destination, capture_output=True, text=True,
            )
            self.assertEqual(exported.returncode, 0, exported.stderr)
            markdown = output.read_text(encoding="utf-8")
            self.assertIn("Completeness: verified", exported.stdout)
            self.assertIn("## User\n\nA question", markdown)
            self.assertIn("```python\nprint(42)\n```", markdown)

    def test_builds_vendor_skills_and_universal_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "package_skill.py"),
                    "--output-dir",
                    str(destination),
                    "--mcp-url",
                    "https://exports.example/mcp",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            with ZipFile(destination / "shared-url-to-markdown-openai.zip") as archive:
                self.assertIn("SKILL.md", archive.namelist())
                self.assertNotIn("shared-url-to-markdown/SKILL.md", archive.namelist())

            with ZipFile(destination / "shared-url-to-markdown-claude.zip") as archive:
                self.assertIn("shared-url-to-markdown/SKILL.md", archive.namelist())

            with ZipFile(destination / "shared-url-to-markdown-plugin.zip") as archive:
                names = archive.namelist()
                prefix = "shared-url-to-markdown/"
                self.assertIn(prefix + ".codex-plugin/plugin.json", names)
                self.assertIn(prefix + ".claude-plugin/plugin.json", names)
                self.assertIn(prefix + "skills/shared-url-to-markdown/SKILL.md", names)
                config = json.loads(archive.read(prefix + ".mcp.json"))
                self.assertEqual(
                    config["mcpServers"]["shared-url-to-markdown"]["url"],
                    "https://exports.example/mcp",
                )

    def test_rejects_non_https_remote_connector(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "package_skill.py"),
                    "--output-dir",
                    temporary,
                    "--mcp-url",
                    "http://exports.example/mcp",
                ],
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be HTTPS", result.stderr)


if __name__ == "__main__":
    unittest.main()
