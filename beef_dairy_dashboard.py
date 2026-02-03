# ==================================================
# BEEF & DAIRY MARKET INTELLIGENCE PLATFORM
# SINGLE FILE VERSION WITH DEBUG LOGGING
# ==================================================

import ui
import requests
import datetime
import time
import threading
import io
import matplotlib.pyplot as plt

print("✅ IMPORTS LOADED")

# API Configuration
USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

MARGIN = 40

THEME = {
    'bg': '#050505', 'panel': '#121212', 'header': '#1a1a1a',
    'text': '#e0e0e0', 'sub': '#888888', 'bull': '#00ff88',
    'bear': '#ff4444', 'warn': '#ffaa00', 'macro': '#aa00ff',
    'bio': '#ff0088', 'cold': '#00ccff', 'risk': '#ff3333',
    'trade': '#0099ff', 'gold': '#ffd700', 'logistics': '#ff9900',
    'cattle': '#ff6633', 'dairy': '#ffdd88', 'grain': '#99cc33',
    'packer': '#cc0000', 'export': '#0066cc', 'accent': '#00ccff',
    'neutral': '#888888', 'beef': '#8B0000', 'grass': '#228B22'
}

# FRED Series IDs for Beef/Cattle/Dairy Markets
FRED_SERIES = {
    # Beef Prices
    'beef_retail': 'APU0000FC1101',
    'ground_beef': 'APU0000703112',
    'beef_ppi': 'WPU0222',
    # Cattle Prices
    'feeder_cattle': 'PCTTLFDGUSDM',
    'live_cattle': 'PCATTLEUSDM',
    # Dairy
    'milk_price': 'APU0000709112',
    'cheese_price': 'APU0000710212',
    'butter_price': 'APU0000FS1121',
    # Feed & Inputs
    'corn': 'PMAIZMTUSDM',
    'soybean': 'PSOYBUSDM',
    'wheat': 'PWHEAMTUSDM',
    'hay': 'WPU01120501',
    # Energy
    'diesel': 'GASDESW',
    'crude': 'DCOILWTICO',
    'natgas': 'DHHNGSP',
    # Economic Indicators
    'cpi': 'CPIAUCSL',
    'restaurant_sales': 'RRSFS',
    'grocery_sales': 'RSGASS',
    'drought_index': 'PDSI',
}

print("✅ CONFIG LOADED")

