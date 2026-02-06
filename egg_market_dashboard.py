"""
EGG MARKET DASHBOARD - Clean Working Version
Pythonista-compatible with mock data support
"""

import ui
import datetime
import threading

# ==================================================
# CONFIGURATION
# ==================================================

MARGIN = 40

THEME = {
    'bg': '#050505',
    'panel': '#121212',
    'text': '#e0e0e0',
    'sub': '#888888',
    'bull': '#00ff88',
    'bear': '#ff4444',
    'warn': '#ffaa00',
    'risk': '#ff3333',
    'cold': '#00ccff',
    'logistics': '#ff9900',
    'eggs': '#ffdd44',
    'layer': '#ff6b9d',
}

# ==================================================
# MOCK DATA ENGINE
# ==================================================

class MockDataEngine:
    """Mock data for offline testing"""

    def get_market_snapshot(self):
        return {
            'corn': {'current': 215.5, 'available': True},
            'soybean': {'current': 456.2, 'available': True},
            'egg_retail': {'current': 3.28, 'available': True},
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
        }

    def calculate_forecast_dates(self):
        today = datetime.date.today()
        return {
            'd30': (today + datetime.timedelta(days=30)).strftime("%b %d"),
            'd60': (today + datetime.timedelta(days=60)).strftime("%b %d"),
            'd90': (today + datetime.timedelta(days=90)).strftime("%b %d"),
        }

    def clear_cache(self):
        print("🔄 Cache cleared")

# ==================================================
# ANALYZER
# ==================================================

class EggAnalyzer:
    """Analyze egg market data"""

    def __init__(self, market_data):
        self.market_data = market_data

    def calculate_metrics(self, dates):
        corn = self.market_data['corn']['current']
        soy = self.market_data['soybean']['current']
        retail = self.market_data['egg_retail']['current']

        return {
            'meta': {'time': self.market_data['timestamp'], 'dates': dates},
            'flock': {
                "LAYER INVENTORY": {
                    "val": "320.5M", "unit": "Birds", "status": "TIGHT",
                    "insight": "Flock recovering from HPAI. Pullet placements down."
                },
                "CAGE-FREE SHIFT": {
                    "val": "38.5%", "unit": "of Flock", "status": "GROWING",
                    "insight": "State mandates driving conversion. Higher costs."
                },
            },
            'hpai': {
                "BIRD FLU RISK": {
                    "val": "VERY HIGH", "unit": "Alert", "status": "CRITICAL",
                    "insight": "2.1M birds culled. Supply vulnerable to outbreaks."
                },
            },
            'costs': {
                "FEED COSTS": {
                    "val": f"${(corn/100*0.015 + soy/100*0.008)*12:.2f}",
                    "unit": "/bird/year", "status": "ELEVATED",
                    "insight": f"Corn ${corn:.0f}, Soy ${soy:.0f}. Major cost driver."
                },
            },
            'market': {
                "RETAIL PRICE": {
                    "val": f"${retail:.2f}", "unit": "/dozen", "status": "ELEVATED",
                    "insight": "Current conventional egg price. HPAI support."
                },
                "CAGE-FREE PREMIUM": {
                    "val": "+$0.85", "unit": "/dozen", "status": "WIDENING",
                    "insight": "Shortage driving premium. Mandates accelerating."
                },
            },
            'forecasts': {
                "CONVENTIONAL": {
                    "current": retail,
                    "target": retail * 1.12,
                    "logic": f"Tight supply. Target ${retail*1.12:.2f} in 90 days."
                },
                "CAGE-FREE": {
                    "current": retail + 0.85,
                    "target": (retail + 0.85) * 1.15,
                    "logic": "Mandate shortage. Strong upside potential."
                },
            }
        }

# ==================================================
# UI COMPONENTS
# ==================================================

class InsightCard:
    @staticmethod
    def create(name, data, color, width, y_pos):
        h = 120
        card = ui.View(frame=(MARGIN, y_pos, width, h))
        card.background_color = THEME['panel']
        card.corner_radius = 8
        card.border_width = 1
        card.border_color = '#222'

        # Title
        t = ui.Label(frame=(15, 10, width-30, 20))
        t.text = name
        t.font = ('<system-bold>', 13)
        t.text_color = color
        card.add_subview(t)

        # Value
        v = ui.Label(frame=(15, 32, 200, 28))
        v.text = f"{data['val']} {data.get('unit', '')}"
        v.font = ('<system-bold>', 22)
        v.text_color = 'white'
        card.add_subview(v)

        # Status badge
        b = ui.Label(frame=(width-110, 10, 95, 20))
        b.text = data['status']
        b.font = ('<system-bold>', 9)
        b.alignment = ui.ALIGN_CENTER
        b.text_color = 'black'
        b.background_color = color
        b.corner_radius = 4
        card.add_subview(b)

        # Insight
        txt = ui.Label(frame=(15, 65, width-30, 45))
        txt.text = data['insight']
        txt.font = ('<system>', 11)
        txt.text_color = '#ccc'
        txt.number_of_lines = 3
        card.add_subview(txt)

        return card, h

