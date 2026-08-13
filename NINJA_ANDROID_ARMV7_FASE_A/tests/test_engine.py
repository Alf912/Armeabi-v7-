import tempfile
import unittest
from pathlib import Path

from ninja.engine import create_default_engine


class TestEngine(unittest.TestCase):
    def test_pass_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = create_default_engine(Path(tmp) / "data")
            result = engine.procesar_entrada_maestra(
                '```python\nSES_RESULTADO = "PASS"\n```',
                "ninja_op_flow.py",
            )
            self.assertEqual(result.status, "PASS")
            self.assertTrue(result.persisted)
            self.assertTrue(result.indexed)

    def test_fail_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = create_default_engine(Path(tmp) / "data")
            result = engine.procesar_entrada_maestra(
                '```python\nSES_RESULTADO = "FAIL"\n```',
                "ninja_op_flow.py",
            )
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(result.persisted)

    def test_invalid_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = create_default_engine(Path(tmp) / "data")
            result = engine.procesar_entrada_maestra("texto sin cierre")
            self.assertEqual(result.status, "FAIL")
            self.assertEqual(result.error, "ENTRADA_INVALIDA")

    def test_unsafe_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = create_default_engine(Path(tmp) / "data")
            result = engine.procesar_entrada_maestra(
                "```python\nimport os\nSES_RESULTADO = \"PASS\"\n```"
            )
            self.assertEqual(result.status, "FAIL")
            self.assertEqual(result.error, "CODIGO_NO_SEGURO")

    def test_no_old_scripts_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "data"
            engine = create_default_engine(root)
            engine.procesar_entrada_maestra(
                '```python\nSES_RESULTADO = "PASS"\n```',
                "ninja_op_flow.py",
            )
            self.assertFalse((Path(tmp) / "03_Scripts").exists())
            self.assertTrue((root / "scripts").is_dir())


if __name__ == "__main__":
    unittest.main()
