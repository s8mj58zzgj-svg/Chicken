"""
PROTEIN MARKETS INTELLIGENCE - Launch Screen
=============================================
Dedicated launcher for the Protein Markets Intelligence platform
Covers: Beef, Dairy, Poultry, Eggs, Pork, Turkey, Cold Storage + Grains
"""

import ui
from config import THEME

class ProteinMarketsLauncher(ui.View):
    """Main launch screen for Protein Markets Intelligence"""

    def __init__(self):
        super().__init__()
        self.background_color = '#000000'  # Pure black background

    def did_load(self):
        """Setup UI when view loads"""
        w, h = ui.get_screen_size()

        # Main Title
        title = ui.Label(frame=(0, 140, w, 80))
        title.text = "PROTEIN MARKETS\nINTELLIGENCE"
        title.font = ('<system-bold>', 38)
        title.text_color = '#ff6b6b'  # Protein red color
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        # Subtitle
        subtitle = ui.Label(frame=(0, 240, w, 30))
        subtitle.text = "COMPREHENSIVE PROTEIN & GRAINS MARKETS"
        subtitle.font = ('<system>', 13)
        subtitle.text_color = '#888888'
        subtitle.alignment = ui.ALIGN_CENTER
        self.add_subview(subtitle)

        # Market Coverage Info
        coverage = ui.Label(frame=(40, 280, w - 80, 60))
        coverage.text = "Beef • Dairy • Poultry • Eggs • Pork • Turkey\nCold Storage • Grains • Feed Commodities"
        coverage.font = ('<system>', 12)
        coverage.text_color = '#666666'
        coverage.alignment = ui.ALIGN_CENTER
        coverage.number_of_lines = 2
        self.add_subview(coverage)

        # Launch Buttons
        btn_width = min(w - 80, 320)
        btn_x = (w - btn_width) / 2
        btn_y = 370

        # Pro Version Button (Primary)
        pro_btn = ui.Button(frame=(btn_x, btn_y, btn_width, 70))
        pro_btn.title = "Launch PRO Dashboard"
        pro_btn.font = ('<system-bold>', 22)
        pro_btn.background_color = '#ff6b6b'  # Protein red
        pro_btn.tint_color = '#000000'
        pro_btn.corner_radius = 12
        pro_btn.action = self.launch_pro_dashboard
        self.add_subview(pro_btn)

        # Standard Version Button (Secondary)
        standard_btn = ui.Button(frame=(btn_x, btn_y + 85, btn_width, 60))
        standard_btn.title = "Launch Standard Dashboard"
        standard_btn.font = ('<system>', 18)
        standard_btn.background_color = '#2a2a2a'
        standard_btn.tint_color = '#ff6b6b'
        standard_btn.corner_radius = 12
        standard_btn.action = self.launch_standard_dashboard
        self.add_subview(standard_btn)

        # Features badge
        features = ui.Label(frame=(btn_x, btn_y + 160, btn_width, 50))
        features.text = "PRO: Charts • Forecasts • Alerts • Export\nStandard: Essential Market Data"
        features.font = ('<system>', 11)
        features.text_color = '#666666'
        features.alignment = ui.ALIGN_CENTER
        features.number_of_lines = 2
        self.add_subview(features)

        # Footer info
        footer = ui.Label(frame=(40, h - 120, w - 80, 70))
        footer.text = (
            "Powered by USDA & FRED APIs\n"
            "7 Data Sources • Real-time Updates\n"
            "Multi-Commodity Analysis"
        )
        footer.font = ('<system>', 11)
        footer.text_color = '#555555'
        footer.alignment = ui.ALIGN_CENTER
        footer.number_of_lines = 3
        self.add_subview(footer)

    def launch_pro_dashboard(self, sender):
        """Launch the PRO version with advanced features"""
        try:
            from protein_markets_pro import ProteinMarketsPro

            dashboard = ProteinMarketsPro()
            view = dashboard.create_main_view()
            view.present('fullscreen', hide_title_bar=True)

        except ImportError as e:
            print(f"Import error: {e}")
            self._show_error("PRO Dashboard not available. Make sure protein_markets_pro.py exists.")
        except Exception as e:
            print(f"Error launching PRO dashboard: {e}")
            self._show_error(str(e))

    def launch_standard_dashboard(self, sender):
        """Launch the standard version"""
        try:
            from protein_markets_app import ProteinMarketsApp

            app = ProteinMarketsApp()
            view = app.create_main_view()
            view.present('fullscreen', hide_title_bar=True)

        except ImportError as e:
            print(f"Import error: {e}")
            self._show_error("Standard Dashboard not available. Make sure protein_markets_app.py exists.")
        except Exception as e:
            print(f"Error launching standard dashboard: {e}")
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
    # Launch the protein markets intelligence platform
    launcher = ProteinMarketsLauncher()
    launcher.present('fullscreen')
