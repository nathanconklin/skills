from __future__ import annotations

import os
import secrets
import tempfile
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from shared_url_to_markdown.browser import BrowserExtractionError, extract_browser
from shared_url_to_markdown.fetch import RetrievalError, extract_http
from shared_url_to_markdown.models import Conversation
from shared_url_to_markdown.render import render_markdown, slugify
from shared_url_to_markdown.urls import parse_shared_url


MIB = 1024 * 1024


@dataclass(frozen=True, slots=True)
class ServiceSettings:
    public_base_url: str = "http://127.0.0.1:8000"
    export_dir: Path = Path(tempfile.gettempdir()) / "shared-url-to-markdown-service"
    timeout_seconds: float = 90.0
    download_ttl_seconds: int = 900
    max_output_bytes: int = 25 * MIB
    exports_per_minute: int = 10
    browser_concurrency: int = 2
    allowed_hosts: tuple[str, ...] = ("127.0.0.1:*", "localhost:*")
    allowed_origins: tuple[str, ...] = ("https://chatgpt.com", "https://claude.ai")

    @classmethod
    def from_env(cls) -> ServiceSettings:
        public_base_url = os.getenv(
            "SHARED_URL_PUBLIC_BASE_URL", "http://127.0.0.1:8000"
        ).rstrip("/")
        parsed_base = urlsplit(public_base_url)
        configured_hosts = os.getenv("SHARED_URL_ALLOWED_HOSTS", "")
        if configured_hosts:
            allowed_hosts = tuple(
                host.strip() for host in configured_hosts.split(",") if host.strip()
            )
        elif parsed_base.hostname in {"127.0.0.1", "localhost"}:
            allowed_hosts = ("127.0.0.1:*", "localhost:*")
        else:
            allowed_hosts = (parsed_base.netloc,)
        settings = cls(
            public_base_url=public_base_url,
            export_dir=Path(
                os.getenv(
                    "SHARED_URL_EXPORT_DIR",
                    str(Path(tempfile.gettempdir()) / "shared-url-to-markdown-service"),
                )
            ),
            timeout_seconds=float(os.getenv("SHARED_URL_TIMEOUT_SECONDS", "90")),
            download_ttl_seconds=int(
                os.getenv("SHARED_URL_DOWNLOAD_TTL_SECONDS", "900")
            ),
            max_output_bytes=int(os.getenv("SHARED_URL_MAX_OUTPUT_BYTES", str(25 * MIB))),
            exports_per_minute=int(os.getenv("SHARED_URL_EXPORTS_PER_MINUTE", "10")),
            browser_concurrency=int(os.getenv("SHARED_URL_BROWSER_CONCURRENCY", "2")),
            allowed_hosts=allowed_hosts,
            allowed_origins=tuple(
                origin.strip()
                for origin in os.getenv(
                    "SHARED_URL_ALLOWED_ORIGINS", "https://chatgpt.com,https://claude.ai"
                ).split(",")
                if origin.strip()
            ),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        parsed = urlsplit(self.public_base_url)
        local_http = parsed.scheme == "http" and parsed.hostname in {
            "127.0.0.1",
            "localhost",
        }
        if (parsed.scheme != "https" and not local_http) or not parsed.netloc:
            raise ValueError("SHARED_URL_PUBLIC_BASE_URL must use HTTPS outside localhost")
        if parsed.query or parsed.fragment or parsed.username or parsed.password:
            raise ValueError("SHARED_URL_PUBLIC_BASE_URL must be an origin without credentials")
        if not self.allowed_hosts:
            raise ValueError("At least one MCP Host header must be allowed")
        for origin in self.allowed_origins:
            parsed_origin = urlsplit(origin)
            local_origin = parsed_origin.scheme == "http" and parsed_origin.hostname in {
                "127.0.0.1", "localhost"
            }
            if (
                (parsed_origin.scheme != "https" and not local_origin)
                or not parsed_origin.hostname
                or "*" in origin
                or parsed_origin.path
                or parsed_origin.query
                or parsed_origin.fragment
                or parsed_origin.username
                or parsed_origin.password
            ):
                raise ValueError(
                    "SHARED_URL_ALLOWED_ORIGINS requires exact HTTPS origins "
                    "without paths or wildcards; localhost HTTP is allowed for testing"
                )
            # Accessing port also rejects malformed or out-of-range port values.
            parsed_origin.port
        positive = (
            self.timeout_seconds,
            self.download_ttl_seconds,
            self.max_output_bytes,
            self.exports_per_minute,
            self.browser_concurrency,
        )
        if any(value <= 0 for value in positive):
            raise ValueError("Service limits must all be greater than zero")


@dataclass(frozen=True, slots=True)
class ExportRecord:
    token: str
    filename: str
    content: bytes
    conversation: Conversation
    expires_at: float

    def result(self, public_base_url: str) -> dict[str, object]:
        expires = datetime.fromtimestamp(self.expires_at, timezone.utc).isoformat(
            timespec="seconds"
        )
        download_url = f"{public_base_url}/downloads/{self.token}"
        return {
            "provider": self.conversation.provider,
            "title": self.conversation.title,
            "message_count": len(self.conversation.messages),
            "completeness": self.conversation.completeness,
            "warnings": list(self.conversation.warnings),
            "filename": self.filename,
            "download_url": download_url,
            "expires_at": expires,
        }


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_seconds: float = 60.0) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str, now: float | None = None) -> None:
        timestamp = time.monotonic() if now is None else now
        with self._lock:
            events = self._events[key]
            cutoff = timestamp - self.window_seconds
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= self.limit:
                raise RuntimeError("Export rate limit exceeded; retry in one minute")
            events.append(timestamp)


