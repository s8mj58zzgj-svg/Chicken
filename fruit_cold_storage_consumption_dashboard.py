# ==================================================
# FRUIT COLD STORAGE & US CONSUMPTION TRENDS DASHBOARD
# 10-Year Historical Analysis
# ==================================================

import ui
import requests
import datetime
import time
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np

# ==================================================
# API CONFIGURATION
# ==================================================

USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"

# ==================================================
# CONFIGURATION
# ==================================================

MARGIN = 40

THEME = {
    'bg': '#050505',
    'text': '#e0e0e0',
    'sub': '#888888',
    'bull': '#00ff88',
    'bear': '#ff4444',
    'warn': '#ffaa00',
    'strawberry': '#ff1493',
    'blueberry': '#4169e1',
    'raspberry': '#e30b5d',
    'blackberry': '#2e0854',
    'cherry': '#de3163',
    'apple': '#8db600',
    'peach': '#ffb347',
    'grape': '#6f2da8',
    'citrus': '#ff8c00',
    'total': '#00ff88'
}

# ==================================================
# FRUIT DATA ENGINE
# ==================================================

class FruitDataEngine:
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.cache_ttl = 1800  # 30 minutes
        self.use_sample_data = False

    def generate_sample_cold_storage(self, fruit_name, category=None):
        """Generate realistic 10-year cold storage history"""
        import random
        import datetime as dt

        # Base values in thousand lbs - realistic cold storage levels
        base_values = {
            'STRAWBERRIES': 120000,
            'BLUEBERRIES': 85000,
            'RASPBERRIES': 35000,
            'BLACKBERRIES': 28000,
            'CHERRIES': 42000,
            'CHERRIES, TART': 35000,
            'CHERRIES, SWEET': 15000,
            'APPLES': 55000,
            'PEACHES': 32000,
            'GRAPES': 18000,
            'CRANBERRIES': 65000,
            'MANGOES': 25000,
            'PINEAPPLE': 38000,
            'MELONS': 45000,
            'ORANGES': 420000,  # Mostly as juice concentrate
            'GRAPEFRUIT': 85000,
            'LEMONS': 12000,
            'LIMES': 8000,
            'BANANAS': 5000,  # Small - mostly fresh market
            'AVOCADOS': 15000
        }

        base = base_values.get(fruit_name, 25000)

        # Generate 10 years (120 months) of history
        history = []
        dates = []
        current_date = dt.datetime.now()

        for i in range(120):  # 10 years
            month_date = current_date - dt.timedelta(days=30*i)
            month = month_date.month

            # Seasonal pattern - harvest increases storage
            seasonal_factor = 1.0
            if fruit_name in ['STRAWBERRIES', 'BLUEBERRIES', 'RASPBERRIES', 'BLACKBERRIES']:
                # Summer berries - peak June-August
                if month in [6, 7, 8]:
                    seasonal_factor = 1.4
                elif month in [9, 10, 11]:
                    seasonal_factor = 1.2
                elif month in [3, 4, 5]:
                    seasonal_factor = 0.7
            elif fruit_name == 'CRANBERRIES':
                # Fall harvest
                if month in [10, 11, 12]:
                    seasonal_factor = 1.5
                elif month in [1, 2, 3]:
                    seasonal_factor = 1.3
                elif month in [7, 8, 9]:
                    seasonal_factor = 0.6
            elif fruit_name in ['CHERRIES', 'CHERRIES, TART', 'CHERRIES, SWEET', 'PEACHES']:
                # Summer stone fruits
                if month in [7, 8, 9]:
                    seasonal_factor = 1.5
                elif month in [10, 11]:
                    seasonal_factor = 1.2
                elif month in [3, 4, 5]:
                    seasonal_factor = 0.6
            elif fruit_name == 'APPLES':
                # Fall harvest
                if month in [10, 11, 12]:
                    seasonal_factor = 1.4
                elif month in [1, 2]:
                    seasonal_factor = 1.2
                elif month in [6, 7, 8]:
                    seasonal_factor = 0.7
            elif fruit_name in ['ORANGES', 'GRAPEFRUIT']:
                # Winter citrus
                if month in [1, 2, 3]:
                    seasonal_factor = 1.3
                elif month in [7, 8, 9]:
                    seasonal_factor = 0.8

            # Growth trend (berry demand increasing over 10 years)
            years_ago = i / 12.0
            if fruit_name in ['BLUEBERRIES', 'RASPBERRIES', 'BLACKBERRIES']:
                growth_trend = 1.0 - (years_ago * 0.05)  # 5% annual growth backward
            elif fruit_name == 'STRAWBERRIES':
                growth_trend = 1.0 - (years_ago * 0.03)  # 3% growth
            elif fruit_name in ['AVOCADOS', 'MANGOES']:
                growth_trend = 1.0 - (years_ago * 0.08)  # 8% growth
            else:
                growth_trend = 1.0 - (years_ago * 0.01)  # 1% growth

            # Random variation
            random_factor = 1.0 + (random.random() - 0.5) * 0.15

            value = base * seasonal_factor * growth_trend * random_factor * 1000
            history.append(value)
            dates.append(month_date.strftime("%b %Y"))

        history.reverse()
        dates.reverse()

        return history, dates

    def generate_sample_consumption(self, fruit_name):
        """Generate realistic 10-year consumption trends (per capita lbs/year)"""
        import random
        import datetime as dt

        # Base per capita consumption in lbs/year
        base_consumption = {
            'STRAWBERRIES': 8.2,
            'BLUEBERRIES': 2.1,
            'RASPBERRIES': 0.8,
            'BLACKBERRIES': 0.6,
            'CHERRIES': 1.2,
            'APPLES': 16.5,
            'PEACHES': 2.8,
            'GRAPES': 7.8,
            'CRANBERRIES': 2.3,
            'MANGOES': 2.9,
            'ORANGES': 12.3,
            'BANANAS': 27.4,
            'AVOCADOS': 8.5,
            'WATERMELON': 15.3,
            'CANTALOUPE': 8.2,
            'PINEAPPLE': 6.4
        }

        base = base_consumption.get(fruit_name, 3.0)

        history = []
        dates = []
        current_date = dt.datetime.now()

        for i in range(10):  # 10 years
            year = current_date.year - i

            # Growth trends
            years_ago = i
            if fruit_name in ['BLUEBERRIES', 'AVOCADOS', 'MANGOES']:
                growth = 1.0 + (years_ago * -0.08)  # Strong growth (going back = lower)
            elif fruit_name in ['STRAWBERRIES', 'RASPBERRIES']:
                growth = 1.0 + (years_ago * -0.04)
            elif fruit_name in ['ORANGES', 'APPLES']:
                growth = 1.0 + (years_ago * 0.01)  # Slight decline
            else:
                growth = 1.0

            random_var = 1.0 + (random.random() - 0.5) * 0.05
            value = base * growth * random_var

            history.append(value)
            dates.append(str(year))

        history.reverse()
        dates.reverse()

        return history, dates

    def fetch_usda_cold_storage(self, fruit_name, category=None):
        """Fetch 10-year cold storage data from USDA NASS"""
        cache_key = f"fruit_cold_{fruit_name}_{category}"

        if cache_key in self.cache:
            ts, data = self.cache[cache_key]
            if time.time() - ts < self.cache_ttl:
                return data

        if self.use_sample_data:
            history, dates = self.generate_sample_cold_storage(fruit_name, category)
            return {'history': history, 'dates': dates}

        try:
            url = "http://quickstats.nass.usda.gov/api/api_GET/"

            search_term = f"{fruit_name}"
            if category:
                search_term += f", {category}"
            search_term += " - COLD STORAGE"

            params = {
                'key': USDA_KEY,
                'short_desc__LIKE': search_term,
                'freq_desc': 'MONTHLY',
                'agg_level_desc': 'NATIONAL',
                'format': 'JSON',
                'year__GE': str(datetime.datetime.now().year - 10)  # 10 years
            }

            r = self.session.get(url, params=params, timeout=15)

            if r.status_code == 403:
                print(f"⚠️  USDA API blocked - using sample data")
                self.use_sample_data = True
                history, dates = self.generate_sample_cold_storage(fruit_name, category)
                return {'history': history, 'dates': dates}

            if r.status_code == 200:
                resp_data = r.json()
                data = resp_data.get('data', [])

                if not data:
                    params['short_desc__LIKE'] = f"{fruit_name} - STOCKS"
                    r = self.session.get(url, params=params, timeout=15)
                    if r.status_code == 200:
                        data = r.json().get('data', [])

                if data:
                    sorted_data = sorted(
                        data,
                        key=lambda x: (x.get('year', ''), x.get('reference_period_desc', '')),
                        reverse=True
                    )

                    history = []
                    dates = []
                    for entry in sorted_data[:120]:  # 10 years
                        try:
                            val = float(entry.get('Value', '0').replace(',', ''))
                            year = entry.get('year', '')
                            month = entry.get('reference_period_desc', '')
                            history.append(val)
                            dates.append(f"{month} {year}")
                        except:
                            pass

                    history.reverse()
                    dates.reverse()

                    result = {'history': history, 'dates': dates}
                    self.cache[cache_key] = (time.time(), result)
                    return result
                else:
                    if not self.use_sample_data:
                        self.use_sample_data = True
                    history, dates = self.generate_sample_cold_storage(fruit_name, category)
                    return {'history': history, 'dates': dates}

        except Exception as e:
            print(f"Error fetching {fruit_name}: {e}")
            if not self.use_sample_data:
                self.use_sample_data = True
            history, dates = self.generate_sample_cold_storage(fruit_name, category)
            return {'history': history, 'dates': dates}

        return {'history': [], 'dates': []}

    def fetch_consumption_data(self, fruit_name):
        """Fetch per capita consumption data (10 years)"""
        # Note: In production, this would fetch from USDA ERS Food Availability data
        # For now, using sample data with realistic trends
        history, dates = self.generate_sample_consumption(fruit_name)
        return {'history': history, 'dates': dates}

    def get_fruit_snapshot(self):
        """Get comprehensive fruit data"""
        print("🍓 FETCHING FRUIT COLD STORAGE & CONSUMPTION DATA...")

        fruits = {
            'STRAWBERRIES': self.fetch_usda_cold_storage('STRAWBERRIES'),
            'BLUEBERRIES': self.fetch_usda_cold_storage('BLUEBERRIES'),
            'RASPBERRIES': self.fetch_usda_cold_storage('RASPBERRIES'),
            'BLACKBERRIES': self.fetch_usda_cold_storage('BLACKBERRIES'),
            'CHERRIES_TOTAL': self.fetch_usda_cold_storage('CHERRIES'),
            'CHERRIES_TART': self.fetch_usda_cold_storage('CHERRIES', 'TART'),
            'CHERRIES_SWEET': self.fetch_usda_cold_storage('CHERRIES', 'SWEET'),
            'APPLES': self.fetch_usda_cold_storage('APPLES', 'FROZEN'),
            'PEACHES': self.fetch_usda_cold_storage('PEACHES', 'FROZEN'),
            'GRAPES': self.fetch_usda_cold_storage('GRAPES', 'FROZEN'),
            'CRANBERRIES': self.fetch_usda_cold_storage('CRANBERRIES'),
            'MANGOES': self.fetch_usda_cold_storage('MANGOES'),
            'PINEAPPLE': self.fetch_usda_cold_storage('PINEAPPLE'),
            'MELONS': self.fetch_usda_cold_storage('MELONS')
        }

        # Get consumption trends
        consumption = {
            'STRAWBERRIES': self.fetch_consumption_data('STRAWBERRIES'),
            'BLUEBERRIES': self.fetch_consumption_data('BLUEBERRIES'),
            'RASPBERRIES': self.fetch_consumption_data('RASPBERRIES'),
            'BLACKBERRIES': self.fetch_consumption_data('BLACKBERRIES'),
            'CHERRIES': self.fetch_consumption_data('CHERRIES'),
            'APPLES': self.fetch_consumption_data('APPLES'),
            'PEACHES': self.fetch_consumption_data('PEACHES'),
            'GRAPES': self.fetch_consumption_data('GRAPES'),
            'CRANBERRIES': self.fetch_consumption_data('CRANBERRIES'),
            'MANGOES': self.fetch_consumption_data('MANGOES'),
            'AVOCADOS': self.fetch_consumption_data('AVOCADOS'),
            'BANANAS': self.fetch_consumption_data('BANANAS'),
            'ORANGES': self.fetch_consumption_data('ORANGES')
        }

        return {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'cold_storage': fruits,
            'consumption': consumption
        }

