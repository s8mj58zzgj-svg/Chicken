# ==================================================
# BEEF & DAIRY MARKET INTELLIGENCE PLATFORM
# PART 1: Configuration & Data Engine
# ==================================================

import ui
import requests
import datetime
import time
import threading
import io
import matplotlib.pyplot as plt

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
    'beef_retail': 'APU0000FC1101',           # Retail Beef Price
    'ground_beef': 'APU0000703112',           # Ground Beef Retail
    'beef_ppi': 'WPU0222',                    # PPI Beef & Veal

    # Cattle Prices
    'feeder_cattle': 'PCTTLFDGUSDM',          # Feeder Cattle Price Index
    'live_cattle': 'PCATTLEUSDM',             # Live Cattle Price

    # Dairy
    'milk_price': 'APU0000709112',            # Milk Retail Price
    'cheese_price': 'APU0000710212',          # Cheese Price
    'butter_price': 'APU0000FS1121',          # Butter Price

    # Feed & Inputs
    'corn': 'PMAIZMTUSDM',                    # Corn Price Index
    'soybean': 'PSOYBUSDM',                   # Soybean Price
    'wheat': 'PWHEAMTUSDM',                   # Wheat Price
    'hay': 'WPU01120501',                     # Hay Price Index

    # Energy
    'diesel': 'GASDESW',                      # Diesel Fuel
    'crude': 'DCOILWTICO',                    # WTI Crude Oil
    'natgas': 'DHHNGSP',                      # Natural Gas

    # Economic Indicators
    'cpi': 'CPIAUCSL',                        # Consumer Price Index
    'restaurant_sales': 'RRSFS',              # Restaurant Sales
    'grocery_sales': 'RSGASS',                # Grocery Sales
    'drought_index': 'PDSI',                  # Palmer Drought Severity
}

class DataEngine:
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.cache_duration = 300  # 5 minutes

    def fetch_fred(self, series_id, limit=12):
        cache_key = f"fred_{series_id}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                return cached_data
        try:
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
                        return result
            return 0.0, []
        except Exception as e:
            print(f"FRED Error ({series_id}): {e}")
            return 0.0, []

    def get_market_snapshot(self):
        print(f"⚡ FETCHING BEEF/DAIRY DATA: {datetime.datetime.now().strftime('%H:%M:%S')}")

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

        return {
            'beef_retail': {'current': beef_retail_latest if beef_retail_latest > 0 else 8.10, 'history': beef_retail_hist},
            'ground_beef': {'current': ground_beef_latest if ground_beef_latest > 0 else 5.25, 'history': ground_beef_hist},
            'beef_ppi': {'current': beef_ppi_latest if beef_ppi_latest > 0 else 245.0, 'history': beef_ppi_hist},
            'feeder_cattle': {'current': feeder_latest if feeder_latest > 0 else 285.0, 'history': feeder_hist},
            'live_cattle': {'current': live_cattle_latest if live_cattle_latest > 0 else 195.0, 'history': live_cattle_hist},
            'milk': {'current': milk_latest if milk_latest > 0 else 4.15, 'history': milk_hist},
            'cheese': {'current': cheese_latest if cheese_latest > 0 else 5.85, 'history': cheese_hist},
            'butter': {'current': butter_latest if butter_latest > 0 else 4.25, 'history': butter_hist},
            'corn': {'current': corn_latest if corn_latest > 0 else 215.0, 'history': corn_hist},
            'soybean': {'current': soy_latest if soy_latest > 0 else 450.0, 'history': soy_hist},
            'hay': {'current': hay_latest if hay_latest > 0 else 175.0, 'history': hay_hist},
            'diesel': {'current': diesel_latest if diesel_latest > 0 else 3.85, 'history': diesel_hist},
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'date': datetime.date.today()
        }

    def calculate_forecast_dates(self):
        today = datetime.date.today()
        return {
            'd30': (today + datetime.timedelta(days=30)).strftime("%b %d"),
            'd60': (today + datetime.timedelta(days=60)).strftime("%b %d"),
            'd90': (today + datetime.timedelta(days=90)).strftime("%b %d"),
            'd180': (today + datetime.timedelta(days=180)).strftime("%b %d"),
            'today': today.strftime("%b %d, %Y")
        }

def render_chart(title, data, color, width=5, height=3.0):
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
        img.image = render_chart(f"{name} Trend", data, col_c)
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
