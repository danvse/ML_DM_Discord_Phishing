#!/usr/bin/env bash
# ===============================================================================
#   Starting Discord Sentinel - Angular 18 Frontend Portal (Port 4200)
# ===============================================================================

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "[INFO] First-time setup: Installing frontend dependencies via npm..."
    npm install
fi

echo "[INFO] Launching Angular 18 dev server at http://localhost:4200/ ..."
npx ng serve --host 127.0.0.1 --port 4200
