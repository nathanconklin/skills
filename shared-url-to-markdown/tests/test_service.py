from __future__ import annotations

import sys
import os
import tempfile
import unittest
from asyncio import run
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from service.runtime import ExportCoordinator, ExportStore, ServiceSettings, SlidingWindowLimiter
from shared_url_to_markdown.models import Conversation, Message


class ServiceSettingsTests(unittest.TestCase):
    def test_origin_override_replaces_defaults(self) -> None:
        with patch.dict(os.environ, {"SHARED_URL_ALLOWED_ORIGINS": " https://example.com , http://localhost:6274 "}, clear=True):
            settings = ServiceSettings.from_env()
        self.assertEqual(settings.allowed_origins, ("https://example.com", "http://localhost:6274"))

    def test_rejects_origins_that_cannot_match_browser_headers(self) -> None:
        for origin in ("*", "https://*.example.com", "https://chatgpt.com/", "https://chatgpt.com/path", "http://example.com", "https://user@example.com", "https://example.com:bad"):
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                ServiceSettings(allowed_origins=(origin,)).validate()

    def test_requires_https_except_localhost(self) -> None:
        with self.assertRaises(ValueError):
            ServiceSettings(public_base_url="http://example.com").validate()
        with self.assertRaises(ValueError):
            ServiceSettings(public_base_url="http://localhost.evil:8000").validate()
        ServiceSettings(public_base_url="https://example.com").validate()
        ServiceSettings(public_base_url="http://127.0.0.1:8000").validate()


class SlidingWindowLimiterTests(unittest.TestCase):
    def test_limits_each_client_and_expires_old_events(self) -> None:
        limiter = SlidingWindowLimiter(limit=2, window_seconds=60)
        limiter.check("a", now=0)
        limiter.check("a", now=1)
        limiter.check("b", now=1)
        with self.assertRaises(RuntimeError):
            limiter.check("a", now=2)
        limiter.check("a", now=61)


