"""OpenAI-compatible HTTP model adapters using only the standard library."""

import json
from urllib import request

from .config import Config
from .models import ModelResponse, ToolCall


class ModelClient:
    def __init__(self, config: Config) -> None:
        self.config = config

    def complete(self, messages: list[dict], tools: list[dict]) -> ModelResponse:
        body = self._request_body(messages, tools)
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        http_request = request.Request(
            f"{self.config.base_url}/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {self.config.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(http_request, timeout=self.config.timeout_seconds) as response:
            response_body = json.loads(response.read().decode("utf-8"))
        return self._parse_response(response_body)

    def _request_body(self, messages: list[dict], tools: list[dict]) -> dict:
        return {"model": self.config.model, "messages": messages, "tools": tools}

    def _parse_response(self, body: dict) -> ModelResponse:
        message = body["choices"][0]["message"]
        calls = [
            ToolCall(
                id=call.get("id", f"call-{index}"),
                name=call["function"]["name"],
                arguments=_parse_arguments(call["function"].get("arguments", "{}")),
            )
            for index, call in enumerate(message.get("tool_calls", []), start=1)
        ]
        return ModelResponse(
            content=message.get("content"),
            tool_calls=calls,
            reasoning_content=message.get("reasoning_content"),
        )


class DeepSeekModelClient(ModelClient):
    """DeepSeek Chat Completions adapter with thinking enabled."""

    def _request_body(self, messages: list[dict], tools: list[dict]) -> dict:
        return {
            "model": self.config.model,
            "messages": messages,
            "tools": tools,
            "thinking": {"type": "enabled"},
        }


def _parse_arguments(raw: str | dict) -> dict:
    if isinstance(raw, dict):
        return raw
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Model tool arguments must decode to a JSON object.")
    return parsed


