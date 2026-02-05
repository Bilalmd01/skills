#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv_kasa"
PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  echo "python3 not found. Please install Python 3.9+"
  exit 2
fi
# Check Python version >= 3.9
PY_VER=$($PY -c 'import sys; print("%d.%d"%(sys.version_info.major, sys.version_info.minor))')
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 9 ]; }; then
  echo "Detected Python $PY_VER — python 3.9+ is required. Please install a newer Python."
  exit 2
fi
if [ -d "$VENV_DIR" ]; then
  echo "Virtualenv already exists at $VENV_DIR"
  exit 0
fi
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python3" -m pip install --upgrade pip
# Pin python-kasa to a minimum compatible version for reproducibility
"$VENV_DIR/bin/python3" -m pip install "python-kasa>=0.13.0"
echo "Created venv at $VENV_DIR"
