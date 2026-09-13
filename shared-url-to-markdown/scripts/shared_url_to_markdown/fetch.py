from __future__ import annotations

import json
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener

from .models import Conversation
from .providers import (
    ProviderParseError,
    normalize_snapshot,
    parse_chatgpt_html,
)
from .urls import SharedUrl, validate_redirect


class RetrievalError(RuntimeError):
    pass


MAX_RETRIEVAL_BYTES = 25 * 1024 * 1024


class _RestrictedRedirectHandler(HTTPRedirectHandler):
    def __init__(self, allowed_host: str) -> None:
        super().__init__()
        self.allowed_host = allowed_host

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        parsed = urlsplit(new_url)
        if parsed.scheme != "https" or (parsed.hostname or "").lower() != self.allowed_host:
            raise RetrievalError(f"Blocked redirect outside {self.allowed_host}")
        return super().redirect_request(request, file_pointer, code, message, headers, new_url)


def extract_http(shared: SharedUrl, timeout: float) -> Conversation:
    if shared.provider == "chatgpt":
        snapshot_error: Exception | None = None
        endpoint = f"https://chatgpt.com/backend-api/share/{shared.share_id}"
        try:
            content, content_type, _ = _get(endpoint, "chatgpt.com", timeout)
            if "json" not in content_type:
                raise RetrievalError("ChatGPT's snapshot endpoint requires a browser challenge")
            return extract_snapshot_bytes(shared, content, "chatgpt-snapshot-api")
        except (RetrievalError, ProviderParseError, ValueError) as exc:
            snapshot_error = exc

        content, content_type, final_url = _get(shared.normalized, "chatgpt.com", timeout)
        validate_redirect(shared, final_url)
        if "html" not in content_type:
            raise RetrievalError(f"ChatGPT returned unexpected content type: {content_type}")
        try:
            return parse_chatgpt_html(content.decode("utf-8", errors="replace"), shared)
        except ProviderParseError as exc:
            raise RetrievalError(
                f"Snapshot endpoint failed ({snapshot_error}); share-page parsing failed ({exc})"
            ) from exc

    endpoint = (
        f"https://claude.ai/api/chat_snapshots/{shared.share_id}"
        "?rendering_mode=messages&render_all_tools=true"
    )
    content, content_type, _ = _get(endpoint, "claude.ai", timeout)
    prefix = content[:512].lower()
    if b"just a moment" in prefix or b"cf-mitigated" in prefix or "json" not in content_type:
        raise RetrievalError("Claude's snapshot endpoint requires a browser challenge")
    try:
        return extract_snapshot_bytes(shared, content, "claude-snapshot-api")
    except (json.JSONDecodeError, TypeError, ProviderParseError) as exc:
        raise RetrievalError(f"Could not parse Claude snapshot data: {exc}") from exc


def extract_snapshot_bytes(
    shared: SharedUrl, content: bytes, extraction_method: str = "provided-snapshot"
) -> Conversation:
    if len(content) > MAX_RETRIEVAL_BYTES:
        raise RetrievalError(
            f"Snapshot exceeds the {MAX_RETRIEVAL_BYTES // (1024 * 1024)} MiB limit"
        )
    try:
        payload = json.loads(content.decode("utf-8-sig"))
        if not isinstance(payload, dict):
            raise TypeError("snapshot response is not an object")
        return normalize_snapshot(payload, shared, extraction_method)
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ProviderParseError) as exc:
        raise RetrievalError(f"Could not parse {shared.provider} snapshot data: {exc}") from exc


def _get(url: str, allowed_host: str, timeout: float) -> tuple[bytes, str, str]:
    headers = {
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
        ),
    }
    request = Request(url, headers=headers)
    opener = build_opener(
        _RestrictedRedirectHandler(allowed_host),
        # Use the platform trust store and normal hostname verification.
        HTTPSHandler(context=ssl.create_default_context()),
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            content = response.read(MAX_RETRIEVAL_BYTES + 1)
            if len(content) > MAX_RETRIEVAL_BYTES:
                raise RetrievalError(
                    f"Shared page exceeds the {MAX_RETRIEVAL_BYTES // (1024 * 1024)} MiB limit"
                )
            return (
                content,
                response.headers.get("Content-Type", "").lower(),
                response.geturl(),
            )
    except RetrievalError:
        raise
    except HTTPError as exc:
        raise RetrievalError(f"Shared page returned HTTP {exc.code}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise RetrievalError(f"Could not retrieve shared page: {exc}") from exc
