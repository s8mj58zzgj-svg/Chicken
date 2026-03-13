#!/bin/bash
# =============================================
#  BEEF & CATTLE MARKET INTELLIGENCE DASHBOARD
#  Double-click this file to launch!
# =============================================

clear
echo ""
echo "  ============================================"
echo "  |                                          |"
echo "  |   BEEF & CATTLE MARKET INTELLIGENCE      |"
echo "  |   A+ Dashboard                           |"
echo "  |                                          |"
echo "  ============================================"
echo ""
echo "  Starting up... please wait..."
echo ""

# Go to the folder this script is in
cd "$(dirname "$0")"

# Find Python 3
if command -v python3 &> /dev/null; then
    PY=python3
elif command -v python &> /dev/null; then
    PY=python
else
    echo "  ERROR: Python not found on this Mac."
    echo ""
    echo "  To fix this:"
    echo "  1. Go to https://www.python.org/downloads/"
    echo "  2. Download and install Python 3"
    echo "  3. Then double-click this file again"
    echo ""
    echo "  Press any key to close..."
    read -n 1
    exit 1
fi

echo "  Using: $($PY --version)"
echo ""

# Install Flask if needed (one time)
$PY -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "  First-time setup: installing Flask..."
    echo "  (This only happens once)"
    echo ""
    $PY -m pip install flask --quiet
    if [ $? -ne 0 ]; then
        $PY -m pip install flask --user --quiet
    fi
    echo ""
    echo "  Flask installed!"
    echo ""
fi

# Check that templates folder exists
if [ ! -f "templates/beef.html" ]; then
    echo "  ERROR: templates/beef.html not found."
    echo "  Make sure the 'templates' folder is in the same"
    echo "  directory as this file and BeefDashboard.py"
    echo ""
    echo "  Press any key to close..."
    read -n 1
    exit 1
fi

echo "  Launching dashboard in your browser..."
echo ""
echo "  ============================================"
echo "  |  Dashboard running at:                   |"
echo "  |  http://localhost:5051                    |"
echo "  |                                          |"
echo "  |  To stop: close this window              |"
echo "  ============================================"
echo ""

# Run the dashboard
$PY BeefDashboard.py
