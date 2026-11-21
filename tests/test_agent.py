import unittest

from tinyagent.agent import AgentLimitError, AgentLoop
from tinyagent.models import ModelResponse, ToolCall
from tinyagent.tools import ToolDefinition, ToolRegistry


class FakeModel:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def complete(self, messages, tools):
        self.calls.append((messages, tools))
        return self.responses.pop(0)


def registry():
    tools = ToolRegistry()
    tools.register(
        ToolDefinition(
            name="add",
            description="Add two integers.",
            parameters={
                "type": "object",
                "properties": {"left": {"type": "integer"}, "right": {"type": "integer"}},
                "required": ["left", "right"],
                "additionalProperties": False,
            },
            handler=lambda left, right: left + right,
        )
    )
    return tools


class AgentLoopTests(unittest.TestCase):
    def test_direct_text_response(self):
        model = FakeModel([ModelResponse(content="hello")])
        self.assertEqual(AgentLoop(model, registry()).run("hi"), "hello")
        self.assertEqual(len(model.calls), 1)

    def test_tool_result_is_returned_to_model(self):
        model = FakeModel(
            [
                ModelResponse(tool_calls=[ToolCall("call-1", "add", {"left": 2, "right": 3})]),
                ModelResponse(content="The answer is five."),
            ]
        )
        self.assertEqual(AgentLoop(model, registry()).run("calculate"), "The answer is five.")
        self.assertEqual(model.calls[1][0][-1]["role"], "tool")
        self.assertIn("5", model.calls[1][0][-1]["content"])

    def test_unknown_tool_and_bad_arguments_are_model_visible(self):
        model = FakeModel(
            [
                ModelResponse(
                    tool_calls=[
                        ToolCall("unknown", "missing", {}),
                        ToolCall("bad", "add", {"left": "two", "right": 3}),
                    ]
                ),
                ModelResponse(content="recovered"),
            ]
        )
        self.assertEqual(AgentLoop(model, registry()).run("calculate"), "recovered")
        results = [message["content"] for message in model.calls[1][0] if message["role"] == "tool"]
        self.assertTrue(any("Unknown tool" in result for result in results))
        self.assertTrue(any("must be integer" in result for result in results))

    def test_round_limit(self):
        model = FakeModel([ModelResponse(tool_calls=[ToolCall("call", "add", {"left": 1, "right": 1})])] * 2)
        with self.assertRaises(AgentLimitError):
            AgentLoop(model, registry(), max_rounds=2).run("loop")


if __name__ == "__main__":
    unittest.main()


