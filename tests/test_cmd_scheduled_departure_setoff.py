import unittest
from unittest import mock

# Import the tesla script as a module
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class DummyVehicle:
    def __init__(self, display_name="Test Car", state="online", vehicle_data=None):
        self._display_name = display_name
        self._state = state
        self._vehicle_data = vehicle_data or {}
        self.command_calls = []

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

    def get_vehicle_data(self):
        return self._vehicle_data

    def command(self, name, **kwargs):
        self.command_calls.append((name, kwargs))


class CmdScheduledDepartureSetOffTests(unittest.TestCase):
    def test_scheduled_departure_set_requires_yes(self):
        vehicle = DummyVehicle()
        args = mock.Mock()
        args.car = None
        args.action = "set"
        args.time = "07:30"
        args.yes = False
        args.no_wake = False
        args.json = False

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "wake_vehicle", return_value=True):
            with self.assertRaises(SystemExit) as ctx:
                tesla.cmd_scheduled_departure(args)

        self.assertEqual(ctx.exception.code, 2)
        self.assertEqual(vehicle.command_calls, [])

    def test_scheduled_departure_set_calls_endpoint(self):
        vehicle = DummyVehicle()
        args = mock.Mock()
        args.car = None
        args.action = "set"
        args.time = "07:30"
        args.yes = True
        args.no_wake = False
        args.json = False

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "wake_vehicle", return_value=True):
            tesla.cmd_scheduled_departure(args)

        self.assertEqual(vehicle.command_calls, [("SCHEDULED_DEPARTURE", {"enable": True, "departure_time": 450})])

    def test_scheduled_departure_off_calls_endpoint(self):
        vehicle = DummyVehicle()
        args = mock.Mock()
        args.car = None
        args.action = "off"
        args.time = None
        args.yes = True
        args.no_wake = False
        args.json = False

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "wake_vehicle", return_value=True):
            tesla.cmd_scheduled_departure(args)

        self.assertEqual(vehicle.command_calls, [("SCHEDULED_DEPARTURE", {"enable": False, "departure_time": 0})])


if __name__ == "__main__":
    unittest.main()
