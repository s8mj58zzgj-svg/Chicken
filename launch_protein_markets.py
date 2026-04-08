"""
Simple launcher for Protein Markets Intelligence
Run this file in Pythonista to launch the protein markets dashboard
"""

import sys
import os

# Add current directory to Python path to ensure imports work in Pythonista
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from protein_markets_launcher import ProteinMarketsLauncher

if __name__ == '__main__':
    launcher = ProteinMarketsLauncher()
    launcher.present('fullscreen')
