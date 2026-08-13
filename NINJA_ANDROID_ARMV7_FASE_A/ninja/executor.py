"""Ninja Android ARMv7 - controlled executor.

The public contract is independent from the process-isolation mechanism.
This phase deliberately uses a thread-based timeout so the core remains
portable; Android-specific process isolation is deferred to the host layer.
"""

import builtins
import io
import threading
import traceback
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    status: str
    error: str = "NINGUNO"
    output: str = ""
    elapsed_seconds: float = 0.0


class SesExecutor:
    TIMEOUT_SECONDS = 3.0

    ALLOWED_BUILTINS = {
        "print": print,
        "len": len,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
        "range": range,
        "enumerate": enumerate,
        "zip": zip,
        "min": min,
        "max": max,
        "sum": sum,
        "abs": abs,
        "round": round,
        "sorted": sorted,
    }

    def __init__(self, timeout_seconds=None):
        self.timeout_seconds = (
            float(timeout_seconds)
            if timeout_seconds is not None
            else self.TIMEOUT_SECONDS
        )

    def _run(self, codigo, result_box):
        buffer = io.StringIO()

        def safe_import(*args, **kwargs):
            raise ImportError("IMPORT_NO_AUTORIZADO")

        namespace = {
            "__builtins__": dict(self.ALLOWED_BUILTINS, __import__=safe_import),
            "SES_RESULTADO": None,
        }

        original_stdout = __import__("sys").stdout
        try:
            __import__("sys").stdout = buffer
            compiled = compile(codigo, "<ninja>", "exec")
            exec(compiled, namespace, namespace)

            resultado = namespace.get("SES_RESULTADO")
            if resultado == "PASS":
                result_box["result"] = ExecutionResult(
                    status="PASS",
                    output=buffer.getvalue(),
                )
            elif resultado == "FAIL":
                result_box["result"] = ExecutionResult(
                    status="FAIL",
                    error="CONTRATO_FAIL",
                    output=buffer.getvalue(),
                )
            else:
                result_box["result"] = ExecutionResult(
                    status="SIN_CONTRATO",
                    error="SES_RESULTADO_AUSENTE",
                    output=buffer.getvalue(),
                )
        except Exception as exc:
            result_box["result"] = ExecutionResult(
                status="EXCEPCION",
                error=f"{type(exc).__name__}: {exc}",
                output=buffer.getvalue(),
            )
        finally:
            __import__("sys").stdout = original_stdout

    def execute(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            return ExecutionResult(
                status="FAIL",
                error="CODIGO_INVALIDO",
            )

        result_box = {}
        worker = threading.Thread(
            target=self._run,
            args=(codigo, result_box),
            daemon=True,
        )
        worker.start()
        worker.join(self.timeout_seconds)

        if worker.is_alive():
            return ExecutionResult(
                status="TIMEOUT",
                error="TIMEOUT_3S",
            )

        return result_box.get(
            "result",
            ExecutionResult(
                status="PROCESO_SIN_RESPUESTA",
                error="RESULTADO_NO_GENERADO",
            ),
        )
