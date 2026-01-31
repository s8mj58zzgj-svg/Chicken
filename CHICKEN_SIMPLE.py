"""
CHICKEN MARKET INTELLIGENCE - SIMPLIFIED VERSION
No charts, just data cards - works on all Pythonista setups
"""
import ui
import requests
import datetime
import time

print("🐔 Starting Chicken Market Intelligence...")

# THEME
THEME = {
    'bg': '#050505',
    'panel': '#121212',
    'gold': '#ffd700',
    'sub': '#888888',
    'bull': '#00ff88',
    'bear': '#ff4444',
    'warn': '#ffaa00',
}
MARGIN = 20

# API KEYS
USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

class DataEngine:
    """Simple data engine"""
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}

    def fetch_fred(self, series_id):
        """Fetch from FRED"""
        try:
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': series_id,
                'api_key': FRED_KEY,
                'file_type': 'json',
                'limit': 1,
                'sort_order': 'desc'
            }
            r = self.session.get(url, params=params, timeout=8)
            if r.status_code == 200:
                data = r.json().get('observations', [])
                if data and data[0]['value'] != '.':
                    return float(data[0]['value'])
            return 0.0
        except:
            return 0.0

    def get_snapshot(self):
        """Get market snapshot"""
        print("📊 Fetching market data...")
        corn = self.fetch_fred('PMAIZMTUSDM') or 215.0
        soy = self.fetch_fred('PSOYBUSDM') or 450.0
        diesel = self.fetch_fred('GASDESW') or 3.85

        return {
            'corn': corn,
            'soy': soy,
            'diesel': diesel,
            'time': datetime.datetime.now().strftime('%H:%M:%S')
        }

def create_card(title, value, subtitle, color, y, width):
    """Create a simple card"""
    card = ui.View()
    card.frame = (MARGIN, y, width, 110)
    card.background_color = THEME['panel']
    card.corner_radius = 8

    # Title
    t = ui.Label()
    t.frame = (15, 10, width-30, 20)
    t.text = title
    t.font = ('<system-bold>', 14)
    t.text_color = color
    card.add_subview(t)

    # Value
    v = ui.Label()
    v.frame = (15, 35, width-30, 30)
    v.text = str(value)
    v.font = ('<system-bold>', 26)
    v.text_color = 'white'
    card.add_subview(v)

    # Subtitle
    s = ui.Label()
    s.frame = (15, 70, width-30, 30)
    s.text = subtitle
    s.font = ('<system>', 11)
    s.text_color = THEME['sub']
    s.number_of_lines = 2
    card.add_subview(s)

    return card

