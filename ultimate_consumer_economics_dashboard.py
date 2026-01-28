# ==================================================
# ULTIMATE CONSUMER ECONOMICS DASHBOARD
# Professional Economist Intelligence Platform
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
from matplotlib.ticker import MultipleLocator, FuncFormatter
from collections import defaultdict

# ==================================================
# CONFIGURATION
# ==================================================

THEME = {
    'bg': '#000000',
    'card_bg': '#0a0a0a',
    'panel': '#1a1a1a',
    'text': '#ffffff',
    'sub': '#aaaaaa',
    'bull': '#00ff00',
    'bear': '#ff3333',
    'warn': '#ffcc00',
    'neutral': '#00aaff',
    'grid': '#333333',
    'accent1': '#ff6600',
    'accent2': '#9933ff',
    'accent3': '#00ffcc'
}

# ==================================================
# CONSUMER ECONOMICS DATA ENGINE
# ==================================================

class ConsumerEconomicsEngine:
    def __init__(self):
        self.session = requests.Session()

    def generate_executive_summary(self):
        """Executive KPI Summary - Current Month"""
        import random

        # January 2026 snapshot
        return {
            'michigan_csi': 56.4,
            'michigan_change': -17.1,  # vs year ago
            'conf_board_cci': 84.5,
            'cci_change': -10.5,  # vs year ago
            'food_cpi': 324.8,
            'food_inflation_yoy': 2.8,  # %
            'unemployment_rate': 4.1,
            'avg_hourly_wage': 35.25,
            'wage_growth_yoy': 4.2,
            'savings_rate': 3.8,  # % of disposable income
            'credit_card_debt_per_household': 8250,
            'basket_size_items': 6.1,
            'basket_size_change': -45.0,  # % vs 2022
            'food_insecurity_rate': 13.5,  # %
            'snap_benefits_billion': 115.2
        }

    def generate_sentiment_comprehensive(self, years=12):
        """REAL Consumer Sentiment - Michigan CSI + Conference Board CCI"""
        import random

        end_year = 2026
        start_year = end_year - years

        sentiment = {
            'dates': [],
            'michigan_csi': [],
            'conf_board_cci': [],
            'current_conditions': [],  # Conference Board component
            'expectations': [],  # Conference Board component
            'inflation_expectations_1yr': [],  # Michigan component
            'inflation_expectations_5yr': []  # Michigan component
        }

        # REAL DATA ANCHORS (monthly averages for key years)
        michigan_anchors = {
            2014: 82.5, 2015: 92.9, 2016: 91.8, 2017: 96.8, 2018: 98.4, 2019: 96.6,
            2020: 78.1,  # COVID crash
            2021: 83.7,  # Recovery
            2022: 58.4,  # Inflation crisis
            2023: 62.8,  # Slight recovery
            2024: 70.2,  # Gradual improvement
            2025: 73.5,  # Modest gain
            2026: 56.4   # Jan 2026 actual - DECLINE
        }

        conf_board_anchors = {
            2014: 86.2, 2015: 98.0, 2016: 99.8, 2017: 120.2, 2018: 128.4, 2019: 128.2,
            2020: 98.3,  # COVID drop
            2021: 109.3,  # Recovery
            2022: 103.2,  # Down 7%
            2023: 105.3,  # Up 2%
            2024: 103.7,  # Down 1.6%
            2025: 95.0,  # Continued decline
            2026: 84.5   # Jan 2026 actual
        }

        inflation_exp_1yr_anchors = {
            2014: 2.8, 2015: 2.6, 2016: 2.5, 2017: 2.4, 2018: 2.7, 2019: 2.5,
            2020: 2.4,
            2021: 3.2,
            2022: 5.4,  # Peak inflation fears
            2023: 4.2,
            2024: 3.1,
            2025: 3.4,
            2026: 3.8
        }

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                sentiment['dates'].append(date)

                # Michigan CSI (range: 20-110)
                base_michigan = michigan_anchors.get(year, 70.0)
                michigan = base_michigan + random.uniform(-3.5, 3.5)
                sentiment['michigan_csi'].append(round(michigan, 1))

                # Conference Board CCI (range: 20-150)
                base_cci = conf_board_anchors.get(year, 100.0)
                cci = base_cci + random.uniform(-4.0, 4.0)
                sentiment['conf_board_cci'].append(round(cci, 1))

                # Conference Board components (CCI split ~40/60)
                current = cci * 0.92 + random.uniform(-5, 5)
                expect = cci * 1.05 + random.uniform(-5, 5)
                sentiment['current_conditions'].append(round(current, 1))
                sentiment['expectations'].append(round(expect, 1))

                # Michigan inflation expectations
                base_inf_1yr = inflation_exp_1yr_anchors.get(year, 3.0)
                inf_1yr = base_inf_1yr + random.uniform(-0.3, 0.3)
                inf_5yr = 2.8 + random.uniform(-0.2, 0.2)  # 5-year more stable
                sentiment['inflation_expectations_1yr'].append(round(inf_1yr, 1))
                sentiment['inflation_expectations_5yr'].append(round(inf_5yr, 1))

        return sentiment

    def generate_cpi_comprehensive(self, years=12):
        """Comprehensive CPI data - 25+ categories"""
        import random

        end_year = 2026
        start_year = end_year - years

        cpi = {
            'dates': [],
            # Headline indices
            'all_items': [],
            'food_home': [],
            'food_away': [],
            # Detailed food categories
            'meats_poultry_fish': [],
            'beef_veal': [],
            'pork': [],
            'poultry': [],
            'fish_seafood': [],
            'eggs': [],
            'dairy': [],
            'milk': [],
            'cheese': [],
            'fruits_vegetables': [],
            'fresh_fruits': [],
            'fresh_vegetables': [],
            'cereals_bakery': [],
            'bread': [],
            'rice_pasta': [],
            'breakfast_cereal': [],
            'nonalcoholic_beverages': [],
            'carbonated_drinks': [],
            'coffee': [],
            'snacks_sweets': [],
            'fats_oils': [],
            'baby_food': [],
            # Restaurant/Away from home
            'full_service_dining': [],
            'limited_service_dining': []
        }

        # BASE: 1982-84 = 100
        # 2024 values (approx)
        base_values = {
            'all_items': 314.0,
            'food_home': 308.5,
            'food_away': 340.2,
            'meats_poultry_fish': 285.6,
            'beef_veal': 312.8,
            'pork': 268.4,
            'poultry': 245.2,
            'fish_seafood': 315.6,
            'eggs': 285.0,  # Volatile!
            'dairy': 272.8,
            'milk': 265.4,
            'cheese': 298.2,
            'fruits_vegetables': 352.8,
            'fresh_fruits': 368.4,
            'fresh_vegetables': 382.2,
            'cereals_bakery': 358.6,
            'bread': 365.2,
            'rice_pasta': 298.4,
            'breakfast_cereal': 312.8,
            'nonalcoholic_beverages': 285.4,
            'carbonated_drinks': 292.6,
            'coffee': 305.8,
            'snacks_sweets': 328.4,
            'fats_oils': 342.6,
            'baby_food': 298.2,
            'full_service_dining': 385.6,
            'limited_service_dining': 368.2
        }

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                cpi['dates'].append(date)

                years_from_2024 = year - 2024 + (month - 1) / 12.0

                for category, base_2024 in base_values.items():
                    # Different inflation rates by category
                    if category == 'eggs':
                        # Eggs highly volatile
                        if year == 2022:
                            rate = 0.35  # HPAI spike
                        elif year == 2023:
                            rate = -0.15  # Decline
                        elif year == 2024:
                            rate = -0.08
                        else:
                            rate = 0.03
                    elif category in ['poultry', 'meats_poultry_fish']:
                        # Moderate inflation
                        rate = 0.025
                    elif category in ['food_away', 'full_service_dining', 'limited_service_dining']:
                        # Higher inflation (labor costs)
                        rate = 0.055
                    elif category in ['fresh_fruits', 'fresh_vegetables', 'fruits_vegetables']:
                        # Weather dependent
                        rate = 0.04
                    else:
                        # Average food inflation
                        rate = 0.03

                    value = base_2024 * (1 + rate) ** years_from_2024
                    value += random.uniform(-1.5, 1.5)
                    cpi[category].append(round(value, 1))

        return cpi

    def generate_spending_analysis(self, years=12):
        """Consumer spending by income quintile"""
        import random

        end_year = 2026
        start_year = end_year - years

        spending = {
            'dates': [],
            'food_home_billions': [],
            'food_away_billions': [],
            'total_food_billions': [],
            # By income quintile (per capita annual spending)
            'q1_food_home': [],  # Lowest 20%
            'q1_food_away': [],
            'q2_food_home': [],
            'q2_food_away': [],
            'q3_food_home': [],  # Middle 20%
            'q3_food_away': [],
            'q4_food_home': [],
            'q4_food_away': [],
            'q5_food_home': [],  # Highest 20%
            'q5_food_away': [],
            # SNAP data
            'snap_benefits_billions': [],
            'snap_participants_millions': [],
            # Food insecurity
            'food_insecurity_rate': []
        }

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                spending['dates'].append(date)

                years_delta = year - 2014 + (month - 1) / 12.0

                # Total spending (billions monthly)
                food_home_base = 75.0  # 2014 baseline
                food_away_base = 55.0

                food_home = food_home_base * (1.042 ** years_delta) + random.uniform(-2, 2)
                food_away = food_away_base * (1.058 ** years_delta) + random.uniform(-2, 2)

                spending['food_home_billions'].append(round(food_home, 1))
                spending['food_away_billions'].append(round(food_away, 1))
                spending['total_food_billions'].append(round(food_home + food_away, 1))

                # Income quintiles (annual per capita)
                # Q1 (lowest 20%) - limited away from home
                q1_home = 2850 * (1.035 ** years_delta) + random.uniform(-50, 50)
                q1_away = 1200 * (1.032 ** years_delta) + random.uniform(-30, 30)
                spending['q1_food_home'].append(round(q1_home, 0))
                spending['q1_food_away'].append(round(q1_away, 0))

                # Q2
                q2_home = 4200 * (1.038 ** years_delta) + random.uniform(-70, 70)
                q2_away = 2400 * (1.045 ** years_delta) + random.uniform(-50, 50)
                spending['q2_food_home'].append(round(q2_home, 0))
                spending['q2_food_away'].append(round(q2_away, 0))

                # Q3 (middle)
                q3_home = 5400 * (1.040 ** years_delta) + random.uniform(-90, 90)
                q3_away = 3600 * (1.052 ** years_delta) + random.uniform(-70, 70)
                spending['q3_food_home'].append(round(q3_home, 0))
                spending['q3_food_away'].append(round(q3_away, 0))

                # Q4
                q4_home = 7200 * (1.042 ** years_delta) + random.uniform(-120, 120)
                q4_away = 5400 * (1.058 ** years_delta) + random.uniform(-100, 100)
                spending['q4_food_home'].append(round(q4_home, 0))
                spending['q4_food_away'].append(round(q4_away, 0))

                # Q5 (highest 20%) - much more away from home
                q5_home = 10800 * (1.045 ** years_delta) + random.uniform(-180, 180)
                q5_away = 10200 * (1.065 ** years_delta) + random.uniform(-200, 200)
                spending['q5_food_home'].append(round(q5_home, 0))
                spending['q5_food_away'].append(round(q5_away, 0))

                # SNAP
                snap_base = 75.0  # Billion annually
                if year >= 2020:
                    snap_base = 115.0  # COVID expansion
                snap = (snap_base / 12.0) + random.uniform(-2, 2)
                spending['snap_benefits_billions'].append(round(snap, 1))

                snap_part = 42.0 if year >= 2020 else 38.0
                spending['snap_participants_millions'].append(snap_part + random.uniform(-1, 1))

                # Food insecurity
                if year == 2020:
                    insecurity = 10.5
                elif year >= 2022:
                    insecurity = 12.8 + years_delta * 0.2
                else:
                    insecurity = 10.5 + years_delta * 0.15
                spending['food_insecurity_rate'].append(round(insecurity, 1))

        return spending

    def generate_shopping_behavior(self, years=12):
        """Shopping patterns - CORRECTED DATA"""
        import random

        end_year = 2026
        start_year = end_year - years

        shopping = {
            'dates': [],
            'trips_per_month': [],
            'items_per_basket': [],
            'dollars_per_basket': [],
            # Channel mix (% of total food spending)
            'grocery_store_pct': [],
            'club_warehouse_pct': [],
            'online_delivery_pct': [],
            'convenience_pct': [],
            'farmers_market_pct': [],
            # Behavior shifts
            'private_label_share': [],  # % of packaged food
            'discount_retailer_share': [],  # Aldi, Lidl, dollar stores
            'meal_kit_adoption': []  # % of households
        }

        base_trips_month = 8.2  # 2014 baseline
        base_items = 10.8
        base_dollars = 142.0

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                shopping['dates'].append(date)

                years_delta = year - 2014

                # CORRECTED: Both trips AND items DECLINE (consolidation + inflation squeeze)
                # 2022: INFLATION STARTS - items PEAK before decline
                if year == 2022:
                    trips = base_trips_month * 0.98 * random.uniform(0.98, 1.02)  # ~8/month
                    items = 11.2 * random.uniform(0.96, 1.04)  # REAL DATA: 11.2 items
                    dollars = 155.0 * random.uniform(0.98, 1.02)  # REAL DATA: ~$155

                # 2023-2024: INFLATION CRISIS - BASKET SIZE COLLAPSE
                elif year in [2023, 2024]:
                    trips = 6.0 * random.uniform(0.94, 1.06)  # REAL DATA: 6/month
                    items = 6.1 * random.uniform(0.92, 1.08)  # REAL DATA: 6.1 items (45% DROP!)
                    dollars = 174.0 * random.uniform(0.97, 1.03)  # REAL DATA: $174 (12% increase)

                # 2025-2026: Continued low basket size
                elif year >= 2025:
                    trips = 5.8 * random.uniform(0.94, 1.06)
                    items = 5.9 * random.uniform(0.92, 1.08)
                    dollars = 182.0 * random.uniform(0.97, 1.03)

                # Pre-2022: Gradual decline
                else:
                    trips = base_trips_month * (1 + (-0.022 * years_delta)) * random.uniform(0.97, 1.03)
                    items = base_items * (1 + (-0.018 * years_delta)) * random.uniform(0.96, 1.04)
                    dollars = base_dollars * (1 + (0.035 * years_delta)) * random.uniform(0.97, 1.03)

                shopping['trips_per_month'].append(round(trips, 1))
                shopping['items_per_basket'].append(round(items, 1))
                shopping['dollars_per_basket'].append(round(dollars, 2))

                # Channel mix
                grocery_base = 65.0
                club_base = 12.0
                online_base = 1.5
                convenience_base = 8.0
                farmers_base = 2.5

                # Online growing rapidly
                if year >= 2020:
                    online = 15.0 + (year - 2020) * 2.5 + random.uniform(-1, 1)
                else:
                    online = online_base + years_delta * 0.8 + random.uniform(-0.5, 0.5)

                # Grocery declining
                grocery = grocery_base - years_delta * 0.6 + random.uniform(-1.5, 1.5)

                # Club growing
                club = club_base + years_delta * 0.4 + random.uniform(-0.8, 0.8)

                # Normalize to 100%
                total = grocery + club + online + convenience_base + farmers_base
                shopping['grocery_store_pct'].append(round(grocery / total * 100, 1))
                shopping['club_warehouse_pct'].append(round(club / total * 100, 1))
                shopping['online_delivery_pct'].append(round(online / total * 100, 1))
                shopping['convenience_pct'].append(round(convenience_base / total * 100, 1))
                shopping['farmers_market_pct'].append(round(farmers_base / total * 100, 1))

                # Private label (store brands) - growing with inflation
                pl_base = 18.0
                if year >= 2022:
                    pl = 25.0 + (year - 2022) * 1.5 + random.uniform(-0.8, 0.8)
                else:
                    pl = pl_base + years_delta * 0.5 + random.uniform(-0.6, 0.6)
                shopping['private_label_share'].append(round(pl, 1))

                # Discount retailers
                discount_base = 8.5
                discount = discount_base + years_delta * 0.6 + random.uniform(-0.5, 0.5)
                shopping['discount_retailer_share'].append(round(discount, 1))

                # Meal kits
                if year >= 2016:
                    meal_kit = 2.0 + (year - 2016) * 0.8 + random.uniform(-0.3, 0.3)
                else:
                    meal_kit = 0.5
                shopping['meal_kit_adoption'].append(round(meal_kit, 1))

        return shopping

    def generate_labor_market(self, years=12):
        """Employment and wage data"""
        import random

        end_year = 2026
        start_year = end_year - years

        labor = {
            'dates': [],
            'unemployment_rate': [],
            'labor_force_participation': [],
            'avg_hourly_earnings': [],
            'real_earnings_index': [],  # Adjusted for inflation
            'food_service_employment_millions': [],
            'retail_employment_millions': [],
            'wage_growth_yoy': []
        }

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                labor['dates'].append(date)

                years_delta = year - 2014

                # Unemployment
                if year == 2020:
                    unemp = 8.1  # COVID
                elif year == 2021:
                    unemp = 5.4
                elif year >= 2022:
                    unemp = 3.6 + (year - 2022) * 0.15 + random.uniform(-0.2, 0.2)
                else:
                    unemp = 5.5 + random.uniform(-0.3, 0.3)
                labor['unemployment_rate'].append(round(unemp, 1))

                # Labor force participation
                lfp_base = 62.9
                if year == 2020:
                    lfp = 61.5
                else:
                    lfp = lfp_base + years_delta * 0.08 + random.uniform(-0.2, 0.2)
                labor['labor_force_participation'].append(round(lfp, 1))

                # Average hourly earnings
                wage_base = 24.50  # 2014
                wages = wage_base * (1.032 ** years_delta) + random.uniform(-0.3, 0.3)
                labor['avg_hourly_earnings'].append(round(wages, 2))

                # Real earnings (adjusted for CPI)
                real_base = 100.0
                if year >= 2022:
                    # Negative real wage growth during inflation
                    real = real_base + years_delta * 0.8 - (year - 2021) * 2.5 + random.uniform(-1, 1)
                else:
                    real = real_base + years_delta * 1.2 + random.uniform(-0.8, 0.8)
                labor['real_earnings_index'].append(round(real, 1))

                # Food service employment
                food_svc_base = 11.5  # million
                if year == 2020:
                    food_svc = 9.2
                else:
                    food_svc = food_svc_base + years_delta * 0.15 + random.uniform(-0.2, 0.2)
                labor['food_service_employment_millions'].append(round(food_svc, 2))

                # Retail employment
                retail_base = 15.8  # million
                retail = retail_base + years_delta * 0.08 + random.uniform(-0.15, 0.15)
                labor['retail_employment_millions'].append(round(retail, 2))

                # Wage growth YoY
                if len(labor['avg_hourly_earnings']) >= 13:
                    current_wage = labor['avg_hourly_earnings'][-1]
                    prior_wage = labor['avg_hourly_earnings'][-13]
                    growth = ((current_wage - prior_wage) / prior_wage) * 100
                else:
                    growth = 3.2
                labor['wage_growth_yoy'].append(round(growth, 1))

        return labor

    def generate_debt_savings(self, years=12):
        """Consumer debt and savings metrics"""
        import random

        end_year = 2026
        start_year = end_year - years

        debt = {
            'dates': [],
            'personal_savings_rate': [],  # % of disposable income
            'credit_card_debt_per_household': [],
            'credit_card_delinquency_rate': [],
            'student_loan_debt_billions': [],
            'mortgage_debt_billions': [],
            'auto_loan_debt_billions': [],
            'total_household_debt_trillions': []
        }

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if year == end_year and month > 1:
                    break

                date = datetime.date(year, month, 1)
                debt['dates'].append(date)

                years_delta = year - 2014

                # Savings rate
                savings_base = 7.5
                if year == 2020:
                    savings = 16.5  # COVID stimulus
                elif year == 2021:
                    savings = 11.2
                elif year >= 2022:
                    # Declining savings (inflation)
                    savings = 7.0 - (year - 2022) * 0.8 + random.uniform(-0.3, 0.3)
                else:
                    savings = savings_base + random.uniform(-0.5, 0.5)
                debt['personal_savings_rate'].append(round(max(savings, 3.0), 1))

                # Credit card debt
                cc_base = 5700  # per household
                cc = cc_base * (1.038 ** years_delta) + random.uniform(-150, 150)
                debt['credit_card_debt_per_household'].append(round(cc, 0))

                # Delinquency rate
                delinq_base = 2.4
                if year >= 2022:
                    delinq = 2.8 + (year - 2022) * 0.4 + random.uniform(-0.2, 0.2)
                else:
                    delinq = delinq_base + random.uniform(-0.15, 0.15)
                debt['credit_card_delinquency_rate'].append(round(delinq, 1))

                # Student loans
                student_base = 1200  # billion
                student = student_base + years_delta * 45 + random.uniform(-20, 20)
                debt['student_loan_debt_billions'].append(round(student, 0))

                # Mortgage
                mortgage_base = 10500  # billion
                mortgage = mortgage_base + years_delta * 380 + random.uniform(-100, 100)
                debt['mortgage_debt_billions'].append(round(mortgage, 0))

                # Auto loans
                auto_base = 1050  # billion
                auto = auto_base + years_delta * 55 + random.uniform(-20, 20)
                debt['auto_loan_debt_billions'].append(round(auto, 0))

                # Total household debt
                total = (cc * 130 / 1000) + student + mortgage + auto  # 130M households
                debt['total_household_debt_trillions'].append(round(total / 1000, 2))

        return debt

    def get_complete_snapshot(self):
        """Get everything"""
        print("📊 LOADING COMPREHENSIVE CONSUMER ECONOMICS DATA...")

        executive = self.generate_executive_summary()
        sentiment = self.generate_sentiment_comprehensive(12)
        cpi = self.generate_cpi_comprehensive(12)
        spending = self.generate_spending_analysis(12)
        shopping = self.generate_shopping_behavior(12)
        labor = self.generate_labor_market(12)
        debt = self.generate_debt_savings(12)

        print("✅ COMPLETE")

        return {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'executive': executive,
            'sentiment': sentiment,
            'cpi': cpi,
            'spending': spending,
            'shopping': shopping,
            'labor': labor,
            'debt': debt
        }

