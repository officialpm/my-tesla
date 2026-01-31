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
        return {
            "charge_state": {
                "battery_level": 55,
                "battery_range": 123.4,
                "usable_battery_level": 52,
                "charging_state": "Disconnected",
                "charge_limit_soc": 80,
            },
            "climate_state": {},
            "vehicle_state": {"timestamp": 1700000000000},
        }


class CmdChargeCompactJsonTests(unittest.TestCase):
    def test_cmd_charge_status_compact_json_is_single_line_valid_json(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout
        import json as _json

        v = DummyVehicle(state="online", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            action="status",
            value=None,
            no_wake=False,
            json=True,
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
                tesla.cmd_charge(args)

        out = buf.getvalue().strip()
        self.assertTrue(out.startswith("{"))
        self.assertNotIn("\n", out, "Expected compact JSON to be single-line")

        payload = _json.loads(out)
        self.assertEqual(payload.get("battery_level"), 55)
        self.assertEqual(payload.get("charging_state"), "Disconnected")


if __name__ == "__main__":
    unittest.main()
