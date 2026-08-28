from __future__ import annotations

import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from .models import Conversation


WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def render_markdown(conversation: Conversation, generated_at: datetime | None = None) -> str:
    conversation.validate()
    timestamp = generated_at or datetime.now(timezone.utc)
    lines = [
        "---",
        f"provider: {_yaml_string(conversation.provider)}",
        f"title: {_yaml_string(conversation.title)}",
        f"source_url: {_yaml_string(conversation.source_url)}",
        f"generated_at: {_yaml_string(timestamp.isoformat(timespec='seconds'))}",
        f"extraction_method: {_yaml_string(conversation.extraction_method)}",
        f"completeness: {_yaml_string(conversation.completeness)}",
    ]
    if conversation.warnings:
        lines.append("warnings:")
        lines.extend(f"  - {_yaml_string(warning)}" for warning in conversation.warnings)
    else:
        lines.append("warnings: []")
    title = _heading_text(conversation.title)
    lines.extend(["---", "", f"# {title}", ""])

    if conversation.completeness != "verified" or conversation.warnings:
        warning = " ".join(conversation.warnings) or "This export could not be verified as complete."
        lines.extend([f"> [!WARNING] {warning}", ""])

    for message in conversation.messages:
        heading = "User" if message.role == "user" else "Assistant"
        lines.extend([f"## {heading}", ""])
        if message.markdown:
            lines.extend([message.markdown.strip(), ""])
        for artifact in message.artifacts:
            lines.extend(
                [
                    f"### Artifact: {_heading_text(artifact.title)}",
                    "",
                    f"Type: `{artifact.kind}`",
                    "",
                    artifact.markdown.strip(),
                    "",
                ]
            )
        lines.extend(["---", ""])
    return "\n".join(lines).rstrip() + "\n"


def default_output_path(conversation: Conversation, directory: Path) -> Path:
    title = slugify(conversation.title) or "shared-conversation"
    base = f"{conversation.provider}-{title}-{conversation.share_id[:8]}"
    candidate = directory / f"{base}.md"
    suffix = 2
    while candidate.exists():
        candidate = directory / f"{base}-{suffix}.md"
        suffix += 1
    return candidate


def write_markdown(path: Path, content: str, force: bool = False) -> None:
    path = path.expanduser().resolve()
    if path.exists() and not force:
        raise FileExistsError(f"Output already exists: {path}")
    if path.exists() and path.is_dir():
        raise IsADirectoryError(f"Output is a directory: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-. ")[:80].rstrip("-. ")
    if slug.upper() in WINDOWS_RESERVED:
        slug = f"conversation-{slug}"
    return slug


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _heading_text(value: str) -> str:
    return " ".join(value.splitlines()).strip() or "Untitled"
