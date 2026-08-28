from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit


SHARE_ID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
PROVIDER_HOSTS = {"chatgpt.com": "chatgpt", "claude.ai": "claude"}


class UrlValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class SharedUrl:
    provider: str
    share_id: str
    normalized: str


def parse_shared_url(value: str) -> SharedUrl:
    try:
        parsed = urlsplit(value.strip())
    except ValueError as exc:
        raise UrlValidationError(f"Invalid shared URL: {exc}") from exc

    host = (parsed.hostname or "").lower()
    provider = PROVIDER_HOSTS.get(host)
    if parsed.scheme.lower() != "https" or provider is None:
        raise UrlValidationError(
            "URL must use https://chatgpt.com/share/<uuid> or "
            "https://claude.ai/share/<uuid>"
        )
    if parsed.username or parsed.password or parsed.port:
        raise UrlValidationError("Credentials and custom ports are not allowed")

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 2 or parts[0] != "share" or not SHARE_ID_RE.fullmatch(parts[1]):
        raise UrlValidationError("Shared URL path must be /share/<uuid>")

    normalized = urlunsplit(("https", host, f"/share/{parts[1].lower()}", "", ""))
    return SharedUrl(provider=provider, share_id=parts[1].lower(), normalized=normalized)


def validate_redirect(original: SharedUrl, redirected_url: str) -> None:
    redirected = parse_shared_url(redirected_url)
    if redirected.provider != original.provider or redirected.share_id != original.share_id:
        raise UrlValidationError("The shared URL redirected to a different conversation")
