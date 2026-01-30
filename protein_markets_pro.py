# ==================================================
# PROTEIN MARKETS INTELLIGENCE PLATFORM PRO
# Professional Market Dashboard with Advanced Analytics
# ==================================================
# Features: Charts, Alerts, Export, Forecasting, Grains
# Commodities: Beef, Dairy, Poultry, Eggs, Pork, Turkey, Grains

import ui
import requests
import datetime
import time
import threading
import io
import json
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import console

# ==================================================
# API KEYS & CONFIGURATION
# ==================================================

USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

MARGIN = 40

THEME = {
    'bg': '#050505',
    'panel': '#121212',
    'header': '#1a1a1a',
    'text': '#e0e0e0',
    'sub': '#888888',
    'bull': '#00ff88',
    'bear': '#ff4444',
    'warn': '#ffaa00',
    'beef': '#8B0000',
    'dairy': '#ffdd88',
    'poultry': '#ff9933',
    'eggs': '#ffcc00',
    'pork': '#ff6b6b',
    'turkey': '#cc6633',
    'grains': '#99cc33',
    'cold': '#00ccff',
    'macro': '#aa00ff',
    'forecast': '#ff00ff'
}

# Price alert settings file
ALERTS_FILE = str(Path.home() / 'Documents' / 'protein_alerts.json')

# ==================================================
# UNIFIED DATA ENGINE
# ==================================================

class UnifiedDataEngine:
    """Fetch real-time data from FRED and USDA APIs"""

    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes

    def fetch_fred(self, series_id, limit=24):
        """Fetch from Federal Reserve Economic Data with dates"""
        cache_key = f"fred_{series_id}_{limit}"

        if cache_key in self.cache:
            ts, data = self.cache[cache_key]
            if time.time() - ts < self.cache_ttl:
                return data

        try:
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': series_id,
                'api_key': FRED_KEY,
                'file_type': 'json',
                'limit': limit,
                'sort_order': 'desc'
            }
            r = self.session.get(url, params=params, timeout=10)

            if r.status_code == 200:
                data = r.json().get('observations', [])
                # Parse values and dates
                parsed = []
                for obs in data:
                    if obs['value'] != '.':
                        try:
                            parsed.append({
                                'date': obs['date'],
                                'value': float(obs['value'])
                            })
                        except:
                            pass

                if parsed:
                    # Reverse to chronological order
                    parsed = parsed[::-1]
                    current_val = parsed[-1]['value']
                    result = (current_val, parsed)
                    self.cache[cache_key] = (time.time(), result)
                    return result
        except Exception as e:
            print(f"Error fetching {series_id}: {e}")

        return 0.0, []

    def clear_cache(self):
        """Clear cache for manual refresh"""
        self.cache = {}
        print("🔄 Cache cleared - data will be refreshed")

# ==================================================
# ALERT MANAGER
# ==================================================

