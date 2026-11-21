import tempfile
import time
import unittest
from pathlib import Path

from tinyagent.catalog import build_tool_registry
from tinyagent.providers import MockSearchProvider, MockWeatherProvider
from tinyagent.tools import ToolDefinition, ToolRegistry


class CatalogTests(unittest.TestCase):
    def test_nine_tools_have_independent_schemas(self):
        schemas = build_tool_registry().schemas()
        self.assertEqual({item["function"]["name"] for item in schemas}, {"bash", "read", "edit", "write", "calculator", "search", "read_docs", "todo", "weather"})
        self.assertTrue(all(item["function"]["parameters"]["type"] == "object" for item in schemas))

    def test_providers_and_calculator_are_deterministic(self):
        registry = build_tool_registry(search_provider=MockSearchProvider(), weather_provider=MockWeatherProvider())
        self.assertIn("Mock result", registry.execute("search", {"query": "tinyagent"}))
        self.assertIn('"value": 14', registry.execute("calculator", {"expression": "2 + 3 * 4"}))
        self.assertIn('"condition": "unknown"', registry.execute("weather", {"location": "Shanghai"}))

    def test_read_docs_is_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.md").write_text("hello", encoding="utf-8")
            registry = build_tool_registry(docs_root=root)
            self.assertIn("hello", registry.execute("read_docs", {"path": "guide.md"}))
            self.assertIn("must stay inside", registry.execute("read_docs", {"path": "../secret"}))

    def test_parallel_calls_preserve_order(self):
        registry = ToolRegistry()
        def slow(value, delay):
            time.sleep(delay)
            return value
        schema = {"type": "object", "properties": {"value": {"type": "string"}, "delay": {"type": "number"}}, "required": ["value", "delay"]}
        registry.register(ToolDefinition("slow", "slow", schema, slow))
        started = time.perf_counter()
        results = registry.execute_many([("slow", {"value": "first", "delay": 0.08}), ("slow", {"value": "second", "delay": 0.01})])
        elapsed = time.perf_counter() - started
        self.assertLess(elapsed, 0.15)
        self.assertIn("first", results[0])
        self.assertIn("second", results[1])


if __name__ == "__main__":
    unittest.main()

