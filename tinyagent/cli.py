"""Command-line entry point and the default Issue-002 tool catalog."""

import argparse

from .agent import AgentLoop, AgentLimitError
from .catalog import build_tool_registry
from .config import ConfigError, load_config
from .model import DeepSeekModelClient, ModelClient
from .tools import ToolDefinition


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal TinyAgent loop.")
    parser.add_argument("message", nargs="?", help="Question to send to the model")
    args = parser.parse_args()
    try:
        config = load_config()
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return 2
    registry = build_tool_registry()
    registry.register(ToolDefinition(name="echo", description="Return the supplied text.", parameters={"type": "object", "properties": {"text": {"type": "string", "description": "Text to return"}}, "required": ["text"], "additionalProperties": False}, handler=lambda text: text))
    message = args.message or input("You: ")
    try:
        model = DeepSeekModelClient(config) if config.provider == "deepseek" else ModelClient(config)
        answer = AgentLoop(model, registry).run(message)
    except (AgentLimitError, OSError, ValueError, KeyError) as exc:
        print(f"Agent error: {exc}")
        return 1
    print(answer)
    return 0