# ==================================================
# CHART GENERATOR
# ==================================================

class FruitChartGenerator:
    @staticmethod
    def create_cold_storage_chart(data, title, color):
        """Create 10-year cold storage trend chart"""
        if not data.get('history'):
            return None

        fig, ax = plt.subplots(figsize=(12, 5))
        history = [x/1_000_000 for x in data['history']]
        dates = data['dates']

        # Plot every 6 months for 10 years
        indices = range(0, len(history), 6)
        x_vals = list(indices)
        y_vals = [history[i] for i in indices]
        x_labels = [dates[i] for i in indices]

        ax.plot(range(len(history)), history, '-', color=color, linewidth=2, alpha=0.7)
        ax.plot(x_vals, y_vals, 'o', color=color, markersize=6)

        # Calculate trend
        if len(history) > 12:
            recent_avg = np.mean(history[-12:])
            older_avg = np.mean(history[:12])
            ax.axhline(y=recent_avg, color='#00ff88', linestyle='--', linewidth=2,
                      label=f'Recent 12mo Avg: {recent_avg:.1f}M', alpha=0.7)
            ax.axhline(y=older_avg, color='#888888', linestyle='--', linewidth=2,
                      label=f'10yr Ago Avg: {older_avg:.1f}M', alpha=0.7)

        ax.set_title(title, fontsize=16, fontweight='bold', color=color)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Million lbs', fontsize=12)
        ax.set_xticks([indices[i] for i in range(0, len(indices), 4)])
        ax.set_xticklabels([x_labels[i] for i in range(0, len(x_labels), 4)], rotation=45, ha='right')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
        buf.seek(0)
        img = ui.Image.from_data(buf.read())
        plt.close()
        return img

    @staticmethod
    def create_consumption_chart(data, title, color):
        """Create 10-year consumption trend chart"""
        if not data.get('history'):
            return None

        fig, ax = plt.subplots(figsize=(12, 5))
        history = data['history']
        dates = data['dates']

        ax.plot(range(len(history)), history, 'o-', color=color, linewidth=3, markersize=8)

        # Add trend line
        if len(history) >= 3:
            z = np.polyfit(range(len(history)), history, 1)
            p = np.poly1d(z)
            ax.plot(range(len(history)), p(range(len(history))), "--",
                   color='#ffaa00', linewidth=2, alpha=0.7,
                   label=f'Trend: {z[0]:+.2f} lbs/year')

        ax.set_title(title, fontsize=16, fontweight='bold', color=color)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Per Capita Consumption (lbs/year)', fontsize=12)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha='right')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
        buf.seek(0)
        img = ui.Image.from_data(buf.read())
        plt.close()
        return img

    @staticmethod
    def create_comparison_chart(storage_data, title):
        """Create comparison chart for multiple fruits"""
        fig, ax = plt.subplots(figsize=(12, 6))

        colors = {
            'STRAWBERRIES': '#ff1493',
            'BLUEBERRIES': '#4169e1',
            'RASPBERRIES': '#e30b5d',
            'BLACKBERRIES': '#2e0854',
            'CHERRIES_TOTAL': '#de3163',
            'APPLES': '#8db600',
            'CRANBERRIES': '#dc143c'
        }

        for fruit_name, data in storage_data.items():
            if fruit_name in colors and data.get('history'):
                history = [x/1_000_000 for x in data['history']]
                # Sample every 3 months for clarity
                indices = range(0, len(history), 3)
                sampled = [history[i] for i in indices if i < len(history)]
                ax.plot(range(len(sampled)), sampled, '-',
                       color=colors[fruit_name], linewidth=2,
                       label=fruit_name.replace('_', ' ').title(), alpha=0.8)

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Time (Quarters)', fontsize=12)
        ax.set_ylabel('Million lbs', fontsize=12)
        ax.legend(fontsize=10, loc='best')
        ax.grid(True, alpha=0.3)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
        buf.seek(0)
        img = ui.Image.from_data(buf.read())
        plt.close()
        return img

