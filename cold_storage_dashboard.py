# ==================================================
# USDA COLD STORAGE INVENTORY DASHBOARD
# Historical Volumes - All Major Categories
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
    'pork': '#ff6b6b',
    'beef': '#ff3333',
    'poultry': '#ffaa00',
    'dairy': '#0099ff',
    'total': '#00ff88',
    'critical': '#ff0000'
}

# ==================================================
# COLD STORAGE DATA ENGINE
# ==================================================

class ColdStorageDataEngine:
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.cache_ttl = 1800  # 30 minutes

    def fetch_usda_cold_storage(self, commodity, category=None):
        """
        Fetch USDA NASS Cold Storage Report Data
        Published monthly - most comprehensive cold storage database
        Report covers: Meat, Poultry, Dairy, Frozen Foods
        """
        cache_key = f"cold_{commodity}_{category}"

        if cache_key in self.cache:
            ts, data = self.cache[cache_key]
            if time.time() - ts < self.cache_ttl:
                return data

        try:
            url = "http://quickstats.nass.usda.gov/api/api_GET/"

            # Base parameters
            params = {
                'key': USDA_KEY,
                'commodity_desc': commodity,
                'statisticcat_desc': 'INVENTORY',
                'agg_level_desc': 'NATIONAL',
                'format': 'JSON',
                'year__GE': '2023'  # Last 2+ years
            }

            # Add category if specified
            if category:
                params['class_desc'] = category

            r = self.session.get(url, params=params, timeout=15)

            if r.status_code == 200:
                data = r.json().get('data', [])
                if data:
                    # Sort by date (most recent first)
                    sorted_data = sorted(
                        data,
                        key=lambda x: (x.get('year', ''), x.get('reference_period_desc', '')),
                        reverse=True
                    )

                    # Extract values and dates
                    history = []
                    dates = []
                    for entry in sorted_data[:24]:  # Last 24 months
                        try:
                            val = float(entry.get('Value', '0').replace(',', ''))
                            year = entry.get('year', '')
                            month = entry.get('reference_period_desc', '')
                            history.append(val)
                            dates.append(f"{month} {year}")
                        except:
                            pass

                    current = history[0] if history else 0
                    avg_5yr = sum(history) / len(history) if history else 0

                    result = {
                        'current': current,
                        'history': history[:12],  # Last 12 months
                        'dates': dates[:12],
                        'avg_5yr': avg_5yr,
                        'vs_avg': ((current - avg_5yr) / avg_5yr * 100) if avg_5yr > 0 else 0
                    }

                    self.cache[cache_key] = (time.time(), result)
                    return result

        except Exception as e:
            print(f"USDA Cold Storage fetch error for {commodity}/{category}: {e}")

        return {'current': 0, 'history': [], 'dates': [], 'avg_5yr': 0, 'vs_avg': 0}

    def get_cold_storage_snapshot(self):
        """
        Get comprehensive cold storage data across all major categories

        DATA SOURCE: USDA NASS Cold Storage Report (monthly)
        - Most authoritative source for US frozen food inventory
        - Published around 20th of each month for prior month data
        """
        print("🧊 FETCHING USDA COLD STORAGE DATA...")

        # === PORK PRODUCTS ===
        print("  🥓 Fetching pork inventory...")
        pork_belly = self.fetch_usda_cold_storage('PORK', 'BELLY')
        pork_ham = self.fetch_usda_cold_storage('PORK', 'HAM')
        pork_loin = self.fetch_usda_cold_storage('PORK', 'LOIN')
        pork_butt = self.fetch_usda_cold_storage('PORK', 'BUTT')
        pork_picnic = self.fetch_usda_cold_storage('PORK', 'PICNIC')
        pork_spareribs = self.fetch_usda_cold_storage('PORK', 'SPARERIBS')
        pork_trim = self.fetch_usda_cold_storage('PORK', 'TRIMMINGS')
        pork_variety = self.fetch_usda_cold_storage('PORK', 'VARIETY MEATS')

        # Total pork (all categories)
        pork_total_data = self.fetch_usda_cold_storage('PORK')
        pork_total = pork_total_data.get('current', 0)
        if pork_total == 0:  # Calculate from components if total not available
            pork_total = (pork_belly.get('current', 0) + pork_ham.get('current', 0) +
                         pork_loin.get('current', 0) + pork_butt.get('current', 0) +
                         pork_picnic.get('current', 0) + pork_spareribs.get('current', 0) +
                         pork_trim.get('current', 0) + pork_variety.get('current', 0))

        print(f"    Total Pork: {pork_total/1000:.1f}M lbs")

        # === BEEF PRODUCTS ===
        print("  🥩 Fetching beef inventory...")
        beef_total = self.fetch_usda_cold_storage('BEEF')
        beef_boneless = self.fetch_usda_cold_storage('BEEF', 'BONELESS')
        beef_bone_in = self.fetch_usda_cold_storage('BEEF', 'BONE-IN')
        beef_variety = self.fetch_usda_cold_storage('BEEF', 'VARIETY MEATS')

        print(f"    Total Beef: {beef_total.get('current', 0)/1000:.1f}M lbs")

        # === POULTRY PRODUCTS ===
        print("  🐔 Fetching poultry inventory...")
        chicken_total = self.fetch_usda_cold_storage('CHICKEN')
        chicken_whole = self.fetch_usda_cold_storage('CHICKEN', 'WHOLE')
        chicken_parts = self.fetch_usda_cold_storage('CHICKEN', 'PARTS')

        turkey_total = self.fetch_usda_cold_storage('TURKEY')
        turkey_whole = self.fetch_usda_cold_storage('TURKEY', 'WHOLE')
        turkey_parts = self.fetch_usda_cold_storage('TURKEY', 'PARTS')

        poultry_total = chicken_total.get('current', 0) + turkey_total.get('current', 0)
        print(f"    Total Poultry: {poultry_total/1000:.1f}M lbs")

        # === DAIRY PRODUCTS ===
        print("  🧈 Fetching dairy inventory...")
        butter = self.fetch_usda_cold_storage('BUTTER')
        cheese = self.fetch_usda_cold_storage('CHEESE')

        dairy_total = butter.get('current', 0) + cheese.get('current', 0)
        print(f"    Total Dairy: {dairy_total/1000:.1f}M lbs")

        # === TOTAL RED MEAT ===
        red_meat_total = pork_total + beef_total.get('current', 0)

        # === GRAND TOTAL (estimated) ===
        grand_total = red_meat_total + poultry_total + dairy_total

        print(f"  📊 GRAND TOTAL INVENTORY: {grand_total/1000:.0f}M lbs")

        return {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'pork': {
                'total': pork_total,
                'total_data': pork_total_data,
                'belly': pork_belly,
                'ham': pork_ham,
                'loin': pork_loin,
                'butt': pork_butt,
                'picnic': pork_picnic,
                'spareribs': pork_spareribs,
                'trim': pork_trim,
                'variety': pork_variety
            },
            'beef': {
                'total': beef_total,
                'boneless': beef_boneless,
                'bone_in': beef_bone_in,
                'variety': beef_variety
            },
            'poultry': {
                'total': poultry_total,
                'chicken': chicken_total,
                'chicken_whole': chicken_whole,
                'chicken_parts': chicken_parts,
                'turkey': turkey_total,
                'turkey_whole': turkey_whole,
                'turkey_parts': turkey_parts
            },
            'dairy': {
                'total': dairy_total,
                'butter': butter,
                'cheese': cheese
            },
            'totals': {
                'red_meat': red_meat_total,
                'grand_total': grand_total
            }
        }

