import tempfile
import unittest
from pathlib import Path

from android.host import AndroidHost
from android.bridge import NinjaAndroidBridge


class TestAndroidPhaseE(unittest.TestCase):
    def test_host_creates_private_ninja_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            host = AndroidHost(Path(tmp) / "files")
            root = host.get_ninja_data_dir()
            self.assertTrue(root.is_dir())
            self.assertEqual(root.name, "ninja")

    def test_bridge_executes_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            bridge = NinjaAndroidBridge(AndroidHost(Path(tmp) / "files"))
            response = bridge.process_markdown(
                '```python\nSES_RESULTADO = "PASS"\n```',
                "ninja_op_android.py",
            )
            self.assertEqual(response.status, "PASS")
            self.assertTrue(response.persisted)
            self.assertTrue(response.indexed)

    def test_old_working_directory_is_not_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = root / "03_Scripts"
            bridge = NinjaAndroidBridge(AndroidHost(root / "files"))
            bridge.process_markdown(
                '```python\nSES_RESULTADO = "PASS"\n```',
                "ninja_op_android.py",
            )
            self.assertFalse(old.exists())


if __name__ == "__main__":
    unittest.main()
