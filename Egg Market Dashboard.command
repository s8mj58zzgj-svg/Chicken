#!/bin/bash
# ============================================
# EGG MARKET INTELLIGENCE DASHBOARD
# Double-click this file to launch!
# ============================================

clear
echo "============================================"
echo "  EGG MARKET INTELLIGENCE DASHBOARD"
echo "  Starting up..."
echo "============================================"
echo ""

# Navigate to the folder where this script lives
cd "$(dirname "$0")"

# Use python3 (comes with macOS)
PYTHON=python3

# Check Python exists
if ! command -v $PYTHON &> /dev/null; then
    echo "ERROR: Python 3 not found."
    echo "Install from https://www.python.org/downloads/"
    echo ""
    echo "Press any key to close..."
    read -n 1
    exit 1
fi

# Install Flask if needed (one time)
$PYTHON -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Flask (one-time setup)..."
    $PYTHON -m pip install flask
    echo ""
fi

echo "Launching dashboard..."
echo "Your browser will open automatically."
echo ""
echo "To stop: close this window or press Ctrl+C"
echo ""

# Run the dashboard
$PYTHON EggDashboard.py
