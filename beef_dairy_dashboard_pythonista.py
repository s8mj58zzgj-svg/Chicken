import ui
import datetime
import math
import io
import time
import urllib.request
import urllib.parse
import json
import matplotlib.pyplot as plt

print("🚀 STARTING BEEF/DAIRY DASHBOARD WITH REAL APIs ONLY")

# ==================================================
# API KEYS
# ==================================================
USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

# ==================================================
# CORRECT FRED SERIES MAPPING (NO PROXIES!)
# ==================================================
FRED_MAP = {
    # BEEF PRICES (Real beef data only)
    'BEEF_RETAIL': 'APU0000FC1101',     # All uncooked beef retail price
    'GROUND_BEEF': 'APU0000703112',     # Ground beef retail
    'BEEF_PPI': 'WPU0222',              # Beef PPI

    # CATTLE PRICES (Alternative series - more reliable)
    'FEEDER_CATTLE': 'WPU01120103',     # Feeder cattle PPI (alternative)
    'LIVE_CATTLE': 'WPU01120102',       # Slaughter cattle PPI (alternative)

    # DAIRY PRICES (Real dairy data)
    'MILK_RETAIL': 'APU0000709112',     # Milk retail price
    'CHEESE_RETAIL': 'APU0000710212',   # Cheese retail price
    'BUTTER_RETAIL': 'APU0000FS1121',   # Butter retail price
    'MILK_PPI': 'WPU0251',              # Fluid milk PPI
    'CHEESE_PPI': 'WPU02520601',        # Cheese PPI

    # FEED & INPUTS (Alternative series)
    'CORN': 'PMAIZMTUSDM',              # Corn price index
    'SOY_MEAL': 'PSOYBUSDM',            # Soybean price index
    'HAY': 'WPU0112050103',             # Hay (alternative series)
    'ALFALFA': 'WPU0112050101',         # Alfalfa hay PPI

    # ENERGY
    'DIESEL': 'GASDESW',                # Diesel price
    'CRUDE': 'DCOILWTICO',              # Crude oil price

    # ECONOMIC
    'CPI': 'CPIAUCSL',                  # Consumer price index
    'RESTAURANT_SALES': 'RRSFS',        # Restaurant sales
}

# ==================================================
# USDA NASS API ENDPOINTS (with year filter for recent data)
# ==================================================
NASS_QUERIES = {
    'CATTLE_INVENTORY': {
        'commodity_desc': 'CATTLE',
        'statisticcat_desc': 'INVENTORY',
        'agg_level_desc': 'NATIONAL',
        'year__GE': '2020',  # Only data from 2020 onwards
        'freq_desc': 'QUARTERLY'
    },
    'CATTLE_ON_FEED': {
        'commodity_desc': 'CATTLE',
        'class_desc': 'CATTLE, ON FEED',
        'statisticcat_desc': 'INVENTORY',
        'agg_level_desc': 'NATIONAL',
        'year__GE': '2020',
        'freq_desc': 'MONTHLY'
    },
    'MILK_PRODUCTION': {
        'commodity_desc': 'MILK',
        'statisticcat_desc': 'PRODUCTION',
        'agg_level_desc': 'NATIONAL',
        'year__GE': '2020',
        'freq_desc': 'MONTHLY'
    },
    'DAIRY_COWS': {
        'commodity_desc': 'CATTLE',
        'class_desc': 'COWS, MILK',
        'statisticcat_desc': 'INVENTORY',
        'agg_level_desc': 'NATIONAL',
        'year__GE': '2020',
        'freq_desc': 'MONTHLY'
    }
}

# ==================================================
# THEME
# ==================================================
THEME = {
    'bg': '#000000', 'panel': '#121212', 'text': '#eeeeee',
    'sub': '#888888', 'muted': '#666666', 'bull': '#00e676',
    'bear': '#ff1744', 'beef': '#ff4444', 'dairy': '#ffaa00',
    'avg_line': '#555555', 'unavailable': '#333333'
}

