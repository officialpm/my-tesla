import unittest
import sys
from pathlib import Path

# Allow importing scripts/tesla.py as a module
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class ReportChargingCurrentRequestTests(unittest.TestCase):
    def test_report_includes_charging_current_request_when_present(self):
        vehicle = {"display_name": "Test Car", "state": "online"}
        data = {
            "charge_state": {
                "battery_level": 50,
                "battery_range": 123.4,
                "charging_state": "Charging",
                "charge_current_request": 16,
                "charge_current_request_max": 32,
            },
            "climate_state": {},
            "vehicle_state": {},
        }

        out = tesla._report(vehicle, data)
        self.assertIn("Charging: Charging", out)
        self.assertIn("Charging current request: 16A (max 32A)", out)


if __name__ == "__main__":
    unittest.main()
