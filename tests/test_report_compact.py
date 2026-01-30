import unittest
import sys
from pathlib import Path

# Allow importing scripts/tesla.py as a module
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class ReportCompactTests(unittest.TestCase):
    def test_report_compact_hides_non_core_lines(self):
        vehicle = {"display_name": "Test Car", "state": "online"}
        data = {
            "charge_state": {
                "battery_level": 80,
                "battery_range": 250.2,
                "usable_battery_level": 78,
                "charging_state": "Charging",
                "charge_limit_soc": 90,
                "minutes_to_full_charge": 75,
                "charger_voltage": 240,
                "charger_actual_current": 16,
                "charge_port_door_open": True,
                "conn_charge_cable": "SAE",
                "fast_charger_present": True,
                "fast_charger_type": "Tesla",
                "scheduled_charging_pending": True,
                "scheduled_charging_start_time": 60,
            },
            "climate_state": {
                "inside_temp": 21,
                "outside_temp": 10,
                "is_climate_on": True,
                "seat_heater_left": 3,
            },
            "vehicle_state": {
                "locked": False,
                "sentry_mode": True,
                "tpms_pressure_fl": 42.0,
                "car_version": "2025.44.30.7",
                "timestamp": 1767220800000,
                "odometer": 12345.6,
                # Openings
                "df": 1,
            },
        }

        out = tesla._report(vehicle, data, compact=True)

        # Core lines should remain
        self.assertIn("🚗 Test Car", out)
        self.assertIn("Battery: 80%", out)
        self.assertIn("Charging: Charging", out)
        self.assertIn("Inside:", out)
        self.assertIn("Outside:", out)
        self.assertIn("Locked:", out)
        self.assertIn("Sentry:", out)

        # Non-core lines should be suppressed in compact mode
        self.assertNotIn("Openings:", out)
        self.assertNotIn("Usable battery:", out)
        self.assertNotIn("Charging power:", out)
        self.assertNotIn("Charging current request:", out)
        self.assertNotIn("Charge port door:", out)
        self.assertNotIn("Charge cable:", out)
        self.assertNotIn("Fast charger:", out)
        self.assertNotIn("Scheduled charging:", out)
        self.assertNotIn("Seat heaters:", out)
        self.assertNotIn("Tires (TPMS):", out)
        self.assertNotIn("Software:", out)
        self.assertNotIn("Updated:", out)
        self.assertNotIn("Odometer:", out)


if __name__ == "__main__":
    unittest.main()
