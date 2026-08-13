#!/usr/bin/env bash
set -euo pipefail
if [ -x "./gradlew" ]; then
  ./gradlew :app:assembleDebug
elif command -v gradle >/dev/null 2>&1; then
  gradle wrapper --gradle-version 8.9
  ./gradlew :app:assembleDebug
else
  echo "ERROR: no hay gradlew ni gradle"
  exit 3
fi