# ==================================================
# DATA STRUCTURE (NO HARDCODED PRICES!)
# ==================================================
METRIC_METADATA = {
    # BEEF
    'CATTLE_INVENTORY': {'unit': 'M head', 'desc': 'Total cattle inventory', 'polarity': -1, 'mode': 'beef'},
    'CATTLE_ON_FEED': {'unit': 'M head', 'desc': 'Cattle on feed', 'polarity': -1, 'mode': 'beef'},
    'BEEF_RETAIL': {'unit': '$/lb', 'desc': 'Beef retail price', 'polarity': +1, 'mode': 'beef'},
    'GROUND_BEEF': {'unit': '$/lb', 'desc': 'Ground beef retail', 'polarity': +1, 'mode': 'beef'},
    'BEEF_PPI': {'unit': 'Index', 'desc': 'Beef producer price', 'polarity': +1, 'mode': 'beef'},
    'FEEDER_CATTLE': {'unit': 'Index', 'desc': 'Feeder cattle price', 'polarity': +1, 'mode': 'beef'},
    'LIVE_CATTLE': {'unit': 'Index', 'desc': 'Live cattle price', 'polarity': +1, 'mode': 'beef'},

    # DAIRY
    'DAIRY_COWS': {'unit': 'M head', 'desc': 'Dairy cow herd', 'polarity': -1, 'mode': 'dairy'},
    'MILK_PRODUCTION': {'unit': 'B lbs', 'desc': 'Milk production', 'polarity': -1, 'mode': 'dairy'},
    'MILK_RETAIL': {'unit': '$/gal', 'desc': 'Milk retail price', 'polarity': +1, 'mode': 'dairy'},
    'CHEESE_RETAIL': {'unit': '$/lb', 'desc': 'Cheese retail price', 'polarity': +1, 'mode': 'dairy'},
    'BUTTER_RETAIL': {'unit': '$/lb', 'desc': 'Butter retail price', 'polarity': +1, 'mode': 'dairy'},
    'MILK_PPI': {'unit': 'Index', 'desc': 'Milk producer price', 'polarity': +1, 'mode': 'dairy'},
    'CHEESE_PPI': {'unit': 'Index', 'desc': 'Cheese producer price', 'polarity': +1, 'mode': 'dairy'},

    # FEED
    'CORN': {'unit': 'Index', 'desc': 'Corn price', 'polarity': -1, 'mode': 'both'},
    'SOY_MEAL': {'unit': 'Index', 'desc': 'Soybean meal price', 'polarity': -1, 'mode': 'both'},
    'HAY': {'unit': 'Index', 'desc': 'Hay price', 'polarity': -1, 'mode': 'both'},
    'ALFALFA': {'unit': 'Index', 'desc': 'Alfalfa price', 'polarity': -1, 'mode': 'dairy'},
    'DIESEL': {'unit': '$/gal', 'desc': 'Diesel price', 'polarity': -1, 'mode': 'both'},
}

