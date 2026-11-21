"""TinyAgent's model, tool catalog, and execution loop."""

from .agent import AgentLoop, AgentLimitError
from .catalog import build_tool_registry
from .config import Config, ConfigError, load_config
from .models import ModelResponse, ToolCall
from .providers import MockSearchProvider, MockWeatherProvider
from .tools import ToolDefinition, ToolRegistry

__all__ = [
    "AgentLimitError",
    "AgentLoop",
    "Config",
    "ConfigError",
    "MockSearchProvider",
    "MockWeatherProvider",
    "ModelResponse",
    "ToolCall",
    "ToolDefinition",
    "ToolRegistry",
    "build_tool_registry",
    "load_config",
]

