# ==================================================
# USDA COLD STORAGE INVENTORY DASHBOARD - COMPLETE
# Historical Volumes - ALL Categories (Meat, Poultry, Dairy, Fruits, Vegetables, Seafood, Eggs, Juices)
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
    'fruit': '#ff1493',
    'veg': '#32cd32',
    'seafood': '#00bfff',
    'eggs': '#ffeb3b',
    'juice': '#ff8c00',
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
        self.use_sample_data = False  # Set to True if API is unavailable

    def generate_sample_data(self, commodity, category=None):
        """Generate realistic sample cold storage data for testing"""
        import random
        import datetime as dt

        # Base values in thousand lbs for different commodities
        base_values = {
            'PORK': {'BELLY': 35000, 'HAM': 85000, 'LOIN': 45000, 'BUTT': 55000,
                    'PICNIC': 40000, 'SPARERIBS': 12000, 'TRIMMINGS': 25000,
                    'VARIETY MEATS': 8000, None: 305000},
            'BEEF': {None: 450000, 'BONELESS': 280000, 'BONE-IN': 120000,
                    'VARIETY MEATS': 50000},
            'CHICKEN': {None: 720000, 'WHOLE': 180000, 'PARTS': 400000,
                       'BREAST': 200000, 'WING': 80000, 'LEG QUARTERS': 120000},
            'TURKEY': {None: 420000, 'WHOLE': 200000, 'PARTS': 180000,
                      'BREAST': 100000},
            'BUTTER': {None: 280000},
            'CHEESE': {None: 1400000, 'AMERICAN': 350000, 'CHEDDAR': 700000,
                      'SWISS': 150000, 'OTHER': 200000},
            'STRAWBERRIES': {None: 120000},
            'BLUEBERRIES': {None: 85000},
            'RASPBERRIES': {None: 35000},
            'BLACKBERRIES': {None: 28000},
            'CHERRIES': {None: 42000},
            'APPLES': {'FROZEN': 55000},
            'PEACHES': {'FROZEN': 32000},
            'GRAPES': {'FROZEN': 18000},
            'PEAS': {'FROZEN': 95000},
            'CORN': {'FROZEN': 140000},
            'BEANS': {'GREEN, FROZEN': 78000, 'LIMA, FROZEN': 35000},
            'CARROTS': {'FROZEN': 62000},
            'BROCCOLI': {None: 72000},
            'CAULIFLOWER': {'FROZEN': 48000},
            'SPINACH': {'FROZEN': 38000},
            'VEGETABLES': {'MIXED, FROZEN': 110000},
            'POTATOES': {'FRENCH FRIED': 850000, 'OTHER FROZEN': 180000},
            'ONIONS': {'FROZEN': 42000},
            'ORANGES': {'JUICE CONCENTRATE': 420000},
            'GRAPEFRUIT': {'JUICE': 85000},
            'FISH': {None: 280000, 'FILLETS': 150000},
            'SHELLFISH': {None: 95000},
            'SHRIMP': {None: 180000},
            'EGGS': {'SHELL': 42000, 'FROZEN': 68000, 'DRIED': 35000}
        }

        # Get base value
        base = base_values.get(commodity, {}).get(category, 50000)

        # Generate 12 months of history with seasonal variation
        history = []
        dates = []
        current_date = dt.datetime.now()

        for i in range(12):
            month_date = current_date - dt.timedelta(days=30*i)
            # Add seasonal variation (±15%)
            variation = 1.0 + (random.random() - 0.5) * 0.3
            value = base * variation * 1000  # Convert to lbs
            history.append(value)
            dates.append(month_date.strftime("%b %Y"))

        history.reverse()
        dates.reverse()

        current = history[-1]
        avg_5yr = sum(history) / len(history)

        return {
            'current': current,
            'history': history,
            'dates': dates,
            'avg_5yr': avg_5yr,
            'vs_avg': ((current - avg_5yr) / avg_5yr * 100) if avg_5yr > 0 else 0
        }

    def fetch_usda_cold_storage(self, commodity, category=None):
        """
        Fetch USDA NASS Cold Storage Report Data
        Published monthly - most comprehensive cold storage database
        Report covers: Meat, Poultry, Dairy, Frozen Foods, Fruits, Vegetables
        """
        cache_key = f"cold_{commodity}_{category}"

        if cache_key in self.cache:
            ts, data = self.cache[cache_key]
            if time.time() - ts < self.cache_ttl:
                return data

        # Use sample data if enabled
        if self.use_sample_data:
            return self.generate_sample_data(commodity, category)

        try:
            url = "http://quickstats.nass.usda.gov/api/api_GET/"

            # Build search term for short_desc
            search_term = f"{commodity}"
            if category:
                search_term += f", {category}"
            search_term += " - COLD STORAGE"

            # Base parameters - using short_desc for more specific searching
            params = {
                'key': USDA_KEY,
                'short_desc__LIKE': search_term,
                'freq_desc': 'MONTHLY',
                'agg_level_desc': 'NATIONAL',
                'format': 'JSON',
                'year__GE': '2023'  # Last 2+ years
            }

            r = self.session.get(url, params=params, timeout=15)

            # Check for 403 or other errors that indicate API is blocked
            if r.status_code == 403:
                print(f"⚠️  USDA API blocked (403) - switching to sample data mode")
                self.use_sample_data = True
                return self.generate_sample_data(commodity, category)

            if r.status_code == 200:
                resp_data = r.json()
                data = resp_data.get('data', [])

                # If no data with full search, try simpler search
                if not data:
                    # Try without category
                    params['short_desc__LIKE'] = f"{commodity} - COLD STORAGE"
                    r = self.session.get(url, params=params, timeout=15)
                    if r.status_code == 200:
                        data = r.json().get('data', [])

                # If still no data, try with STOCKS instead of COLD STORAGE
                if not data:
                    params['short_desc__LIKE'] = f"{commodity} - STOCKS"
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
                else:
                    # No data found, switch to sample data
                    print(f"⚠️  No USDA data found for {commodity}/{category} - using sample data")
                    if not self.use_sample_data:  # Only switch once
                        self.use_sample_data = True
                    return self.generate_sample_data(commodity, category)

        except Exception as e:
            print(f"USDA Cold Storage fetch error for {commodity}/{category}: {e}")
            # Fall back to sample data on error
            if not self.use_sample_data:
                self.use_sample_data = True
                print(f"⚠️  Switching to sample data mode due to API error")
            return self.generate_sample_data(commodity, category)

        return {'current': 0, 'history': [], 'dates': [], 'avg_5yr': 0, 'vs_avg': 0}

    def get_cold_storage_snapshot(self):
        """
        Get comprehensive cold storage data across ALL categories

        DATA SOURCE: USDA NASS Cold Storage Report (monthly)
        - Most authoritative source for US frozen food inventory
        - Published around 20th of each month for prior month data
        """
        print("🧊 FETCHING COMPLETE USDA COLD STORAGE DATA...")

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
        pork_total_data = self.fetch_usda_cold_storage('PORK')
        pork_total = pork_total_data.get('current', 0)
        if pork_total == 0:
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
        chicken_breast = self.fetch_usda_cold_storage('CHICKEN', 'BREAST')
        chicken_wing = self.fetch_usda_cold_storage('CHICKEN', 'WING')
        chicken_leg = self.fetch_usda_cold_storage('CHICKEN', 'LEG QUARTERS')

        turkey_total = self.fetch_usda_cold_storage('TURKEY')
        turkey_whole = self.fetch_usda_cold_storage('TURKEY', 'WHOLE')
        turkey_parts = self.fetch_usda_cold_storage('TURKEY', 'PARTS')
        turkey_breast = self.fetch_usda_cold_storage('TURKEY', 'BREAST')

        poultry_total = chicken_total.get('current', 0) + turkey_total.get('current', 0)
        print(f"    Total Poultry: {poultry_total/1000:.1f}M lbs")

        # === DAIRY PRODUCTS ===
        print("  🧈 Fetching dairy inventory...")
        butter = self.fetch_usda_cold_storage('BUTTER')
        cheese = self.fetch_usda_cold_storage('CHEESE')
        cheese_american = self.fetch_usda_cold_storage('CHEESE', 'AMERICAN')
        cheese_cheddar = self.fetch_usda_cold_storage('CHEESE', 'CHEDDAR')
        cheese_swiss = self.fetch_usda_cold_storage('CHEESE', 'SWISS')
        cheese_other = self.fetch_usda_cold_storage('CHEESE', 'OTHER')
        dairy_total = butter.get('current', 0) + cheese.get('current', 0)
        print(f"    Total Dairy: {dairy_total/1000:.1f}M lbs")

        # === FROZEN FRUITS ===
        print("  🍓 Fetching frozen fruit inventory...")
        fruit_strawberries = self.fetch_usda_cold_storage('STRAWBERRIES')
        fruit_blueberries = self.fetch_usda_cold_storage('BLUEBERRIES')
        fruit_raspberries = self.fetch_usda_cold_storage('RASPBERRIES')
        fruit_blackberries = self.fetch_usda_cold_storage('BLACKBERRIES')
        fruit_cherries = self.fetch_usda_cold_storage('CHERRIES')
        fruit_apples = self.fetch_usda_cold_storage('APPLES', 'FROZEN')
        fruit_peaches = self.fetch_usda_cold_storage('PEACHES', 'FROZEN')
        fruit_grapes = self.fetch_usda_cold_storage('GRAPES', 'FROZEN')
        fruit_total = (fruit_strawberries.get('current', 0) + fruit_blueberries.get('current', 0) +
                      fruit_raspberries.get('current', 0) + fruit_blackberries.get('current', 0) +
                      fruit_cherries.get('current', 0) + fruit_apples.get('current', 0) +
                      fruit_peaches.get('current', 0) + fruit_grapes.get('current', 0))
        print(f"    Total Frozen Fruit: {fruit_total/1000:.1f}M lbs")

        # === FROZEN VEGETABLES ===
        print("  🥦 Fetching frozen vegetable inventory...")
        veg_peas = self.fetch_usda_cold_storage('PEAS', 'FROZEN')
        veg_corn = self.fetch_usda_cold_storage('CORN', 'FROZEN')
        veg_green_beans = self.fetch_usda_cold_storage('BEANS', 'GREEN, FROZEN')
        veg_lima_beans = self.fetch_usda_cold_storage('BEANS', 'LIMA, FROZEN')
        veg_carrots = self.fetch_usda_cold_storage('CARROTS', 'FROZEN')
        veg_broccoli = self.fetch_usda_cold_storage('BROCCOLI')
        veg_cauliflower = self.fetch_usda_cold_storage('CAULIFLOWER', 'FROZEN')
        veg_spinach = self.fetch_usda_cold_storage('SPINACH', 'FROZEN')
        veg_mixed = self.fetch_usda_cold_storage('VEGETABLES', 'MIXED, FROZEN')
        veg_potatoes_fries = self.fetch_usda_cold_storage('POTATOES', 'FRENCH FRIED')
        veg_potatoes_other = self.fetch_usda_cold_storage('POTATOES', 'OTHER FROZEN')
        veg_onions = self.fetch_usda_cold_storage('ONIONS', 'FROZEN')
        veg_total = (veg_peas.get('current', 0) + veg_corn.get('current', 0) +
                    veg_green_beans.get('current', 0) + veg_lima_beans.get('current', 0) +
                    veg_carrots.get('current', 0) + veg_broccoli.get('current', 0) +
                    veg_cauliflower.get('current', 0) + veg_spinach.get('current', 0) +
                    veg_mixed.get('current', 0) + veg_potatoes_fries.get('current', 0) +
                    veg_potatoes_other.get('current', 0) + veg_onions.get('current', 0))
        print(f"    Total Frozen Vegetables: {veg_total/1000:.1f}M lbs")

        # === FROZEN JUICES ===
        print("  🍊 Fetching frozen juice inventory...")
        juice_orange = self.fetch_usda_cold_storage('ORANGES', 'JUICE CONCENTRATE')
        juice_grapefruit = self.fetch_usda_cold_storage('GRAPEFRUIT', 'JUICE')
        juice_apple = self.fetch_usda_cold_storage('APPLES', 'JUICE CONCENTRATE')
        juice_grape = self.fetch_usda_cold_storage('GRAPES', 'JUICE')
        juice_total = (juice_orange.get('current', 0) + juice_grapefruit.get('current', 0) +
                      juice_apple.get('current', 0) + juice_grape.get('current', 0))
        print(f"    Total Frozen Juice: {juice_total/1000:.1f}M lbs")

        # === SEAFOOD/FISH ===
        print("  🐟 Fetching seafood inventory...")
        fish_total = self.fetch_usda_cold_storage('FISH')
        fish_fillets = self.fetch_usda_cold_storage('FISH', 'FILLETS')
        fish_shellfish = self.fetch_usda_cold_storage('SHELLFISH')
        fish_shrimp = self.fetch_usda_cold_storage('SHRIMP')
        seafood_total = (fish_total.get('current', 0) + fish_shellfish.get('current', 0) +
                        fish_shrimp.get('current', 0))
        if seafood_total == 0:
            seafood_total = fish_total.get('current', 0)
        print(f"    Total Seafood: {seafood_total/1000:.1f}M lbs")

        # === EGGS ===
        print("  🥚 Fetching egg inventory...")
        eggs_shell = self.fetch_usda_cold_storage('EGGS', 'SHELL')
        eggs_frozen = self.fetch_usda_cold_storage('EGGS', 'FROZEN')
        eggs_dried = self.fetch_usda_cold_storage('EGGS', 'DRIED')
        eggs_total = (eggs_shell.get('current', 0) + eggs_frozen.get('current', 0) +
                     eggs_dried.get('current', 0))
        print(f"    Total Eggs: {eggs_total/1000:.1f}M lbs")

        # === TOTALS ===
        red_meat_total = pork_total + beef_total.get('current', 0)
        grand_total = (red_meat_total + poultry_total + dairy_total + fruit_total +
                      veg_total + juice_total + seafood_total + eggs_total)

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
                'chicken_breast': chicken_breast,
                'chicken_wing': chicken_wing,
                'chicken_leg': chicken_leg,
                'turkey': turkey_total,
                'turkey_whole': turkey_whole,
                'turkey_parts': turkey_parts,
                'turkey_breast': turkey_breast
            },
            'dairy': {
                'total': dairy_total,
                'butter': butter,
                'cheese': cheese,
                'cheese_american': cheese_american,
                'cheese_cheddar': cheese_cheddar,
                'cheese_swiss': cheese_swiss,
                'cheese_other': cheese_other
            },
            'fruits': {
                'total': fruit_total,
                'strawberries': fruit_strawberries,
                'blueberries': fruit_blueberries,
                'raspberries': fruit_raspberries,
                'blackberries': fruit_blackberries,
                'cherries': fruit_cherries,
                'apples': fruit_apples,
                'peaches': fruit_peaches,
                'grapes': fruit_grapes
            },
            'vegetables': {
                'total': veg_total,
                'peas': veg_peas,
                'corn': veg_corn,
                'green_beans': veg_green_beans,
                'lima_beans': veg_lima_beans,
                'carrots': veg_carrots,
                'broccoli': veg_broccoli,
                'cauliflower': veg_cauliflower,
                'spinach': veg_spinach,
                'mixed': veg_mixed,
                'fries': veg_potatoes_fries,
                'potatoes_other': veg_potatoes_other,
                'onions': veg_onions
            },
            'juices': {
                'total': juice_total,
                'orange': juice_orange,
                'grapefruit': juice_grapefruit,
                'apple': juice_apple,
                'grape': juice_grape
            },
            'seafood': {
                'total': seafood_total,
                'fish': fish_total,
                'fillets': fish_fillets,
                'shellfish': fish_shellfish,
                'shrimp': fish_shrimp
            },
            'eggs': {
                'total': eggs_total,
                'shell': eggs_shell,
                'frozen': eggs_frozen,
                'dried': eggs_dried
            },
            'totals': {
                'red_meat': red_meat_total,
                'poultry': poultry_total,
                'dairy': dairy_total,
                'fruits': fruit_total,
                'vegetables': veg_total,
                'juices': juice_total,
                'seafood': seafood_total,
                'eggs': eggs_total,
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

    def get_status(self, vs_avg):
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

    def calculate_metrics(self):
        """Analyze cold storage inventory levels and trends"""
        print(f"🧊 ANALYZING COMPLETE COLD STORAGE: {self.storage_data['timestamp']}")

        # Helper function
        def m(val):
            """Convert to millions"""
            return val / 1_000_000

        # === EXTRACT ALL DATA ===
        pork = self.storage_data['pork']
        beef = self.storage_data['beef']
        poultry = self.storage_data['poultry']
        dairy = self.storage_data['dairy']
        fruits = self.storage_data['fruits']
        vegetables = self.storage_data['vegetables']
        juices = self.storage_data['juices']
        seafood = self.storage_data['seafood']
        eggs = self.storage_data['eggs']
        totals = self.storage_data['totals']

        return {
            'meta': {'time': self.storage_data['timestamp']},

            # 1. GRAND OVERVIEW
            'overview': {
                "GRAND TOTAL INVENTORY": {
                    "val": f"{m(totals['grand_total']):.0f}M", "unit": "lbs", "status": "ALL CATEGORIES",
                    "insight": f"Total frozen food inventory: {m(totals['grand_total']):.0f}M lbs across ALL major categories. USDA monthly cold storage report."
                },
                "RED MEAT (PORK + BEEF)": {
                    "val": f"{m(totals['red_meat']):.0f}M", "unit": "lbs", "status": "COMBINED",
                    "insight": f"Pork: {m(pork['total']):.0f}M ({m(pork['total'])/m(totals['red_meat'])*100 if totals['red_meat'] > 0 else 0:.0f}%), Beef: {m(beef['total'].get('current',0)):.0f}M ({m(beef['total'].get('current',0))/m(totals['red_meat'])*100 if totals['red_meat'] > 0 else 0:.0f}%)."
                },
                "POULTRY (CHICKEN + TURKEY)": {
                    "val": f"{m(totals['poultry']):.0f}M", "unit": "lbs", "status": "HIGH VOLUME",
                    "insight": f"Chicken: {m(poultry['chicken'].get('current',0)):.0f}M, Turkey: {m(poultry['turkey'].get('current',0)):.0f}M. Fast turnover protein."
                },
                "DAIRY (BUTTER + CHEESE)": {
                    "val": f"{m(totals['dairy']):.0f}M", "unit": "lbs", "status": "PRICE SENSITIVE",
                    "insight": f"Butter: {m(dairy['butter'].get('current',0)):.0f}M, Cheese: {m(dairy['cheese'].get('current',0)):.0f}M. Retail price discovery."
                },
                "FROZEN FRUITS": {
                    "val": f"{m(totals['fruits']):.0f}M", "unit": "lbs", "status": "BERRIES HEAVY",
                    "insight": f"Berries, cherries, apples, peaches. Smoothie boom driving demand. Import heavy (Chile, Mexico)."
                },
                "FROZEN VEGETABLES": {
                    "val": f"{m(totals['vegetables']):.0f}M", "unit": "lbs", "status": "STAPLE FOODS",
                    "insight": f"Peas, corn, beans, fries, etc. Retail + foodservice. French fries = largest volume single item."
                },
                "FROZEN JUICES": {
                    "val": f"{m(totals['juices']):.0f}M", "unit": "lbs", "status": "DECLINING TREND",
                    "insight": f"Orange juice concentrate dominant. Category declining (shift to fresh/not-from-concentrate)."
                },
                "SEAFOOD/FISH": {
                    "val": f"{m(totals['seafood']):.0f}M", "unit": "lbs", "status": "IMPORT HEAVY",
                    "insight": f"Fish fillets, shrimp, shellfish. Mostly imported (Vietnam, India, China, Thailand)."
                },
                "EGGS": {
                    "val": f"{m(totals['eggs']):.0f}M", "unit": "lbs", "status": "BREAKER STOCK",
                    "insight": f"Shell eggs, frozen liquid, dried. Bakery/food manufacturing demand driver."
                }
            },

            # 2. PORK DETAIL
            'pork': self._build_pork_metrics(pork),

            # 3. BEEF DETAIL
            'beef': self._build_beef_metrics(beef),

            # 4. CHICKEN DETAIL
            'chicken': self._build_chicken_metrics(poultry),

            # 5. TURKEY DETAIL
            'turkey': self._build_turkey_metrics(poultry),

            # 6. DAIRY DETAIL
            'dairy': self._build_dairy_metrics(dairy),

            # 7. FROZEN FRUITS
            'fruits': self._build_fruit_metrics(fruits),

            # 8. FROZEN VEGETABLES
            'vegetables': self._build_veg_metrics(vegetables),

            # 9. FROZEN JUICES
            'juices': self._build_juice_metrics(juices),

            # 10. SEAFOOD
            'seafood': self._build_seafood_metrics(seafood),

            # 11. EGGS
            'eggs': self._build_egg_metrics(eggs),

            # Historical data for charts
            'historical': {
                'pork_belly': pork['belly'],
                'pork_total': pork['total_data'],
                'beef_total': beef['total'],
                'chicken_total': poultry['chicken'],
                'turkey_total': poultry['turkey'],
                'butter': dairy['butter'],
                'cheese': dairy['cheese'],
                'strawberries': fruits['strawberries'],
                'corn': vegetables['corn'],
                'fries': vegetables['fries'],
                'orange_juice': juices['orange']
            }
        }

    def _build_pork_metrics(self, pork):
        m = lambda x: x / 1_000_000
        return {
            "PORK TOTAL": {
                "val": f"{m(pork['total']):.0f}M", "unit": "lbs",
                "status": self.get_status(pork['total_data'].get('vs_avg', 0)),
                "insight": f"All pork: {m(pork['total']):.0f}M lbs. vs 5-yr avg: {pork['total_data'].get('vs_avg', 0):+.1f}%. Bellies, hams, loins, butts, etc."
            },
            "BELLIES (BACON)": {
                "val": f"{m(pork['belly'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(pork['belly'].get('vs_avg', 0)),
                "insight": f"Belly {m(pork['belly'].get('current',0)):.1f}M vs avg {m(pork['belly'].get('avg_5yr',0)):.1f}M ({pork['belly'].get('vs_avg',0):+.1f}%). CRITICAL - bacon pricing driver."
            },
            "HAMS": {
                "val": f"{m(pork['ham'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(pork['ham'].get('vs_avg', 0)),
                "insight": f"Ham {m(pork['ham'].get('current',0)):.1f}M ({pork['ham'].get('vs_avg',0):+.1f}% vs avg). Easter/summer build. Mexico export."
            },
            "LOINS": {
                "val": f"{m(pork['loin'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(pork['loin'].get('vs_avg', 0)),
                "insight": f"Loin {m(pork['loin'].get('current',0)):.1f}M ({pork['loin'].get('vs_avg',0):+.1f}%). Premium - chops, roasts, tenderloins."
            },
            "BUTTS + PICNICS": {
                "val": f"{m(pork['butt'].get('current',0) + pork['picnic'].get('current',0)):.1f}M", "unit": "lbs", "status": "SHOULDERS",
                "insight": f"Butt {m(pork['butt'].get('current',0)):.1f}M, Picnic {m(pork['picnic'].get('current',0)):.1f}M. Pulled pork, ground, export."
            },
            "SPARERIBS": {
                "val": f"{m(pork['spareribs'].get('current', 0)):.1f}M", "unit": "lbs", "status": "SEASONAL",
                "insight": f"Ribs {m(pork['spareribs'].get('current',0)):.1f}M. Grilling season demand. Asian market strong."
            },
            "TRIMMINGS": {
                "val": f"{m(pork['trim'].get('current', 0)):.1f}M", "unit": "lbs", "status": "PROCESSING",
                "insight": f"Trim {m(pork['trim'].get('current',0)):.1f}M. Sausage, pepperoni, ground pork raw material."
            }
        }

    def _build_beef_metrics(self, beef):
        m = lambda x: x / 1_000_000
        return {
            "BEEF TOTAL": {
                "val": f"{m(beef['total'].get('current', 0)):.0f}M", "unit": "lbs",
                "status": self.get_status(beef['total'].get('vs_avg', 0)),
                "insight": f"All beef: {m(beef['total'].get('current',0)):.0f}M ({beef['total'].get('vs_avg',0):+.1f}% vs avg). Lower inventory than pork (higher price)."
            },
            "BONELESS BEEF": {
                "val": f"{m(beef['boneless'].get('current', 0)):.1f}M", "unit": "lbs", "status": "PREMIUM",
                "insight": f"Boneless {m(beef['boneless'].get('current',0)):.1f}M. Ground beef, steaks, roasts. Fast turnover."
            },
            "BONE-IN BEEF": {
                "val": f"{m(beef['bone_in'].get('current', 0)):.1f}M", "unit": "lbs", "status": "STEAKHOUSE",
                "insight": f"Bone-in {m(beef['bone_in'].get('current',0)):.1f}M. Ribs, T-bones, porterhouse. Premium grilling."
            }
        }

    def _build_chicken_metrics(self, poultry):
        m = lambda x: x / 1_000_000
        return {
            "CHICKEN TOTAL": {
                "val": f"{m(poultry['chicken'].get('current', 0)):.0f}M", "unit": "lbs",
                "status": self.get_status(poultry['chicken'].get('vs_avg', 0)),
                "insight": f"All chicken: {m(poultry['chicken'].get('current',0)):.0f}M ({poultry['chicken'].get('vs_avg',0):+.1f}%). QSR demand giant."
            },
            "WHOLE BIRDS": {
                "val": f"{m(poultry['chicken_whole'].get('current', 0)):.1f}M", "unit": "lbs", "status": "RETAIL",
                "insight": f"Whole chickens {m(poultry['chicken_whole'].get('current',0)):.1f}M. Rotisserie, roasting. Lower margin."
            },
            "CHICKEN PARTS": {
                "val": f"{m(poultry['chicken_parts'].get('current', 0)):.1f}M", "unit": "lbs", "status": "FOODSERVICE",
                "insight": f"Parts {m(poultry['chicken_parts'].get('current',0)):.1f}M. Breasts, wings, thighs. QSR heavy."
            },
            "BREASTS": {
                "val": f"{m(poultry['chicken_breast'].get('current', 0)):.1f}M", "unit": "lbs", "status": "PREMIUM",
                "insight": f"Breast meat {m(poultry['chicken_breast'].get('current',0)):.1f}M. Highest value. Health-conscious consumer."
            },
            "WINGS": {
                "val": f"{m(poultry['chicken_wing'].get('current', 0)):.1f}M", "unit": "lbs", "status": "SPORTS BARS",
                "insight": f"Wings {m(poultry['chicken_wing'].get('current',0)):.1f}M. Super Bowl spike. Volatile pricing."
            }
        }

    def _build_turkey_metrics(self, poultry):
        m = lambda x: x / 1_000_000
        return {
            "TURKEY TOTAL": {
                "val": f"{m(poultry['turkey'].get('current', 0)):.0f}M", "unit": "lbs",
                "status": self.get_status(poultry['turkey'].get('vs_avg', 0)),
                "insight": f"All turkey: {m(poultry['turkey'].get('current',0)):.0f}M ({poultry['turkey'].get('vs_avg',0):+.1f}%). EXTREME SEASONALITY - Thanksgiving!"
            },
            "WHOLE TURKEYS": {
                "val": f"{m(poultry['turkey_whole'].get('current', 0)):.1f}M", "unit": "lbs", "status": "THANKSGIVING",
                "insight": f"Whole birds {m(poultry['turkey_whole'].get('current',0)):.1f}M. Peak Oct-Nov, crash Jan-Mar. Holiday driver."
            },
            "TURKEY PARTS": {
                "val": f"{m(poultry['turkey_parts'].get('current', 0)):.1f}M", "unit": "lbs", "status": "YEAR-ROUND",
                "insight": f"Parts {m(poultry['turkey_parts'].get('current',0)):.1f}M. Deli meat, ground turkey. Steadier demand."
            }
        }

    def _build_dairy_metrics(self, dairy):
        m = lambda x: x / 1_000_000
        return {
            "BUTTER": {
                "val": f"{m(dairy['butter'].get('current', 0)):.0f}M", "unit": "lbs",
                "status": self.get_status(dairy['butter'].get('vs_avg', 0)),
                "insight": f"Butter {m(dairy['butter'].get('current',0)):.0f}M ({dairy['butter'].get('vs_avg',0):+.1f}%). PRICE SPIKE RISK when <250M. Holiday baking."
            },
            "CHEESE TOTAL": {
                "val": f"{m(dairy['cheese'].get('current', 0)):.0f}M", "unit": "lbs",
                "status": self.get_status(dairy['cheese'].get('vs_avg', 0)),
                "insight": f"All cheese {m(dairy['cheese'].get('current',0)):.0f}M ({dairy['cheese'].get('vs_avg',0):+.1f}%). CME spot market benchmark."
            },
            "AMERICAN CHEESE": {
                "val": f"{m(dairy['cheese_american'].get('current', 0)):.1f}M", "unit": "lbs", "status": "QSR STAPLE",
                "insight": f"American {m(dairy['cheese_american'].get('current',0)):.1f}M. Burgers, sandwiches. McDonald's etc."
            },
            "CHEDDAR": {
                "val": f"{m(dairy['cheese_cheddar'].get('current', 0)):.1f}M", "unit": "lbs", "status": "VERSATILE",
                "insight": f"Cheddar {m(dairy['cheese_cheddar'].get('current',0)):.1f}M. Retail #1 cheese. Aging inventory."
            }
        }

    def _build_fruit_metrics(self, fruits):
        m = lambda x: x / 1_000_000
        return {
            "STRAWBERRIES": {
                "val": f"{m(fruits['strawberries'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(fruits['strawberries'].get('vs_avg', 0)),
                "insight": f"Strawberries {m(fruits['strawberries'].get('current',0)):.1f}M ({fruits['strawberries'].get('vs_avg',0):+.1f}%). KING of frozen fruit. Smoothie boom."
            },
            "BLUEBERRIES": {
                "val": f"{m(fruits['blueberries'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(fruits['blueberries'].get('vs_avg', 0)),
                "insight": f"Blueberries {m(fruits['blueberries'].get('current',0)):.1f}M ({fruits['blueberries'].get('vs_avg',0):+.1f}%). Health food darling. Antioxidants."
            },
            "RASPBERRIES": {
                "val": f"{m(fruits['raspberries'].get('current', 0)):.1f}M", "unit": "lbs", "status": "PREMIUM",
                "insight": f"Raspberries {m(fruits['raspberries'].get('current',0)):.1f}M. Premium berry. Delicate, expensive."
            },
            "CHERRIES": {
                "val": f"{m(fruits['cherries'].get('current', 0)):.1f}M", "unit": "lbs", "status": "PIE FILLING",
                "insight": f"Cherries {m(fruits['cherries'].get('current',0)):.1f}M. Tart cherries for pies. Sweet cherries premium."
            },
            "OTHER FRUIT (APPLES, PEACHES)": {
                "val": f"{m(fruits['apples'].get('current',0) + fruits['peaches'].get('current',0)):.1f}M", "unit": "lbs", "status": "DECLINING",
                "insight": f"Apples + Peaches. Older category declining. Consumer prefers fresh or IQF berries."
            }
        }

    def _build_veg_metrics(self, veg):
        m = lambda x: x / 1_000_000
        return {
            "FRENCH FRIES": {
                "val": f"{m(veg['fries'].get('current', 0)):.0f}M", "unit": "lbs",
                "status": self.get_status(veg['fries'].get('vs_avg', 0)),
                "insight": f"French fries {m(veg['fries'].get('current',0)):.0f}M ({veg['fries'].get('vs_avg',0):+.1f}%). LARGEST frozen veg item. McDonald's etc."
            },
            "PEAS": {
                "val": f"{m(veg['peas'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(veg['peas'].get('vs_avg', 0)),
                "insight": f"Peas {m(veg['peas'].get('current',0)):.1f}M ({veg['peas'].get('vs_avg',0):+.1f}%). Classic frozen veg. Retail side dish."
            },
            "CORN": {
                "val": f"{m(veg['corn'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(veg['corn'].get('vs_avg', 0)),
                "insight": f"Corn {m(veg['corn'].get('current',0)):.1f}M ({veg['corn'].get('vs_avg',0):+.1f}%). Sweet corn. Summer harvest freeze."
            },
            "GREEN BEANS": {
                "val": f"{m(veg['green_beans'].get('current', 0)):.1f}M", "unit": "lbs", "status": "CLASSIC",
                "insight": f"Green beans {m(veg['green_beans'].get('current',0)):.1f}M. Retail staple. Thanksgiving casserole."
            },
            "BROCCOLI": {
                "val": f"{m(veg['broccoli'].get('current', 0)):.1f}M", "unit": "lbs", "status": "HEALTHY",
                "insight": f"Broccoli {m(veg['broccoli'].get('current',0)):.1f}M. Health-conscious. Stir fry, steamed."
            },
            "MIXED VEGETABLES": {
                "val": f"{m(veg['mixed'].get('current', 0)):.1f}M", "unit": "lbs", "status": "CONVENIENCE",
                "insight": f"Mixed veg {m(veg['mixed'].get('current',0)):.1f}M. Peas/carrots/corn blends. Convenience product."
            },
            "OTHER (CARROTS, SPINACH, ETC)": {
                "val": f"{m(veg['carrots'].get('current',0) + veg['spinach'].get('current',0) + veg['cauliflower'].get('current',0)):.1f}M",
                "unit": "lbs", "status": "DIVERSE",
                "insight": f"Carrots, spinach, cauliflower combined. Diverse frozen veg options."
            }
        }

    def _build_juice_metrics(self, juices):
        m = lambda x: x / 1_000_000
        return {
            "ORANGE JUICE CONCENTRATE": {
                "val": f"{m(juices['orange'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(juices['orange'].get('vs_avg', 0)),
                "insight": f"OJ concentrate {m(juices['orange'].get('current',0)):.1f}M ({juices['orange'].get('vs_avg',0):+.1f}%). DECLINING - shift to fresh/NFC."
            },
            "GRAPEFRUIT JUICE": {
                "val": f"{m(juices['grapefruit'].get('current', 0)):.1f}M", "unit": "lbs", "status": "NICHE",
                "insight": f"Grapefruit {m(juices['grapefruit'].get('current',0)):.1f}M. Small category. Health-conscious niche."
            },
            "APPLE + GRAPE JUICE": {
                "val": f"{m(juices['apple'].get('current',0) + juices['grape'].get('current',0)):.1f}M",
                "unit": "lbs", "status": "MINOR",
                "insight": f"Apple + Grape juice. Very small frozen category. Most sold fresh/shelf-stable."
            }
        }

    def _build_seafood_metrics(self, seafood):
        m = lambda x: x / 1_000_000
        return {
            "FISH TOTAL": {
                "val": f"{m(seafood['fish'].get('current', 0)):.1f}M", "unit": "lbs",
                "status": self.get_status(seafood['fish'].get('vs_avg', 0)),
                "insight": f"All fish {m(seafood['fish'].get('current',0)):.1f}M ({seafood['fish'].get('vs_avg',0):+.1f}%). Import heavy - Vietnam, China tilapia/pangasius."
            },
            "FISH FILLETS": {
                "val": f"{m(seafood['fillets'].get('current', 0)):.1f}M", "unit": "lbs", "status": "RETAIL",
                "insight": f"Fillets {m(seafood['fillets'].get('current',0)):.1f}M. Cod, haddock, tilapia, salmon. Grocery frozen section."
            },
            "SHRIMP": {
                "val": f"{m(seafood['shrimp'].get('current', 0)):.1f}M", "unit": "lbs", "status": "IMPORTS",
                "insight": f"Shrimp {m(seafood['shrimp'].get('current',0)):.1f}M. India, Thailand, Vietnam. Farm-raised dominant."
            },
            "SHELLFISH": {
                "val": f"{m(seafood['shellfish'].get('current', 0)):.1f}M", "unit": "lbs", "status": "PREMIUM",
                "insight": f"Shellfish {m(seafood['shellfish'].get('current',0)):.1f}M. Scallops, lobster, crab. Premium pricing."
            }
        }

    def _build_egg_metrics(self, eggs):
        m = lambda x: x / 1_000_000
        return {
            "SHELL EGGS (COLD)": {
                "val": f"{m(eggs['shell'].get('current', 0)):.1f}M", "unit": "lbs", "status": "STORAGE",
                "insight": f"Shell eggs in cold storage {m(eggs['shell'].get('current',0)):.1f}M. Seasonal storage for price smoothing."
            },
            "FROZEN EGGS (LIQUID)": {
                "val": f"{m(eggs['frozen'].get('current', 0)):.1f}M", "unit": "lbs", "status": "FOOD MFG",
                "insight": f"Frozen liquid eggs {m(eggs['frozen'].get('current',0)):.1f}M. Bakery, food manufacturing. Breaking operations."
            },
            "DRIED EGG PRODUCTS": {
                "val": f"{m(eggs['dried'].get('current', 0)):.1f}M", "unit": "lbs", "status": "SHELF-STABLE",
                "insight": f"Dried eggs {m(eggs['dried'].get('current',0)):.1f}M. Powder for baking mixes, processed foods. Long shelf life."
            }
        }

    def generate_charts(self, metrics):
        """Generate comprehensive charts for all categories"""
        charts = {}
        plt.style.use('dark_background')
        hist = metrics['historical']

        # 1. PORK BELLY TREND
        if hist['pork_belly'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))
            history = [x/1_000_000 for x in hist['pork_belly']['history']]
            dates = hist['pork_belly']['dates']
            avg = hist['pork_belly']['avg_5yr'] / 1_000_000

            ax.plot(range(len(history)), history, 'o-', color='#ff6b6b', linewidth=3, markersize=8, label='Actual')
            ax.axhline(y=avg, color='#00ff88', linestyle='--', linewidth=2, label=f'5-Yr Avg ({avg:.1f}M)')
            ax.set_title('PORK BELLY INVENTORY - 12 MONTH TREND', fontsize=16, fontweight='bold', color='#ff6b6b')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Million lbs', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['belly_trend'] = ui.Image.from_data(buf.read())
            plt.close()

        # 2. MEAT COMPARISON (Pork, Beef, Chicken, Turkey)
        if all([hist['pork_total'].get('history'), hist['beef_total'].get('history'),
                hist['chicken_total'].get('history'), hist['turkey_total'].get('history')]):
            fig, ax = plt.subplots(figsize=(10, 5))
            pork = [x/1_000_000 for x in hist['pork_total']['history']]
            beef = [x/1_000_000 for x in hist['beef_total']['history']]
            chicken = [x/1_000_000 for x in hist['chicken_total']['history']]
            turkey = [x/1_000_000 for x in hist['turkey_total']['history']]
            dates = hist['pork_total']['dates']

            x = range(len(pork))
            ax.plot(x, pork, 'o-', color='#ff6b6b', linewidth=2, markersize=6, label='Pork')
            ax.plot(x, beef, 's-', color='#ff3333', linewidth=2, markersize=6, label='Beef')
            ax.plot(x, chicken, '^-', color='#ffaa00', linewidth=2, markersize=6, label='Chicken')
            ax.plot(x, turkey, 'd-', color='#ff9900', linewidth=2, markersize=6, label='Turkey')

            ax.set_title('ALL MEAT CATEGORIES - INVENTORY COMPARISON', fontsize=16, fontweight='bold')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Million lbs', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['meat_comparison'] = ui.Image.from_data(buf.read())
            plt.close()

        # 3. DAIRY (Butter vs Cheese)
        if hist['butter'].get('history') and hist['cheese'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))
            butter = [x/1_000_000 for x in hist['butter']['history']]
            cheese = [x/1_000_000 for x in hist['cheese']['history']]
            dates = hist['butter']['dates']

            x = range(len(butter))
            ax.plot(x, butter, 'o-', color='#ffdd44', linewidth=3, markersize=8, label='Butter')
            ax.plot(x, cheese, 's-', color='#0099ff', linewidth=3, markersize=8, label='Cheese')

            ax.set_title('DAIRY INVENTORY - BUTTER VS CHEESE', fontsize=16, fontweight='bold', color='#0099ff')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Million lbs', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['dairy_trend'] = ui.Image.from_data(buf.read())
            plt.close()

        # 4. FROZEN FRUITS & VEGETABLES
        if hist['strawberries'].get('history') and hist['corn'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))
            strawberries = [x/1_000_000 for x in hist['strawberries']['history']]
            corn = [x/1_000_000 for x in hist['corn']['history']]
            dates = hist['strawberries']['dates']

            x = range(len(strawberries))
            ax.plot(x, strawberries, 'o-', color='#ff1493', linewidth=3, markersize=8, label='Strawberries')
            ax.plot(x, corn, 's-', color='#32cd32', linewidth=3, markersize=8, label='Corn')

            ax.set_title('FROZEN PRODUCE - STRAWBERRIES VS CORN', fontsize=16, fontweight='bold', color='#32cd32')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Million lbs', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['produce_trend'] = ui.Image.from_data(buf.read())
            plt.close()

        # 5. FRENCH FRIES TREND
        if hist['fries'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))
            fries = [x/1_000_000 for x in hist['fries']['history']]
            dates = hist['fries']['dates']
            avg = hist['fries']['avg_5yr'] / 1_000_000

            ax.plot(range(len(fries)), fries, 'o-', color='#ffaa00', linewidth=3, markersize=8, label='Actual')
            ax.axhline(y=avg, color='#00ff88', linestyle='--', linewidth=2, label=f'5-Yr Avg ({avg:.0f}M)')

            ax.set_title('FRENCH FRIES INVENTORY - QSR BELLWETHER', fontsize=16, fontweight='bold', color='#ffaa00')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Million lbs', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['fries_trend'] = ui.Image.from_data(buf.read())
            plt.close()

        # 6. ORANGE JUICE CONCENTRATE DECLINE
        if hist['orange_juice'].get('history'):
            fig, ax = plt.subplots(figsize=(10, 5))
            oj = [x/1_000_000 for x in hist['orange_juice']['history']]
            dates = hist['orange_juice']['dates']

            ax.plot(range(len(oj)), oj, 'o-', color='#ff8c00', linewidth=3, markersize=8, label='OJ Concentrate')
            ax.set_title('ORANGE JUICE CONCENTRATE - SECULAR DECLINE', fontsize=16, fontweight='bold', color='#ff8c00')
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Million lbs', fontsize=12)
            ax.set_xticks(range(0, len(dates), 2))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), 2)], rotation=45, ha='right')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
            buf.seek(0)
            charts['oj_trend'] = ui.Image.from_data(buf.read())
            plt.close()

        return charts