class ForecastCard:
    @staticmethod
    def create(name, data, width, y_pos):
        h = 100
        card = ui.View(frame=(MARGIN, y_pos, width, h))
        card.background_color = THEME['panel']
        card.corner_radius = 8

        # Title
        l = ui.Label(frame=(15, 10, width-30, 22))
        l.text = name
        l.font = ('<system-bold>', 15)
        l.text_color = 'white'
        card.add_subview(l)

        # Current
        curr_l = ui.Label(frame=(15, 35, 120, 15))
        curr_l.text = "CURRENT"
        curr_l.font = ('<system>', 10)
        curr_l.text_color = THEME['sub']
        card.add_subview(curr_l)

        curr_v = ui.Label(frame=(15, 48, 120, 22))
        curr_v.text = f"${data['current']:.2f}"
        curr_v.font = ('<system-bold>', 18)
        curr_v.text_color = 'white'
        card.add_subview(curr_v)

        # Target
        targ_l = ui.Label(frame=(140, 35, 120, 15))
        targ_l.text = "90-DAY TARGET"
        targ_l.font = ('<system>', 10)
        targ_l.text_color = THEME['sub']
        card.add_subview(targ_l)

        targ_v = ui.Label(frame=(140, 48, 120, 22))
        targ_v.text = f"${data['target']:.2f}"
        targ_v.font = ('<system-bold>', 18)
        targ_v.text_color = THEME['bull']
        card.add_subview(targ_v)

        # Logic
        logic = ui.Label(frame=(15, 75, width-30, 20))
        logic.text = data['logic']
        logic.font = ('<system>', 10)
        logic.text_color = THEME['sub']
        logic.number_of_lines = 1
        card.add_subview(logic)

        return card, h

# ==================================================
# MAIN DASHBOARD
# ==================================================

