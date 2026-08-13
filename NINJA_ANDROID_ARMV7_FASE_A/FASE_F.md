# Ninja Android ARMv7 — Fase F

## Estado
CONFIGURACIÓN COMPLETADA — BUILD REAL PENDIENTE.

## Objetivo

Fijar una única configuración Android para `armeabi-v7a`, sin variantes.

## Decisiones

- Chaquopy: 17.0.0.
- Python: 3.11.
- ABI: `armeabi-v7a` exclusivamente.
- minSdk: 24.
- targetSdk: 35.
- Android Gradle Plugin: 8.7.3.
- El código Python se coloca en `app/src/main/python`, que es el source set
  estándar de Chaquopy.
- El núcleo no utiliza `multiprocessing`.

## Motivo Python 3.11

Chaquopy 17.0 documenta que `armeabi-v7a` solo está disponible con Python
3.11 y anteriores. Python 3.12+ es exclusivamente 64-bit.

## Importante

Esta fase fija la configuración, pero NO declara un APK compilado ni
certificado. La compilación real requiere un entorno Android/Gradle con los
SDK correspondientes.

## Archivos

- `settings.gradle`
- `build.gradle`
- `app/build.gradle`
- `app/src/main/AndroidManifest.xml`
- `app/src/main/python/ninja/*`
- `app/src/main/java/com/ninja/android/MainActivity.java`
- `gradle.properties`
