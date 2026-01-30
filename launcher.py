"""
Simple launcher for Chicken Market Intelligence
Run this file in Pythonista to launch the dashboard
"""

from chicken_market_launcher import ChickenMarketLauncher

if __name__ == '__main__':
    launcher = ChickenMarketLauncher()
    launcher.present('fullscreen')