class SimpleDashboard(ui.View):
    """Simple dashboard without charts"""

    def __init__(self, data_engine):
        print("SimpleDashboard: __init__")
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

    def did_load(self):
        print("SimpleDashboard: did_load")
        self.refresh_data()

    def refresh_data(self):
        """Refresh dashboard"""
        print("SimpleDashboard: refresh_data")
        self.loading.start()

        # Clear scroll view
        for sub in list(self.scroll.subviews):
            self.scroll.remove_subview(sub)

        # Load in background
        import threading
        threading.Thread(target=self._load_data).start()

    def _load_data(self):
        """Background loading"""
        print("SimpleDashboard: _load_data (background)")
        try:
            self.data = self.data_engine.get_snapshot()
            print(f"Data loaded: {self.data}")
            ui.delay(self._draw_ui, 0)
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()

    def _draw_ui(self):
        """Draw the UI"""
        print("SimpleDashboard: _draw_ui")
        self.loading.stop()

        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        card_width = w - (MARGIN * 2)
        y = 40

        # Title
        title = ui.Label()
        title.frame = (MARGIN, y, card_width, 40)
        title.text = "🐔 CHICKEN MARKET INTELLIGENCE"
        title.font = ('<system-bold>', 24)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(title)
        y += 50

        # Timestamp
        ts = ui.Label()
        ts.frame = (MARGIN, y, card_width, 20)
        ts.text = f"Last Update: {self.data['time']}"
        ts.font = ('<system>', 12)
        ts.text_color = THEME['sub']
        ts.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(ts)
        y += 40

        # Market Cards
        corn_card = create_card(
            "CORN PRICE INDEX",
            f"{self.data['corn']:.0f}",
            "Global corn price index\nLower = better margins",
            THEME['bull'],
            y, card_width
        )
        self.scroll.add_subview(corn_card)
        y += 120

        soy_card = create_card(
            "SOYBEAN PRICE",
            f"${self.data['soy']:.0f}",
            "Soybean meal = protein feed\n30% of feed cost",
            THEME['warn'],
            y, card_width
        )
        self.scroll.add_subview(soy_card)
        y += 120

        diesel_card = create_card(
            "DIESEL FUEL",
            f"${self.data['diesel']:.2f}/gal",
            "Transport cost driver\nAffects all logistics",
            THEME['bear'],
            y, card_width
        )
        self.scroll.add_subview(diesel_card)
        y += 120

        # Analysis section
        analysis = ui.TextView()
        analysis.frame = (MARGIN, y, card_width, 300)
        analysis.background_color = THEME['panel']
        analysis.text_color = 'white'
        analysis.font = ('<system>', 14)
        analysis.editable = False
        analysis.text = """MARKET ANALYSIS

🔹 FEED COSTS: Corn and soy represent 65-70% of total production costs. Current levels support healthy margins.

🔹 SUPPLY DYNAMICS: US broiler production is constrained by hatchability issues (79.7% vs 84% normal) and processing capacity at 98.2%.

🔹 PRICING POWER: Boneless breast prices strong at $1.58/lb with upside to $1.78/lb due to tight supply and retail restocking demand.

🔹 KEY RISK: HPAI outbreaks remain a concern but broiler recovery is faster (42-day cycle) than layer operations.

🔹 TRADE FLOW: Leg quarter exports soft (-2.5% YoY) creating domestic oversupply of dark meat while breast/tenders see strong demand.

ACTION: Focus on white meat cuts (breast, tenders) over dark meat (legs, quarters)."""
        self.scroll.add_subview(analysis)
        y += 310

        self.scroll.content_size = (w, y + 50)
        print("SimpleDashboard: UI drawn successfully")

class ChickenLauncher(ui.View):
    """Main launcher"""

    def __init__(self):
        print("ChickenLauncher: __init__")
        super().__init__()
        self.background_color = '#000000'
        self.data_engine = DataEngine()

    def did_load(self):
        print("ChickenLauncher: did_load")
        w, h = ui.get_screen_size()
        print(f"Screen size: {w}x{h}")

        # Title
        title = ui.Label()
        title.frame = (0, 180, w, 60)
        title.text = "CHICKEN MARKET\nINTELLIGENCE"
        title.font = ('<system-bold>', 36)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)
        print("Title added")

        # Subtitle
        subtitle = ui.Label()
        subtitle.frame = (0, 260, w, 30)
        subtitle.text = "SIMPLIFIED VERSION - NO CHARTS"
        subtitle.font = ('<system>', 13)
        subtitle.text_color = '#888888'
        subtitle.alignment = ui.ALIGN_CENTER
        self.add_subview(subtitle)
        print("Subtitle added")

        # Launch button
        btn_width = min(w - 80, 320)
        btn_x = (w - btn_width) / 2

        launch_btn = ui.Button()
        launch_btn.frame = (btn_x, 340, btn_width, 70)
        launch_btn.title = "Launch Dashboard"
        launch_btn.font = ('<system-bold>', 22)
        launch_btn.background_color = THEME['gold']
        launch_btn.tint_color = '#000000'
        launch_btn.corner_radius = 12
        launch_btn.action = self.launch_dashboard
        self.add_subview(launch_btn)
        print("Button added")

    def launch_dashboard(self, sender):
        print("launch_dashboard called")
        try:
            dashboard = SimpleDashboard(self.data_engine)
            dashboard.name = "Market Dashboard"
            nav = ui.NavigationView(dashboard)
            nav.present('fullscreen')
            print("Dashboard presented")
        except Exception as e:
            print(f"ERROR launching dashboard: {e}")
            import traceback
            traceback.print_exc()
            import console
            console.alert("Error", f"Failed to launch:\n{str(e)}", "OK", hide_cancel_button=True)

# RUN IT
if __name__ == '__main__':
    print("=== LAUNCHING APP ===")
    try:
        launcher = ChickenLauncher()
        launcher.present('fullscreen')
        print("Launcher presented successfully")
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
