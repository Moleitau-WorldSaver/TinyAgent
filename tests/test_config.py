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


if __name__ == "__main__":
    unittest.main()