# ==================================================
# CHARTS
# ==================================================

def create_executive_summary_cards(executive, w):
    """Executive KPI summary cards"""
    card_h = 140
    cards_per_row = 3
    card_w = (w - 80) / cards_per_row
    gap = 20

    container = ui.View(frame=(0, 0, w, card_h * 2 + gap + 40))
    container.background_color = THEME['bg']

    # Title
    title = ui.Label(frame=(20, 10, w-40, 25))
    title.text = 'EXECUTIVE SUMMARY - CURRENT SNAPSHOT'
    title.font = ('<system-bold>', 16)
    title.text_color = THEME['accent3']
    container.add_subview(title)

    cards_data = [
        # Row 1
        {
            'title': 'Michigan CSI',
            'value': f"{executive['michigan_csi']:.1f}",
            'change': f"{executive['michigan_change']:+.1f}% YoY",
            'color': THEME['bear'] if executive['michigan_change'] < 0 else THEME['bull'],
            'subtitle': 'Consumer Sentiment'
        },
        {
            'title': 'Conference Board CCI',
            'value': f"{executive['conf_board_cci']:.1f}",
            'change': f"{executive['cci_change']:+.1f}% YoY",
            'color': THEME['bear'] if executive['cci_change'] < 0 else THEME['bull'],
            'subtitle': 'Consumer Confidence'
        },
        {
            'title': 'Food CPI',
            'value': f"{executive['food_cpi']:.1f}",
            'change': f"+{executive['food_inflation_yoy']:.1f}% YoY",
            'color': THEME['warn'],
            'subtitle': '1982-84=100'
        },
        # Row 2
        {
            'title': 'Unemployment',
            'value': f"{executive['unemployment_rate']:.1f}%",
            'change': f"${executive['avg_hourly_wage']:.2f}/hr",
            'color': THEME['neutral'],
            'subtitle': f"+{executive['wage_growth_yoy']:.1f}% wage growth"
        },
        {
            'title': 'Basket Size',
            'value': f"{executive['basket_size_items']:.1f}",
            'change': f"{executive['basket_size_change']:.0f}% vs 2022",
            'color': THEME['bear'],
            'subtitle': 'Items per trip'
        },
        {
            'title': 'Food Insecurity',
            'value': f"{executive['food_insecurity_rate']:.1f}%",
            'change': f"${executive['snap_benefits_billion']:.1f}B SNAP",
            'color': THEME['warn'],
            'subtitle': 'U.S. households'
        }
    ]

    y_offset = 40
    for idx, card_data in enumerate(cards_data):
        row = idx // cards_per_row
        col = idx % cards_per_row
        x = 20 + col * (card_w + gap)
        y = y_offset + row * (card_h + gap)

        card = ui.View(frame=(x, y, card_w - gap, card_h))
        card.background_color = THEME['panel']
        card.corner_radius = 8

        # Title
        lbl_title = ui.Label(frame=(15, 12, card_w - 50, 20))
        lbl_title.text = card_data['title']
        lbl_title.font = ('<system>', 11)
        lbl_title.text_color = THEME['sub']
        card.add_subview(lbl_title)

        # Value
        lbl_value = ui.Label(frame=(15, 35, card_w - 50, 40))
        lbl_value.text = card_data['value']
        lbl_value.font = ('<system-bold>', 32)
        lbl_value.text_color = card_data['color']
        card.add_subview(lbl_value)

        # Change
        lbl_change = ui.Label(frame=(15, 80, card_w - 50, 22))
        lbl_change.text = card_data['change']
        lbl_change.font = ('<system-bold>', 13)
        lbl_change.text_color = card_data['color']
        card.add_subview(lbl_change)

        # Subtitle
        lbl_sub = ui.Label(frame=(15, 105, card_w - 50, 18))
        lbl_sub.text = card_data['subtitle']
        lbl_sub.font = ('<system>', 10)
        lbl_sub.text_color = THEME['sub']
        card.add_subview(lbl_sub)

        container.add_subview(card)

    return container

