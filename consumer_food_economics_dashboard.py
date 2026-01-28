# ==================================================
# COMPREHENSIVE CONSUMER FOOD ECONOMICS DASHBOARD
# CPI, Consumer Spending, Shopping Behavior, Channels, Sentiment
# The Ultimate Economist Report for Food Consumer Behavior
# ==================================================

import ui
import requests
import datetime
import time
import io
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# ==================================================
# CONFIGURATION
# ==================================================

THEME = {
    'bg': '#050505',
    'text': '#e0e0e0',
    'sub': '#888888',
    'bull': '#00ff88',
    'bear': '#ff4444',
    'warn': '#ffaa00',
    'food': '#ff6b35',
    'home': '#4ecdc4',
    'away': '#f7b731',
    'online': '#5f27cd',
    'retail': '#00d2d3',
    'sentiment': '#ff9ff3',
    'highlight': '#00ffff'
}

# Shopping channels with realistic market shares (2026)
SHOPPING_CHANNELS = {
    'Supermarkets/Grocery': 0.38,  # Traditional grocers (declining)
    'Warehouse Clubs': 0.16,       # Costco, Sam's Club (growing)
    'Supercenters': 0.22,          # Walmart (stable/declining slightly)
    'Online Grocery': 0.12,        # Amazon, Instacart (explosive growth)
    'Dollar Stores': 0.05,         # Growing rapidly
    'Convenience Stores': 0.03,
    'Natural/Organic': 0.02,       # Whole Foods, etc.
    'Other': 0.02
}

# Food categories for CPI tracking
FOOD_CATEGORIES = {
    'Meat/Poultry/Fish': 0.18,
    'Dairy': 0.12,
    'Fruits/Vegetables': 0.16,
    'Cereals/Bakery': 0.14,
    'Beverages': 0.10,
    'Snacks/Sweets': 0.08,
    'Fats/Oils': 0.04,
    'Baby Food': 0.03,
    'Other': 0.15
}

# ==================================================
# COMPREHENSIVE DATA ENGINE
# ==================================================

