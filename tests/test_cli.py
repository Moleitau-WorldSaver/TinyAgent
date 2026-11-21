import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class CliEntryPointTests(unittest.TestCase):
    def test_module_entry_point_reports_missing_configuration(self):
        repository = Path(__file__).resolve().parents[1]
        environment = os.environ.copy()
        environment.pop("TINYAGENT_API_KEY", None)
        environment.pop("TINYAGENT_MODEL", None)
        environment["PYTHONPATH"] = str(repository)

        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-m", "tinyagent.cli", "hello"],
                cwd=directory,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("Configuration error", result.stdout)


if __name__ == "__main__":
    unittest.main()
