#!/bin/bash
# Instalador APK Ninja Android ARMv7 — Todas las Fases Integradas

set -e

APK_PATH="/workspaces/Armeabi-v7-/NINJA_ANDROID_ARMV7_FASE_A/app/build/outputs/apk/debug/app-debug.apk"

if [ ! -f "$APK_PATH" ]; then
    echo "❌ ERROR: APK no encontrado en $APK_PATH"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  INSTALADOR APK: Ninja Android ARMv7"
echo "  Todas las Fases (A→G) Integradas"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 APK: $(basename "$APK_PATH")"
echo "📏 Tamaño: $(ls -lh "$APK_PATH" | awk '{print $5}')"
echo "🏗️  Arquitectura: 32-bits ARMv7 (armeabi-v7a)"
echo "🐍 Python: 3.11 (Chaquopy)"
echo ""

# Verificar que adb está disponible
if ! command -v adb &> /dev/null; then
    echo "❌ ERROR: adb no encontrado. Instala Android SDK Platform-Tools"
    exit 1
fi

# Verificar dispositivos conectados
echo "🔍 Buscando dispositivos Android..."
DEVICES=$(adb devices | grep -v "List of attached devices" | grep "device$")

if [ -z "$DEVICES" ]; then
    echo "⚠️  ADVERTENCIA: No hay dispositivos/emuladores conectados"
    echo ""
    echo "Para conectar un dispositivo:"
    echo "  1. Habilita 'USB Debugging' en Ajustes > Opciones de Desarrollador"
    echo "  2. Conecta el dispositivo USB"
    echo "  3. Ejecuta: adb devices"
    echo ""
    echo "Para usar un emulador:"
    echo "  1. Abre Android Studio"
    echo "  2. AVD Manager → Crear emulador ARMv7 (API 24+)"
    echo "  3. Inicia el emulador"
    exit 1
fi

echo "✅ Dispositivos encontrados:"
adb devices

echo ""
echo "📥 Instalando APK..."
adb install -r "$APK_PATH"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ INSTALACIÓN COMPLETADA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Próximos pasos:"
echo "  1. Abre la app: Ninja Android"
echo "  2. Verifica que todas las fases están activas"
echo "  3. Prueba con Markdown + Python embebido"
echo ""
echo "Para ver logs en tiempo real:"
echo "  adb logcat | grep NinjaAndroid"
echo ""