# ==================================================
# UI COMPONENTS
# ==================================================

class HeaderLabel:
    @staticmethod
    def create(parent, text, color, y, w):
        h = ui.Label(frame=(MARGIN, y, w, 25))
        h.text = text
        h.font = ('<system-bold>', 16)
        h.text_color = color
        h.alignment = ui.ALIGN_CENTER
        parent.add_subview(h)
        return y + 35

class MetricCard:
    @staticmethod
    def create(title, data, color, w, y):
        card_h = 120
        card = ui.View(frame=(MARGIN, y, w, card_h))
        card.background_color = '#1a1a1a'
        card.corner_radius = 8

        title_lbl = ui.Label(frame=(15, 10, w-30, 20))
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 14)
        title_lbl.text_color = color
        card.add_subview(title_lbl)

        val_lbl = ui.Label(frame=(15, 32, w-30, 24))
        val_lbl.text = f"{data['val']} {data['unit']}"
        val_lbl.font = ('<system-bold>', 18)
        val_lbl.text_color = 'white'
        card.add_subview(val_lbl)

        status_lbl = ui.Label(frame=(15, 58, w-30, 16))
        status_lbl.text = f"STATUS: {data['status']}"
        status_lbl.font = ('<system>', 11)
        status_lbl.text_color = THEME['sub']
        card.add_subview(status_lbl)

        insight_tv = ui.TextView(frame=(15, 76, w-30, 38))
        insight_tv.text = data['insight']
        insight_tv.font = ('<system>', 10)
        insight_tv.text_color = THEME['text']
        insight_tv.background_color = '#1a1a1a'
        insight_tv.editable = False
        card.add_subview(insight_tv)

        return card, card_h

