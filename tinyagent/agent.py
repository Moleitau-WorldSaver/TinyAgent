"""The synchronous model/tool decision loop."""

import copy
import json
from typing import Protocol

from .models import ModelResponse, ToolCall
from .tools import ToolRegistry


class Model(Protocol):
    def complete(self, messages: list[dict], tools: list[dict]) -> ModelResponse: ...


class AgentLimitError(RuntimeError):
    """Raised when the model does not produce a final answer in time."""


class AgentLoop:
    def __init__(self, model: Model, tools: ToolRegistry, max_rounds: int = 50) -> None:
        if max_rounds <= 0:
            raise ValueError("max_rounds must be greater than zero")
        self.model = model
        self.tools = tools
        self.max_rounds = max_rounds

    def run(self, user_input: str) -> str:
        messages: list[dict] = [{"role": "user", "content": user_input}]
        for _ in range(self.max_rounds):
            response = self.model.complete(copy.deepcopy(messages), self.tools.schemas())
            calls = _unique_calls(response.tool_calls)
            assistant_message: dict = {"role": "assistant", "content": response.content}
            if calls:
                assistant_message["tool_calls"] = [{"id": call.id, "type": "function", "function": {"name": call.name, "arguments": json.dumps(call.arguments, ensure_ascii=False)}} for call in calls]
            messages.append(assistant_message)
            if not calls:
                return response.content or ""
            results = self.tools.execute_many([(call.name, call.arguments) for call in calls])
            for call, result in zip(calls, results):
                messages.append({"role": "tool", "tool_call_id": call.id, "name": call.name, "content": result})
        raise AgentLimitError(f"Agent stopped after reaching the {self.max_rounds}-round limit.")


def _unique_calls(calls: list[ToolCall]) -> list[ToolCall]:
    unique: list[ToolCall] = []
    seen_ids: set[str] = set()
    for call in calls:
        if call.id not in seen_ids:
            seen_ids.add(call.id)
            unique.append(call)
    return unique

