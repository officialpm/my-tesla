import unittest
from unittest import mock

# Import the tesla script as a module
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class DummyVehicle:
    def __init__(self, display_name="Test Car", state="online"):
        self._display_name = display_name
        self._state = state

    def __getitem__(self, k):
        if k == "display_name":
            return self._display_name
        if k == "state":
            return self._state
        raise KeyError(k)

    def get(self, k, default=None):
        if k == "display_name":
            return self._display_name
        if k == "state":
            return self._state
        return default


class CmdChargeStatusHumanTests(unittest.TestCase):
    def test_charge_status_includes_scheduled_charging_line(self):
        vehicle = DummyVehicle(display_name="My Car")

        args = mock.Mock()
        args.car = None
        args.action = "status"
        args.no_wake = True
        args.json = False
        args.metric = False
        args.retries = 0
        args.retry_delay = 0

        vehicle_data = {
            'charge_state': {
                'battery_level': 55,
                'battery_range': 123.4,
                'charging_state': 'Stopped',
                'charge_limit_soc': 80,
                'scheduled_charging_start_time': 420,  # 07:00
                'scheduled_charging_pending': True,
            }
        }

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "_ensure_online_or_exit"), \
             mock.patch.object(tesla, "fetch_vehicle_data", return_value=vehicle_data), \
             mock.patch("builtins.print") as p:
            tesla.cmd_charge(args)

        printed = "\n".join(str(call.args[0]) for call in p.call_args_list)
        self.assertIn("Scheduled charging:", printed)
        self.assertIn("On", printed)
        self.assertIn("07:00", printed)


if __name__ == "__main__":
    unittest.main()
