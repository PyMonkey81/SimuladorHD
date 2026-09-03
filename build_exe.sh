#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "$0")"

SKIP_SMOKE="${SKIP_SMOKE:-0}"
CI_MODE="${CI:-0}"

echo "==============================================="
echo "COMPILANDO SIMULADOR HD-2026 EXE (Linux)"
echo "==============================================="

# Activar entorno virtual
PYTHON_EXE=""
if [ -f ".venv-1/bin/activate" ]; then
    # shellcheck disable=SC1091
    source ".venv-1/bin/activate"
elif [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source ".venv/bin/activate"
fi

if [ -n "${VIRTUAL_ENV:-}" ]; then
    PYTHON_EXE="$VIRTUAL_ENV/bin/python"
else
    PYTHON_EXE="python3"
fi

# Limpiar todo (incluyendo caché de PyInstaller)
echo
echo "Limpiando builds anteriores y caché..."
if [ -d "dist" ]; then
    rm -rf dist
    if [ -d "dist" ]; then
        echo "ERROR: No se pudo limpiar dist/ porque hay archivos en uso."
        echo "Cierra cualquier proceso que tenga abierto el binario en dist/ e intenta de nuevo."
        exit 1
    fi
fi
rm -rf build
rm -rf __pycache__
# Borra caché global de PyInstaller (importante)
rm -rf "$HOME/.cache/pyinstaller"

# Elimina el paquete "serial" (distinto de pyserial) que sobrescribe serial/__init__.py
"$PYTHON_EXE" -m pip uninstall -y serial >/dev/null 2>&1

echo
echo "Instalando/actualizando dependencias..."
"$PYTHON_EXE" -m pip install --force-reinstall --no-cache-dir -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias."
    exit 1
fi

if [ "$SKIP_SMOKE" = "0" ] && [ -f "tests/smoke_startup.py" ]; then
    echo
    echo "Ejecutando smoke test de arranque/cierre..."
    export SIMULADORHD_SMOKE_TEST_SECONDS=2
    export QT_QPA_PLATFORM=offscreen
    "$PYTHON_EXE" tests/smoke_startup.py
    if [ $? -ne 0 ]; then
        echo "Smoke test falló. Cancelando build."
        exit 1
    fi
fi

echo
echo "Compilando ejecutable LIMPIO..."
"$PYTHON_EXE" -m PyInstaller --clean --noconfirm HemodialisisApp.spec
if [ $? -ne 0 ]; then
    echo "ERROR: PyInstaller no pudo generar el ejecutable."
    exit 1
fi

if [ -d "config" ]; then
    mkdir -p "dist/config"
    cp -r config/. dist/config/
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo copiar la configuracion a dist/config/."
        exit 1
    fi
fi

echo
echo "==============================================="
echo "COMPILACION FINALIZADA"
echo "==============================================="

LAST_EXE=""
for f in dist/*; do
    [ -f "$f" ] && [ -x "$f" ] && LAST_EXE="$(basename "$f")"
done
if [ -n "$LAST_EXE" ]; then
    echo "Ejecutable generado en: dist/$LAST_EXE"
else
    echo "No se encontro ejecutable en dist/"
fi

if [ -f "build/build_history.csv" ]; then
    echo "Registro actualizado en: build/build_history.csv"
fi

echo
if [ "$CI_MODE" = "0" ]; then
    read -r -p "Presiona Enter para continuar..." _
fi
