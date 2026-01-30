import tempfile
import unittest
from pathlib import Path

from scripts.tesla import _cleanup_bytecode_under


class TestCleanupBytecode(unittest.TestCase):
    def test_cleanup_removes_pyc_and_pycache(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)

            # Create a nested __pycache__ directory with a .pyc file.
            pc = base / "pkg" / "__pycache__"
            pc.mkdir(parents=True)
            (pc / "mod.cpython-312.pyc").write_bytes(b"x")

            # And a stray .pyo file elsewhere.
            other = base / "other"
            other.mkdir(parents=True)
            (other / "x.pyo").write_bytes(b"y")

            self.assertTrue(pc.exists())
            self.assertTrue((other / "x.pyo").exists())

            _cleanup_bytecode_under(base)

            self.assertFalse(pc.exists())
            self.assertFalse((other / "x.pyo").exists())