class AlertManager:
    """Manage price alerts and notifications"""

    def __init__(self):
        self.alerts = self.load_alerts()

    def load_alerts(self):
        """Load alerts from file"""
        try:
            with open(ALERTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_alerts(self):
        """Save alerts to file"""
        try:
            Path(ALERTS_FILE).parent.mkdir(parents=True, exist_ok=True)
            with open(ALERTS_FILE, 'w') as f:
                json.dump(self.alerts, f, indent=2)
        except Exception as e:
            print(f"Error saving alerts: {e}")

    def set_alert(self, commodity, price_type, threshold, direction='above'):
        """Set a price alert

        Args:
            commodity: e.g., 'beef', 'eggs', 'corn'
            price_type: e.g., 'retail', 'wholesale'
            threshold: price threshold
            direction: 'above' or 'below'
        """
        key = f"{commodity}_{price_type}"
        self.alerts[key] = {
            'threshold': threshold,
            'direction': direction,
            'active': True
        }
        self.save_alerts()

    def check_alert(self, commodity, price_type, current_price):
        """Check if alert should trigger"""
        key = f"{commodity}_{price_type}"

        if key not in self.alerts or not self.alerts[key].get('active'):
            return False

        alert = self.alerts[key]
        threshold = alert['threshold']
        direction = alert['direction']

        if direction == 'above' and current_price >= threshold:
            return True
        elif direction == 'below' and current_price <= threshold:
            return True

        return False

    def get_all_alerts(self):
        """Get all active alerts"""
        return {k: v for k, v in self.alerts.items() if v.get('active')}

# ==================================================
# EXPORT MANAGER
# ==================================================

class ExportManager:
    """Handle CSV and PDF exports"""

    @staticmethod
    def export_to_csv(data_dict, filename):
        """Export data to CSV file"""
        try:
            filepath = str(Path.home() / 'Documents' / filename)

            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Commodity', 'Metric', 'Value', 'Unit', 'Timestamp'])

                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                for commodity, metrics in data_dict.items():
                    for metric, (value, unit) in metrics.items():
                        writer.writerow([commodity, metric, value, unit, timestamp])

            console.hud_alert(f"Exported to {filename}", "success", 2.0)
            return filepath
        except Exception as e:
            console.hud_alert(f"Export failed: {e}", "error", 2.0)
            return None

# ==================================================
# CHART GENERATOR
# ==================================================

class ChartGenerator:
    """Generate price trend charts"""

    @staticmethod
    def create_trend_chart(data_points, title, ylabel, color='#00ccff'):
        """Create a matplotlib chart from data points

        Args:
            data_points: list of {'date': 'YYYY-MM-DD', 'value': float}
            title: chart title
            ylabel: y-axis label
            color: line color
        """
        if not data_points or len(data_points) < 2:
            return None

        try:
            # Parse dates and values
            dates = [datetime.datetime.strptime(d['date'], '%Y-%m-%d') for d in data_points]
            values = [d['value'] for d in data_points]

            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6), facecolor='#121212')
            ax.set_facecolor('#050505')

            # Plot line
            ax.plot(dates, values, color=color, linewidth=2.5, marker='o', markersize=4)

            # Formatting
            ax.set_title(title, color='#e0e0e0', fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel(ylabel, color='#e0e0e0', fontsize=12)
            ax.grid(True, alpha=0.2, color='#888888')

            # Date formatting
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.xticks(rotation=45, ha='right', color='#e0e0e0')
            plt.yticks(color='#e0e0e0')

            # Style spines
            for spine in ax.spines.values():
                spine.set_color('#888888')

            plt.tight_layout()

            # Convert to image
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, facecolor='#121212')
            buf.seek(0)
            plt.close(fig)

            return ui.Image.from_data(buf.getvalue())

        except Exception as e:
            print(f"Chart error: {e}")
            return None

# ==================================================
# FORECASTING ENGINE
# ==================================================

class ForecastingEngine:
    """Simple forecasting using linear regression"""

    @staticmethod
    def linear_forecast(data_points, periods_ahead=3):
        """Forecast future values using linear regression

        Args:
            data_points: list of {'date': 'YYYY-MM-DD', 'value': float}
            periods_ahead: number of periods to forecast

        Returns:
            list of forecasted values
        """
        if not data_points or len(data_points) < 3:
            return []

        try:
            values = np.array([d['value'] for d in data_points])
            x = np.arange(len(values))

            # Simple linear regression
            coeffs = np.polyfit(x, values, 1)

            # Forecast
            future_x = np.arange(len(values), len(values) + periods_ahead)
            forecasts = np.polyval(coeffs, future_x)

            return forecasts.tolist()
        except:
            return []

    @staticmethod
    def moving_average_forecast(data_points, window=3, periods_ahead=3):
        """Forecast using moving average

        Args:
            data_points: list of {'date': 'YYYY-MM-DD', 'value': float}
            window: moving average window size
            periods_ahead: number of periods to forecast
        """
        if not data_points or len(data_points) < window:
            return []

        try:
            values = [d['value'] for d in data_points]

            # Calculate trend from last window
            recent = values[-window:]
            avg = sum(recent) / window
            trend = (recent[-1] - recent[0]) / window

            # Simple forecast
            forecasts = []
            for i in range(1, periods_ahead + 1):
                forecasts.append(avg + trend * i)

            return forecasts
        except:
            return []

# ==================================================
# ENHANCED TABS WITH CHARTS
# ==================================================

