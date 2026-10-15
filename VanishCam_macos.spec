"""PyInstaller build de l'app macOS (VanishCam.app, Apple Silicon)."""

from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs


root = Path(SPECPATH).resolve()
icon_file = root / "assets" / "vanish_icon.icns"
resources = [
    (root / "hand_landmarker.task", "."),
    (root / "models" / "gesture_recognizer.task", "models"),
    (root / "models" / "selfie_segmenter_landscape.tflite", "models"),
    (root / "assets" / "substitution_log.png", "assets"),
    (root / "assets" / "vanish.MP3", "assets"),
]
missing = [str(path) for path, _ in resources if not path.is_file()]
if not icon_file.is_file():
    missing.append(str(icon_file))
if missing:
    raise SystemExit("Fichiers nécessaires au build manquants :\n" + "\n".join(missing))

a = Analysis(
    [str(root / "vanish_cam.py")],
    pathex=[str(root)],
    binaries=collect_dynamic_libs("mediapipe"),
    datas=[(str(path), destination) for path, destination in resources],
    hiddenimports=["pygame.mixer", "mediapipe.tasks.c", "macos_support"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

# Build "onedir" : c'est le format recommandé pour un .app (démarrage plus
# rapide, signature fiable), contrairement au "onefile" utilisé sous Windows.
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VanishCam",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="VanishCam",
)
app = BUNDLE(
    coll,
    name="VanishCam.app",
    icon=str(icon_file),
    bundle_identifier="com.vanishcam.mac",
    info_plist={
        "CFBundleName": "VanishCam",
        "CFBundleDisplayName": "VanishCam",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1.0.0",
        "LSMinimumSystemVersion": "13.0",
        "NSHighResolutionCapable": True,
        # Obligatoire : sans cette clé, macOS refuse l'accès à la webcam.
        "NSCameraUsageDescription": (
            "VanishCam uses the webcam to detect your hands and apply the "
            "vanish effect. Video stays on your Mac."
        ),
    },
)
