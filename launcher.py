"""
Simple launcher for Protein Dashboard
Run this file in Pythonista to launch the dashboard
"""

import sys
import os

# Add current directory to Python path to ensure imports work in Pythonista
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from protein_dashboard_launcher import ProteinDashboardLauncher

if __name__ == '__main__':
    launcher = ProteinDashboardLauncher()
    launcher.present('fullscreen')
