#!/usr/bin/env python3
"""
Professional Protein Market Intelligence Platform
Run: python3 pro_dashboard.py
"""

from flask import Flask, jsonify, render_template_string
import requests
from datetime import datetime, timedelta
import threading
import webbrowser
import time

app = Flask(__name__)

USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

class MarketData:
    cache = {}

    @staticmethod
    def get_usda_data(commodity, stat_cat='INVENTORY'):
        try:
            params = {
                'key': USDA_KEY,
                'commodity_desc': commodity,
                'statisticcat_desc': stat_cat,
                'agg_level_desc': 'NATIONAL',
                'format': 'JSON',
                'year__GE': '2023'
            }
            r = requests.get('https://quickstats.nass.usda.gov/api/api_GET/', params=params, timeout=8)
            if r.status_code == 200 and 'data' in r.json():
                data = r.json()['data']
                if data:
                    # Sort by year, period_desc to get latest
                    sorted_data = sorted(data, key=lambda x: (x.get('year', '0'), x.get('period_desc', '')), reverse=True)
                    return sorted_data
            return []
        except:
            return []

    @staticmethod
    def parse_value(data_list):
        if not data_list:
            return None, None, None

        latest = data_list[0]
        try:
            val_str = latest.get('Value', '').replace(',', '')
            value = float(val_str)
            year = latest.get('year', 'N/A')
            unit = latest.get('unit_desc', '')
            return value, year, unit
        except:
            return None, None, None

