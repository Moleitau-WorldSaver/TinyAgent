"""The stable Issue-002 tool catalog and offline tool implementations."""

import ast
from pathlib import Path
from typing import Any

from .providers import MockSearchProvider, MockWeatherProvider, SearchProvider, WeatherProvider
from .tools import ToolDefinition, ToolRegistry


def build_tool_registry(
    *,
    docs_root: str | Path = "docs",
    search_provider: SearchProvider | None = None,
    weather_provider: WeatherProvider | None = None,
) -> ToolRegistry:
    """Create the nine tools promised by Issue-002 without live side effects."""
    docs_path = Path(docs_root).resolve()
    search = search_provider or MockSearchProvider()
    weather = weather_provider or MockWeatherProvider()
    registry = ToolRegistry()
    registry.register(_definition("bash", "Describe a shell command without executing it.", {"command": {"type": "string"}}, ["command"], lambda command: {"simulated": True, "command": command}))
    registry.register(_definition("read", "Describe a file read without changing files.", {"path": {"type": "string"}}, ["path"], lambda path: {"simulated": True, "path": path}))
    registry.register(_definition("edit", "Describe a file edit without changing files.", {"path": {"type": "string"}, "content": {"type": "string"}}, ["path", "content"], lambda path, content: {"simulated": True, "path": path, "content": content}))
    registry.register(_definition("write", "Describe a file write without changing files.", {"path": {"type": "string"}, "content": {"type": "string"}}, ["path", "content"], lambda path, content: {"simulated": True, "path": path, "content": content}))
    registry.register(_definition("calculator", "Evaluate a basic arithmetic expression deterministically.", {"expression": {"type": "string"}}, ["expression"], _calculate))
    registry.register(_definition("search", "Search using the configured search provider.", {"query": {"type": "string"}}, ["query"], search.search))
    registry.register(_definition("read_docs", "Read a UTF-8 file beneath the docs directory.", {"path": {"type": "string"}}, ["path"], lambda path: _read_doc(docs_path, path)))
    registry.register(_definition("todo", "Return a non-persistent todo acknowledgement.", {"action": {"type": "string"}, "item": {"type": "string"}}, ["action", "item"], lambda action, item: {"simulated": True, "action": action, "item": item}))
    registry.register(_definition("weather", "Get weather using the configured weather provider.", {"location": {"type": "string"}}, ["location"], weather.forecast))
    return registry


def _definition(name: str, description: str, properties: dict[str, dict[str, str]], required: list[str], handler: Any) -> ToolDefinition:
    return ToolDefinition(name=name, description=description, parameters={"type": "object", "properties": properties, "required": required, "additionalProperties": False}, handler=handler)


def _read_doc(root: Path, relative_path: str) -> dict[str, str]:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("read_docs path must stay inside docs/") from exc
    if not candidate.is_file():
        raise FileNotFoundError(f"Document not found: {relative_path}")
    return {"path": relative_path, "content": candidate.read_text(encoding="utf-8")}


def _calculate(expression: str) -> dict[str, int | float]:
    tree = ast.parse(expression, mode="eval")
    allowed = (ast.Expression, ast.Constant, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.USub, ast.UAdd)
    if any(not isinstance(node, allowed) for node in ast.walk(tree)) or any(isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)) for node in ast.walk(tree)):
        raise ValueError("calculator accepts arithmetic numbers and operators only")
    value = eval(compile(tree, "<calculator>", "eval"), {"__builtins__": {}}, {})
    if not isinstance(value, (int, float)):
        raise ValueError("calculator result must be numeric")
    return {"value": value}

