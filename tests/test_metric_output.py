import unittest
import sys
from pathlib import Path

# Allow importing scripts/tesla.py as a module
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class MetricOutputTests(unittest.TestCase):
    def test_fmt_distance_defaults_to_miles(self):
        self.assertEqual(tesla._fmt_distance(100, metric=False, decimals=0), "100 mi")

    def test_fmt_distance_metric_converts_to_km(self):
        # 100 mi -> 160.9344 km -> 161 km (0 decimals)
        self.assertEqual(tesla._fmt_distance(100, metric=True, decimals=0), "161 km")

    def test_short_status_metric_uses_km(self):
        vehicle = {"display_name": "Test Car", "state": "online"}
        data = {
            "charge_state": {"battery_level": 80, "battery_range": 100.0, "charging_state": "Disconnected"},
            "vehicle_state": {"locked": True},
            "climate_state": {"inside_temp": 20, "is_climate_on": False},
        }

        out = tesla._short_status(vehicle, data, metric=True)
        self.assertIn("(161 km)", out)
        self.assertNotIn(" mi)", out)

    def test_report_metric_uses_km_for_battery_range(self):
        vehicle = {"display_name": "Test Car", "state": "online"}
        data = {
            "charge_state": {"battery_level": 80, "battery_range": 100.0},
            "vehicle_state": {"locked": True},
            "climate_state": {},
        }

        out = tesla._report(vehicle, data, metric=True, compact=True)
        self.assertIn("Battery: 80% (161 km)", out)

    def test_fmt_speed_metric_converts_to_kmh(self):
        # 10 mph -> 16.09344 km/h -> 16 km/h (0 decimals)
        self.assertEqual(tesla._fmt_speed(10, metric=True, decimals=0), "16 km/h")
        self.assertEqual(tesla._fmt_speed(10, metric=False, decimals=0), "10 mph")

    def test_report_metric_uses_kmh_for_charge_rate(self):
        vehicle = {"display_name": "Test Car", "state": "online"}
        data = {
            "charge_state": {
                "battery_level": 80,
                "battery_range": 100.0,
                "charging_state": "Charging",
                "charge_rate": 10.0,
                "charge_limit_soc": 90,
            },
            "vehicle_state": {"locked": True},
            "climate_state": {},
        }

        out = tesla._report(vehicle, data, metric=True, compact=True)
        self.assertIn("Charging: Charging", out)
        self.assertIn("16 km/h", out)


if __name__ == "__main__":
    unittest.main()
