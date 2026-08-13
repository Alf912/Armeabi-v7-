import time
import unittest
from ninja.executor import SesExecutor


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = SesExecutor()

    def test_pass_contract(self):
        r = self.executor.execute('SES_RESULTADO = "PASS"')
        self.assertEqual(r.status, "PASS")

    def test_fail_contract(self):
        r = self.executor.execute('SES_RESULTADO = "FAIL"')
        self.assertEqual(r.status, "FAIL")

    def test_missing_contract(self):
        r = self.executor.execute("x = 1")
        self.assertEqual(r.status, "SIN_CONTRATO")

    def test_exception(self):
        r = self.executor.execute("raise ValueError('x')")
        self.assertEqual(r.status, "EXCEPCION")

    def test_import_blocked(self):
        r = self.executor.execute("import os")
        self.assertEqual(r.status, "EXCEPCION")
        self.assertIn("IMPORT_NO_AUTORIZADO", r.error)

    def test_timeout(self):
        r = self.executor.execute("while True: pass")
        self.assertEqual(r.status, "TIMEOUT")

    def test_output(self):
        r = self.executor.execute('print("NINJA"); SES_RESULTADO = "PASS"')
        self.assertEqual(r.status, "PASS")
        self.assertIn("NINJA", r.output)


if __name__ == "__main__":
    unittest.main()
