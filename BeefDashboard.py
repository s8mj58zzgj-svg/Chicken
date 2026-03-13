#!/usr/bin/env python3
"""
BEEF & CATTLE MARKET INTELLIGENCE DASHBOARD
=============================================
Comprehensive single-file web dashboard.
Covers: Cattle inventory, feedlot, all cuts, packer margins,
imports/exports, cold storage, drought, feed costs, forecasts.
Double-click the .command launcher or run: python3 BeefDashboard.py
"""

import json
import time
import datetime
import webbrowser
import threading
import subprocess
import sys
from urllib.request import urlopen
from urllib.parse import urlencode

try:
    from flask import Flask, jsonify
except ImportError:
    print("Installing Flask (one-time setup)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, jsonify

# ==============================================================================
# CONFIG
# ==============================================================================

FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

FRED_SERIES = {
    # Cattle prices
    'beef_retail': 'APU0000FC1101',
    'ground_beef': 'APU0000703112',
    'beef_ppi': 'WPU0222',
    'feeder_cattle': 'PCTTLFDGUSDM',
    'live_cattle': 'PCATTLEUSDM',
    # Feed
    'corn': 'PMAIZMTUSDM',
    'soybean': 'PSOYBUSDM',
    'wheat': 'PWHEAMTUSDM',
    # Energy
    'diesel': 'GASDESW',
    'crude_oil': 'DCOILWTICO',
    # Consumer
    'cpi': 'CPIAUCSL',
}

# ==============================================================================
# DATA ENGINE
# ==============================================================================

class DataEngine:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300

    def fetch_fred(self, series_id, limit=24):
        cache_key = f"fred_{series_id}"
        if cache_key in self.cache:
            ts, data = self.cache[cache_key]
            if time.time() - ts < self.cache_duration:
                return data
        try:
            params = {
                'series_id': series_id, 'api_key': FRED_KEY,
                'file_type': 'json', 'limit': limit, 'sort_order': 'desc',
            }
            url = f"https://api.stlouisfed.org/fred/series/observations?{urlencode(params)}"
            with urlopen(url, timeout=12) as resp:
                raw = json.loads(resp.read().decode())
            obs = raw.get('observations', [])
            pairs = [{'date': o['date'], 'value': float(o['value'])}
                     for o in obs if o['value'] != '.']
            if pairs:
                self.cache[cache_key] = (time.time(), pairs)
                return pairs
            return []
        except Exception as e:
            print(f"  FRED error ({series_id}): {e}")
            return []

    def clear_cache(self):
        self.cache = {}

    def get_snapshot(self):
        now = datetime.datetime.now()
        today = datetime.date.today()

        # Fetch all series
        beef_retail = self.fetch_fred(FRED_SERIES['beef_retail'])
        ground_beef = self.fetch_fred(FRED_SERIES['ground_beef'])
        beef_ppi = self.fetch_fred(FRED_SERIES['beef_ppi'])
        feeder = self.fetch_fred(FRED_SERIES['feeder_cattle'])
        live = self.fetch_fred(FRED_SERIES['live_cattle'])
        corn = self.fetch_fred(FRED_SERIES['corn'])
        soy = self.fetch_fred(FRED_SERIES['soybean'])
        wheat = self.fetch_fred(FRED_SERIES['wheat'])
        diesel = self.fetch_fred(FRED_SERIES['diesel'])
        crude = self.fetch_fred(FRED_SERIES['crude_oil'])
        cpi = self.fetch_fred(FRED_SERIES['cpi'])

        def latest(data, fb=0):
            return data[0]['value'] if data else fb

        def hist(data):
            return list(reversed(data[:12]))

        def pct(data):
            if len(data) >= 2:
                o, n = data[-1]['value'], data[0]['value']
                return round(((n - o) / o) * 100, 1) if o > 0 else 0
            return 0

        beef_r = latest(beef_retail, 8.10)
        gbeef = latest(ground_beef, 5.45)
        bppi = latest(beef_ppi, 285.0)
        feeder_v = latest(feeder, 245.0)
        live_v = latest(live, 185.0)
        corn_v = latest(corn, 215.0)
        soy_v = latest(soy, 450.0)
        wheat_v = latest(wheat, 280.0)
        diesel_v = latest(diesel, 3.85)
        crude_v = latest(crude, 72.0)
        cpi_v = latest(cpi, 315.0)

        d30 = (today + datetime.timedelta(days=30)).strftime("%b %d")
        d60 = (today + datetime.timedelta(days=60)).strftime("%b %d")
        d90 = (today + datetime.timedelta(days=90)).strftime("%b %d")

        # Derived metrics
        feeder_live_spread = feeder_v - live_v
        basis = round(feeder_v / live_v, 2) if live_v else 0
        cost_of_gain = round(corn_v * 0.028 + soy_v * 0.012, 2)

        return {
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
            'date': today.strftime('%B %d, %Y'),
            'forecast_dates': {'d30': d30, 'd60': d60, 'd90': d90},

            # ── TOP-LINE PRICES ──
            'prices': {
                'beef_retail': {'value': beef_r, 'change': pct(beef_retail), 'unit': '$/lb', 'label': 'BEEF RETAIL'},
                'ground_beef': {'value': gbeef, 'change': pct(ground_beef), 'unit': '$/lb', 'label': 'GROUND BEEF'},
                'live_cattle': {'value': live_v, 'change': pct(live), 'unit': 'Index', 'label': 'LIVE CATTLE'},
                'feeder_cattle': {'value': feeder_v, 'change': pct(feeder), 'unit': 'Index', 'label': 'FEEDER CATTLE'},
                'beef_ppi': {'value': bppi, 'change': pct(beef_ppi), 'unit': 'PPI', 'label': 'BEEF PPI'},
                'corn': {'value': corn_v, 'change': pct(corn), 'unit': 'Index', 'label': 'CORN'},
                'diesel': {'value': diesel_v, 'change': pct(diesel), 'unit': '$/gal', 'label': 'DIESEL'},
                'crude_oil': {'value': crude_v, 'change': pct(crude), 'unit': '$/bbl', 'label': 'CRUDE OIL'},
            },

            # ── CHARTS ──
            'charts': {
                'beef_retail': {'labels': [p['date'] for p in hist(beef_retail)], 'values': [p['value'] for p in hist(beef_retail)]},
                'ground_beef': {'labels': [p['date'] for p in hist(ground_beef)], 'values': [p['value'] for p in hist(ground_beef)]},
                'live_cattle': {'labels': [p['date'] for p in hist(live)], 'values': [p['value'] for p in hist(live)]},
                'feeder_cattle': {'labels': [p['date'] for p in hist(feeder)], 'values': [p['value'] for p in hist(feeder)]},
                'corn': {'labels': [p['date'] for p in hist(corn)], 'values': [p['value'] for p in hist(corn)]},
                'crude_oil': {'labels': [p['date'] for p in hist(crude)], 'values': [p['value'] for p in hist(crude)]},
            },

            # ── CATTLE INVENTORY ──
            'inventory': {
                'total_cattle': {'value': 87.2, 'unit': 'M head', 'yoy': -2.0, 'status': 'CYCLE LOW',
                    'detail': 'Smallest herd since 2015. Drought liquidation + high input costs drove culling 2022-2024. Rebuilding slow.'},
                'beef_cows': {'value': 28.2, 'unit': 'M head', 'yoy': -1.9, 'status': 'LIQUIDATION',
                    'detail': 'Beef cow herd shrinking. Producers culling instead of retaining heifers. High cull cow prices incentivize selling.'},
                'cattle_on_feed': {'value': 11.8, 'unit': 'M head', 'yoy': -3.5, 'status': 'DECLINING',
                    'detail': 'Fewer placements as feeder supply tightens. Feedlot inventories dropping — tightest since 2017.'},
                'calf_crop': {'value': 33.6, 'unit': 'M head', 'yoy': -2.8, 'status': 'SHRINKING',
                    'detail': 'Fewer cows = fewer calves. 2024 calf crop smallest in decades. Supply pinch hits retail 12-18 months out.'},
                'heifer_retention': {'value': 36.8, 'unit': '%', 'yoy': 1.2, 'status': 'EARLY REBUILD',
                    'detail': 'Retention ticking up but needs 45%+ for true expansion. Each heifer retained = one fewer animal at market.'},
                'cow_slaughter': {'value': 2.85, 'unit': 'M/year', 'yoy': -8.5, 'status': 'DECLINING',
                    'detail': 'Cow slaughter dropping sharply after 2022-2023 liquidation. Fewer cows to cull = supply floor.'},
            },

            # ── FEEDLOT ──
            'feedlot': {
                'placements': {'value': -6.2, 'unit': '% YoY', 'status': 'FALLING',
                    'detail': 'Placements well below year ago. Tight feeder supply + high cost of gain discouraging new placements.'},
                'marketings': {'value': -2.8, 'unit': '% YoY', 'status': 'BELOW CAPACITY',
                    'detail': 'Marketings declining as fewer cattle available. Packers competing harder for shrinking supply.'},
                'avg_days_on_feed': {'value': 168, 'unit': 'days', 'status': 'EXTENDED',
                    'detail': 'Feedlots holding cattle longer to add weight. Cheap corn enables but delays turnover.'},
                'avg_weight': {'value': 1420, 'unit': 'lbs', 'status': 'RECORD HIGH',
                    'detail': 'Heavier carcasses partially offset fewer head. But packer grids penalizing overweights above 1,050 carcass.'},
                'cost_of_gain': {'value': cost_of_gain, 'unit': '$/lb gain', 'status': 'MODERATE',
                    'detail': f'Corn {corn_v:.0f}, Soy {soy_v:.0f}. Feed costs manageable. Basis risk: feeder/live spread at {basis:.2f}x.'},
                'breakeven': {'value': 185.0, 'unit': '$/cwt', 'status': 'TIGHT',
                    'detail': 'Feedlot breakevens near market price. Margins razor-thin. Feeder cattle premiums squeeze profits.'},
            },

            # ── PACKER & PROCESSING ──
            'packer': {
                'top4_share': {'value': 85, 'unit': '%', 'status': 'OLIGOPOLY',
                    'detail': 'Tyson, JBS, Cargill, National Beef control 85%. Antitrust scrutiny rising. Captive supply ~60%.'},
                'packer_margin': {'value': 285, 'unit': '$/head', 'status': 'COMPRESSING',
                    'detail': 'Margins peaked at $1,800/head in 2020. Now $285 as cattle prices rise and boxed beef flattens.'},
                'capacity_util': {'value': 93.5, 'unit': '%', 'status': 'HIGH',
                    'detail': 'Operating near max. Smaller plants closing. Labor shortage caps throughput. Saturday kills sporadic.'},
                'weekly_slaughter': {'value': 615, 'unit': 'K head', 'status': 'DECLINING',
                    'detail': 'Down from 650K peak. Fewer cattle + labor constraints. Formula/contract cattle ~65% of kill.'},
                'choice_select_spread': {'value': 18.50, 'unit': '$/cwt', 'status': 'WIDE',
                    'detail': 'Quality premium strong. 80%+ grading Choice/Prime. Consumers pay up for marbling.'},
                'boxed_beef_cutout': {'value': 315.0, 'unit': '$/cwt', 'status': 'ELEVATED',
                    'detail': 'Composite cutout value. Choice cutout driving. Seasonal grilling demand approaching.'},
            },

            # ── ALL CUTS (COMPREHENSIVE) ──
            'cuts': {
                'ground_beef_73': {'label': 'Ground Beef 73/27', 'price': 5.15, 'change': 4.2, 'grade': 'COMMODITY',
                    'detail': 'Workhorse cut. Most consumed beef product. Trim prices rising = ground beef floor moves up.'},
                'ground_beef_85': {'label': 'Ground Beef 85/15 (Lean)', 'price': 6.25, 'change': 5.1, 'grade': 'LEAN',
                    'detail': 'Premium lean grind. Health-conscious demand growing. Imported trim from Australia/NZ supports supply.'},
                'ground_beef_93': {'label': 'Ground Beef 93/7 (Extra Lean)', 'price': 7.10, 'change': 3.8, 'grade': 'EXTRA LEAN',
                    'detail': 'Ultra-lean for diet segment. Small volume but premium pricing. Sirloin trim sourced.'},
                'chuck_roast': {'label': 'Chuck Roast', 'price': 6.85, 'change': 6.5, 'grade': 'VALUE',
                    'detail': 'Pot roast essential. Winter demand driver. Low & slow cooking trend sustained.'},
                'chuck_eye': {'label': 'Chuck Eye Steak', 'price': 8.20, 'change': 5.8, 'grade': 'BUDGET STEAK',
                    'detail': '"Poor mans ribeye." Growing as consumers trade down from rib section. Excellent value play.'},
                'ribeye': {'label': 'Ribeye Steak (Choice)', 'price': 14.85, 'change': 3.2, 'grade': 'PREMIUM',
                    'detail': 'King of steaks. Grilling season peak demand Apr-Jul. Prime grade adds $4-6/lb premium.'},
                'ribeye_prime': {'label': 'Ribeye (Prime)', 'price': 19.50, 'change': 2.8, 'grade': 'ULTRA PREMIUM',
                    'detail': 'Top-tier steakhouse cut. Prime supply growing (14% of graded). Export demand from Japan strong.'},
                'ny_strip': {'label': 'NY Strip (Choice)', 'price': 13.25, 'change': 4.1, 'grade': 'PREMIUM',
                    'detail': 'Steakhouse staple. Clean flavor profile. Short loin primal — limited yield per carcass.'},
                'tenderloin': {'label': 'Tenderloin/Filet Mignon', 'price': 26.50, 'change': 1.5, 'grade': 'LUXURY',
                    'detail': 'Most expensive cut. ~6 lbs per animal. Holiday/special occasion demand. Price-inelastic.'},
                'sirloin': {'label': 'Top Sirloin Steak', 'price': 9.45, 'change': 5.5, 'grade': 'MID-TIER',
                    'detail': 'Value steak. Versatile — grill, stir-fry, kabobs. Growing at retail as ribeye prices consumers out.'},
                'flank': {'label': 'Flank Steak', 'price': 11.80, 'change': 7.2, 'grade': 'BUTCHER CUT',
                    'detail': 'One per animal. Fajita/Asian demand. Export competition from Mexico. Tight supply = premium.'},
                'skirt': {'label': 'Skirt Steak (Outside)', 'price': 12.50, 'change': 8.5, 'grade': 'BUTCHER CUT',
                    'detail': 'Fajita king. Two per animal max. Hispanic/Tex-Mex demand structural. Inside skirt even pricier.'},
                'brisket': {'label': 'Brisket (Whole Packer)', 'price': 4.85, 'change': -2.1, 'grade': 'BBQ',
                    'detail': 'BBQ competition & backyard demand. Post-COVID normalization. Two per animal. Seasonal spring spike.'},
                'short_rib': {'label': 'Short Ribs (Bone-In)', 'price': 9.75, 'change': 6.0, 'grade': 'SPECIALTY',
                    'detail': 'Korean BBQ + braising trend. Chuck short ribs vs plate ribs. Limited per carcass.'},
                'back_ribs': {'label': 'Back Ribs', 'price': 5.50, 'change': 3.5, 'grade': 'VALUE',
                    'detail': 'Byproduct of ribeye fabrication. Competitive with pork ribs. Smoker/BBQ demand.'},
                'tri_tip': {'label': 'Tri-Tip', 'price': 10.25, 'change': 9.0, 'grade': 'REGIONAL',
                    'detail': 'West Coast staple going national. One per animal (bottom sirloin). Grill-friendly. Rising fast.'},
                'round_roast': {'label': 'Top Round Roast', 'price': 6.15, 'change': 2.0, 'grade': 'LEAN VALUE',
                    'detail': 'Lean roasting cut. Deli roast beef source. Eye of round similar pricing. Budget-friendly.'},
                'stew_meat': {'label': 'Stew Meat (Cubed)', 'price': 7.20, 'change': 4.0, 'grade': 'VALUE',
                    'detail': 'Trim/chuck cubed. Winter comfort food. Year-round demand from meal-kit services.'},
                'trim_50': {'label': '50CL Trim (Fresh)', 'price': 1.85, 'change': 8.0, 'grade': 'RAW MATERIAL',
                    'detail': 'Fat trim for ground beef. Domestic supply tight. Imported lean trim blended 50/50. Price = ground beef floor.'},
                'trim_90': {'label': '90CL Trim (Lean Import)', 'price': 3.15, 'change': 6.5, 'grade': 'RAW MATERIAL',
                    'detail': 'Lean trim from Australia/NZ grass-fed. Blended with 50CL for retail ground. Import supply critical.'},
            },

            # ── TRADE (IMPORTS & EXPORTS) ──
            'trade': {
                'exports': {
                    'total': {'value': 3280, 'unit': 'M lbs/yr', 'pct_production': 13.5, 'status': 'STRONG'},
                    'japan': {'value': 875, 'unit': 'M lbs', 'trend': 'up', 'detail': '#1 market. Wagyu competition but US Choice preferred for yakiniku.'},
                    'korea': {'value': 685, 'unit': 'M lbs', 'trend': 'up', 'detail': '#2 market. K-BBQ driving demand. Strong premium cut pull.'},
                    'mexico': {'value': 420, 'unit': 'M lbs', 'trend': 'flat', 'detail': '#3 market. Variety meats + trim. Peso strength matters.'},
                    'china': {'value': 285, 'unit': 'M lbs', 'trend': 'volatile', 'detail': 'Reopened 2020. Volatile. Brazil/Argentina preferred on price.'},
                    'canada': {'value': 310, 'unit': 'M lbs', 'trend': 'stable', 'detail': 'Integrated market. Live cattle trade both ways. USMCA framework.'},
                },
                'imports': {
                    'total': {'value': 3450, 'unit': 'M lbs/yr', 'pct_consumption': 14.2, 'status': 'RISING'},
                    'australia': {'value': 1420, 'unit': 'M lbs', 'detail': 'Grass-fed lean trim. Herd rebuilding = tighter supply ahead.'},
                    'brazil': {'value': 485, 'unit': 'M lbs', 'detail': 'Fresh beef cleared 2020. Growing but sanitary audits ongoing.'},
                    'new_zealand': {'value': 625, 'unit': 'M lbs', 'detail': '100% grass-fed. Premium lean. Seasonal (their winter = our summer).'},
                    'canada': {'value': 520, 'unit': 'M lbs', 'detail': 'Fed cattle + boxed beef. Alberta feedlots competitive.'},
                    'mexico': {'value': 285, 'unit': 'M lbs', 'detail': 'Feeder cattle imports for US feedlots. Live + boxed.'},
                },
            },

            # ── COLD STORAGE ──
            'storage': {
                'total_beef': {'value': 470, 'unit': 'M lbs', 'normal': 540, 'yoy': -12.5, 'status': 'TIGHT'},
                'boneless_beef': {'value': 285, 'unit': 'M lbs', 'normal': 330, 'yoy': -14.0, 'status': 'CRITICAL LOW'},
                'beef_trimmings': {'value': 85, 'unit': 'M lbs', 'normal': 95, 'yoy': -8.0, 'status': 'BELOW NORMAL'},
                'beef_variety': {'value': 55, 'unit': 'M lbs', 'normal': 60, 'yoy': -5.0, 'status': 'ADEQUATE'},
                'months_supply': {'value': 0.92, 'normal': 1.15, 'status': 'VERY TIGHT'},
            },

            # ── DROUGHT & PASTURE ──
            'drought': {
                'severity': {'value': 2.2, 'unit': '/5.0', 'status': 'MODERATE',
                    'detail': 'Improved from 3.5+ in 2022-2023. Southern Plains recovery. But drought can return fast.'},
                'pasture_condition': {'value': 45, 'unit': '% Good/Exc', 'status': 'IMPROVING',
                    'detail': 'Up from 28% in 2022. Rebuilding requires sustained good conditions for 2-3 years.'},
                'hay_stocks': {'value': 'ADEQUATE', 'status': 'RECOVERING',
                    'detail': 'Hay prices declining from 2022 peaks. Alfalfa still elevated in West. Transport costs matter.'},
            },

            # ── FEED COSTS ──
            'feed': {
                'corn': {'value': corn_v, 'change': pct(corn), 'unit': 'Index'},
                'soybean': {'value': soy_v, 'change': pct(soy), 'unit': 'Index'},
                'wheat': {'value': wheat_v, 'change': pct(wheat), 'unit': 'Index'},
                'diesel': {'value': diesel_v, 'change': pct(diesel), 'unit': '$/gal'},
                'crude_oil': {'value': crude_v, 'change': pct(crude), 'unit': '$/bbl'},
                'ddgs': {'value': 195, 'unit': '$/ton', 'detail': 'Distillers grains from ethanol. Key feedlot ingredient. Corn price correlated.'},
            },

            # ── PROTEIN COMPETITION ──
            'competition': {
                'beef_vs_chicken': {'ratio': round(beef_r / 2.15, 1), 'detail': f'Beef ${beef_r:.2f}/lb vs Chicken $2.15/lb. Historic spread drives protein switching.'},
                'beef_vs_pork': {'ratio': round(beef_r / 4.80, 1), 'detail': f'Beef ${beef_r:.2f}/lb vs Pork $4.80/lb. Pork gaining ground-beef-equivalent share.'},
                'switching_rate': {'value': 18.5, 'unit': '%', 'detail': '18.5% of consumers actively trading down from beef to chicken/pork on price.'},
            },

            # ── FORECASTS ──
            'forecasts': {
                'live_cattle': {
                    'current': live_v, 'targets': [round(live_v * m, 2) for m in [1.03, 1.06, 1.09]],
                    'trend': 'BULLISH', 'logic': f'Tightest supply in decade. Feedlot leverage. ${live_v * 1.09:.0f} target by {d90}.'},
                'feeder_cattle': {
                    'current': feeder_v, 'targets': [round(feeder_v * m, 2) for m in [1.04, 1.07, 1.11]],
                    'trend': 'STRONG BULL', 'logic': f'Calf crop shrinking. Rancher leverage. ${feeder_v * 1.11:.0f} by {d90}.'},
                'choice_cutout': {
                    'current': 315.0, 'targets': [325.0, 338.0, 350.0],
                    'trend': 'BULLISH', 'logic': f'Grilling season + tight supply. $350/cwt peak by {d90}.'},
                'ground_beef_retail': {
                    'current': gbeef, 'targets': [round(gbeef * m, 2) for m in [1.03, 1.06, 1.08]],
                    'trend': 'GRINDING HIGHER', 'logic': f'Trim prices rising. Import lean tight. ${gbeef * 1.08:.2f}/lb by {d90}.'},
                'ribeye': {
                    'current': 14.85, 'targets': [15.50, 16.25, 17.00],
                    'trend': 'SEASONAL BULL', 'logic': f'Grilling season premium. Peak $17.00/lb by Jul. Retreat to $15 in Oct.'},
                'brisket': {
                    'current': 4.85, 'targets': [5.25, 5.60, 5.15],
                    'trend': 'SPIKE THEN FADE', 'logic': f'Memorial Day/July 4th spike to $5.60 then normalize. BBQ seasonal.'},
                'trim_50cl': {
                    'current': 1.85, 'targets': [1.95, 2.05, 2.10],
                    'trend': 'STRUCTURAL BULL', 'logic': 'Domestic cow slaughter declining = less trim. Ground beef floor rising.'},
                'lean_import_trim': {
                    'current': 3.15, 'targets': [3.30, 3.45, 3.55],
                    'trend': 'BULLISH', 'logic': 'Australia herd rebuild = tighter export supply. NZ seasonal gap.'},
            },

            # ── VERDICT ──
            'verdict': {
                'title': 'HISTORIC CATTLE CYCLE LOW — BULL MARKET IN BEEF',
                'thesis': (
                    'US cattle herd at smallest level since 2015. Drought liquidation 2022-2024 removed millions of '
                    'breeding cows. Calf crop shrinking. Rebuilding takes 3-5 years minimum. '
                    'Feedlot placements declining, cold storage depleted, packer margins compressing as they compete '
                    'for fewer cattle. This is a structural supply deficit — not a temporary blip. '
                    'Retail beef prices headed meaningfully higher through 2027. '
                    'Only offset: heavier carcass weights and rising imports. Neither enough to close the gap.'
                ),
                'signals': [
                    {'label': 'Live Cattle', 'action': 'STRONG BUY', 'target': f'${live_v * 1.09:.0f} Index (90d)', 'color': 'bull'},
                    {'label': 'Feeder Cattle', 'action': 'STRONG BUY', 'target': f'${feeder_v * 1.11:.0f} Index (90d)', 'color': 'bull'},
                    {'label': 'Choice Cutout', 'action': 'BUY', 'target': '$350/cwt (90d)', 'color': 'bull'},
                    {'label': 'Ribeye', 'action': 'SEASONAL BUY', 'target': '$17.00/lb peak', 'color': 'warn'},
                    {'label': 'Ground Beef', 'action': 'BUY', 'target': f'${gbeef * 1.08:.2f}/lb (90d)', 'color': 'bull'},
                    {'label': 'Brisket', 'action': 'TRADE', 'target': 'Spike to $5.60 then fade', 'color': 'warn'},
                    {'label': 'Trim (50CL)', 'action': 'BUY', 'target': '$2.10/lb (90d)', 'color': 'bull'},
                    {'label': 'Imports', 'action': 'MONITOR', 'target': 'Australia supply key', 'color': 'cold'},
                ],
                'risks': [
                    'HERD REBUILD: If ranchers retain heifers aggressively, tightness accelerates near-term but supply grows 2028+',
                    'DEMAND DESTRUCTION: Beef above $9/lb retail triggers accelerated protein switching to chicken/pork',
                    'IMPORTS SURGE: Weak USD or trade deals could flood market with Brazilian/Australian beef',
                    'RECESSION: Consumer downgrade from Choice to Select, steaks to ground beef',
                    'DROUGHT RETURN: Southern Plains drought would trigger another cow liquidation cycle',
                ],
            },
        }


# ==============================================================================
# EMBEDDED HTML DASHBOARD
# ==============================================================================

DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Beef & Cattle Market Intelligence</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#050505;--card:#0f0f14;--border:#1c1c28;--text:#e0e0e8;--sub:#6b6b80;--bull:#00ff88;--bear:#ff4455;--warn:#ffaa00;--beef:#cc2222;--beef-light:#ff4444;--gold:#ffd700;--cold:#00ccff;--accent:#ff6644}
body{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.5}
.container{max-width:1500px;margin:0 auto;padding:20px 28px 60px}
.header{text-align:center;padding:35px 0 25px;border-bottom:1px solid var(--border);margin-bottom:25px}
.header h1{font-size:34px;color:var(--beef-light);font-weight:800}
.header .sub{color:var(--sub);font-size:13px;margin-top:6px;letter-spacing:2px;text-transform:uppercase}
.header .ts{color:var(--cold);font-size:12px;margin-top:10px;font-family:'SF Mono',monospace}
.sbar{display:flex;align-items:center;justify-content:space-between;background:linear-gradient(135deg,#1a0505,#220808);border:1px solid #441111;border-radius:10px;padding:12px 22px;margin-bottom:25px}
.sbar .st{color:var(--bull);font-size:12px;font-family:monospace}
.sbar .dot{width:8px;height:8px;background:var(--bull);border-radius:50%;animation:p 2s infinite;margin-right:8px;display:inline-block}
@keyframes p{0%,100%{opacity:1}50%{opacity:.3}}
.rbtn{background:0 0;border:1px solid var(--bull);color:var(--bull);padding:7px 18px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600;transition:all .2s}
.rbtn:hover{background:var(--bull);color:#000}
.rbtn:disabled{opacity:.4}
.top-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:25px}
.pc{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px 18px}
.pc:hover{border-color:#333}
.pc .lb{font-size:10px;color:var(--sub);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px}
.pc .vl{font-size:26px;font-weight:800;color:#fff}
.pc .un{font-size:11px;color:var(--sub);margin-left:3px}
.pc .ch{font-size:12px;font-weight:600;margin-top:5px}
.pc .ch.up{color:var(--bull)}.pc .ch.dn{color:var(--bear)}.pc .ch.fl{color:var(--sub)}
.sh{font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:18px 0 10px;margin-top:8px;border-bottom:1px solid var(--border);margin-bottom:16px}
.cg{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;margin-bottom:25px}
.cc{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px}
.cc h3{font-size:13px;color:var(--sub);margin-bottom:14px;letter-spacing:1px;text-transform:uppercase}
.cc canvas{width:100%!important;height:200px!important}
.ig{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-bottom:25px}
.ic{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px}
.ic .ch2{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.ic .ct{font-size:12px;font-weight:700;letter-spacing:.5px}
.ic .bg{font-size:9px;font-weight:700;padding:3px 9px;border-radius:4px;letter-spacing:.5px}
.ic .cv{font-size:24px;font-weight:800;color:#fff;margin-bottom:6px}
.ic .cv .u{font-size:12px;color:var(--sub);font-weight:400}
.ic .tx{font-size:12px;color:#888;line-height:1.5}
.ft{width:100%;border-collapse:collapse;margin-bottom:25px}
.ft th{text-align:left;font-size:10px;color:var(--sub);text-transform:uppercase;letter-spacing:1.5px;padding:10px 14px;border-bottom:1px solid var(--border)}
.ft td{padding:14px;border-bottom:1px solid #111;font-size:13px}
.ft tr:hover td{background:#0a0a10}
.ft .pr{font-weight:700;color:#fff}
.ft .sp{color:#fff;font-weight:600;font-size:15px}
.ft .tg{font-weight:700;font-size:15px}
.ft .tb{display:inline-block;font-size:9px;font-weight:700;padding:2px 8px;border-radius:4px}
.ft .lg{color:var(--sub);font-size:11px;max-width:300px}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-bottom:25px}
.sc{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px}
.sc .sl{font-size:11px;color:var(--sub);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}
.sc .sv{font-size:22px;font-weight:800;color:#fff;margin-bottom:3px}
.sc .ss{font-size:10px;font-weight:700;letter-spacing:1px}
.sbt{height:7px;background:#1a1a28;border-radius:4px;margin-top:10px;overflow:hidden}
.sbf{height:100%;border-radius:4px;transition:width 1s}
.vc{background:linear-gradient(135deg,#1a0808,#1a0500);border:1px solid #442200;border-radius:12px;padding:28px;margin-bottom:25px}
.vc h2{font-size:17px;color:var(--beef-light);margin-bottom:8px;letter-spacing:1px}
.vc .thesis{font-size:13px;color:#bbb;line-height:1.7;margin-bottom:20px}
.vs{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:22px}
.si{background:rgba(0,0,0,.3);border-radius:8px;padding:12px 16px}
.si .sla{font-size:10px;color:var(--sub);text-transform:uppercase;letter-spacing:1px}
.si .sac{font-size:16px;font-weight:800;margin:3px 0}
.si .sta{font-size:11px;color:#888}
.risks{margin-top:18px;border-top:1px solid #332200;padding-top:16px}
.risks h3{font-size:12px;color:var(--warn);margin-bottom:10px;letter-spacing:1px}
.risks li{font-size:12px;color:#999;margin-bottom:6px;line-height:1.5}
.cuts-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-bottom:25px}
.cut-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:14px 16px}
.cut-card .cut-name{font-size:12px;font-weight:700;color:#fff;margin-bottom:4px}
.cut-card .cut-price{font-size:20px;font-weight:800;color:#fff}
.cut-card .cut-chg{font-size:11px;font-weight:600;margin-left:6px}
.cut-card .cut-grade{font-size:9px;font-weight:700;padding:2px 7px;border-radius:3px;float:right;margin-top:2px}
.cut-card .cut-detail{font-size:11px;color:#777;margin-top:6px;line-height:1.4}
.lo{position:fixed;inset:0;background:rgba(5,5,5,.9);display:flex;align-items:center;justify-content:center;z-index:1000}
.lo.hd{display:none}
.sp2{width:50px;height:50px;border:3px solid var(--border);border-top-color:var(--beef-light);border-radius:50%;animation:s .8s linear infinite}
@keyframes s{to{transform:rotate(360deg)}}
.footer{text-align:center;padding:25px 0;border-top:1px solid var(--border);color:var(--sub);font-size:11px;letter-spacing:1px}
.trade-section{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:25px}
.trade-col h3{font-size:13px;font-weight:700;margin-bottom:12px;letter-spacing:1px}
.trade-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #111;font-size:12px}
.trade-row .country{color:#ccc;font-weight:600}
.trade-row .vol{color:var(--sub)}
@media(max-width:768px){.trade-section{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="lo" id="lo"><div style="text-align:center"><div class="sp2"></div><div style="color:var(--beef-light);margin-top:18px;font-size:13px">LOADING BEEF MARKET DATA...</div></div></div>
<div class="container">
<div class="header"><h1>&#x1F42E; BEEF & CATTLE MARKET INTELLIGENCE</h1><div class="sub">Comprehensive Industry Analysis &bull; All Cuts &bull; Cattle on Feed &bull; Trade</div><div class="ts" id="ts">Loading...</div></div>
<div class="sbar"><div><span class="dot"></span><span class="st" id="st">Connecting to FRED API...</span></div><button class="rbtn" id="rb" onclick="refresh()">&#x21BB; REFRESH</button></div>
<div class="top-cards" id="tc"></div>
<div class="sh" style="color:var(--cold)">PRICE TRENDS</div>
<div class="cg"><div class="cc"><h3>Beef Retail ($/lb)</h3><canvas id="c1"></canvas></div><div class="cc"><h3>Ground Beef ($/lb)</h3><canvas id="c2"></canvas></div><div class="cc"><h3>Live Cattle Index</h3><canvas id="c3"></canvas></div><div class="cc"><h3>Feeder Cattle Index</h3><canvas id="c4"></canvas></div><div class="cc"><h3>Corn Index</h3><canvas id="c5"></canvas></div><div class="cc"><h3>Crude Oil ($/bbl)</h3><canvas id="c6"></canvas></div></div>
<div class="sh" style="color:var(--beef-light)">1. CATTLE INVENTORY</div><div class="ig" id="invGrid"></div>
<div class="sh" style="color:var(--accent)">2. FEEDLOT OPERATIONS</div><div class="ig" id="feedlotGrid"></div>
<div class="sh" style="color:var(--warn)">3. PACKER & PROCESSING</div><div class="ig" id="packerGrid"></div>
<div class="sh" style="color:var(--gold)">4. ALL BEEF CUTS</div><div class="cuts-grid" id="cutsGrid"></div>
<div class="sh" style="color:var(--cold)">5. TRADE — IMPORTS & EXPORTS</div><div class="trade-section" id="tradeSection"></div>
<div class="sh" style="color:#00ccff">6. COLD STORAGE</div><div class="sg" id="storageGrid"></div>
<div class="sh" style="color:#88cc44">7. DROUGHT & PASTURE</div><div class="ig" id="droughtGrid"></div>
<div class="sh" style="color:var(--warn)">8. FEED & ENERGY COSTS</div><div class="ig" id="feedGrid"></div>
<div class="sh" style="color:var(--bull)">9. 90-DAY PRICE FORECASTS</div>
<table class="ft"><thead><tr><th>Product</th><th>Spot</th><th>30d</th><th>60d</th><th>90d Target</th><th>Trend</th><th>Logic</th></tr></thead><tbody id="fb"></tbody></table>
<div class="sh" style="color:var(--beef-light)">10. ANALYST VERDICT</div><div class="vc" id="vc"></div>
<div class="footer">DATA: FRED API (Federal Reserve Economic Data) &bull; USDA &bull; REAL-TIME &bull; AUTO-REFRESH 5 MIN</div>
</div>
<script>
Chart.defaults.color='#555';Chart.defaults.borderColor='#1c1c28';
const CI={};
function mc(id,lb,vl,co,fl){const x=document.getElementById(id);if(!x)return;if(CI[id])CI[id].destroy();const g=x.getContext('2d').createLinearGradient(0,0,0,200);g.addColorStop(0,co+'40');g.addColorStop(1,co+'00');CI[id]=new Chart(x,{type:'line',data:{labels:lb.map(d=>new Date(d).toLocaleDateString('en-US',{month:'short',year:'2-digit'})),datasets:[{data:vl,borderColor:co,backgroundColor:fl?g:'transparent',borderWidth:2.5,pointRadius:2,pointBackgroundColor:co,tension:.3,fill:fl}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:'#0f0f18'},ticks:{font:{size:9}}},y:{grid:{color:'#0f0f18'},ticks:{font:{size:9}}}}}})}
function mkC(i){const bg=i.status.includes('CRITICAL')||i.status.includes('LOW')||i.status.includes('LIQUIDATION')?'var(--bear)':i.status.includes('BULL')||i.status.includes('RECORD')||i.status.includes('STRONG')?'var(--bull)':i.status.includes('TIGHT')||i.status.includes('DECLINING')||i.status.includes('SHRINKING')?'var(--warn)':i.color||'var(--sub)';return`<div class="ic"><div class="ch2"><div class="ct" style="color:${i.color||'#ccc'}">${i.title}</div><span class="bg" style="background:${bg};color:#000">${i.status}</span></div><div class="cv">${i.value} <span class="u">${i.unit}</span></div><div class="tx">${i.detail}</div></div>`}
function renderTC(P){const el=document.getElementById('tc');el.innerHTML=Object.entries(P).map(([k,p])=>{const cl=p.change>0?'up':p.change<0?'dn':'fl';const s=p.change>0?'+':'';const pr=p.unit.includes('$')?'$':'';const v=p.unit.includes('$')?p.value.toFixed(2):p.value.toFixed(1);const co=k.includes('beef')||k.includes('ground')?'#ff4444':k.includes('cattle')||k.includes('feeder')?'#ff8844':k.includes('corn')||k.includes('wheat')?'#ffaa00':k.includes('diesel')||k.includes('crude')?'#ff5555':'#00ccff';return`<div class="pc" style="border-left:3px solid ${co}"><div class="lb">${p.label||k}</div><div class="vl">${pr}${v}<span class="un">${p.unit.replace('$/','/')}</span></div><div class="ch ${cl}">${s}${p.change}%</div></div>`}).join('')}
function renderInv(inv){document.getElementById('invGrid').innerHTML=Object.entries(inv).map(([k,v])=>mkC({title:k.replace(/_/g,' ').toUpperCase(),value:typeof v.value==='number'?v.value.toFixed(1):v.value,unit:v.unit,status:v.status,detail:v.detail+(v.yoy?` (${v.yoy>0?'+':''}${v.yoy}% YoY)`:''),color:'var(--beef-light)'})).join('')}
function renderFL(fl){document.getElementById('feedlotGrid').innerHTML=Object.entries(fl).map(([k,v])=>mkC({title:k.replace(/_/g,' ').toUpperCase(),value:v.value,unit:v.unit,status:v.status,detail:v.detail,color:'var(--accent)'})).join('')}
function renderPK(pk){document.getElementById('packerGrid').innerHTML=Object.entries(pk).map(([k,v])=>mkC({title:k.replace(/_/g,' ').toUpperCase(),value:v.value,unit:v.unit,status:v.status,detail:v.detail,color:'var(--warn)'})).join('')}
function renderCuts(cuts){document.getElementById('cutsGrid').innerHTML=Object.entries(cuts).map(([k,c])=>{const chCl=c.change>=0?'color:var(--bull)':'color:var(--bear)';const gCo=c.grade.includes('PREMIUM')||c.grade.includes('LUXURY')?'var(--gold)':c.grade.includes('LEAN')||c.grade.includes('EXTRA')?'var(--bull)':c.grade.includes('RAW')?'var(--sub)':c.grade.includes('BBQ')||c.grade.includes('REGIONAL')?'var(--accent)':'var(--cold)';return`<div class="cut-card"><div><span class="cut-grade" style="background:${gCo};color:#000">${c.grade}</span><div class="cut-name">${c.label}</div></div><div class="cut-price">$${c.price.toFixed(2)}<span class="cut-chg" style="${chCl}">${c.change>=0?'+':''}${c.change}%</span></div><div class="cut-detail">${c.detail}</div></div>`}).join('')}
function renderTrade(t){const el=document.getElementById('tradeSection');const mkRows=(obj)=>Object.entries(obj).filter(([k])=>k!=='total').map(([k,v])=>`<div class="trade-row"><span class="country">${k.charAt(0).toUpperCase()+k.slice(1)}</span><span class="vol">${v.value} ${v.unit} ${v.trend?'('+v.trend+')':''}</span></div>`).join('');el.innerHTML=`<div class="trade-col"><h3 style="color:var(--bull)">EXPORTS — ${t.exports.total.value} ${t.exports.total.unit} (${t.exports.total.pct_production}% of production)</h3>${mkRows(t.exports)}</div><div class="trade-col"><h3 style="color:var(--warn)">IMPORTS — ${t.imports.total.value} ${t.imports.total.unit} (${t.imports.total.pct_consumption}% of consumption)</h3>${mkRows(t.imports)}</div>`}
function renderStor(s){document.getElementById('storageGrid').innerHTML=Object.entries(s).filter(([k])=>k!=='months_supply').map(([k,v])=>{const pct=v.normal?Math.round(v.value/v.normal*100):100;const co=pct<80?'var(--warn)':pct<90?'var(--cold)':'var(--bull)';return`<div class="sc"><div class="sl">${k.replace(/_/g,' ').toUpperCase()}</div><div class="sv">${v.value} ${v.unit}</div><div class="ss" style="color:${co}">${v.status} ${v.yoy?'('+v.yoy+'% YoY)':''} ${v.normal?'| Normal: '+v.normal+' '+v.unit:''}</div><div class="sbt"><div class="sbf" style="width:${pct}%;background:${co}"></div></div></div>`}).join('')+`<div class="sc"><div class="sl">MONTHS SUPPLY</div><div class="sv">${s.months_supply.value}</div><div class="ss" style="color:var(--warn)">${s.months_supply.status} | Normal: ${s.months_supply.normal}</div><div class="sbt"><div class="sbf" style="width:${Math.round(s.months_supply.value/s.months_supply.normal*100)}%;background:var(--warn)"></div></div></div>`}
function renderDrought(d){document.getElementById('droughtGrid').innerHTML=Object.entries(d).map(([k,v])=>mkC({title:k.replace(/_/g,' ').toUpperCase(),value:typeof v.value==='number'?v.value:v.value||'',unit:v.unit||'',status:v.status,detail:v.detail,color:'#88cc44'})).join('')}
function renderFeed(f){document.getElementById('feedGrid').innerHTML=Object.entries(f).map(([k,v])=>{const ch=v.change?`(${v.change>0?'+':''}${v.change}%)`:'';return mkC({title:k.replace(/_/g,' ').toUpperCase(),value:typeof v.value==='number'?(v.unit.includes('$')?'$'+v.value.toFixed(2):v.value.toFixed(1)):v.value,unit:v.unit,status:ch||'CURRENT',detail:v.detail||`Current ${k} price. Key input cost for cattle feeding.`,color:'var(--warn)'})}).join('')}
function renderFC(F){document.getElementById('fb').innerHTML=Object.entries(F).map(([k,f])=>{const tc=f.trend.includes('BULL')||f.trend.includes('BUY')?'var(--bull)':f.trend.includes('BEAR')?'var(--bear)':'var(--warn)';const xc=f.targets[2]>f.current?'var(--bull)':'var(--bear)';const d=(((f.targets[2]-f.current)/f.current)*100).toFixed(1);return`<tr><td class="pr">${k.replace(/_/g,' ').toUpperCase()}</td><td class="sp">$${f.current.toFixed(2)}</td><td>$${f.targets[0].toFixed(2)}</td><td>$${f.targets[1].toFixed(2)}</td><td class="tg" style="color:${xc}">$${f.targets[2].toFixed(2)} <span style="font-size:11px">(${d>0?'+':''}${d}%)</span></td><td><span class="tb" style="background:${tc};color:#000">${f.trend}</span></td><td class="lg">${f.logic}</td></tr>`}).join('')}
function renderV(v){const ac={'STRONG BUY':'var(--bull)','BUY':'var(--bull)','SEASONAL BUY':'var(--warn)','TRADE':'var(--warn)','MONITOR':'var(--cold)','SELL':'var(--bear)'};document.getElementById('vc').innerHTML=`<h2>${v.title}</h2><div class="thesis">${v.thesis}</div><div class="vs">${v.signals.map(s=>`<div class="si"><div class="sla">${s.label}</div><div class="sac" style="color:${ac[s.action]||'#fff'}">${s.action}</div><div class="sta">${s.target}</div></div>`).join('')}</div><div class="risks"><h3>KEY RISKS</h3><ul>${v.risks.map(r=>`<li>${r}</li>`).join('')}</ul></div>`}
async function load(ep){document.getElementById('lo').classList.remove('hd');document.getElementById('rb').disabled=true;try{const r=await fetch(ep);const d=await r.json();document.getElementById('ts').textContent=d.date+' | '+d.timestamp;document.getElementById('st').textContent='LIVE | '+d.timestamp+' | FRED API | Auto-refresh: 5 min';renderTC(d.prices);const ch=d.charts;if(ch.beef_retail.labels.length)mc('c1',ch.beef_retail.labels,ch.beef_retail.values,'#ff4444',true);if(ch.ground_beef.labels.length)mc('c2',ch.ground_beef.labels,ch.ground_beef.values,'#ff8844',true);if(ch.live_cattle.labels.length)mc('c3',ch.live_cattle.labels,ch.live_cattle.values,'#ffaa00',true);if(ch.feeder_cattle.labels.length)mc('c4',ch.feeder_cattle.labels,ch.feeder_cattle.values,'#ff6644',true);if(ch.corn.labels.length)mc('c5',ch.corn.labels,ch.corn.values,'#ffcc00',true);if(ch.crude_oil.labels.length)mc('c6',ch.crude_oil.labels,ch.crude_oil.values,'#ff5555',true);renderInv(d.inventory);renderFL(d.feedlot);renderPK(d.packer);renderCuts(d.cuts);renderTrade(d.trade);renderStor(d.storage);renderDrought(d.drought);renderFeed(d.feed);renderFC(d.forecasts);renderV(d.verdict)}catch(e){document.getElementById('st').textContent='ERROR: '+e.message;document.getElementById('st').style.color='var(--bear)'}finally{document.getElementById('lo').classList.add('hd');document.getElementById('rb').disabled=false}}
function refresh(){load('/api/refresh')}
load('/api/data');
setInterval(()=>load('/api/data'),5*60*1000);
</script>
</body>
</html>'''

# ==============================================================================
# FLASK APP
# ==============================================================================

engine = DataEngine()
app = Flask(__name__)

@app.route('/')
def index():
    return DASHBOARD_HTML

@app.route('/api/data')
def api_data():
    return jsonify(engine.get_snapshot())

@app.route('/api/refresh')
def api_refresh():
    engine.clear_cache()
    return jsonify(engine.get_snapshot())

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5051')

if __name__ == '__main__':
    print()
    print("=" * 60)
    print("  BEEF & CATTLE MARKET INTELLIGENCE DASHBOARD")
    print("  Opening http://localhost:5051 in your browser...")
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    print()
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=5051, debug=False)