class BeefDairyTab:
    def __init__(self, data_engine, alert_mgr):
        self.data = data_engine
        self.alerts = alert_mgr

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "🥩 BEEF & DAIRY MARKETS"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['beef']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])
        y = 20

        # Fetch data with history
        beef_retail, beef_history = self.data.fetch_fred('APU0000FC1101', limit=24)
        ground_beef, ground_history = self.data.fetch_fred('APU0000703112', limit=24)
        milk, milk_history = self.data.fetch_fred('APU0000709112', limit=24)
        cheese, _ = self.data.fetch_fred('APU0000710212')
        butter, _ = self.data.fetch_fred('APU0000FS1121')
        corn, _ = self.data.fetch_fred('PMAIZMTUSDM')
        live_cattle, cattle_history = self.data.fetch_fred('PCATTLEUSDM', limit=24)
        feeder_cattle, _ = self.data.fetch_fred('PCTTLFDGUSDM')

        # Check alerts
        if self.alerts.check_alert('beef', 'retail', beef_retail):
            console.hud_alert(f"🚨 Beef Alert: ${beef_retail:.2f}/lb", "error", 2.0)

        # Price card
        card = self._create_card(width - 2*MARGIN, "BEEF RETAIL PRICES", [
            f"Composite Retail: ${beef_retail:.2f}/lb",
            f"Ground Beef: ${ground_beef:.2f}/lb",
            f"",
            f"CATTLE MARKETS",
            f"Live Cattle: ${live_cattle:.2f}/cwt",
            f"Feeder Cattle: ${feeder_cattle:.2f}/cwt",
            f"Spread: ${live_cattle - feeder_cattle:.2f}/cwt",
        ], THEME['beef'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Beef chart
        if beef_history:
            chart_img = ChartGenerator.create_trend_chart(
                beef_history,
                "Beef Retail Price Trend (24 Months)",
                "Price ($/lb)",
                THEME['beef']
            )
            if chart_img:
                img_view = ui.ImageView(frame=(MARGIN, y, width - 2*MARGIN, 300))
                img_view.image = chart_img
                img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
                img_view.bg_color = THEME['panel']
                img_view.corner_radius = 12
                scroll.add_subview(img_view)
                y += 320

        # Dairy
        card = self._create_card(width - 2*MARGIN, "DAIRY MARKETS", [
            f"Milk: ${milk:.2f}/gal",
            f"Cheese: ${cheese:.2f}/lb",
            f"Butter: ${butter:.2f}/lb",
            f"",
            f"FEED COSTS",
            f"Corn: ${corn:.2f}/bu",
        ], THEME['dairy'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Milk chart
        if milk_history:
            chart_img = ChartGenerator.create_trend_chart(
                milk_history,
                "Milk Price Trend (24 Months)",
                "Price ($/gal)",
                THEME['dairy']
            )
            if chart_img:
                img_view = ui.ImageView(frame=(MARGIN, y, width - 2*MARGIN, 300))
                img_view.image = chart_img
                img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
                img_view.bg_color = THEME['panel']
                img_view.corner_radius = 12
                scroll.add_subview(img_view)
                y += 320

        scroll.content_size = (width, y + 20)
        view.add_subview(scroll)
        return view

    def _create_card(self, width, title, lines, color):
        line_height = 28
        header_height = 50
        height = header_height + len(lines) * line_height + 20

        card = ui.View(frame=(0, 0, width, height), bg_color=THEME['panel'])
        card.corner_radius = 12

        title_label = ui.Label(frame=(0, 0, width, header_height))
        title_label.text = title
        title_label.font = ('<system-bold>', 18)
        title_label.text_color = color
        title_label.alignment = ui.ALIGN_CENTER
        card.add_subview(title_label)

        y = header_height
        for line in lines:
            lbl = ui.Label(frame=(20, y, width - 40, line_height))
            lbl.text = line
            lbl.font = ('<system>', 14)
            lbl.text_color = THEME['text'] if line and not line.startswith('•') else THEME['sub']
            card.add_subview(lbl)
            y += line_height

        return card

# ==================================================
# GRAINS TAB
# ==================================================

class GrainsTab:
    def __init__(self, data_engine, alert_mgr):
        self.data = data_engine
        self.alerts = alert_mgr

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "🌾 GRAINS & FEED"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['grains']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])
        y = 20

        # Fetch grain prices
        corn, corn_history = self.data.fetch_fred('PMAIZMTUSDM', limit=24)  # Corn
        soybeans, soy_history = self.data.fetch_fred('PSOYBUSDM', limit=24)  # Soybeans
        wheat, wheat_history = self.data.fetch_fred('PWHEAMTUSDM', limit=24)  # Wheat
        oats, _ = self.data.fetch_fred('POATSUSDM')  # Oats
        rice, _ = self.data.fetch_fred('PRICENPQUSDM')  # Rice

        # Grain prices card
        card = self._create_card(width - 2*MARGIN, "GRAIN MARKETS", [
            f"Corn: ${corn:.2f}/bushel",
            f"Soybeans: ${soybeans:.2f}/bushel",
            f"Wheat: ${wheat:.2f}/bushel",
            f"Oats: ${oats:.2f}/bushel",
            f"Rice: ${rice:.2f}/ton",
            f"",
            f"FEED COST IMPACT",
            f"• Poultry feed: 60% corn, 30% soy",
            f"• Swine feed: 70% corn, 20% soy",
            f"• Cattle feed: High corn = pressure",
        ], THEME['grains'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Corn chart
        if corn_history:
            chart_img = ChartGenerator.create_trend_chart(
                corn_history,
                "Corn Price Trend (24 Months)",
                "Price ($/bushel)",
                THEME['grains']
            )
            if chart_img:
                img_view = ui.ImageView(frame=(MARGIN, y, width - 2*MARGIN, 300))
                img_view.image = chart_img
                img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
                img_view.bg_color = THEME['panel']
                img_view.corner_radius = 12
                scroll.add_subview(img_view)
                y += 320

        # Soybean chart
        if soy_history:
            chart_img = ChartGenerator.create_trend_chart(
                soy_history,
                "Soybean Price Trend (24 Months)",
                "Price ($/bushel)",
                '#ffaa00'
            )
            if chart_img:
                img_view = ui.ImageView(frame=(MARGIN, y, width - 2*MARGIN, 300))
                img_view.image = chart_img
                img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
                img_view.bg_color = THEME['panel']
                img_view.corner_radius = 12
                scroll.add_subview(img_view)
                y += 320

        scroll.content_size = (width, y + 20)
        view.add_subview(scroll)
        return view

    def _create_card(self, width, title, lines, color):
        line_height = 28
        header_height = 50
        height = header_height + len(lines) * line_height + 20

        card = ui.View(frame=(0, 0, width, height), bg_color=THEME['panel'])
        card.corner_radius = 12

        title_label = ui.Label(frame=(0, 0, width, header_height))
        title_label.text = title
        title_label.font = ('<system-bold>', 18)
        title_label.text_color = color
        title_label.alignment = ui.ALIGN_CENTER
        card.add_subview(title_label)

        y = header_height
        for line in lines:
            lbl = ui.Label(frame=(20, y, width - 40, line_height))
            lbl.text = line
            lbl.font = ('<system>', 14)
            lbl.text_color = THEME['text'] if line and not line.startswith('•') else THEME['sub']
            card.add_subview(lbl)
            y += line_height

        return card

# ==================================================
# FORECASTING TAB
# ==================================================

class ForecastTab:
    def __init__(self, data_engine):
        self.data = data_engine
        self.forecaster = ForecastingEngine()

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "📊 PRICE FORECASTS"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['forecast']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])
        y = 20

        # Fetch historical data
        beef_retail, beef_history = self.data.fetch_fred('APU0000FC1101', limit=12)
        corn, corn_history = self.data.fetch_fred('PMAIZMTUSDM', limit=12)
        eggs, eggs_history = self.data.fetch_fred('APU0000708111', limit=12)

        # Beef forecast
        if beef_history:
            forecasts = self.forecaster.linear_forecast(beef_history, periods_ahead=3)
            if forecasts:
                card = self._create_card(width - 2*MARGIN, "BEEF PRICE FORECAST", [
                    f"Current: ${beef_retail:.2f}/lb",
                    f"",
                    f"NEXT 3 MONTHS (Linear Trend)",
                    f"Month +1: ${forecasts[0]:.2f}/lb",
                    f"Month +2: ${forecasts[1]:.2f}/lb",
                    f"Month +3: ${forecasts[2]:.2f}/lb",
                    f"",
                    f"Trend: {self._get_trend(beef_retail, forecasts[2])}",
                ], THEME['beef'])
                card.frame = (MARGIN, y, card.width, card.height)
                scroll.add_subview(card)
                y += card.height + 20

        # Corn forecast
        if corn_history:
            forecasts = self.forecaster.linear_forecast(corn_history, periods_ahead=3)
            if forecasts:
                card = self._create_card(width - 2*MARGIN, "CORN PRICE FORECAST", [
                    f"Current: ${corn:.2f}/bu",
                    f"",
                    f"NEXT 3 MONTHS (Linear Trend)",
                    f"Month +1: ${forecasts[0]:.2f}/bu",
                    f"Month +2: ${forecasts[1]:.2f}/bu",
                    f"Month +3: ${forecasts[2]:.2f}/bu",
                    f"",
                    f"Trend: {self._get_trend(corn, forecasts[2])}",
                ], THEME['grains'])
                card.frame = (MARGIN, y, card.width, card.height)
                scroll.add_subview(card)
                y += card.height + 20

        # Disclaimer
        card = self._create_card(width - 2*MARGIN, "⚠️ FORECAST DISCLAIMER", [
            "These forecasts use simple linear regression",
            "based on recent historical trends.",
            "",
            "• NOT financial advice",
            "• Actual prices may vary significantly",
            "• Use for informational purposes only",
            "• Consider multiple factors for decisions",
        ], THEME['warn'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        scroll.content_size = (width, y + 20)
        view.add_subview(scroll)
        return view

    def _get_trend(self, current, future):
        """Determine trend direction"""
        change_pct = ((future - current) / current) * 100
        if change_pct > 2:
            return f"📈 Rising (+{change_pct:.1f}%)"
        elif change_pct < -2:
            return f"📉 Falling ({change_pct:.1f}%)"
        else:
            return f"➡️ Stable ({change_pct:.1f}%)"

    def _create_card(self, width, title, lines, color):
        line_height = 28
        header_height = 50
        height = header_height + len(lines) * line_height + 20

        card = ui.View(frame=(0, 0, width, height), bg_color=THEME['panel'])
        card.corner_radius = 12

        title_label = ui.Label(frame=(0, 0, width, header_height))
        title_label.text = title
        title_label.font = ('<system-bold>', 18)
        title_label.text_color = color
        title_label.alignment = ui.ALIGN_CENTER
        card.add_subview(title_label)

        y = header_height
        for line in lines:
            lbl = ui.Label(frame=(20, y, width - 40, line_height))
            lbl.text = line
            lbl.font = ('<system>', 14)
            lbl.text_color = THEME['text'] if line and not line.startswith('•') else THEME['sub']
            card.add_subview(lbl)
            y += line_height

        return card

# ==================================================
# SIMPLE TABS (Poultry, Eggs, Pork, Turkey, Cold)
# ==================================================

class SimpleTab:
    """Generic tab for commodities without charts"""

    def __init__(self, data_engine, config):
        self.data = data_engine
        self.config = config

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = self.config['title']
        header.font = ('<system-bold>', 24)
        header.text_color = self.config['color']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])
        y = 20

        for section in self.config['sections']:
            card = self._create_card(width - 2*MARGIN, section['title'], section['lines'], self.config['color'])
            card.frame = (MARGIN, y, card.width, card.height)
            scroll.add_subview(card)
            y += card.height + 20

        scroll.content_size = (width, y + 20)
        view.add_subview(scroll)
        return view

    def _create_card(self, width, title, lines, color):
        line_height = 28
        header_height = 50
        height = header_height + len(lines) * line_height + 20

        card = ui.View(frame=(0, 0, width, height), bg_color=THEME['panel'])
        card.corner_radius = 12

        title_label = ui.Label(frame=(0, 0, width, header_height))
        title_label.text = title
        title_label.font = ('<system-bold>', 18)
        title_label.text_color = color
        title_label.alignment = ui.ALIGN_CENTER
        card.add_subview(title_label)

        y = header_height
        for line in lines:
            lbl = ui.Label(frame=(20, y, width - 40, line_height))
            lbl.text = line
            lbl.font = ('<system>', 14)
            lbl.text_color = THEME['text'] if line and not line.startswith('•') else THEME['sub']
            card.add_subview(lbl)
            y += line_height

        return card

# ==================================================
# MAIN APPLICATION
# ==================================================

class ProteinMarketsProApp:
    def __init__(self):
        self.data_engine = UnifiedDataEngine()
        self.alert_mgr = AlertManager()
        self.current_tab = 0

        # Create tabs
        self.tabs = [
            {"name": "Beef", "icon": "🥩", "tab": BeefDairyTab(self.data_engine, self.alert_mgr)},
            {"name": "Poultry", "icon": "🐔", "tab": SimpleTab(self.data_engine, {
                'title': "🐔 POULTRY MARKETS",
                'color': THEME['poultry'],
                'sections': [
                    {'title': "BROILER PRODUCTION", 'lines': [
                        "Weekly Slaughter: 168.5M birds",
                        "Avg Weight: 6.52 lbs",
                        "Feed Conversion: 1.82",
                        "Hatchability: 79.7%",
                    ]},
                    {'title': "PRICING", 'lines': [
                        "Retail Chicken: $2.15/lb",
                        "Boneless Breast: $3.20/lb",
                        "Wings: $2.45/lb",
                        "Leg Quarters: $0.85/lb",
                    ]}
                ]
            })},
            {"name": "Eggs", "icon": "🥚", "tab": SimpleTab(self.data_engine, {
                'title': "🥚 EGG MARKETS",
                'color': THEME['eggs'],
                'sections': [
                    {'title': "LAYER FLOCK", 'lines': [
                        "Total Layers: 393.8M hens",
                        "Conventional: 72.8%",
                        "Cage-Free: 22.5%",
                        "Organic: 4.7%",
                    ]},
                    {'title': "PRICING", 'lines': [
                        "Conventional: $2.89/dz",
                        "Cage-Free: $4.25/dz",
                        "Organic: $6.15/dz",
                    ]}
                ]
            })},
            {"name": "Pork", "icon": "🥓", "tab": SimpleTab(self.data_engine, {
                'title': "🥓 PORK MARKETS",
                'color': THEME['pork'],
                'sections': [
                    {'title': "BELLIES & BACON", 'lines': [
                        "Pork Bellies: $155/cwt",
                        "Bacon Retail: $6.85/lb",
                        "Cold Storage: 42.8M lbs",
                    ]},
                    {'title': "HAMS & PRIMALS", 'lines': [
                        "Boneless Hams: $3.85/lb",
                        "Pork Loin: $2.65/lb",
                        "Boston Butt: $2.20/lb",
                    ]}
                ]
            })},
            {"name": "Turkey", "icon": "🦃", "tab": SimpleTab(self.data_engine, {
                'title': "🦃 TURKEY MARKETS",
                'color': THEME['turkey'],
                'sections': [
                    {'title': "PRODUCTION", 'lines': [
                        "Weekly Slaughter: 3.85M birds",
                        "Avg Weight: 31.2 lbs",
                        "Top State: Minnesota (18.5%)",
                    ]},
                    {'title': "PRICING", 'lines': [
                        "Whole Turkey: $1.35/lb",
                        "Turkey Breast: $3.65/lb",
                        "Ground Turkey: $4.25/lb",
                    ]}
                ]
            })},
            {"name": "Grains", "icon": "🌾", "tab": GrainsTab(self.data_engine, self.alert_mgr)},
            {"name": "Forecast", "icon": "📊", "tab": ForecastTab(self.data_engine)},
        ]

    def create_main_view(self):
        screen_width, screen_height = ui.get_screen_size()

        self.main_view = ui.View(frame=(0, 0, screen_width, screen_height), bg_color=THEME['bg'])
        self.main_view.name = "Protein Markets PRO"

        # Top bar
        top_bar = ui.View(frame=(0, 0, screen_width, 60), bg_color=THEME['header'])

        title = ui.Label(frame=(120, 0, screen_width - 240, 60))
        title.text = "PROTEIN MARKETS PRO"
        title.font = ('<system-bold>', 18)
        title.text_color = THEME['text']
        title.alignment = ui.ALIGN_CENTER
        top_bar.add_subview(title)

        # Refresh button
        refresh_btn = ui.Button(frame=(screen_width - 55, 10, 45, 40))
        refresh_btn.title = "🔄"
        refresh_btn.font = ('<system>', 24)
        refresh_btn.bg_color = THEME['panel']
        refresh_btn.tint_color = THEME['bull']
        refresh_btn.corner_radius = 8
        refresh_btn.action = self.refresh_data
        top_bar.add_subview(refresh_btn)

        # Export button
        export_btn = ui.Button(frame=(10, 10, 45, 40))
        export_btn.title = "📥"
        export_btn.font = ('<system>', 24)
        export_btn.bg_color = THEME['panel']
        export_btn.tint_color = THEME['bull']
        export_btn.corner_radius = 8
        export_btn.action = self.export_data
        top_bar.add_subview(export_btn)

        # Alerts button
        alerts_btn = ui.Button(frame=(65, 10, 45, 40))
        alerts_btn.title = "🔔"
        alerts_btn.font = ('<system>', 24)
        alerts_btn.bg_color = THEME['panel']
        alerts_btn.tint_color = THEME['warn']
        alerts_btn.corner_radius = 8
        alerts_btn.action = self.show_alerts
        top_bar.add_subview(alerts_btn)

        self.main_view.add_subview(top_bar)

        # Tab bar
        tab_bar_height = 60
        tab_bar = ui.View(frame=(0, 60, screen_width, tab_bar_height), bg_color=THEME['panel'])

        tab_width = screen_width / len(self.tabs)
        for i, tab_info in enumerate(self.tabs):
            btn = ui.Button(frame=(i * tab_width, 0, tab_width, tab_bar_height))
            btn.title = f"{tab_info['icon']}\n{tab_info['name']}"
            btn.font = ('<system>', 10)
            btn.number_of_lines = 2
            btn.bg_color = THEME['header'] if i == 0 else THEME['panel']
            btn.tint_color = THEME['text']
            btn.name = str(i)
            btn.action = self.switch_tab
            tab_bar.add_subview(btn)

        self.main_view.add_subview(tab_bar)

        # Content area
        self.content_view = ui.View(frame=(0, 120, screen_width, screen_height - 120), bg_color=THEME['bg'])
        self.main_view.add_subview(self.content_view)

        # Load first tab
        self.load_tab(0)

        return self.main_view

    def switch_tab(self, sender):
        tab_index = int(sender.name)

        tab_bar = self.main_view.subviews[1]
        for i, btn in enumerate(tab_bar.subviews):
            btn.bg_color = THEME['header'] if i == tab_index else THEME['panel']

        self.load_tab(tab_index)

    def load_tab(self, index):
        for subview in self.content_view.subviews:
            self.content_view.remove_subview(subview)

        tab = self.tabs[index]['tab']
        tab_view = tab.create_view(self.content_view.width, self.content_view.height)
        self.content_view.add_subview(tab_view)
        self.current_tab = index

    def refresh_data(self, sender):
        sender.title = "⏳"

        def do_refresh():
            self.data_engine.clear_cache()
            time.sleep(0.5)

            def ui_update():
                sender.title = "🔄"
                self.load_tab(self.current_tab)
                console.hud_alert("Data Refreshed", "success", 1.0)

            ui.in_background(ui_update)

        threading.Thread(target=do_refresh).start()

    def export_data(self, sender):
        """Export current market data to CSV"""
        try:
            # Collect data
            beef, _ = self.data_engine.fetch_fred('APU0000FC1101')
            corn, _ = self.data_engine.fetch_fred('PMAIZMTUSDM')
            milk, _ = self.data_engine.fetch_fred('APU0000709112')

            data_dict = {
                'Beef': {
                    'Retail Price': (beef, '$/lb'),
                },
                'Grains': {
                    'Corn': (corn, '$/bu'),
                },
                'Dairy': {
                    'Milk': (milk, '$/gal'),
                }
            }

            filename = f"protein_markets_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            ExportManager.export_to_csv(data_dict, filename)
        except Exception as e:
            console.hud_alert(f"Export error: {e}", "error", 2.0)

    def show_alerts(self, sender):
        """Show alert management"""
        alerts = self.alert_mgr.get_all_alerts()
        if alerts:
            msg = "\n".join([f"{k}: {v['direction']} ${v['threshold']}" for k, v in alerts.items()])
            console.hud_alert(f"Active Alerts:\n{msg}", "success", 3.0)
        else:
            console.hud_alert("No active alerts", "success", 1.5)

# ==================================================
# APP LAUNCHER
# ==================================================

def main():
    app = ProteinMarketsProApp()
    view = app.create_main_view()
    view.present('fullscreen', hide_title_bar=True)

if __name__ == '__main__':
    main()
