# ==================================================
# EGG MARKET DASHBOARD - WORKING VERSION WITH MOCK DATA
# ==================================================
# This version works without API access for testing/demo
# Replace MockDataEngine with real DataEngine when APIs work

import ui
import datetime
from config import THEME, MARGIN
from ui_components import InsightCard, ForecastCard, HeaderLabel

class MockDataEngine:
    """Mock data engine for offline testing"""

    def get_market_snapshot(self):
        """Return realistic mock data"""
        return {
            'corn': {'current': 215.5, 'history': [210, 212, 214, 215, 215.5], 'available': True},
            'soybean': {'current': 456.2, 'history': [445, 448, 452, 454, 456.2], 'available': True},
            'diesel': {'current': 3.89, 'history': [3.75, 3.80, 3.85, 3.87, 3.89], 'available': True},
            'egg_ppi': {'current': 168.5, 'history': [160, 163, 165, 167, 168.5], 'available': True},
            'egg_retail': {'current': 3.28, 'history': [2.95, 3.05, 3.12, 3.20, 3.28], 'available': True},
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'date': datetime.date.today(),
            'fresh_fetch': True
        }

    def calculate_forecast_dates(self):
        """Calculate forecast dates"""
        today = datetime.date.today()
        return {
            'd30': (today + datetime.timedelta(days=30)).strftime("%b %d"),
            'd60': (today + datetime.timedelta(days=60)).strftime("%b %d"),
            'd90': (today + datetime.timedelta(days=90)).strftime("%b %d"),
            'today': today.strftime("%b %d, %Y")
        }

    def clear_cache(self):
        """Mock cache clear"""
        print("🔄 Cache cleared (mock)")


