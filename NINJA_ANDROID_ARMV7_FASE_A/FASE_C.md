# Ninja Android ARMv7 — Fase C

## Estado
COMPLETADA.

## Ejecutor

Se introduce `SesExecutor` con un contrato independiente del mecanismo de
aislamiento.

Resultados:
- `PASS`
- `FAIL`
- `SIN_CONTRATO`
- `EXCEPCION`
- `TIMEOUT`
- `PROCESO_SIN_RESPUESTA`

El límite nominal heredado del núcleo SES es de 3 segundos.

## Decisión importante

La fase no asume que `multiprocessing`/`fork`/`spawn` del v2.6 deba trasladarse
directamente a Android. El ejecutor queda desacoplado para que la integración
Android pueda seleccionar posteriormente el mecanismo de aislamiento apropiado.

El timeout basado en hilo no puede matar de forma segura un hilo Python que
quede ejecutándose. Por tanto, `TIMEOUT` en esta fase es un contrato de
detección, no una garantía de terminación forzada.

Antes de certificar Android se debe resolver el aislamiento real.
