import tempfile
import unittest
from pathlib import Path
from ninja.storage import SesStorage
from ninja.indexer import SesIndexer

class TestFaseB(unittest.TestCase):
    def test_storage_uses_injected_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = SesStorage(Path(tmp) / "ninja-data")
            self.assertTrue(s.scripts_dir.is_dir())
            self.assertTrue(s.logs_dir.is_dir())
            self.assertTrue(s.index_dir.is_dir())
            self.assertTrue(s.config_dir.is_dir())

    def test_safe_script_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = SesStorage(Path(tmp) / "ninja-data")
            self.assertTrue(s.escribir_codigo_seguro("ninja_op_test.py", 'SES_RESULTADO = "PASS"'))
            self.assertTrue((s.scripts_dir / "ninja_op_test.py").is_file())

    def test_reject_path_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = SesStorage(Path(tmp) / "ninja-data")
            self.assertFalse(s.escribir_codigo_seguro("ninja_op_../escape.py", "x = 1"))

    def test_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = SesStorage(Path(tmp) / "ninja-data")
            self.assertTrue(s.escribir_codigo_seguro("ninja_op_test.py", "x = 1"))
            self.assertFalse(s.escribir_codigo_seguro("ninja_op_test.py", "x = 2"))

    def test_indexer_detects_cycle(self):
        i = SesIndexer()
        i.registrar_documento("A", ["B"])
        i.registrar_documento("B", ["A"])
        self.assertFalse(i.escanear_bucles_circulares())

    def test_indexer_accepts_acyclic_graph(self):
        i = SesIndexer()
        i.registrar_documento("A", ["B"])
        i.registrar_documento("B", [])
        self.assertTrue(i.escanear_bucles_circulares())

if __name__ == "__main__":
    unittest.main()
