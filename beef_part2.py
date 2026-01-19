# ==================================================
# BEEF & DAIRY MARKET INTELLIGENCE PLATFORM
# PART 2: Market Analyzers (Comprehensive)
# ==================================================

from beef_part1 import *

class BeefMarketAnalyzer:
    """Comprehensive beef & cattle market analyzer"""

    def __init__(self, market_data):
        self.market_data = market_data

    def calculate_metrics(self, dates):
        print(f"🥩 ANALYZING BEEF MARKET: {self.market_data['timestamp']}")

        # Get real market data
        beef_retail = self.market_data['beef_retail']['current']
        ground_beef = self.market_data['ground_beef']['current']
        feeder_cattle = self.market_data['feeder_cattle']['current']
        live_cattle = self.market_data['live_cattle']['current']
        corn_price = self.market_data['corn']['current']
        hay_price = self.market_data['hay']['current']
        diesel_price = self.market_data['diesel']['current']

        # CATTLE INVENTORY & SUPPLY
        total_cattle = 94.8  # Million head (US total inventory)
        beef_cows = 30.4  # Million beef cows
        dairy_cows = 9.4  # Million dairy cows
        cattle_on_feed = 14.2  # Million in feedlots
        calf_crop = 35.8  # Million calves born annually

        # Placements & Marketings (monthly rates)
        feedlot_placements = 1.85  # Million/month
        feedlot_marketings = 1.92  # Million/month
        placement_weight = 825  # lbs avg
        marketing_weight = 1350  # lbs avg

        # HERD DYNAMICS
        herd_expansion = -1.8  # % YoY (liquidation phase)
        heifer_retention = 38.2  # % kept for breeding (low = liquidation)
        cow_slaughter = 3.1  # Million annually (high = herd liquidation)

        # FEED COSTS & MARGINS
        corn_bushels_per_head = 52  # Bushels to finish a steer
        hay_tons_per_head = 2.8  # Tons hay per year
        total_feed_cost = 950  # $ per head (finish)
        cost_of_gain = 1.45  # $/lb of gain

        # Calculate break-even
        breakeven_price = (feeder_cattle * (placement_weight/100) + total_feed_cost) / (marketing_weight/100)

        # PACKER MARGINS & PROCESSING
        packer_margin = 285  # $/head (gross packer margin)
        packer_capacity = 128500  # Head/day (total US)
        capacity_utilization = 96.5  # % (tight)
        processing_cost = 375  # $/head
        four_firm_concentration = 85  # % (oligopoly)

        # BEEF PRODUCTION
        weekly_slaughter = 650000  # Head/week
        carcass_weight = 850  # lbs avg
        weekly_production = 275  # Million lbs/week
        cutout_value = 315  # $/cwt (composite cutout)

        # EXPORT/IMPORT (Critical for beef!)
        export_volume = 3280  # Million lbs/year
        export_pct = 13.5  # % of production
        japan_exports = 875  # Million lbs (top destination)
        korea_exports = 685  # Million lbs
        mexico_exports = 420  # Million lbs
        china_exports = 285  # Million lbs (volatile)

        import_volume = 3450  # Million lbs/year (US imports more than exports!)
        australia_imports = 1420  # Million lbs
        nz_imports = 625  # Million lbs
        import_pct = 14.2  # % of consumption

        # COLD STORAGE
        beef_cold_storage = 485  # Million lbs
        storage_pct_change = -12.5  # % YoY (drawdown)
        months_supply = 0.95  # Months (tight!)

        # GRASS/DROUGHT CONDITIONS
        drought_severity = 2.8  # Index (0-5, higher = worse)
        pasture_condition = 42  # % good/excellent (poor = 58%)
        hay_shortage = "MODERATE"  # Condition

        # RETAIL DEMAND
        per_capita_consumption = 58.4  # lbs/year
        restaurant_beef_index = 142.5  # Index
        retail_feature_rate = 28.5  # % of beef on sale

        return {
            'meta': {'time': self.market_data['timestamp'], 'dates': dates},

            # 1. MACRO & PROTEIN COMPETITION
            'macro': {
                "BEEF RETAIL COMPOSITE": {
                    "val": f"${beef_retail:.2f}", "unit": "/lb", "status": "PREMIUM",
                    "insight": f"Beef at ${beef_retail:.2f}/lb vs chicken $2.15, pork $4.80. Price premium = reduced demand, consumers trading down."
                },
                "GROUND BEEF (80/20)": {
                    "val": f"${ground_beef:.2f}", "unit": "/lb", "status": "VALUE ENTRY",
                    "insight": f"Ground beef ${ground_beef:.2f} is gateway drug. When middle meats hurt wallet, consumers shift to ground."
                },
                "PER CAPITA CONSUMPTION": {
                    "val": f"{per_capita_consumption} lbs", "unit": "/year", "status": "FLAT",
                    "insight": "Consumption plateaued. High prices killing demand growth. Plant-based taking 2-3% share."
                },
                "RESTAURANT DEMAND": {
                    "val": f"{restaurant_beef_index:.0f}", "unit": "Index", "status": "STRONG",
                    "insight": "QSRs driving demand for ground beef, brisket (smoked), chuck (burgers). Premium steakhouses struggling."
                }
            },

            # 2. CATTLE SUPPLY & HERD LIQUIDATION
            'supply': {
                "US CATTLE INVENTORY": {
                    "val": f"{total_cattle}M", "unit": "Head", "status": "LIQUIDATION",
                    "insight": f"Total inventory {total_cattle}M head. Down {abs(herd_expansion)}% YoY. In liquidation phase = short-term supply up, long-term DOWN."
                },
                "HEIFER RETENTION": {
                    "val": f"{heifer_retention}%", "unit": "Rate", "status": "CRISIS",
                    "insight": f"Only {heifer_retention}% heifers kept for breeding. Should be 45%+. Ranchers selling breeding stock = future supply collapse."
                },
                "COW SLAUGHTER RATE": {
                    "val": f"{cow_slaughter}M", "unit": "/year", "status": "RECORD HIGH",
                    "insight": f"{cow_slaughter}M cows slaughtered (should be 2.5M). Herd liquidation accelerating. Rebuilding takes 3-5 years minimum."
                },
                "CALF CROP": {
                    "val": f"{calf_crop}M", "unit": "Calves", "status": "DECLINING",
                    "insight": "Fewer cows = fewer calves. Calf prices skyrocketing. Feeder cattle will be scarce 2025-2027."
                }
            },

            # 3. FEEDLOT ECONOMICS
            'feedlot': {
                "CATTLE ON FEED": {
                    "val": f"{cattle_on_feed}M", "unit": "Head", "status": "STEADY",
                    "insight": f"{cattle_on_feed}M head in feedlots. Placements ({feedlot_placements}M/mo) < Marketings ({feedlot_marketings}M/mo) = inventory draw."
                },
                "COST OF GAIN": {
                    "val": f"${cost_of_gain:.2f}", "unit": "/lb", "status": "ELEVATED",
                    "insight": f"Corn at {corn_price:.0f} = ${cost_of_gain:.2f}/lb to add weight. Feedlots losing money when live cattle < ${breakeven_price:.0f}/cwt."
                },
                "BREAKEVEN PRICE": {
                    "val": f"${breakeven_price:.0f}", "unit": "/cwt", "status": "SQUEEZED",
                    "insight": f"Break-even ${breakeven_price:.0f}/cwt. Live cattle at {live_cattle:.0f}. Margins thin. Feedlots reducing placements."
                },
                "FEEDER CATTLE": {
                    "val": f"{feeder_cattle:.0f}", "unit": "Index", "status": "STRONG",
                    "insight": f"Feeder cattle {feeder_cattle:.0f}. Tight calf supply = high feeder prices. Ranchers have pricing power for first time in years."
                }
            },

            # 4. FEED COSTS & DROUGHT
            'feed_drought': {
                "CORN (Feed)": {
                    "val": f"{corn_price:.0f}", "unit": "Index", "status": "MODERATE",
                    "insight": f"Corn {corn_price:.0f}. Takes {corn_bushels_per_head} bushels to finish steer. Feed cost = 60% of finishing expense."
                },
                "HAY PRICES": {
                    "val": f"{hay_price:.0f}", "unit": "Index", "status": "ELEVATED",
                    "insight": f"Hay {hay_price:.0f}. Drought = hay shortage. Cow-calf ops need {hay_tons_per_head} tons/head/year. Forcing herd liquidation."
                },
                "DROUGHT SEVERITY": {
                    "val": f"{drought_severity:.1f}/5", "unit": "Index", "status": "STRESS",
                    "insight": f"Drought index {drought_severity}/5. Pasture only {pasture_condition}% good. Ranchers can't feed herds = forced selling."
                },
                "PASTURE CONDITIONS": {
                    "val": f"{pasture_condition}%", "unit": "Good/Exc", "status": "POOR",
                    "insight": f"Only {pasture_condition}% pastures rated good. Grass-fed ops crushed. Hay prices spiking forces feedlot placement earlier."
                }
            },

            # 5. PACKER POWER & PROCESSING
            'packer': {
                "PACKER MARGIN": {
                    "val": f"${packer_margin}", "unit": "/head", "status": "ELEVATED",
                    "insight": f"Gross margin ${packer_margin}/head. Big 4 packers (Tyson, JBS, Cargill, National) = {four_firm_concentration}% market. Oligopoly pricing."
                },
                "CAPACITY UTILIZATION": {
                    "val": f"{capacity_utilization}%", "unit": "Rate", "status": "MAXED",
                    "insight": f"Plants at {capacity_utilization}%. No room to grow. This caps slaughter even when cattle available. Structural bottleneck."
                },
                "FOUR-FIRM CONCENTRATION": {
                    "val": f"{four_firm_concentration}%", "unit": "Market Share", "status": "OLIGOPOLY",
                    "insight": f"Top 4 packers = {four_firm_concentration}% of slaughter. Price-setting power. Ranchers are price-takers. Political issue."
                },
                "PROCESSING BACKLOG": {
                    "val": f"{weekly_slaughter/1000:.0f}K", "unit": "Head/week", "status": "STEADY",
                    "insight": f"Processing {weekly_slaughter/1000:.0f}K/week. Labor tight. Any plant closure = backlog chaos like COVID-19."
                }
            },

            # 6. EXPORT/IMPORT DYNAMICS
            'trade': {
                "EXPORT VOLUME": {
                    "val": f"{export_pct}%", "unit": "of Production", "status": "CRITICAL",
                    "insight": f"Exports = {export_pct}% production. Japan ({japan_exports}M lbs), Korea ({korea_exports}M lbs) are lifeblood. Dollar strength kills exports."
                },
                "CHINA MARKET": {
                    "val": f"{china_exports}M lbs", "unit": "/year", "status": "VOLATILE",
                    "insight": f"China imports {china_exports}M lbs. Tariff/trade war wild card. When China bans = oversupply crash. When open = price spike."
                },
                "IMPORT PRESSURE": {
                    "val": f"{import_pct}%", "unit": "of Consumption", "status": "COMPETITION",
                    "insight": f"US imports {import_pct}% of beef consumed! Australia ({australia_imports}M lbs), NZ ({nz_imports}M lbs) = lean grinding beef competition."
                },
                "AUSTRALIA THREAT": {
                    "val": "HIGH", "unit": "Competition", "status": "GRASS-FED",
                    "insight": "Australia dominates grass-fed market. US can't compete on price. Imports cap ground beef prices. Structural headwind."
                }
            },

            # 7. COLD STORAGE
            'storage': {
                "TOTAL BEEF IN STORAGE": {
                    "val": f"{beef_cold_storage}M lbs", "unit": "lbs", "status": "TIGHT",
                    "insight": f"{beef_cold_storage}M lbs in freezers. Down {abs(storage_pct_change)}% YoY. Only {months_supply:.1f} months supply. Price support."
                },
                "SUPPLY COVERAGE": {
                    "val": f"{months_supply:.1f} mo", "unit": "Supply", "status": "CRITICAL",
                    "insight": f"Less than 1 month supply in storage. Normal = 1.5-2 months. Retail scrambling for inventory. Bullish for prices."
                }
            },

            # 8. BEEF CUT PRICE FORECASTS
            'cuts': {
                "GROUND BEEF (80/20)": {
                    "current": ground_beef, "target": 5.65, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [4.85, 4.95, 5.05, 5.12, 5.18, ground_beef],
                    "fut": [5.35, 5.50, 5.65],
                    "logic": f"Cow slaughter declining (herd rebuild coming). Ground beef tightens. Target ${5.65:.2f} by {dates['d90']}."
                },
                "CHUCK (Roast/Ground)": {
                    "current": 6.25, "target": 6.75, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [5.65, 5.80, 5.95, 6.05, 6.15, 6.25],
                    "fut": [6.40, 6.58, 6.75],
                    "logic": "Chuck = burger heaven. QSR demand strong. Restaurant recovery driving. $6.75 target."
                },
                "RIBEYE (Middle Meat)": {
                    "current": 15.85, "target": 17.25, "trend": "PREMIUM HOLD",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [14.50, 14.85, 15.20, 15.50, 15.68, 15.85],
                    "fut": [16.25, 16.75, 17.25],
                    "logic": "Ribeye = premium cut. Steakhouses recovering. Supply limited. $17.25 by Q2."
                },
                "STRIP LOIN (NY Strip)": {
                    "current": 14.25, "target": 15.50, "trend": "BULLISH",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [12.85, 13.20, 13.55, 13.90, 14.08, 14.25],
                    "fut": [14.65, 15.05, 15.50],
                    "logic": "Strip = white tablecloth demand. Tight supply + restaurant recovery = $15.50."
                },
                "SIRLOIN": {
                    "current": 8.95, "target": 9.45, "trend": "STEADY",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [8.25, 8.45, 8.60, 8.75, 8.85, 8.95],
                    "fut": [9.10, 9.28, 9.45],
                    "logic": "Sirloin = value steak. Grocery features. Steady demand. $9.45 target."
                },
                "BRISKET": {
                    "current": 7.45, "target": 8.25, "trend": "BBQ BOOM",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [6.50, 6.75, 6.95, 7.15, 7.30, 7.45],
                    "fut": [7.70, 7.98, 8.25],
                    "logic": "Brisket = BBQ craze. Limited supply (1 per animal). Demand exploding. $8.25+ easy."
                },
                "SHORT RIB": {
                    "current": 12.50, "target": 13.85, "trend": "RESTAURANT DARLING",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [10.85, 11.25, 11.65, 12.05, 12.28, 12.50],
                    "fut": [12.95, 13.40, 13.85],
                    "logic": "Short ribs = high-end restaurant trend. Korean BBQ, fine dining. Scarce cut. $13.85."
                },
                "TRIM (50/50)": {
                    "current": 3.25, "target": 3.65, "trend": "GRINDING BEEF",
                    "dates": [dates['d30'], dates['d60'], dates['d90']],
                    "hist": [2.85, 2.95, 3.05, 3.12, 3.18, 3.25],
                    "fut": [3.35, 3.50, 3.65],
                    "logic": "50/50 trim for ground beef. Cow slaughter down = lean trim scarce. $3.65."
                }
            }
        }

