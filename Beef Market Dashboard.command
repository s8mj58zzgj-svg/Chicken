#!/bin/bash
clear
echo ""
echo "  ============================================"
echo "  |                                          |"
echo "  |   BEEF & CATTLE MARKET INTELLIGENCE      |"
echo "  |                                          |"
echo "  ============================================"
echo ""
echo "  Starting up..."
cd "$(dirname "$0")"
PY=python3
if ! command -v $PY &> /dev/null; then
    echo "  ERROR: Python 3 not found."
    echo "  Install from https://www.python.org/downloads/"
    read -n 1; exit 1
fi
$PY -c "import flask" 2>/dev/null || $PY -m pip install flask --quiet
echo "  Launching in your browser..."
echo "  To stop: close this window"
echo ""
$PY BeefDashboard.py