class ExportStoreTests(unittest.TestCase):
    def conversation(self) -> Conversation:
        return Conversation(
            provider="chatgpt",
            share_id="11111111-2222-4333-8444-555555555555",
            title="Stored example",
            source_url=(
                "https://chatgpt.com/share/11111111-2222-4333-8444-555555555555"
            ),
            messages=[Message("u1", "user", "Hello")],
            extraction_method="fixture",
        )

    def test_creates_download_record_with_safe_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            store = ExportStore(Path(temporary), ttl_seconds=900, max_bytes=1024 * 1024)
            record = store.create(self.conversation())
            loaded = store.get(record.token)
            self.assertIsNotNone(loaded)
            self.assertIn(b"# Stored example", loaded.content)
            result = loaded.result("https://exports.example")
            self.assertEqual(result["completeness"], "verified")
            self.assertTrue(str(result["download_url"]).startswith("https://exports.example/"))
            self.assertNotIn("Hello", str(result))

    def test_rejects_oversize_output_and_invalid_token(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            store = ExportStore(Path(temporary), ttl_seconds=900, max_bytes=10)
            with self.assertRaises(ValueError):
                store.create(self.conversation())
            self.assertIsNone(store.get("../escape"))


class McpToolTests(unittest.TestCase):
    def test_tool_returns_metadata_and_resource_link_without_transcript(self) -> None:
        from service import app as service_app

        conversation = Conversation(
            provider="chatgpt",
            share_id="11111111-2222-4333-8444-555555555555",
            title="MCP example",
            source_url=(
                "https://chatgpt.com/share/11111111-2222-4333-8444-555555555555"
            ),
            messages=[Message("u1", "user", "Transcript must stay out of tool metadata")],
            extraction_method="fixture",
        )
        with tempfile.TemporaryDirectory() as temporary:
            store = ExportStore(Path(temporary), ttl_seconds=900, max_bytes=1024 * 1024)
            record = store.create(conversation)

            class FakeContext:
                client_id = "test-client"

            with patch.object(service_app.coordinator, "export", return_value=record):
                result = run(service_app.export_shared_chat(conversation.source_url, FakeContext()))

        self.assertEqual(result.structuredContent["message_count"], 1)
        self.assertEqual(result.content[1].type, "resource_link")
        self.assertNotIn("Transcript must stay out", result.content[0].text)


class McpHttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from service import app as service_app
        from starlette.testclient import TestClient

        # MCP's session manager has one lifespan per instance, as in production.
        cls.service = service_app
        cls.contexts = ExitStack()
        cls.addClassCleanup(cls.contexts.close)
        temporary = cls.contexts.enter_context(tempfile.TemporaryDirectory())
        settings = ServiceSettings(export_dir=Path(temporary))
        cls.contexts.enter_context(patch.object(service_app, "settings", settings))
        cls.contexts.enter_context(patch.object(service_app, "coordinator", ExportCoordinator(settings)))
        cls.client = cls.contexts.enter_context(TestClient(service_app.app, base_url=settings.public_base_url))

    def rpc(self, method, params, origin=None, host=None):
        headers = {"Accept": "application/json, text/event-stream"}
        if origin is not None:
            headers["Origin"] = origin
        if host is not None:
            headers["Host"] = host
        return self.client.post("/mcp", headers=headers, json={
            "jsonrpc": "2.0", "id": 1, "method": method, "params": params,
        })

    def initialize(self, origin=None, host=None):
        return self.rpc("initialize", {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "regression-test", "version": "1"},
        }, origin=origin, host=host)

    def test_accepts_configured_origins_and_requests_without_origin(self) -> None:
        for origin in (None, "https://chatgpt.com", "https://claude.ai"):
            with self.subTest(origin=origin):
                response = self.initialize(origin)
                self.assertEqual(response.status_code, 200, response.text)
                self.assertIn("serverInfo", response.json()["result"])
                if origin:
                    self.assertEqual(response.headers["access-control-allow-origin"], origin)

    def test_rejects_unconfigured_origins_and_hosts(self) -> None:
        for origin in ("https://untrusted.example", "https://chatgpt.com.evil.example", "null"):
            with self.subTest(origin=origin):
                response = self.initialize(origin)
                self.assertEqual(response.status_code, 403)
                self.assertNotIn("access-control-allow-origin", response.headers)
        self.assertEqual(self.initialize(host="untrusted.example").status_code, 421)

    def test_cors_preflight_agrees_with_mcp_origin_checks(self) -> None:
        for origin, expected in (("https://chatgpt.com", 200), ("https://untrusted.example", 400)):
            with self.subTest(origin=origin):
                response = self.client.options("/mcp", headers={
                    "Origin": origin, "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "content-type,mcp-protocol-version",
                })
                self.assertEqual(response.status_code, expected)

    def test_discovers_tool_exports_fixture_and_downloads_markdown(self) -> None:
        self.assertEqual(self.initialize("https://chatgpt.com").status_code, 200)
        tools = self.rpc("tools/list", {}, origin="https://chatgpt.com").json()["result"]["tools"]
        self.assertIn("export_shared_chat", [tool["name"] for tool in tools])
        conversation = ExportStoreTests().conversation()
        # Only provider retrieval is mocked; MCP, coordination, rendering, storage,
        # resource metadata, and the HTTP download execute normally.
        with patch("service.runtime.extract_http", return_value=conversation):
            response = self.rpc("tools/call", {
                "name": "export_shared_chat", "arguments": {"url": conversation.source_url},
            }, origin="https://chatgpt.com")
        self.assertEqual(response.status_code, 200, response.text)
        result = response.json()["result"]
        self.assertFalse(result.get("isError"), result)
        metadata = result["structuredContent"]
        self.assertEqual(metadata["message_count"], 1)
        self.assertEqual(metadata["completeness"], "verified")
        link = next(item for item in result["content"] if item["type"] == "resource_link")
        self.assertEqual(link["uri"], metadata["download_url"])
        download = self.client.get(urlsplit(metadata["download_url"]).path)
        self.assertEqual(download.status_code, 200)
        self.assertIn("# Stored example", download.text)
        self.assertIn("Hello", download.text)
        self.assertIn("attachment;", download.headers["content-disposition"])
        self.assertEqual(len(download.content), link["size"])
        self.assertEqual(self.client.get("/downloads/missing-token").status_code, 404)


if __name__ == "__main__":
    unittest.main()
