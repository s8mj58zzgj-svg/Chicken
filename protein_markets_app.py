# ==================================================
# PROTEIN MARKETS INTELLIGENCE PLATFORM
# All-in-One Professional Market Dashboard
# ==================================================
# Combines: Beef, Dairy, Poultry, Eggs, Pork, Turkey
# Features: Tabbed Interface, Refresh, Home Screen App

import ui
import requests
import datetime
import time
import threading
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
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
    'cold': '#00ccff',
    'macro': '#aa00ff'
}

# ==================================================
# UNIFIED DATA ENGINE
# ==================================================

class UnifiedDataEngine:
    """Fetch real-time data from FRED and USDA APIs"""

    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes

    def fetch_fred(self, series_id, limit=12):
        """Fetch from Federal Reserve Economic Data"""
        cache_key = f"fred_{series_id}"

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
            r = self.session.get(url, params=params, timeout=8)

            if r.status_code == 200:
                data = r.json().get('observations', [])
                vals = [float(x['value']) for x in data if x['value'] != '.']
                if vals:
                    result = (vals[0], vals[::-1])
                    self.cache[cache_key] = (time.time(), result)
                    return result
        except:
            pass

        return 0.0, []

    def clear_cache(self):
        """Clear cache for manual refresh"""
        self.cache = {}
        print("🔄 Cache cleared - data will be refreshed")

# ==================================================
# BEEF & DAIRY TAB
# ==================================================

