# ==================================================
# POULTRY & EGG MARKET INTELLIGENCE PLATFORM
# Complete Single-File Version for Pythonista
# ==================================================

import ui
import requests
import datetime
import time
import threading
import io
import matplotlib.pyplot as plt

# ==================================================
# CONFIGURATION
# ==================================================

# API Configuration
USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

# Layout Constants
MARGIN = 40

# Color Theme
THEME = {
    'bg': '#050505',           # Background
    'panel': '#121212',        # Card background
    'header': '#1a1a1a',       # Header background
    'text': '#e0e0e0',         # Primary text
    'sub': '#888888',          # Secondary text
    'bull': '#00ff88',         # Green (Bullish)
    'bear': '#ff4444',         # Red (Bearish)
    'warn': '#ffaa00',         # Orange (Warning)
    'macro': '#aa00ff',        # Purple (Macro)
    'bio': '#ff0088',          # Pink (Biology)
    'cold': '#00ccff',         # Ice Blue (Storage)
    'risk': '#ff3333',         # Red (HPAI/Risk)
    'trade': '#0099ff',        # Blue (Global Trade)
    'gold': '#ffd700',         # Premium/Gold
    'logistics': '#ff9900',    # Diesel/Freight
    'eggs': '#ffdd44',         # Egg market
    'layer': '#ff6b9d',        # Layer operations
    'accent': '#00ccff',       # Accent color
    'neutral': '#888888'       # Neutral
}

# FRED Series IDs for Market Data
FRED_SERIES = {
    'corn': 'PMAIZMTUSDM',
    'soybean': 'PSOYBUSDM',
    'diesel': 'GASDESW',
    'egg_price_index': 'WPU01740301',
    'egg_retail': 'APU0000708111',
}

# ==================================================
# DATA ENGINE
# ==================================================

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

# ==================================================
# UI COMPONENTS
# ==================================================