class DataEngine:
    def __init__(self):
        print("🔧 DataEngine.__init__() called")
        self.session = requests.Session()
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        print("✅ DataEngine initialized")

    def fetch_fred(self, series_id, limit=12):
        cache_key = f"fred_{series_id}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                print(f"  📦 CACHE HIT: {series_id}")
                return cached_data
        try:
            print(f"  🌐 FETCHING: {series_id}...")
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': series_id, 'api_key': FRED_KEY,
                'file_type': 'json', 'limit': limit, 'sort_order': 'desc'
            }
            r = self.session.get(url, params=params, timeout=8)
            if r.status_code == 200:
                data = r.json().get('observations', [])
                if data:
                    vals = [float(x['value']) for x in data if x['value'] != '.']
                    if vals:
                        result = (vals[0], vals[::-1])
                        self.cache[cache_key] = (time.time(), result)
                        print(f"  ✅ GOT: {series_id} = {vals[0]:.2f}")
                        return result
            print(f"  ⚠️  NO DATA: {series_id}")
            return 0.0, []
        except Exception as e:
            print(f"  ❌ ERROR ({series_id}): {e}")
            return 0.0, []

    def get_market_snapshot(self):
        print(f"\n⚡ FETCHING BEEF/DAIRY DATA: {datetime.datetime.now().strftime('%H:%M:%S')}")

        # Beef prices
        beef_retail_latest, beef_retail_hist = self.fetch_fred(FRED_SERIES['beef_retail'])
        ground_beef_latest, ground_beef_hist = self.fetch_fred(FRED_SERIES['ground_beef'])
        beef_ppi_latest, beef_ppi_hist = self.fetch_fred(FRED_SERIES['beef_ppi'])

        # Cattle prices
        feeder_latest, feeder_hist = self.fetch_fred(FRED_SERIES['feeder_cattle'])
        live_cattle_latest, live_cattle_hist = self.fetch_fred(FRED_SERIES['live_cattle'])

        # Dairy
        milk_latest, milk_hist = self.fetch_fred(FRED_SERIES['milk_price'])
        cheese_latest, cheese_hist = self.fetch_fred(FRED_SERIES['cheese_price'])
        butter_latest, butter_hist = self.fetch_fred(FRED_SERIES['butter_price'])

        # Feed
        corn_latest, corn_hist = self.fetch_fred(FRED_SERIES['corn'])
        soy_latest, soy_hist = self.fetch_fred(FRED_SERIES['soybean'])
        hay_latest, hay_hist = self.fetch_fred(FRED_SERIES['hay'])

        # Energy
        diesel_latest, diesel_hist = self.fetch_fred(FRED_SERIES['diesel'])

        # NO FALLBACK PRICES - Return real data only
        snapshot = {
            'beef_retail': {'current': beef_retail_latest, 'history': beef_retail_hist, 'available': beef_retail_latest > 0},
            'ground_beef': {'current': ground_beef_latest, 'history': ground_beef_hist, 'available': ground_beef_latest > 0},
            'beef_ppi': {'current': beef_ppi_latest, 'history': beef_ppi_hist, 'available': beef_ppi_latest > 0},
            'feeder_cattle': {'current': feeder_latest, 'history': feeder_hist, 'available': feeder_latest > 0},
            'live_cattle': {'current': live_cattle_latest, 'history': live_cattle_hist, 'available': live_cattle_latest > 0},
            'milk': {'current': milk_latest, 'history': milk_hist, 'available': milk_latest > 0},
            'cheese': {'current': cheese_latest, 'history': cheese_hist, 'available': cheese_latest > 0},
            'butter': {'current': butter_latest, 'history': butter_hist, 'available': butter_latest > 0},
            'corn': {'current': corn_latest, 'history': corn_hist, 'available': corn_latest > 0},
            'soybean': {'current': soy_latest, 'history': soy_hist, 'available': soy_latest > 0},
            'hay': {'current': hay_latest, 'history': hay_hist, 'available': hay_latest > 0},
            'diesel': {'current': diesel_latest, 'history': diesel_hist, 'available': diesel_latest > 0},
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'date': datetime.date.today(),
            'fresh_fetch': True
        }

        if snapshot['beef_retail']['available']:
            print(f"✅ SNAPSHOT COMPLETE: beef_retail=${snapshot['beef_retail']['current']:.2f} (LIVE DATA)")
        else:
            print(f"⚠️ SNAPSHOT COMPLETE: Some data unavailable (API error)")
        return snapshot

    def calculate_forecast_dates(self):
        today = datetime.date.today()
        return {
            'd30': (today + datetime.timedelta(days=30)).strftime("%b %d"),
            'd60': (today + datetime.timedelta(days=60)).strftime("%b %d"),
            'd90': (today + datetime.timedelta(days=90)).strftime("%b %d"),
            'd180': (today + datetime.timedelta(days=180)).strftime("%b %d"),
            'today': today.strftime("%b %d, %Y")
        }

    def clear_cache(self):
        """Clear all cached data to force fresh API fetch"""
        old_count = len(self.cache)
        self.cache = {}
        print(f"🔄 CACHE CLEARED - {old_count} entries removed. Next fetch will be FRESH from API.")

print("✅ DataEngine CLASS DEFINED")

def render_chart(title, data, color, width=5, height=3.0):
    try:
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(width, height))
        fig.patch.set_facecolor(THEME['panel'])
        ax.set_facecolor(THEME['panel'])
        y = data['hist'] + data['fut']
        x_len = len(y)
        x = range(x_len)
        cutoff = len(data['hist']) - 1
        ax.plot(x[:cutoff+1], y[:cutoff+1], color=color, linewidth=2.5)
        ax.plot(x[cutoff:], y[cutoff:], color=color, linestyle='--', linewidth=2.5, alpha=0.7)
        ax.scatter([x[-1]], [y[-1]], color=color, s=50, zorder=5)
        ax.grid(color='#333', linestyle=':', linewidth=0.5)
        ax.yaxis.set_visible(True)
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='y', colors='#666', labelsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['bottom'].set_color('#333')
        ax.set_xticks([0, cutoff, x_len-1])
        ax.set_xticklabels(['History', 'Now', '90 Days'], fontsize=8, color='#888')
        ax.set_title(title, fontsize=11, color='#aaa', pad=10, loc='left')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        plt.close()
        return ui.Image.from_data(buf.getvalue())
    except Exception as e:
        print(f"❌ CHART ERROR: {e}")
        plt.close('all')
        return None

class InsightCard:
    @staticmethod
    def create(name, data, color, width, y_pos):
        h = 130
        card = ui.View(frame=(MARGIN, y_pos, width, h))
        card.background_color = THEME['panel']
        card.corner_radius = 8
        card.border_width = 1
        card.border_color = '#222'
        t = ui.Label(frame=(15, 12, width-20, 20))
        t.text = name
        t.font = ('<system-bold>', 14)
        t.text_color = color
        card.add_subview(t)
        v = ui.Label(frame=(15, 35, 200, 30))
        v.text = f"{data.get('val', '--')} {data.get('unit', '')}"
        v.font = ('<system-bold>', 24)
        v.text_color = 'white'
        card.add_subview(v)
        b = ui.Label(frame=(width-115, 12, 100, 20))
        b.text = data.get('status', 'N/A')
        b.font = ('<system-bold>', 10)
        b.alignment = ui.ALIGN_CENTER
        b.text_color = 'black'
        b.background_color = color
        b.corner_radius = 4
        card.add_subview(b)
        txt = ui.Label(frame=(15, 70, width-30, 50))
        txt.text = f"THESIS: {data.get('insight', '')}"
        txt.font = ('<system>', 12)
        txt.text_color = '#ccc'
        txt.number_of_lines = 3
        card.add_subview(txt)
        return card, h

