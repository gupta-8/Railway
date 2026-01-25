#!/usr/bin/env bash
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
RELOAD="${RELOAD:-1}"          # 1=dev (reload), 0=prod-like (no reload)
APP_MODULE="${APP_MODULE:-app.main:app}"

# Create venv only if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment in $VENV_DIR..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# Activate venv
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Install deps (idempotent; fast when already satisfied)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Build uvicorn args
UVICORN_ARGS=( "$APP_MODULE" --host "$HOST" --port "$PORT" )
if [ "$RELOAD" = "1" ]; then
  UVICORN_ARGS+=( --reload )
fi

echo "Starting server: uvicorn ${UVICORN_ARGS[*]}"
exec uvicorn "${UVICORN_ARGS[@]}"
