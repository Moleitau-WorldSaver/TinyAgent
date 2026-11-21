"""Registered tool definitions, validation, and safe execution."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import json
from typing import Any, Callable


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, definition: ToolDefinition) -> None:
        if not definition.name or definition.name in self._tools:
            raise ValueError(f"Tool name is empty or already registered: {definition.name!r}")
        self._tools[definition.name] = definition

    def schemas(self) -> list[dict[str, Any]]:
        return [
            {"type": "function", "function": {"name": definition.name, "description": definition.description, "parameters": definition.parameters}}
            for definition in self._tools.values()
        ]

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        definition = self._tools.get(name)
        if definition is None:
            return json.dumps({"error": f"Unknown tool: {name}"})
        validation_error = _validate_arguments(definition.parameters, arguments)
        if validation_error:
            return json.dumps({"error": validation_error})
        try:
            result = definition.handler(**arguments)
        except Exception as exc:  # Tool errors are data for the next model turn.
            return json.dumps({"error": f"Tool {name} failed: {exc}"})
        return _serialize_result(result)

    def execute_many(self, calls: list[tuple[str, dict[str, Any]]]) -> list[str]:
        """Execute calls concurrently and return results in the input order."""
        if not calls:
            return []
        with ThreadPoolExecutor(max_workers=len(calls)) as executor:
            futures = [executor.submit(self.execute, name, arguments) for name, arguments in calls]
            return [future.result() for future in futures]


def _serialize_result(result: Any) -> str:
    try:
        return json.dumps(result, ensure_ascii=False)
    except TypeError:
        return json.dumps({"result": str(result)}, ensure_ascii=False)


def _validate_arguments(schema: dict[str, Any], arguments: Any) -> str | None:
    if not isinstance(arguments, dict):
        return "Tool arguments must be a JSON object."
    missing = [name for name in schema.get("required", []) if name not in arguments]
    if missing:
        return f"Missing required argument(s): {', '.join(missing)}"
    properties = schema.get("properties", {})
    unknown = [name for name in arguments if name not in properties]
    if unknown:
        return f"Unknown argument(s): {', '.join(unknown)}"
    for name, value in arguments.items():
        expected = properties[name].get("type")
        if expected and not _matches_type(value, expected):
            return f"Argument {name!r} must be {expected}."
    return None


def _matches_type(value: Any, expected: str) -> bool:
    return {"string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool), "number": isinstance(value, (int, float)) and not isinstance(value, bool), "boolean": isinstance(value, bool), "object": isinstance(value, dict), "array": isinstance(value, list), "null": value is None}.get(expected, True)

