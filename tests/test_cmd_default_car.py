import json
import tempfile
import unittest
from pathlib import Path

import scripts.tesla as tesla


class DefaultCarCommandTests(unittest.TestCase):
    def test_default_car_force_sets_requested_value_without_validation(self):
        with tempfile.TemporaryDirectory() as td:
            defaults_path = Path(td) / "my_tesla.json"

            old = tesla.DEFAULTS_FILE
            try:
                tesla.DEFAULTS_FILE = defaults_path

                class Args:
                    # Simulate argparse Namespace
                    name = "My Test Car"
                    force = True
                    email = None

                tesla.cmd_default_car(Args())

                raw = defaults_path.read_text()
                obj = json.loads(raw)
                self.assertEqual(obj.get("default_car"), "My Test Car")
            finally:
                tesla.DEFAULTS_FILE = old


if __name__ == "__main__":
    unittest.main()
