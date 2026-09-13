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

    return _normalize_chatgpt_messages(
        payload,
        raw_messages,
        shared,
        extraction_method,
    )


def normalize_chatgpt_snapshot(
    payload: dict[str, Any], shared: SharedUrl, extraction_method: str
) -> Conversation:
    """Normalize either ChatGPT's linear or graph-shaped public snapshot."""

    if isinstance(payload.get("linear_conversation"), list):
        return normalize_chatgpt(payload, shared, extraction_method)

    mapping = payload.get("mapping")
    if not isinstance(mapping, dict) or not mapping:
        raise ProviderParseError("ChatGPT snapshot has no conversation mapping")

    ordered, ambiguous = _active_chatgpt_path(payload, mapping)
    conversation = _normalize_chatgpt_messages(
        payload,
        ordered,
        shared,
        extraction_method,
    )
    if ambiguous:
        conversation.completeness = "best-effort"
        conversation.warnings.append(
            "The ChatGPT snapshot did not identify one active branch. The most recent "
            "complete branch was exported, but branch selection could not be verified."
        )
    conversation.validate()
    return conversation


def normalize_snapshot(
    payload: dict[str, Any], shared: SharedUrl, extraction_method: str
) -> Conversation:
    """Dispatch a complete provider snapshot supplied by a hosted runtime."""

    explicit_share_id = _first_text(payload, "share_id", "share_uuid")
    if explicit_share_id and explicit_share_id.lower() != shared.share_id.lower():
        raise ProviderParseError("Snapshot share ID does not match the supplied URL")

    if shared.provider == "chatgpt":
        if not any(key in payload for key in ("mapping", "linear_conversation")):
            raise ProviderParseError("Snapshot is not a ChatGPT conversation payload")
        return normalize_chatgpt_snapshot(payload, shared, extraction_method)

    if not any(key in payload for key in ("chat_messages", "messages")):
        raise ProviderParseError("Snapshot is not a Claude conversation payload")
    return normalize_claude(payload, shared, extraction_method)


def _normalize_chatgpt_messages(
    payload: dict[str, Any],
    raw_messages: list[Any],
    shared: SharedUrl,
    extraction_method: str,
) -> Conversation:

    messages: list[Message] = []
    seen: set[str] = set()
    for index, raw_item in enumerate(raw_messages):
        if not isinstance(raw_item, dict):
            continue
        raw_message = raw_item.get("message")
        if not isinstance(raw_message, dict):
            raw_message = raw_item
        metadata = raw_message.get("metadata")
        if isinstance(metadata, dict) and (
            metadata.get("is_visually_hidden_from_conversation")
            or metadata.get("is_user_system_message")
        ):
            continue
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


def _active_chatgpt_path(
    payload: dict[str, Any], mapping: dict[str, Any]
) -> tuple[list[dict[str, Any]], bool]:
    current_node = payload.get("current_node") or payload.get("current_node_id")
    ambiguous = False
    if not isinstance(current_node, str) or current_node not in mapping:
        leaves: list[tuple[float, str]] = []
        for node_id, node in mapping.items():
            if not isinstance(node_id, str) or not isinstance(node, dict):
                continue
            children = node.get("children")
            if isinstance(children, list) and children:
                continue
            raw_message = node.get("message")
            created = raw_message.get("create_time") if isinstance(raw_message, dict) else None
            timestamp = float(created) if isinstance(created, (int, float)) else 0.0
            leaves.append((timestamp, node_id))
        if not leaves:
            raise ProviderParseError("ChatGPT snapshot has no traversable conversation branch")
        leaves.sort(key=lambda item: (item[0], item[1]))
        current_node = leaves[-1][1]
        ambiguous = len(leaves) != 1

    ordered: list[dict[str, Any]] = []
    seen: set[str] = set()
    node_id: str | None = current_node
    while node_id:
        if node_id in seen:
            raise ProviderParseError("ChatGPT snapshot contains a cyclic conversation mapping")
        seen.add(node_id)
        node = mapping.get(node_id)
        if not isinstance(node, dict):
            raise ProviderParseError("ChatGPT snapshot branch references a missing node")
        ordered.append(node)
        parent = node.get("parent")
        node_id = parent if isinstance(parent, str) and parent else None
    ordered.reverse()
    return ordered, ambiguous


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
