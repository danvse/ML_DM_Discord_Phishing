#!/usr/bin/env bash
# ===============================================================================
#   Starting Discord Sentinel - FastAPI Backend Server (Port 8000)
# ===============================================================================

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR/backend"

if command -v python3 &>/dev/null; then
    python3 -m uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
elif command -v python &>/dev/null; then
    python -m uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
else
    echo "[ERROR] Python 3 was not found in PATH."
    exit 1
fi
