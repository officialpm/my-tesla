import unittest
from unittest import mock

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


class CmdTrunkTests(unittest.TestCase):
    def test_trunk_status_no_wake_json(self):
        vehicle = DummyVehicle(vehicle_data={
            'vehicle_state': {
                'rt': 0,
                'ft': 1,
            }
        })
        args = mock.Mock()
        args.car = None
        args.action = 'status'
        args.which = 'frunk'
        args.no_wake = True
        args.json = True

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "wake_vehicle", return_value=True) as wake, \
             mock.patch("builtins.print") as p:
            tesla.cmd_trunk(args)

        # status should respect --no-wake
        wake.assert_called_once_with(vehicle, allow_wake=False)
        printed = "\n".join(str(call.args[0]) for call in p.call_args_list)
        self.assertIn('"which": "frunk"', printed)
        self.assertIn('"state": "open"', printed)

    def test_trunk_open_when_already_open_no_command(self):
        vehicle = DummyVehicle(vehicle_data={
            'vehicle_state': {
                'rt': 1,
            }
        })
        args = mock.Mock()
        args.car = None
        args.action = 'open'
        args.which = 'trunk'
        args.yes = True
        args.force = False

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "wake_vehicle") as wake, \
             mock.patch.object(tesla, "fetch_vehicle_data", return_value=vehicle.get_vehicle_data()), \
             mock.patch("builtins.print") as p:
            tesla.cmd_trunk(args)

        wake.assert_called_once()
        self.assertEqual(vehicle.command_calls, [])
        printed = "\n".join(str(call.args[0]) for call in p.call_args_list)
        self.assertIn('already open', printed)

    def test_trunk_close_unknown_state_requires_force(self):
        vehicle = DummyVehicle(vehicle_data={
            'vehicle_state': {
                'rt': None,
            }
        })
        args = mock.Mock()
        args.car = None
        args.action = 'close'
        args.which = 'trunk'
        args.yes = True
        args.force = False

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "wake_vehicle"), \
             mock.patch.object(tesla, "fetch_vehicle_data", return_value=vehicle.get_vehicle_data()):
            with self.assertRaises(ValueError):
                tesla.cmd_trunk(args)

    def test_trunk_close_unknown_state_force_toggles(self):
        vehicle = DummyVehicle(vehicle_data={
            'vehicle_state': {
                'rt': None,
            }
        })
        args = mock.Mock()
        args.car = None
        args.action = 'close'
        args.which = 'trunk'
        args.yes = True
        args.force = True

        with mock.patch.object(tesla, "get_tesla"), \
             mock.patch.object(tesla, "get_vehicle", return_value=vehicle), \
             mock.patch.object(tesla, "require_email", return_value="test@example.com"), \
             mock.patch.object(tesla, "wake_vehicle") as wake, \
             mock.patch.object(tesla, "fetch_vehicle_data", return_value=vehicle.get_vehicle_data()):
            tesla.cmd_trunk(args)

        wake.assert_called_once()
        self.assertEqual(vehicle.command_calls, [("ACTUATE_TRUNK", {"which_trunk": "rear"})])


if __name__ == '__main__':
    unittest.main()