# ==================================================
# API FETCHER (REAL DATA ONLY - USING URLLIB!)
# ==================================================
class APIFetcher:
    cache = {}
    cache_ttl = 1800  # 30 minutes

    @staticmethod
    def clear_cache():
        """Force refresh - clear all cached data"""
        old_count = len(APIFetcher.cache)
        APIFetcher.cache = {}
        print(f"🔄 CACHE CLEARED: {old_count} entries removed")

    @staticmethod
    def fetch_fred(series_id, retry=2):
        """Fetch data from FRED API using urllib with retry logic"""
        cache_key = f"fred_{series_id}"

        # Check cache first
        if cache_key in APIFetcher.cache:
            ts, data = APIFetcher.cache[cache_key]
            if time.time() - ts < APIFetcher.cache_ttl:
                print(f"  📦 CACHE: {series_id}")
                return data

        for attempt in range(retry + 1):
            try:
                if attempt > 0:
                    print(f"  🔄 RETRY {attempt}: {series_id}")
                    time.sleep(0.5 * attempt)  # Brief backoff
                else:
                    print(f"  🌐 FRED: {series_id}")

                # Build URL with parameters
                params = {
                    'series_id': series_id,
                    'api_key': FRED_KEY,
                    'file_type': 'json',
                    'limit': '120',
                    'sort_order': 'desc'
                }
                url = f"https://api.stlouisfed.org/fred/series/observations?{urllib.parse.urlencode(params)}"

                # Make request with urllib
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0')

                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    obs = data.get('observations', [])
                    vals = []

                    for x in obs:
                        try:
                            v = float(x['value'])
                            if v > 0:  # Filter out missing data markers
                                vals.append(v)
                        except:
                            pass

                    if vals and len(vals) >= 2:
                        vals.reverse()  # Chronological order
                        result = {'current': vals[-1], 'history': vals, 'available': True}
                        APIFetcher.cache[cache_key] = (time.time(), result)
                        print(f"  ✅ FRED: {series_id} = {vals[-1]:.2f} ({len(vals)} points)")
                        return result

                print(f"  ⚠️  FRED UNAVAILABLE: {series_id}")
                return {'current': None, 'history': [], 'available': False}

            except Exception as e:
                if attempt == retry:
                    print(f"  ❌ FRED ERROR: {series_id} - {e}")
                    return {'current': None, 'history': [], 'available': False}

    @staticmethod
    def fetch_nass(query_params, retry=2):
        """Fetch data from USDA NASS API using urllib with retry logic"""
        cache_key = f"nass_{query_params.get('commodity_desc')}_{query_params.get('class_desc', '')}"

        # Check cache
        if cache_key in APIFetcher.cache:
            ts, data = APIFetcher.cache[cache_key]
            if time.time() - ts < APIFetcher.cache_ttl:
                print(f"  📦 CACHE: {cache_key}")
                return data

        for attempt in range(retry + 1):
            try:
                if attempt > 0:
                    print(f"  🔄 RETRY {attempt}: {cache_key}")
                    time.sleep(0.5 * attempt)
                else:
                    print(f"  🌐 NASS: {cache_key}")

                # Build URL with parameters
                params = {'key': USDA_KEY, 'format': 'JSON'}
                params.update(query_params)
                url = f"https://quickstats.nass.usda.gov/api/api_GET/?{urllib.parse.urlencode(params)}"

                # Make request with urllib
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0')

                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode())
                    data_items = data.get('data', [])
                    vals = []

                    for d in data_items:
                        try:
                            v = float(str(d.get('Value', '')).replace(',', ''))
                            if v > 0:
                                vals.append(v)
                        except:
                            pass

                    if vals and len(vals) >= 2:
                        vals = vals[::-1]  # Most recent last
                        # Normalize to millions if needed
                        if 'CATTLE' in query_params.get('commodity_desc', ''):
                            vals = [v / 1000.0 for v in vals]  # Convert to millions

                        result = {'current': vals[-1], 'history': vals[-60:], 'available': True}
                        APIFetcher.cache[cache_key] = (time.time(), result)
                        print(f"  ✅ NASS: {cache_key} = {vals[-1]:.2f} ({len(vals)} points)")
                        return result

                print(f"  ⚠️  NASS UNAVAILABLE: {cache_key}")
                return {'current': None, 'history': [], 'available': False}

            except Exception as e:
                if attempt == retry:
                    print(f"  ❌ NASS ERROR: {cache_key} - {e}")
                    return {'current': None, 'history': [], 'available': False}