class ExportStore:
    def __init__(self, directory: Path, ttl_seconds: int, max_bytes: int) -> None:
        self.directory = directory.expanduser().resolve()
        self.ttl_seconds = ttl_seconds
        self.max_bytes = max_bytes
        self._records: dict[str, ExportRecord] = {}
        self._lock = threading.Lock()
        self.directory.mkdir(parents=True, exist_ok=True)

    def create(self, conversation: Conversation) -> ExportRecord:
        content = render_markdown(conversation).encode("utf-8")
        if len(content) > self.max_bytes:
            raise ValueError(
                f"Markdown output exceeds the {self.max_bytes // MIB} MiB limit"
            )
        filename = (
            f"{conversation.provider}-{slugify(conversation.title)}-"
            f"{conversation.share_id[:8]}.md"
        )
        token = secrets.token_urlsafe(32)
        expires_at = time.time() + self.ttl_seconds
        target = self._path(token)
        temporary = target.with_suffix(".tmp")
        temporary.write_bytes(content)
        temporary.replace(target)
        record = ExportRecord(token, filename, content, conversation, expires_at)
        with self._lock:
            self._cleanup_locked(time.time())
            self._records[token] = record
        return record

    def get(self, token: str) -> ExportRecord | None:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        if not token or any(character not in alphabet for character in token):
            return None
        with self._lock:
            self._cleanup_locked(time.time())
            record = self._records.get(token)
            if record is None:
                return None
            path = self._path(token)
            try:
                content = path.read_bytes()
            except FileNotFoundError:
                self._records.pop(token, None)
                return None
            return ExportRecord(
                record.token,
                record.filename,
                content,
                record.conversation,
                record.expires_at,
            )

    def _cleanup_locked(self, now: float) -> None:
        expired = [
            token
            for token, record in self._records.items()
            if record.expires_at <= now
        ]
        for token in expired:
            self._records.pop(token, None)
            self._path(token).unlink(missing_ok=True)

    def _path(self, token: str) -> Path:
        return self.directory / f"{token}.md"


class ExportCoordinator:
    def __init__(self, settings: ServiceSettings) -> None:
        settings.validate()
        self.settings = settings
        self.store = ExportStore(
            settings.export_dir,
            settings.download_ttl_seconds,
            settings.max_output_bytes,
        )
        self.limiter = SlidingWindowLimiter(settings.exports_per_minute)
        self.browser_slots = threading.BoundedSemaphore(settings.browser_concurrency)

    def export(self, url: str, client_key: str = "anonymous") -> ExportRecord:
        shared = parse_shared_url(url)
        self.limiter.check(client_key or "anonymous")
        try:
            conversation = extract_http(shared, self.settings.timeout_seconds)
        except (RetrievalError, ValueError) as http_error:
            acquired = self.browser_slots.acquire(timeout=self.settings.timeout_seconds)
            if not acquired:
                raise RuntimeError("Browser export capacity is busy; retry later") from http_error
            try:
                conversation = extract_browser(
                    shared,
                    self.settings.timeout_seconds,
                    headed=False,
                )
            except BrowserExtractionError as browser_error:
                raise RuntimeError(
                    f"Structured retrieval failed ({http_error}); browser fallback failed "
                    f"({browser_error})"
                ) from browser_error
            finally:
                self.browser_slots.release()
        return self.store.create(conversation)
