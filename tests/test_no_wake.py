import unittest
import sys
from pathlib import Path
from unittest import mock

# Allow importing scripts/tesla.py as a module
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class DummyVehicle(dict):
    def sync_wake_up(self):
        raise AssertionError("sync_wake_up should not be called in this test")


class NoWakeTests(unittest.TestCase):
    def test_wake_vehicle_allow_wake_false_offline_returns_false(self):
        v = DummyVehicle(state="asleep", display_name="Test Car")
        self.assertFalse(tesla.wake_vehicle(v, allow_wake=False))

    def test_wake_vehicle_online_returns_true(self):
        v = DummyVehicle(state="online", display_name="Test Car")
        self.assertTrue(tesla.wake_vehicle(v, allow_wake=False))

    def test_ensure_online_or_exit_exits_3_when_no_wake(self):
        v = DummyVehicle(state="asleep", display_name="Test Car")
        with mock.patch.object(tesla, "wake_vehicle", return_value=False):
            with self.assertRaises(SystemExit) as ctx:
                tesla._ensure_online_or_exit(v, allow_wake=False)
            self.assertEqual(ctx.exception.code, 3)

    def test_summary_no_wake_offline_prints_minimal_human_output_and_exits_3(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout

        v = DummyVehicle(state="asleep", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=True,
            json=False,
            raw_json=False,
            retries=0,
            retry_delay=0,
            metric=False,
        )

        buf = io.StringIO()
        with mock.patch.object(tesla, "get_tesla") as _gt, mock.patch.object(tesla, "get_vehicle", return_value=v):
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit) as ctx:
                    tesla.cmd_summary(args)

        self.assertEqual(ctx.exception.code, 3)
        out = buf.getvalue()
        self.assertIn("🚗 Test Car", out)
        self.assertIn("--no-wake", out)

    def test_report_no_wake_offline_prints_minimal_json_and_exits_3(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout
        import json as _json

        v = DummyVehicle(state="offline", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=True,
            json=True,
            raw_json=False,
            retries=0,
            retry_delay=0,
            metric=False,
            compact=False,
        )

        buf = io.StringIO()
        with mock.patch.object(tesla, "get_tesla") as _gt, mock.patch.object(tesla, "get_vehicle", return_value=v):
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit) as ctx:
                    tesla.cmd_report(args)

        self.assertEqual(ctx.exception.code, 3)
        payload = _json.loads(buf.getvalue())
        self.assertEqual(payload.get("online"), False)
        self.assertEqual(payload.get("vehicle", {}).get("display_name"), "Test Car")

    def test_report_no_wake_offline_compact_json_is_single_line(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout
        import json as _json

        v = DummyVehicle(state="offline", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=True,
            json=True,
            raw_json=False,
            retries=0,
            retry_delay=0,
            metric=False,
            compact=True,
        )

        buf = io.StringIO()
        with mock.patch.object(tesla, "get_tesla") as _gt, mock.patch.object(tesla, "get_vehicle", return_value=v):
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit) as ctx:
                    tesla.cmd_report(args)

        self.assertEqual(ctx.exception.code, 3)
        out = buf.getvalue().strip()
        # Single-line JSON: no newline, no indentation.
        self.assertNotIn("\n", out)
        payload = _json.loads(out)
        self.assertEqual(payload.get("online"), False)

    def test_status_no_wake_offline_prints_minimal_human_output_and_exits_3(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout

        v = DummyVehicle(state="asleep", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=True,
            json=False,
            summary=False,
            retries=0,
            retry_delay=0,
            metric=False,
        )

        buf = io.StringIO()
        with mock.patch.object(tesla, "get_tesla") as _gt, mock.patch.object(tesla, "get_vehicle", return_value=v):
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit) as ctx:
                    tesla.cmd_status(args)

        self.assertEqual(ctx.exception.code, 3)
        out = buf.getvalue()
        self.assertIn("🚗 Test Car", out)
        self.assertIn("--no-wake", out)

    def test_status_no_wake_offline_prints_minimal_json_and_exits_3(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout
        import json as _json

        v = DummyVehicle(state="offline", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=True,
            json=True,
            summary=False,
            retries=0,
            retry_delay=0,
            metric=False,
            compact=False,
        )

        buf = io.StringIO()
        with mock.patch.object(tesla, "get_tesla") as _gt, mock.patch.object(tesla, "get_vehicle", return_value=v):
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit) as ctx:
                    tesla.cmd_status(args)

        self.assertEqual(ctx.exception.code, 3)
        payload = _json.loads(buf.getvalue())
        self.assertEqual(payload.get("online"), False)
        self.assertEqual(payload.get("vehicle", {}).get("display_name"), "Test Car")

    def test_status_no_wake_offline_compact_json_is_single_line(self):
        from types import SimpleNamespace
        import io
        from contextlib import redirect_stdout
        import json as _json

        v = DummyVehicle(state="offline", display_name="Test Car")

        args = SimpleNamespace(
            email="you@email.com",
            car=None,
            no_wake=True,
            json=True,
            summary=False,
            retries=0,
            retry_delay=0,
            metric=False,
            compact=True,
        )

        buf = io.StringIO()
        with mock.patch.object(tesla, "get_tesla") as _gt, mock.patch.object(tesla, "get_vehicle", return_value=v):
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit) as ctx:
                    tesla.cmd_status(args)

        self.assertEqual(ctx.exception.code, 3)
        out = buf.getvalue().strip()
        self.assertNotIn("\n", out)
        payload = _json.loads(out)
        self.assertEqual(payload.get("online"), False)


if __name__ == "__main__":
    unittest.main()