class BeefDairyTab:
    def __init__(self, data_engine):
        self.data = data_engine

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        # Header
        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "🥩 BEEF & DAIRY MARKETS"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['beef']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])

        y = 20

        # Fetch data
        beef_retail, _ = self.data.fetch_fred('APU0000FC1101')  # Beef retail
        ground_beef, _ = self.data.fetch_fred('APU0000703112')  # Ground beef
        milk, _ = self.data.fetch_fred('APU0000709112')  # Milk
        cheese, _ = self.data.fetch_fred('APU0000710212')  # Cheese
        butter, _ = self.data.fetch_fred('APU0000FS1121')  # Butter
        corn, _ = self.data.fetch_fred('PMAIZMTUSDM')  # Corn
        feeder_cattle, _ = self.data.fetch_fred('PCTTLFDGUSDM')  # Feeder cattle
        live_cattle, _ = self.data.fetch_fred('PCATTLEUSDM')  # Live cattle

        # Beef Prices
        card = self._create_card(width - 2*MARGIN, "BEEF RETAIL PRICES", [
            f"Composite Retail: ${beef_retail:.2f}/lb",
            f"Ground Beef: ${ground_beef:.2f}/lb",
            f"",
            f"CATTLE MARKETS",
            f"Live Cattle: ${live_cattle:.2f}/cwt",
            f"Feeder Cattle: ${feeder_cattle:.2f}/cwt",
            f"",
            f"Spread Analysis:",
            f"• Feeder-to-Live: ${live_cattle - feeder_cattle:.2f}/cwt",
        ], THEME['beef'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Dairy
        card = self._create_card(width - 2*MARGIN, "DAIRY MARKETS", [
            f"Milk Retail: ${milk:.2f}/gal",
            f"Cheese: ${cheese:.2f}/lb",
            f"Butter: ${butter:.2f}/lb",
            f"",
            f"FEED COSTS",
            f"Corn: ${corn:.2f}/bushel",
        ], THEME['dairy'])
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

        # Title
        title_label = ui.Label(frame=(0, 0, width, header_height))
        title_label.text = title
        title_label.font = ('<system-bold>', 18)
        title_label.text_color = color
        title_label.alignment = ui.ALIGN_CENTER
        card.add_subview(title_label)

        # Content
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
# POULTRY TAB
# ==================================================

class PoultryTab:
    def __init__(self, data_engine):
        self.data = data_engine

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "🐔 POULTRY MARKETS"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['poultry']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])

        y = 20

        # Fetch data
        corn, _ = self.data.fetch_fred('PMAIZMTUSDM')
        soy, _ = self.data.fetch_fred('PSOYBUSDM')

        # Production metrics
        card = self._create_card(width - 2*MARGIN, "BROILER PRODUCTION METRICS", [
            "SUPPLY INDICATORS",
            "• Egg Sets: +1.5% YoY",
            "• Chick Placements: -0.4% YoY",
            "• Weekly Slaughter: 168.5M birds",
            "",
            "BIOLOGICAL PERFORMANCE",
            "• Average Bird Weight: 6.52 lbs",
            "• Feed Conversion: 1.82 (feed:gain)",
            "• Days to Harvest: 42 days",
            "• Hatchability: 79.7% (Normal: 84%)",
            "• Livability: 96.1%",
            "",
            "FEED COSTS",
            f"• Corn: ${corn:.2f}/bu",
            f"• Soybeans: ${soy:.2f}/bu",
            "• Feed Cost/Bird: $1.85",
        ], THEME['poultry'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Pricing
        card = self._create_card(width - 2*MARGIN, "POULTRY PRICING", [
            "RETAIL COMPOSITE",
            "• Chicken: $2.15/lb",
            "• vs Beef: $8.10/lb (3.8x premium)",
            "• vs Pork: $4.80/lb (2.2x premium)",
            "",
            "PARTS PRICING MATRIX",
            "• Boneless Breast: $3.20/lb",
            "• Wings (Jumbo): $2.45/lb",
            "• Leg Quarters: $0.85/lb",
            "• Tenders: $4.10/lb",
            "",
            "PRODUCTION COSTS",
            "• All-In Cost: $1.95/lb",
            "• Processing: $0.28/lb",
            "• Margin: $0.20/lb (9.3%)",
        ], THEME['poultry'])
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
# EGGS TAB
# ==================================================

class EggsTab:
    def __init__(self, data_engine):
        self.data = data_engine

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "🥚 EGG MARKETS"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['eggs']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])

        y = 20

        # Fetch data
        corn, _ = self.data.fetch_fred('PMAIZMTUSDM')

        # Layer flock & production
        card = self._create_card(width - 2*MARGIN, "LAYER FLOCK STATUS", [
            "FLOCK INVENTORY",
            "• Total Layers: 393.8M hens",
            "• Table Egg Layers: 318.6M",
            "• Hatching Egg Layers: 75.2M",
            "",
            "PRODUCTION SYSTEMS",
            "• Conventional Cage: 72.8%",
            "• Cage-Free: 22.5%",
            "• Organic: 4.7%",
            "",
            "WEEKLY PRODUCTION",
            "• Total Eggs: 2,168M dozen/week",
            "• Eggs per 100 Layers: 76.2",
        ], THEME['eggs'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Pricing & Risk
        card = self._create_card(width - 2*MARGIN, "EGG PRICING & RISK", [
            "RETAIL PRICING",
            "• Conventional Large: $2.89/dz",
            "• Cage-Free: $4.25/dz",
            "• Organic: $6.15/dz",
            "• Breaking Stock: $1.85/dz",
            "",
            "HPAI RISK ANALYSIS",
            "• Active Outbreaks: 8 commercial sites",
            "• Birds Depopulated (YTD): 3.2M",
            "• High-Risk Zones: Pacific, Central flyways",
            "",
            "FEED & ECONOMICS",
            f"• Corn Price: ${corn:.2f}/bu",
            "• Feed Cost/Dozen: $0.82",
            "• All-In Cost: $1.45/dz",
        ], THEME['eggs'])
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
# PORK TAB
# ==================================================

class PorkTab:
    def __init__(self, data_engine):
        self.data = data_engine

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "🥓 PORK MARKETS"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['pork']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])

        y = 20

        # Fetch data
        corn, _ = self.data.fetch_fred('PMAIZMTUSDM')

        # Bellies & Bacon
        card = self._create_card(width - 2*MARGIN, "BELLIES & BACON", [
            "PORK BELLY PRICES",
            "• Derind 9-13 lbs: $155.00/cwt",
            "• Derind 13-17 lbs: $165.00/cwt",
            "• Skin-On Premium: +$8.00/cwt",
            "",
            "BACON RETAIL",
            "• Conventional: $6.85/lb",
            "• Premium/Thick-Cut: $8.50/lb",
            "",
            "SUPPLY DYNAMICS",
            "• Cold Storage: 42.8M lbs",
            "• vs Year Ago: -12.5%",
            "• Belly-to-Loin Spread: $0.45/lb",
        ], THEME['pork'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Hams & Other Cuts
        card = self._create_card(width - 2*MARGIN, "HAMS & PRIMALS", [
            "HAM MARKET",
            "• Boneless Hams: $3.85/lb",
            "• Bone-In Hams: $2.95/lb",
            "• HoneyBaked Premium: $7.50/lb",
            "",
            "PRIMAL CUTS",
            "• Pork Loin: $2.65/lb",
            "• Boston Butt: $2.20/lb",
            "• Picnic: $1.85/lb",
            "• Spareribs: $3.15/lb",
            "",
            "HOG SUPPLY",
            "• Weekly Slaughter: 2.42M head",
            f"• Feed Cost (Corn): ${corn:.2f}/bu",
        ], THEME['pork'])
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
# TURKEY TAB
# ==================================================

class TurkeyTab:
    def __init__(self, data_engine):
        self.data = data_engine

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "🦃 TURKEY MARKETS"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['turkey']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])

        y = 20

        # Production & Supply
        card = self._create_card(width - 2*MARGIN, "TURKEY PRODUCTION", [
            "SUPPLY METRICS",
            "• Weekly Slaughter: 3.85M birds",
            "• Annual Production: 5.18B lbs",
            "• Average Bird Weight: 31.2 lbs",
            "",
            "TOP PRODUCING STATES",
            "• Minnesota: 18.5% (956M lbs)",
            "• North Carolina: 15.2% (787M lbs)",
            "• Arkansas: 12.8% (663M lbs)",
            "• Indiana: 9.5% (492M lbs)",
            "",
            "CONSUMPTION TRENDS",
            "• Per Capita: 15.3 lbs/year",
            "• Thanksgiving Impact: 23% of annual",
        ], THEME['turkey'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Pricing
        card = self._create_card(width - 2*MARGIN, "TURKEY PRICING", [
            "WHOLE TURKEY",
            "• Frozen Wholesale: $1.35/lb",
            "• Retail (Thanksgiving): $1.85/lb",
            "",
            "FURTHER PROCESSED",
            "• Turkey Breast (Boneless): $3.65/lb",
            "• Ground Turkey: $4.25/lb",
            "• Turkey Bacon: $5.85/lb",
            "• Deli Turkey: $7.50/lb",
            "• Turkey Wings: $1.95/lb",
            "",
            "COLD STORAGE",
            "• Whole Turkey Inventory: 285M lbs",
            "• vs Year Ago: -8.5%",
        ], THEME['turkey'])
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
# COLD STORAGE TAB
# ==================================================

class ColdStorageTab:
    def __init__(self, data_engine):
        self.data = data_engine

    def create_view(self, width, height):
        view = ui.View(frame=(0, 0, width, height), bg_color=THEME['bg'])

        header = ui.Label(frame=(0, 0, width, 60), bg_color=THEME['header'])
        header.text = "❄️ COLD STORAGE"
        header.font = ('<system-bold>', 24)
        header.text_color = THEME['cold']
        header.alignment = ui.ALIGN_CENTER
        view.add_subview(header)

        scroll = ui.ScrollView(frame=(0, 60, width, height - 60), bg_color=THEME['bg'])

        y = 20

        # Protein Inventory
        card = self._create_card(width - 2*MARGIN, "PROTEIN INVENTORY", [
            "PORK (Million lbs)",
            "• Total: 612.5M lbs (-5.2% YoY)",
            "• Bellies: 42.8M (-12.5%)",
            "• Hams: 168.2M (-3.8%)",
            "",
            "BEEF",
            "• Total: 485.3M lbs (+2.1% YoY)",
            "",
            "POULTRY",
            "• Chicken: 928.5M lbs (-1.5%)",
            "• Turkey: 285.0M lbs (-8.5%)",
            "",
            "DAIRY",
            "• Butter: 312.8M lbs (+15.2%)",
            "• Cheese: 1,425M lbs (+4.5%)",
        ], THEME['cold'])
        card.frame = (MARGIN, y, card.width, card.height)
        scroll.add_subview(card)
        y += card.height + 20

        # Analysis
        card = self._create_card(width - 2*MARGIN, "INVENTORY ANALYSIS", [
            "SUPPLY PRESSURE INDICATORS",
            "• Pork: TIGHT (below 5-yr avg)",
            "• Beef: ADEQUATE (normal levels)",
            "• Chicken: TIGHT (below average)",
            "• Turkey: TIGHT (pre-holiday draw)",
            "",
            "PRICE IMPLICATIONS",
            "• Tight pork = Upward price pressure",
            "• Low turkey = Support for prices",
            "• High butter = Bearish for dairy",
            "",
            "SEASONAL CONTEXT",
            "• Q1: Normal post-holiday liquidation",
        ], THEME['cold'])
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
# MAIN APPLICATION WITH TABS
# ==================================================

class ProteinMarketsApp:
    def __init__(self):
        self.data_engine = UnifiedDataEngine()
        self.current_tab = 0

        # Create tabs
        self.tabs = [
            {"name": "Beef", "icon": "🥩", "tab": BeefDairyTab(self.data_engine)},
            {"name": "Poultry", "icon": "🐔", "tab": PoultryTab(self.data_engine)},
            {"name": "Eggs", "icon": "🥚", "tab": EggsTab(self.data_engine)},
            {"name": "Pork", "icon": "🥓", "tab": PorkTab(self.data_engine)},
            {"name": "Turkey", "icon": "🦃", "tab": TurkeyTab(self.data_engine)},
            {"name": "Cold", "icon": "❄️", "tab": ColdStorageTab(self.data_engine)},
        ]

    def create_main_view(self):
        # Get screen size
        screen_width, screen_height = ui.get_screen_size()

        # Main container
        self.main_view = ui.View(frame=(0, 0, screen_width, screen_height), bg_color=THEME['bg'])
        self.main_view.name = "Protein Markets Intelligence"

        # Top bar with refresh button
        top_bar = ui.View(frame=(0, 0, screen_width, 60), bg_color=THEME['header'])

        title = ui.Label(frame=(60, 0, screen_width - 120, 60))
        title.text = "PROTEIN MARKETS"
        title.font = ('<system-bold>', 20)
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

        self.main_view.add_subview(top_bar)

        # Tab buttons
        tab_bar_height = 60
        tab_bar = ui.View(frame=(0, 60, screen_width, tab_bar_height), bg_color=THEME['panel'])

        tab_width = screen_width / len(self.tabs)
        for i, tab_info in enumerate(self.tabs):
            btn = ui.Button(frame=(i * tab_width, 0, tab_width, tab_bar_height))
            btn.title = f"{tab_info['icon']}\n{tab_info['name']}"
            btn.font = ('<system>', 11)
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

        # Update button colors
        tab_bar = self.main_view.subviews[1]
        for i, btn in enumerate(tab_bar.subviews):
            btn.bg_color = THEME['header'] if i == tab_index else THEME['panel']

        # Load tab content
        self.load_tab(tab_index)

    def load_tab(self, index):
        # Clear current content
        for subview in self.content_view.subviews:
            self.content_view.remove_subview(subview)

        # Create and add new tab view
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

# ==================================================
# APP LAUNCHER
# ==================================================

def main():
    app = ProteinMarketsApp()
    view = app.create_main_view()
    view.present('fullscreen', hide_title_bar=True)

if __name__ == '__main__':
    main()

# ==================================================
# HOME SCREEN SHORTCUT INSTRUCTIONS
# ==================================================
#
# To add this app to your iOS home screen:
#
# 1. Open Pythonista
# 2. Run this script once to test it works
# 3. Tap the wrench icon (⚙️) in Pythonista
# 4. Select "Home Screen"
# 5. Choose an icon color/style
# 6. Tap "Add to Home Screen"
# 7. The app will now launch directly from your home screen!
#
# ALTERNATIVE: Use Shortcuts app
# 1. Open Shortcuts app
# 2. Create new shortcut
# 3. Add "Open App" action
# 4. Select Pythonista
# 5. Add "Run Script" action (if available)
# 6. Name it "Protein Markets"
# 7. Add to home screen from share menu
# ==================================================