class ConsumerFoodEconomicsEngine:
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}

    def generate_cpi_data(self, years=12):
        """Generate CPI data - food at home and away"""
        import random

        end_year = 2026
        start_year = end_year - years

        cpi_data = {
            'dates': [],
            'food_at_home': [],      # CPI index (1982-84 = 100)
            'food_away': [],         # CPI index
            'all_food': [],
            'meat_poultry': [],
            'dairy': [],
            'fruits_veg': [],
            'cereals': [],
            'beverages': [],
            'all_items': []          # Overall CPI for comparison
        }

        # Base values (2016)
        base_home = 241.5
        base_away = 258.3
        base_all_food = 248.6
        base_meat = 218.5
        base_dairy = 216.8
        base_fruits = 288.2
        base_cereals = 275.4
        base_beverages = 242.1
        base_all_items = 240.0

        # Trends (annual growth rates)
        home_trend = 0.025      # 2.5% annual
        away_trend = 0.035      # 3.5% annual (faster than home)
        meat_trend = 0.032
        dairy_trend = 0.021
        fruits_trend = 0.028
        cereals_trend = 0.024
        beverages_trend = 0.022
        all_items_trend = 0.023

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                cpi_data['dates'].append(date)

                years_delta = (year - start_year) + (month - 1) / 12.0

                # Seasonal factors
                seasonal_home = 1.0
                seasonal_away = 1.0

                if month in [6, 7, 8]:  # Summer - fresh produce expensive
                    seasonal_home = 1.015
                elif month in [11, 12]:  # Holiday season
                    seasonal_home = 1.025
                    seasonal_away = 1.035

                noise = random.uniform(-0.008, 0.008)

                # Calculate indices
                home = base_home * (1 + home_trend * years_delta) * seasonal_home * (1 + noise)
                away = base_away * (1 + away_trend * years_delta) * seasonal_away * (1 + noise * 0.9)
                all_food = (home * 0.55 + away * 0.45)  # Weighted average

                meat = base_meat * (1 + meat_trend * years_delta) * (1 + noise * 1.2)
                dairy = base_dairy * (1 + dairy_trend * years_delta) * (1 + noise * 0.8)
                fruits = base_fruits * (1 + fruits_trend * years_delta) * (1 + noise * 1.5)
                cereals = base_cereals * (1 + cereals_trend * years_delta) * (1 + noise * 0.9)
                beverages = base_beverages * (1 + beverages_trend * years_delta) * (1 + noise * 0.7)
                all_items = base_all_items * (1 + all_items_trend * years_delta) * (1 + noise * 0.6)

                # COVID impact (2020-2021)
                if year == 2020 and month >= 3:
                    home *= 1.04  # Panic buying, supply chain
                    away *= 0.88  # Restaurants closed
                    meat *= 1.18  # Meat plant closures
                elif year == 2021:
                    home *= 1.035
                    away *= 0.95

                # 2021-2022 inflation surge
                if year == 2022:
                    inflation_factor = 1.08
                    home *= inflation_factor
                    away *= inflation_factor * 0.95
                    meat *= inflation_factor * 1.1
                    dairy *= inflation_factor

                cpi_data['food_at_home'].append(round(home, 1))
                cpi_data['food_away'].append(round(away, 1))
                cpi_data['all_food'].append(round(all_food, 1))
                cpi_data['meat_poultry'].append(round(meat, 1))
                cpi_data['dairy'].append(round(dairy, 1))
                cpi_data['fruits_veg'].append(round(fruits, 1))
                cpi_data['cereals'].append(round(cereals, 1))
                cpi_data['beverages'].append(round(beverages, 1))
                cpi_data['all_items'].append(round(all_items, 1))

        return cpi_data

    def generate_consumer_spending(self, years=12):
        """Generate consumer food spending data"""
        import random

        end_year = 2026
        start_year = end_year - years

        spending = {
            'year': [],
            'food_at_home': [],          # Billions $
            'food_away': [],             # Billions $
            'total_food': [],
            'per_capita_home': [],       # $ per person
            'per_capita_away': [],
            'per_capita_total': [],
            'pct_income_food': [],       # % of disposable income
            'pct_home': [],              # % at home vs away
            'pct_away': []
        }

        # Base spending (2016 - billions)
        base_home = 778.5
        base_away = 782.2
        us_population_2016 = 323.1  # Million
        pop_growth = 0.0055

        # Trends
        home_spending_growth = 0.038
        away_spending_growth = 0.045  # Faster pre-COVID

        for year in range(start_year, end_year + 1):
            years_delta = year - start_year

            population = us_population_2016 * (1 + pop_growth * years_delta)

            home_spend = base_home * (1 + home_spending_growth * years_delta) * random.uniform(0.98, 1.02)
            away_spend = base_away * (1 + away_spending_growth * years_delta) * random.uniform(0.98, 1.02)

            # COVID impact
            if year == 2020:
                home_spend *= 1.12  # Surge in grocery
                away_spend *= 0.62  # Collapse in restaurants
            elif year == 2021:
                home_spend *= 1.06
                away_spend *= 0.82
            elif year == 2022:
                away_spend *= 1.15  # Strong recovery

            total = home_spend + away_spend

            pc_home = (home_spend * 1000) / population
            pc_away = (away_spend * 1000) / population
            pc_total = pc_home + pc_away

            pct_home = (home_spend / total) * 100
            pct_away = (away_spend / total) * 100

            # % of disposable income (realistic range 9-11%)
            pct_income = 9.8 + (years_delta * 0.08) + random.uniform(-0.2, 0.2)
            if year == 2022:
                pct_income += 0.8  # Inflation impact

            spending['year'].append(year)
            spending['food_at_home'].append(round(home_spend, 1))
            spending['food_away'].append(round(away_spend, 1))
            spending['total_food'].append(round(total, 1))
            spending['per_capita_home'].append(round(pc_home, 0))
            spending['per_capita_away'].append(round(pc_away, 0))
            spending['per_capita_total'].append(round(pc_total, 0))
            spending['pct_income_food'].append(round(pct_income, 1))
            spending['pct_home'].append(round(pct_home, 1))
            spending['pct_away'].append(round(pct_away, 1))

        return spending

    def generate_shopping_behavior(self, years=12):
        """Generate shopping behavior metrics"""
        import random

        end_year = 2026
        start_year = end_year - years

        behavior = {
            'year': [],
            'trips_per_week': [],        # Average shopping trips
            'basket_size_items': [],     # Items per trip
            'basket_value': [],          # $ per trip
            'online_penetration': [],    # % of grocery sales
            'stockup_pct': [],          # % of trips that are stock-up
            'fillin_pct': [],           # % of trips that are fill-in
            'avg_distance_miles': []     # Miles traveled to store
        }

        # Base metrics (2016)
        base_trips = 1.6         # Per week
        base_items = 15.2
        base_value = 52.80
        base_online = 2.1        # %
        base_stockup = 32.0

        # Trends
        trips_trend = -0.025     # Fewer trips (consolidation)
        items_trend = 0.018      # More items per trip
        value_trend = 0.042      # $ growing faster (inflation + items)
        online_trend = 0.95      # Explosive growth in online

        for year in range(start_year, end_year + 1):
            years_delta = year - start_year

            trips = base_trips * (1 + trips_trend * years_delta) * random.uniform(0.98, 1.02)
            items = base_items * (1 + items_trend * years_delta) * random.uniform(0.97, 1.03)
            value = base_value * (1 + value_trend * years_delta) * random.uniform(0.98, 1.02)
            online = base_online * (1 + online_trend * years_delta) * random.uniform(0.95, 1.05)
            stockup = base_stockup + (years_delta * 0.8) + random.uniform(-1, 1)

            # COVID impact
            if year == 2020:
                trips *= 0.82  # Fewer trips
                items *= 1.28  # Much larger baskets
                value *= 1.35
                online *= 2.8  # Huge online surge
                stockup += 18  # Stock-up shopping
            elif year == 2021:
                trips *= 0.88
                items *= 1.18
                value *= 1.22
                online *= 1.8
                stockup += 12

            fillin = 100 - stockup
            distance = 4.2 - (years_delta * 0.08) + random.uniform(-0.2, 0.2)  # Declining (more local/online)

            behavior['year'].append(year)
            behavior['trips_per_week'].append(round(trips, 2))
            behavior['basket_size_items'].append(round(items, 1))
            behavior['basket_value'].append(round(value, 2))
            behavior['online_penetration'].append(round(online, 1))
            behavior['stockup_pct'].append(round(stockup, 1))
            behavior['fillin_pct'].append(round(fillin, 1))
            behavior['avg_distance_miles'].append(round(distance, 1))

        return behavior

    def generate_channel_evolution(self, years=12):
        """Generate shopping channel market share evolution"""
        import random

        end_year = 2026
        start_year = end_year - years

        channels = {
            'year': [],
            'traditional_grocery': [],    # %
            'warehouse_clubs': [],
            'supercenters': [],
            'online': [],
            'dollar_stores': [],
            'convenience': [],
            'natural_organic': [],
            'other': []
        }

        # Base shares (2016) - %
        base = {
            'traditional_grocery': 48.5,
            'warehouse_clubs': 11.2,
            'supercenters': 25.8,
            'online': 1.8,
            'dollar_stores': 2.2,
            'convenience': 3.5,
            'natural_organic': 1.8,
            'other': 5.2
        }

        # Annual changes (percentage points per year)
        trends = {
            'traditional_grocery': -0.95,  # Declining
            'warehouse_clubs': 0.42,       # Growing
            'supercenters': -0.35,         # Slight decline
            'online': 0.88,                # Explosive growth
            'dollar_stores': 0.24,         # Growing
            'convenience': -0.02,
            'natural_organic': 0.018,
            'other': -0.22
        }

        for year in range(start_year, end_year + 1):
            years_delta = year - start_year

            shares = {}
            for channel, base_share in base.items():
                share = base_share + (trends[channel] * years_delta)
                share *= random.uniform(0.98, 1.02)

                # COVID acceleration for online
                if channel == 'online' and year == 2020:
                    share *= 2.1
                elif channel == 'online' and year == 2021:
                    share *= 1.5
                elif channel == 'traditional_grocery' and year == 2020:
                    share *= 0.92

                shares[channel] = max(0, share)

            # Normalize to 100%
            total = sum(shares.values())
            for channel in shares:
                shares[channel] = (shares[channel] / total) * 100

            channels['year'].append(year)
            channels['traditional_grocery'].append(round(shares['traditional_grocery'], 1))
            channels['warehouse_clubs'].append(round(shares['warehouse_clubs'], 1))
            channels['supercenters'].append(round(shares['supercenters'], 1))
            channels['online'].append(round(shares['online'], 1))
            channels['dollar_stores'].append(round(shares['dollar_stores'], 1))
            channels['convenience'].append(round(shares['convenience'], 1))
            channels['natural_organic'].append(round(shares['natural_organic'], 1))
            channels['other'].append(round(shares['other'], 1))

        return channels

    def generate_consumer_sentiment(self, years=12):
        """Generate consumer sentiment and confidence indices"""
        import random

        end_year = 2026
        start_year = end_year - years

        sentiment = {
            'dates': [],
            'confidence_index': [],      # Consumer confidence (100 = 1985 baseline)
            'food_security': [],         # % feeling secure about affording food
            'value_consciousness': [],   # Index of price sensitivity
            'inflation_concern': [],     # % very concerned about food prices
            'trade_down': []            # % trading down to cheaper options
        }

        # Base values (2016)
        base_confidence = 98.5
        base_security = 82.3
        base_value = 68.2
        base_inflation = 42.5
        base_tradedown = 38.2

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                sentiment['dates'].append(date)

                years_delta = (year - start_year) + (month - 1) / 12.0

                # Base trends
                confidence = base_confidence + (years_delta * 1.2) + random.uniform(-3, 3)
                security = base_security + (years_delta * 0.3) + random.uniform(-2, 2)
                value = base_value + (years_delta * 1.5) + random.uniform(-2, 2)
                inflation = base_inflation + (years_delta * 0.8) + random.uniform(-2, 2)
                tradedown = base_tradedown + (years_delta * 0.6) + random.uniform(-2, 2)

                # COVID impact
                if year == 2020 and month >= 3:
                    confidence *= 0.72  # Huge drop
                    security *= 0.85
                    value += 15
                    inflation += 8
                    tradedown += 12
                elif year == 2021:
                    confidence *= 0.88
                    security *= 0.92
                    value += 8

                # 2022-2023 inflation impact
                if year >= 2022:
                    inflation_factor = 1.0 + ((year - 2021) * 0.15)
                    inflation *= inflation_factor
                    tradedown *= inflation_factor * 0.95
                    value *= inflation_factor * 0.9
                    security *= 0.95

                sentiment['confidence_index'].append(round(confidence, 1))
                sentiment['food_security'].append(round(min(100, max(0, security)), 1))
                sentiment['value_consciousness'].append(round(value, 1))
                sentiment['inflation_concern'].append(round(min(100, max(0, inflation)), 1))
                sentiment['trade_down'].append(round(min(100, max(0, tradedown)), 1))

        return sentiment

    def generate_food_trends(self, years=12):
        """Generate emerging food trend adoption"""
        import random

        end_year = 2026
        start_year = end_year - years

        trends = {
            'year': [],
            'private_label': [],         # % of grocery sales
            'organic': [],               # % of food sales
            'plant_based_meat': [],      # % of meat alternatives
            'meal_kits': [],            # % of households
            'ready_to_eat': [],         # % growth YoY
            'local_food': [],           # % prioritizing local
            'sustainable': []            # % considering sustainability
        }

        # Base values (2016)
        base = {
            'private_label': 17.8,
            'organic': 5.3,
            'plant_based_meat': 0.8,
            'meal_kits': 2.1,
            'ready_to_eat': 8.5,
            'local_food': 28.5,
            'sustainable': 24.2
        }

        # Growth rates
        growth = {
            'private_label': 0.052,      # 5.2% CAGR
            'organic': 0.088,            # 8.8% CAGR
            'plant_based_meat': 0.28,    # 28% CAGR (declining after peak)
            'meal_kits': 0.15,
            'ready_to_eat': 0.065,
            'local_food': 0.038,
            'sustainable': 0.052
        }

        for year in range(start_year, end_year + 1):
            years_delta = year - start_year

            values = {}
            for trend_name, base_val in base.items():
                value = base_val * (1 + growth[trend_name] * years_delta)
                value *= random.uniform(0.97, 1.03)

                # Special adjustments
                if trend_name == 'private_label' and year >= 2022:
                    value *= 1.12  # Inflation drives private label
                if trend_name == 'plant_based_meat' and year >= 2023:
                    value *= 0.88  # Market correction
                if trend_name == 'meal_kits' and year == 2020:
                    value *= 2.2  # COVID surge

                values[trend_name] = value

            trends['year'].append(year)
            trends['private_label'].append(round(values['private_label'], 1))
            trends['organic'].append(round(values['organic'], 1))
            trends['plant_based_meat'].append(round(values['plant_based_meat'], 1))
            trends['meal_kits'].append(round(values['meal_kits'], 1))
            trends['ready_to_eat'].append(round(values['ready_to_eat'], 1))
            trends['local_food'].append(round(values['local_food'], 1))
            trends['sustainable'].append(round(values['sustainable'], 1))

        return trends

    def get_comprehensive_snapshot(self):
        """Get ALL consumer food economics data"""
        print("🛒 FETCHING COMPREHENSIVE CONSUMER FOOD DATA...")

        cpi = self.generate_cpi_data(12)
        spending = self.generate_consumer_spending(12)
        behavior = self.generate_shopping_behavior(12)
        channels = self.generate_channel_evolution(12)
        sentiment = self.generate_consumer_sentiment(12)
        trends = self.generate_food_trends(12)

        # Current metrics
        current_cpi_home = cpi['food_at_home'][-1]
        current_cpi_away = cpi['food_away'][-1]
        prev_year_cpi_home = cpi['food_at_home'][-13] if len(cpi['food_at_home']) > 13 else cpi['food_at_home'][0]
        yoy_inflation_home = ((current_cpi_home - prev_year_cpi_home) / prev_year_cpi_home) * 100

        current_online = behavior['online_penetration'][-1]
        current_trips = behavior['trips_per_week'][-1]
        current_basket = behavior['basket_value'][-1]

        print(f"   Food at Home CPI: {current_cpi_home:.1f} ({yoy_inflation_home:+.1f}% YoY)")
        print(f"   Food Away CPI: {current_cpi_away:.1f}")
        print(f"   Online Penetration: {current_online:.1f}%")
        print(f"   Trips/Week: {current_trips:.2f}")
        print(f"   Basket Size: ${current_basket:.2f}")
        print("✅ DATA READY")

        return {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'cpi': cpi,
            'spending': spending,
            'behavior': behavior,
            'channels': channels,
            'sentiment': sentiment,
            'trends': trends,
            'current_metrics': {
                'cpi_home': current_cpi_home,
                'cpi_away': current_cpi_away,
                'inflation_yoy': yoy_inflation_home,
                'online_pct': current_online,
                'trips_per_week': current_trips,
                'basket_value': current_basket,
                'total_spending': spending['total_food'][-1],
                'per_capita': spending['per_capita_total'][-1],
                'confidence': sentiment['confidence_index'][-1],
                'food_security': sentiment['food_security'][-1]
            }
        }

