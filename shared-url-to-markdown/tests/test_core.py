from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from shared_url_to_markdown.devalue import unflatten
from shared_url_to_markdown.models import Conversation, Message
from shared_url_to_markdown.providers import (
    merge_dom_messages,
    normalize_claude,
    parse_chatgpt_html,
)
from shared_url_to_markdown.render import (
    default_output_path,
    render_markdown,
    slugify,
    write_markdown,
)
from shared_url_to_markdown.urls import UrlValidationError, parse_shared_url, validate_redirect


CHATGPT_URL = "https://chatgpt.com/share/11111111-2222-4333-8444-555555555555"
CLAUDE_URL = "https://claude.ai/share/aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"


class UrlTests(unittest.TestCase):
    def test_accepts_and_normalizes_supported_urls(self) -> None:
        parsed = parse_shared_url(CHATGPT_URL + "?utm_source=test#fragment")
        self.assertEqual(parsed.provider, "chatgpt")
        self.assertEqual(parsed.normalized, CHATGPT_URL)

    def test_rejects_lookalike_hosts_and_private_pages(self) -> None:
        for url in (
            "https://chatgpt.com.evil.example/share/11111111-2222-4333-8444-555555555555",
            "https://evilchatgpt.com/share/11111111-2222-4333-8444-555555555555",
            "https://chatgpt.com/c/11111111-2222-4333-8444-555555555555",
            "http://chatgpt.com/share/11111111-2222-4333-8444-555555555555",
        ):
            with self.subTest(url=url), self.assertRaises(UrlValidationError):
                parse_shared_url(url)

    def test_redirect_must_remain_on_the_same_shared_conversation(self) -> None:
        original = parse_shared_url(CHATGPT_URL)
        validate_redirect(original, CHATGPT_URL + "?ignored=true")
        with self.assertRaises(UrlValidationError):
            validate_redirect(
                original,
                "https://chatgpt.com/share/99999999-2222-4333-8444-555555555555",
            )


class ProviderTests(unittest.TestCase):
    def test_devalue_unflattens_encoded_keys_and_references(self) -> None:
        values = [
            {"_1": 2},
            "linear_conversation",
            [3],
            {"_4": 5, "_6": 7, "_10": 11},
            "id",
            "m1",
            "author",
            {"_8": 9},
            "role",
            "user",
            "content",
            {"_12": 13},
            "parts",
            [14],
            "hello",
        ]
        hydrated = unflatten(values)
        self.assertEqual(hydrated["linear_conversation"][0]["content"]["parts"], ["hello"])

    def test_parses_chatgpt_react_router_payload(self) -> None:
        values = [
            {"_1": 2, "_15": 16},
            "linear_conversation",
            [3],
            {"_4": 5, "_6": 7, "_10": 11},
            "id",
            "m1",
            "author",
            {"_8": 9},
            "role",
            "user",
            "content",
            {"_12": 13},
            "parts",
            [14],
            "hello",
            "title",
            "Example Chat",
        ]
        chunk = json.dumps(values, separators=(",", ":")) + "\n"
        html = f"<script>window.__reactRouterContext.streamController.enqueue({json.dumps(chunk)});</script>"
        conversation = parse_chatgpt_html(html, parse_shared_url(CHATGPT_URL))
        self.assertEqual(conversation.title, "Example Chat")
        self.assertEqual([message.markdown for message in conversation.messages], ["hello"])

    def test_normalizes_claude_text_artifact_and_attachment_reference(self) -> None:
        payload = {
            "name": "Artifact example",
            "chat_messages": [
                {"uuid": "u1", "sender": "human", "content": [{"type": "text", "text": "Build it"}]},
                {
                    "uuid": "a1",
                    "sender": "assistant",
                    "content": [
                        {"type": "text", "text": "Done"},
                        {
                            "type": "tool_use",
                            "name": "create_artifact",
                            "input": {"id": "art1", "title": "Demo", "type": "html", "content": "<h1>Hi</h1>"},
                        },
                    ],
                    "attachments": [{"file_name": "source.txt"}],
                },
            ],
        }
        conversation = normalize_claude(payload, parse_shared_url(CLAUDE_URL), "fixture")
        self.assertEqual([message.role for message in conversation.messages], ["user", "assistant"])
        self.assertIn("[Attachment: source.txt]", conversation.messages[1].markdown)
        self.assertEqual(conversation.messages[1].artifacts[0].title, "Demo")

    def test_dom_merge_preserves_first_seen_top_to_bottom_order(self) -> None:
        merged = merge_dom_messages(
            [
                {"id": "1", "role": "user", "text": "one", "html": "one"},
                {"id": "2", "role": "assistant", "text": "two", "html": "two"},
                {"id": "2", "role": "assistant", "text": "two", "html": "two"},
                {"id": "3", "role": "user", "text": "three", "html": "three"},
            ]
        )
        self.assertEqual([item["id"] for item in merged], ["1", "2", "3"])


class RenderTests(unittest.TestCase):
    def conversation(self, completeness: str = "verified") -> Conversation:
        warnings = ["Completeness could not be verified."] if completeness != "verified" else []
        return Conversation(
            provider="chatgpt",
            share_id="11111111-2222-4333-8444-555555555555",
            title="CON: A / Demo?",
            source_url=CHATGPT_URL,
            messages=[Message("1", "user", "Hello"), Message("2", "assistant", "Hi")],
            extraction_method="fixture",
            completeness=completeness,
            warnings=warnings,
        )

    def test_warning_is_prominent_for_best_effort_output(self) -> None:
        rendered = render_markdown(
            self.conversation("best-effort"),
            generated_at=datetime(2026, 1, 2, 3, 4, tzinfo=timezone.utc),
        )
        self.assertIn('completeness: "best-effort"', rendered)
        self.assertIn("> [!WARNING]", rendered)
        self.assertLess(rendered.index("## User"), rendered.index("## Assistant"))

    def test_verified_frontmatter_uses_an_empty_warning_list(self) -> None:
        rendered = render_markdown(self.conversation())
        self.assertIn("warnings: []", rendered)

    def test_filename_is_portable_unique_and_never_silently_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            first = default_output_path(self.conversation(), directory)
            self.assertTrue(first.name.endswith("-11111111.md"))
            write_markdown(first, "first")
            second = default_output_path(self.conversation(), directory)
            self.assertNotEqual(first, second)
            with self.assertRaises(FileExistsError):
                write_markdown(first, "replacement")
            self.assertEqual(first.read_text(encoding="utf-8"), "first")

    def test_slugify_handles_reserved_names(self) -> None:
        self.assertEqual(slugify("CON"), "conversation-con")


if __name__ == "__main__":
    unittest.main()
