# ==================================================
# POULTRY DASHBOARD - Enhanced Chicken/Broiler Market Analysis
# ==================================================

import ui
import datetime
from config import THEME, MARGIN
from ui_components import InsightCard, ForecastCard, HeaderLabel

class PoultryMarketAnalyzer:
    """Enhanced poultry market analyzer with comprehensive metrics"""

    def __init__(self, market_data):
        self.market_data = market_data

    def calculate_metrics(self, dates):
        """Calculate comprehensive poultry market metrics"""
        print(f"🐔 ANALYZING POULTRY MARKET: {self.market_data['timestamp']}")

        # Get real data
        corn_price = self.market_data['corn']['current']
        soy_price = self.market_data['soybean']['current']
        diesel_price = self.market_data['diesel']['current']

        # --- MACRO & CONSUMER ---
        beef_composite = 8.10
        pork_composite = 4.80
        chicken_composite = 2.15
        beef_spread = beef_composite / chicken_composite
        pork_spread = pork_composite / chicken_composite

        # Food away from home vs at home
        fafh_idx = 365.0
        fah_idx = 305.0
        dining_premium = ((fafh_idx - fah_idx) / fah_idx) * 100

        # Consumer behavior
        protein_switching = 15.2  # % of consumers trading down from beef
        qsr_traffic = 3.5  # % YoY growth in quick service restaurants

        # --- HATCHABILITY & SURVIVAL (CRITICAL PRODUCTION METRICS) ---
        fertile_egg_sets = 242.5  # Million eggs set weekly
        hatchability_rate = 79.7  # % of fertile eggs that hatch (Normal: 84%)
        hatch_of_fertile = 79.7  # Industry standard metric
        hatch_of_total = 76.2  # Including infertile eggs

        # Fertility & Hatch Issues
        fertility_rate = 95.6  # % of eggs that are fertile
        early_dead = 3.2  # % embryo mortality days 1-7
        mid_dead = 1.8  # % embryo mortality days 8-14
        late_dead = 2.5  # % embryo mortality days 15-21
        pipped_dead = 0.9  # % died after pipping shell
        culled_chicks = 1.2  # % culled at hatch (weak, deformed)

        # Post-Hatch Survival Critical Metrics
        doa_rate = 0.45  # % Dead on Arrival to farm
        first_week_mortality = 2.8  # % mortality days 0-7
        second_week_mortality = 0.9  # % mortality days 8-14
        third_week_mortality = 0.6  # % mortality days 15-21
        fourth_week_mortality = 0.5  # % mortality days 22-28
        week_5_6_mortality = 0.8  # % mortality days 29-42

        # Overall Livability
        total_livability = 96.1  # % of placed chicks reaching harvest
        condemnation_rate = 0.8  # % condemned at processing
        net_livability = total_livability - condemnation_rate  # Saleable birds

        # Economic Impact of Survival
        placed_chicks = 193.2  # Million chicks placed (after hatch loss)
        harvest_ready = placed_chicks * (total_livability / 100)
        mortality_loss_value = (placed_chicks - harvest_ready) * 0.52  # Lost chick cost

        # Breeder Flock Performance
        breeder_flock_size = 62.5  # Million breeder hens
        eggs_per_hen_week = 4.2  # Laying rate
        breeder_age_weeks = 42  # Average flock age (affects fertility)
        pullet_placements = -2.1  # % YoY (future breeders)

        # --- BIOLOGY & SUPPLY ---
        egg_sets = 1.5  # % YoY change
        placements = -0.4  # Chick placements YoY
        avg_bird_weight = 6.52  # lbs live weight
        feed_conversion = 1.82  # lbs feed per lb bird
        days_to_harvest = 42  # Average grow-out time

        # Weekly production
        weekly_slaughter = 168.5  # Million birds
        ready_to_cook_lbs = 1098  # Million lbs/week

        # --- INPUTS & COSTS ---
        soy_meal = soy_price * 0.767  # Convert to meal
        total_feed_cost = 1.85  # $/bird to harvest
        chick_cost = 0.52  # $/chick
        processing_cost = 0.28  # $/lb
        all_in_cost = 1.95  # $/lb total

        # --- GLOBAL RISK & TRADE ---
        hpai_cases = 12  # Active commercial sites
        export_volume_change = -2.5  # % YoY to Mexico/China
        brazil_advantage = "HIGH"  # Competitive threat
        russia_ban = "ACTIVE"  # Trade restriction
        leg_quarter_exports = 755  # Million lbs (annualized)

        # --- LABOR & PROCESSING ---
        processing_capacity = 98.2  # % utilization
        labor_shortage = 8500  # Open positions industry-wide
        automation_investment = 2.4  # Billion $ (2024-2026)

        # --- FOODSERVICE & RETAIL ---
        qsr_wing_demand = "ELEVATED"  # Super Bowl, March Madness
        retail_rotisserie = 12.5  # % of whole bird sales
        meal_kit_demand = 4.8  # % YoY growth

        return {
            'meta': {
                'time': self.market_data['timestamp'],
                'dates': dates
            },

            # A. MACRO ARBITRAGE
            'macro': {
                "BEEF vs. CHICKEN SPREAD": {
                    "val": f"{beef_spread:.2f}x", "unit": "Ratio", "status": "HISTORIC HIGH",
                    "insight": f"Beef at ${beef_composite:.2f} vs Chicken ${chicken_composite:.2f}. Consumers forced to trade down. {protein_switching}% actively switching protein sources."
                },
                "PORK COMPETITION": {
                    "val": f"{pork_spread:.2f}x", "unit": "Ratio", "status": "FAVORABLE",
                    "insight": f"Pork at ${pork_composite:.2f} still double chicken. Pork struggles with African Swine Fever abroad, giving chicken global edge."
                },
                "DINING vs GROCERY PREMIUM": {
                    "val": f"+{dining_premium:.1f}%", "unit": "Premium", "status": "EATING OUT",
                    "insight": "Restaurant inflation drives consumers to cook at home. Retail chicken sales (Breast, Thighs) benefit while QSR margins squeeze."
                },
                "QSR TRAFFIC SURGE": {
                    "val": f"+{qsr_traffic}%", "unit": "YoY", "status": "WINGS/TENDERS",
                    "insight": "Fast food winning share from casual dining. High demand for wings, tenders, nuggets - premium cuts driving pricing power."
                }
            },

            # B. HATCHABILITY & FERTILITY (CRITICAL PRODUCTION FUNNEL)
            'hatchability': {
                "HATCHABILITY CRISIS": {
                    "val": f"{hatchability_rate}%", "unit": "of Fertile", "status": "CRITICAL",
                    "insight": f"Normal = 84%. Currently {hatchability_rate}%. Missing 4-5 chicks per 100 eggs. Causes: breeder age, heat stress, disease pressure, poor egg handling."
                },
                "FERTILITY RATE": {
                    "val": f"{fertility_rate}%", "unit": "Viable Eggs", "status": "ACCEPTABLE",
                    "insight": f"Breeder flock at {breeder_age_weeks} weeks avg age. Fertility drops after week 45. Pullet placements down {pullet_placements}% = aging flock risk."
                },
                "EMBRYO MORTALITY - EARLY": {
                    "val": f"{early_dead}%", "unit": "Days 1-7", "status": "HIGH",
                    "insight": f"Early embryo death at {early_dead}% (normal 1.5%). Signals: poor breeder nutrition, egg storage issues, incubation temperature problems."
                },
                "EMBRYO MORTALITY - MID": {
                    "val": f"{mid_dead}%", "unit": "Days 8-14", "status": "ELEVATED",
                    "insight": "Mid-stage losses suggest genetic issues or incubator contamination. Normal = 1.0%. Needs hatchery biosecurity review."
                },
                "EMBRYO MORTALITY - LATE": {
                    "val": f"{late_dead}%", "unit": "Days 15-21", "status": "WARNING",
                    "insight": "Late-stage death = wasted incubation cost. Often humidity/ventilation issues in final days. Each point = $4M annual loss."
                },
                "PIPPED & CULLED CHICKS": {
                    "val": f"{pipped_dead + culled_chicks}%", "unit": "Hatch Loss", "status": "WASTE",
                    "insight": f"Chicks die after pipping ({pipped_dead}%) or culled as weak/deformed ({culled_chicks}%). Total {pipped_dead + culled_chicks}% revenue destruction."
                },
                "HATCH OF TOTAL EGGS": {
                    "val": f"{hatch_of_total}%", "unit": "All Eggs", "status": "EFFICIENCY",
                    "insight": f"Industry benchmark: 80-82%. At {hatch_of_total}%, we're underperforming. Every point = 2.4M fewer chicks/week."
                }
            },

            # C. SURVIVAL & LIVABILITY (PLACEMENT TO HARVEST)
            'survival': {
                "DEAD ON ARRIVAL (DOA)": {
                    "val": f"{doa_rate}%", "unit": "Transport", "status": "ACCEPTABLE",
                    "insight": f"Chicks dying in transport from hatchery to farm. {doa_rate}% is industry standard. Heat stress in summer can spike to 1.2%."
                },
                "FIRST WEEK MORTALITY": {
                    "val": f"{first_week_mortality}%", "unit": "Days 0-7", "status": "CRITICAL PERIOD",
                    "insight": f"First 7 days = highest risk. {first_week_mortality}% loss (normal 2.0%). Causes: chick quality, brooding temp, water access, disease."
                },
                "SECOND WEEK MORTALITY": {
                    "val": f"{second_week_mortality}%", "unit": "Days 8-14", "status": "STABLE",
                    "insight": "Mortality declining. Chicks past vulnerable period. Respiratory disease and ascites start showing up."
                },
                "WEEKS 3-4 MORTALITY": {
                    "val": f"{third_week_mortality + fourth_week_mortality}%", "unit": "Days 15-28", "status": "NORMAL",
                    "insight": "Birds gaining weight rapidly. Leg issues, sudden death syndrome (SDS) appear. Lighting programs critical."
                },
                "LATE GROW-OUT MORTALITY": {
                    "val": f"{week_5_6_mortality}%", "unit": "Days 29-42", "status": "ELEVATED",
                    "insight": f"Final weeks before harvest. {week_5_6_mortality}% loss from heat stress, leg failure, heart issues. Heavy birds = fragile birds."
                },
                "TOTAL LIVABILITY": {
                    "val": f"{total_livability}%", "unit": "Placement to Harvest", "status": "BENCHMARK",
                    "insight": f"Industry target = 97%. At {total_livability}%, we're losing {100 - total_livability}% of placed chicks. {mortality_loss_value:.1f}M/week in chick cost alone."
                },
                "CONDEMNATION RATE": {
                    "val": f"{condemnation_rate}%", "unit": "at Processing", "status": "QUALITY LOSS",
                    "insight": f"Birds condemned for disease, bruising, contamination. {condemnation_rate}% = birds that survived but can't sell. Pure waste."
                },
                "NET SALEABLE LIVABILITY": {
                    "val": f"{net_livability:.1f}%", "unit": "Effective Yield", "status": "TRUE METRIC",
                    "insight": f"What actually matters: {net_livability:.1f}% of placed chicks become revenue. Industry gold standard = 96.5%. We're underperforming."
                }
            },

            # D. BREEDER FLOCK DYNAMICS
            'breeders': {
                "BREEDER HEN INVENTORY": {
                    "val": f"{breeder_flock_size}M", "unit": "Hens", "status": "TIGHT",
                    "insight": f"Pullet placements down {abs(pullet_placements)}% = flock shrinking. Takes 24 weeks to mature replacement breeders. Supply locked tight."
                },
                "EGG PRODUCTION RATE": {
                    "val": f"{eggs_per_hen_week:.1f}", "unit": "eggs/hen/wk", "status": "DECLINING",
                    "insight": f"Peak production = 5.2 eggs/hen/wk at 30 weeks age. Current flock at {breeder_age_weeks} weeks averaging {eggs_per_hen_week}. Aging flock risk."
                },
                "BREEDER FLOCK AGE": {
                    "val": f"{breeder_age_weeks} weeks", "unit": "Average Age", "status": "MATURE",
                    "insight": "Optimal age: 28-45 weeks. After 50 weeks, fertility/hatchability crash. Flock needs constant replacement - but pullet supply down."
                },
                "EGGS SET WEEKLY": {
                    "val": f"{fertile_egg_sets}M", "unit": "Eggs", "status": "FLAT",
                    "insight": f"Setting {fertile_egg_sets}M eggs/week but only getting {hatch_of_total}% hatch = {fertile_egg_sets * hatch_of_total / 100:.0f}M chicks. Hatch efficiency is the crisis."
                }
            },

            # E. GLOBAL RISK & TRADE FLOW
            'risk': {
                "HPAI THREAT (Broilers)": {
                    "val": "MODERATE", "unit": "Risk", "status": "WATCH",
                    "insight": f"{hpai_cases} sites under quarantine. Risk is spillover from layer farms. Broiler cycle is fast (42 days) so recovery quicker than eggs."
                },
                "EXPORT HEADWINDS": {
                    "val": f"{export_volume_change}%", "unit": "YoY", "status": "CLOGGED",
                    "insight": f"Leg Quarter exports soft. Mexico economic slowdown, China prefers Brazil. {leg_quarter_exports}M lbs seeking alternative markets."
                },
                "BRAZIL COMPETITION": {
                    "val": brazil_advantage, "unit": "Threat", "status": "LOSING SHARE",
                    "insight": "Brazil's currency advantage lets them undercut US by $0.15/lb. They're winning Asia, Middle East. We keep domestic, lose global."
                },
                "RUSSIA BAN IMPACT": {
                    "val": russia_ban, "unit": "Trade", "status": "PERMANENT",
                    "insight": "Russia was a major buyer pre-2014. Market never recovered that volume. Structural oversupply of dark meat remains."
                }
            },

            # F. BIOLOGICAL SUPPLY DYNAMICS
            'bio': {
                "CHICK PLACEMENTS": {
                    "val": f"{placements}%", "unit": "YoY Change", "status": "DECLINING",
                    "insight": f"Placements down {abs(placements)}% despite egg sets up {egg_sets}%. Gap = hatchability crisis eating the funnel."
                },
                "BIRDS TO MARKET": {
                    "val": f"{harvest_ready:.1f}M", "unit": "Weekly", "status": "CONSTRAINED",
                    "insight": f"Placed {placed_chicks}M chicks, lose {100 - total_livability:.1f}% to mortality = only {harvest_ready:.1f}M to harvest. Supply is biology-capped."
                },
                "BIRD WEIGHTS": {
                    "val": f"{avg_bird_weight} lbs", "unit": "Live Wt", "status": "GROWING",
                    "insight": f"Heavier birds = better feed conversion for Breast meat. Cheap corn at {corn_price:.0f} encourages longer {days_to_harvest}-day cycles. Favors Breast over Leg pricing."
                },
                "FEED CONVERSION": {
                    "val": f"{feed_conversion:.2f}", "unit": "FCR", "status": "EFFICIENT",
                    "insight": "Industry-leading efficiency. 1.82 lbs feed → 1 lb chicken. Genetics maxed out. Future gains come from gut health, not breeding."
                },
                "GROW-OUT TIME": {
                    "val": f"{days_to_harvest} days", "unit": "to Harvest", "status": "STANDARD",
                    "insight": f"Average {days_to_harvest} days placement to processing. Heavier birds = longer cycle. Fast food wants smaller birds (35-38 days) for tenders."
                }
            },

            # G. FEED & LOGISTICS
            'inputs': {
                "CORN (Global Index)": {
                    "val": f"{corn_price:.0f}", "unit": "Index", "status": "FAVORABLE",
                    "insight": f"Corn index at {corn_price:.0f}. Cheap energy supports heavier birds, better margins. Represents 50% of feed cost."
                },
                "SOYBEAN MEAL": {
                    "val": f"${soy_meal:.0f}", "unit": "/ton", "status": "ELEVATED",
                    "insight": f"Soy meal protein component at ${soy_meal:.0f}/ton. Elevated but manageable. South America harvest coming - expect relief in Q2."
                },
                "DIESEL FUEL": {
                    "val": f"${diesel_price:.2f}", "unit": "/gal", "status": "FREIGHT DRAG",
                    "insight": f"Diesel adds ~$0.02-0.03/lb in logistics cost (farm → plant → retail). Sticky at ${diesel_price:.2f} due to refinery constraints."
                },
                "ALL-IN COST": {
                    "val": f"${all_in_cost:.2f}", "unit": "/lb", "status": "FLOOR",
                    "insight": f"Total cost to produce = ${all_in_cost:.2f}/lb. Breast must stay above $2.10 or producers lose money. Price floor is structural."
                }
            },

            # H. PROCESSING & LABOR
            'processing': {
                "PLANT CAPACITY": {
                    "val": f"{processing_capacity}%", "unit": "Utilization", "status": "MAXED",
                    "insight": f"Running at {processing_capacity}% capacity. No room to grow without new plants ($250M+ each, 3-year build). Supply ceiling."
                },
                "LABOR SHORTAGE": {
                    "val": f"{labor_shortage:,}", "unit": "Open Jobs", "status": "CRISIS",
                    "insight": "Processing plants need bodies. Automation coming but 5+ years away. Meanwhile, overtime costs eating margins."
                },
                "AUTOMATION WAVE": {
                    "val": f"${automation_investment}B", "unit": "Investment", "status": "TRANSFORMING",
                    "insight": "Robotics for de-boning, cut-up, packaging. Will reduce labor dependency but takes time. Favors large integrators (Tyson, Pilgrim's)."
                }
            },

            # I. COLD STORAGE
            'storage': {
                "BREAST MEAT": {
                    "val": "180M", "unit": "lbs", "status": "CRITICAL LOW",
                    "insight": "Inventories 35% below 5-year average. Retail restocking demand strong. Upward price pressure through Q1."
                },
                "LEG QUARTERS": {
                    "val": "95M", "unit": "lbs", "status": "HEAVY",
                    "insight": "Exports soft = domestic buildup. Dark meat backing up in freezers. Price pressure on Legs while Breast soars - historic spread."
                },
                "WINGS": {
                    "val": "72M", "unit": "lbs", "status": "DRAWDOWN",
                    "insight": "Pre-Super Bowl inventory pull active. Wings are seasonal - spike Jan-Feb (NFL), then crash March-July."
                },
                "WHOLE BIRDS": {
                    "val": "125M", "unit": "lbs", "status": "STABLE",
                    "insight": "Rotisserie programs (Costco, Kroger) provide steady demand floor. Whole bird is margin manager - balances cut-up economics."
                }
            },

            # J. PRICE FORECASTS
            'cuts': {
                "WHOLE BIRD (WOG)": {
                    "current": 1.28, "target": 1.38, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.15, 1.18, 1.20, 1.24, 1.26, 1.28],
                    "fut": [1.32, 1.35, 1.38],
                    "logic": f"Limited slaughter due to tight placements. Rotisserie demand stable. Target ${1.38:.2f} by {dates['d90']}."
                },
                "BONELESS/SKINLESS BREAST": {
                    "current": 1.58, "target": 1.78, "trend": "STRONG BUY",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.30, 1.35, 1.42, 1.48, 1.52, 1.58],
                    "fut": [1.64, 1.71, 1.78],
                    "logic": f"Storage crisis + retail restocking = price explosion. ${1.71:.2f} by {dates['d60']}, ${1.78:.2f} by {dates['d90']}. BUY."
                },
                "BONELESS/SKINLESS THIGHS": {
                    "current": 1.45, "target": 1.62, "trend": "STRUCTURAL BULL",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.10, 1.20, 1.28, 1.35, 1.40, 1.45],
                    "fut": [1.51, 1.57, 1.62],
                    "logic": "Labor shortage limits de-boning capacity. QSRs pay premium for boneless dark meat (higher yield). Secular trend continues."
                },
                "JUMBO WINGS": {
                    "current": 1.68, "target": 2.25, "trend": "SPIKE THEN CRASH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.45, 1.48, 1.50, 1.55, 1.62, 1.68],
                    "fut": [2.05, 2.25, 1.85],
                    "logic": f"Super Bowl peak = ${2.25:.2f} by {dates['d60']}, then crash to ${1.85:.2f}. Seasonal play only."
                },
                "LEG QUARTERS": {
                    "current": 0.42, "target": 0.45, "trend": "NEUTRAL",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [0.38, 0.39, 0.40, 0.41, 0.41, 0.42],
                    "fut": [0.43, 0.44, 0.45],
                    "logic": "Export-dependent. Brazil competition caps upside. Domestic demand weak. Stuck in range until trade improves."
                },
                "MECHANICALLY SEPARATED": {
                    "current": 0.28, "target": 0.30, "trend": "STABLE",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [0.25, 0.26, 0.27, 0.27, 0.28, 0.28],
                    "fut": [0.29, 0.29, 0.30],
                    "logic": "Processed food (hot dogs, nuggets) demand absorbs supply. Inflation-resistant. Slow grind higher."
                },
                "PAWS/FEET (Export)": {
                    "current": 0.95, "target": 0.82, "trend": "BEARISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.10, 1.05, 1.00, 0.98, 0.96, 0.95],
                    "fut": [0.90, 0.86, 0.82],
                    "logic": "China licensing issues persist. Volume to Hong Kong declining. Oversupply drives fade to ${0.82:.2f}."
                },
                "TENDERS (Premium)": {
                    "current": 2.15, "target": 2.35, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [1.85, 1.92, 2.00, 2.05, 2.10, 2.15],
                    "fut": [2.22, 2.28, 2.35],
                    "logic": "QSR gold standard. Labor to hand-cut limits supply. Premium to breast widens. Target ${2.35:.2f}."
                }
            }
        }