# ==================================================
# CHART FUNCTIONS
# ==================================================

def create_cpi_chart(cpi, w, h):
    """Create CPI chart with food at home and away"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(w/100, h/100), dpi=100)
    fig.patch.set_facecolor('#0a0a0a')

    dates = cpi['dates']

    # Top: Food at home vs away
    ax1.set_facecolor('#0a0a0a')
    ax1.plot(dates, cpi['food_at_home'], color=THEME['home'], linewidth=2.5, label='Food at Home', alpha=0.9)
    ax1.plot(dates, cpi['food_away'], color=THEME['away'], linewidth=2.5, label='Food Away from Home', alpha=0.9)
    ax1.plot(dates, cpi['all_items'], color=THEME['sub'], linewidth=1.5, label='All Items CPI', alpha=0.7, linestyle='--')

    ax1.set_ylabel('CPI Index (1982-84=100)', color=THEME['text'], fontsize=10)
    ax1.set_title('Consumer Price Index - Food (12-Year)', color=THEME['text'], fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.2, color=THEME['sub'])
    ax1.tick_params(colors=THEME['text'], labelsize=8)

    # COVID highlight
    covid_start = datetime.date(2020, 3, 1)
    covid_end = datetime.date(2021, 12, 1)
    ax1.axvspan(covid_start, covid_end, alpha=0.1, color=THEME['bear'])

    # Bottom: Food categories
    ax2.set_facecolor('#0a0a0a')
    ax2.plot(dates, cpi['meat_poultry'], color=THEME['bear'], linewidth=2, label='Meat/Poultry', alpha=0.9)
    ax2.plot(dates, cpi['fruits_veg'], color=THEME['bull'], linewidth=2, label='Fruits/Veg', alpha=0.9)
    ax2.plot(dates, cpi['dairy'], color=THEME['online'], linewidth=2, label='Dairy', alpha=0.9)
    ax2.plot(dates, cpi['cereals'], color=THEME['warn'], linewidth=2, label='Cereals', alpha=0.9)

    ax2.set_xlabel('Year', color=THEME['text'], fontsize=10)
    ax2.set_ylabel('CPI Index', color=THEME['text'], fontsize=10)
    ax2.set_title('Food Categories CPI', color=THEME['text'], fontsize=11, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=7)
    ax2.grid(True, alpha=0.2, color=THEME['sub'])
    ax2.tick_params(colors=THEME['text'], labelsize=8)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=100)
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_spending_chart(spending, w, h):
    """Create consumer spending chart"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(w/100, h/100), dpi=100)
    fig.patch.set_facecolor('#0a0a0a')

    years = spending['year']

    # Top: Spending breakdown
    ax1.set_facecolor('#0a0a0a')
    ax1.bar(years, spending['food_at_home'], color=THEME['home'], alpha=0.8, label='Food at Home')
    ax1.bar(years, spending['food_away'], bottom=spending['food_at_home'],
            color=THEME['away'], alpha=0.8, label='Food Away')

    ax1.set_ylabel('Billions $', color=THEME['text'], fontsize=10)
    ax1.set_title('Consumer Food Spending', color=THEME['text'], fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.2, color=THEME['sub'], axis='y')
    ax1.tick_params(colors=THEME['text'], labelsize=8)

    # COVID annotation
    if 2020 in years:
        idx = years.index(2020)
        ax1.annotate('COVID', xy=(2020, spending['total_food'][idx]),
                    xytext=(0, 20), textcoords='offset points',
                    color=THEME['bear'], fontsize=8, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color=THEME['bear']))

    # Bottom: Per capita spending
    ax2.set_facecolor('#0a0a0a')
    ax2.plot(years, spending['per_capita_home'], color=THEME['home'], linewidth=2.5,
             marker='o', markersize=4, label='Per Capita Home', alpha=0.9)
    ax2.plot(years, spending['per_capita_away'], color=THEME['away'], linewidth=2.5,
             marker='s', markersize=4, label='Per Capita Away', alpha=0.9)

    ax2.set_xlabel('Year', color=THEME['text'], fontsize=10)
    ax2.set_ylabel('$ per Person', color=THEME['text'], fontsize=10)
    ax2.set_title('Per Capita Food Spending', color=THEME['text'], fontsize=11, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(True, alpha=0.2, color=THEME['sub'])
    ax2.tick_params(colors=THEME['text'], labelsize=8)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=100)
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_channels_chart(channels, w, h):
    """Create shopping channels evolution chart"""
    fig, ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')

    years = channels['year']

    # Stacked area chart
    ax.fill_between(years, 0, channels['online'],
                    color=THEME['online'], alpha=0.8, label='Online Grocery')
    ax.fill_between(years, channels['online'],
                    [o+w for o,w in zip(channels['online'], channels['warehouse_clubs'])],
                    color=THEME['bull'], alpha=0.8, label='Warehouse Clubs')
    ax.fill_between(years, [o+w for o,w in zip(channels['online'], channels['warehouse_clubs'])],
                    [o+w+s for o,w,s in zip(channels['online'], channels['warehouse_clubs'], channels['supercenters'])],
                    color=THEME['warn'], alpha=0.8, label='Supercenters')
    ax.fill_between(years, [o+w+s for o,w,s in zip(channels['online'], channels['warehouse_clubs'], channels['supercenters'])],
                    [o+w+s+t for o,w,s,t in zip(channels['online'], channels['warehouse_clubs'],
                                                  channels['supercenters'], channels['traditional_grocery'])],
                    color=THEME['home'], alpha=0.8, label='Traditional Grocery')
    ax.fill_between(years, [o+w+s+t for o,w,s,t in zip(channels['online'], channels['warehouse_clubs'],
                                                         channels['supercenters'], channels['traditional_grocery'])],
                    100, color=THEME['sub'], alpha=0.6, label='Other')

    ax.set_xlabel('Year', color=THEME['text'], fontsize=10)
    ax.set_ylabel('Market Share (%)', color=THEME['text'], fontsize=10)
    ax.set_title('Shopping Channel Evolution', color=THEME['text'], fontsize=12, fontweight='bold', pad=15)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper left', fontsize=7)
    ax.grid(True, alpha=0.2, color=THEME['sub'])
    ax.tick_params(colors=THEME['text'], labelsize=8)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=100)
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_behavior_chart(behavior, w, h):
    """Create shopping behavior chart"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(w/100, h/100), dpi=100)
    fig.patch.set_facecolor('#0a0a0a')

    years = behavior['year']

    # Top: Trips and basket size
    ax1.set_facecolor('#0a0a0a')
    ax1_twin = ax1.twinx()

    ln1 = ax1.plot(years, behavior['trips_per_week'], color=THEME['away'], linewidth=2.5,
                   marker='o', markersize=5, label='Trips/Week', alpha=0.9)
    ln2 = ax1_twin.plot(years, behavior['basket_size_items'], color=THEME['home'], linewidth=2.5,
                        marker='s', markersize=5, label='Items/Trip', alpha=0.9)

    ax1.set_ylabel('Trips per Week', color=THEME['away'], fontsize=10)
    ax1_twin.set_ylabel('Items per Trip', color=THEME['home'], fontsize=10)
    ax1.set_title('Shopping Frequency & Basket Size', color=THEME['text'], fontsize=12, fontweight='bold')

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left', fontsize=8)

    ax1.grid(True, alpha=0.2, color=THEME['sub'])
    ax1.tick_params(colors=THEME['text'], labelsize=8)
    ax1_twin.tick_params(colors=THEME['text'], labelsize=8)

    # Bottom: Online penetration
    ax2.set_facecolor('#0a0a0a')
    ax2.plot(years, behavior['online_penetration'], color=THEME['online'], linewidth=3,
             marker='o', markersize=5, label='Online Grocery %', alpha=0.9)
    ax2.fill_between(years, 0, behavior['online_penetration'], color=THEME['online'], alpha=0.3)

    ax2.set_xlabel('Year', color=THEME['text'], fontsize=10)
    ax2.set_ylabel('% of Grocery Sales', color=THEME['text'], fontsize=10)
    ax2.set_title('Online Grocery Penetration', color=THEME['text'], fontsize=11, fontweight='bold')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.2, color=THEME['sub'])
    ax2.tick_params(colors=THEME['text'], labelsize=8)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=100)
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_sentiment_chart(sentiment, w, h):
    """Create consumer sentiment chart"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(w/100, h/100), dpi=100)
    fig.patch.set_facecolor('#0a0a0a')

    dates = sentiment['dates']

    # Top: Confidence and food security
    ax1.set_facecolor('#0a0a0a')
    ax1.plot(dates, sentiment['confidence_index'], color=THEME['bull'], linewidth=2.5,
             label='Consumer Confidence', alpha=0.9)
    ax1.plot(dates, sentiment['food_security'], color=THEME['home'], linewidth=2.5,
             label='Food Security', alpha=0.9)

    ax1.set_ylabel('Index / %', color=THEME['text'], fontsize=10)
    ax1.set_title('Consumer Confidence & Food Security', color=THEME['text'], fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, alpha=0.2, color=THEME['sub'])
    ax1.tick_params(colors=THEME['text'], labelsize=8)

    # Bottom: Inflation concern and trade-down
    ax2.set_facecolor('#0a0a0a')
    ax2.plot(dates, sentiment['inflation_concern'], color=THEME['bear'], linewidth=2.5,
             label='Inflation Concern', alpha=0.9)
    ax2.plot(dates, sentiment['trade_down'], color=THEME['warn'], linewidth=2.5,
             label='Trading Down', alpha=0.9)

    ax2.set_xlabel('Year', color=THEME['text'], fontsize=10)
    ax2.set_ylabel('% of Consumers', color=THEME['text'], fontsize=10)
    ax2.set_title('Price Sensitivity & Behavior', color=THEME['text'], fontsize=11, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(True, alpha=0.2, color=THEME['sub'])
    ax2.tick_params(colors=THEME['text'], labelsize=8)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=100)
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_trends_chart(trends, w, h):
    """Create food trends adoption chart"""
    fig, ax = plt.subplots(figsize=(w/100, h/100), dpi=100)
    fig.patch.set_facecolor('#0a0a0a')
    ax.set_facecolor('#0a0a0a')

    years = trends['year']

    ax.plot(years, trends['private_label'], color=THEME['home'], linewidth=2.5,
            marker='o', markersize=4, label='Private Label', alpha=0.9)
    ax.plot(years, trends['organic'], color=THEME['bull'], linewidth=2.5,
            marker='s', markersize=4, label='Organic', alpha=0.9)
    ax.plot(years, trends['ready_to_eat'], color=THEME['away'], linewidth=2.5,
            marker='^', markersize=4, label='Ready-to-Eat', alpha=0.9)
    ax.plot(years, trends['plant_based_meat'], color=THEME['online'], linewidth=2,
            marker='d', markersize=4, label='Plant-Based Meat', alpha=0.8)
    ax.plot(years, trends['meal_kits'], color=THEME['warn'], linewidth=2,
            marker='v', markersize=4, label='Meal Kits', alpha=0.8)

    ax.set_xlabel('Year', color=THEME['text'], fontsize=10)
    ax.set_ylabel('% Market Share / Adoption', color=THEME['text'], fontsize=10)
    ax.set_title('Food Trends & Innovation Adoption', color=THEME['text'], fontsize=12, fontweight='bold', pad=15)
    ax.legend(loc='upper left', fontsize=7)
    ax.grid(True, alpha=0.2, color=THEME['sub'])
    ax.tick_params(colors=THEME['text'], labelsize=8)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='#0a0a0a', dpi=100)
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

