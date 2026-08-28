from __future__ import annotations

import hashlib
import json
import re
from html import unescape
from typing import Any, Iterable

from .devalue import DevalueError, unflatten
from .models import Artifact, Conversation, Message
from .urls import SharedUrl


class ProviderParseError(ValueError):
    pass


ENQUEUE_RE = re.compile(
    r"streamController\.enqueue\((?P<argument>\"(?:\\.|[^\"\\])*\")\)",
    re.DOTALL,
)


def parse_chatgpt_html(html: str, shared: SharedUrl) -> Conversation:
    errors: list[str] = []
    for match in ENQUEUE_RE.finditer(html):
        try:
            chunk = json.loads(match.group("argument"))
            if "linear_conversation" not in chunk:
                continue
            flattened = json.loads(chunk.strip())
            payload_reference = _devalue_object_with_key(flattened, "linear_conversation")
            if payload_reference is None:
                continue
            hydrated = unflatten(flattened, root_reference=payload_reference)
            payload = hydrated if isinstance(hydrated, dict) else None
            if payload is None:
                continue
            return normalize_chatgpt(payload, shared, extraction_method="chatgpt-page-state")
        except (json.JSONDecodeError, DevalueError, ProviderParseError, TypeError) as exc:
            errors.append(str(exc))
    detail = f" ({errors[-1]})" if errors else ""
    raise ProviderParseError(f"ChatGPT structured conversation data was not found{detail}")


def normalize_chatgpt(
    payload: dict[str, Any], shared: SharedUrl, extraction_method: str
) -> Conversation:
    raw_messages = payload.get("linear_conversation")
    if not isinstance(raw_messages, list):
        raise ProviderParseError("ChatGPT payload has no linear conversation list")

    messages: list[Message] = []
    seen: set[str] = set()
    for index, raw_item in enumerate(raw_messages):
        if not isinstance(raw_item, dict):
            continue
        raw_message = raw_item.get("message")
        if not isinstance(raw_message, dict):
            raw_message = raw_item
        author = raw_message.get("author")
        role = author.get("role") if isinstance(author, dict) else raw_message.get("role")
        if role not in {"user", "assistant"}:
            continue
        markdown, artifacts = _chatgpt_content(raw_message.get("content"))
        markdown = markdown.strip()
        if not markdown and not artifacts:
            continue
        message_id = str(raw_message.get("id") or raw_item.get("id") or f"message-{index}")
        dedupe_key = message_id if message_id else _fingerprint(role, markdown)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        messages.append(Message(message_id, role, markdown, artifacts))

    title = _first_text(payload, "title", "pageTitle", "og_title", "ogTitle")
    if not title:
        title = "ChatGPT Shared Conversation"
    conversation = Conversation(
        provider="chatgpt",
        share_id=shared.share_id,
        title=title,
        source_url=shared.normalized,
        messages=messages,
        extraction_method=extraction_method,
    )
    conversation.validate()
    return conversation


def normalize_claude(
    payload: dict[str, Any], shared: SharedUrl, extraction_method: str
) -> Conversation:
    raw_messages = payload.get("chat_messages") or payload.get("messages")
    if not isinstance(raw_messages, list):
        raise ProviderParseError("Claude snapshot has no chat_messages list")

    messages: list[Message] = []
    seen: set[str] = set()
    for index, raw_message in enumerate(raw_messages):
        if not isinstance(raw_message, dict):
            continue
        sender = raw_message.get("sender") or raw_message.get("role")
        role = {"human": "user", "user": "user", "assistant": "assistant"}.get(str(sender))
        if role is None:
            continue
        markdown, artifacts = _claude_content(raw_message)
        markdown = markdown.strip()
        if not markdown and not artifacts:
            continue
        message_id = str(raw_message.get("uuid") or raw_message.get("id") or f"message-{index}")
        dedupe_key = message_id if message_id else _fingerprint(role, markdown)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        messages.append(Message(message_id, role, markdown, artifacts))

    title = _first_text(payload, "name", "title", "conversation_name")
    if not title:
        title = "Claude Shared Conversation"
    conversation = Conversation(
        provider="claude",
        share_id=shared.share_id,
        title=title,
        source_url=shared.normalized,
        messages=messages,
        extraction_method=extraction_method,
    )
    conversation.validate()
    return conversation


def _chatgpt_content(content: Any) -> tuple[str, list[Artifact]]:
    if isinstance(content, str):
        return content, []
    if not isinstance(content, dict):
        return _render_generic(content), []
    parts = content.get("parts")
    values = parts if isinstance(parts, list) else [content]
    rendered: list[str] = []
    artifacts: list[Artifact] = []
    for part in values:
        artifact = _artifact_from_block(part)
        if artifact:
            artifacts.append(artifact)
        else:
            text = _render_generic(part)
            if text:
                rendered.append(text)
    return "\n\n".join(rendered), artifacts


