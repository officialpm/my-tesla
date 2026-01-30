import io
import unittest
from contextlib import redirect_stderr
from unittest import mock

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import tesla  # noqa: E402


class RequireYesTests(unittest.TestCase):
    def test_require_yes_prints_rerun_suggestion(self):
        args = mock.Mock()
        args.yes = False

        old_argv = list(sys.argv)
        try:
            sys.argv = ["tesla.py", "lock", "--car", "My Car"]
            buf = io.StringIO()
            with redirect_stderr(buf):
                with self.assertRaises(SystemExit) as cm:
                    tesla.require_yes(args, "lock")
            self.assertEqual(cm.exception.code, 2)
            out = buf.getvalue()
            self.assertIn("--yes", out)
            self.assertIn("lock", out)
            # Suggestion should include the original args and append --yes.
            self.assertIn("--car", out)
            self.assertIn("My Car", out)
        finally:
            sys.argv = old_argv