class PoultryDashboard(ui.View):
    """Enhanced Poultry Market Dashboard"""

    def __init__(self, data_engine):
        super().__init__()
        self.data_engine = data_engine
        self.background_color = THEME['bg']
        self.data = None

        self.scroll = ui.ScrollView(flex='WH')
        self.add_subview(self.scroll)

        self.loading = ui.ActivityIndicator(style=ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE)
        self.loading.flex = 'WH'
        self.loading.start()
        self.add_subview(self.loading)

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
        for sub in self.scroll.subviews:
            sub.remove_from_superview()

        import threading
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        """Background data loading"""
        market_data = self.data_engine.get_market_snapshot()
        dates = self.data_engine.calculate_forecast_dates()
        analyzer = PoultryMarketAnalyzer(market_data)
        self.data = analyzer.calculate_metrics(dates)
        ui.delay(self.draw_ui, 0)

    def draw_ui(self):
        """Render dashboard UI"""
        self.loading.stop()
        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        # HEADER
        self._add_label("🐔 POULTRY MARKET COMMAND", 28, THEME['gold'], y, cw, bold=True)
        y += 35
        ts = self.data['meta']['time']
        self._add_label(f"BROILER PRODUCTION + SURVIVAL + TRADE + PROCESSING | {ts}", 12, THEME['sub'], y, cw)
        y += 40

        # 1. MACRO ARBITRAGE
        y = HeaderLabel.create(self.scroll, "1. MACRO ARBITRAGE & PROTEIN COMPETITION", THEME['macro'], y, cw)
        for k, v in self.data['macro'].items():
            card, h = InsightCard.create(k, v, THEME['macro'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 2. HATCHABILITY & FERTILITY (CRITICAL)
        y = HeaderLabel.create(self.scroll, "2. HATCHABILITY & FERTILITY CRISIS", THEME['risk'], y, cw)
        for k, v in self.data['hatchability'].items():
            card, h = InsightCard.create(k, v, THEME['risk'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 3. SURVIVAL & LIVABILITY (CRITICAL)
        y = HeaderLabel.create(self.scroll, "3. SURVIVAL & LIVABILITY METRICS", THEME['bio'], y, cw)
        for k, v in self.data['survival'].items():
            card, h = InsightCard.create(k, v, THEME['bio'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 4. BREEDER FLOCK DYNAMICS
        y = HeaderLabel.create(self.scroll, "4. BREEDER FLOCK DYNAMICS", THEME['layer'], y, cw)
        for k, v in self.data['breeders'].items():
            card, h = InsightCard.create(k, v, THEME['layer'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 5. RISK & TRADE
        y = HeaderLabel.create(self.scroll, "5. GLOBAL RISK & TRADE FLOW", THEME['trade'], y, cw)
        for k, v in self.data['risk'].items():
            col = THEME['risk'] if "THREAT" in k or "HPAI" in k else THEME['trade']
            card, h = InsightCard.create(k, v, col, cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 6. BIOLOGY & SUPPLY
        y = HeaderLabel.create(self.scroll, "6. BIOLOGICAL SUPPLY DYNAMICS", THEME['warn'], y, cw)
        for k, v in self.data['bio'].items():
            card, h = InsightCard.create(k, v, THEME['warn'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 7. INPUTS
        y = HeaderLabel.create(self.scroll, "7. FEED & LOGISTICS COSTS", THEME['logistics'], y, cw)
        for k, v in self.data['inputs'].items():
            card, h = InsightCard.create(k, v, THEME['logistics'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 8. PROCESSING & LABOR
        y = HeaderLabel.create(self.scroll, "8. PROCESSING & LABOR DYNAMICS", THEME['accent'], y, cw)
        for k, v in self.data['processing'].items():
            card, h = InsightCard.create(k, v, THEME['accent'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 9. STORAGE
        y = HeaderLabel.create(self.scroll, "9. COLD STORAGE INVENTORY", THEME['cold'], y, cw)
        for k, v in self.data['storage'].items():
            col = THEME['cold']
            if "CRITICAL" in v['status'] or "LOW" in v['status']:
                col = THEME['bull']
            elif "HEAVY" in v['status']:
                col = THEME['bear']
            card, h = InsightCard.create(k, v, col, cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 10. PRICE MATRIX
        y = HeaderLabel.create(self.scroll, "10. PRICE MATRIX & 90-DAY FORECASTS", THEME['bull'], y, cw)
        for k, v in self.data['cuts'].items():
            card, h = ForecastCard.create(k, v, cw, y, self.data['meta']['dates'])
            self.scroll.add_subview(card)
            y += h + 15

        # 11. VERDICT
        y = self._draw_verdict(y, cw)

        self.scroll.content_size = (w, y + 100)

    def _draw_verdict(self, y, w):
        """Draw analyst verdict section"""
        y = HeaderLabel.create(self.scroll, "11. ANALYST VERDICT", THEME['warn'], y, w)
        h = 500
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8

        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 14)
        tv.editable = False
        tv.text = (
            "THE POULTRY VERDICT: 'SURVIVAL CRISIS MEETS STRUCTURAL TIGHTNESS'\n\n"
            "1. THE HATCHABILITY CATASTROPHE:\n"
            "Hatchability at 79.7% vs normal 84% is a 4-5 point disaster. We're setting 242M eggs/week "
            "but only hatching 76% = losing 58 MILLION potential chicks weekly. This is not weather - "
            "it's breeder flock age (42 weeks), disease pressure, and heat stress. With pullet placements "
            "down 2.1%, the breeder flock keeps aging. No quick fix - locked in through mid-2027.\n\n"
            "2. THE SURVIVAL FUNNEL:\n"
            "First week mortality at 2.8% (normal 2.0%) + late grow-out losses = only 96.1% livability. "
            "Add 0.8% condemnations = 95.3% net saleable birds. We're losing 4.7% of placed chicks "
            "AFTER paying for feed, housing, labor. At 193M placements/week × $0.52/chick, that's $4.7M "
            "weekly in direct chick cost waste alone. Scale in feed waste = $15M+ weekly industry-wide.\n\n"
            "3. THE BIOLOGY BOTTLENECK:\n"
            "Egg sets up 1.5% but placements down 0.4% = the hatch crisis eating the entire funnel. "
            "Even if we wanted to expand, we can't - breeder flock is shrinking and takes 24 weeks to "
            "replace. Processing at 98% capacity. Labor crisis with 8,500 open jobs. Biology + infrastructure "
            "= hard supply ceiling through 2027.\n\n"
            "4. THE BREAST vs LEG CHASM:\n"
            "Historic spread forming. Breast demand (domestic retail + QSR) is on fire. Low storage, "
            "tight supply → $1.78+ target. Meanwhile Leg Quarters rot in freezers because exports are "
            "dead (Brazil wins on price, Mexico weak, China licensing mess). Dark meat is the industry's albatross.\n\n"
            "5. ACTION PLAN:\n"
            "• STRONG BUY: Breast, Tenders (retail + QSR demand unstoppable)\n"
            "• BUY: Boneless Thighs (labor shortage = de-boning premium)\n"
            "• SHORT-TERM TRADE: Wings (spike to $2.25 Super Bowl, then dump)\n"
            "• AVOID: Leg Quarters (export trap), Paws (China issues)\n"
            "• WATCH: Hatchability reports weekly - any improvement = supply relief signal\n\n"
            "BOTTOM LINE: The hatchability + livability crisis is THE story. We can't produce enough birds "
            "to meet domestic demand, let alone exports. Play the domestic white meat cuts (Breast/Thighs/"
            "Tenders). Ignore export-dependent dark meat. Supply stays tight through 2027 minimum."
        )
        card.add_subview(tv)
        self.scroll.add_subview(card)
        return y + h + 20

    def _add_label(self, text, size, color, y, w, bold=False):
        """Add centered label"""
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)
