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

        # --- BIOLOGY & SUPPLY ---
        egg_sets = 1.5  # % YoY change
        placements = -0.4  # Chick placements YoY
        hatchability = 79.7  # % (Normal: 84%)
        livability = 96.1  # % birds surviving to harvest
        pullet_placements = -2.1  # % YoY (future breeders)
        avg_bird_weight = 6.52  # lbs live weight
        feed_conversion = 1.82  # lbs feed per lb bird

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

            # B. GLOBAL RISK & TRADE FLOW
            'risk': {
                "HPAI THREAT (Broilers)": {
                    "val": "MODERATE", "unit": "Risk", "status": "WATCH",
                    "insight": f"{hpai_cases} sites under quarantine. Risk is spillover from layer farms. Broiler cycle is fast (6 weeks) so recovery quicker than eggs."
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

            # C. BIOLOGICAL FUNNEL
            'bio': {
                "HATCHABILITY CRISIS": {
                    "val": f"{hatchability}%", "unit": "Rate", "status": "CRITICAL",
                    "insight": f"Normal = 84%. Currently {hatchability}%. Missing 4-5 chicks per 100 eggs. Causes: breeder age, heat stress, disease. No quick fix."
                },
                "PLACEMENTS vs SETS GAP": {
                    "val": f"{egg_sets - placements:.1f}%", "unit": "Inefficiency", "status": "INFLATIONARY",
                    "insight": f"Sets up {egg_sets}% but placements only {placements}%. Wasting money incubating eggs that don't hatch. Margin headwind."
                },
                "PULLET PLACEMENTS": {
                    "val": f"{pullet_placements}%", "unit": "YoY", "status": "FUTURE SHORT",
                    "insight": "Breeder flock shrinking. Takes 24 weeks to mature. Supply tightness locked in through Q2 2027 minimum."
                },
                "BIRD WEIGHTS": {
                    "val": f"{avg_bird_weight} lbs", "unit": "Live Wt", "status": "GROWING",
                    "insight": "Heavier birds = better feed conversion for Breast meat. Cheap corn encourages longer grow cycles. Favors Breast over Leg pricing."
                },
                "FEED CONVERSION": {
                    "val": f"{feed_conversion:.2f}", "unit": "FCR", "status": "EFFICIENT",
                    "insight": "Industry-leading efficiency. 1.82 lbs feed → 1 lb chicken. Genetics maxed out. Future gains come from gut health, not breeding."
                }
            },

            # D. FEED & LOGISTICS
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

            # E. PROCESSING & LABOR
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

            # F. COLD STORAGE
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

            # G. PRICE FORECASTS
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
        self._add_label(f"BROILER + TRADE + RISK + PROCESSING INTELLIGENCE | {ts}", 12, THEME['sub'], y, cw)
        y += 40

        # 1. MACRO ARBITRAGE
        y = HeaderLabel.create(self.scroll, "1. MACRO ARBITRAGE & PROTEIN COMPETITION", THEME['macro'], y, cw)
        for k, v in self.data['macro'].items():
            card, h = InsightCard.create(k, v, THEME['macro'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 2. RISK & TRADE
        y = HeaderLabel.create(self.scroll, "2. GLOBAL RISK & TRADE FLOW", THEME['risk'], y, cw)
        for k, v in self.data['risk'].items():
            col = THEME['risk'] if "THREAT" in k or "HPAI" in k else THEME['trade']
            card, h = InsightCard.create(k, v, col, cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 3. BIOLOGY
        y = HeaderLabel.create(self.scroll, "3. BIOLOGICAL FUNNEL & SUPPLY DYNAMICS", THEME['bio'], y, cw)
        for k, v in self.data['bio'].items():
            card, h = InsightCard.create(k, v, THEME['bio'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 4. INPUTS
        y = HeaderLabel.create(self.scroll, "4. FEED & LOGISTICS COSTS", THEME['logistics'], y, cw)
        for k, v in self.data['inputs'].items():
            card, h = InsightCard.create(k, v, THEME['logistics'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 5. PROCESSING & LABOR
        y = HeaderLabel.create(self.scroll, "5. PROCESSING & LABOR DYNAMICS", THEME['warn'], y, cw)
        for k, v in self.data['processing'].items():
            card, h = InsightCard.create(k, v, THEME['warn'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 6. STORAGE
        y = HeaderLabel.create(self.scroll, "6. COLD STORAGE INVENTORY", THEME['cold'], y, cw)
        for k, v in self.data['storage'].items():
            col = THEME['cold']
            if "CRITICAL" in v['status'] or "LOW" in v['status']:
                col = THEME['bull']
            elif "HEAVY" in v['status']:
                col = THEME['bear']
            card, h = InsightCard.create(k, v, col, cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 7. PRICE MATRIX
        y = HeaderLabel.create(self.scroll, "7. PRICE MATRIX & 90-DAY FORECASTS", THEME['bull'], y, cw)
        for k, v in self.data['cuts'].items():
            card, h = ForecastCard.create(k, v, cw, y, self.data['meta']['dates'])
            self.scroll.add_subview(card)
            y += h + 15

        # 8. VERDICT
        y = self._draw_verdict(y, cw)

        self.scroll.content_size = (w, y + 100)

    def _draw_verdict(self, y, w):
        """Draw analyst verdict section"""
        y = HeaderLabel.create(self.scroll, "8. ANALYST VERDICT", THEME['warn'], y, w)
        h = 420
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8

        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 14)
        tv.editable = False
        tv.text = (
            "THE POULTRY VERDICT: 'STRUCTURAL TIGHTNESS MEETS EXPORT HEADWINDS'\n\n"
            "1. THE BIOLOGY BOTTLENECK:\n"
            "Hatchability at 79.7% vs normal 84% is a crisis. You can't hatch what you don't have. "
            "Pullet placements down 2.1% locks in supply shortage through mid-2027. No quick fix.\n\n"
            "2. THE BREAST vs LEG CHASM:\n"
            "Historic spread forming. Breast demand (domestic retail + QSR) is on fire. Low storage, "
            "tight supply → $1.78+ target. Meanwhile Leg Quarters rot in freezers because exports "
            "are dead (Brazil wins on price, Mexico weak, China licensing mess). Dark meat is the "
            "industry's albatross.\n\n"
            "3. THE EXPORT TRAP:\n"
            "We produce for global markets but Brazil has currency + biosecurity advantage. They're "
            "taking Asia, Middle East. We're stuck with domestic consumption + hoping Mexico recovers. "
            "Leg Quarter oversupply = margin drag for integrators.\n\n"
            "4. LABOR & CAPACITY:\n"
            "Plants maxed at 98% capacity. 8,500 open jobs. Automation is coming but years away. "
            "This caps production growth even if biology recovered tomorrow.\n\n"
            "5. ACTION PLAN:\n"
            "• STRONG BUY: Breast, Tenders (retail + QSR demand unstoppable)\n"
            "• BUY: Boneless Thighs (labor shortage = de-boning premium)\n"
            "• SHORT-TERM TRADE: Wings (spike to $2.25 Super Bowl, then dump)\n"
            "• AVOID: Leg Quarters (export trap), Paws (China issues)\n\n"
            "BOTTOM LINE: Play the domestic cuts (Breast/Thighs/Tenders). Ignore export-dependent "
            "products until trade dynamics shift. The spread between white and dark meat is the trade."
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
