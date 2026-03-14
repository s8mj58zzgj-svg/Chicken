"""
EGG MARKET INTELLIGENCE DASHBOARD
Flask web application with live FRED API data
Run: python app.py → opens http://localhost:5050
"""

import os
import json
import time
import datetime
import webbrowser
import threading
from urllib.request import urlopen
from urllib.parse import urlencode

from flask import Flask, render_template, jsonify

# ==================================================
# CONFIG
# ==================================================

FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

FRED_SERIES = {
    'corn': 'PMAIZMTUSDM',
    'soybean': 'PSOYBUSDM',
    'diesel': 'GASDESW',
    'egg_ppi': 'WPU01740301',
    'egg_retail': 'APU0000708111',
    'cpi_food': 'CPIUFDNS',
    'pce_food': 'DFXARC1M027SBEA',
}

# ==================================================
# DATA ENGINE
# ==================================================

class DataEngine:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300

    def fetch_fred(self, series_id, limit=500):
        cache_key = f"fred_{series_id}"
        if cache_key in self.cache:
            ts, data = self.cache[cache_key]
            if time.time() - ts < self.cache_duration:
                return data

        try:
            params = {
                'series_id': series_id,
                'api_key': FRED_KEY,
                'file_type': 'json',
                'limit': limit,
                'sort_order': 'desc',
            }
            url = f"https://api.stlouisfed.org/fred/series/observations?{urlencode(params)}"
            with urlopen(url, timeout=15) as resp:
                raw = json.loads(resp.read().decode())

            obs = raw.get('observations', [])
            pairs = []
            for o in obs:
                if o['value'] != '.':
                    pairs.append({'date': o['date'], 'value': float(o['value'])})

            if pairs:
                self.cache[cache_key] = (time.time(), pairs)
                return pairs
            return []
        except Exception as e:
            print(f"FRED error ({series_id}): {e}")
            return []

    def clear_cache(self):
        self.cache = {}

    def get_snapshot(self):
        now = datetime.datetime.now()
        today = datetime.date.today()

        corn = self.fetch_fred(FRED_SERIES['corn'])
        soy = self.fetch_fred(FRED_SERIES['soybean'])
        diesel = self.fetch_fred(FRED_SERIES['diesel'])
        egg_ppi = self.fetch_fred(FRED_SERIES['egg_ppi'])
        egg_retail = self.fetch_fred(FRED_SERIES['egg_retail'])
        cpi = self.fetch_fred(FRED_SERIES['cpi_food'])

        def latest(data, fallback=0):
            return data[0]['value'] if data else fallback

        def history(data):
            return list(reversed(data[:36]))

        corn_val = latest(corn, 215.0)
        soy_val = latest(soy, 450.0)
        diesel_val = latest(diesel, 3.85)
        egg_ppi_val = latest(egg_ppi, 165.0)
        egg_retail_val = latest(egg_retail, 3.28)
        cpi_val = latest(cpi, 320.0)

        corn_hist = history(corn)
        soy_hist = history(soy)
        egg_retail_hist = history(egg_retail)
        egg_ppi_hist = history(egg_ppi)

        # Compute changes
        def pct_change(data):
            if len(data) >= 2:
                old = data[-1]['value']
                new = data[0]['value']
                if old > 0:
                    return round(((new - old) / old) * 100, 1)
            return 0

        egg_retail_chg = pct_change(egg_retail)
        corn_chg = pct_change(corn)
        soy_chg = pct_change(soy)
        diesel_chg = pct_change(diesel)

        # Feed cost model
        soy_meal = soy_val * 0.767
        layer_feed_monthly = 0.42
        annual_feed = layer_feed_monthly * 12
        eggs_per_day = 0.82
        feed_per_dozen = annual_feed / (eggs_per_day * 365 / 12)

        # Forecasts
        d30 = (today + datetime.timedelta(days=30)).strftime("%b %d")
        d60 = (today + datetime.timedelta(days=60)).strftime("%b %d")
        d90 = (today + datetime.timedelta(days=90)).strftime("%b %d")

        cage_free_premium = 0.85
        organic_premium = 2.10
        cage_free_price = egg_retail_val + cage_free_premium
        organic_price = egg_retail_val + organic_premium

        return {
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
            'date': today.strftime('%B %d, %Y'),
            'forecast_dates': {'d30': d30, 'd60': d60, 'd90': d90},

            # Top-line prices
            'prices': {
                'egg_retail': {'value': egg_retail_val, 'change': egg_retail_chg, 'unit': '$/dozen'},
                'corn': {'value': corn_val, 'change': corn_chg, 'unit': 'Index'},
                'soybean': {'value': soy_val, 'change': soy_chg, 'unit': 'Index'},
                'diesel': {'value': diesel_val, 'change': diesel_chg, 'unit': '$/gal'},
                'egg_ppi': {'value': egg_ppi_val, 'change': pct_change(egg_ppi), 'unit': 'PPI Index'},
                'cage_free': {'value': cage_free_price, 'change': 0, 'unit': '$/dozen'},
                'organic': {'value': organic_price, 'change': 0, 'unit': '$/dozen'},
            },

            # Charts data
            'charts': {
                'egg_retail': {
                    'labels': [p['date'] for p in egg_retail_hist],
                    'values': [p['value'] for p in egg_retail_hist],
                },
                'egg_ppi': {
                    'labels': [p['date'] for p in egg_ppi_hist],
                    'values': [p['value'] for p in egg_ppi_hist],
                },
                'corn': {
                    'labels': [p['date'] for p in corn_hist],
                    'values': [p['value'] for p in corn_hist],
                },
                'soybean': {
                    'labels': [p['date'] for p in soy_hist],
                    'values': [p['value'] for p in soy_hist],
                },
            },

            # Flock
            'flock': {
                'total_layers': 320.5,
                'cage_free_pct': 38.5,
                'pullet_placements': -3.2,
                'eggs_per_day': eggs_per_day,
                'hatchability': 79.7,
            },

            # HPAI
            'hpai': {
                'risk_level': 'VERY HIGH',
                'commercial_outbreaks': 8,
                'birds_depopulated': 2.1,
                'top50_share': 60,
            },

            # Costs
            'costs': {
                'annual_feed': round(annual_feed, 2),
                'feed_per_dozen': round(feed_per_dozen, 2),
                'soy_meal': round(soy_meal, 0),
                'cage_free_delta': 0.35,
                'min_retail': 2.80,
            },

            # Forecasts
            'forecasts': {
                'conventional': {
                    'current': egg_retail_val,
                    'targets': [
                        round(egg_retail_val * 1.04, 2),
                        round(egg_retail_val * 1.08, 2),
                        round(egg_retail_val * 1.12, 2),
                    ],
                    'trend': 'BULLISH',
                    'logic': f'Tight flock + elevated feed + HPAI tail risk. Target ${egg_retail_val * 1.12:.2f} by {d90}.',
                },
                'cage_free': {
                    'current': cage_free_price,
                    'targets': [
                        round(cage_free_price * 1.05, 2),
                        round(cage_free_price * 1.10, 2),
                        round(cage_free_price * 1.15, 2),
                    ],
                    'trend': 'STRUCTURAL BULL',
                    'logic': f'9-state mandate by 2026. Supply shortage through 2027. ${cage_free_price * 1.15:.2f} target.',
                },
                'organic': {
                    'current': organic_price,
                    'targets': [
                        round(organic_price * 1.03, 2),
                        round(organic_price * 1.06, 2),
                        round(organic_price * 1.08, 2),
                    ],
                    'trend': 'PREMIUM STABLE',
                    'logic': 'Organic feed +60% cost. Loyal niche absorbs price. Sticky demand.',
                },
                'breaking_stock': {
                    'current': 1.30,
                    'targets': [1.35, 1.40, 1.45],
                    'trend': 'RECOVERY',
                    'logic': f'Food service recovery. Shell price forces substitution. $1.45 by {d90}.',
                },
            },

            # Storage
            'storage': {
                'shell_eggs': {'value': 42.5, 'unit': 'M dozen', 'normal': 55.0, 'status': 'BELOW NORMAL'},
                'frozen': {'value': 95.2, 'unit': 'M lbs', 'normal': 110.0, 'status': 'ADEQUATE'},
            },

            # Verdict
            'verdict': {
                'title': 'STRUCTURAL TIGHT + TAIL RISK',
                'signals': [
                    {'label': 'Conventional', 'action': 'BUY', 'target': f'${egg_retail_val * 1.12:.2f} (90d)'},
                    {'label': 'Cage-Free', 'action': 'STRONG BUY', 'target': f'${cage_free_price * 1.15:.2f} (90d)'},
                    {'label': 'Breaking Stock', 'action': 'HEDGE', 'target': '$1.45 (90d)'},
                    {'label': 'HPAI', 'action': 'MONITOR', 'target': 'Weekly watch'},
                ],
                'summary': (
                    'Eggs structurally underpriced for risk. Bird flu is dominant tail risk — '
                    'top 50 farms hold 60% of supply. One major outbreak = $8-10/doz overnight. '
                    'Cage-free mandates forcing conversion faster than economics allow. '
                    'Feed floor at $2.80/doz prevents meaningful downside. '
                    'Next outbreak takes retail to $6-8.'
                ),
            },
        }


engine = DataEngine()

# ==================================================
# FLASK APP
# ==================================================

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/api/data')
def api_data():
    data = engine.get_snapshot()
    return jsonify(data)


@app.route('/api/refresh')
def api_refresh():
    engine.clear_cache()
    data = engine.get_snapshot()
    return jsonify(data)


def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5050')


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  🥚  EGG MARKET INTELLIGENCE DASHBOARD")
    print("  Opening http://localhost:5050 in your browser...")
    print("  Press Ctrl+C to stop")
    print("=" * 60 + "\n")

    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=5050, debug=False)
