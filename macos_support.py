"""Support spécifique au .app macOS.

Une app lancée depuis le Finder n'a pas de terminal : les messages que la
version Windows affiche dans la console (acquisition du fond, erreurs) seraient
perdus. Ce module, inactif hors .app macOS, les redirige vers un fichier de log,
relaie les messages clés en notifications et affiche les erreurs fatales dans
une boîte de dialogue.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

LOG_PATH = Path.home() / "Library" / "Logs" / "VanishCam" / "vanishcam.log"

# Messages console relayés en notification macOS (le reste ne va que dans le log).
NOTIFY_MARKERS = (
    "Step out of frame",
    "Background ready",
    "Virtual output active",
    "Virtual webcam unavailable",
)


def _is_macos_app_without_terminal() -> bool:
    return (
        sys.platform == "darwin"
        and getattr(sys, "frozen", False)
        and not (sys.stdout and sys.stdout.isatty())
    )


def _osascript(script: str, wait: bool = False) -> None:
    try:
        process = subprocess.Popen(
            ["osascript", "-e", script],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if wait:
            process.wait()
    except OSError:
        pass


def _quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def notify(message: str) -> None:
    _osascript(f"display notification {_quote(message)} with title \"VanishCam\"")


class _NotifyingLog:
    """Écrit dans le fichier de log et notifie les lignes importantes."""

    def __init__(self, stream):
        self.stream = stream
        self.pending = ""

    def write(self, text: str) -> int:
        self.stream.write(text)
        self.pending += text
        while "\n" in self.pending:
            line, self.pending = self.pending.split("\n", 1)
            if any(marker in line for marker in NOTIFY_MARKERS):
                notify(line.replace("[Webcam]", "").strip()[:200])
        return len(text)

    def flush(self) -> None:
        self.stream.flush()

    def isatty(self) -> bool:
        return False


def setup_macos_app() -> None:
    if not _is_macos_app_without_terminal():
        return
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        stream = LOG_PATH.open("a", encoding="utf-8", buffering=1)
    except OSError:
        return
    sys.stdout = _NotifyingLog(stream)
    sys.stderr = stream


def report_fatal_error(error: BaseException) -> None:
    if not _is_macos_app_without_terminal():
        return
    message = f"{error}\n\nLog: {LOG_PATH}"
    _osascript(
        f"display dialog {_quote(message)} with title \"VanishCam\" "
        "buttons {\"OK\"} default button \"OK\" with icon stop",
        wait=True,
    )
