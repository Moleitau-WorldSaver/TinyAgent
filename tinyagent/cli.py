"""Command-line entry point and a deterministic example tool."""

import argparse

from .agent import AgentLoop, AgentLimitError
from .config import ConfigError, load_config
from .model import ModelClient
from .tools import ToolDefinition, ToolRegistry


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a minimal TinyAgent loop.")
    parser.add_argument("message", nargs="?", help="Question to send to the model")
    args = parser.parse_args()
    try:
        config = load_config()
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return 2
    registry = ToolRegistry()
    registry.register(
        ToolDefinition(
            name="echo",
            description="Return the supplied text.",
            parameters={
                "type": "object",
                "properties": {"text": {"type": "string", "description": "Text to return"}},
                "required": ["text"],
                "additionalProperties": False,
            },
            handler=lambda text: text,
        )
    )
    message = args.message or input("You: ")
    try:
        answer = AgentLoop(ModelClient(config), registry).run(message)
    except (AgentLimitError, OSError, ValueError, KeyError) as exc:
        print(f"Agent error: {exc}")
        return 1
    print(answer)
    return 0


