#!/usr/bin/env bash
set -e

VENV_DIR=".venv"
PYTHON_BIN="python3"

# Create virtual environment only if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  $PYTHON_BIN -m venv $VENV_DIR
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Reload toggle (default: enabled for dev)
RELOAD_FLAG=""
if [ "${RELOAD:-1}" = "1" ]; then
  RELOAD_FLAG="--reload"
fi

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 $RELOAD_FLAG
