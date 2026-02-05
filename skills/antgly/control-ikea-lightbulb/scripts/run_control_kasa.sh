#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv_kasa"
PY="$VENV_DIR/bin/python3"
BOOTSTRAP="$ROOT_DIR/scripts/bootstrap_venv.sh"
SCRIPT="$ROOT_DIR/scripts/control_kasa_light.py"

# If venv missing, try to bootstrap it
if [ ! -x "$PY" ]; then
  echo "Virtualenv not found at $VENV_DIR — attempting to bootstrap..."
  if [ -x "$BOOTSTRAP" ]; then
    "$BOOTSTRAP"
  else
    echo "Bootstrap script missing: $BOOTSTRAP"
    echo "You can create a venv manually or run the control script with a Python that has python-kasa installed."
    exit 1
  fi
fi

# Execute
"$PY" "$SCRIPT" "$@"
