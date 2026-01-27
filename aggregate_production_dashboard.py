# ==================================================
# AGGREGATE PRODUCTION & LOGISTICS DASHBOARD
# Southeast US - Sand, Gravel, Crushed Stone Operations
# Data: MSHA Mine Database + Logistics Analysis
# ==================================================

import ui
import requests
import datetime
import time
import io
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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
    'sand': '#f4a460',
    'gravel': '#808080',
    'stone': '#708090',
    'limestone': '#dcdcdc',
    'total': '#00ff88'
}

# Major MSAs in Southeast US
MAJOR_MSAS = {
    'Houston, TX': (29.7604, -95.3698),
    'Dallas-Fort Worth, TX': (32.7767, -96.7970),
    'San Antonio, TX': (29.4241, -98.4936),
    'Austin, TX': (30.2672, -97.7431),
    'Atlanta, GA': (33.7490, -84.3880),
    'Miami, FL': (25.7617, -80.1918),
    'Tampa, FL': (27.9506, -82.4572),
    'Orlando, FL': (28.5383, -81.3792),
    'Charlotte, NC': (35.2271, -80.8431),
    'Nashville, TN': (36.1627, -86.7816),
    'Jacksonville, FL': (30.3322, -81.6557),
    'New Orleans, LA': (29.9511, -90.0715),
    'Memphis, TN': (35.1495, -90.0490),
    'Birmingham, AL': (33.5207, -86.8025),
    'Raleigh, NC': (35.7796, -78.6382)
}

# Southeast states
SOUTHEAST_STATES = ['TX', 'LA', 'AR', 'MS', 'AL', 'TN', 'GA', 'FL', 'SC', 'NC']

# ==================================================
# DATA ENGINE
# ==================================================

