"""The synchronous model/tool decision loop."""

import copy
import json
from typing import Protocol

from .models import ModelResponse
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
            assistant_message: dict = {"role": "assistant", "content": response.content}
            if response.tool_calls:
                assistant_message["tool_calls"] = [{"id": call.id, "type": "function", "function": {"name": call.name, "arguments": json.dumps(call.arguments, ensure_ascii=False)}} for call in response.tool_calls]
            messages.append(assistant_message)
            if not response.tool_calls:
                return response.content or ""
            unique_calls = []
            seen_ids: set[str] = set()
            for call in response.tool_calls:
                if call.id in seen_ids:
                    unique_calls.append((call.name, {"__duplicate_call_id__": call.id}))
                else:
                    seen_ids.add(call.id)
                    unique_calls.append((call.name, call.arguments))
            results = self.tools.execute_many(unique_calls)
            for call, result in zip(response.tool_calls, results):
                messages.append({"role": "tool", "tool_call_id": call.id, "name": call.name, "content": result})
        raise AgentLimitError(f"Agent stopped after reaching the {self.max_rounds}-round limit.")