# ==================================================
# MAIN DASHBOARD
# ==================================================

class ConsumerFoodEconomicsDashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.name = 'Consumer Food Economics'
        self.data_engine = ConsumerFoodEconomicsEngine()
        self.current_data = None
        self.data_loaded = False

    def did_load(self):
        if not self.data_loaded:
            self.refresh_data(None)

    def refresh_data(self, sender):
        print("🔄 REFRESHING CONSUMER FOOD DATA...")
        self.current_data = self.data_engine.get_comprehensive_snapshot()
        self.data_loaded = True
        self.rebuild_ui()
        print("✅ REFRESH COMPLETE")

    def rebuild_ui(self):
        for subview in list(self.subviews):
            self.remove_subview(subview)
        self.layout()

    def layout(self):
        if not self.data_loaded and self.width > 0 and self.height > 0:
            self.refresh_data(None)
            return

        if not self.current_data:
            loading = ui.Label(frame=(0, 0, self.width, self.height))
            loading.text = 'Loading Consumer Food Economics Data...'
            loading.alignment = ui.ALIGN_CENTER
            loading.text_color = THEME['text']
            loading.font = ('<system>', 20)
            self.add_subview(loading)
            return

        w = self.width
        h = self.height

        scroll = ui.ScrollView(frame=(0, 0, w, h))
        scroll.background_color = THEME['bg']
        self.add_subview(scroll)

        y = 10

        # Header
        header = ui.View(frame=(0, y, w, 70))
        header.background_color = '#1a1a1a'
        scroll.add_subview(header)

        title = ui.Label(frame=(15, 10, w-120, 30))
        title.text = '🛒 CONSUMER FOOD ECONOMICS'
        title.font = ('<system-bold>', 18)
        title.text_color = THEME['food']
        header.add_subview(title)

        subtitle = ui.Label(frame=(15, 40, w-120, 20))
        subtitle.text = f"CPI, Spending, Behavior, Sentiment | {self.current_data['timestamp']}"
        subtitle.font = ('<system>', 9)
        subtitle.text_color = THEME['sub']
        header.add_subview(subtitle)

        refresh_btn = ui.Button(frame=(w-100, 20, 85, 35))
        refresh_btn.title = '🔄 Refresh'
        refresh_btn.background_color = THEME['bull']
        refresh_btn.tint_color = 'white'
        refresh_btn.corner_radius = 6
        refresh_btn.action = self.refresh_data
        header.add_subview(refresh_btn)

        y += 80

        # Metrics cards
        metrics = self.current_data['current_metrics']
        card_width = (w - 90) / 5

        metric_data = [
            ('CPI HOME', f"{metrics['cpi_home']:.1f}", f"{metrics['inflation_yoy']:+.1f}% YoY", THEME['home']),
            ('CPI AWAY', f"{metrics['cpi_away']:.1f}", 'Restaurants', THEME['away']),
            ('ONLINE %', f"{metrics['online_pct']:.1f}%", 'Grocery Sales', THEME['online']),
            ('BASKET', f"${metrics['basket_value']:.2f}", f"{metrics['trips_per_week']:.1f} trips/wk", THEME['food']),
            ('SPENDING', f"${metrics['total_spending']:.0f}B", f"${metrics['per_capita']:.0f} per capita", THEME['bull'])
        ]

        for i, (label, value, sub, color) in enumerate(metric_data):
            card = self.create_metric_card(15 + i * (card_width + 15), y, card_width, 80, label, value, sub, color)
            scroll.add_subview(card)

        y += 95

        # CPI Chart
        section_title = ui.Label(frame=(15, y, w-30, 25))
        section_title.text = 'CONSUMER PRICE INDEX (CPI) - 12-YEAR TRENDS'
        section_title.font = ('<system-bold>', 14)
        section_title.text_color = THEME['highlight']
        scroll.add_subview(section_title)
        y += 30

        chart_h = 380
        cpi_chart = create_cpi_chart(self.current_data['cpi'], w-30, chart_h)
        cpi_img = ui.ImageView(frame=(15, y, w-30, chart_h))
        cpi_img.image = cpi_chart
        scroll.add_subview(cpi_img)
        y += chart_h + 15

        # Spending Chart
        section_title = ui.Label(frame=(15, y, w-30, 25))
        section_title.text = 'CONSUMER FOOD SPENDING'
        section_title.font = ('<system-bold>', 14)
        section_title.text_color = THEME['highlight']
        scroll.add_subview(section_title)
        y += 30

        chart_h = 350
        spending_chart = create_spending_chart(self.current_data['spending'], w-30, chart_h)
        spending_img = ui.ImageView(frame=(15, y, w-30, chart_h))
        spending_img.image = spending_chart
        scroll.add_subview(spending_img)
        y += chart_h + 15

        # Shopping Channels
        section_title = ui.Label(frame=(15, y, w-30, 25))
        section_title.text = 'SHOPPING CHANNELS - WHERE CONSUMERS SHOP'
        section_title.font = ('<system-bold>', 14)
        section_title.text_color = THEME['highlight']
        scroll.add_subview(section_title)
        y += 30

        chart_h = 300
        channels_chart = create_channels_chart(self.current_data['channels'], w-30, chart_h)
        channels_img = ui.ImageView(frame=(15, y, w-30, chart_h))
        channels_img.image = channels_chart
        scroll.add_subview(channels_img)
        y += chart_h + 15

        # Shopping Behavior
        section_title = ui.Label(frame=(15, y, w-30, 25))
        section_title.text = 'SHOPPING BEHAVIOR & BASKET METRICS'
        section_title.font = ('<system-bold>', 14)
        section_title.text_color = THEME['highlight']
        scroll.add_subview(section_title)
        y += 30

        chart_h = 350
        behavior_chart = create_behavior_chart(self.current_data['behavior'], w-30, chart_h)
        behavior_img = ui.ImageView(frame=(15, y, w-30, chart_h))
        behavior_img.image = behavior_chart
        scroll.add_subview(behavior_img)
        y += chart_h + 15

        # Consumer Sentiment
        section_title = ui.Label(frame=(15, y, w-30, 25))
        section_title.text = 'CONSUMER SENTIMENT & CONFIDENCE'
        section_title.font = ('<system-bold>', 14)
        section_title.text_color = THEME['highlight']
        scroll.add_subview(section_title)
        y += 30

        chart_h = 350
        sentiment_chart = create_sentiment_chart(self.current_data['sentiment'], w-30, chart_h)
        sentiment_img = ui.ImageView(frame=(15, y, w-30, chart_h))
        sentiment_img.image = sentiment_chart
        scroll.add_subview(sentiment_img)
        y += chart_h + 15

        # Food Trends
        section_title = ui.Label(frame=(15, y, w-30, 25))
        section_title.text = 'FOOD TRENDS & INNOVATION'
        section_title.font = ('<system-bold>', 14)
        section_title.text_color = THEME['highlight']
        scroll.add_subview(section_title)
        y += 30

        chart_h = 300
        trends_chart = create_trends_chart(self.current_data['trends'], w-30, chart_h)
        trends_img = ui.ImageView(frame=(15, y, w-30, chart_h))
        trends_img.image = trends_chart
        scroll.add_subview(trends_img)
        y += chart_h + 20

        scroll.content_size = (w, y)

    def create_metric_card(self, x, y, w, h, label, value, subtext, color):
        card = ui.View(frame=(x, y, w, h))
        card.background_color = '#1a1a1a'
        card.corner_radius = 8

        lbl = ui.Label(frame=(10, 5, w-20, 16))
        lbl.text = label
        lbl.font = ('<system-bold>', 9)
        lbl.text_color = THEME['sub']
        card.add_subview(lbl)

        val = ui.Label(frame=(10, 24, w-20, 26))
        val.text = value
        val.font = ('<system-bold>', 15)
        val.text_color = color
        card.add_subview(val)

        sub = ui.Label(frame=(10, 52, w-20, 20))
        sub.text = subtext
        sub.font = ('<system>', 8)
        sub.text_color = THEME['text']
        sub.number_of_lines = 2
        card.add_subview(sub)

        return card

if __name__ == '__main__':
    plt.style.use('dark_background')
    v = ConsumerFoodEconomicsDashboard()
    v.present('fullscreen')