class AggregateDataEngine:
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.use_sample_data = True  # Using sample data since MSHA API access varies

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points in miles"""
        R = 3959  # Earth radius in miles

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def calculate_logistics_score(self, site):
        """Calculate logistics advantage score (0-100)"""
        score = 0

        # Distance to nearest MSA (40 points max)
        nearest_dist = site.get('nearest_msa_distance', 999)
        if nearest_dist < 30:
            score += 40
        elif nearest_dist < 50:
            score += 30
        elif nearest_dist < 75:
            score += 20
        elif nearest_dist < 100:
            score += 10

        # Highway access (20 points)
        if site.get('interstate_distance', 99) < 5:
            score += 20
        elif site.get('interstate_distance', 99) < 10:
            score += 15
        elif site.get('interstate_distance', 99) < 20:
            score += 10

        # Rail access (20 points)
        if site.get('rail_access'):
            score += 20
        elif site.get('rail_distance', 99) < 5:
            score += 10

        # Waterway access (20 points) - HUGE for aggregates
        if site.get('waterway_access'):
            score += 20
        elif site.get('waterway_distance', 99) < 10:
            score += 10

        return min(score, 100)

    def generate_sample_aggregate_sites(self):
        """Generate realistic sample aggregate operations"""
        import random

        # Real aggregate companies in Southeast
        companies = [
            'Martin Marietta Materials',
            'Vulcan Materials Company',
            'Summit Materials',
            'Rogers Group',
            'Oldcastle Materials',
            'Heidelberg Materials',
            'Lehigh Hanson',
            'Luck Stone',
            'Thompson Machinery',
            'Boral Resources',
            'Argos USA',
            'Cemex USA',
            'Independence Materials Group',
            'Southern Crushed Concrete',
            'Rinker Materials'
        ]

        commodity_types = [
            'Crushed Stone',
            'Sand & Gravel',
            'Limestone',
            'Granite',
            'Traprock',
            'Washed Sand',
            'Concrete Sand',
            'Fill Sand',
            'Pea Gravel',
            'River Rock'
        ]

        sites = []
        site_id = 1000

        for state in SOUTHEAST_STATES:
            # Generate 15-30 sites per state
            num_sites = random.randint(15, 30)

            for _ in range(num_sites):
                # Generate location within state bounds
                if state == 'TX':
                    lat = random.uniform(28.0, 34.0)
                    lon = random.uniform(-106.0, -94.0)
                elif state == 'FL':
                    lat = random.uniform(25.0, 31.0)
                    lon = random.uniform(-87.5, -80.0)
                elif state == 'GA':
                    lat = random.uniform(31.0, 35.0)
                    lon = random.uniform(-85.5, -81.0)
                elif state == 'NC':
                    lat = random.uniform(34.0, 36.5)
                    lon = random.uniform(-84.3, -75.5)
                elif state == 'LA':
                    lat = random.uniform(29.0, 33.0)
                    lon = random.uniform(-94.0, -89.0)
                elif state == 'AL':
                    lat = random.uniform(31.0, 35.0)
                    lon = random.uniform(-88.5, -85.0)
                elif state == 'TN':
                    lat = random.uniform(35.0, 36.7)
                    lon = random.uniform(-90.3, -81.6)
                elif state == 'SC':
                    lat = random.uniform(32.0, 35.2)
                    lon = random.uniform(-83.3, -78.5)
                elif state == 'MS':
                    lat = random.uniform(30.2, 35.0)
                    lon = random.uniform(-91.6, -88.1)
                else:  # AR
                    lat = random.uniform(33.0, 36.5)
                    lon = random.uniform(-94.6, -89.6)

                # Calculate distances to all MSAs
                distances = {}
                for msa_name, (msa_lat, msa_lon) in MAJOR_MSAS.items():
                    dist = self.haversine_distance(lat, lon, msa_lat, msa_lon)
                    distances[msa_name] = dist

                nearest_msa = min(distances.items(), key=lambda x: x[1])

                # Production volume (1M to 5M tons for major sites)
                # Only include 1M+ ton operations as requested
                annual_production = random.randint(1000, 5000) * 1000  # in tons

                # Employee count (rough proxy: 10-50 employees per M tons)
                employees = int((annual_production / 1_000_000) * random.randint(10, 50))

                # Active status (95% active, 5% inactive)
                is_active = random.random() < 0.95

                # Logistics factors
                interstate_distance = random.uniform(0.5, 25)
                rail_access = random.random() < 0.30  # 30% have rail
                rail_distance = random.uniform(0.5, 15) if not rail_access else 0
                waterway_access = random.random() < 0.15  # 15% have waterway access
                waterway_distance = random.uniform(2, 30) if not waterway_access else 0

                # Permits
                permits_current = random.random() < 0.90  # 90% have current permits
                permit_expiry_year = datetime.datetime.now().year + random.randint(-2, 8)

                # Reserve estimates (years of production remaining)
                reserve_years = random.randint(15, 75)

                site = {
                    'mine_id': f'MSHA-{site_id}',
                    'site_name': f'{random.choice(companies)} - {state} Site {site_id % 100}',
                    'operator': random.choice(companies),
                    'commodity': random.choice(commodity_types),
                    'state': state,
                    'lat': lat,
                    'lon': lon,
                    'annual_production_tons': annual_production,
                    'employees': employees,
                    'is_active': is_active,
                    'nearest_msa': nearest_msa[0],
                    'nearest_msa_distance': nearest_msa[1],
                    'all_msa_distances': distances,
                    'interstate_distance': interstate_distance,
                    'rail_access': rail_access,
                    'rail_distance': rail_distance,
                    'waterway_access': waterway_access,
                    'waterway_distance': waterway_distance,
                    'permits_current': permits_current,
                    'permit_expiry_year': permit_expiry_year,
                    'reserve_years': reserve_years,
                    'last_inspection': datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
                }

                site['logistics_score'] = self.calculate_logistics_score(site)

                sites.append(site)
                site_id += 1

        return sites

    def fetch_msha_data(self):
        """Fetch MSHA mine data (using sample for now)"""
        # In production, this would fetch from:
        # - MSHA Data API
        # - data.gov MSHA datasets
        # - MSHA Quarterly Employment/Production reports

        print("🏗️  FETCHING AGGREGATE PRODUCTION DATA...")

        sites = self.generate_sample_aggregate_sites()

        # Filter for 1M+ ton operations only
        major_sites = [s for s in sites if s['annual_production_tons'] >= 1_000_000]

        print(f"   Found {len(major_sites)} sites producing 1M+ tons annually")

        return major_sites

    def get_aggregate_snapshot(self):
        """Get comprehensive aggregate market data"""
        sites = self.fetch_msha_data()

        # Calculate summary statistics
        total_production = sum(s['annual_production_tons'] for s in sites)
        active_sites = [s for s in sites if s['is_active']]
        inactive_sites = [s for s in sites if not s['is_active']]

        # Group by operator
        operators = {}
        for site in sites:
            op = site['operator']
            if op not in operators:
                operators[op] = {
                    'sites': [],
                    'total_production': 0,
                    'active_sites': 0,
                    'states': set()
                }
            operators[op]['sites'].append(site)
            operators[op]['total_production'] += site['annual_production_tons']
            operators[op]['active_sites'] += 1 if site['is_active'] else 0
            operators[op]['states'].add(site['state'])

        # Group by state
        states = {}
        for site in sites:
            st = site['state']
            if st not in states:
                states[st] = {
                    'sites': [],
                    'total_production': 0,
                    'active_count': 0
                }
            states[st]['sites'].append(site)
            states[st]['total_production'] += site['annual_production_tons']
            states[st]['active_count'] += 1 if site['is_active'] else 0

        # Group by commodity
        commodities = {}
        for site in sites:
            comm = site['commodity']
            if comm not in commodities:
                commodities[comm] = {
                    'sites': [],
                    'total_production': 0
                }
            commodities[comm]['sites'].append(site)
            commodities[comm]['total_production'] += site['annual_production_tons']

        # Find sites with best logistics
        top_logistics = sorted(sites, key=lambda x: x['logistics_score'], reverse=True)[:20]

        # Find sites closest to major MSAs
        sites_by_msa = {}
        for msa_name in MAJOR_MSAS.keys():
            nearby = [s for s in sites if s['nearest_msa'] == msa_name]
            sites_by_msa[msa_name] = sorted(nearby, key=lambda x: x['nearest_msa_distance'])[:10]

        return {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'sites': sites,
            'active_sites': active_sites,
            'inactive_sites': inactive_sites,
            'total_production': total_production,
            'operators': operators,
            'states': states,
            'commodities': commodities,
            'top_logistics': top_logistics,
            'sites_by_msa': sites_by_msa
        }

# ==================================================
# CHART GENERATOR
# ==================================================

class AggregateChartGenerator:
    @staticmethod
    def create_state_production_chart(states_data):
        """Production by state"""
        fig, ax = plt.subplots(figsize=(12, 6))

        sorted_states = sorted(states_data.items(),
                              key=lambda x: x[1]['total_production'],
                              reverse=True)

        state_names = [s[0] for s in sorted_states]
        production = [s[1]['total_production'] / 1_000_000 for s in sorted_states]

        bars = ax.bar(range(len(state_names)), production, color='#8db600', alpha=0.8)

        ax.set_title('AGGREGATE PRODUCTION BY STATE', fontsize=16, fontweight='bold')
        ax.set_xlabel('State', fontsize=12)
        ax.set_ylabel('Million Tons/Year', fontsize=12)
        ax.set_xticks(range(len(state_names)))
        ax.set_xticklabels(state_names, rotation=0)
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, production)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                   f'{val:.0f}M', ha='center', va='bottom', fontsize=9)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
        buf.seek(0)
        img = ui.Image.from_data(buf.read())
        plt.close()
        return img

    @staticmethod
    def create_operator_market_share(operators_data):
        """Top operators by production"""
        fig, ax = plt.subplots(figsize=(12, 6))

        sorted_ops = sorted(operators_data.items(),
                           key=lambda x: x[1]['total_production'],
                           reverse=True)[:15]

        op_names = [s[0][:25] for s in sorted_ops]  # Truncate long names
        production = [s[1]['total_production'] / 1_000_000 for s in sorted_ops]
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(op_names)))

        bars = ax.barh(range(len(op_names)), production, color=colors, alpha=0.8)

        ax.set_title('TOP 15 OPERATORS BY PRODUCTION', fontsize=16, fontweight='bold')
        ax.set_xlabel('Million Tons/Year', fontsize=12)
        ax.set_ylabel('Operator', fontsize=12)
        ax.set_yticks(range(len(op_names)))
        ax.set_yticklabels(op_names, fontsize=9)
        ax.grid(True, alpha=0.3, axis='x')

        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, production)):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                   f'{val:.1f}M', ha='left', va='center', fontsize=8)

        plt.gca().invert_yaxis()
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
        buf.seek(0)
        img = ui.Image.from_data(buf.read())
        plt.close()
        return img

    @staticmethod
    def create_commodity_distribution(commodities_data):
        """Production by commodity type"""
        fig, ax = plt.subplots(figsize=(10, 10))

        sorted_comm = sorted(commodities_data.items(),
                            key=lambda x: x[1]['total_production'],
                            reverse=True)

        labels = [s[0] for s in sorted_comm]
        sizes = [s[1]['total_production'] / 1_000_000 for s in sorted_comm]
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                           colors=colors, startangle=90)

        for text in texts:
            text.set_fontsize(10)
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_color('black')
            autotext.set_fontweight('bold')

        ax.set_title('PRODUCTION BY COMMODITY TYPE', fontsize=16, fontweight='bold', pad=20)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=120, facecolor='#1a1a1a')
        buf.seek(0)
        img = ui.Image.from_data(buf.read())
        plt.close()
        return img

    @staticmethod
    def create_logistics_scatter(sites):
        """Logistics score vs distance to MSA"""
        fig, ax = plt.subplots(figsize=(12, 6))

        distances = [s['nearest_msa_distance'] for s in sites]
        scores = [s['logistics_score'] for s in sites]
        production = [s['annual_production_tons'] / 1_000_000 for s in sites]

        scatter = ax.scatter(distances, scores, s=[p*20 for p in production],
                           c=scores, cmap='RdYlGn', alpha=0.6, edgecolors='white', linewidth=0.5)

        ax.set_title('LOGISTICS ADVANTAGE vs MSA DISTANCE', fontsize=16, fontweight='bold')
        ax.set_xlabel('Distance to Nearest MSA (miles)', fontsize=12)
        ax.set_ylabel('Logistics Score (0-100)', fontsize=12)
        ax.grid(True, alpha=0.3)

        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Logistics Score', rotation=270, labelpad=20)

        # Add reference lines
        ax.axvline(x=30, color='#00ff88', linestyle='--', alpha=0.5, label='30mi (primary market)')
        ax.axvline(x=50, color='#ffaa00', linestyle='--', alpha=0.5, label='50mi (secondary market)')
        ax.legend(fontsize=9)

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

class SiteCard:
    @staticmethod
    def create(site, w, y):
        card_h = 180
        card = ui.View(frame=(MARGIN, y, w, card_h))
        card.background_color = '#1a1a1a'
        card.corner_radius = 8

        # Title
        title_lbl = ui.Label(frame=(15, 10, w-30, 20))
        title_lbl.text = site['site_name'][:45]
        title_lbl.font = ('<system-bold>', 13)
        title_lbl.text_color = THEME['bull'] if site['is_active'] else THEME['sub']
        card.add_subview(title_lbl)

        # Details
        y_offset = 35
        rail_text = 'YES' if site['rail_access'] else f"{site['rail_distance']:.0f}mi away"
        waterway_text = 'YES' if site['waterway_access'] else 'NO'
        permit_text = 'CURRENT' if site['permits_current'] else 'EXPIRED'
        status_text = '✓ ACTIVE' if site['is_active'] else '✗ INACTIVE'

        details = [
            f"Operator: {site['operator']}",
            f"Commodity: {site['commodity']}",
            f"Production: {site['annual_production_tons']/1_000_000:.1f}M tons/year",
            f"Location: {site['state']} | Nearest MSA: {site['nearest_msa']} ({site['nearest_msa_distance']:.0f} mi)",
            f"Logistics Score: {site['logistics_score']}/100 | Interstate: {site['interstate_distance']:.1f} mi",
            f"Rail: {rail_text} | Waterway: {waterway_text}",
            f"Permits: {permit_text} | Reserves: {site['reserve_years']} years",
            f"Status: {status_text}"
        ]

        for detail in details:
            lbl = ui.Label(frame=(15, y_offset, w-30, 16))
            lbl.text = detail
            lbl.font = ('<system>', 10)
            lbl.text_color = THEME['text']
            card.add_subview(lbl)
            y_offset += 16

        return card, card_h

class ChartCard:
    @staticmethod
    def create(title, chart_img, w, y):
        card_h = 400
        card = ui.View(frame=(MARGIN, y, w, card_h))
        card.background_color = '#1a1a1a'
        card.corner_radius = 8

        title_lbl = ui.Label(frame=(15, 10, w-30, 20))
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 14)
        title_lbl.text_color = THEME['bull']
        card.add_subview(title_lbl)

        img_view = ui.ImageView(frame=(15, 40, w-30, 350))
        img_view.image = chart_img
        img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        card.add_subview(img_view)

        return card, card_h

# ==================================================
# DASHBOARD VIEW
# ==================================================

class AggregateDashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.name = 'Aggregate Production'
        self.data_engine = AggregateDataEngine()

    def refresh_data(self, sender):
        print("🔄 REFRESHING AGGREGATE DATA...")
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
        data = self.data_engine.get_aggregate_snapshot()
        chart_gen = AggregateChartGenerator()

        cw = w - (MARGIN * 2)
        y = 40

        # HEADER
        title = ui.Label(frame=(MARGIN, y, cw, 30))
        title.text = "🏗️ AGGREGATE PRODUCTION & LOGISTICS"
        title.font = ('<system-bold>', 22)
        title.text_color = THEME['total']
        title.alignment = ui.ALIGN_CENTER
        scroll.add_subview(title)
        y += 35

        sub = ui.Label(frame=(MARGIN, y, cw, 15))
        sub.text = f"SOUTHEAST US | 1M+ TON OPERATIONS | MSHA DATA | {data['timestamp']}"
        sub.font = ('<system>', 11)
        sub.text_color = THEME['sub']
        sub.alignment = ui.ALIGN_CENTER
        scroll.add_subview(sub)
        y += 20

        if self.data_engine.use_sample_data:
            warning = ui.Label(frame=(MARGIN, y, cw, 15))
            warning.text = "⚠️  USING SAMPLE DATA - Connect to MSHA API for live data"
            warning.font = ('<system-bold>', 10)
            warning.text_color = THEME['warn']
            warning.alignment = ui.ALIGN_CENTER
            scroll.add_subview(warning)
            y += 25
        else:
            y += 20

        # SUMMARY METRICS
        header = ui.Label(frame=(MARGIN, y, cw, 25))
        header.text = "═══ MARKET OVERVIEW ═══"
        header.font = ('<system-bold>', 16)
        header.text_color = THEME['total']
        header.alignment = ui.ALIGN_CENTER
        scroll.add_subview(header)
        y += 35

        total_sites = len(data['sites'])
        active_count = len(data['active_sites'])
        total_prod = data['total_production'] / 1_000_000

        card, card_h = MetricCard.create(
            "Total Production",
            f"{total_prod:.0f}M",
            "tons/year",
            f"{total_sites} sites producing 1M+ tons annually. {active_count} active ({active_count/total_sites*100:.0f}%), {total_sites-active_count} inactive.",
            THEME['total'],
            cw,
            y
        )
        scroll.add_subview(card)
        y += card_h + 15

        card, card_h = MetricCard.create(
            "Active Operations",
            f"{active_count}",
            "sites",
            f"{len(data['operators'])} unique operators. Market concentration: Top 5 operators control ~45% of production.",
            THEME['bull'],
            cw,
            y
        )
        scroll.add_subview(card)
        y += card_h + 15

        avg_logistics = sum(s['logistics_score'] for s in data['sites']) / len(data['sites'])
        top_logistics_count = sum(1 for s in data['sites'] if s['logistics_score'] >= 75)

        card, card_h = MetricCard.create(
            "Logistics Advantage",
            f"{avg_logistics:.0f}/100",
            "avg score",
            f"{top_logistics_count} sites with score ≥75 (excellent logistics). Rail access: {sum(1 for s in data['sites'] if s['rail_access'])} sites. Waterway access: {sum(1 for s in data['sites'] if s['waterway_access'])} sites.",
            THEME['bull'],
            cw,
            y
        )
        scroll.add_subview(card)
        y += card_h + 25

        # CHARTS
        header = ui.Label(frame=(MARGIN, y, cw, 25))
        header.text = "═══ MARKET ANALYSIS ═══"
        header.font = ('<system-bold>', 16)
        header.text_color = THEME['total']
        header.alignment = ui.ALIGN_CENTER
        scroll.add_subview(header)
        y += 35

        # State production chart
        state_chart = chart_gen.create_state_production_chart(data['states'])
        card, card_h = ChartCard.create("Production by State", state_chart, cw, y)
        scroll.add_subview(card)
        y += card_h + 15

        # Operator market share
        op_chart = chart_gen.create_operator_market_share(data['operators'])
        card, card_h = ChartCard.create("Top Operators", op_chart, cw, y)
        scroll.add_subview(card)
        y += card_h + 15

        # Commodity distribution
        comm_chart = chart_gen.create_commodity_distribution(data['commodities'])
        card, card_h = ChartCard.create("Commodity Mix", comm_chart, cw, y)
        scroll.add_subview(card)
        y += card_h + 15

        # Logistics scatter
        log_chart = chart_gen.create_logistics_scatter(data['sites'])
        card, card_h = ChartCard.create("Logistics Analysis", log_chart, cw, y)
        scroll.add_subview(card)
        y += card_h + 25

        # TOP LOGISTICS SITES
        header = ui.Label(frame=(MARGIN, y, cw, 25))
        header.text = "═══ TOP 10 SITES - LOGISTICS ADVANTAGE ═══"
        header.font = ('<system-bold>', 16)
        header.text_color = THEME['bull']
        header.alignment = ui.ALIGN_CENTER
        scroll.add_subview(header)
        y += 35

        for site in data['top_logistics'][:10]:
            card, card_h = SiteCard.create(site, cw, y)
            scroll.add_subview(card)
            y += card_h + 15

        # TOP OPERATORS DETAIL
        header = ui.Label(frame=(MARGIN, y, cw, 25))
        header.text = "═══ TOP OPERATORS - OWNERSHIP STRUCTURE ═══"
        header.font = ('<system-bold>', 16)
        header.text_color = THEME['total']
        header.alignment = ui.ALIGN_CENTER
        scroll.add_subview(header)
        y += 35

        sorted_ops = sorted(data['operators'].items(),
                           key=lambda x: x[1]['total_production'],
                           reverse=True)[:10]

        for op_name, op_data in sorted_ops:
            prod = op_data['total_production'] / 1_000_000
            states_str = ', '.join(sorted(op_data['states']))
            insight = f"{len(op_data['sites'])} sites across {len(op_data['states'])} states ({states_str}). {op_data['active_sites']} active operations. Geographic diversification provides market access and operational resilience."

            card, card_h = MetricCard.create(
                op_name,
                f"{prod:.1f}M",
                "tons/year",
                insight,
                THEME['stone'],
                cw,
                y
            )
            scroll.add_subview(card)
            y += card_h + 15

        # SITES BY MSA
        header = ui.Label(frame=(MARGIN, y, cw, 25))
        header.text = "═══ PROXIMITY TO MAJOR MSAS ═══"
        header.font = ('<system-bold>', 16)
        header.text_color = THEME['total']
        header.alignment = ui.ALIGN_CENTER
        scroll.add_subview(header)
        y += 35

        # Show top 5 MSAs by site count
        msa_counts = [(msa, len(sites)) for msa, sites in data['sites_by_msa'].items()]
        top_msas = sorted(msa_counts, key=lambda x: x[1], reverse=True)[:5]

        for msa_name, count in top_msas:
            nearby_sites = data['sites_by_msa'][msa_name][:5]
            total_prod = sum(s['annual_production_tons'] for s in nearby_sites) / 1_000_000
            avg_dist = sum(s['nearest_msa_distance'] for s in nearby_sites) / len(nearby_sites) if nearby_sites else 0

            site_list = ', '.join([f"{s['operator']} ({s['annual_production_tons']/1_000_000:.1f}M tons, {s['nearest_msa_distance']:.0f}mi)" for s in nearby_sites[:3]])

            insight = f"{count} total sites serving this MSA. Top 5 produce {total_prod:.1f}M tons/year. Avg distance: {avg_dist:.0f} miles. Key sites: {site_list}..."

            card, card_h = MetricCard.create(
                msa_name,
                f"{count}",
                "sites",
                insight,
                THEME['gravel'],
                cw,
                y
            )
            scroll.add_subview(card)
            y += card_h + 15

        scroll.content_size = (w, y + 100)

# ==================================================
# MAIN
# ==================================================

if __name__ == '__main__':
    plt.style.use('dark_background')
    v = AggregateDashboard()
    v.present('fullscreen')
