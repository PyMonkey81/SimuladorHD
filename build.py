#!/usr/bin/env python3
"""Punto de entrada único: detecta el sistema operativo y ejecuta el script de build correspondiente."""
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    system = platform.system()
    if system == "Windows":
        script = ROOT / "build_exe.bat"
        cmd = [str(script)]
    elif system == "Linux":
        script = ROOT / "build_exe.sh"
        cmd = ["bash", str(script)]
    else:
        print(f"ERROR: Sistema operativo no soportado para build: {system}")
        return 1

    if not script.exists():
        print(f"ERROR: No se encontró el script de build: {script}")
        return 1

    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    sys.exit(main())
