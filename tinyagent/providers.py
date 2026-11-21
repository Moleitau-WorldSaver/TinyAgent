"""Replaceable deterministic providers for search and weather tools."""

from dataclasses import dataclass
from typing import Protocol


class SearchProvider(Protocol):
    def search(self, query: str) -> list[dict[str, str]]: ...


class WeatherProvider(Protocol):
    def forecast(self, location: str) -> dict[str, str]: ...


@dataclass(frozen=True)
class MockSearchProvider:
    """Offline provider used by tests and the default catalog."""

    def search(self, query: str) -> list[dict[str, str]]:
        return [{"title": f"Mock result for {query}", "snippet": "No live search provider configured."}]


@dataclass(frozen=True)
class MockWeatherProvider:
    """Offline provider used by tests and the default catalog."""

    def forecast(self, location: str) -> dict[str, str]:
        return {"location": location, "condition": "unknown", "note": "No live weather provider configured."}

