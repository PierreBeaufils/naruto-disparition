#!/bin/bash
# Construit dist/VanishCam.app et dist/VanishCam.dmg (Mac Apple Silicon uniquement).
set -euo pipefail
cd "$(dirname "$0")"

if [ "$(uname -m)" != "arm64" ]; then
  echo "Ce build nécessite un Mac Apple Silicon (MediaPipe n'existe pas pour Mac Intel)."
  exit 1
fi

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Python 3 introuvable. Installez-le depuis https://www.python.org/downloads/macos/"
  exit 1
fi

VENV=".venv-build"
if [ ! -x "$VENV/bin/python" ]; then
  echo "Création de l'environnement de build..."
  "$PYTHON" -m venv "$VENV"
fi
PY="$VENV/bin/python"

if ! "$PY" -c "import PyInstaller, cv2, mediapipe, numpy, pyvirtualcam, pygame" >/dev/null 2>&1; then
  echo "Installation des dépendances de build..."
  "$PY" -m pip install --upgrade pip
  "$PY" -m pip install -r requirements.txt "pyinstaller>=6,<7"
fi

if [ ! -f models/gesture_recognizer.task ] || [ ! -f models/selfie_segmenter_landscape.tflite ]; then
  echo "Téléchargement des modèles MediaPipe..."
  "$PY" -c "from vanish_cam import download_models; download_models()"
fi

rm -rf build dist/VanishCam dist/VanishCam.app dist/VanishCam.dmg
"$PY" -m PyInstaller --noconfirm --distpath dist --workpath build VanishCam_macos.spec

# Signature ad hoc de tout le bundle (obligatoire sur Apple Silicon).
codesign --force --deep --sign - dist/VanishCam.app

echo "Self-test du bundle..."
dist/VanishCam.app/Contents/MacOS/VanishCam --self-test

echo "Création du DMG..."
STAGING="$(mktemp -d)"
cp -R dist/VanishCam.app "$STAGING/"
cp "Lancer VanishCam (Terminal).command" "$STAGING/" 2>/dev/null || true
ln -s /Applications "$STAGING/Applications"
hdiutil create -volname "VanishCam" -srcfolder "$STAGING" -ov -format UDZO dist/VanishCam.dmg >/dev/null
rm -rf "$STAGING"

echo
echo "Prêt : dist/VanishCam.app et dist/VanishCam.dmg"
