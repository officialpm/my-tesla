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
            "charge_state": {"battery_level": 55, "battery_range": 123.4, "charging_state": "Disconnected"},
            "climate_state": {"inside_temp": 21.0, "is_climate_on": False},
            "vehicle_state": {"locked": True, "timestamp": 1700000000000},
        }


class CmdReportOneLineTests(unittest.TestCase):
    def test_cmd_report_one_line_outputs_single_line_summary(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout

        v = DummyVehicle(state="online", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=False,
            json=False,
            raw_json=False,
            compact=False,
            one_line=True,
            retries=0,
            retry_delay=0,
            metric=False,
        )

        buf = io.StringIO()
        with (
            mock.patch.object(tesla, "get_tesla"),
            mock.patch.object(tesla, "get_vehicle", return_value=v),
            mock.patch.object(tesla, "wake_vehicle", return_value=True),
        ):
            with redirect_stdout(buf):
                tesla.cmd_report(args)

        out = buf.getvalue().strip()
        self.assertTrue(out.startswith("🚗 Test Car"))
        self.assertNotIn("\n", out)
        # Should include at-a-glance lock + battery
        self.assertIn("Locked", out)
        self.assertIn("55%", out)