class EggMarketAnalyzer:
    """Egg market analyzer with REAL DATA"""

    def __init__(self, market_data):
        self.market_data = market_data

    def calculate_metrics(self, dates):
        """Calculate comprehensive egg market metrics"""
        print(f"🥚 ANALYZING EGG MARKET: {self.market_data['timestamp']}")

        # Get API data
        corn_price = self.market_data['corn']['current']
        soy_price = self.market_data['soybean']['current']
        diesel_price = self.market_data['diesel']['current']
        egg_ppi = self.market_data['egg_ppi']['current']
        egg_retail = self.market_data['egg_retail']['current']

        # Check availability
        data_available = self.market_data['egg_retail']['available']
        corn_available = self.market_data['corn']['available']
        soy_available = self.market_data['soybean']['available']

        # Static industry data
        total_layers = 320.5
        cage_free_pct = 38.5
        pullet_placements = -3.2
        eggs_per_layer_day = 0.82

        # Prices
        conventional_retail = egg_retail if data_available else 0.0
        cage_free_premium = 0.85
        organic_premium = 2.10
        breaking_stock = 1.30

        # Storage
        shell_storage = 42.5
        frozen_products = 95.2
        dried_products = 22.1

        # HPAI
        hpai_risk_level = "VERY HIGH"
        commercial_outbreaks = 8
        birds_depopulated = 2.1

        # Feed costs from real data
        if corn_available and soy_available:
            layer_feed_cost = (corn_price / 100 * 0.015) + (soy_price / 100 * 0.008)
            annual_feed_cost = layer_feed_cost * 12
            feed_cost_per_dozen = (annual_feed_cost) / (eggs_per_layer_day * 365 / 12)
        else:
            layer_feed_cost = 0.0
            annual_feed_cost = 0.0
            feed_cost_per_dozen = 0.0

        return {
            'meta': {
                'time': self.market_data['timestamp'],
                'dates': dates,
                'data_status': {
                    'egg_retail': data_available,
                    'corn': corn_available,
                    'soybean': soy_available,
                    'fresh_fetch': self.market_data.get('fresh_fetch', False)
                }
            },

            'flock': {
                "TOTAL LAYER INVENTORY": {
                    "val": f"{total_layers}M", "unit": "Birds", "status": "TIGHT",
                    "insight": f"Flock recovering from HPAI. Pullet placements {pullet_placements}% YoY."
                },
                "CAGE-FREE TRANSITION": {
                    "val": f"{cage_free_pct}%", "unit": "of Flock", "status": "ACCELERATING",
                    "insight": "9 states mandate by 2026. Conversion $1,850/bird."
                },
                "FLOCK PRODUCTIVITY": {
                    "val": f"{eggs_per_layer_day:.0%}", "unit": "Rate", "status": "PEAK",
                    "insight": f"{eggs_per_layer_day} eggs/bird/day. Biology maxed."
                }
            },

            'hpai': {
                "BIRD FLU THREAT": {
                    "val": hpai_risk_level, "unit": "Risk", "status": "CRITICAL",
                    "insight": f"{birds_depopulated}M culled YTD. {commercial_outbreaks} active sites."
                },
                "BIOSECURITY PREMIUM": {
                    "val": "+$0.20", "unit": "$/doz", "status": "BAKED IN",
                    "insight": "Enhanced protocols, vaccines, insurance costs."
                },
                "SUPPLY VULNERABILITY": {
                    "val": "EXTREME", "unit": "Fragility", "status": "BLACK SWAN",
                    "insight": "Top 50 farms = 60% supply. One outbreak = crisis."
                }
            },

            'costs': {
                "LAYER FEED COST": {
                    "val": f"${annual_feed_cost:.2f}" if annual_feed_cost > 0 else "N/A",
                    "unit": "/bird/year",
                    "status": "ELEVATED" if annual_feed_cost > 0 else "NO DATA",
                    "insight": f"Corn ${corn_price:.0f}, Soy ${soy_price:.0f}. 18 months feeding." if corn_available else "Feed data unavailable"
                },
                "COST PER DOZEN": {
                    "val": f"${feed_cost_per_dozen:.2f}" if feed_cost_per_dozen > 0 else "N/A",
                    "unit": "Feed Only",
                    "status": "FLOOR" if feed_cost_per_dozen > 0 else "NO DATA",
                    "insight": "Just feed cost. Total floor ~$2.80/doz with all costs."
                },
                "CAGE-FREE DELTA": {
                    "val": "+$0.35", "unit": "$/doz", "status": "STRUCTURAL",
                    "insight": "40% more space = permanently higher prices."
                }
            },

            'market': {
                "CONVENTIONAL RETAIL": {
                    "val": f"${conventional_retail:.2f}" if data_available else "N/A",
                    "unit": "/dozen",
                    "status": "ELEVATED" if data_available and conventional_retail > 3.0 else "NORMAL",
                    "insight": f"LIVE PRICE: ${conventional_retail:.2f}/doz. Caged large eggs." if data_available else "Price unavailable"
                },
                "CAGE-FREE PREMIUM": {
                    "val": f"+${cage_free_premium:.2f}", "unit": "/doz", "status": "WIDENING",
                    "insight": f"Total: ${conventional_retail + cage_free_premium:.2f}/doz. Mandates driving premium." if data_available else "Premium over conventional"
                },
                "ORGANIC PREMIUM": {
                    "val": f"+${organic_premium:.2f}", "unit": "/doz", "status": "LUXURY",
                    "insight": f"Total: ${conventional_retail + organic_premium:.2f}/doz. Whole Foods premium." if data_available else "Premium over conventional"
                },
                "BREAKING STOCK": {
                    "val": f"${breaking_stock:.2f}", "unit": "/doz equiv", "status": "FOOD SERVICE",
                    "insight": "Liquid eggs. Recovering but 15% below 2019."
                }
            },

            'storage': {
                "SHELL EGG INVENTORY": {
                    "val": f"{shell_storage}M", "unit": "dozen", "status": "BELOW NORMAL",
                    "insight": "Normal = 55M. Current = zero buffer."
                },
                "FROZEN EGG PRODUCTS": {
                    "val": f"{frozen_products}M", "unit": "lbs", "status": "ADEQUATE",
                    "insight": "6-8 week cover. Will bid up if fresh spikes."
                },
                "DRIED EGG PRODUCTS": {
                    "val": f"{dried_products}M", "unit": "lbs", "status": "STABLE",
                    "insight": "Price ceiling - competitive when fresh hits $6."
                }
            },

            'forecasts': self._generate_forecasts(conventional_retail, cage_free_premium, organic_premium, breaking_stock, dates, data_available)
        }

    def _generate_forecasts(self, current_retail, cage_free_premium, organic_premium, breaking_stock, dates, data_available):
        """Generate forecasts from current prices"""
        if not data_available or current_retail == 0:
            return {
                "CONVENTIONAL (Large)": {
                    "current": 0, "target": 0, "trend": "NO DATA",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [0]*6, "fut": [0]*3,
                    "logic": "Price data unavailable"
                }
            }

        conv_target = current_retail * 1.12
        cage_target = (current_retail + cage_free_premium) * 1.15
        org_target = (current_retail + organic_premium) * 1.09
        break_target = breaking_stock * 1.12

        hist_base = [
            current_retail * 0.88,
            current_retail * 0.91,
            current_retail * 0.94,
            current_retail * 0.96,
            current_retail * 0.98,
            current_retail
        ]

        return {
            "CONVENTIONAL (Large)": {
                "current": current_retail,
                "target": conv_target,
                "trend": "BULLISH",
                "dates": [dates['d30'], dates['d60'], dates['d90']],
                "hist": hist_base,
                "fut": [current_retail * 1.04, current_retail * 1.08, conv_target],
                "logic": f"Current ${current_retail:.2f}. Tight supply → ${conv_target:.2f} by {dates['d90']}."
            },
            "CAGE-FREE": {
                "current": current_retail + cage_free_premium,
                "target": cage_target,
                "trend": "STRUCTURAL BULL",
                "dates": [dates['d30'], dates['d60'], dates['d90']],
                "hist": [x + cage_free_premium for x in hist_base],
                "fut": [(current_retail + cage_free_premium) * 1.05,
                       (current_retail + cage_free_premium) * 1.10, cage_target],
                "logic": f"${current_retail + cage_free_premium:.2f} now. Shortage → ${cage_target:.2f}."
            },
            "ORGANIC": {
                "current": current_retail + organic_premium,
                "target": org_target,
                "trend": "PREMIUM STABLE",
                "dates": [dates['d30'], dates['d60'], dates['d90']],
                "hist": [x + organic_premium for x in hist_base],
                "fut": [(current_retail + organic_premium) * 1.03,
                       (current_retail + organic_premium) * 1.06, org_target],
                "logic": f"${current_retail + organic_premium:.2f}. Steady premium market."
            },
            "BREAKING STOCK": {
                "current": breaking_stock,
                "target": break_target,
                "trend": "RECOVERY",
                "dates": [dates['d30'], dates['d60'], dates['d90']],
                "hist": [1.05, 1.12, 1.18, 1.22, 1.26, breaking_stock],
                "fut": [breaking_stock * 1.04, breaking_stock * 1.08, break_target],
                "logic": f"Food service recovery. ${break_target:.2f} target."
            }
        }


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
        print("🔄 REFRESH: Fetching data...")
        self.data_engine.clear_cache()

        self.loading.start()
        for sub in self.scroll.subviews:
            sub.remove_from_superview()

        import threading
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        try:
            market_data = self.data_engine.get_market_snapshot()
            dates = self.data_engine.calculate_forecast_dates()
            analyzer = EggMarketAnalyzer(market_data)
            self.data = analyzer.calculate_metrics(dates)
            ui.delay(self.draw_ui, 0)
        except Exception as e:
            print(f"❌ ERROR: {e}")
            ui.delay(lambda: self.show_error(str(e)), 0)

    def show_error(self, error_msg):
        self.loading.stop()
        error_label = ui.Label()
        error_label.text = f"Error:\n{error_msg}\n\nTap refresh to retry"
        error_label.text_color = THEME['bear']
        error_label.alignment = ui.ALIGN_CENTER
        error_label.number_of_lines = 0
        error_label.flex = 'WH'
        self.scroll.add_subview(error_label)

    def draw_ui(self):
        self.loading.stop()
        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        # HEADER
        self._add_label("🥚 EGG MARKET COMMAND", 28, THEME['eggs'], y, cw, bold=True)
        y += 35
        ts = self.data['meta']['time']
        self._add_label(f"LAYER OPS + RETAIL + RISK | {ts}", 12, THEME['sub'], y, cw)
        y += 40

        # STATUS
        status = self.data['meta']['data_status']
        if not status['egg_retail'] or not status['corn'] or not status['soybean']:
            banner = ui.View(frame=(MARGIN, y, cw, 70))
            banner.background_color = '#3d1a00'
            banner.border_color = THEME['warn']
            banner.border_width = 2
            banner.corner_radius = 8

            warn_label = ui.Label(frame=(10, 5, cw-20, 60))
            warn_label.number_of_lines = 0
            warn_label.font = ('<system-bold>', 13)
            warn_label.text_color = THEME['warn']
            missing = []
            if not status['egg_retail']: missing.append('Egg Retail')
            if not status['corn']: missing.append('Corn')
            if not status['soybean']: missing.append('Soybean')
            warn_label.text = f"⚠️ DATA WARNING\nMissing: {', '.join(missing)}\nUsing mock data for demo"
            banner.add_subview(warn_label)
            self.scroll.add_subview(banner)
            y += 85
        else:
            banner = ui.View(frame=(MARGIN, y, cw, 45))
            banner.background_color = '#002200'
            banner.border_color = THEME['bull']
            banner.border_width = 1
            banner.corner_radius = 6

            ok_label = ui.Label(frame=(10, 5, cw-20, 35))
            ok_label.font = ('<system>', 12)
            ok_label.text_color = THEME['bull']
            ok_label.text = f"✓ DATA LOADED | {ts} | Ready"
            banner.add_subview(ok_label)
            self.scroll.add_subview(banner)
            y += 60

        # SECTIONS
        y = HeaderLabel.create(self.scroll, "1. LAYER FLOCK STATUS", THEME['layer'], y, cw)
        for k, v in self.data['flock'].items():
            card, h = InsightCard.create(k, v, THEME['layer'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "2. HPAI & BIOSECURITY RISK", THEME['risk'], y, cw)
        for k, v in self.data['hpai'].items():
            card, h = InsightCard.create(k, v, THEME['risk'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "3. FEED & PRODUCTION COSTS", THEME['logistics'], y, cw)
        for k, v in self.data['costs'].items():
            card, h = InsightCard.create(k, v, THEME['logistics'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "4. MARKET STRUCTURE & PRICING", THEME['eggs'], y, cw)
        for k, v in self.data['market'].items():
            card, h = InsightCard.create(k, v, THEME['eggs'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        y = HeaderLabel.create(self.scroll, "5. COLD STORAGE INVENTORY", THEME['cold'], y, cw)
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
        h = 350
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8

        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 14)
        tv.editable = False

        current_price = self.data['forecasts']['CONVENTIONAL (Large)']['current']
        price_text = f"${current_price:.2f}" if current_price > 0 else "N/A"

        tv.text = (
            "EGG VERDICT: 'STRUCTURALLY TIGHT + TAIL RISK'\n\n"
            f"CURRENT: {price_text}/doz conventional\n\n"
            "1. HPAI RISK: Top 50 farms = 60% supply. One outbreak → $8-10/doz overnight. "
            "2022-23 hit $7.50. One farm away from repeat.\n\n"
            "2. CAGE-FREE TRAP: Mandates forcing conversion. Costs +35¢/doz but consumers resist. "
            "Small farms exit → consolidation → more risk.\n\n"
            "3. FEED FLOOR: Production cost floors rising. Tight flock + high costs = structural support.\n\n"
            "ACTION:\n"
            "• BUY: Conventional targeting +12% (90d)\n"
            "• STRONG BUY: Cage-free (shortage thru 2027)\n"
            "• HEDGE: Breaking stock (recovery play)\n"
            "• RISK: Watch USDA HPAI weekly\n\n"
            "BOTTOM LINE: Underpriced for risk. Next outbreak → $6-8 retail."
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
# RUN THE DASHBOARD
# ==================================================
if __name__ == '__main__':
    # Use MockDataEngine for testing (works offline)
    # Replace with: from data_engine import DataEngine when APIs work
    engine = MockDataEngine()

    dashboard = EggDashboard(engine)
    dashboard.name = "Egg Market Dashboard"

    nav = ui.NavigationView(dashboard)
    nav.present('fullscreen')