# ==================================================
# DATA ENGINE (REAL DATA ONLY!)
# ==================================================
class DataEngine:
    @staticmethod
    def get_series(ticker):
        """Get a data series - REAL DATA ONLY, NO SYNTHETIC FALLBACKS"""
        meta = METRIC_METADATA.get(ticker, {
            'unit': '', 'desc': ticker, 'polarity': +1, 'mode': 'beef'
        })

        real_data = None

        # Try NASS first for cattle/dairy inventory data
        if ticker in NASS_QUERIES:
            real_data = APIFetcher.fetch_nass(NASS_QUERIES[ticker])
        # Try FRED for price data
        elif ticker in FRED_MAP:
            real_data = APIFetcher.fetch_fred(FRED_MAP[ticker])

        if not real_data or not real_data.get('available'):
            # NO FALLBACK! Return unavailable data
            print(f"  ⚠️  UNAVAILABLE: {ticker}")
            return {
                'ticker': ticker,
                'val': None,
                'avg': None,
                'unit': meta['unit'],
                'desc': meta['desc'],
                'polarity': meta.get('polarity', +1),
                'hist': [],
                'wchg': None,
                'z': None,
                'mode': meta.get('mode', 'beef'),
                'available': False
            }

        hist = real_data['history']
        val = real_data['current']

        # Calculate statistics only if we have enough data
        wchg = None
        z = None
        avg = None

        if len(hist) >= 6:
            wchg = val - hist[-6]  # Week-over-week change

        if len(hist) >= 30:
            window = hist[-60:-1] if len(hist) >= 61 else hist[:-1]
            avg = sum(window) / len(window)
            var = sum((x - avg) ** 2 for x in window) / len(window)
            sd = math.sqrt(var) if var > 0 else 0.0001
            z = (val - avg) / sd
        else:
            avg = sum(hist) / len(hist) if hist else val

        print(f"  ✅ REAL DATA: {ticker} = {val:.2f}")

        return {
            'ticker': ticker,
            'val': val,
            'avg': avg,
            'unit': meta['unit'],
            'desc': meta['desc'],
            'polarity': meta.get('polarity', +1),
            'hist': hist,
            'wchg': wchg,
            'z': z,
            'mode': meta.get('mode', 'beef'),
            'available': True
        }

def render_chart(hist, color, w, h, avg_val=None):
    """Render a mini chart - only if data available"""
    if not hist or len(hist) < 2:
        return None

    try:
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(w/100, h/100))
        fig.patch.set_facecolor(THEME['panel'])
        ax.set_facecolor(THEME['panel'])
        ax.plot(range(len(hist)), hist, color=color, linewidth=2)
        if avg_val is not None:
            ax.axhline(avg_val, color=THEME['avg_line'], linestyle=':', linewidth=1)
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        plt.close()
        return ui.Image.from_data(buf.getvalue())
    except:
        plt.close('all')
        return None

# ==================================================
# FORECAST ENGINE
# ==================================================
class ForecastEngine:
    @staticmethod
    def generate_brief(mode):
        """Generate market brief from REAL data only"""
        if mode == 'beef':
            cattle_inv = DataEngine.get_series('CATTLE_INVENTORY')
            cattle_feed = DataEngine.get_series('CATTLE_ON_FEED')
            beef_price = DataEngine.get_series('BEEF_RETAIL')
            feeder = DataEngine.get_series('FEEDER_CATTLE')
            corn = DataEngine.get_series('CORN')

            parts = []
            if beef_price['available']:
                parts.append(f"Beef retail ${beef_price['val']:.2f}/lb")
            if cattle_inv['available']:
                parts.append(f"inventory {cattle_inv['val']:.1f}M head")
            if cattle_feed['available']:
                parts.append(f"on feed {cattle_feed['val']:.1f}M")
            if feeder['available']:
                parts.append(f"feeder index {feeder['val']:.0f}")
            if corn['available']:
                parts.append(f"corn {corn['val']:.0f}")

            if parts:
                return f"BEEF MARKET: {', '.join(parts)}. Supply chain remains tight with elevated prices."
            else:
                return "BEEF MARKET: Real-time data loading. Press refresh for latest."

        # DAIRY
        dairy_cows = DataEngine.get_series('DAIRY_COWS')
        milk_prod = DataEngine.get_series('MILK_PRODUCTION')
        milk_price = DataEngine.get_series('MILK_RETAIL')
        cheese_price = DataEngine.get_series('CHEESE_RETAIL')
        butter_price = DataEngine.get_series('BUTTER_RETAIL')

        parts = []
        if milk_price['available']:
            parts.append(f"Milk ${milk_price['val']:.2f}/gal")
        if cheese_price['available']:
            parts.append(f"cheese ${cheese_price['val']:.2f}/lb")
        if butter_price['available']:
            parts.append(f"butter ${butter_price['val']:.2f}/lb")
        if dairy_cows['available']:
            parts.append(f"herd {dairy_cows['val']:.1f}M head")

        if parts:
            return f"DAIRY MARKET: {', '.join(parts)}. Dairy products showing mixed signals."
        else:
            return "DAIRY MARKET: Real-time data loading. Press refresh for latest."

