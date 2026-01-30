"""
CHICKEN MARKET INTELLIGENCE - Launch Screen
============================================
Simplified launcher for the Chicken Market Intelligence platform
"""

import ui
from config import THEME
from data_engine import DataEngine
from poultry_dashboard import PoultryDashboard


class ChickenMarketLauncher(ui.View):
    """Main launch screen for Chicken Market Intelligence"""

    def __init__(self):
        super().__init__()
        self.background_color = '#000000'  # Pure black background
        self.data_engine = DataEngine()

    def did_load(self):
        """Setup UI when view loads"""
        w, h = ui.get_screen_size()

        # Main Title
        title = ui.Label(frame=(0, 180, w, 60))
        title.text = "CHICKEN MARKET\nINTELLIGENCE"
        title.font = ('<system-bold>', 36)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        # Subtitle
        subtitle = ui.Label(frame=(0, 260, w, 30))
        subtitle.text = "REAL-TIME MARKET ANALYSIS & FORECASTING"
        subtitle.font = ('<system>', 13)
        subtitle.text_color = '#888888'
        subtitle.alignment = ui.ALIGN_CENTER
        self.add_subview(subtitle)

        # Launch Dashboard Button
        btn_width = min(w - 80, 320)
        btn_x = (w - btn_width) / 2
        btn_y = 340

        launch_btn = ui.Button(frame=(btn_x, btn_y, btn_width, 70))
        launch_btn.title = "Launch Dashboard"
        launch_btn.font = ('<system-bold>', 22)
        launch_btn.background_color = THEME['gold']
        launch_btn.tint_color = '#000000'
        launch_btn.corner_radius = 12
        launch_btn.action = self.launch_dashboard
        self.add_subview(launch_btn)

        # Footer info
        footer = ui.Label(frame=(40, h - 100, w - 80, 50))
        footer.text = (
            "Powered by USDA & FRED APIs\n"
            "90-day forecasts • Real-time data"
        )
        footer.font = ('<system>', 12)
        footer.text_color = '#666666'
        footer.alignment = ui.ALIGN_CENTER
        footer.number_of_lines = 2
        self.add_subview(footer)

    def launch_dashboard(self, sender):
        """Launch the chicken/poultry market dashboard"""
        try:
            # Create and present the poultry dashboard
            dashboard = PoultryDashboard(self.data_engine)
            dashboard.name = "Chicken Market Intelligence"
            nav = ui.NavigationView(dashboard)
            nav.present('fullscreen')
        except Exception as e:
            # Show error if dashboard fails to load
            print(f"Error launching dashboard: {e}")
            self._show_error(str(e))

    def _show_error(self, error_msg):
        """Display error message to user"""
        import console
        console.alert(
            "Error",
            f"Failed to launch dashboard:\n{error_msg}",
            "OK",
            hide_cancel_button=True
        )


if __name__ == '__main__':
    # Launch the chicken market intelligence platform
    launcher = ChickenMarketLauncher()
    launcher.present('fullscreen')
