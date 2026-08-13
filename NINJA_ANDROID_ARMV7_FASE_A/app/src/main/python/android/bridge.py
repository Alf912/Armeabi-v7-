"""Platform-neutral bridge between Android UI and Ninja Engine."""

from dataclasses import dataclass

from ninja.engine import EngineResult


@dataclass
class BridgeResponse:
    status: str
    error: str
    persisted: bool
    indexed: bool
    output: str = ""


class NinjaAndroidBridge:
    def __init__(self, host):
        self.host = host
        self.engine = host.create_engine()

    def process_markdown(self, markdown, destination="ninja_op_usuario.py"):
        result = self.engine.procesar_entrada_maestra(markdown, destination)
        output = ""
        if result.execution is not None:
            output = result.execution.output

        return BridgeResponse(
            status=result.status,
            error=result.error,
            persisted=result.persisted,
            indexed=result.indexed,
            output=output,
        )
