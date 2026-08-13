# Ninja Android ARMv7 — Fase E

## Estado
COMPLETADA.

## Objetivo

Crear la frontera entre Android y el motor Python sin introducir dependencias
Android dentro del núcleo.

## Componentes

- `android/host.py`
  - recibe el directorio privado de archivos de la aplicación;
  - crea `files/ninja`;
  - inyecta esa raíz en `SesStorage` mediante `create_default_engine()`.

- `android/bridge.py`
  - expone `process_markdown()`;
  - transforma `EngineResult` en una respuesta estable para la interfaz.

- `android/AndroidManifest.xml`
  - especificación mínima del host Android.

- `android/build.gradle.spec`
  - documento de diseño del build;
  - no fija todavía ABI ni versiones.

## Regla

El núcleo `ninja/` no conoce Android.

## Pendiente

La Fase E no certifica un APK. No contiene todavía una configuración final de
Gradle/Chaquopy ni ABI. Esas decisiones pertenecen a la Fase F.
