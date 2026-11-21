import os
from pathlib import Path
import tempfile
import unittest

from tinyagent.config import ConfigError, load_config


class ConfigTests(unittest.TestCase):
    def test_missing_key_is_clear(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ConfigError, "API key is missing"):
                load_config(Path(directory) / "missing.toml")

    def test_toml_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text('api_key = "test-key"\nmodel = "test-model"\ntimeout_seconds = 10\n')
            old_key = os.environ.pop("TINYAGENT_API_KEY", None)
            try:
                config = load_config(path)
            finally:
                if old_key is not None:
                    os.environ["TINYAGENT_API_KEY"] = old_key
            self.assertEqual(config.api_key, "test-key")
            self.assertEqual(config.model, "test-model")
            self.assertEqual(config.timeout_seconds, 10)
            self.assertEqual(config.provider, "openai_compatible")

    def test_deepseek_provider_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text(
                'provider = "deepseek"\napi_key = "test-key"\nmodel = "deepseek-chat"\n',
                encoding="utf-8",
            )
            config = load_config(path)
            self.assertEqual(config.provider, "deepseek")

    def test_unknown_provider_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.toml"
            path.write_text('provider = "unknown"\napi_key = "test-key"\nmodel = "test-model"\n', encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "provider must be"):
                load_config(path)


if __name__ == "__main__":
    unittest.main()