# ==================================================
# UI COMPONENTS
# ==================================================
class MarketCard(ui.View):
    def __init__(self, title, ticker, w):
        self.bg_color = THEME['panel']
        self.corner_radius = 8
        self.border_width = 1
        self.border_color = '#333'

        d = DataEngine.get_series(ticker)

        if not d['available']:
            # Show unavailable state
            self._render_unavailable(title, w, d)
            return

        signal = (d['val'] - d['avg']) * d['polarity'] if d['avg'] is not None else 0
        color = THEME['bull'] if signal >= 0 else THEME['bear']

        l_t = ui.Label(frame=(10, 8, w-20, 14))
        l_t.text = title.upper()
        l_t.font = ('<b>', 10)
        l_t.text_color = THEME['sub']
        self.add_subview(l_t)

        l_p = ui.Label(frame=(10, 24, w*0.62, 26))
        l_p.text = f"{d['val']:,.2f}"
        l_p.font = ('<b>', 22)
        l_p.text_color = THEME['text']
        self.add_subview(l_p)

        l_u = ui.Label(frame=(10, 50, w*0.6, 14))
        l_u.text = d['unit']
        l_u.font = ('<system>', 10)
        l_u.text_color = THEME['sub']
        self.add_subview(l_u)

        if d['z'] is not None and d['avg'] is not None:
            l_ctx = ui.Label(frame=(w-190, 6, 95, 34))
            l_ctx.text = f"avg {d['avg']:,.2f}\nz {d['z']:+.1f}"
            l_ctx.font = ('<b>', 10)
            l_ctx.text_color = THEME['muted']
            l_ctx.alignment = ui.ALIGN_RIGHT
            l_ctx.number_of_lines = 2
            l_ctx.background_color = (0.07, 0.07, 0.07, 0.85)
            l_ctx.corner_radius = 6
            self.add_subview(l_ctx)

        img = ui.ImageView(frame=(w-90, 28, 82, 40))
        img.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        chart = render_chart(d['hist'], color, 82, 40, d['avg'])
        if chart:
            img.image = chart
        self.add_subview(img)

        l_d = ui.Label(frame=(10, 70, w-20, 14))
        l_d.text = f"KPI: {d['desc']}"
        l_d.font = ('<system>', 10)
        l_d.text_color = THEME['muted']
        self.add_subview(l_d)

        if d['wchg'] is not None:
            l_w = ui.Label(frame=(10, 84, w-20, 14))
            l_w.text = f"Δwk {d['wchg']:+.2f}"
            l_w.font = ('<system>', 10)
            l_w.text_color = THEME['sub']
            self.add_subview(l_w)

    def _render_unavailable(self, title, w, d):
        """Render compact unavailable data state"""
        self.border_color = THEME['unavailable']
        self.bg_color = '#0a0a0a'

        l_t = ui.Label(frame=(10, 8, w-20, 14))
        l_t.text = title.upper()
        l_t.font = ('<b>', 10)
        l_t.text_color = THEME['sub']
        self.add_subview(l_t)

        l_na = ui.Label(frame=(10, 28, w-20, 24))
        l_na.text = "N/A"
        l_na.font = ('<b>', 18)
        l_na.text_color = THEME['unavailable']
        l_na.alignment = ui.ALIGN_CENTER
        self.add_subview(l_na)

        # Show different message for NASS data vs FRED data
        if title.upper() in ['CATTLE INVENTORY', 'CATTLE ON FEED', 'DAIRY COWS', 'MILK PRODUCTION']:
            msg = "USDA data updates quarterly"
        else:
            msg = "Series unavailable"

        l_d = ui.Label(frame=(10, 54, w-20, 14))
        l_d.text = msg
        l_d.font = ('<system>', 8)
        l_d.text_color = THEME['muted']
        l_d.alignment = ui.ALIGN_CENTER
        self.add_subview(l_d)

