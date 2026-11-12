#!/usr/bin/env bash
# macOS bundle naming for the staff client. Run from the repo root after apply.py.
# The bundle and its executable must be named after APP_NAME: src/platform/macos.rs builds
# /Applications/<APP_NAME>.app and the launchd plists from get_app_name().
set -euo pipefail
NAME="${1:?usage: apply_macos.sh <AppName>}"
[[ "$NAME" =~ ^[A-Za-z0-9_][A-Za-z0-9_-]*$ ]] || { echo "bad name: $NAME" >&2; exit 1; }
perl -pi -e "s/^PRODUCT_NAME = .*/PRODUCT_NAME = ${NAME}/" flutter/macos/Runner/Configs/AppInfo.xcconfig
perl -pi -e "s/RustDesk\.app/${NAME}.app/g" flutter/macos/Runner.xcodeproj/project.pbxproj build.py
grep -q "PRODUCT_NAME = ${NAME}" flutter/macos/Runner/Configs/AppInfo.xcconfig
grep -q "${NAME}.app/Contents/MacOS" build.py
echo "macOS bundle -> ${NAME}.app"
