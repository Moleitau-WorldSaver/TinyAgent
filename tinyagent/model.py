"""OpenAI-compatible HTTP model adapter using only the Python standard library."""

import json
from urllib import request

from .config import Config
from .models import ModelResponse, ToolCall


class ModelClient:
    def __init__(self, config: Config) -> None:
        self.config = config

    def complete(self, messages: list[dict], tools: list[dict]) -> ModelResponse:
        payload = json.dumps({"model": self.config.model, "messages": messages, "tools": tools}).encode()
        http_request = request.Request(
            f"{self.config.base_url}/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(http_request, timeout=self.config.timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
        message = body["choices"][0]["message"]
        calls = [
            ToolCall(
                id=call.get("id", f"call-{index}"),
                name=call["function"]["name"],
                arguments=_parse_arguments(call["function"].get("arguments", "{}")),
            )
            for index, call in enumerate(message.get("tool_calls", []), start=1)
        ]
        return ModelResponse(content=message.get("content"), tool_calls=calls)


def _parse_arguments(raw: str | dict) -> dict:
    if isinstance(raw, dict):
        return raw
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Model tool arguments must decode to a JSON object.")
    return parsed


