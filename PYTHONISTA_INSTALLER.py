"""
PYTHONISTA INSTALLER
====================
Copy this entire file into Pythonista and run it.
It will create all necessary files for the Chicken Market Intelligence app.
"""

import os

print("🐔 Installing Chicken Market Intelligence Platform...")
print("=" * 50)

# File contents as strings
FILES = {
    'config.py': '''# ==================================================
# CONFIGURATION - API Keys & Theme
# ==================================================

# API Configuration
USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

# Layout Constants
MARGIN = 40

# Color Theme
THEME = {
    'bg': '#050505',
    'panel': '#121212',
    'header': '#1a1a1a',
    'text': '#e0e0e0',
    'sub': '#888888',
    'bull': '#00ff88',
    'bear': '#ff4444',
    'warn': '#ffaa00',
    'macro': '#aa00ff',
    'bio': '#ff0088',
    'cold': '#00ccff',
    'risk': '#ff3333',
    'trade': '#0099ff',
    'gold': '#ffd700',
    'logistics': '#ff9900',
    'eggs': '#ffdd44',
    'layer': '#ff6b9d',
    'accent': '#00ccff',
    'neutral': '#888888'
}

# FRED Series IDs
FRED_SERIES = {
    'corn': 'PMAIZMTUSDM',
    'soybean': 'PSOYBUSDM',
    'wheat': 'PWHEAMTUSDM',
    'beef': 'APU0000FC1101',
    'pork': 'APU0000FD3101',
    'diesel': 'GASDESW',
    'crude': 'DCOILWTICO',
    'natgas': 'DHHNGSP',
    'cpi': 'CPIAUCSL',
    'ppi_food': 'WPU02',
    'employment': 'PAYEMS',
    'consumer_sentiment': 'UMCSENT',
    'restaurant_sales': 'RRSFS',
    'grocery_sales': 'RSGASS',
    'egg_price_index': 'WPU01740301',
    'egg_retail': 'APU0000708111',
}
''',

    'data_engine.py': '''# ==================================================
# DATA ENGINE - Centralized Data Fetching & Caching
# ==================================================

import requests
import datetime
import time
from config import USDA_KEY, FRED_KEY, FRED_SERIES

class DataEngine:
    """Centralized data engine with caching and error handling"""

    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.cache_duration = 300  # 5 minutes

    def fetch_fred(self, series_id, limit=12):
        """Fetch data from FRED API with caching"""
        cache_key = f"fred_{series_id}"

        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                return cached_data

        try:
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': series_id,
                'api_key': FRED_KEY,
                'file_type': 'json',
                'limit': limit,
                'sort_order': 'desc'
            }
            r = self.session.get(url, params=params, timeout=8)

            if r.status_code == 200:
                data = r.json().get('observations', [])
                if data:
                    vals = [float(x['value']) for x in data if x['value'] != '.']
                    if vals:
                        result = (vals[0], vals[::-1])
                        self.cache[cache_key] = (time.time(), result)
                        return result

            return 0.0, []
        except Exception as e:
            print(f"FRED Error ({series_id}): {e}")
            return 0.0, []

    def get_market_snapshot(self):
        """Get comprehensive market snapshot"""
        print(f"⚡ FETCHING MARKET DATA: {datetime.datetime.now().strftime('%H:%M:%S')}")

        corn_latest, corn_hist = self.fetch_fred(FRED_SERIES['corn'])
        soy_latest, soy_hist = self.fetch_fred(FRED_SERIES['soybean'])
        diesel_latest, diesel_hist = self.fetch_fred(FRED_SERIES['diesel'])
        egg_ppi_latest, egg_ppi_hist = self.fetch_fred(FRED_SERIES['egg_price_index'])
        egg_retail_latest, egg_retail_hist = self.fetch_fred(FRED_SERIES['egg_retail'])

        return {
            'corn': {'current': corn_latest if corn_latest > 0 else 215.0, 'history': corn_hist},
            'soybean': {'current': soy_latest if soy_latest > 0 else 450.0, 'history': soy_hist},
            'diesel': {'current': diesel_latest if diesel_latest > 0 else 3.85, 'history': diesel_hist},
            'egg_ppi': {'current': egg_ppi_latest if egg_ppi_latest > 0 else 165.0, 'history': egg_ppi_hist},
            'egg_retail': {'current': egg_retail_latest if egg_retail_latest > 0 else 3.25, 'history': egg_retail_hist},
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'date': datetime.date.today()
        }

    def calculate_forecast_dates(self):
        """Calculate 30/60/90 day forecast dates"""
        today = datetime.date.today()
        return {
            'd30': (today + datetime.timedelta(days=30)).strftime("%b %d"),
            'd60': (today + datetime.timedelta(days=60)).strftime("%b %d"),
            'd90': (today + datetime.timedelta(days=90)).strftime("%b %d"),
            'today': today.strftime("%b %d, %Y")
        }
'''
}

# Create files
for filename, content in FILES.items():
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✅ Created {filename}")

print("\n" + "=" * 50)
print("🎉 Installation Complete!")
print("\nCore files installed:")
print("  - config.py")
print("  - data_engine.py")
print("\n⚠️  Note: This is a minimal install.")
print("For full dashboards, you need:")
print("  - ui_components.py")
print("  - main.py")
print("  - poultry_dashboard.py")
print("  - egg_dashboard.py")
print("\nWould you like me to create an installer for those too?")
