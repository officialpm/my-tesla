import unittest
import sys
from pathlib import Path

# Allow importing scripts/tesla.py as a module
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class ReportValetTests(unittest.TestCase):
    def test_report_includes_valet_mode_when_present(self):
        vehicle = {"display_name": "Test Car", "state": "online"}
        data = {
            "charge_state": {"battery_level": 80, "battery_range": 250.0},
            "climate_state": {"inside_temp": 20, "outside_temp": 10, "is_climate_on": False},
            "vehicle_state": {"locked": True, "sentry_mode": False, "valet_mode": True},
        }

        out = tesla._report(vehicle, data)
        self.assertIn("Valet: On", out)


if __name__ == "__main__":
    unittest.main()