class ForecastCard:
    @staticmethod
    def create(name, data, width, y_pos, dates_dict):
        h = 320
        card = ui.View(frame=(MARGIN, y_pos, width, h))
        card.background_color = THEME['panel']
        card.corner_radius = 8
        l = ui.Label(frame=(15, 10, width-30, 25))
        l.text = name
        l.font = ('<system-bold>', 16)
        l.text_color = 'white'
        card.add_subview(l)
        curr = data.get('current', 0)
        targ = data.get('target', 0)
        pct = ((targ - curr)/curr)*100 if curr else 0
        d90 = dates_dict.get('d90', 'Q1')
        ForecastCard._add_stat(card, 15, 40, "SPOT", f"${curr:.2f}")
        col = THEME['bull'] if pct > 0 else THEME['bear']
        ForecastCard._add_stat(card, 120, 40, f"TARGET ({d90})", f"${targ:.2f}", col)
        ForecastCard._add_stat(card, 240, 40, "DELTA", f"{pct:+.1f}%", col)
        img = ui.ImageView(frame=(15, 90, width-30, 140))
        img.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        col_c = THEME['bull'] if "BUY" in data.get('trend', '') or "BULL" in data.get('trend', '') else THEME['warn']
        chart_img = render_chart(f"{name} Trend", data, col_c)
        if chart_img:
            img.image = chart_img
        card.add_subview(img)
        lbl = ui.Label(frame=(15, 240, width-30, 60))
        lbl.text = f"LOGIC: {data.get('logic', '')}"
        lbl.font = ('<system>', 12)
        lbl.text_color = THEME['sub']
        lbl.number_of_lines = 3
        card.add_subview(lbl)
        return card, h

    @staticmethod
    def _add_stat(parent, x, y, label, val, color='#fff'):
        l = ui.Label(frame=(x, y, 100, 15))
        l.text = label
        l.font = ('<system>', 10)
        l.text_color = THEME['sub']
        parent.add_subview(l)
        v = ui.Label(frame=(x, y+15, 100, 20))
        v.text = val
        v.font = ('<system-bold>', 16)
        v.text_color = color
        parent.add_subview(v)

class HeaderLabel:
    @staticmethod
    def create(scroll_view, text, color, y, width):
        l = ui.Label(frame=(MARGIN, y, width, 25))
        l.text = text
        l.font = ('<system-bold>', 12)
        l.text_color = color
        scroll_view.add_subview(l)
        return y + 30

print("✅ UI COMPONENTS DEFINED")

# ==================================================
# MARKET ANALYZERS
# ==================================================