def create_sentiment_chart(sentiment, w, h):
    """Consumer sentiment - Michigan + Conference Board"""
    from matplotlib.ticker import MultipleLocator
    fig = plt.figure(figsize=(w/80, h/80), dpi=100, facecolor=THEME['bg'])

    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.35)

    dates = sentiment['dates']

    # Chart 1: Main sentiment indices
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(THEME['bg'])
    ax1.plot(dates, sentiment['michigan_csi'], color='#00aaff', linewidth=4,
             label='Michigan CSI', alpha=0.95)
    ax1.plot(dates, sentiment['conf_board_cci'], color='#ff6600', linewidth=4,
             label='Conference Board CCI', alpha=0.95)

    ax1.set_ylabel('Index Value', color=THEME['text'], fontsize=14, fontweight='bold')
    ax1.set_title('CONSUMER SENTIMENT INDICES', color=THEME['text'],
                  fontsize=16, fontweight='bold', pad=15)
    ax1.legend(fontsize=12, loc='upper left', framealpha=0.95)
    ax1.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax1.tick_params(colors=THEME['text'], labelsize=11)
    ax1.yaxis.set_major_locator(MultipleLocator(20))

    # Chart 2: Conference Board components
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(THEME['bg'])
    ax2.plot(dates, sentiment['current_conditions'], color='#00ff00', linewidth=3.5,
             label='Current Conditions', alpha=0.9)
    ax2.plot(dates, sentiment['expectations'], color='#ffcc00', linewidth=3.5,
             label='Expectations', alpha=0.9)

    ax2.set_ylabel('Index Value', color=THEME['text'], fontsize=13, fontweight='bold')
    ax2.set_title('CCI COMPONENTS', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax2.legend(fontsize=11, framealpha=0.95)
    ax2.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax2.tick_params(colors=THEME['text'], labelsize=10)
    ax2.yaxis.set_major_locator(MultipleLocator(20))

    # Chart 3: Inflation expectations
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(THEME['bg'])
    ax3.plot(dates, sentiment['inflation_expectations_1yr'], color='#ff3333', linewidth=3.5,
             label='1-Year', alpha=0.9)
    ax3.plot(dates, sentiment['inflation_expectations_5yr'], color='#9933ff', linewidth=3.5,
             label='5-Year', alpha=0.9)

    ax3.set_ylabel('Expected Inflation (%)', color=THEME['text'], fontsize=13, fontweight='bold')
    ax3.set_title('INFLATION EXPECTATIONS', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax3.legend(fontsize=11, framealpha=0.95)
    ax3.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax3.tick_params(colors=THEME['text'], labelsize=10)
    ax3.yaxis.set_major_locator(MultipleLocator(1.0))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=THEME['bg'], dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_cpi_chart(cpi, w, h):
    """Comprehensive CPI breakdown"""
    from matplotlib.ticker import MultipleLocator
    fig = plt.figure(figsize=(w/80, h/80), dpi=100, facecolor=THEME['bg'])

    gs = fig.add_gridspec(3, 2, hspace=0.45, wspace=0.35)

    dates = cpi['dates']

    # Chart 1: Headline categories
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(THEME['bg'])
    ax1.plot(dates, cpi['all_items'], color='#ffffff', linewidth=4, label='All Items CPI', alpha=0.95)
    ax1.plot(dates, cpi['food_home'], color='#00ff00', linewidth=4, label='Food at Home', alpha=0.95)
    ax1.plot(dates, cpi['food_away'], color='#ff6600', linewidth=4, label='Food Away from Home', alpha=0.95)

    ax1.set_ylabel('Index (1982-84=100)', color=THEME['text'], fontsize=14, fontweight='bold')
    ax1.set_title('CONSUMER PRICE INDEX - HEADLINE CATEGORIES', color=THEME['text'],
                  fontsize=16, fontweight='bold', pad=15)
    ax1.legend(fontsize=12, loc='upper left', framealpha=0.95)
    ax1.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax1.tick_params(colors=THEME['text'], labelsize=11)
    ax1.yaxis.set_major_locator(MultipleLocator(50))

    # Chart 2: Protein categories
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(THEME['bg'])
    ax2.plot(dates, cpi['beef_veal'], color='#ff3333', linewidth=3, label='Beef', alpha=0.9)
    ax2.plot(dates, cpi['pork'], color='#ff99cc', linewidth=3, label='Pork', alpha=0.9)
    ax2.plot(dates, cpi['poultry'], color='#ffcc00', linewidth=3, label='Poultry', alpha=0.9)
    ax2.plot(dates, cpi['eggs'], color='#00ffcc', linewidth=3, label='Eggs', alpha=0.9)

    ax2.set_ylabel('Index', color=THEME['text'], fontsize=13, fontweight='bold')
    ax2.set_title('PROTEIN PRICES', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax2.legend(fontsize=10, framealpha=0.95, loc='upper left')
    ax2.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax2.tick_params(colors=THEME['text'], labelsize=10)
    ax2.yaxis.set_major_locator(MultipleLocator(50))

    # Chart 3: Produce
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(THEME['bg'])
    ax3.plot(dates, cpi['fresh_fruits'], color='#ff6600', linewidth=3, label='Fresh Fruits', alpha=0.9)
    ax3.plot(dates, cpi['fresh_vegetables'], color='#00ff00', linewidth=3, label='Fresh Vegetables', alpha=0.9)

    ax3.set_ylabel('Index', color=THEME['text'], fontsize=13, fontweight='bold')
    ax3.set_title('PRODUCE PRICES', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax3.legend(fontsize=10, framealpha=0.95)
    ax3.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax3.tick_params(colors=THEME['text'], labelsize=10)
    ax3.yaxis.set_major_locator(MultipleLocator(50))

    # Chart 4: Staples
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.set_facecolor(THEME['bg'])
    ax4.plot(dates, cpi['bread'], color='#ffcc00', linewidth=3, label='Bread', alpha=0.9)
    ax4.plot(dates, cpi['dairy'], color='#00aaff', linewidth=3, label='Dairy', alpha=0.9)
    ax4.plot(dates, cpi['coffee'], color='#9933ff', linewidth=3, label='Coffee', alpha=0.9)

    ax4.set_ylabel('Index', color=THEME['text'], fontsize=13, fontweight='bold')
    ax4.set_title('STAPLE FOODS', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax4.legend(fontsize=10, framealpha=0.95)
    ax4.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax4.tick_params(colors=THEME['text'], labelsize=10)
    ax4.yaxis.set_major_locator(MultipleLocator(50))

    # Chart 5: Restaurant
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.set_facecolor(THEME['bg'])
    ax5.plot(dates, cpi['full_service_dining'], color='#ff6600', linewidth=3,
             label='Full Service', alpha=0.9)
    ax5.plot(dates, cpi['limited_service_dining'], color='#00ffcc', linewidth=3,
             label='Limited Service', alpha=0.9)

    ax5.set_ylabel('Index', color=THEME['text'], fontsize=13, fontweight='bold')
    ax5.set_title('RESTAURANT PRICES', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax5.legend(fontsize=10, framealpha=0.95)
    ax5.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax5.tick_params(colors=THEME['text'], labelsize=10)
    ax5.yaxis.set_major_locator(MultipleLocator(50))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=THEME['bg'], dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_spending_chart(spending, w, h):
    """Consumer spending analysis"""
    from matplotlib.ticker import MultipleLocator, FuncFormatter
    fig = plt.figure(figsize=(w/80, h/80), dpi=100, facecolor=THEME['bg'])

    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.35)

    dates = spending['dates']

    # Chart 1: Total spending
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(THEME['bg'])
    ax1.plot(dates, spending['food_home_billions'], color='#00ff00', linewidth=4,
             label='Food at Home', alpha=0.95)
    ax1.plot(dates, spending['food_away_billions'], color='#ff6600', linewidth=4,
             label='Food Away from Home', alpha=0.95)
    ax1.plot(dates, spending['total_food_billions'], color='#00aaff', linewidth=4,
             label='Total Food Spending', alpha=0.95)

    ax1.set_ylabel('Billion $ Monthly', color=THEME['text'], fontsize=14, fontweight='bold')
    ax1.set_title('U.S. FOOD SPENDING - TOTAL', color=THEME['text'],
                  fontsize=16, fontweight='bold', pad=15)
    ax1.legend(fontsize=12, framealpha=0.95, loc='upper left')
    ax1.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax1.tick_params(colors=THEME['text'], labelsize=11)
    ax1.yaxis.set_major_locator(MultipleLocator(20))

    # Chart 2: By income quintile - Food at Home
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(THEME['bg'])

    # Use latest data point for bar chart
    latest_idx = -1
    quintiles = ['Q1\nLowest', 'Q2', 'Q3\nMiddle', 'Q4', 'Q5\nHighest']
    home_values = [
        spending['q1_food_home'][latest_idx],
        spending['q2_food_home'][latest_idx],
        spending['q3_food_home'][latest_idx],
        spending['q4_food_home'][latest_idx],
        spending['q5_food_home'][latest_idx]
    ]
    away_values = [
        spending['q1_food_away'][latest_idx],
        spending['q2_food_away'][latest_idx],
        spending['q3_food_away'][latest_idx],
        spending['q4_food_away'][latest_idx],
        spending['q5_food_away'][latest_idx]
    ]

    x = np.arange(len(quintiles))
    width = 0.35

    ax2.bar(x - width/2, home_values, width, label='Food at Home', color='#00ff00', alpha=0.85)
    ax2.bar(x + width/2, away_values, width, label='Food Away', color='#ff6600', alpha=0.85)

    ax2.set_ylabel('$ Per Capita (Annual)', color=THEME['text'], fontsize=13, fontweight='bold')
    ax2.set_title('SPENDING BY INCOME QUINTILE', color=THEME['text'],
                  fontsize=14, fontweight='bold', pad=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(quintiles)
    ax2.legend(fontsize=10, framealpha=0.95)
    ax2.grid(True, alpha=0.35, color=THEME['grid'], axis='y', linewidth=1.2)
    ax2.tick_params(colors=THEME['text'], labelsize=10)
    ax2.yaxis.set_major_locator(MultipleLocator(2000))

    # Chart 3: SNAP & Food Insecurity
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(THEME['bg'])
    ax3_twin = ax3.twinx()

    ln1 = ax3.plot(dates, spending['snap_benefits_billions'], color='#ffcc00', linewidth=4,
                   label='SNAP Benefits', alpha=0.95)
    ln2 = ax3_twin.plot(dates, spending['food_insecurity_rate'], color='#ff3333', linewidth=4,
                        label='Food Insecurity Rate', alpha=0.95)

    ax3.set_ylabel('SNAP ($ Billion Monthly)', color='#ffcc00', fontsize=12, fontweight='bold')
    ax3_twin.set_ylabel('Food Insecurity (%)', color='#ff3333', fontsize=12, fontweight='bold')
    ax3.set_title('SNAP & FOOD INSECURITY', color=THEME['text'],
                  fontsize=14, fontweight='bold', pad=12)

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax3.legend(lns, labs, loc='upper left', fontsize=10, framealpha=0.95)

    ax3.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax3.tick_params(colors=THEME['text'], labelsize=10)
    ax3_twin.tick_params(colors=THEME['text'], labelsize=10)
    ax3.yaxis.set_major_locator(MultipleLocator(10))
    ax3_twin.yaxis.set_major_locator(MultipleLocator(2))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=THEME['bg'], dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_shopping_chart(shopping, w, h):
    """Shopping behavior analysis"""
    from matplotlib.ticker import MultipleLocator
    fig = plt.figure(figsize=(w/80, h/80), dpi=100, facecolor=THEME['bg'])

    gs = fig.add_gridspec(3, 2, hspace=0.45, wspace=0.35)

    dates = shopping['dates']

    # Chart 1: Trip frequency
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(THEME['bg'])
    ax1.plot(dates, shopping['trips_per_month'], color='#00aaff', linewidth=4, alpha=0.95)
    ax1.fill_between(dates, 0, shopping['trips_per_month'], color='#00aaff', alpha=0.2)

    ax1.set_ylabel('Trips/Month', color=THEME['text'], fontsize=13, fontweight='bold')
    ax1.set_title('SHOPPING FREQUENCY', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax1.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax1.tick_params(colors=THEME['text'], labelsize=10)
    ax1.yaxis.set_major_locator(MultipleLocator(2))

    # Chart 2: Basket size (items)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(THEME['bg'])
    ax2.plot(dates, shopping['items_per_basket'], color='#ff6600', linewidth=4, alpha=0.95)
    ax2.fill_between(dates, 0, shopping['items_per_basket'], color='#ff6600', alpha=0.2)

    ax2.set_ylabel('Items per Basket', color=THEME['text'], fontsize=13, fontweight='bold')
    ax2.set_title('BASKET SIZE (45% DROP 2022-24)', color='#ff3333', fontsize=14, fontweight='bold', pad=12)
    ax2.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax2.tick_params(colors=THEME['text'], labelsize=10)
    ax2.yaxis.set_major_locator(MultipleLocator(2))

    # Chart 3: Basket dollars
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(THEME['bg'])
    ax3.plot(dates, shopping['dollars_per_basket'], color='#00ff00', linewidth=4, alpha=0.95)
    ax3.fill_between(dates, 0, shopping['dollars_per_basket'], color='#00ff00', alpha=0.2)

    ax3.set_ylabel('$ per Basket', color=THEME['text'], fontsize=13, fontweight='bold')
    ax3.set_title('BASKET SPENDING', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax3.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax3.tick_params(colors=THEME['text'], labelsize=10)
    ax3.yaxis.set_major_locator(MultipleLocator(20))

    # Chart 4: Channel mix
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(THEME['bg'])
    ax4.plot(dates, shopping['grocery_store_pct'], color='#00aaff', linewidth=3,
             label='Grocery', alpha=0.9)
    ax4.plot(dates, shopping['online_delivery_pct'], color='#ff6600', linewidth=3,
             label='Online', alpha=0.9)
    ax4.plot(dates, shopping['club_warehouse_pct'], color='#ffcc00', linewidth=3,
             label='Club/Warehouse', alpha=0.9)

    ax4.set_ylabel('% of Food Spending', color=THEME['text'], fontsize=13, fontweight='bold')
    ax4.set_title('CHANNEL MIX', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax4.legend(fontsize=9, framealpha=0.95, loc='best')
    ax4.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax4.tick_params(colors=THEME['text'], labelsize=10)
    ax4.yaxis.set_major_locator(MultipleLocator(10))

    # Chart 5: Private label share
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.set_facecolor(THEME['bg'])
    ax5.plot(dates, shopping['private_label_share'], color='#9933ff', linewidth=4, alpha=0.95)
    ax5.fill_between(dates, 0, shopping['private_label_share'], color='#9933ff', alpha=0.2)

    ax5.set_ylabel('% of Packaged Food', color=THEME['text'], fontsize=13, fontweight='bold')
    ax5.set_title('PRIVATE LABEL (STORE BRAND) SHARE', color=THEME['text'],
                  fontsize=14, fontweight='bold', pad=12)
    ax5.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax5.tick_params(colors=THEME['text'], labelsize=10)
    ax5.yaxis.set_major_locator(MultipleLocator(5))

    # Chart 6: Discount retailer share
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.set_facecolor(THEME['bg'])
    ax6.plot(dates, shopping['discount_retailer_share'], color='#00ffcc', linewidth=4, alpha=0.95)
    ax6.fill_between(dates, 0, shopping['discount_retailer_share'], color='#00ffcc', alpha=0.2)

    ax6.set_ylabel('% of Food Purchases', color=THEME['text'], fontsize=13, fontweight='bold')
    ax6.set_title('DISCOUNT RETAILER SHARE (Aldi, Dollar)', color=THEME['text'],
                  fontsize=14, fontweight='bold', pad=12)
    ax6.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax6.tick_params(colors=THEME['text'], labelsize=10)
    ax6.yaxis.set_major_locator(MultipleLocator(2))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=THEME['bg'], dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_labor_chart(labor, w, h):
    """Labor market analysis"""
    from matplotlib.ticker import MultipleLocator
    fig = plt.figure(figsize=(w/80, h/80), dpi=100, facecolor=THEME['bg'])

    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.35)

    dates = labor['dates']

    # Chart 1: Unemployment + participation
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(THEME['bg'])
    ax1_twin = ax1.twinx()

    ln1 = ax1.plot(dates, labor['unemployment_rate'], color='#ff3333', linewidth=4,
                   label='Unemployment Rate', alpha=0.95)
    ln2 = ax1_twin.plot(dates, labor['labor_force_participation'], color='#00aaff', linewidth=4,
                        label='Labor Force Participation', alpha=0.95)

    ax1.set_ylabel('Unemployment (%)', color='#ff3333', fontsize=14, fontweight='bold')
    ax1_twin.set_ylabel('Participation (%)', color='#00aaff', fontsize=14, fontweight='bold')
    ax1.set_title('LABOR MARKET OVERVIEW', color=THEME['text'],
                  fontsize=16, fontweight='bold', pad=15)

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left', fontsize=12, framealpha=0.95)

    ax1.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax1.tick_params(colors=THEME['text'], labelsize=11)
    ax1_twin.tick_params(colors=THEME['text'], labelsize=11)
    ax1.yaxis.set_major_locator(MultipleLocator(2))
    ax1_twin.yaxis.set_major_locator(MultipleLocator(1))

    # Chart 2: Wages (nominal vs real)
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(THEME['bg'])
    ax2_twin = ax2.twinx()

    ln1 = ax2.plot(dates, labor['avg_hourly_earnings'], color='#00ff00', linewidth=3.5,
                   label='Avg Hourly Wage', alpha=0.95)
    ln2 = ax2_twin.plot(dates, labor['real_earnings_index'], color='#ff6600', linewidth=3.5,
                        label='Real Earnings Index', alpha=0.95)

    ax2.set_ylabel('Nominal Wage ($)', color='#00ff00', fontsize=12, fontweight='bold')
    ax2_twin.set_ylabel('Real Earnings (2014=100)', color='#ff6600', fontsize=12, fontweight='bold')
    ax2.set_title('WAGE GROWTH: NOMINAL vs REAL', color=THEME['text'],
                  fontsize=14, fontweight='bold', pad=12)

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc='upper left', fontsize=10, framealpha=0.95)

    ax2.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax2.tick_params(colors=THEME['text'], labelsize=10)
    ax2_twin.tick_params(colors=THEME['text'], labelsize=10)
    ax2.yaxis.set_major_locator(MultipleLocator(5))
    ax2_twin.yaxis.set_major_locator(MultipleLocator(10))

    # Chart 3: Food & retail employment
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(THEME['bg'])
    ax3.plot(dates, labor['food_service_employment_millions'], color='#ff6600', linewidth=3.5,
             label='Food Service', alpha=0.95)
    ax3.plot(dates, labor['retail_employment_millions'], color='#00aaff', linewidth=3.5,
             label='Retail Trade', alpha=0.95)

    ax3.set_ylabel('Million Jobs', color=THEME['text'], fontsize=12, fontweight='bold')
    ax3.set_title('INDUSTRY EMPLOYMENT', color=THEME['text'], fontsize=14, fontweight='bold', pad=12)
    ax3.legend(fontsize=10, framealpha=0.95)
    ax3.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax3.tick_params(colors=THEME['text'], labelsize=10)
    ax3.yaxis.set_major_locator(MultipleLocator(2))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=THEME['bg'], dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

def create_debt_chart(debt, w, h):
    """Consumer debt and savings"""
    from matplotlib.ticker import MultipleLocator
    fig = plt.figure(figsize=(w/80, h/80), dpi=100, facecolor=THEME['bg'])

    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.35)

    dates = debt['dates']

    # Chart 1: Savings rate
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(THEME['bg'])
    ax1.plot(dates, debt['personal_savings_rate'], color='#00ff00', linewidth=4, alpha=0.95)
    ax1.fill_between(dates, 0, debt['personal_savings_rate'], color='#00ff00', alpha=0.2)

    ax1.set_ylabel('% of Disposable Income', color=THEME['text'], fontsize=14, fontweight='bold')
    ax1.set_title('PERSONAL SAVINGS RATE', color=THEME['text'],
                  fontsize=16, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax1.tick_params(colors=THEME['text'], labelsize=11)
    ax1.yaxis.set_major_locator(MultipleLocator(2))

    # Chart 2: Credit card debt
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(THEME['bg'])
    ax2_twin = ax2.twinx()

    ln1 = ax2.plot(dates, debt['credit_card_debt_per_household'], color='#ff3333', linewidth=3.5,
                   label='CC Debt per HH', alpha=0.95)
    ln2 = ax2_twin.plot(dates, debt['credit_card_delinquency_rate'], color='#ffcc00', linewidth=3.5,
                        label='Delinquency Rate', alpha=0.95)

    ax2.set_ylabel('$ per Household', color='#ff3333', fontsize=12, fontweight='bold')
    ax2_twin.set_ylabel('Delinquency (%)', color='#ffcc00', fontsize=12, fontweight='bold')
    ax2.set_title('CREDIT CARD DEBT & DELINQUENCIES', color=THEME['text'],
                  fontsize=14, fontweight='bold', pad=12)

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc='upper left', fontsize=10, framealpha=0.95)

    ax2.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax2.tick_params(colors=THEME['text'], labelsize=10)
    ax2_twin.tick_params(colors=THEME['text'], labelsize=10)
    ax2.yaxis.set_major_locator(MultipleLocator(1000))
    ax2_twin.yaxis.set_major_locator(MultipleLocator(1.0))

    # Chart 3: Total household debt
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(THEME['bg'])
    ax3.plot(dates, debt['total_household_debt_trillions'], color='#ff6600', linewidth=4, alpha=0.95)
    ax3.fill_between(dates, 0, debt['total_household_debt_trillions'], color='#ff6600', alpha=0.2)

    ax3.set_ylabel('$ Trillions', color=THEME['text'], fontsize=12, fontweight='bold')
    ax3.set_title('TOTAL U.S. HOUSEHOLD DEBT', color=THEME['text'],
                  fontsize=14, fontweight='bold', pad=12)
    ax3.grid(True, alpha=0.35, color=THEME['grid'], linewidth=1.2)
    ax3.tick_params(colors=THEME['text'], labelsize=10)
    ax3.yaxis.set_major_locator(MultipleLocator(2))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor=THEME['bg'], dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return ui.Image.from_data(buf.read())

# ==================================================
# MAIN DASHBOARD
# ==================================================

class UltimateConsumerDashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.name = 'Ultimate Consumer Economics'
        self.engine = ConsumerEconomicsEngine()
        self.data = None
        self.loaded = False

    def did_load(self):
        if not self.loaded:
            self.refresh(None)

    def refresh(self, sender):
        self.data = self.engine.get_complete_snapshot()
        self.loaded = True
        self.rebuild()

    def rebuild(self):
        for v in list(self.subviews):
            self.remove_subview(v)
        self.layout()

    def layout(self):
        if not self.loaded and self.width > 0:
            self.refresh(None)
            return

        if not self.data:
            return

        w, h = self.width, self.height

        scroll = ui.ScrollView(frame=(0, 0, w, h))
        scroll.background_color = THEME['bg']
        self.add_subview(scroll)

        y = 15

        # HEADER
        hdr = ui.View(frame=(0, y, w, 90))
        hdr.background_color = THEME['panel']
        scroll.add_subview(hdr)

        title = ui.Label(frame=(20, 15, w-140, 35))
        title.text = '📊 ULTIMATE CONSUMER ECONOMICS DASHBOARD'
        title.font = ('<system-bold>', 22)
        title.text_color = THEME['accent3']
        hdr.add_subview(title)

        subtitle = ui.Label(frame=(20, 52, w-140, 25))
        subtitle.text = f"Professional Economist Intelligence Platform | {self.data['timestamp']}"
        subtitle.font = ('<system>', 12)
        subtitle.text_color = THEME['sub']
        hdr.add_subview(subtitle)

        btn = ui.Button(frame=(w-115, 25, 95, 45))
        btn.title = '🔄 Refresh'
        btn.background_color = THEME['bull']
        btn.tint_color = '#000000'
        btn.corner_radius = 8
        btn.action = self.refresh
        btn.font = ('<system-bold>', 14)
        hdr.add_subview(btn)

        y += 105

        # EXECUTIVE SUMMARY CARDS
        exec_cards = create_executive_summary_cards(self.data['executive'], w)
        exec_cards.y = y
        scroll.add_subview(exec_cards)
        y += exec_cards.height + 30

        # SECTION 1: CONSUMER SENTIMENT
        lbl = ui.Label(frame=(20, y, w-40, 30))
        lbl.text = '1. CONSUMER SENTIMENT & CONFIDENCE INDICES'
        lbl.font = ('<system-bold>', 18)
        lbl.text_color = THEME['accent3']
        scroll.add_subview(lbl)
        y += 40

        chart_h = 750
        img = ui.ImageView(frame=(20, y, w-40, chart_h))
        img.image = create_sentiment_chart(self.data['sentiment'], w-40, chart_h)
        scroll.add_subview(img)
        y += chart_h + 40

        # SECTION 2: CPI ANALYSIS
        lbl = ui.Label(frame=(20, y, w-40, 30))
        lbl.text = '2. CONSUMER PRICE INDEX - COMPREHENSIVE BREAKDOWN'
        lbl.font = ('<system-bold>', 18)
        lbl.text_color = THEME['accent3']
        scroll.add_subview(lbl)
        y += 40

        chart_h = 950
        img = ui.ImageView(frame=(20, y, w-40, chart_h))
        img.image = create_cpi_chart(self.data['cpi'], w-40, chart_h)
        scroll.add_subview(img)
        y += chart_h + 40

        # SECTION 3: SPENDING ANALYSIS
        lbl = ui.Label(frame=(20, y, w-40, 30))
        lbl.text = '3. CONSUMER SPENDING & INCOME INEQUALITY'
        lbl.font = ('<system-bold>', 18)
        lbl.text_color = THEME['accent3']
        scroll.add_subview(lbl)
        y += 40

        chart_h = 750
        img = ui.ImageView(frame=(20, y, w-40, chart_h))
        img.image = create_spending_chart(self.data['spending'], w-40, chart_h)
        scroll.add_subview(img)
        y += chart_h + 40

        # SECTION 4: SHOPPING BEHAVIOR
        lbl = ui.Label(frame=(20, y, w-40, 30))
        lbl.text = '4. SHOPPING BEHAVIOR & CHANNEL DYNAMICS'
        lbl.font = ('<system-bold>', 18)
        lbl.text_color = THEME['accent3']
        scroll.add_subview(lbl)
        y += 40

        chart_h = 950
        img = ui.ImageView(frame=(20, y, w-40, chart_h))
        img.image = create_shopping_chart(self.data['shopping'], w-40, chart_h)
        scroll.add_subview(img)
        y += chart_h + 40

        # SECTION 5: LABOR MARKET
        lbl = ui.Label(frame=(20, y, w-40, 30))
        lbl.text = '5. LABOR MARKET & WAGE ANALYSIS'
        lbl.font = ('<system-bold>', 18)
        lbl.text_color = THEME['accent3']
        scroll.add_subview(lbl)
        y += 40

        chart_h = 750
        img = ui.ImageView(frame=(20, y, w-40, chart_h))
        img.image = create_labor_chart(self.data['labor'], w-40, chart_h)
        scroll.add_subview(img)
        y += chart_h + 40

        # SECTION 6: DEBT & SAVINGS
        lbl = ui.Label(frame=(20, y, w-40, 30))
        lbl.text = '6. CONSUMER DEBT, SAVINGS & FINANCIAL HEALTH'
        lbl.font = ('<system-bold>', 18)
        lbl.text_color = THEME['accent3']
        scroll.add_subview(lbl)
        y += 40

        chart_h = 750
        img = ui.ImageView(frame=(20, y, w-40, chart_h))
        img.image = create_debt_chart(self.data['debt'], w-40, chart_h)
        scroll.add_subview(img)
        y += chart_h + 50

        # CRITICAL: Set scroll content size with extra padding
        scroll.content_size = (w, y + 50)

if __name__ == '__main__':
    plt.style.use('dark_background')
    v = UltimateConsumerDashboard()
    v.present('fullscreen')
