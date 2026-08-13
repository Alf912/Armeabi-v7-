"""Ninja Android ARMv7 - AST Sanitizer.
Preserves the banned-name and attribute contracts from SES v2.6.
"""

import ast


class SesSanitizer(ast.NodeVisitor):
    def __init__(self):
        self.BANNED_NAMES = {
            "os", "sys", "subprocess", "ctypes",
            "eval", "exec", "__import__", "compile",
        }
        self.is_safe = True

    def verificar_codigo(self, codigo_fuente: str) -> bool:
        try:
            lineas_limpias = [
                line
                for line in codigo_fuente.splitlines()
                if not line.strip().startswith("#")
            ]
            arbol = ast.parse("\n".join(lineas_limpias))
            self.is_safe = True
            self.visit(arbol)
            return self.is_safe
        except Exception:
            self.is_safe = False
            return False

    def visit_Name(self, node):
        if node.id in self.BANNED_NAMES:
            self.is_safe = False
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value in self.BANNED_NAMES:
            self.is_safe = False
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr.startswith("__") and node.attr.endswith("__"):
            self.is_safe = False
        if node.attr in {
            "__globals__", "__builtins__", "__subclasses__",
            "__mro__", "__base__",
        }:
            self.is_safe = False
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in self.BANNED_NAMES:
                self.is_safe = False
        self.generic_visit(node)