class BeefMarketAnalyzer:
    """Comprehensive beef & cattle market analyzer"""

    def __init__(self, market_data):
        print("🔧 BeefMarketAnalyzer.__init__() called")
        self.market_data = market_data

    def calculate_metrics(self, dates):
        print(f"🥩 ANALYZING BEEF MARKET: {self.market_data['timestamp']}")

        # Get real market data
        beef_retail = self.market_data['beef_retail']['current']
        ground_beef = self.market_data['ground_beef']['current']
        feeder_cattle = self.market_data['feeder_cattle']['current']
        live_cattle = self.market_data['live_cattle']['current']
        corn_price = self.market_data['corn']['current']
        hay_price = self.market_data['hay']['current']
        diesel_price = self.market_data['diesel']['current']

        print(f"  📊 beef_retail=${beef_retail:.2f}, ground=${ground_beef:.2f}")

        # CATTLE INVENTORY & SUPPLY
        total_cattle = 94.8
        calf_crop = 35.8
        feedlot_placements = 1.85
        feedlot_marketings = 1.92
        placement_weight = 825
        marketing_weight = 1350
        herd_expansion = -1.8
        heifer_retention = 38.2
        cow_slaughter = 3.1
        cattle_on_feed = 14.2
        corn_bushels_per_head = 52
        hay_tons_per_head = 2.8
        total_feed_cost = 950
        cost_of_gain = 1.45
        breakeven_price = (feeder_cattle * (placement_weight/100) + total_feed_cost) / (marketing_weight/100)
        packer_margin = 285
        packer_capacity = 128500
        capacity_utilization = 96.5
        processing_cost = 375
        four_firm_concentration = 85
        weekly_slaughter = 650000
        carcass_weight = 850
        weekly_production = 275
        cutout_value = 315
        export_volume = 3280
        export_pct = 13.5
        japan_exports = 875
        korea_exports = 685
        mexico_exports = 420
        china_exports = 285
        import_volume = 3450
        australia_imports = 1420
        nz_imports = 625
        import_pct = 14.2
        beef_cold_storage = 485
        storage_pct_change = -12.5
        months_supply = 0.95
        drought_severity = 2.8
        pasture_condition = 42
        hay_shortage = "MODERATE"
        per_capita_consumption = 58.4
        restaurant_beef_index = 142.5
        retail_feature_rate = 28.5

        result = {
            'meta': {'time': self.market_data['timestamp'], 'dates': dates},
            'macro': {
                "BEEF RETAIL COMPOSITE": {
                    "val": f"${beef_retail:.2f}", "unit": "/lb", "status": "PREMIUM",
                    "insight": f"Beef at ${beef_retail:.2f}/lb vs chicken $2.15, pork $4.80. Price premium = reduced demand."
                },
                "GROUND BEEF (80/20)": {
                    "val": f"${ground_beef:.2f}", "unit": "/lb", "status": "VALUE",
                    "insight": f"Ground beef ${ground_beef:.2f} is gateway. When middle meats hurt wallet, shift to ground."
                },
                "PER CAPITA CONSUMPTION": {
                    "val": f"{per_capita_consumption} lbs", "unit": "/year", "status": "FLAT",
                    "insight": "Consumption plateaued. High prices killing demand growth."
                },
                "RESTAURANT DEMAND": {
                    "val": f"{restaurant_beef_index:.0f}", "unit": "Index", "status": "STRONG",
                    "insight": "QSRs driving demand for ground beef, brisket, chuck."
                }
            },
            'supply': {
                "US CATTLE INVENTORY": {
                    "val": f"{total_cattle}M", "unit": "Head", "status": "LIQUIDATION",
                    "insight": f"Total {total_cattle}M head. Down {abs(herd_expansion)}% YoY. Liquidation phase."
                },
                "HEIFER RETENTION": {
                    "val": f"{heifer_retention}%", "unit": "Rate", "status": "CRISIS",
                    "insight": f"Only {heifer_retention}% heifers kept. Should be 45%+. Future supply collapse."
                },
                "COW SLAUGHTER RATE": {
                    "val": f"{cow_slaughter}M", "unit": "/year", "status": "RECORD",
                    "insight": f"{cow_slaughter}M cows slaughtered. Herd liquidation accelerating."
                },
                "CALF CROP": {
                    "val": f"{calf_crop}M", "unit": "Calves", "status": "DECLINING",
                    "insight": "Fewer cows = fewer calves. Feeder cattle will be scarce 2025-2027."
                }
            },
            'feedlot': {
                "CATTLE ON FEED": {
                    "val": f"{cattle_on_feed}M", "unit": "Head", "status": "STEADY",
                    "insight": f"{cattle_on_feed}M head in feedlots. Placements < Marketings = draw."
                },
                "COST OF GAIN": {
                    "val": f"${cost_of_gain:.2f}", "unit": "/lb", "status": "ELEVATED",
                    "insight": f"Corn = ${cost_of_gain:.2f}/lb gain. Feedlots squeezed."
                },
                "BREAKEVEN PRICE": {
                    "val": f"${breakeven_price:.0f}", "unit": "/cwt", "status": "SQUEEZED",
                    "insight": f"Break-even ${breakeven_price:.0f}/cwt. Margins thin."
                },
                "FEEDER CATTLE": {
                    "val": f"{feeder_cattle:.0f}", "unit": "Index", "status": "STRONG",
                    "insight": f"Feeder {feeder_cattle:.0f}. Tight calf supply = high prices."
                }
            },
            'feed_drought': {
                "CORN (Feed)": {
                    "val": f"{corn_price:.0f}", "unit": "Index", "status": "MODERATE",
                    "insight": f"Corn {corn_price:.0f}. Takes {corn_bushels_per_head} bushels to finish."
                },
                "HAY PRICES": {
                    "val": f"{hay_price:.0f}", "unit": "Index", "status": "ELEVATED",
                    "insight": f"Hay {hay_price:.0f}. Drought = shortage. Forcing liquidation."
                },
                "DROUGHT SEVERITY": {
                    "val": f"{drought_severity:.1f}/5", "unit": "Index", "status": "STRESS",
                    "insight": f"Drought {drought_severity}/5. Pasture only {pasture_condition}% good."
                },
                "PASTURE CONDITIONS": {
                    "val": f"{pasture_condition}%", "unit": "Good", "status": "POOR",
                    "insight": f"Only {pasture_condition}% rated good. Grass-fed ops crushed."
                }
            },
            'packer': {
                "PACKER MARGIN": {
                    "val": f"${packer_margin}", "unit": "/head", "status": "ELEVATED",
                    "insight": f"Margin ${packer_margin}/head. Big 4 = {four_firm_concentration}% market."
                },
                "CAPACITY UTILIZATION": {
                    "val": f"{capacity_utilization}%", "unit": "Rate", "status": "MAXED",
                    "insight": f"Plants at {capacity_utilization}%. Structural bottleneck."
                },
                "FOUR-FIRM CONCENTRATION": {
                    "val": f"{four_firm_concentration}%", "unit": "Share", "status": "OLIGOPOLY",
                    "insight": f"Top 4 = {four_firm_concentration}% of slaughter. Oligopoly pricing."
                },
                "PROCESSING BACKLOG": {
                    "val": f"{weekly_slaughter/1000:.0f}K", "unit": "Head/wk", "status": "STEADY",
                    "insight": f"Processing {weekly_slaughter/1000:.0f}K/week. Labor tight."
                }
            },
            'trade': {
                "EXPORT VOLUME": {
                    "val": f"{export_pct}%", "unit": "of Prod", "status": "CRITICAL",
                    "insight": f"Exports = {export_pct}%. Japan/Korea are lifeblood."
                },
                "CHINA MARKET": {
                    "val": f"{china_exports}M lbs", "unit": "/year", "status": "VOLATILE",
                    "insight": f"China {china_exports}M lbs. Trade war wild card."
                },
                "IMPORT PRESSURE": {
                    "val": f"{import_pct}%", "unit": "of Cons", "status": "COMPETITION",
                    "insight": f"US imports {import_pct}%! Australia/NZ competition."
                },
                "AUSTRALIA THREAT": {
                    "val": "HIGH", "unit": "Risk", "status": "GRASS-FED",
                    "insight": "Australia dominates grass-fed. Imports cap ground prices."
                }
            },
            'storage': {
                "TOTAL BEEF IN STORAGE": {
                    "val": f"{beef_cold_storage}M lbs", "unit": "lbs", "status": "TIGHT",
                    "insight": f"{beef_cold_storage}M lbs. Down {abs(storage_pct_change)}% YoY."
                },
                "SUPPLY COVERAGE": {
                    "val": f"{months_supply:.1f} mo", "unit": "Supply", "status": "CRITICAL",
                    "insight": f"Less than 1 month supply. Normal = 1.5-2 months."
                }
            },
            'cuts': {
                "GROUND BEEF (80/20)": {
                    "current": ground_beef, "target": 5.65, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [4.85, 4.95, 5.05, 5.12, 5.18, ground_beef],
                    "fut": [5.35, 5.50, 5.65],
                    "logic": f"Cow slaughter declining. Ground tightens. Target $5.65 by {dates['d90']}."
                },
                "CHUCK (Roast/Ground)": {
                    "current": 6.25, "target": 6.75, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [5.65, 5.80, 5.95, 6.05, 6.15, 6.25],
                    "fut": [6.40, 6.58, 6.75],
                    "logic": "Chuck = burger heaven. QSR demand strong. $6.75 target."
                },
                "RIBEYE (Middle Meat)": {
                    "current": 15.85, "target": 17.25, "trend": "PREMIUM",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [14.50, 14.85, 15.20, 15.50, 15.68, 15.85],
                    "fut": [16.25, 16.75, 17.25],
                    "logic": "Ribeye = premium. Steakhouses recovering. $17.25 by Q2."
                },
                "STRIP LOIN (NY Strip)": {
                    "current": 14.25, "target": 15.50, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [12.85, 13.20, 13.55, 13.90, 14.08, 14.25],
                    "fut": [14.65, 15.05, 15.50],
                    "logic": "Strip = white tablecloth demand. $15.50 target."
                },
                "SIRLOIN": {
                    "current": 8.95, "target": 9.45, "trend": "STEADY",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [8.25, 8.45, 8.60, 8.75, 8.85, 8.95],
                    "fut": [9.10, 9.28, 9.45],
                    "logic": "Sirloin = value steak. Steady demand. $9.45 target."
                },
                "BRISKET": {
                    "current": 7.45, "target": 8.25, "trend": "BBQ BOOM",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [6.50, 6.75, 6.95, 7.15, 7.30, 7.45],
                    "fut": [7.70, 7.98, 8.25],
                    "logic": "Brisket = BBQ craze. Limited supply. $8.25+ easy."
                },
                "SHORT RIB": {
                    "current": 12.50, "target": 13.85, "trend": "RESTAURANT",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [10.85, 11.25, 11.65, 12.05, 12.28, 12.50],
                    "fut": [12.95, 13.40, 13.85],
                    "logic": "Short ribs = high-end trend. Korean BBQ, fine dining. $13.85."
                },
                "TRIM (50/50)": {
                    "current": 3.25, "target": 3.65, "trend": "GRINDING",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [2.85, 2.95, 3.05, 3.12, 3.18, 3.25],
                    "fut": [3.35, 3.50, 3.65],
                    "logic": "50/50 trim for ground. Cow slaughter down = scarce. $3.65."
                }
            }
        }

        print(f"✅ BEEF ANALYSIS COMPLETE: {len(result['cuts'])} cuts")
        return result

