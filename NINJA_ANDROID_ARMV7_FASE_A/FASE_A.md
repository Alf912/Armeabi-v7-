# Ninja Android ARMv7 — Fase A

## Estado
Núcleo base separado de la implementación anterior.

## Componentes
- `ninja/core.py` — SesCore
- `ninja/sanitizer.py` — SesSanitizer
- `ninja/validator.py` — SesClipboardValidator

## Regla
Los contratos funcionales relevantes de SES v2.6 se conservan.
No se incorpora todavía almacenamiento Android, ejecución aislada ni interfaz.

## Próxima fase
Servicios de persistencia e indexación, con almacenamiento desacoplado de
`./03_Scripts/`.
