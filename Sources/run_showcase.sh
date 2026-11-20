#!/usr/bin/env bash
# ===============================================================================
#   Discord Phishing Sentinel - Master Showcase Pipeline
#   Author: Edwin Lin (Team #18 - Solo Project)
# ===============================================================================

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "==============================================================================="
echo "  Discord Phishing Sentinel - Master Showcase Pipeline (Unix/macOS)"
echo "  Author: Edwin Lin (Team #18)"
echo "==============================================================================="
echo ""

if command -v python3 &>/dev/null; then
    python3 run_showcase_pipeline.py
elif command -v python &>/dev/null; then
    python run_showcase_pipeline.py
else
    echo "[ERROR] Python 3 was not found in PATH. Please install Python 3.10+."
    exit 1
fi