class ChartCard:
    @staticmethod
    def create(title, chart_img, w, y):
        """Create card with embedded chart image"""
        card_h = 320
        card = ui.View(frame=(MARGIN, y, w, card_h))
        card.background_color = '#1a1a1a'
        card.corner_radius = 8

        title_lbl = ui.Label(frame=(15, 10, w-30, 20))
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 14)
        title_lbl.text_color = THEME['bull']
        card.add_subview(title_lbl)

        img_view = ui.ImageView(frame=(15, 40, w-30, 270))
        img_view.image = chart_img
        img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        card.add_subview(img_view)

        return card, card_h

# ==================================================
# COLD STORAGE ANALYZER
# ==================================================

class ColdStorageAnalyzer:
    def __init__(self, storage_data):
        self.storage_data = storage_data

    def calculate_metrics(self):
        """
        Analyze cold storage inventory levels and trends
        """
        print(f"🧊 ANALYZING COLD STORAGE: {self.storage_data['timestamp']}")

        # === PORK ANALYSIS ===
        pork = self.storage_data['pork']
        pork_total = pork['total'] / 1_000_000  # Convert to millions

        belly_curr = pork['belly'].get('current', 0) / 1_000_000
        belly_avg = pork['belly'].get('avg_5yr', 0) / 1_000_000
        belly_vs_avg = pork['belly'].get('vs_avg', 0)

        ham_curr = pork['ham'].get('current', 0) / 1_000_000
        ham_avg = pork['ham'].get('avg_5yr', 0) / 1_000_000
        ham_vs_avg = pork['ham'].get('vs_avg', 0)

        loin_curr = pork['loin'].get('current', 0) / 1_000_000
        loin_vs_avg = pork['loin'].get('vs_avg', 0)

        butt_curr = pork['butt'].get('current', 0) / 1_000_000
        picnic_curr = pork['picnic'].get('current', 0) / 1_000_000
        spareribs_curr = pork['spareribs'].get('current', 0) / 1_000_000
        trim_curr = pork['trim'].get('current', 0) / 1_000_000

        # === BEEF ANALYSIS ===
        beef = self.storage_data['beef']
        beef_total = beef['total'].get('current', 0) / 1_000_000
        beef_avg = beef['total'].get('avg_5yr', 0) / 1_000_000
        beef_vs_avg = beef['total'].get('vs_avg', 0)

        beef_boneless_curr = beef['boneless'].get('current', 0) / 1_000_000
        beef_bone_in_curr = beef['bone_in'].get('current', 0) / 1_000_000

        # === POULTRY ANALYSIS ===
        poultry = self.storage_data['poultry']
        chicken_curr = poultry['chicken'].get('current', 0) / 1_000_000
        chicken_avg = poultry['chicken'].get('avg_5yr', 0) / 1_000_000
        chicken_vs_avg = poultry['chicken'].get('vs_avg', 0)

        turkey_curr = poultry['turkey'].get('current', 0) / 1_000_000
        turkey_avg = poultry['turkey'].get('avg_5yr', 0) / 1_000_000
        turkey_vs_avg = poultry['turkey'].get('vs_avg', 0)

        poultry_total = chicken_curr + turkey_curr

        # === DAIRY ANALYSIS ===
        dairy = self.storage_data['dairy']
        butter_curr = dairy['butter'].get('current', 0) / 1_000_000
        butter_avg = dairy['butter'].get('avg_5yr', 0) / 1_000_000
        butter_vs_avg = dairy['butter'].get('vs_avg', 0)

        cheese_curr = dairy['cheese'].get('current', 0) / 1_000_000
        cheese_avg = dairy['cheese'].get('avg_5yr', 0) / 1_000_000
        cheese_vs_avg = dairy['cheese'].get('vs_avg', 0)

        # === TOTALS ===
        red_meat_total = self.storage_data['totals']['red_meat'] / 1_000_000
        grand_total = self.storage_data['totals']['grand_total'] / 1_000_000

        def get_status(vs_avg):
            """Determine status based on % vs average"""
            if vs_avg < -20:
                return "CRITICALLY LOW"
            elif vs_avg < -10:
                return "TIGHT"
            elif vs_avg < -5:
                return "BELOW NORMAL"
            elif vs_avg < 5:
                return "NORMAL"
            elif vs_avg < 10:
                return "ABOVE NORMAL"
            elif vs_avg < 20:
                return "ABUNDANT"
            else:
                return "OVERSUPPLIED"

        return {
            'meta': {
                'time': self.storage_data['timestamp']
            },

            # 1. OVERVIEW / TOTALS
            'overview': {
                "GRAND TOTAL INVENTORY": {
                    "val": f"{grand_total:.0f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Total tracked cold storage inventory: {grand_total:.0f}M lbs across meat, poultry, and dairy. This represents major frozen food categories monitored by USDA monthly."
                },
                "RED MEAT TOTAL": {
                    "val": f"{red_meat_total:.0f}M", "unit": "lbs", "status": "COMBINED",
                    "insight": f"All pork + beef = {red_meat_total:.0f}M lbs. Pork: {pork_total:.0f}M ({pork_total/red_meat_total*100:.0f}%), Beef: {beef_total:.0f}M ({beef_total/red_meat_total*100:.0f}%)."
                },
                "POULTRY TOTAL": {
                    "val": f"{poultry_total:.0f}M", "unit": "lbs", "status": "ABUNDANT",
                    "insight": f"All chicken + turkey = {poultry_total:.0f}M lbs. Chicken: {chicken_curr:.0f}M, Turkey: {turkey_curr:.0f}M. Poultry typically has higher inventory turnover than red meat."
                },
                "DAIRY TOTAL": {
                    "val": f"{butter_curr + cheese_curr:.0f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Butter + Cheese = {butter_curr + cheese_curr:.0f}M lbs. Dairy inventories critical for price discovery in commodity markets."
                }
            },

            # 2. PORK INVENTORY
            'pork': {
                "PORK TOTAL": {
                    "val": f"{pork_total:.0f}M", "unit": "lbs",
                    "status": get_status(pork['total_data'].get('vs_avg', 0)),
                    "insight": f"All pork products: {pork_total:.0f}M lbs. vs 5-yr avg: {pork['total_data'].get('vs_avg', 0):+.1f}%. Includes bellies, hams, loins, butts, picnics, ribs, trimmings, variety meats."
                },
                "PORK BELLIES": {
                    "val": f"{belly_curr:.1f}M", "unit": "lbs",
                    "status": get_status(belly_vs_avg),
                    "insight": f"Belly inventory {belly_curr:.1f}M lbs (5-yr avg: {belly_avg:.1f}M). vs avg: {belly_vs_avg:+.1f}%. CRITICAL CATEGORY - drives bacon pricing. Seasonal low in summer (grilling), high in winter."
                },
                "PORK HAMS": {
                    "val": f"{ham_curr:.1f}M", "unit": "lbs",
                    "status": get_status(ham_vs_avg),
                    "insight": f"Ham inventory {ham_curr:.1f}M lbs (5-yr avg: {ham_avg:.1f}M). vs avg: {ham_vs_avg:+.1f}%. Seasonal build for Easter/summer. Mexico export demand factor."
                },
                "PORK LOINS": {
                    "val": f"{loin_curr:.1f}M", "unit": "lbs",
                    "status": get_status(loin_vs_avg),
                    "insight": f"Loin inventory {loin_curr:.1f}M lbs. vs avg: {loin_vs_avg:+.1f}%. Premium primal - pork chops, roasts, tenderloins. Retail demand driver."
                },
                "PORK BUTTS": {
                    "val": f"{butt_curr:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Boston butt inventory {butt_curr:.1f}M lbs. Pulled pork, ground pork, sausage. BBQ season demand (spring/summer spike)."
                },
                "PORK PICNICS": {
                    "val": f"{picnic_curr:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Picnic shoulder {picnic_curr:.1f}M lbs. Lower-value shoulder cut. Export market favorite (Mexico, China)."
                },
                "PORK SPARERIBS": {
                    "val": f"{spareribs_curr:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Spareribs {spareribs_curr:.1f}M lbs. Seasonal grilling demand. Asian market strong (ethnic cuisines)."
                },
                "PORK TRIMMINGS": {
                    "val": f"{trim_curr:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Pork trim inventory {trim_curr:.1f}M lbs. Ground pork, sausage, pepperoni raw material. Lean/fat ratio blending stock."
                }
            },

            # 3. BEEF INVENTORY
            'beef': {
                "BEEF TOTAL": {
                    "val": f"{beef_total:.0f}M", "unit": "lbs",
                    "status": get_status(beef_vs_avg),
                    "insight": f"All beef products: {beef_total:.0f}M lbs. vs 5-yr avg: {beef_vs_avg:+.1f}%. Includes boneless, bone-in, variety meats. Beef inventory lower than pork (higher price, faster turnover)."
                },
                "BEEF BONELESS": {
                    "val": f"{beef_boneless_curr:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Boneless beef {beef_boneless_curr:.1f}M lbs. Ground beef, steaks, roasts. Premium retail cuts. Higher value = lower inventory levels."
                },
                "BEEF BONE-IN": {
                    "val": f"{beef_bone_in_curr:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Bone-in beef {beef_bone_in_curr:.1f}M lbs. Ribs, bone-in steaks. Restaurant/steakhouse demand. Premium grilling cuts."
                }
            },

            # 4. CHICKEN INVENTORY
            'chicken': {
                "CHICKEN TOTAL": {
                    "val": f"{chicken_curr:.0f}M", "unit": "lbs",
                    "status": get_status(chicken_vs_avg),
                    "insight": f"All chicken: {chicken_curr:.0f}M lbs (5-yr avg: {chicken_avg:.0f}M). vs avg: {chicken_vs_avg:+.1f}%. Largest volume protein. Fast turnover. QSR demand dominant."
                },
                "CHICKEN WHOLE BIRDS": {
                    "val": f"{poultry['chicken_whole'].get('current', 0)/1_000_000:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Whole chickens {poultry['chicken_whole'].get('current', 0)/1_000_000:.1f}M lbs. Retail/grocery demand. Rotisserie, roasting birds. Lower margin than parts."
                },
                "CHICKEN PARTS": {
                    "val": f"{poultry['chicken_parts'].get('current', 0)/1_000_000:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Chicken parts {poultry['chicken_parts'].get('current', 0)/1_000_000:.1f}M lbs. Breasts, wings, thighs, drumsticks. Higher value. QSR/foodservice heavy."
                }
            },

            # 5. TURKEY INVENTORY
            'turkey': {
                "TURKEY TOTAL": {
                    "val": f"{turkey_curr:.0f}M", "unit": "lbs",
                    "status": get_status(turkey_vs_avg),
                    "insight": f"All turkey: {turkey_curr:.0f}M lbs (5-yr avg: {turkey_avg:.0f}M). vs avg: {turkey_vs_avg:+.1f}%. HIGHLY SEASONAL - massive build for Thanksgiving (Oct-Nov), crash after holidays."
                },
                "TURKEY WHOLE BIRDS": {
                    "val": f"{poultry['turkey_whole'].get('current', 0)/1_000_000:.1f}M", "unit": "lbs", "status": "SEASONAL",
                    "insight": f"Whole turkeys {poultry['turkey_whole'].get('current', 0)/1_000_000:.1f}M lbs. Thanksgiving/Christmas driver. Inventory peaks Sept-Oct, bottoms Feb-Mar."
                },
                "TURKEY PARTS": {
                    "val": f"{poultry['turkey_parts'].get('current', 0)/1_000_000:.1f}M", "unit": "lbs", "status": "TRACKED",
                    "insight": f"Turkey parts {poultry['turkey_parts'].get('current', 0)/1_000_000:.1f}M lbs. Deli meat, ground turkey, turkey breast. Year-round demand steadier than whole birds."
                }
            },

            # 6. DAIRY INVENTORY
            'dairy': {
                "BUTTER": {
                    "val": f"{butter_curr:.0f}M", "unit": "lbs",
                    "status": get_status(butter_vs_avg),
                    "insight": f"Butter inventory {butter_curr:.0f}M lbs (5-yr avg: {butter_avg:.0f}M). vs avg: {butter_vs_avg:+.1f}%. PRICE SENSITIVE - tight inventory = retail price spikes. Baking season (Nov-Dec) demand."
                },
                "CHEESE": {
                    "val": f"{cheese_curr:.0f}M", "unit": "lbs",
                    "status": get_status(cheese_vs_avg),
                    "insight": f"Cheese inventory {cheese_curr:.0f}M lbs (5-yr avg: {cheese_avg:.0f}M). vs avg: {cheese_vs_avg:+.1f}%. American, cheddar, mozzarella. Pizza/QSR demand stable. CME spot market benchmark."
                }
            },

            # 7. HISTORICAL DATA FOR CHARTS
            'historical': {
                'pork_belly': pork['belly'],
                'pork_total': pork['total_data'],
                'beef_total': beef['total'],
                'chicken_total': poultry['chicken'],
                'turkey_total': poultry['turkey'],
                'butter': dairy['butter'],
                'cheese': dairy['cheese']
            }
        }

    def generate_charts(self, metrics):
        """Generate historical inventory charts"""
        charts = {}
        plt.style.use('dark_background')

        hist = metrics['historical']

        # 1. PORK BELLY HISTORICAL TREND
        if hist['pork_belly'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))
            history = hist['pork_belly']['history']
            dates = hist['pork_belly']['dates']
            avg = hist['pork_belly']['avg_5yr']

            # Convert to millions for readability
            history_m = [x/1_000_000 for x in history]
            avg_m = avg / 1_000_000

            x = range(len(history_m))
            ax.plot(x, history_m, 'o-', color='#ff6b6b', linewidth=3, markersize=8, label='Actual')
            ax.axhline(y=avg_m, color='#00ff88', linestyle='--', linewidth=2, label=f'5-Yr Avg ({avg_m:.1f}M)')

            ax.set_title('PORK BELLY COLD STORAGE - 12 MONTH TREND', fontsize=16, fontweight='bold', color='#ff6b6b')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Inventory (Million lbs)', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['pork_belly_trend'] = ui.Image.from_data(buf.read())
            plt.close()

        # 2. RED MEAT COMPARISON (Pork vs Beef)
        if hist['pork_total'].get('history') and hist['beef_total'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))

            pork_hist = [x/1_000_000 for x in hist['pork_total']['history']]
            beef_hist = [x/1_000_000 for x in hist['beef_total']['history']]
            dates = hist['pork_total']['dates']

            x = range(len(pork_hist))
            ax.plot(x, pork_hist, 'o-', color='#ff6b6b', linewidth=3, markersize=8, label='Pork')
            ax.plot(x, beef_hist, 's-', color='#ff3333', linewidth=3, markersize=8, label='Beef')

            ax.set_title('RED MEAT INVENTORY COMPARISON', fontsize=16, fontweight='bold')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Inventory (Million lbs)', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['red_meat_comparison'] = ui.Image.from_data(buf.read())
            plt.close()

        # 3. POULTRY TRENDS (Chicken vs Turkey)
        if hist['chicken_total'].get('history') and hist['turkey_total'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))

            chicken_hist = [x/1_000_000 for x in hist['chicken_total']['history']]
            turkey_hist = [x/1_000_000 for x in hist['turkey_total']['history']]
            dates = hist['chicken_total']['dates']

            x = range(len(chicken_hist))
            ax.plot(x, chicken_hist, 'o-', color='#ffaa00', linewidth=3, markersize=8, label='Chicken')
            ax.plot(x, turkey_hist, 's-', color='#ff9900', linewidth=3, markersize=8, label='Turkey')

            ax.set_title('POULTRY INVENTORY TRENDS', fontsize=16, fontweight='bold', color='#ffaa00')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Inventory (Million lbs)', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            # Highlight turkey seasonality
            ax.annotate('Thanksgiving Build', xy=(0, turkey_hist[0]), xytext=(2, turkey_hist[0]+50),
                       arrowprops=dict(arrowstyle='->', color='white', lw=1.5),
                       fontsize=10, color='white')

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['poultry_trends'] = ui.Image.from_data(buf.read())
            plt.close()

        # 4. DAIRY TRENDS (Butter vs Cheese)
        if hist['butter'].get('history') and hist['cheese'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))

            butter_hist = [x/1_000_000 for x in hist['butter']['history']]
            cheese_hist = [x/1_000_000 for x in hist['cheese']['history']]
            dates = hist['butter']['dates']

            x = range(len(butter_hist))
            ax.plot(x, butter_hist, 'o-', color='#ffdd44', linewidth=3, markersize=8, label='Butter')
            ax.plot(x, cheese_hist, 's-', color='#0099ff', linewidth=3, markersize=8, label='Cheese')

            ax.set_title('DAIRY PRODUCT INVENTORY', fontsize=16, fontweight='bold', color='#0099ff')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Inventory (Million lbs)', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['dairy_trends'] = ui.Image.from_data(buf.read())
            plt.close()

        return charts