# ==================================================
# UI COMPONENTS
# ==================================================

class MetricCard:
    @staticmethod
    def create(title, value, unit, insight, color, w, y):
        card_h = 110
        card = ui.View(frame=(MARGIN, y, w, card_h))
        card.background_color = '#1a1a1a'
        card.corner_radius = 8

        title_lbl = ui.Label(frame=(15, 10, w-30, 20))
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 14)
        title_lbl.text_color = color
        card.add_subview(title_lbl)

        val_lbl = ui.Label(frame=(15, 32, w-30, 24))
        val_lbl.text = f"{value} {unit}"
        val_lbl.font = ('<system-bold>', 18)
        val_lbl.text_color = 'white'
        card.add_subview(val_lbl)

        insight_tv = ui.TextView(frame=(15, 60, w-30, 45))
        insight_tv.text = insight
        insight_tv.font = ('<system>', 10)
        insight_tv.text_color = THEME['text']
        insight_tv.background_color = '#1a1a1a'
        insight_tv.editable = False
        card.add_subview(insight_tv)

        return card, card_h

class ChartCard:
    @staticmethod
    def create(title, chart_img, w, y):
        card_h = 350
        card = ui.View(frame=(MARGIN, y, w, card_h))
        card.background_color = '#1a1a1a'
        card.corner_radius = 8

        title_lbl = ui.Label(frame=(15, 10, w-30, 20))
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 14)
        title_lbl.text_color = THEME['bull']
        card.add_subview(title_lbl)

        img_view = ui.ImageView(frame=(15, 40, w-30, 300))
        img_view.image = chart_img
        img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        card.add_subview(img_view)

        return card, card_h

