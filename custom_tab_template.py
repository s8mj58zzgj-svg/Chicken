"""
CUSTOM TAB TEMPLATE
===================
Use this template to create your own custom dashboard tab

HOW TO ADD A NEW TAB:
1. Copy this file and rename it (e.g., my_market_dashboard.py)
2. Customize the class name and content
3. Add your tab to market_intelligence_tabs.py in the 'tabs' list:

   {'name': 'MyMarket', 'icon': '📊', 'module': 'my_market_dashboard', 'class': 'MyMarketDashboard'}

"""

import ui
from config import THEME, MARGIN
from ui_components import InsightCard, HeaderLabel


class CustomDashboard(ui.View):
    """Custom Market Dashboard Template"""

    def __init__(self, data_engine):
        super().__init__()
        self.data_engine = data_engine
        self.background_color = THEME['bg']
        self.data = None

        # Create scrollable content area
        self.scroll = ui.ScrollView(flex='WH')
        self.add_subview(self.scroll)

        # Loading indicator
        self.loading = ui.ActivityIndicator(style=ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE)
        self.loading.flex = 'WH'
        self.loading.start()
        self.add_subview(self.loading)

        # Refresh button in navigation bar
        self.right_button_items = [
            ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh)
        ]

    def will_appear(self):
        """Load data when view appears"""
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        """Refresh dashboard data"""
        self.loading.start()

        # Clear existing content
        for sub in self.scroll.subviews:
            sub.remove_from_superview()

        # Load data in background thread
        import threading
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        """Background data loading"""
        # Get market data from data engine
        market_data = self.data_engine.get_market_snapshot()
        dates = self.data_engine.calculate_forecast_dates()

        # Process your custom metrics here
        self.data = self.calculate_custom_metrics(market_data, dates)

        # Update UI on main thread
        ui.delay(self.draw_ui, 0)

    def calculate_custom_metrics(self, market_data, dates):
        """Calculate your custom market metrics"""

        # Example: Get commodity prices
        corn_price = market_data['corn']['current']
        soy_price = market_data['soybean']['current']
        diesel_price = market_data['diesel']['current']

        return {
            'meta': {
                'time': market_data['timestamp'],
                'dates': dates
            },

            # Example section: Market Overview
            'overview': {
                "CORN PRICE": {
                    "val": f"{corn_price:.0f}",
                    "unit": "Index",
                    "status": "FAVORABLE",
                    "insight": f"Corn index at {corn_price:.0f}. This represents the base feed cost for livestock."
                },
                "SOYBEAN PRICE": {
                    "val": f"{soy_price:.0f}",
                    "unit": "Index",
                    "status": "ELEVATED",
                    "insight": f"Soybean index at {soy_price:.0f}. Key protein component in animal feed."
                },
                "DIESEL FUEL": {
                    "val": f"${diesel_price:.2f}",
                    "unit": "/gal",
                    "status": "MODERATE",
                    "insight": f"Diesel at ${diesel_price:.2f}/gal affects transportation and logistics costs."
                }
            },

            # Add more sections as needed
            'custom_section': {
                "CUSTOM METRIC 1": {
                    "val": "123",
                    "unit": "Units",
                    "status": "NORMAL",
                    "insight": "Your custom metric insight here."
                },
                "CUSTOM METRIC 2": {
                    "val": "+5.2%",
                    "unit": "YoY",
                    "status": "GROWING",
                    "insight": "Another custom metric with detailed explanation."
                }
            }
        }

    def draw_ui(self):
        """Render dashboard UI"""
        self.loading.stop()
        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        # HEADER
        self._add_label("📊 CUSTOM MARKET DASHBOARD", 28, THEME['gold'], y, cw, bold=True)
        y += 35

        ts = self.data['meta']['time']
        self._add_label(f"YOUR CUSTOM MARKET ANALYSIS | {ts}", 12, THEME['sub'], y, cw)
        y += 40

        # Section 1: Market Overview
        y = HeaderLabel.create(self.scroll, "1. MARKET OVERVIEW", THEME['macro'], y, cw)
        for k, v in self.data['overview'].items():
            card, h = InsightCard.create(k, v, THEME['macro'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # Section 2: Custom Section
        y = HeaderLabel.create(self.scroll, "2. CUSTOM METRICS", THEME['accent'], y, cw)
        for k, v in self.data['custom_section'].items():
            card, h = InsightCard.create(k, v, THEME['accent'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # Add more sections as needed
        # y = self._draw_custom_section(y, cw)

        # Set scroll content size
        self.scroll.content_size = (w, y + 100)

    def _add_label(self, text, size, color, y, w, bold=False):
        """Add centered label"""
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)


# Example: How to test your dashboard standalone
if __name__ == '__main__':
    from data_engine import DataEngine

    data_engine = DataEngine()
    dashboard = CustomDashboard(data_engine)
    dashboard.name = "Custom Dashboard"
    nav = ui.NavigationView(dashboard)
    nav.present('fullscreen')
