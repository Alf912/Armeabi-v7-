"""Ninja Android ARMv7 - Storage service."""
from pathlib import Path
import os

class SesStorage:
    VALID_OPS = {"INGESTA", "SANITIZAR", "EJECUTAR", "PERSISTENCIA", "INDEXAR"}

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir).expanduser().resolve()
        self.scripts_dir = self.root_dir / "scripts"
        self.logs_dir = self.root_dir / "logs"
        self.index_dir = self.root_dir / "index"
        self.config_dir = self.root_dir / "config"
        for directory in (self.scripts_dir, self.logs_dir, self.index_dir, self.config_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def emitir_telemetria(self, *args, **kwargs):
        return {"ESTADO": "OK", "TELEMETRIA": True}

    @staticmethod
    def _valid_script_name(nombre_archivo):
        if not isinstance(nombre_archivo, str):
            return False
        if not nombre_archivo.startswith("ninja_op_") or not nombre_archivo.lower().endswith(".py"):
            return False
        if os.path.basename(nombre_archivo) != nombre_archivo:
            return False
        if "/" in nombre_archivo or "\\" in nombre_archivo:
            return False
        return True

    def escribir_codigo_seguro(self, nombre_archivo, contenido):
        if not self._valid_script_name(nombre_archivo):
            return False
        if not isinstance(contenido, str) or not contenido:
            return False
        destination = (self.scripts_dir / nombre_archivo).resolve()
        if destination.parent != self.scripts_dir or destination.exists():
            return False
        temporary = self.scripts_dir / f".{nombre_archivo}.{os.getpid()}.tmp"
        try:
            with temporary.open("x", encoding="utf-8") as handle:
                handle.write(contenido)
                handle.flush()
                os.fsync(handle.fileno())
            if temporary.stat().st_size == 0:
                temporary.unlink(missing_ok=True)
                return False
            os.replace(temporary, destination)
            return True
        except (OSError, ValueError):
            temporary.unlink(missing_ok=True)
            return False

    def limpiar_archivos_prueba(self):
        for archivo in self.scripts_dir.glob("ninja_op_e2e_*.py"):
            try:
                archivo.unlink()
            except OSError:
                pass
