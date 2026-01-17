# ==================================================
# MAIN - Unified Poultry & Egg Market Intelligence Platform
# ==================================================

import ui
from config import THEME
from data_engine import DataEngine
from poultry_dashboard import PoultryDashboard
from egg_dashboard import EggDashboard

class MarketSelector(ui.View):
    """Main navigation screen for selecting market dashboards"""

    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.data_engine = DataEngine()

    def did_load(self):
        """Setup UI when view loads"""
        w, h = ui.get_screen_size()

        # Title
        title = ui.Label(frame=(0, 80, w, 50))
        title.text = "POULTRY & EGG\nMARKET INTELLIGENCE"
        title.font = ('<system-bold>', 32)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        # Subtitle
        subtitle = ui.Label(frame=(0, 145, w, 30))
        subtitle.text = "PROFESSIONAL MARKET ANALYSIS & FORECASTING"
        subtitle.font = ('<system>', 12)
        subtitle.text_color = THEME['sub']
        subtitle.alignment = ui.ALIGN_CENTER
        self.add_subview(subtitle)

        # Buttons container
        btn_width = min(w - 80, 400)
        btn_x = (w - btn_width) / 2
        btn_y = 220

        # Poultry Button
        poultry_btn = self._create_market_button(
            "🐔 POULTRY MARKET",
            "Chicken, Broilers & Processed Products",
            THEME['gold'],
            (btn_x, btn_y, btn_width, 100)
        )
        poultry_btn.action = self.show_poultry
        self.add_subview(poultry_btn)

        # Egg Button
        egg_btn = self._create_market_button(
            "🥚 EGG MARKET",
            "Layer Operations, Retail & Breaking Stock",
            THEME['eggs'],
            (btn_x, btn_y + 120, btn_width, 100)
        )
        egg_btn.action = self.show_eggs
        self.add_subview(egg_btn)

        # Footer info
        footer = ui.Label(frame=(40, h - 100, w - 80, 60))
        footer.text = (
            "Real-time market data powered by USDA & FRED APIs\n"
            "90-day forecasts • Risk analysis • Trade intelligence"
        )
        footer.font = ('<system>', 11)
        footer.text_color = THEME['neutral']
        footer.alignment = ui.ALIGN_CENTER
        footer.number_of_lines = 2
        self.add_subview(footer)

    def _create_market_button(self, title, subtitle, color, frame):
        """Create a styled market selection button"""
        btn = ui.Button(frame=frame)
        btn.background_color = THEME['panel']
        btn.border_color = color
        btn.border_width = 2
        btn.corner_radius = 12

        # Title label
        title_lbl = ui.Label()
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 24)
        title_lbl.text_color = color
        title_lbl.alignment = ui.ALIGN_CENTER
        title_lbl.frame = (10, 20, frame[2] - 20, 35)
        btn.add_subview(title_lbl)

        # Subtitle label
        sub_lbl = ui.Label()
        sub_lbl.text = subtitle
        sub_lbl.font = ('<system>', 13)
        sub_lbl.text_color = THEME['sub']
        sub_lbl.alignment = ui.ALIGN_CENTER
        sub_lbl.frame = (10, 58, frame[2] - 20, 20)
        btn.add_subview(sub_lbl)

        return btn

    def show_poultry(self, sender):
        """Navigate to poultry dashboard"""
        dashboard = PoultryDashboard(self.data_engine)
        dashboard.name = "Poultry Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')

    def show_eggs(self, sender):
        """Navigate to egg dashboard"""
        dashboard = EggDashboard(self.data_engine)
        dashboard.name = "Egg Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')


if __name__ == '__main__':
    # Launch main selector
    selector = MarketSelector()
    selector.present('fullscreen')
