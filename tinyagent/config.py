"""Local, ignored configuration for a model API."""

from dataclasses import dataclass
from pathlib import Path
import os
import tomllib


class ConfigError(RuntimeError):
    """Raised when the local model configuration is missing or invalid."""


@dataclass(frozen=True)
class Config:
    api_key: str
    base_url: str
    model: str
    timeout_seconds: int = 60


def load_config(path: str | Path = ".tinyagent.toml") -> Config:
    """Load configuration from TOML, with environment variables as overrides."""
    config_path = Path(path)
    values: dict[str, object] = {}
    if config_path.exists():
        with config_path.open("rb") as handle:
            values = tomllib.load(handle)

    api_key = os.getenv("TINYAGENT_API_KEY", str(values.get("api_key", "")))
    base_url = os.getenv("TINYAGENT_BASE_URL", str(values.get("base_url", "https://api.openai.com/v1")))
    model = os.getenv("TINYAGENT_MODEL", str(values.get("model", "")))
    timeout_value = os.getenv("TINYAGENT_TIMEOUT_SECONDS", str(values.get("timeout_seconds", 60)))

    if not api_key or api_key == "your-api-key":
        raise ConfigError("API key is missing. Copy config.example.toml to .tinyagent.toml and set api_key.")
    if not model:
        raise ConfigError("Model is missing. Set model in .tinyagent.toml or TINYAGENT_MODEL.")
    try:
        timeout_seconds = int(timeout_value)
    except ValueError as exc:
        raise ConfigError("timeout_seconds must be an integer.") from exc
    if timeout_seconds <= 0:
        raise ConfigError("timeout_seconds must be greater than zero.")

    return Config(api_key=api_key, base_url=base_url.rstrip("/"), model=model, timeout_seconds=timeout_seconds)


