"""
MARKET INTELLIGENCE - Tabbed Dashboard
=======================================
Multi-market tabbed interface for comprehensive market analysis
"""

import ui
from config import THEME, MARGIN
from data_engine import DataEngine


class MarketIntelligenceTabs(ui.View):
    """Tabbed interface for multiple market dashboards"""

    def __init__(self, data_engine):
        super().__init__()
        self.data_engine = data_engine
        self.background_color = THEME['bg']
        self.name = "Market Intelligence"

        # Create tab container
        self.tab_view = ui.View()
        self.tab_view.background_color = THEME['bg']
        self.tab_view.flex = 'WH'
        self.add_subview(self.tab_view)

        # Tab buttons container
        self.tab_bar = ui.View()
        self.tab_bar.background_color = '#1a1a1a'
        self.add_subview(self.tab_bar)

        # Content area
        self.content_view = ui.View()
        self.content_view.background_color = THEME['bg']
        self.add_subview(self.content_view)

        # Track current tab
        self.current_tab = None
        self.tab_buttons = []
        self.dashboards = {}

        # Define tabs
        self.tabs = [
            {'name': 'Poultry', 'icon': '🐔', 'module': 'poultry_dashboard', 'class': 'PoultryDashboard'},
            {'name': 'Eggs', 'icon': '🥚', 'module': 'egg_dashboard', 'class': 'EggDashboard'},
            {'name': 'Beef', 'icon': '🥩', 'module': 'beef_dairy_dashboard', 'class': 'BeefDashboard'},
            {'name': 'Turkey', 'icon': '🦃', 'module': 'turkey_comprehensive_dashboard', 'class': 'TurkeyDashboard'},
            {'name': 'Storage', 'icon': '🧊', 'module': 'cold_storage_dashboard', 'class': 'ColdStorageDashboard'},
        ]

        # Refresh button
        self.right_button_items = [
            ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh_current)
        ]

    def did_load(self):
        """Setup UI when view loads"""
        self.setup_tabs()
        self.switch_to_tab(0)

    def layout(self):
        """Layout subviews"""
        w, h = self.bounds.size

        # Tab bar at top (60pt height)
        tab_bar_height = 60
        self.tab_bar.frame = (0, 0, w, tab_bar_height)

        # Content area below tab bar
        self.content_view.frame = (0, tab_bar_height, w, h - tab_bar_height)

        # Layout tab buttons
        num_tabs = len(self.tabs)
        tab_width = w / num_tabs

        for i, btn in enumerate(self.tab_buttons):
            btn.frame = (i * tab_width, 0, tab_width, tab_bar_height)

    def setup_tabs(self):
        """Create tab buttons"""
        num_tabs = len(self.tabs)
        w = ui.get_screen_size()[0]
        tab_width = w / num_tabs

        for i, tab_info in enumerate(self.tabs):
            btn = ui.Button()
            btn.background_color = '#1a1a1a'
            btn.border_width = 0.5
            btn.border_color = '#333'
            btn.title = f"{tab_info['icon']}\n{tab_info['name']}"
            btn.font = ('<system>', 12)
            btn.tint_color = '#888'
            btn.action = lambda sender, idx=i: self.switch_to_tab(idx)
            btn.number_of_lines = 2

            self.tab_bar.add_subview(btn)
            self.tab_buttons.append(btn)

    def switch_to_tab(self, index):
        """Switch to specified tab"""
        if index == self.current_tab:
            return

        # Update button states
        for i, btn in enumerate(self.tab_buttons):
            if i == index:
                btn.background_color = '#2a2a2a'
                btn.tint_color = THEME['gold']
            else:
                btn.background_color = '#1a1a1a'
                btn.tint_color = '#888'

        # Remove current dashboard
        for subview in self.content_view.subviews:
            subview.remove_from_superview()

        # Load or show dashboard
        tab_info = self.tabs[index]
        tab_name = tab_info['name']

        if tab_name not in self.dashboards:
            # Lazy load dashboard
            try:
                dashboard = self.load_dashboard(tab_info)
                if dashboard:
                    self.dashboards[tab_name] = dashboard
                else:
                    self._show_placeholder(tab_name)
                    return
            except Exception as e:
                print(f"Error loading {tab_name}: {e}")
                self._show_error(tab_name, str(e))
                return

        # Add dashboard to content view
        dashboard = self.dashboards[tab_name]
        dashboard.frame = self.content_view.bounds
        dashboard.flex = 'WH'
        self.content_view.add_subview(dashboard)

        self.current_tab = index

    def load_dashboard(self, tab_info):
        """Dynamically load dashboard module"""
        try:
            module_name = tab_info['module']
            class_name = tab_info['class']

            # Import module dynamically
            module = __import__(module_name, fromlist=[class_name])
            dashboard_class = getattr(module, class_name, None)

            if dashboard_class is None:
                print(f"Class {class_name} not found in {module_name}")
                return None

            # Create dashboard instance
            dashboard = dashboard_class(self.data_engine)
            return dashboard

        except ImportError as e:
            print(f"Could not import {tab_info['module']}: {e}")
            return None
        except Exception as e:
            print(f"Error loading dashboard: {e}")
            return None

    def _show_placeholder(self, tab_name):
        """Show placeholder for unavailable tab"""
        placeholder = ui.View()
        placeholder.background_color = THEME['bg']
        placeholder.frame = self.content_view.bounds
        placeholder.flex = 'WH'

        label = ui.Label()
        label.text = f"{tab_name} Dashboard\n\nComing Soon"
        label.font = ('<system>', 24)
        label.text_color = '#666'
        label.alignment = ui.ALIGN_CENTER
        label.number_of_lines = 3
        label.frame = placeholder.bounds
        label.flex = 'WH'

        placeholder.add_subview(label)
        self.content_view.add_subview(placeholder)

    def _show_error(self, tab_name, error_msg):
        """Show error message"""
        error_view = ui.View()
        error_view.background_color = THEME['bg']
        error_view.frame = self.content_view.bounds
        error_view.flex = 'WH'

        label = ui.Label()
        label.text = f"Error loading {tab_name}\n\n{error_msg}"
        label.font = ('<system>', 14)
        label.text_color = THEME['risk']
        label.alignment = ui.ALIGN_CENTER
        label.number_of_lines = 5
        label.frame = error_view.bounds
        label.flex = 'WH'

        error_view.add_subview(label)
        self.content_view.add_subview(error_view)

    def refresh_current(self, sender):
        """Refresh current dashboard"""
        if self.current_tab is not None:
            tab_name = self.tabs[self.current_tab]['name']
            if tab_name in self.dashboards:
                dashboard = self.dashboards[tab_name]
                if hasattr(dashboard, 'refresh'):
                    dashboard.refresh(None)


if __name__ == '__main__':
    # Launch tabbed market intelligence
    data_engine = DataEngine()
    tabs = MarketIntelligenceTabs(data_engine)
    nav = ui.NavigationView(tabs)
    nav.present('fullscreen')
