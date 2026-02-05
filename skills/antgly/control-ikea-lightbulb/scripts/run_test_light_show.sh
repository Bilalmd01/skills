#!/usr/bin/env bash
# Helper to run the light_show test using the local .venv_kasa virtualenv
# Usage: ./run_test_light_show.sh --ip 192.168.4.69 --duration 6 --transition 1 --off-flash --verbose
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv_kasa"
PYTHON="$VENV_DIR/bin/python3"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$SCRIPT_DIR/light_show.py"
if [ ! -x "$PYTHON" ]; then
  echo "Virtualenv python not found at $PYTHON"
  echo "Create it with: ./scripts/bootstrap_venv.sh"
  exit 1
fi
# Forward all args to the script
"$PYTHON" "$SCRIPT" "$@"