def _claude_content(message: dict[str, Any]) -> tuple[str, list[Artifact]]:
    content = message.get("content")
    blocks = content if isinstance(content, list) else []
    rendered: list[str] = []
    artifacts: list[Artifact] = []
    for block in blocks:
        if not isinstance(block, dict):
            text = _render_generic(block)
            if text:
                rendered.append(text)
            continue
        block_type = str(block.get("type") or "").lower()
        if block_type in {"thinking", "redacted_thinking", "tool_result"}:
            continue
        artifact = _artifact_from_block(block)
        if artifact:
            artifacts.append(artifact)
            continue
        text = _render_generic(block)
        if text:
            rendered.append(text)
    if not rendered and isinstance(message.get("text"), str):
        rendered.append(message["text"])
    rendered.extend(_attachment_references(message))
    return "\n\n".join(rendered), artifacts


def _artifact_from_block(block: Any) -> Artifact | None:
    if not isinstance(block, dict):
        return None
    block_type = str(block.get("type") or block.get("content_type") or "").lower()
    name = str(block.get("name") or "").lower()
    is_artifact = "artifact" in block_type or "artifact" in name or block_type in {"canvas", "code"}
    if not is_artifact:
        return None
    source = block.get("input") if isinstance(block.get("input"), dict) else block
    content = source.get("content") or source.get("text") or source.get("code")
    if not isinstance(content, str) or not content.strip():
        return None
    title = str(source.get("title") or source.get("name") or "Untitled artifact")
    kind = str(source.get("type") or source.get("language") or block_type or "artifact")
    artifact_id = str(source.get("id") or block.get("id") or _fingerprint(title, content)[:16])
    if kind.lower() in {"code", "python", "javascript", "typescript", "html", "css", "json"}:
        language = "" if kind.lower() == "code" else kind.lower()
        markdown = f"```{language}\n{content.rstrip()}\n```"
    else:
        markdown = content.strip()
    return Artifact(artifact_id, title, kind, markdown)


def _render_generic(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n\n".join(filter(None, (_render_generic(item) for item in value)))
    if not isinstance(value, dict):
        return ""

    value_type = str(value.get("type") or value.get("content_type") or "").lower()
    if value_type in {"thinking", "redacted_thinking", "tool_result", "tool_use"}:
        return ""
    if value_type in {"image", "image_asset_pointer", "image_url"}:
        url = _first_text(value, "url", "image_url", "asset_pointer")
        alt = _first_text(value, "alt", "name", "filename") or "image"
        return f"![{alt}]({url})" if url and url.startswith(("http://", "https://")) else f"[Image: {alt}]"
    if value_type in {"code", "code_block"}:
        code = _first_text(value, "code", "text", "content")
        language = _first_text(value, "language")
        return f"```{language}\n{code.rstrip()}\n```" if code else ""

    for key in ("text", "markdown", "value"):
        if isinstance(value.get(key), str):
            return value[key].strip()
    for key in ("parts", "content", "items"):
        nested = value.get(key)
        if isinstance(nested, (list, dict, str)):
            rendered = _render_generic(nested)
            if rendered:
                return rendered
    filename = _first_text(value, "filename", "file_name", "name")
    return f"[Attachment: {filename}]" if filename else ""


def _attachment_references(message: dict[str, Any]) -> list[str]:
    references: list[str] = []
    for key in ("attachments", "files"):
        items = message.get(key)
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            name = _first_text(item, "file_name", "filename", "name")
            if name:
                reference = f"[Attachment: {name}]"
                if reference not in references:
                    references.append(reference)
    return references


def _devalue_object_with_key(values: Any, key: str) -> int | None:
    if not isinstance(values, list):
        return None
    try:
        key_reference = values.index(key)
    except ValueError:
        return None
    encoded_key = f"_{key_reference}"
    for index, value in enumerate(values):
        if isinstance(value, dict) and encoded_key in value:
            return index
    return None


def _first_text(mapping: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, str) and value.strip():
            return unescape(value.strip())
    return ""


def _fingerprint(*values: str) -> str:
    return hashlib.sha256("\x1f".join(values).encode("utf-8")).hexdigest()


def merge_dom_messages(items: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Deduplicate top-to-bottom browser snapshots without reordering them."""

    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in items:
        role = item.get("role", "")
        text = re.sub(r"\s+", " ", item.get("text", "")).strip()
        key = item.get("id") or _fingerprint(role, text)
        if role not in {"user", "assistant"} or not text or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
