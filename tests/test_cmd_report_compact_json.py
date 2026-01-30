import unittest
import sys
from pathlib import Path
from unittest import mock

# Allow importing scripts/tesla.py as a module
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class DummyVehicle(dict):
    def get_vehicle_data(self):
        # Minimal vehicle_data payload (no drive_state/location required)
        return {
            "charge_state": {"battery_level": 80, "battery_range": 200.0, "charging_state": "Disconnected"},
            "climate_state": {"inside_temp": 20.0, "outside_temp": 10.0, "is_climate_on": False},
            "vehicle_state": {"locked": True, "timestamp": 1700000000000},
        }


class CmdReportCompactJsonTests(unittest.TestCase):
    def test_cmd_report_compact_json_is_single_line_valid_json(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout
        import json as _json

        v = DummyVehicle(state="online", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=False,
            json=True,
            raw_json=False,
            compact=True,
            retries=0,
            retry_delay=0,
            metric=False,
        )

        buf = io.StringIO()
        with (
            mock.patch.object(tesla, "get_tesla") as _gt,
            mock.patch.object(tesla, "get_vehicle", return_value=v),
            mock.patch.object(tesla, "wake_vehicle", return_value=True),
        ):
            with redirect_stdout(buf):
                tesla.cmd_report(args)

        out = buf.getvalue().strip()
        self.assertTrue(out.startswith("{"))
        self.assertNotIn("\n", out, "Expected compact JSON to be single-line")

        payload = _json.loads(out)
        self.assertEqual(payload.get("vehicle", {}).get("display_name"), "Test Car")
        self.assertEqual(payload.get("battery", {}).get("level_percent"), 80)
