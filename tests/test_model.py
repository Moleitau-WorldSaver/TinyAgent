import json
import unittest
from unittest.mock import patch

from tinyagent.config import Config
from tinyagent.model import DeepSeekModelClient, ModelClient


class FakeHTTPResponse:
    def __init__(self, body):
        self.body = json.dumps(body).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.body


class ModelClientTests(unittest.TestCase):
    def test_deepseek_payload_and_reasoning_content(self):
        config = Config(
            api_key="test-key",
            base_url="https://api.deepseek.com",
            model="deepseek-chat",
            provider="deepseek",
        )
        response = {
            "choices": [
                {
                    "message": {
                        "content": None,
                        "reasoning_content": "Use calculator",
                        "tool_calls": [
                            {
                                "id": "call-1",
                                "function": {"name": "calculator", "arguments": '{"expression":"2 + 2"}'},
                            }
                        ],
                    }
                }
            ]
        }
        captured = {}

        def fake_urlopen(http_request, timeout):
            captured["payload"] = json.loads(http_request.data.decode("utf-8"))
            captured["authorization"] = http_request.headers["Authorization"]
            captured["timeout"] = timeout
            return FakeHTTPResponse(response)

        with patch("tinyagent.model.request.urlopen", fake_urlopen):
            result = DeepSeekModelClient(config).complete([{"role": "user", "content": "2 + 2?"}], [])

        self.assertEqual(captured["payload"]["thinking"], {"type": "enabled"})
        self.assertEqual(captured["payload"]["model"], "deepseek-chat")
        self.assertEqual(captured["authorization"], "Bearer test-key")
        self.assertEqual(captured["timeout"], 60)
        self.assertEqual(result.reasoning_content, "Use calculator")
        self.assertEqual(result.tool_calls[0].name, "calculator")
        self.assertEqual(result.tool_calls[0].arguments, {"expression": "2 + 2"})

    def test_openai_compatible_payload_does_not_enable_thinking(self):
        config = Config(api_key="test-key", base_url="https://example.test/v1", model="test-model")
        captured = {}

        def fake_urlopen(http_request, timeout):
            captured["payload"] = json.loads(http_request.data.decode("utf-8"))
            return FakeHTTPResponse({"choices": [{"message": {"content": "hello"}}]})

        with patch("tinyagent.model.request.urlopen", fake_urlopen):
            result = ModelClient(config).complete([], [])

        self.assertNotIn("thinking", captured["payload"])
        self.assertEqual(result.content, "hello")

    def test_tool_arguments_must_be_an_object(self):
        config = Config(api_key="test-key", base_url="https://example.test/v1", model="test-model")
        response = {"choices": [{"message": {"tool_calls": [{"function": {"name": "x", "arguments": "[]"}}]}}]}
        with patch("tinyagent.model.request.urlopen", lambda *_args, **_kwargs: FakeHTTPResponse(response)):
            with self.assertRaisesRegex(ValueError, "JSON object"):
                ModelClient(config).complete([], [])


if __name__ == "__main__":
    unittest.main()