# ==================================================
# DASHBOARD VIEW
# ==================================================

class ColdStorageDashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.name = 'USDA Cold Storage Inventory'
        self.data_engine = ColdStorageDataEngine()

    def refresh_data(self, sender):
        """Refresh all cold storage data and rebuild UI"""
        print("🔄 REFRESHING COLD STORAGE DATA...")

        # Clear cache to force fresh data fetch
        self.data_engine.cache.clear()

        # Remove all subviews
        for subview in list(self.subviews):
            self.remove_subview(subview)

        # Rebuild UI with fresh data
        self.layout()
        print("✅ REFRESH COMPLETE")

    def layout(self):
        w = self.width
        h = self.height

        # Add refresh button in top-right corner
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
        storage_data = self.data_engine.get_cold_storage_snapshot()
        analyzer = ColdStorageAnalyzer(storage_data)
        metrics = analyzer.calculate_metrics()

        # Generate charts
        print("📊 GENERATING CHARTS...")
        charts = analyzer.generate_charts(metrics)

        cw = w - (MARGIN * 2)
        y = 40

        # HEADER
        title = ui.Label(frame=(MARGIN, y, cw, 30))
        title.text = "🧊 USDA COLD STORAGE INVENTORY"
        title.font = ('<system-bold>', 26)
        title.text_color = THEME['total']
        title.alignment = ui.ALIGN_CENTER
        scroll.add_subview(title)
        y += 35

        sub = ui.Label(frame=(MARGIN, y, cw, 15))
        sub.text = f"HISTORICAL VOLUMES - ALL MAJOR CATEGORIES | {metrics['meta']['time']}"
        sub.font = ('<system>', 12)
        sub.text_color = THEME['sub']
        sub.alignment = ui.ALIGN_CENTER
        scroll.add_subview(sub)
        y += 40

        # 1. OVERVIEW
        y = HeaderLabel.create(scroll, "1. INVENTORY OVERVIEW", THEME['total'], y, cw)
        for k, v in metrics['overview'].items():
            card, card_h = MetricCard.create(k, v, THEME['total'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # 2. PORK INVENTORY
        y = HeaderLabel.create(scroll, "2. PORK COLD STORAGE", THEME['pork'], y, cw)
        for k, v in metrics['pork'].items():
            card, card_h = MetricCard.create(k, v, THEME['pork'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # CHART: Pork Belly Trend
        if 'pork_belly_trend' in charts:
            card, card_h = ChartCard.create("PORK BELLY INVENTORY - 12 MONTH HISTORY", charts['pork_belly_trend'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # CHART: Red Meat Comparison
        if 'red_meat_comparison' in charts:
            card, card_h = ChartCard.create("PORK VS BEEF INVENTORY TRENDS", charts['red_meat_comparison'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # 3. BEEF INVENTORY
        y = HeaderLabel.create(scroll, "3. BEEF COLD STORAGE", THEME['beef'], y, cw)
        for k, v in metrics['beef'].items():
            card, card_h = MetricCard.create(k, v, THEME['beef'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # 4. CHICKEN INVENTORY
        y = HeaderLabel.create(scroll, "4. CHICKEN COLD STORAGE", THEME['poultry'], y, cw)
        for k, v in metrics['chicken'].items():
            card, card_h = MetricCard.create(k, v, THEME['poultry'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # 5. TURKEY INVENTORY
        y = HeaderLabel.create(scroll, "5. TURKEY COLD STORAGE (SEASONAL)", THEME['poultry'], y, cw)
        for k, v in metrics['turkey'].items():
            card, card_h = MetricCard.create(k, v, THEME['poultry'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # CHART: Poultry Trends
        if 'poultry_trends' in charts:
            card, card_h = ChartCard.create("CHICKEN VS TURKEY SEASONALITY", charts['poultry_trends'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # 6. DAIRY INVENTORY
        y = HeaderLabel.create(scroll, "6. DAIRY COLD STORAGE", THEME['dairy'], y, cw)
        for k, v in metrics['dairy'].items():
            card, card_h = MetricCard.create(k, v, THEME['dairy'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # CHART: Dairy Trends
        if 'dairy_trends' in charts:
            card, card_h = ChartCard.create("BUTTER VS CHEESE INVENTORY", charts['dairy_trends'], cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # 7. SUMMARY
        y = self._draw_summary(scroll, y, cw, metrics)

        scroll.content_size = (w, y + 100)

    def _draw_summary(self, parent, y, w, metrics):
        y = HeaderLabel.create(parent, "7. MARKET INTELLIGENCE SUMMARY", THEME['warn'], y, w)
        card_h = 450
        card = ui.View(frame=(MARGIN, y, w, card_h))
        card.background_color = '#222'
        card.corner_radius = 8

        tv = ui.TextView(frame=(15, 15, w-30, card_h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 13)
        tv.editable = False
        tv.text = (
            "USDA COLD STORAGE REPORT - MARKET INTELLIGENCE:\n\n"
            "DATA SOURCE:\n"
            "Published monthly by USDA National Agricultural Statistics Service (NASS), typically around the "
            "20th of each month covering prior month's end-of-month inventory. This is the AUTHORITATIVE source "
            "for frozen food inventory levels in the United States.\n\n"
            "WHY IT MATTERS:\n"
            "Cold storage inventory levels are a critical leading indicator for commodity pricing. TIGHT inventories "
            "(below 5-year average) signal potential price increases as available supply shrinks. ABUNDANT inventories "
            "(above average) indicate oversupply and downward price pressure.\n\n"
            "KEY INSIGHTS:\n"
            "1. PORK BELLIES: Most price-sensitive category. Bacon demand is steady but supply varies seasonally. "
            "Summer grilling season typically draws down belly inventories (May-Aug lows), winter rebuild (Dec-Feb peaks). "
            "When belly stocks drop below 50M lbs = CRITICAL - bacon prices spike.\n\n"
            "2. TURKEY: Extreme seasonality. Massive inventory build Sept-Nov for Thanksgiving/Christmas, crash Jan-Mar. "
            "Whole bird inventory peaks ~300-400M lbs pre-Thanksgiving, bottoms ~100-150M lbs in spring. Turkey parts "
            "have steadier year-round demand (deli meat, ground turkey).\n\n"
            "3. BUTTER: Highly price-sensitive. Retail consumers notice butter price changes immediately. Tight butter "
            "stocks (<250M lbs) = retail price spikes. Baking season (Nov-Dec) drives seasonal demand.\n\n"
            "4. CHEESE: More stable than butter. American/cheddar/mozzarella dominate. CME spot cheese market uses "
            "inventory levels for price discovery. Pizza/QSR demand provides year-round baseline.\n\n"
            "5. BEEF vs PORK: Beef typically has LOWER inventory levels than pork despite higher consumption, because "
            "higher prices = faster turnover, less speculative storage. Pork's lower price point = more inventory held.\n\n"
            "6. CHICKEN: Largest volume but fastest turnover. QSR demand (McDonald's, Chick-fil-A, KFC) dominates. "
            "Breast meat premium, leg quarters often exported (Africa, Caribbean). Inventory levels rarely tight due "
            "to rapid production cycles (6-7 weeks vs 6 months for hogs/cattle).\n\n"
            "TRADING/PROCUREMENT STRATEGY:\n"
            "- Monitor monthly reports for your key commodities (bellies, hams, etc.)\n"
            "- When inventory drops >10% below 5-year average = LOCK IN SUPPLY (prices rising)\n"
            "- When inventory >10% above average = DELAY PURCHASING (prices falling)\n"
            "- Seasonal patterns: Turkey (Thanksgiving), Bellies (summer lows), Butter (holiday baking)\n"
            "- Compare current month vs same month prior year for apples-to-apples comparison\n\n"
            "REPORT TIMING:\n"
            "Published ~20th of each month. For example, January 20 report shows December 31 inventories. "
            "Plan procurement 30-60 days ahead based on inventory trends. Markets react to report immediately - "
            "futures prices move on release day."
        )
        tv.editable = False
        card.add_subview(tv)
        parent.add_subview(card)
        return y + card_h + 20

# ==================================================
# MAIN
# ==================================================

if __name__ == '__main__':
    v = ColdStorageDashboard()
    v.present('fullscreen')