# ==================================================
# DASHBOARD VIEW
# ==================================================

class FruitDashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.name = 'Fruit Storage & Consumption'
        self.data_engine = FruitDataEngine()

    def refresh_data(self, sender):
        print("🔄 REFRESHING FRUIT DATA...")
        self.data_engine.cache.clear()
        self.data_engine.use_sample_data = False
        for subview in list(self.subviews):
            self.remove_subview(subview)
        self.layout()
        print("✅ REFRESH COMPLETE")

    def layout(self):
        w = self.width
        h = self.height

        # Refresh button
        refresh_btn = ui.Button(frame=(w - 100, 10, 80, 32))
        refresh_btn.title = '🔄 Refresh'
        refresh_btn.background_color = '#1a1a1a'
        refresh_btn.tint_color = THEME['bull']
        refresh_btn.corner_radius = 6
        refresh_btn.action = self.refresh_data
        self.add_subview(refresh_btn)

        scroll = ui.ScrollView(frame=(0, 0, w, h))
        scroll.flex = 'WH'
        self.add_subview(scroll)

        # Fetch data
        data = self.data_engine.get_fruit_snapshot()
        chart_gen = FruitChartGenerator()

        cw = w - (MARGIN * 2)
        y = 40

        # HEADER
        title = ui.Label(frame=(MARGIN, y, cw, 30))
        title.text = "🍓 FRUIT COLD STORAGE & CONSUMPTION TRENDS"
        title.font = ('<system-bold>', 22)
        title.text_color = THEME['total']
        title.alignment = ui.ALIGN_CENTER
        scroll.add_subview(title)
        y += 35

        sub = ui.Label(frame=(MARGIN, y, cw, 15))
        sub.text = f"10-YEAR HISTORICAL ANALYSIS | {data['timestamp']}"
        sub.font = ('<system>', 11)
        sub.text_color = THEME['sub']
        sub.alignment = ui.ALIGN_CENTER
        scroll.add_subview(sub)
        y += 20

        if self.data_engine.use_sample_data:
            warning = ui.Label(frame=(MARGIN, y, cw, 15))
            warning.text = "⚠️  USING SAMPLE DATA - USDA API unavailable"
            warning.font = ('<system-bold>', 10)
            warning.text_color = THEME['warn']
            warning.alignment = ui.ALIGN_CENTER
            scroll.add_subview(warning)
            y += 25
        else:
            y += 20

        # COMPARISON CHART
        comp_chart = chart_gen.create_comparison_chart(
            data['cold_storage'],
            "ALL FRUITS - COLD STORAGE COMPARISON (10 YEARS)"
        )
        if comp_chart:
            card, card_h = ChartCard.create("10-Year Cold Storage Trends - All Fruits", comp_chart, cw, y)
            scroll.add_subview(card)
            y += card_h + 20

        # INDIVIDUAL FRUIT SECTIONS
        fruits = [
            ('STRAWBERRIES', 'Strawberries', THEME['strawberry']),
            ('BLUEBERRIES', 'Blueberries', THEME['blueberry']),
            ('RASPBERRIES', 'Raspberries', THEME['raspberry']),
            ('BLACKBERRIES', 'Blackberries', THEME['blackberry']),
            ('CHERRIES_TOTAL', 'Cherries (All)', THEME['cherry']),
            ('APPLES', 'Apples (Frozen)', THEME['apple']),
            ('PEACHES', 'Peaches (Frozen)', THEME['peach']),
            ('GRAPES', 'Grapes (Frozen)', THEME['grape']),
            ('CRANBERRIES', 'Cranberries', '#dc143c')
        ]

        for fruit_key, fruit_name, color in fruits:
            # Section header
            header = ui.Label(frame=(MARGIN, y, cw, 25))
            header.text = f"═══ {fruit_name.upper()} ═══"
            header.font = ('<system-bold>', 16)
            header.text_color = color
            header.alignment = ui.ALIGN_CENTER
            scroll.add_subview(header)
            y += 35

            # Cold storage data
            storage_data = data['cold_storage'].get(fruit_key, {})
            if storage_data.get('history'):
                current = storage_data['history'][-1] / 1_000_000
                year_ago = storage_data['history'][-13] / 1_000_000 if len(storage_data['history']) > 13 else current
                ten_yr_ago = storage_data['history'][0] / 1_000_000 if storage_data['history'] else current

                yoy_change = ((current - year_ago) / year_ago * 100) if year_ago > 0 else 0
                decade_change = ((current - ten_yr_ago) / ten_yr_ago * 100) if ten_yr_ago > 0 else 0

                insight = f"Current: {current:.1f}M lbs. YoY: {yoy_change:+.1f}%. 10-yr change: {decade_change:+.1f}%. "
                if decade_change > 20:
                    insight += "STRONG GROWTH over decade."
                elif decade_change > 5:
                    insight += "Moderate growth trend."
                elif decade_change < -5:
                    insight += "Declining trend."
                else:
                    insight += "Stable over decade."

                card, card_h = MetricCard.create(
                    f"{fruit_name} - Cold Storage",
                    f"{current:.1f}M",
                    "lbs",
                    insight,
                    color,
                    cw,
                    y
                )
                scroll.add_subview(card)
                y += card_h + 15

                # Cold storage chart
                storage_chart = chart_gen.create_cold_storage_chart(
                    storage_data,
                    f"{fruit_name} - 10 Year Cold Storage History",
                    color
                )
                if storage_chart:
                    card, card_h = ChartCard.create(f"{fruit_name} Cold Storage Trend", storage_chart, cw, y)
                    scroll.add_subview(card)
                    y += card_h + 15

            # Consumption data
            consumption_key = fruit_key.replace('_TOTAL', '').replace('_', ' ')
            consumption_data = data['consumption'].get(consumption_key.strip(), {})
            if consumption_data.get('history'):
                current_cons = consumption_data['history'][-1]
                ten_yr_ago_cons = consumption_data['history'][0]
                cons_change = ((current_cons - ten_yr_ago_cons) / ten_yr_ago_cons * 100) if ten_yr_ago_cons > 0 else 0

                cons_insight = f"Current: {current_cons:.1f} lbs/person/year. 10-yr change: {cons_change:+.1f}%. "
                if cons_change > 30:
                    cons_insight += "BOOMING consumer demand!"
                elif cons_change > 10:
                    cons_insight += "Growing consumption trend."
                elif cons_change < -10:
                    cons_insight += "Declining consumption."
                else:
                    cons_insight += "Stable demand."

                card, card_h = MetricCard.create(
                    f"{fruit_name} - US Consumption",
                    f"{current_cons:.1f}",
                    "lbs/capita",
                    cons_insight,
                    color,
                    cw,
                    y
                )
                scroll.add_subview(card)
                y += card_h + 15

                # Consumption chart
                cons_chart = chart_gen.create_consumption_chart(
                    consumption_data,
                    f"{fruit_name} - US Per Capita Consumption (10 Years)",
                    color
                )
                if cons_chart:
                    card, card_h = ChartCard.create(f"{fruit_name} Consumption Trend", cons_chart, cw, y)
                    scroll.add_subview(card)
                    y += card_h + 25

        scroll.content_size = (w, y + 100)

# ==================================================
# MAIN
# ==================================================

if __name__ == '__main__':
    plt.style.use('dark_background')
    v = FruitDashboard()
    v.present('fullscreen')