@app.route('/api/market_data')
def market_data():
    """Get all market data in one call"""

    # Eggs
    egg_prod = MarketData.get_usda_data('EGGS', 'PRODUCTION')
    egg_val, egg_year, egg_unit = MarketData.parse_value(egg_prod)

    # Cattle
    cattle_inv = MarketData.get_usda_data('CATTLE', 'INVENTORY')
    cattle_val, cattle_year, cattle_unit = MarketData.parse_value(cattle_inv)

    # Hogs
    hog_inv = MarketData.get_usda_data('HOGS', 'INVENTORY')
    hog_val, hog_year, hog_unit = MarketData.parse_value(hog_inv)

    # Milk
    milk_prod = MarketData.get_usda_data('MILK', 'PRODUCTION')
    milk_val, milk_year, milk_unit = MarketData.parse_value(milk_prod)

    # Chickens
    chicken_inv = MarketData.get_usda_data('CHICKENS', 'INVENTORY')
    chicken_val, chicken_year, chicken_unit = MarketData.parse_value(chicken_inv)

    return jsonify({
        'eggs': {
            'production': egg_val or 9245.6,
            'unit': egg_unit or 'MILLION EGGS',
            'year': egg_year,
            'status': 'live' if egg_val else 'fallback'
        },
        'cattle': {
            'inventory': cattle_val or 94800000,
            'unit': cattle_unit or 'HEAD',
            'year': cattle_year,
            'status': 'live' if cattle_val else 'fallback'
        },
        'hogs': {
            'inventory': hog_val or 74500000,
            'unit': hog_unit or 'HEAD',
            'year': hog_year,
            'status': 'live' if hog_val else 'fallback'
        },
        'milk': {
            'production': milk_val or 18800000000,
            'unit': milk_unit or 'LB',
            'year': milk_year,
            'status': 'live' if milk_val else 'fallback'
        },
        'chickens': {
            'inventory': chicken_val or 518000000,
            'unit': chicken_unit or 'HEAD',
            'year': chicken_year,
            'status': 'live' if chicken_val else 'fallback'
        },
        'timestamp': datetime.now().isoformat()
    })

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Protein Market Intelligence</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0a0d14;
    color: #e6e8eb;
    line-height: 1.6;
}
.top-bar {
    background: linear-gradient(135deg, #1a1f2e 0%, #0f1419 100%);
    padding: 32px 48px;
    border-bottom: 3px solid #2196f3;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
}
h1 {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(135deg, #2196f3, #00e676);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -1px;
}
.tagline {
    color: #8b92a3;
    font-size: 15px;
    font-weight: 500;
}
.status-bar {
    margin-top: 16px;
    padding: 12px 20px;
    background: rgba(33, 150, 243, 0.1);
    border-radius: 8px;
    border-left: 4px solid #2196f3;
    display: flex;
    align-items: center;
    gap: 12px;
}
.status-dot {
    width: 8px;
    height: 8px;
    background: #00e676;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.container {
    max-width: 1920px;
    margin: 0 auto;
    padding: 48px;
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
    gap: 32px;
}
.card {
    background: linear-gradient(145deg, #161b26 0%, #1a1f2e 100%);
    border: 1px solid #2a3142;
    border-radius: 20px;
    padding: 36px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #2196f3, #00e676);
    opacity: 0;
    transition: opacity 0.3s;
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 24px 64px rgba(33, 150, 243, 0.2);
    border-color: #2196f3;
}
.card:hover::before {
    opacity: 1;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 28px;
}
.icon {
    font-size: 48px;
    line-height: 1;
}
.card-title {
    flex: 1;
}
.card-name {
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 4px;
}
.card-subtitle {
    font-size: 13px;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-live {
    background: rgba(0, 230, 118, 0.15);
    color: #00e676;
    border: 1px solid rgba(0, 230, 118, 0.3);
}
.badge-fallback {
    background: rgba(255, 152, 0, 0.15);
    color: #ff9800;
    border: 1px solid rgba(255, 152, 0, 0.3);
}
.metric {
    margin-bottom: 24px;
}
.metric-value {
    font-size: 48px;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
    margin-bottom: 8px;
}
.metric-unit {
    font-size: 14px;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
}
.metric-meta {
    display: flex;
    gap: 16px;
    margin-top: 12px;
    padding-top: 16px;
    border-top: 1px solid #2a3142;
}
.meta-item {
    font-size: 12px;
    color: #8b92a3;
}
.meta-label {
    color: #6b7280;
    margin-right: 6px;
}
.loading {
    text-align: center;
    padding: 120px 20px;
    font-size: 18px;
    color: #6b7280;
}
.spinner {
    width: 48px;
    height: 48px;
    border: 4px solid #2a3142;
    border-top-color: #2196f3;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 24px;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
.error {
    background: rgba(244, 67, 54, 0.1);
    border: 1px solid #f44336;
    color: #ff5252;
    padding: 20px 24px;
    border-radius: 12px;
    margin: 40px;
}
</style>
</head>
<body>
<div class="top-bar">
    <h1>🥩 Protein Market Intelligence Platform</h1>
    <div class="tagline">Real-time USDA National Agricultural Statistics Service Data</div>
    <div class="status-bar">
        <div class="status-dot"></div>
        <span style="font-size: 13px; color: #8b92a3;">
            Live Data Feed • Last Update: <span id="updateTime">--</span>
        </span>
    </div>
</div>

<div class="container">
    <div id="content" class="loading">
        <div class="spinner"></div>
        <div>Loading market intelligence...</div>
    </div>
</div>

<script>
function formatNumber(num) {
    if (!num) return 'N/A';
    if (num >= 1e9) return (num/1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num/1e6).toFixed(1) + 'M';
    if (num >= 1e3) return (num/1e3).toFixed(1) + 'K';
    return num.toFixed(1);
}

function createCard(icon, name, subtitle, value, unit, year, status) {
    const badge = status === 'live'
        ? '<span class="badge badge-live">● LIVE USDA</span>'
        : '<span class="badge badge-fallback">○ ESTIMATED</span>';

    return `
        <div class="card">
            <div class="card-header">
                <div class="icon">${icon}</div>
                <div class="card-title">
                    <div class="card-name">${name}</div>
                    <div class="card-subtitle">${subtitle}</div>
                </div>
                ${badge}
            </div>
            <div class="metric">
                <div class="metric-value">${formatNumber(value)}</div>
                <div class="metric-unit">${unit}</div>
                <div class="metric-meta">
                    <div class="meta-item">
                        <span class="meta-label">Year:</span>${year || 'N/A'}
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">Source:</span>USDA NASS
                    </div>
                </div>
            </div>
        </div>
    `;
}

async function loadData() {
    try {
        const res = await fetch('/api/market_data');
        const data = await res.json();

        const html = `
            <div class="grid">
                ${createCard('🥚', 'Egg Production', 'National Layer Output',
                    data.eggs.production, data.eggs.unit, data.eggs.year, data.eggs.status)}
                ${createCard('🐄', 'Cattle Inventory', 'National Beef Herd',
                    data.cattle.inventory, data.cattle.unit, data.cattle.year, data.cattle.status)}
                ${createCard('🐷', 'Hog Inventory', 'National Swine Herd',
                    data.hogs.inventory, data.hogs.unit, data.hogs.year, data.hogs.status)}
                ${createCard('🥛', 'Milk Production', 'National Dairy Output',
                    data.milk.production, data.milk.unit, data.milk.year, data.milk.status)}
                ${createCard('🐔', 'Chicken Inventory', 'National Broiler Stock',
                    data.chickens.inventory, data.chickens.unit, data.chickens.year, data.chickens.status)}
            </div>
        `;

        document.getElementById('content').innerHTML = html;
        document.getElementById('updateTime').textContent = new Date().toLocaleTimeString();
    } catch (error) {
        document.getElementById('content').innerHTML = `
            <div class="error">
                <strong>Error loading data:</strong> ${error.message}
            </div>
        `;
    }
}

loadData();
setInterval(loadData, 300000); // Refresh every 5 min
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:8000')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🥩 PROTEIN MARKET INTELLIGENCE PLATFORM")
    print("="*70)
    print("\n  Server: http://localhost:8000")
    print("  Opening browser...")
    print("\n  Press Ctrl+C to stop\n")
    print("="*70 + "\n")

    threading.Thread(target=open_browser, daemon=True).start()
    app.run(debug=False, port=8000, threaded=True)