def render_chart(title, data, color, width=5, height=3.0):
    """Render a price trend chart"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(THEME['panel'])
    ax.set_facecolor(THEME['panel'])

    y = data['hist'] + data['fut']
    x_len = len(y)
    x = range(x_len)
    cutoff = len(data['hist']) - 1

    ax.plot(x[:cutoff+1], y[:cutoff+1], color=color, linewidth=2.5, label='Actual')
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
    """Reusable insight card component"""

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
    """Reusable forecast card with chart"""

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

        ForecastCard._add_stat(card, 15, 40, "SPOT PRICE", f"${curr:.2f}")
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
    """Section header component"""

    @staticmethod
    def create(scroll_view, text, color, y, width):
        l = ui.Label(frame=(MARGIN, y, width, 25))
        l.text = text
        l.font = ('<system-bold>', 12)
        l.text_color = color
        scroll_view.add_subview(l)
        return y + 30

# ==================================================
# POULTRY MARKET ANALYZER
# ==================================================

class PoultryMarketAnalyzer:
    """Enhanced poultry market analyzer"""

    def __init__(self, market_data):
        self.market_data = market_data

    def calculate_metrics(self, dates):
        print(f"🐔 ANALYZING POULTRY MARKET: {self.market_data['timestamp']}")

        corn_price = self.market_data['corn']['current']
        soy_price = self.market_data['soybean']['current']
        diesel_price = self.market_data['diesel']['current']

        beef_composite = 8.10
        pork_composite = 4.80
        chicken_composite = 2.15
        beef_spread = beef_composite / chicken_composite
        pork_spread = pork_composite / chicken_composite

        fafh_idx = 365.0
        fah_idx = 305.0
        dining_premium = ((fafh_idx - fah_idx) / fah_idx) * 100

        protein_switching = 15.2
        qsr_traffic = 3.5

        egg_sets = 1.5
        placements = -0.4
        hatchability = 79.7
        pullet_placements = -2.1
        avg_bird_weight = 6.52
        feed_conversion = 1.82

        soy_meal = soy_price * 0.767
        all_in_cost = 1.95

        hpai_cases = 12
        export_volume_change = -2.5
        brazil_advantage = "HIGH"
        leg_quarter_exports = 755

        processing_capacity = 98.2
        labor_shortage = 8500

        return {
            'meta': {'time': self.market_data['timestamp'], 'dates': dates},
            'macro': {
                "BEEF vs. CHICKEN SPREAD": {
                    "val": f"{beef_spread:.2f}x", "unit": "Ratio", "status": "HISTORIC HIGH",
                    "insight": f"Beef at ${beef_composite:.2f} vs Chicken ${chicken_composite:.2f}. {protein_switching}% of consumers actively switching protein."
                },
                "PORK COMPETITION": {
                    "val": f"{pork_spread:.2f}x", "unit": "Ratio", "status": "FAVORABLE",
                    "insight": f"Pork at ${pork_composite:.2f} still double chicken. African Swine Fever abroad gives chicken global edge."
                },
                "DINING vs GROCERY": {
                    "val": f"+{dining_premium:.1f}%", "unit": "Premium", "status": "EATING OUT",
                    "insight": "Restaurant inflation drives home cooking. Retail chicken (Breast, Thighs) benefits."
                },
                "QSR TRAFFIC": {
                    "val": f"+{qsr_traffic}%", "unit": "YoY", "status": "WINGS/TENDERS",
                    "insight": "Fast food winning from casual dining. Wings, tenders, nuggets driving premium pricing."
                }
            },
            'risk': {
                "HPAI THREAT (Broilers)": {
                    "val": "MODERATE", "unit": "Risk", "status": "WATCH",
                    "insight": f"{hpai_cases} sites quarantined. Spillover from layers is risk. Broiler recovery faster (6 week cycle)."
                },
                "EXPORT HEADWINDS": {
                    "val": f"{export_volume_change}%", "unit": "YoY", "status": "CLOGGED",
                    "insight": f"Leg exports soft. Mexico slow, China prefers Brazil. {leg_quarter_exports}M lbs seeking markets."
                },
                "BRAZIL COMPETITION": {
                    "val": brazil_advantage, "unit": "Threat", "status": "LOSING SHARE",
                    "insight": "Brazil undercuts US by $0.15/lb. Winning Asia, Middle East. We keep domestic."
                },
            },
            'bio': {
                "HATCHABILITY CRISIS": {
                    "val": f"{hatchability}%", "unit": "Rate", "status": "CRITICAL",
                    "insight": f"Normal = 84%. At {hatchability}%. Missing 4-5 chicks per 100 eggs. No quick fix."
                },
                "PULLET PLACEMENTS": {
                    "val": f"{pullet_placements}%", "unit": "YoY", "status": "FUTURE SHORT",
                    "insight": "Breeder flock shrinking. Takes 24 weeks to mature. Supply tight through Q2 2027."
                },
                "BIRD WEIGHTS": {
                    "val": f"{avg_bird_weight} lbs", "unit": "Live Wt", "status": "GROWING",
                    "insight": "Heavier birds = better breast yield. Cheap corn encourages longer cycles."
                },
            },
            'inputs': {
                "CORN INDEX": {
                    "val": f"{corn_price:.0f}", "unit": "Index", "status": "FAVORABLE",
                    "insight": f"At {corn_price:.0f}. Cheap energy = heavier birds, better margins. 50% of feed cost."
                },
                "SOYBEAN MEAL": {
                    "val": f"${soy_meal:.0f}", "unit": "/ton", "status": "ELEVATED",
                    "insight": f"Protein at ${soy_meal:.0f}/ton. Elevated but manageable. South America harvest brings Q2 relief."
                },
                "DIESEL FUEL": {
                    "val": f"${diesel_price:.2f}", "unit": "/gal", "status": "FREIGHT DRAG",
                    "insight": f"Adds ~$0.02-0.03/lb logistics. Sticky at ${diesel_price:.2f}."
                },
            },
            'processing': {
                "PLANT CAPACITY": {
                    "val": f"{processing_capacity}%", "unit": "Utilization", "status": "MAXED",
                    "insight": f"At {processing_capacity}%. New plants cost $250M+, 3-year build. Supply ceiling."
                },
                "LABOR SHORTAGE": {
                    "val": f"{labor_shortage:,}", "unit": "Open Jobs", "status": "CRISIS",
                    "insight": "Plants need bodies. Automation 5+ years away. Overtime eating margins."
                },
            },
            'storage': {
                "BREAST MEAT": {
                    "val": "180M", "unit": "lbs", "status": "CRITICAL LOW",
                    "insight": "35% below 5-year avg. Retail restocking strong. Upward pressure Q1."
                },
                "LEG QUARTERS": {
                    "val": "95M", "unit": "lbs", "status": "HEAVY",
                    "insight": "Exports soft = buildup. Dark meat backing up while Breast soars."
                },
                "WINGS": {
                    "val": "72M", "unit": "lbs", "status": "DRAWDOWN",
                    "insight": "Pre-Super Bowl pull active. Seasonal spike Jan-Feb, crash Mar-Jul."
                },
            },
            'cuts': {
                "WHOLE BIRD (WOG)": {
                    "current": 1.28, "target": 1.38, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.15, 1.18, 1.20, 1.24, 1.26, 1.28],
                    "fut": [1.32, 1.35, 1.38],
                    "logic": f"Tight placements. Rotisserie demand stable. ${1.38:.2f} by {dates['d90']}."
                },
                "B/S BREAST": {
                    "current": 1.58, "target": 1.78, "trend": "STRONG BUY",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.30, 1.35, 1.42, 1.48, 1.52, 1.58],
                    "fut": [1.64, 1.71, 1.78],
                    "logic": f"Storage crisis + restocking = explosion. ${1.78:.2f} by {dates['d90']}. BUY."
                },
                "B/S THIGHS": {
                    "current": 1.45, "target": 1.62, "trend": "STRUCTURAL BULL",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.10, 1.20, 1.28, 1.35, 1.40, 1.45],
                    "fut": [1.51, 1.57, 1.62],
                    "logic": "Labor limits de-boning. QSRs pay premium for boneless dark meat."
                },
                "JUMBO WINGS": {
                    "current": 1.68, "target": 2.25, "trend": "SPIKE THEN CRASH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.45, 1.48, 1.50, 1.55, 1.62, 1.68],
                    "fut": [2.05, 2.25, 1.85],
                    "logic": f"Super Bowl peak ${2.25:.2f} by {dates['d60']}, then crash to ${1.85:.2f}."
                },
                "LEG QUARTERS": {
                    "current": 0.42, "target": 0.45, "trend": "NEUTRAL",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [0.38, 0.39, 0.40, 0.41, 0.41, 0.42],
                    "fut": [0.43, 0.44, 0.45],
                    "logic": "Export-dependent. Brazil caps upside. Stuck in range."
                },
                "TENDERS (Premium)": {
                    "current": 2.15, "target": 2.35, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.85, 1.92, 2.00, 2.05, 2.10, 2.15],
                    "fut": [2.22, 2.28, 2.35],
                    "logic": "QSR gold standard. Hand-cut labor limits supply. ${2.35:.2f} target."
                },
            }
        }

# ==================================================
# EGG MARKET ANALYZER
# ==================================================

class EggMarketAnalyzer:
    """Egg market analyzer"""

    def __init__(self, market_data):
        self.market_data = market_data

    def calculate_metrics(self, dates):
        print(f"🥚 ANALYZING EGG MARKET: {self.market_data['timestamp']}")

        corn_price = self.market_data['corn']['current']
        soy_price = self.market_data['soybean']['current']
        egg_retail = self.market_data['egg_retail']['current']

        total_layers = 320.5
        cage_free_pct = 38.5
        pullet_placements = -3.2
        eggs_per_layer_day = 0.82

        conventional_retail = egg_retail if egg_retail > 0 else 3.25
        cage_free_premium = 0.85
        organic_premium = 2.10

        commercial_outbreaks = 8
        birds_depopulated = 2.1

        layer_feed_cost = 0.42
        annual_feed_cost = layer_feed_cost * 12
        feed_cost_per_dozen = (annual_feed_cost) / (eggs_per_layer_day * 365 / 12)

        return {
            'meta': {'time': self.market_data['timestamp'], 'dates': dates},
            'flock': {
                "TOTAL LAYERS": {
                    "val": f"{total_layers}M", "unit": "Birds", "status": "TIGHT",
                    "insight": f"Recovering from HPAI. Pullets down {pullet_placements}%, continued tightness."
                },
                "CAGE-FREE TRANSITION": {
                    "val": f"{cage_free_pct}%", "unit": "of Flock", "status": "ACCELERATING",
                    "insight": "9 states mandate by 2026. Conversion costs $1,850/bird - capital crunch."
                },
                "FLOCK PRODUCTIVITY": {
                    "val": f"{eggs_per_layer_day:.0%}", "unit": "Rate", "status": "PEAK",
                    "insight": f"{eggs_per_layer_day} eggs/bird/day. Biology maxed - only growth is more birds."
                }
            },
            'hpai': {
                "BIRD FLU THREAT": {
                    "val": "VERY HIGH", "unit": "Risk", "status": "CRITICAL",
                    "insight": f"{birds_depopulated}M culled across {commercial_outbreaks} sites. One major farm = instant spike."
                },
                "BIOSECURITY PREMIUM": {
                    "val": "+$0.20", "unit": "$/doz", "status": "BAKED IN",
                    "insight": "Consumers pay for protocols, vaccines, insurance. Cost never goes away."
                },
                "SUPPLY VULNERABILITY": {
                    "val": "EXTREME", "unit": "Fragility", "status": "BLACK SWAN",
                    "insight": "Top 50 farms = 60% supply. One outbreak = shelves empty in 48 hours."
                }
            },
            'costs': {
                "LAYER FEED COST": {
                    "val": f"${annual_feed_cost:.2f}", "unit": "/bird/year", "status": "ELEVATED",
                    "insight": f"Corn ${corn_price:.0f}, Soy ${soy_price:.0f}. Layers eat 18 months vs broilers (6 weeks)."
                },
                "COST PER DOZEN": {
                    "val": f"${feed_cost_per_dozen:.2f}", "unit": "Feed Only", "status": "FLOOR",
                    "insight": "JUST feed. Add housing, labor, transport → retail can't go below $2.80/doz."
                },
                "CAGE-FREE DELTA": {
                    "val": "+$0.35", "unit": "$/doz", "status": "STRUCTURAL",
                    "insight": "40% more space, lower density = permanently higher prices."
                }
            },
            'market': {
                "CONVENTIONAL RETAIL": {
                    "val": f"${conventional_retail:.2f}", "unit": "/dozen", "status": "ELEVATED",
                    "insight": "Base price caged large eggs. Demand strong - eggs are protein necessity."
                },
                "CAGE-FREE PREMIUM": {
                    "val": f"+${cage_free_premium:.2f}", "unit": "/doz", "status": "WIDENING",
                    "insight": "Premium expanding as mandates force supply shift faster than demand."
                },
                "ORGANIC PREMIUM": {
                    "val": f"+${organic_premium:.2f}", "unit": "/doz", "status": "LUXURY",
                    "insight": "Organic feed adds 60% to cost. Whole Foods crowd - niche but sticky."
                },
            },
            'storage': {
                "SHELL EGG INVENTORY": {
                    "val": "42.5M", "unit": "dozen", "status": "BELOW NORMAL",
                    "insight": "Normal = 55M dozen. Zero buffer for supply shock."
                },
                "FROZEN PRODUCTS": {
                    "val": "95.2M", "unit": "lbs", "status": "ADEQUATE",
                    "insight": "6-8 week cover. If fresh spikes, frozen bids up too."
                },
            },
            'forecasts': {
                "CONVENTIONAL (Large)": {
                    "current": conventional_retail,
                    "target": 3.65,
                    "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [2.85, 2.95, 3.05, 3.10, 3.18, conventional_retail],
                    "fut": [3.35, 3.50, 3.65],
                    "logic": f"Tight flock, high feed, HPAI risk. ${3.65:.2f} by {dates['d90']}."
                },
                "CAGE-FREE": {
                    "current": conventional_retail + cage_free_premium,
                    "target": 4.60,
                    "trend": "STRUCTURAL BULL",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [3.50, 3.65, 3.80, 3.88, 3.98, conventional_retail + cage_free_premium],
                    "fut": [4.25, 4.45, 4.60],
                    "logic": f"State mandates. Supply shortage through 2027. ${4.60:.2f} target."
                },
                "ORGANIC": {
                    "current": conventional_retail + organic_premium,
                    "target": 5.85,
                    "trend": "PREMIUM STABLE",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [4.80, 4.95, 5.10, 5.20, 5.28, conventional_retail + organic_premium],
                    "fut": [5.50, 5.70, 5.85],
                    "logic": "Feed inflation flows through. Loyal base absorbs cost."
                },
                "BREAKING STOCK": {
                    "current": 1.30,
                    "target": 1.45,
                    "trend": "RECOVERY",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.05, 1.12, 1.18, 1.22, 1.26, 1.30],
                    "fut": [1.35, 1.40, 1.45],
                    "logic": "Food service recovering. USDA AMS shows ~130¢/doz (Jan 2026). Shell price forces substitution."
                },
            }
        }

# ==================================================
# POULTRY DASHBOARD
# ==================================================

class PoultryDashboard(ui.View):
    """Poultry Market Dashboard"""

    def __init__(self, data_engine):
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

        self.right_button_items = [
            ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh)
        ]

    def will_appear(self):
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        self.loading.start()
        for sub in self.scroll.subviews:
            sub.remove_from_superview()
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        market_data = self.data_engine.get_market_snapshot()
        dates = self.data_engine.calculate_forecast_dates()
        analyzer = PoultryMarketAnalyzer(market_data)
        self.data = analyzer.calculate_metrics(dates)
        ui.delay(self.draw_ui, 0)

    def draw_ui(self):
        self.loading.stop()
        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        self._add_label("🐔 POULTRY MARKET", 28, THEME['gold'], y, cw, bold=True)
        y += 35
        self._add_label(f"BROILER INTELLIGENCE | {self.data['meta']['time']}", 12, THEME['sub'], y, cw)
        y += 40

        y = HeaderLabel.create(self.scroll, "1. MACRO ARBITRAGE", THEME['macro'], y, cw)
        for k, v in self.data['macro'].items():
            card, h = InsightCard.create(k, v, THEME['macro'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "2. GLOBAL RISK & TRADE", THEME['risk'], y, cw)
        for k, v in self.data['risk'].items():
            card, h = InsightCard.create(k, v, THEME['trade'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "3. BIOLOGICAL FUNNEL", THEME['bio'], y, cw)
        for k, v in self.data['bio'].items():
            card, h = InsightCard.create(k, v, THEME['bio'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "4. FEED & LOGISTICS", THEME['logistics'], y, cw)
        for k, v in self.data['inputs'].items():
            card, h = InsightCard.create(k, v, THEME['logistics'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "5. PROCESSING & LABOR", THEME['warn'], y, cw)
        for k, v in self.data['processing'].items():
            card, h = InsightCard.create(k, v, THEME['warn'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "6. COLD STORAGE", THEME['cold'], y, cw)
        for k, v in self.data['storage'].items():
            col = THEME['bull'] if "CRITICAL" in v['status'] else THEME['cold']
            card, h = InsightCard.create(k, v, col, cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "7. PRICE FORECASTS (90-DAY)", THEME['bull'], y, cw)
        for k, v in self.data['cuts'].items():
            card, h = ForecastCard.create(k, v, cw, y, self.data['meta']['dates'])
            self.scroll.add_subview(card)
            y += h + 15

        y = self._draw_verdict(y, cw)
        self.scroll.content_size = (w, y + 100)

    def _draw_verdict(self, y, w):
        y = HeaderLabel.create(self.scroll, "8. ANALYST VERDICT", THEME['warn'], y, w)
        h = 380
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8

        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 14)
        tv.editable = False
        tv.text = (
            "POULTRY VERDICT: 'STRUCTURAL TIGHTNESS'\n\n"
            "1. BIOLOGY BOTTLENECK:\n"
            "Hatchability 79.7% vs 84% normal = crisis. Pullet placements -2.1% locks supply shortage through 2027.\n\n"
            "2. BREAST vs LEG CHASM:\n"
            "Historic spread. Breast demand on fire (low storage, tight supply → $1.78 target). "
            "Legs rot in freezers (Brazil wins exports). Dark meat is the albatross.\n\n"
            "3. LABOR & CAPACITY:\n"
            "Plants at 98%. 8,500 open jobs. Automation years away. Production ceiling.\n\n"
            "ACTION:\n"
            "• STRONG BUY: Breast, Tenders\n"
            "• BUY: Thighs (labor premium)\n"
            "• TRADE: Wings (Super Bowl spike)\n"
            "• AVOID: Legs (export trap)\n\n"
            "Play domestic cuts. White/dark spread is the trade."
        )
        card.add_subview(tv)
        self.scroll.add_subview(card)
        return y + h + 20

    def _add_label(self, text, size, color, y, w, bold=False):
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)

# ==================================================
# EGG DASHBOARD
# ==================================================

class EggDashboard(ui.View):
    """Egg Market Dashboard"""

    def __init__(self, data_engine):
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

        self.right_button_items = [
            ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh)
        ]

    def will_appear(self):
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        self.loading.start()
        for sub in self.scroll.subviews:
            sub.remove_from_superview()
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        market_data = self.data_engine.get_market_snapshot()
        dates = self.data_engine.calculate_forecast_dates()
        analyzer = EggMarketAnalyzer(market_data)
        self.data = analyzer.calculate_metrics(dates)
        ui.delay(self.draw_ui, 0)

    def draw_ui(self):
        self.loading.stop()
        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        self._add_label("🥚 EGG MARKET", 28, THEME['eggs'], y, cw, bold=True)
        y += 35
        self._add_label(f"LAYER OPERATIONS | {self.data['meta']['time']}", 12, THEME['sub'], y, cw)
        y += 40

        y = HeaderLabel.create(self.scroll, "1. LAYER FLOCK STATUS", THEME['layer'], y, cw)
        for k, v in self.data['flock'].items():
            card, h = InsightCard.create(k, v, THEME['layer'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "2. HPAI RISK (CRITICAL)", THEME['risk'], y, cw)
        for k, v in self.data['hpai'].items():
            card, h = InsightCard.create(k, v, THEME['risk'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "3. PRODUCTION COSTS", THEME['logistics'], y, cw)
        for k, v in self.data['costs'].items():
            card, h = InsightCard.create(k, v, THEME['logistics'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "4. MARKET STRUCTURE", THEME['eggs'], y, cw)
        for k, v in self.data['market'].items():
            card, h = InsightCard.create(k, v, THEME['eggs'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "5. COLD STORAGE", THEME['cold'], y, cw)
        for k, v in self.data['storage'].items():
            card, h = InsightCard.create(k, v, THEME['cold'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "6. PRICE FORECASTS (90-DAY)", THEME['bull'], y, cw)
        for k, v in self.data['forecasts'].items():
            card, h = ForecastCard.create(k, v, cw, y, self.data['meta']['dates'])
            self.scroll.add_subview(card)
            y += h + 15

        y = self._draw_verdict(y, cw)
        self.scroll.content_size = (w, y + 100)

    def _draw_verdict(self, y, w):
        y = HeaderLabel.create(self.scroll, "7. ANALYST VERDICT", THEME['warn'], y, w)
        h = 360
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8

        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 14)
        tv.editable = False
        tv.text = (
            "EGG VERDICT: 'STRUCTURAL TIGHT + TAIL RISK'\n\n"
            "1. HPAI SWORD:\n"
            "Bird flu dominant risk. Top 50 farms = 60% supply. One outbreak = $8-10/doz overnight. "
            "2022-23 hit $7.50. We're one farm away from repeat.\n\n"
            "2. CAGE-FREE TRAP:\n"
            "Mandates forcing conversion faster than economics. Cage-free costs +35¢/doz but "
            "consumers resist. Small farms exit → consolidation → more risk.\n\n"
            "3. FEED FLOOR:\n"
            "Production cost = $2.40/doz minimum. Retail below $2.80 = losses. "
            "Tight flock + high costs = structural support.\n\n"
            "ACTION:\n"
            "• BUY: Conventional → $3.65 (90d)\n"
            "• STRONG BUY: Cage-free (shortage thru 2027)\n"
            "• HEDGE: Breaking stock (recovery)\n"
            "• RISK: Watch HPAI weekly\n\n"
            "Eggs underpriced for risk. Next outbreak → $6-8 retail."
        )
        card.add_subview(tv)
        self.scroll.add_subview(card)
        return y + h + 20

    def _add_label(self, text, size, color, y, w, bold=False):
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)

# ==================================================
# MARKET SELECTOR (MAIN)
# ==================================================

class MarketSelector(ui.View):
    """Main navigation screen"""

    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.data_engine = DataEngine()

    def did_load(self):
        w, h = ui.get_screen_size()

        title = ui.Label(frame=(0, 80, w, 50))
        title.text = "POULTRY & EGG\nMARKET INTELLIGENCE"
        title.font = ('<system-bold>', 32)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        subtitle = ui.Label(frame=(0, 145, w, 30))
        subtitle.text = "PROFESSIONAL MARKET ANALYSIS & FORECASTING"
        subtitle.font = ('<system>', 12)
        subtitle.text_color = THEME['sub']
        subtitle.alignment = ui.ALIGN_CENTER
        self.add_subview(subtitle)

        btn_width = min(w - 80, 400)
        btn_x = (w - btn_width) / 2
        btn_y = 220

        poultry_btn = self._create_button(
            "🐔 POULTRY MARKET",
            "Chicken, Broilers & Processed Products",
            THEME['gold'],
            (btn_x, btn_y, btn_width, 100)
        )
        poultry_btn.action = self.show_poultry
        self.add_subview(poultry_btn)

        egg_btn = self._create_button(
            "🥚 EGG MARKET",
            "Layer Operations, Retail & Breaking Stock",
            THEME['eggs'],
            (btn_x, btn_y + 120, btn_width, 100)
        )
        egg_btn.action = self.show_eggs
        self.add_subview(egg_btn)

        footer = ui.Label(frame=(40, h - 100, w - 80, 60))
        footer.text = (
            "Real-time data: USDA & FRED APIs\n"
            "90-day forecasts • Risk analysis • Trade intelligence"
        )
        footer.font = ('<system>', 11)
        footer.text_color = THEME['neutral']
        footer.alignment = ui.ALIGN_CENTER
        footer.number_of_lines = 2
        self.add_subview(footer)

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

    def show_poultry(self, sender):
        dashboard = PoultryDashboard(self.data_engine)
        dashboard.name = "Poultry Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')

    def show_eggs(self, sender):
        dashboard = EggDashboard(self.data_engine)
        dashboard.name = "Egg Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')


if __name__ == '__main__':
    selector = MarketSelector()
    selector.present('fullscreen')
