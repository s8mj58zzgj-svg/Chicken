# ==================================================
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

        # Check cache
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

    def fetch_usda_nass(self, params):
        """Fetch USDA NASS QuickStats data"""
        try:
            url = "http://quickstats.nass.usda.gov/api/api_GET/"
            params['key'] = USDA_KEY
            params['format'] = 'JSON'

            r = self.session.get(url, params=params, timeout=10)
            if r.status_code == 200:
                return r.json().get('data', [])
            return []
        except Exception as e:
            print(f"USDA Error: {e}")
            return []

    def get_market_snapshot(self):
        """Get comprehensive market snapshot"""
        print(f"⚡ FETCHING MARKET DATA: {datetime.datetime.now().strftime('%H:%M:%S')}")

        # Fetch all key indicators in parallel concept
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
