"""Stable response types shared by the model adapter and agent loop."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ModelResponse:
    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    reasoning_content: str | None = None