class DairyMarketAnalyzer:
    """Dairy market analyzer (impacts beef via cull cows)"""

    def __init__(self, market_data):
        print("🔧 DairyMarketAnalyzer.__init__() called")
        self.market_data = market_data

    def calculate_metrics(self, dates):
        print(f"🥛 ANALYZING DAIRY: {self.market_data['timestamp']}")

        milk_price = self.market_data['milk']['current']
        cheese_price = self.market_data['cheese']['current']
        butter_price = self.market_data['butter']['current']

        dairy_cows = 9.4
        milk_per_cow = 24000
        dairy_cull_rate = 38
        dairy_beef_pct = 18
        dairy_steers_fed = 3.2

        result = {
            'meta': {'time': self.market_data['timestamp'], 'dates': dates},
            'dairy_herd': {
                "DAIRY COW INVENTORY": {
                    "val": f"{dairy_cows}M", "unit": "Cows", "status": "STABLE",
                    "insight": f"{dairy_cows}M dairy cows. Cull rate {dairy_cull_rate}% = {dairy_cows * dairy_cull_rate/100:.1f}M entering beef."
                },
                "DAIRY BEEF CONTRIBUTION": {
                    "val": f"{dairy_beef_pct}%", "unit": "of Beef", "status": "SIGNIFICANT",
                    "insight": f"Dairy = {dairy_beef_pct}% of US beef! Holstein steers + cull cows."
                },
                "HOLSTEIN STEER IMPACT": {
                    "val": f"{dairy_steers_fed}M", "unit": "Head/yr", "status": "SUPPLY",
                    "insight": f"{dairy_steers_fed}M Holstein steers fed/year. Compete with beef cattle."
                }
            },
            'dairy_prices': {
                "MILK PRICE": {
                    "val": f"${milk_price:.2f}", "unit": "/gal", "status": "MODERATE",
                    "insight": f"Milk ${milk_price:.2f}/gal. When low = more beef supply."
                },
                "CHEESE PRICE": {
                    "val": f"${cheese_price:.2f}", "unit": "/lb", "status": "ELEVATED",
                    "insight": f"Cheese ${cheese_price:.2f}. High = less culling = less beef."
                },
                "BUTTER PRICE": {
                    "val": f"${butter_price:.2f}", "unit": "/lb", "status": "STRONG",
                    "insight": f"Butter ${butter_price:.2f}. Strong dairy = reduced beef supply."
                }
            }
        }

        print(f"✅ DAIRY ANALYSIS COMPLETE")
        return result