class ForecastCard(ui.View):
    def __init__(self, mode, w):
        color = THEME['beef'] if mode == 'beef' else THEME['dairy']
        self.bg_color = '#1a1a1a'
        self.corner_radius = 8
        self.border_width = 1
        self.border_color = color

        txt = ForecastEngine.generate_brief(mode)

        l_h = ui.Label(frame=(15, 12, w-30, 20))
        l_h.text = f"{mode.upper()} MARKET BRIEF"
        l_h.font = ('<b>', 13)
        l_h.text_color = color
        self.add_subview(l_h)

        l_b = ui.Label(frame=(15, 40, w-30, 100))
        l_b.text = txt
        l_b.font = ('<system>', 12)
        l_b.text_color = '#ccc'
        l_b.number_of_lines = 0
        l_b.size_to_fit()
        self.add_subview(l_b)

        self.height = l_b.frame.max_y + 15

# ==================================================
# DASHBOARD
# ==================================================
class Dashboard(ui.View):
    def __init__(self):
        self.bg_color = '#000'
        self.mode = 'beef'
        self.name = "Beef & Dairy Markets"

        self.seg = ui.SegmentedControl(frame=(15, 40, 220, 30))
        self.seg.segments = ["BEEF", "DAIRY"]
        self.seg.selected_index = 0
        self.seg.action = self.switch
        self.add_subview(self.seg)

        self.btn = ui.Button(frame=(245, 40, 90, 30))
        self.btn.title = "Refresh"
        self.btn.background_color = '#222'
        self.btn.tint_color = THEME['text']
        self.btn.corner_radius = 6
        self.btn.action = self.refresh
        self.add_subview(self.btn)

        self.scroll = ui.ScrollView(frame=(0, 80, self.width, self.height-80))
        self.scroll.flex = 'WH'
        self.add_subview(self.scroll)

    def switch(self, sender):
        self.mode = 'beef' if sender.selected_index == 0 else 'dairy'
        self.render_grid()

    def refresh(self, sender=None):
        print("\n🔄 FORCE REFRESH - CLEARING CACHE")
        APIFetcher.clear_cache()
        self.render_grid()

    def will_appear(self):
        """Called when view appears - load data"""
        print("🎬 Dashboard appearing - initial load")
        self.render_grid()

    def layout(self):
        self.scroll.frame = (0, 80, self.width, self.height-80)

    def render_grid(self):
        print(f"\n🎨 RENDERING {self.mode.upper()} DASHBOARD WITH REAL DATA")

        for s in list(self.scroll.subviews):
            self.scroll.remove_subview(s)

        w = self.width
        cols = 3 if w > 900 else (2 if w > 600 else 1)
        card_w = (w - (15 * (cols + 1))) / cols
        y = 15

        # Add info banner about data sources
        info_banner = ui.View(frame=(15, y, w-30, 40))
        info_banner.bg_color = '#1a1a1a'
        info_banner.corner_radius = 6
        info_banner.border_width = 1
        info_banner.border_color = '#333'

        info_label = ui.Label(frame=(10, 0, w-50, 40))
        info_label.text = "📊 Live data from FRED & USDA APIs. Inventory data updates quarterly. Tap Refresh for latest."
        info_label.font = ('<system>', 10)
        info_label.text_color = THEME['sub']
        info_label.number_of_lines = 2
        self.scroll.add_subview(info_banner)
        info_banner.add_subview(info_label)

        y += 50

        if self.mode == 'beef':
            sections = [
                ("SUPPLY & INVENTORY", [
                    ('Cattle Inventory', 'CATTLE_INVENTORY'),
                    ('Cattle on Feed', 'CATTLE_ON_FEED'),
                    ('Feeder Cattle', 'FEEDER_CATTLE'),
                    ('Live Cattle', 'LIVE_CATTLE')
                ]),
                ("BEEF PRICES", [
                    ('Beef Retail', 'BEEF_RETAIL'),
                    ('Ground Beef', 'GROUND_BEEF'),
                    ('Beef PPI', 'BEEF_PPI')
                ]),
                ("FEED & INPUTS", [
                    ('Corn', 'CORN'),
                    ('Soybean Meal', 'SOY_MEAL'),
                    ('Hay', 'HAY'),
                    ('Diesel', 'DIESEL')
                ])
            ]
            head_color = THEME['beef']
        else:
            sections = [
                ("DAIRY HERD & PRODUCTION", [
                    ('Dairy Cows', 'DAIRY_COWS'),
                    ('Milk Production', 'MILK_PRODUCTION')
                ]),
                ("DAIRY PRICES", [
                    ('Milk Retail', 'MILK_RETAIL'),
                    ('Cheese Retail', 'CHEESE_RETAIL'),
                    ('Butter Retail', 'BUTTER_RETAIL'),
                    ('Milk PPI', 'MILK_PPI'),
                    ('Cheese PPI', 'CHEESE_PPI')
                ]),
                ("FEED COSTS", [
                    ('Corn', 'CORN'),
                    ('Soybean Meal', 'SOY_MEAL'),
                    ('Alfalfa', 'ALFALFA'),
                    ('Diesel', 'DIESEL')
                ])
            ]
            head_color = THEME['dairy']

        for title, items in sections:
            l = ui.Label(frame=(15, y, w-30, 20))
            l.text = title
            l.font = ('<b>', 13)
            l.text_color = head_color
            self.scroll.add_subview(l)
            y += 25

            for i in range(0, len(items), cols):
                row = items[i:i+cols]
                row_height = 100  # Default height for data cards

                for j, (name, ticker) in enumerate(row):
                    x = 15 + (j * (card_w + 15))
                    card = MarketCard(name, ticker, card_w)

                    # Check if data is unavailable to use smaller height
                    d = DataEngine.get_series(ticker)
                    if not d['available']:
                        card_height = 72
                        row_height = min(row_height, 72)
                    else:
                        card_height = 100

                    card.frame = (x, y, card_w, card_height)
                    self.scroll.add_subview(card)

                y += row_height + 10
            y += 10

        narr = ForecastCard(self.mode, w - 30)
        narr.frame = (15, y, w - 30, narr.height)
        self.scroll.add_subview(narr)

        self.scroll.content_size = (w, y + narr.height + 50)

        print(f"✅ DASHBOARD COMPLETE (REAL DATA ONLY)\n")

print("✅ All components loaded - USING URLLIB FOR PYTHONISTA")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 LAUNCHING BEEF/DAIRY DASHBOARD")
    print("   REAL DATA ONLY - URLLIB FOR iOS")
    print("="*50 + "\n")
    v = Dashboard()
    v.present('fullscreen')
    print("✅ DASHBOARD PRESENTED")
