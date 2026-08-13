"""Ninja Android ARMv7 - Input Validator.
Preserves the SES clipboard-input contract from v2.6.
"""


class SesClipboardValidator:
    def __init__(self):
        self.MAX_CHARACTER_LIMIT = 500000
        self.TOKEN_CIERRE = "```"
        self.buffer_temporal = ""

    def cargar_y_validar_entrada(self, texto_portapapeles: str) -> bool:
        if not isinstance(texto_portapapeles, str):
            self.buffer_temporal = ""
            return False

        if len(texto_portapapeles) > self.MAX_CHARACTER_LIMIT:
            self.buffer_temporal = ""
            return False

        self.buffer_temporal = texto_portapapeles
        texto_limpio = self.buffer_temporal.rstrip()

        if len(texto_limpio) < 3 or not texto_limpio.endswith(self.TOKEN_CIERRE):
            self.buffer_temporal = ""
            return False

        return True

    def extraer_bufer_validado(self) -> str:
        return self.buffer_temporal