class DairyMarketAnalyzer:
    """Dairy market analyzer (impacts beef via cull cows)"""

    def __init__(self, market_data):
        self.market_data = market_data

    def calculate_metrics(self, dates):
        print(f"🥛 ANALYZING DAIRY: {self.market_data['timestamp']}")

        milk_price = self.market_data['milk']['current']
        cheese_price = self.market_data['cheese']['current']
        butter_price = self.market_data['butter']['current']

        # Dairy herd
        dairy_cows = 9.4  # Million
        milk_per_cow = 24000  # lbs/year
        dairy_cull_rate = 38  # % (culls become beef!)

        # Dairy beef impact
        dairy_beef_pct = 18  # % of US beef from dairy cattle
        dairy_steers_fed = 3.2  # Million/year (Holstein steers)

        return {
            'meta': {'time': self.market_data['timestamp'], 'dates': dates},
            'dairy_herd': {
                "DAIRY COW INVENTORY": {
                    "val": f"{dairy_cows}M", "unit": "Cows", "status": "STABLE",
                    "insight": f"{dairy_cows}M dairy cows. Cull rate {dairy_cull_rate}% = {dairy_cows * dairy_cull_rate/100:.1f}M cull cows/year entering beef supply."
                },
                "DAIRY BEEF CONTRIBUTION": {
                    "val": f"{dairy_beef_pct}%", "unit": "of Beef", "status": "SIGNIFICANT",
                    "insight": f"Dairy cattle = {dairy_beef_pct}% of US beef! Holstein steers + cull cows. When milk prices tank, culling increases = more beef."
                },
                "HOLSTEIN STEER IMPACT": {
                    "val": f"{dairy_steers_fed}M", "unit": "Head/year", "status": "SUPPLY FACTOR",
                    "insight": f"{dairy_steers_fed}M Holstein steers fed/year. Compete with beef cattle for feed/packer space. Lower quality but more volume."
                }
            },
            'dairy_prices': {
                "MILK PRICE": {
                    "val": f"${milk_price:.2f}", "unit": "/gal", "status": "MODERATE",
                    "insight": f"Milk ${milk_price:.2f}/gal. When low = aggressive culling = more beef supply = lower beef prices. Inverse relationship."
                },
                "CHEESE PRICE": {
                    "val": f"${cheese_price:.2f}", "unit": "/lb", "status": "ELEVATED",
                    "insight": f"Cheese ${cheese_price:.2f}. High cheese = dairy cows more valuable = less culling = less beef supply = higher beef prices."
                },
                "BUTTER PRICE": {
                    "val": f"${butter_price:.2f}", "unit": "/lb", "status": "STRONG",
                    "insight": f"Butter ${butter_price:.2f}. Strong dairy product prices = keep cows in milk = reduces beef supply from culls."
                }
            }
        }
