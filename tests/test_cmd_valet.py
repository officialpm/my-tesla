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


class CmdValetTests(unittest.TestCase):
    def test_valet_status_json(self):
        vehicle = DummyVehicle(vehicle_data={
            'vehicle_state': {
                'valet_mode': True,
                'valet_pin_needed': False,
            }
        })
        args = mock.Mock()
        args.car = None
        args.action = 'status'
        args.no_wake = True
        args.json = True

        with mock.patch.object(tesla, 'get_tesla'), \
             mock.patch.object(tesla, 'get_vehicle', return_value=vehicle), \
             mock.patch.object(tesla, 'require_email', return_value='test@example.com'), \
             mock.patch.object(tesla, 'wake_vehicle', return_value=True) as wake, \
             mock.patch('builtins.print') as p:
            tesla.cmd_valet(args)

        wake.assert_called_once_with(vehicle, allow_wake=False)
        printed = "\n".join(str(call.args[0]) for call in p.call_args_list)
        self.assertIn('"valet_mode": true', printed.lower())
        self.assertIn('"valet_pin_needed": false', printed.lower())

    def test_valet_on_requires_pin(self):
        vehicle = DummyVehicle()
        args = mock.Mock()
        args.car = None
        args.action = 'on'
        args.yes = True
        args.pin = None

        with mock.patch.object(tesla, 'get_tesla'), \
             mock.patch.object(tesla, 'get_vehicle', return_value=vehicle), \
             mock.patch.object(tesla, 'require_email', return_value='test@example.com'), \
             mock.patch.object(tesla, 'wake_vehicle'):
            with self.assertRaises(ValueError):
                tesla.cmd_valet(args)

    def test_valet_on_calls_endpoint(self):
        vehicle = DummyVehicle()
        args = mock.Mock()
        args.car = None
        args.action = 'on'
        args.yes = True
        args.pin = '1234'

        with mock.patch.object(tesla, 'get_tesla'), \
             mock.patch.object(tesla, 'get_vehicle', return_value=vehicle), \
             mock.patch.object(tesla, 'require_email', return_value='test@example.com'), \
             mock.patch.object(tesla, 'wake_vehicle'):
            tesla.cmd_valet(args)

        self.assertEqual(vehicle.command_calls, [("SET_VALET_MODE", {"on": True, "password": "1234"})])

    def test_valet_off_calls_endpoint(self):
        vehicle = DummyVehicle()
        args = mock.Mock()
        args.car = None
        args.action = 'off'
        args.yes = True

        with mock.patch.object(tesla, 'get_tesla'), \
             mock.patch.object(tesla, 'get_vehicle', return_value=vehicle), \
             mock.patch.object(tesla, 'require_email', return_value='test@example.com'), \
             mock.patch.object(tesla, 'wake_vehicle'):
            tesla.cmd_valet(args)

        self.assertEqual(vehicle.command_calls, [("SET_VALET_MODE", {"on": False})])

    def test_valet_reset_pin_calls_endpoint(self):
        vehicle = DummyVehicle()
        args = mock.Mock()
        args.car = None
        args.action = 'reset-pin'
        args.yes = True

        with mock.patch.object(tesla, 'get_tesla'), \
             mock.patch.object(tesla, 'get_vehicle', return_value=vehicle), \
             mock.patch.object(tesla, 'require_email', return_value='test@example.com'), \
             mock.patch.object(tesla, 'wake_vehicle'):
            tesla.cmd_valet(args)

        self.assertEqual(vehicle.command_calls, [("RESET_VALET_PIN", {})])


if __name__ == '__main__':
    unittest.main()
