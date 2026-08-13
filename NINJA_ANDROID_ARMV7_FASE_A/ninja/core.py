"""Ninja Android ARMv7 - SES Core.
Derived from SES v2.6 contracts; platform-independent.
"""

import threading


class SesCore:
    def __init__(self):
        self._mutex = threading.Lock()
        self.SYSTEM_LOCKED = False
        self.MOTOR_STATUS = "LIBRE"
        self.last_error = "NINGUNO"

    def ejecutar_orden(self, payload: dict) -> dict:
        if self.SYSTEM_LOCKED:
            return {
                "MOTOR": "PROCESANDO",
                "SYSTEM_LOCKED": True,
                "LAST_ERROR": "ERROR_CORRUPT_027",
            }

        if not self._mutex.acquire(blocking=False):
            return {
                "MOTOR": "PROCESANDO",
                "SYSTEM_LOCKED": True,
                "LAST_ERROR": "ERROR_CORRUPT_027",
            }

        self.SYSTEM_LOCKED = True
        self.MOTOR_STATUS = "PROCESANDO"

        try:
            if payload.get("error") and payload.get("error") != "NINGUNO":
                raise ValueError(payload.get("error"))

            self.SYSTEM_LOCKED = False
            self.MOTOR_STATUS = "LIBRE"
            return {
                "MOTOR": self.MOTOR_STATUS,
                "SYSTEM_LOCKED": self.SYSTEM_LOCKED,
                "LAST_ERROR": "NINGUNO",
            }
        except Exception as exc:
            self.SYSTEM_LOCKED = False
            self.MOTOR_STATUS = "LIBRE"
            self.last_error = str(exc) or "ERROR_SYS_028"
            return {
                "MOTOR": self.MOTOR_STATUS,
                "SYSTEM_LOCKED": self.SYSTEM_LOCKED,
                "LAST_ERROR": self.last_error,
            }
        finally:
            if self._mutex.locked():
                self._mutex.release()