# ==================================================
# DASHBOARD VIEW
# ==================================================

class ColdStorageDashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.name = 'USDA Cold Storage - Complete'
        self.data_engine = ColdStorageDataEngine()

    def refresh_data(self, sender):
        """Refresh all cold storage data and rebuild UI"""
        print("🔄 REFRESHING COMPLETE COLD STORAGE DATA...")
        self.data_engine.cache.clear()
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
        storage_data = self.data_engine.get_cold_storage_snapshot()
        analyzer = ColdStorageAnalyzer(storage_data)
        metrics = analyzer.calculate_metrics()
        charts = analyzer.generate_charts(metrics)

        cw = w - (MARGIN * 2)
        y = 40

        # HEADER
        title = ui.Label(frame=(MARGIN, y, cw, 30))
        title.text = "🧊 USDA COLD STORAGE - COMPLETE DATABASE"
        title.font = ('<system-bold>', 24)
        title.text_color = THEME['total']
        title.alignment = ui.ALIGN_CENTER
        scroll.add_subview(title)
        y += 35

        sub = ui.Label(frame=(MARGIN, y, cw, 15))
        sub.text = f"ALL CATEGORIES - MEAT, POULTRY, DAIRY, FRUITS, VEGETABLES, SEAFOOD, EGGS | {metrics['meta']['time']}"
        sub.font = ('<system>', 11)
        sub.text_color = THEME['sub']
        sub.alignment = ui.ALIGN_CENTER
        scroll.add_subview(sub)
        y += 20

        # Warning if using sample data
        if self.data_engine.use_sample_data:
            warning = ui.Label(frame=(MARGIN, y, cw, 15))
            warning.text = "⚠️  USING SAMPLE DATA - USDA API unavailable or returned no data"
            warning.font = ('<system-bold>', 10)
            warning.text_color = THEME['warn']
            warning.alignment = ui.ALIGN_CENTER
            scroll.add_subview(warning)
            y += 25
        else:
            y += 20

        # SECTIONS
        sections = [
            ("1. GRAND OVERVIEW", 'overview', THEME['total']),
            ("2. PORK PRODUCTS", 'pork', THEME['pork']),
            ("3. BEEF PRODUCTS", 'beef', THEME['beef']),
            ("4. CHICKEN PRODUCTS", 'chicken', THEME['poultry']),
            ("5. TURKEY PRODUCTS (SEASONAL)", 'turkey', THEME['poultry']),
            ("6. DAIRY PRODUCTS", 'dairy', THEME['dairy']),
            ("7. FROZEN FRUITS", 'fruits', THEME['fruit']),
            ("8. FROZEN VEGETABLES", 'vegetables', THEME['veg']),
            ("9. FROZEN JUICES", 'juices', THEME['juice']),
            ("10. SEAFOOD/FISH", 'seafood', THEME['seafood']),
            ("11. EGGS", 'eggs', THEME['eggs'])
        ]

        for section_title, section_key, color in sections:
            y = HeaderLabel.create(scroll, section_title, color, y, cw)
            for k, v in metrics[section_key].items():
                card, card_h = MetricCard.create(k, v, color, cw, y)
                scroll.add_subview(card)
                y += card_h + 15

            # Add charts after relevant sections
            if section_key == 'pork' and 'belly_trend' in charts:
                card, card_h = ChartCard.create("PORK BELLY - 12 MONTH HISTORY", charts['belly_trend'], cw, y)
                scroll.add_subview(card)
                y += card_h + 15

            if section_key == 'turkey' and 'meat_comparison' in charts:
                card, card_h = ChartCard.create("ALL MEAT CATEGORIES COMPARISON", charts['meat_comparison'], cw, y)
                scroll.add_subview(card)
                y += card_h + 15

            if section_key == 'dairy' and 'dairy_trend' in charts:
                card, card_h = ChartCard.create("BUTTER VS CHEESE TRENDS", charts['dairy_trend'], cw, y)
                scroll.add_subview(card)
                y += card_h + 15

            if section_key == 'fruits' and 'produce_trend' in charts:
                card, card_h = ChartCard.create("FROZEN PRODUCE TRENDS", charts['produce_trend'], cw, y)
                scroll.add_subview(card)
                y += card_h + 15

            if section_key == 'vegetables' and 'fries_trend' in charts:
                card, card_h = ChartCard.create("FRENCH FRIES - QSR DEMAND INDICATOR", charts['fries_trend'], cw, y)
                scroll.add_subview(card)
                y += card_h + 15

            if section_key == 'juices' and 'oj_trend' in charts:
                card, card_h = ChartCard.create("ORANGE JUICE CONCENTRATE DECLINE", charts['oj_trend'], cw, y)
                scroll.add_subview(card)
                y += card_h + 15

        scroll.content_size = (w, y + 100)

# ==================================================
# MAIN
# ==================================================

if __name__ == '__main__':
    v = ColdStorageDashboard()
    v.present('fullscreen')
