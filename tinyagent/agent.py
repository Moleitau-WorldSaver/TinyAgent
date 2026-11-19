"""The synchronous model/tool decision loop."""

from dataclasses import asdict
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
            response = self.model.complete(messages, self.tools.schemas())
            assistant_message: dict = {"role": "assistant", "content": response.content}
            if response.tool_calls:
                assistant_message["tool_calls"] = [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {"name": call.name, "arguments": _json_arguments(call.arguments)},
                    }
                    for call in response.tool_calls
                ]
            messages.append(assistant_message)
            if not response.tool_calls:
                return response.content or ""
            for call in response.tool_calls:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "name": call.name,
                        "content": self.tools.execute(call.name, call.arguments),
                    }
                )
        raise AgentLimitError(f"Agent stopped after reaching the {self.max_rounds}-round limit.")


def _json_arguments(arguments: dict) -> str:
    import json

    return json.dumps(arguments, ensure_ascii=False)


