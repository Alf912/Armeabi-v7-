"""Ninja Android ARMv7 - engine orchestration layer."""

import re
from dataclasses import dataclass

from .core import SesCore
from .sanitizer import SesSanitizer
from .validator import SesClipboardValidator
from .storage import SesStorage
from .indexer import SesIndexer
from .executor import SesExecutor, ExecutionResult


@dataclass
class EngineResult:
    status: str
    error: str = "NINGUNO"
    execution: ExecutionResult | None = None
    persisted: bool = False
    indexed: bool = False


class SesEngineMaster:
    """Coordinates SES components without knowing Android filesystem details."""

    def __init__(self, core, sanitizer, storage, indexer, validator, executor):
        self.core = core
        self.sanitizer = sanitizer
        self.storage = storage
        self.indexer = indexer
        self.validator = validator
        self.executor = executor

    @staticmethod
    def _extract_python(markdown):
        pattern = r"```(?:python)?\s*\n(.*?)```"
        match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
        if not match:
            return None
        return match.group(1).strip()

    def procesar_entrada_maestra(self, markdown, destino="ninja_op_usuario.py"):
        if not self.validator.cargar_y_validar_entrada(markdown):
            return EngineResult("FAIL", "ENTRADA_INVALIDA")

        codigo = self._extract_python(markdown)
        if codigo is None:
            return EngineResult("FAIL", "BLOQUE_PYTHON_NO_ENCONTRADO")

        if not self.sanitizer.verificar_codigo(codigo):
            return EngineResult("FAIL", "CODIGO_NO_SEGURO")

        core_result = self.core.ejecutar_orden({"operacion": "EJECUTAR"})
        if core_result.get("LAST_ERROR") != "NINGUNO":
            return EngineResult("FAIL", core_result["LAST_ERROR"])

        execution = self.executor.execute(codigo)

        if execution.status not in {"PASS", "FAIL"}:
            return EngineResult(
                execution.status,
                execution.error,
                execution=execution,
            )

        persisted = self.storage.escribir_codigo_seguro(destino, codigo)
        if not persisted:
            return EngineResult(
                "FAIL",
                "PERSISTENCIA_RECHAZADA",
                execution=execution,
            )

        self.indexer.registrar_documento(destino, [])
        indexed = self.indexer.escanear_bucles_circulares()

        if not indexed:
            return EngineResult(
                "FAIL",
                "BUCLE_CIRCULAR",
                execution=execution,
                persisted=True,
                indexed=False,
            )

        return EngineResult(
            execution.status,
            execution.error,
            execution=execution,
            persisted=True,
            indexed=True,
        )


def create_default_engine(root_dir):
    storage = SesStorage(root_dir)
    return SesEngineMaster(
        SesCore(),
        SesSanitizer(),
        storage,
        SesIndexer(),
        SesClipboardValidator(),
        SesExecutor(),
    )
