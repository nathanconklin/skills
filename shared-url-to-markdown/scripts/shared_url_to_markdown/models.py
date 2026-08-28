from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Artifact:
    id: str
    title: str
    kind: str
    markdown: str


@dataclass(slots=True)
class Message:
    id: str
    role: str
    markdown: str
    artifacts: list[Artifact] = field(default_factory=list)


@dataclass(slots=True)
class Conversation:
    provider: str
    share_id: str
    title: str
    source_url: str
    messages: list[Message]
    extraction_method: str
    completeness: str = "verified"
    warnings: list[str] = field(default_factory=list)

    def validate(self) -> None:
        if self.provider not in {"chatgpt", "claude"}:
            raise ValueError(f"Unsupported provider: {self.provider}")
        if self.completeness not in {"verified", "best-effort"}:
            raise ValueError(f"Invalid completeness: {self.completeness}")
        if not self.messages:
            raise ValueError("No visible user or assistant messages were extracted")
        for message in self.messages:
            if message.role not in {"user", "assistant"}:
                raise ValueError(f"Invalid message role: {message.role}")