class EggDashboard(ui.View):
    """Egg Market Dashboard"""

    def __init__(self, data_engine):
        super().__init__()
        self.data_engine = data_engine
        self.background_color = THEME['bg']
        self.data = None

        # Scroll view
        self.scroll = ui.ScrollView()
        self.scroll.flex = 'WH'
        self.add_subview(self.scroll)

        # Loading indicator
        self.loading = ui.ActivityIndicator()
        self.loading.style = ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE
        self.loading.flex = 'WH'
        self.add_subview(self.loading)

        # Refresh button
        self.right_button_items = [
            ui.ButtonItem(
                image=ui.Image.named('iob:ios7_refresh_empty_32'),
                action=self.refresh
            )
        ]

    def will_appear(self):
        """Called when view appears - load data if needed"""
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        """Refresh data"""
        print("🔄 Refreshing...")
        self.data_engine.clear_cache()
        self.loading.start()

        # Clear existing content
        for sub in self.scroll.subviews:
            sub.remove_from_superview()

        # Load in background
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        """Load data in background thread"""
        try:
            market_data = self.data_engine.get_market_snapshot()
            dates = self.data_engine.calculate_forecast_dates()
            analyzer = EggAnalyzer(market_data)
            self.data = analyzer.calculate_metrics(dates)

            # Update UI on main thread
            ui.delay(self.draw_ui, 0)
        except Exception as e:
            print(f"❌ Error: {e}")
            ui.delay(lambda: self.show_error(str(e)), 0)

    def show_error(self, msg):
        """Show error message"""
        self.loading.stop()
        err = ui.Label()
        err.text = f"Error loading data:\n{msg}\n\nTap refresh to retry"
        err.text_color = THEME['bear']
        err.alignment = ui.ALIGN_CENTER
        err.number_of_lines = 0
        err.flex = 'WH'
        self.scroll.add_subview(err)

    def draw_ui(self):
        """Draw the dashboard UI"""
        self.loading.stop()

        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        # Header
        y = self._add_header("🥚 EGG MARKET DASHBOARD", THEME['eggs'], y, cw, 26)
        y = self._add_label(f"LAYER OPS + RETAIL | {self.data['meta']['time']}",
                           11, THEME['sub'], y, cw)
        y += 30

        # Status banner
        banner = ui.View(frame=(MARGIN, y, cw, 50))
        banner.background_color = '#002200'
        banner.border_color = THEME['bull']
        banner.border_width = 1
        banner.corner_radius = 6

        status_lbl = ui.Label(frame=(10, 5, cw-20, 40))
        status_lbl.font = ('<system>', 12)
        status_lbl.text_color = THEME['bull']
        status_lbl.text = f"✓ DATA LOADED | {self.data['meta']['time']}"
        banner.add_subview(status_lbl)
        self.scroll.add_subview(banner)
        y += 65

        # Section 1: Flock
        y = self._add_section_header("1. LAYER FLOCK STATUS", THEME['layer'], y, cw)
        for name, data in self.data['flock'].items():
            card, h = InsightCard.create(name, data, THEME['layer'], cw, y)
            self.scroll.add_subview(card)
            y += h + 12

        # Section 2: HPAI
        y = self._add_section_header("2. HPAI RISK", THEME['risk'], y, cw)
        for name, data in self.data['hpai'].items():
            card, h = InsightCard.create(name, data, THEME['risk'], cw, y)
            self.scroll.add_subview(card)
            y += h + 12

        # Section 3: Costs
        y = self._add_section_header("3. PRODUCTION COSTS", THEME['logistics'], y, cw)
        for name, data in self.data['costs'].items():
            card, h = InsightCard.create(name, data, THEME['logistics'], cw, y)
            self.scroll.add_subview(card)
            y += h + 12

        # Section 4: Market
        y = self._add_section_header("4. MARKET PRICING", THEME['eggs'], y, cw)
        for name, data in self.data['market'].items():
            card, h = InsightCard.create(name, data, THEME['eggs'], cw, y)
            self.scroll.add_subview(card)
            y += h + 12

        # Section 5: Forecasts
        y = self._add_section_header("5. 90-DAY FORECAST", THEME['bull'], y, cw)
        for name, data in self.data['forecasts'].items():
            card, h = ForecastCard.create(name, data, cw, y)
            self.scroll.add_subview(card)
            y += h + 12

        # Verdict
        y = self._add_verdict(y, cw)

        # Set scroll size
        self.scroll.content_size = (w, y + 80)

    def _add_header(self, text, color, y, w, size):
        """Add header label"""
        l = ui.Label(frame=(MARGIN, y, w, size+8))
        l.text = text
        l.font = ('<system-bold>', size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)
        return y + size + 10

    def _add_label(self, text, size, color, y, w):
        """Add regular label"""
        l = ui.Label(frame=(MARGIN, y, w, size+4))
        l.text = text
        l.font = ('<system>', size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)
        return y + size + 8

    def _add_section_header(self, text, color, y, w):
        """Add section header"""
        l = ui.Label(frame=(MARGIN, y, w, 22))
        l.text = text
        l.font = ('<system-bold>', 12)
        l.text_color = color
        self.scroll.add_subview(l)
        return y + 28

    def _add_verdict(self, y, w):
        """Add analyst verdict"""
        y = self._add_section_header("6. ANALYST VERDICT", THEME['warn'], y, w)

        h = 280
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8

        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 13)
        tv.editable = False
        tv.text = (
            "EGG MARKET: STRUCTURALLY TIGHT + TAIL RISK\n\n"
            "1. HPAI THREAT:\n"
            "Bird flu is the dominant risk. Top 50 farms = 60% of supply. "
            "One major outbreak → $8-10/doz overnight.\n\n"
            "2. CAGE-FREE MANDATE:\n"
            "State laws forcing conversion. Supply shortage through 2027. "
            "Premium widening.\n\n"
            "3. FEED FLOOR:\n"
            "Production costs set price floor. Flock tight, costs elevated.\n\n"
            "RECOMMENDATION:\n"
            "• BUY conventional (+12% 90d)\n"
            "• STRONG BUY cage-free (shortage)\n"
            "• MONITOR HPAI weekly\n\n"
            "Eggs underpriced for risk."
        )
        card.add_subview(tv)
        self.scroll.add_subview(card)

        return y + h + 20

# ==================================================
# RUN
# ==================================================

if __name__ == '__main__':
    engine = MockDataEngine()
    dashboard = EggDashboard(engine)
    dashboard.name = "Egg Market"

    nav = ui.NavigationView(dashboard)
    nav.present('fullscreen')
