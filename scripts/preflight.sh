#!/usr/bin/env bash
set -euo pipefail
command -v adb >/dev/null 2>&1 || { echo "ADB_NOT_FOUND"; exit 20; }
adb version
adb devices -l