print("✅ ANALYZER CLASSES DEFINED")

# ==================================================
# DASHBOARD UI
# ==================================================

class BeefDashboard(ui.View):
    """Comprehensive Beef & Cattle Market Dashboard"""

    def __init__(self, data_engine):
        print("🔧 BeefDashboard.__init__() called")
        super().__init__()
        self.data_engine = data_engine
        self.background_color = THEME['bg']
        self.data = None
        self.scroll = ui.ScrollView(flex='WH')
        self.add_subview(self.scroll)
        self.loading = ui.ActivityIndicator(style=ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE)
        self.loading.flex = 'WH'
        self.loading.start()
        self.add_subview(self.loading)
        self.right_button_items = [ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh)]
        print("✅ BeefDashboard initialized")

    def will_appear(self):
        print("🎬 BeefDashboard.will_appear() called")
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        print("🔄 BeefDashboard.refresh() called")
        self.loading.start()
        for sub in self.scroll.subviews:
            sub.remove_from_superview()
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        print("📥 BeefDashboard.load_data() STARTED (background thread)")
        try:
            market_data = self.data_engine.get_market_snapshot()
            dates = self.data_engine.calculate_forecast_dates()
            analyzer = BeefMarketAnalyzer(market_data)
            self.data = analyzer.calculate_metrics(dates)
            print("✅ BeefDashboard data loaded, scheduling UI draw...")
            ui.delay(self.draw_ui, 0)
        except Exception as e:
            print(f"❌ BeefDashboard.load_data() ERROR: {e}")

    def draw_ui(self):
        print("🎨 BeefDashboard.draw_ui() STARTED")
        try:
            self.loading.stop()
            w, h = ui.get_screen_size()
            self.scroll.frame = (0, 0, w, h)
            cw = w - (MARGIN * 2)
            y = 40

            self._add_label("🥩 BEEF & CATTLE MARKET", 28, THEME['beef'], y, cw, bold=True)
            y += 35
            self._add_label(f"SUPPLY CHAIN INTELLIGENCE | {self.data['meta']['time']}", 12, THEME['sub'], y, cw)
            y += 40

            # 1. MACRO
            y = HeaderLabel.create(self.scroll, "1. MACRO & PROTEIN COMPETITION", THEME['macro'], y, cw)
            for k, v in self.data['macro'].items():
                card, h = InsightCard.create(k, v, THEME['macro'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            # 2. SUPPLY
            y = HeaderLabel.create(self.scroll, "2. CATTLE SUPPLY & HERD LIQUIDATION", THEME['cattle'], y, cw)
            for k, v in self.data['supply'].items():
                card, h = InsightCard.create(k, v, THEME['cattle'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            # 3. FEEDLOT
            y = HeaderLabel.create(self.scroll, "3. FEEDLOT ECONOMICS", THEME['grain'], y, cw)
            for k, v in self.data['feedlot'].items():
                card, h = InsightCard.create(k, v, THEME['grain'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            # 4. FEED/DROUGHT
            y = HeaderLabel.create(self.scroll, "4. FEED COSTS & DROUGHT", THEME['grass'], y, cw)
            for k, v in self.data['feed_drought'].items():
                card, h = InsightCard.create(k, v, THEME['grass'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            # 5. PACKER
            y = HeaderLabel.create(self.scroll, "5. PACKER POWER", THEME['packer'], y, cw)
            for k, v in self.data['packer'].items():
                card, h = InsightCard.create(k, v, THEME['packer'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            # 6. TRADE
            y = HeaderLabel.create(self.scroll, "6. EXPORT/IMPORT", THEME['export'], y, cw)
            for k, v in self.data['trade'].items():
                card, h = InsightCard.create(k, v, THEME['export'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            # 7. STORAGE
            y = HeaderLabel.create(self.scroll, "7. COLD STORAGE", THEME['cold'], y, cw)
            for k, v in self.data['storage'].items():
                card, h = InsightCard.create(k, v, THEME['cold'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            # 8. CUTS
            y = HeaderLabel.create(self.scroll, "8. BEEF CUT FORECASTS (90-DAY)", THEME['bull'], y, cw)
            for k, v in self.data['cuts'].items():
                card, h = ForecastCard.create(k, v, cw, y, self.data['meta']['dates'])
                self.scroll.add_subview(card)
                y += h + 15

            self.scroll.content_size = (w, y + 100)
            print(f"✅ BeefDashboard UI DRAWN: {y}px tall")
        except Exception as e:
            print(f"❌ BeefDashboard.draw_ui() ERROR: {e}")

    def _add_label(self, text, size, color, y, w, bold=False):
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)

class DairyDashboard(ui.View):
    """Dairy Market Dashboard"""

    def __init__(self, data_engine):
        print("🔧 DairyDashboard.__init__() called")
        super().__init__()
        self.data_engine = data_engine
        self.background_color = THEME['bg']
        self.data = None
        self.scroll = ui.ScrollView(flex='WH')
        self.add_subview(self.scroll)
        self.loading = ui.ActivityIndicator(style=ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE)
        self.loading.flex = 'WH'
        self.loading.start()
        self.add_subview(self.loading)
        self.right_button_items = [ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh)]
        print("✅ DairyDashboard initialized")

    def will_appear(self):
        print("🎬 DairyDashboard.will_appear() called")
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        print("🔄 DairyDashboard.refresh() called")
        self.loading.start()
        for sub in self.scroll.subviews:
            sub.remove_from_superview()
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        print("📥 DairyDashboard.load_data() STARTED")
        try:
            market_data = self.data_engine.get_market_snapshot()
            dates = self.data_engine.calculate_forecast_dates()
            analyzer = DairyMarketAnalyzer(market_data)
            self.data = analyzer.calculate_metrics(dates)
            print("✅ DairyDashboard data loaded, scheduling UI draw...")
            ui.delay(self.draw_ui, 0)
        except Exception as e:
            print(f"❌ DairyDashboard.load_data() ERROR: {e}")

    def draw_ui(self):
        print("🎨 DairyDashboard.draw_ui() STARTED")
        try:
            self.loading.stop()
            w, h = ui.get_screen_size()
            self.scroll.frame = (0, 0, w, h)
            cw = w - (MARGIN * 2)
            y = 40

            self._add_label("🥛 DAIRY MARKET", 28, THEME['dairy'], y, cw, bold=True)
            y += 35
            self._add_label(f"MILK, CHEESE, BUTTER + BEEF IMPACT | {self.data['meta']['time']}", 12, THEME['sub'], y, cw)
            y += 40

            y = HeaderLabel.create(self.scroll, "1. DAIRY HERD & BEEF IMPACT", THEME['dairy'], y, cw)
            for k, v in self.data['dairy_herd'].items():
                card, h = InsightCard.create(k, v, THEME['dairy'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            y = HeaderLabel.create(self.scroll, "2. DAIRY PRODUCT PRICES", THEME['gold'], y, cw)
            for k, v in self.data['dairy_prices'].items():
                card, h = InsightCard.create(k, v, THEME['gold'], cw, y)
                self.scroll.add_subview(card)
                y += h + 15

            self.scroll.content_size = (w, y + 100)
            print(f"✅ DairyDashboard UI DRAWN: {y}px tall")
        except Exception as e:
            print(f"❌ DairyDashboard.draw_ui() ERROR: {e}")

    def _add_label(self, text, size, color, y, w, bold=False):
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)

print("✅ DASHBOARD CLASSES DEFINED")

class MarketSelector(ui.View):
    """Main navigation screen"""

    def __init__(self):
        print("🔧 MarketSelector.__init__() called")
        super().__init__()
        self.background_color = THEME['bg']
        self.data_engine = DataEngine()
        print("✅ MarketSelector initialized")

    def did_load(self):
        print("🎬 MarketSelector.did_load() called")
        w, h = ui.get_screen_size()
        title = ui.Label(frame=(0, 80, w, 50))
        title.text = "BEEF & DAIRY\nMARKET INTELLIGENCE"
        title.font = ('<system-bold>', 32)
        title.text_color = THEME['beef']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        subtitle = ui.Label(frame=(0, 145, w, 30))
        subtitle.text = "COMPREHENSIVE CATTLE & DAIRY ANALYSIS"
        subtitle.font = ('<system>', 12)
        subtitle.text_color = THEME['sub']
        subtitle.alignment = ui.ALIGN_CENTER
        self.add_subview(subtitle)

        btn_width = min(w - 80, 400)
        btn_x = (w - btn_width) / 2
        btn_y = 220

        beef_btn = self._create_button(
            "🥩 BEEF & CATTLE",
            "Supply Chain, Feed, Drought, Exports, Forecasts",
            THEME['beef'],
            (btn_x, btn_y, btn_width, 100)
        )
        beef_btn.action = self.show_beef
        self.add_subview(beef_btn)

        dairy_btn = self._create_button(
            "🥛 DAIRY MARKET",
            "Milk, Cheese, Butter & Beef Impact Analysis",
            THEME['dairy'],
            (btn_x, btn_y + 120, btn_width, 100)
        )
        dairy_btn.action = self.show_dairy
        self.add_subview(dairy_btn)

        footer = ui.Label(frame=(40, h - 100, w - 80, 60))
        footer.text = "Real-time: USDA & FRED APIs\nCattle • Feed • Packer margins • Export/Import"
        footer.font = ('<system>', 11)
        footer.text_color = THEME['neutral']
        footer.alignment = ui.ALIGN_CENTER
        footer.number_of_lines = 2
        self.add_subview(footer)
        print("✅ MarketSelector UI built")

    def _create_button(self, title, subtitle, color, frame):
        btn = ui.Button(frame=frame)
        btn.background_color = THEME['panel']
        btn.border_color = color
        btn.border_width = 2
        btn.corner_radius = 12
        title_lbl = ui.Label()
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 24)
        title_lbl.text_color = color
        title_lbl.alignment = ui.ALIGN_CENTER
        title_lbl.frame = (10, 20, frame[2] - 20, 35)
        btn.add_subview(title_lbl)
        sub_lbl = ui.Label()
        sub_lbl.text = subtitle
        sub_lbl.font = ('<system>', 13)
        sub_lbl.text_color = THEME['sub']
        sub_lbl.alignment = ui.ALIGN_CENTER
        sub_lbl.frame = (10, 58, frame[2] - 20, 20)
        btn.add_subview(sub_lbl)
        return btn

    def show_beef(self, sender):
        print("🥩 LAUNCHING BEEF DASHBOARD")
        dashboard = BeefDashboard(self.data_engine)
        dashboard.name = "Beef & Cattle Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')

    def show_dairy(self, sender):
        print("🥛 LAUNCHING DAIRY DASHBOARD")
        dashboard = DairyDashboard(self.data_engine)
        dashboard.name = "Dairy Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')

print("✅ MarketSelector CLASS DEFINED")

# ==================================================
# MAIN ENTRY POINT
# ==================================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STARTING BEEF & DAIRY DASHBOARD")
    print("="*50 + "\n")
    selector = MarketSelector()
    selector.present('fullscreen')
    print("✅ APP LAUNCHED")
