# ==================================================
# ENHANCED AGGREGATE PRODUCTION & LOGISTICS DASHBOARD
# Interactive Maps, Site Selection, Filtering, Market Analysis
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
    'total': '#00ff88',
    'highlight': '#00ffff'
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

SOUTHEAST_STATES = ['TX', 'LA', 'AR', 'MS', 'AL', 'TN', 'GA', 'FL', 'SC', 'NC']

# ==================================================
# DATA ENGINE
# ==================================================

class AggregateDataEngine:
    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.use_sample_data = True

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
        nearest_dist = site.get('nearest_msa_distance', 999)
        if nearest_dist < 30:
            score += 40
        elif nearest_dist < 50:
            score += 30
        elif nearest_dist < 75:
            score += 20
        elif nearest_dist < 100:
            score += 10

        if site.get('interstate_distance', 99) < 5:
            score += 20
        elif site.get('interstate_distance', 99) < 10:
            score += 15
        elif site.get('interstate_distance', 99) < 20:
            score += 10

        if site.get('rail_access'):
            score += 20
        elif site.get('rail_distance', 99) < 5:
            score += 10

        if site.get('waterway_access'):
            score += 20
        elif site.get('waterway_distance', 99) < 10:
            score += 10

        return min(score, 100)

    def generate_sample_aggregate_sites(self):
        """Generate realistic sample aggregate operations"""
        import random

        companies = [
            'Martin Marietta Materials', 'Vulcan Materials Company', 'Summit Materials',
            'Rogers Group', 'Oldcastle Materials', 'Heidelberg Materials', 'Lehigh Hanson',
            'Luck Stone', 'Thompson Machinery', 'Boral Resources', 'Argos USA', 'Cemex USA',
            'Independence Materials Group', 'Southern Crushed Concrete', 'Rinker Materials'
        ]

        commodity_types = [
            'Crushed Stone', 'Sand & Gravel', 'Limestone', 'Granite', 'Traprock',
            'Washed Sand', 'Concrete Sand', 'Fill Sand', 'Pea Gravel', 'River Rock'
        ]

        sites = []
        site_id = 1000

        for state in SOUTHEAST_STATES:
            num_sites = random.randint(15, 30)

            for _ in range(num_sites):
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

                distances = {}
                for msa_name, (msa_lat, msa_lon) in MAJOR_MSAS.items():
                    dist = self.haversine_distance(lat, lon, msa_lat, msa_lon)
                    distances[msa_name] = dist

                nearest_msa = min(distances.items(), key=lambda x: x[1])
                annual_production = random.randint(1000, 5000) * 1000
                employees = int((annual_production / 1_000_000) * random.randint(10, 50))
                is_active = random.random() < 0.95
                interstate_distance = random.uniform(0.5, 25)
                rail_access = random.random() < 0.30
                rail_distance = random.uniform(0.5, 15) if not rail_access else 0
                waterway_access = random.random() < 0.15
                waterway_distance = random.uniform(2, 30) if not waterway_access else 0
                permits_current = random.random() < 0.90
                permit_expiry_year = datetime.datetime.now().year + random.randint(-2, 8)
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
        """Fetch MSHA mine data"""
        print("🏗️  FETCHING AGGREGATE PRODUCTION DATA...")
        sites = self.generate_sample_aggregate_sites()
        major_sites = [s for s in sites if s['annual_production_tons'] >= 1_000_000]
        print(f"   Found {len(major_sites)} sites producing 1M+ tons annually")
        return major_sites

    def get_aggregate_snapshot(self):
        """Get comprehensive aggregate market data"""
        sites = self.fetch_msha_data()
        total_production = sum(s['annual_production_tons'] for s in sites)
        active_sites = [s for s in sites if s['is_active']]
        inactive_sites = [s for s in sites if not s['is_active']]

        operators = {}
        for site in sites:
            op = site['operator']
            if op not in operators:
                operators[op] = {'sites': [], 'total_production': 0, 'active_sites': 0, 'states': set()}
            operators[op]['sites'].append(site)
            operators[op]['total_production'] += site['annual_production_tons']
            operators[op]['active_sites'] += 1 if site['is_active'] else 0
            operators[op]['states'].add(site['state'])

        states = {}
        for site in sites:
            st = site['state']
            if st not in states:
                states[st] = {'sites': [], 'total_production': 0, 'active_count': 0}
            states[st]['sites'].append(site)
            states[st]['total_production'] += site['annual_production_tons']
            states[st]['active_count'] += 1 if site['is_active'] else 0

        commodities = {}
        for site in sites:
            comm = site['commodity']
            if comm not in commodities:
                commodities[comm] = {'sites': [], 'total_production': 0}
            commodities[comm]['sites'].append(site)
            commodities[comm]['total_production'] += site['annual_production_tons']

        top_logistics = sorted(sites, key=lambda x: x['logistics_score'], reverse=True)[:20]

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
# INTERACTIVE MAP VIEW
# ==================================================

class InteractiveMapView(ui.View):
    def __init__(self, sites, selected_callback):
        super().__init__()
        self.sites = sites
        self.selected_callback = selected_callback
        self.selected_site = None
        self.background_color = '#1a1a1a'

    def layout(self):
        if self.width > 0 and self.height > 0:
            self.draw_map()

    def draw_map(self):
        # Clear existing subviews
        for subview in list(self.subviews):
            self.remove_subview(subview)

        if not self.sites:
            # Show message if no sites
            msg = ui.Label(frame=(0, 0, self.width, self.height))
            msg.text = 'No sites to display'
            msg.alignment = ui.ALIGN_CENTER
            msg.text_color = THEME['text']
            msg.font = ('<system>', 16)
            self.add_subview(msg)
            return

        # Calculate bounds
        lats = [s['lat'] for s in self.sites]
        lons = [s['lon'] for s in self.sites]
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)

        # Add padding
        lat_range = max(max_lat - min_lat, 0.1)  # Prevent zero range
        lon_range = max(max_lon - min_lon, 0.1)
        min_lat -= lat_range * 0.05
        max_lat += lat_range * 0.05
        min_lon -= lon_range * 0.05
        max_lon += lon_range * 0.05

        # Draw MSA markers
        for msa_name, (msa_lat, msa_lon) in MAJOR_MSAS.items():
            # Skip MSAs outside our bounds
            if msa_lon < min_lon or msa_lon > max_lon or msa_lat < min_lat or msa_lat > max_lat:
                continue

            x = ((msa_lon - min_lon) / (max_lon - min_lon)) * self.width
            y = self.height - ((msa_lat - min_lat) / (max_lat - min_lat)) * self.height

            # MSA circle
            msa_view = ui.View(frame=(x-8, y-8, 16, 16))
            msa_view.background_color = THEME['warn']
            msa_view.corner_radius = 8
            msa_view.alpha = 0.6
            self.add_subview(msa_view)

            # MSA label
            label = ui.Label(frame=(x-60, y+10, 120, 15))
            label.text = msa_name.split(',')[0]
            label.font = ('<system>', 8)
            label.text_color = THEME['warn']
            label.alignment = ui.ALIGN_CENTER
            label.alpha = 0.7
            self.add_subview(label)

        # Draw site markers
        for site in self.sites:
            x = ((site['lon'] - min_lon) / (max_lon - min_lon)) * self.width
            y = self.height - ((site['lat'] - min_lat) / (max_lat - min_lat)) * self.height

            # Size based on production (larger for better tapping)
            visual_size = min(max(site['annual_production_tons'] / 200000, 5), 14)
            tap_size = max(visual_size + 6, 20)  # Larger tap target

            # Color based on logistics score
            if site['logistics_score'] >= 75:
                color = THEME['bull']
            elif site['logistics_score'] >= 50:
                color = THEME['warn']
            else:
                color = THEME['bear']

            if not site['is_active']:
                color = THEME['sub']

            # Create button for each site with larger tap area
            btn = ui.Button(frame=(x-tap_size/2, y-tap_size/2, tap_size, tap_size))
            btn.background_color = color
            btn.corner_radius = tap_size/2
            btn.alpha = 0.8
            btn.name = site['mine_id']
            btn.action = self.site_tapped
            btn.border_width = 0
            self.add_subview(btn)

    def site_tapped(self, sender):
        # Find the site
        site = next((s for s in self.sites if s['mine_id'] == sender.name), None)
        if site:
            self.selected_site = site
            # Visual feedback
            sender.alpha = 1.0
            if self.selected_callback:
                self.selected_callback(site)

# ==================================================
# SITE DETAIL POPUP
# ==================================================

class SiteDetailPopup(ui.View):
    def __init__(self, site, close_callback, all_sites=None):
        super().__init__()
        self.site = site
        self.close_callback = close_callback
        self.all_sites = all_sites or []
        self.background_color = '#0a0a0a'
        self.alpha = 0.98

    def layout(self):
        w = self.width
        h = self.height

        # Close button
        close_btn = ui.Button(frame=(w-50, 10, 40, 40))
        close_btn.title = '✕'
        close_btn.font = ('<system>', 24)
        close_btn.background_color = THEME['bear']
        close_btn.tint_color = 'white'
        close_btn.corner_radius = 20
        close_btn.action = lambda sender: self.close_callback()
        self.add_subview(close_btn)

        # Content scroll view
        scroll = ui.ScrollView(frame=(20, 60, w-40, h-80))
        scroll.background_color = '#1a1a1a'
        scroll.corner_radius = 10
        self.add_subview(scroll)

        y = 20

        # Title
        title = ui.Label(frame=(20, y, w-80, 30))
        title.text = self.site['site_name']
        title.font = ('<system-bold>', 18)
        title.text_color = THEME['bull'] if self.site['is_active'] else THEME['sub']
        title.number_of_lines = 0
        scroll.add_subview(title)
        y += 40

        # Status badge
        status_badge = ui.Label(frame=(20, y, 100, 25))
        status_badge.text = '✓ ACTIVE' if self.site['is_active'] else '✗ INACTIVE'
        status_badge.font = ('<system-bold>', 12)
        status_badge.text_color = 'white'
        status_badge.background_color = THEME['bull'] if self.site['is_active'] else THEME['sub']
        status_badge.alignment = ui.ALIGN_CENTER
        status_badge.corner_radius = 5
        scroll.add_subview(status_badge)
        y += 35

        # Details sections
        sections = [
            ('OPERATOR & PRODUCTION', [
                ('Operator', self.site['operator']),
                ('Commodity', self.site['commodity']),
                ('Annual Production', f"{self.site['annual_production_tons']/1_000_000:.2f}M tons"),
                ('Employees', str(self.site['employees'])),
                ('Mine ID', self.site['mine_id'])
            ]),
            ('LOCATION & MARKET', [
                ('State', self.site['state']),
                ('Coordinates', f"{self.site['lat']:.4f}, {self.site['lon']:.4f}"),
                ('Nearest MSA', self.site['nearest_msa']),
                ('Distance to MSA', f"{self.site['nearest_msa_distance']:.1f} miles"),
                ('Market Position', 'PRIMARY' if self.site['nearest_msa_distance'] < 30 else 'SECONDARY' if self.site['nearest_msa_distance'] < 50 else 'TERTIARY')
            ]),
            ('LOGISTICS ANALYSIS', [
                ('Overall Score', f"{self.site['logistics_score']}/100"),
                ('Interstate Distance', f"{self.site['interstate_distance']:.1f} miles"),
                ('Rail Access', 'YES - ON SITE' if self.site['rail_access'] else f"NO - {self.site['rail_distance']:.1f}mi away"),
                ('Waterway Access', 'YES - BARGE CAPABLE' if self.site['waterway_access'] else f"NO - {self.site['waterway_distance']:.1f}mi away"),
                ('Transport Economics', 'EXCELLENT' if self.site['logistics_score'] >= 75 else 'GOOD' if self.site['logistics_score'] >= 50 else 'FAIR')
            ]),
            ('PERMITS & RESERVES', [
                ('Permit Status', 'CURRENT' if self.site['permits_current'] else 'EXPIRED/PENDING'),
                ('Permit Expires', str(self.site['permit_expiry_year'])),
                ('Reserve Life', f"{self.site['reserve_years']} years"),
                ('Last Inspection', self.site['last_inspection'].strftime('%Y-%m-%d'))
            ]),
            ('COMPETITIVE POSITION', [
                ('MSA Market Size', f"~{len([s for s in self.all_sites if s['nearest_msa'] == self.site['nearest_msa']])} sites in market"),
                ('Distance Advantage', 'PRIME' if self.site['nearest_msa_distance'] < 30 and self.site['logistics_score'] > 70 else 'COMPETITIVE'),
                ('Strategic Assets', f"Rail: {'✓' if self.site['rail_access'] else '✗'} | Water: {'✓' if self.site['waterway_access'] else '✗'}")
            ])
        ]

        for section_title, fields in sections:
            # Section header
            header = ui.Label(frame=(20, y, w-80, 25))
            header.text = section_title
            header.font = ('<system-bold>', 14)
            header.text_color = THEME['total']
            scroll.add_subview(header)
            y += 30

            # Fields
            for label_text, value_text in fields:
                # Label
                lbl = ui.Label(frame=(30, y, 140, 20))
                lbl.text = label_text + ':'
                lbl.font = ('<system>', 11)
                lbl.text_color = THEME['sub']
                scroll.add_subview(lbl)

                # Value
                val = ui.Label(frame=(180, y, w-220, 20))
                val.text = str(value_text)
                val.font = ('<system-bold>', 11)
                val.text_color = THEME['text']
                val.number_of_lines = 0
                scroll.add_subview(val)
                y += 25

            y += 15

        scroll.content_size = (w-40, y + 20)

# ==================================================
# FILTER PANEL
# ==================================================

class FilterPanel(ui.View):
    def __init__(self, data, filter_callback):
        super().__init__()
        self.data = data
        self.filter_callback = filter_callback
        self.background_color = '#1a1a1a'
        self.filters = {
            'state': None,
            'operator': None,
            'commodity': None,
            'min_logistics': 0,
            'active_only': False
        }

    def layout(self):
        w = self.width
        y = 15

        # Title
        title = ui.Label(frame=(15, y, w-30, 25))
        title.text = 'FILTERS'
        title.font = ('<system-bold>', 16)
        title.text_color = THEME['total']
        self.add_subview(title)
        y += 35

        # State filter
        state_lbl = ui.Label(frame=(15, y, 80, 30))
        state_lbl.text = 'State:'
        state_lbl.font = ('<system>', 12)
        state_lbl.text_color = THEME['text']
        self.add_subview(state_lbl)

        state_seg = ui.SegmentedControl(frame=(100, y, w-115, 30))
        state_seg.segments = ['All'] + SOUTHEAST_STATES
        state_seg.selected_index = 0
        state_seg.action = self.state_changed
        self.add_subview(state_seg)
        y += 40

        # Active only toggle
        active_lbl = ui.Label(frame=(15, y, 150, 30))
        active_lbl.text = 'Active Sites Only:'
        active_lbl.font = ('<system>', 12)
        active_lbl.text_color = THEME['text']
        self.add_subview(active_lbl)

        active_switch = ui.Switch(frame=(w-80, y, 60, 30))
        active_switch.value = False
        active_switch.action = self.active_changed
        self.add_subview(active_switch)
        y += 40

        # Logistics score slider
        logistics_lbl = ui.Label(frame=(15, y, w-30, 20))
        logistics_lbl.text = 'Min Logistics Score: 0'
        logistics_lbl.font = ('<system>', 12)
        logistics_lbl.text_color = THEME['text']
        logistics_lbl.name = 'logistics_label'
        self.add_subview(logistics_lbl)
        y += 25

        logistics_slider = ui.Slider(frame=(15, y, w-30, 30))
        logistics_slider.value = 0
        logistics_slider.action = self.logistics_changed
        self.add_subview(logistics_slider)
        y += 40

        # Apply button
        apply_btn = ui.Button(frame=(15, y, w-30, 40))
        apply_btn.title = 'APPLY FILTERS'
        apply_btn.background_color = THEME['bull']
        apply_btn.tint_color = 'white'
        apply_btn.corner_radius = 8
        apply_btn.font = ('<system-bold>', 14)
        apply_btn.action = self.apply_filters
        self.add_subview(apply_btn)
        y += 50

        # Reset button
        reset_btn = ui.Button(frame=(15, y, w-30, 35))
        reset_btn.title = 'Reset All'
        reset_btn.background_color = THEME['sub']
        reset_btn.tint_color = 'white'
        reset_btn.corner_radius = 8
        reset_btn.action = self.reset_filters
        self.add_subview(reset_btn)

    def state_changed(self, sender):
        self.filters['state'] = None if sender.selected_index == 0 else sender.segments[sender.selected_index]

    def active_changed(self, sender):
        self.filters['active_only'] = sender.value

    def logistics_changed(self, sender):
        score = int(sender.value * 100)
        self.filters['min_logistics'] = score
        lbl = self['logistics_label']
        if lbl:
            lbl.text = f'Min Logistics Score: {score}'

    def apply_filters(self, sender):
        if self.filter_callback:
            self.filter_callback(self.filters)

    def reset_filters(self, sender):
        self.filters = {
            'state': None,
            'operator': None,
            'commodity': None,
            'min_logistics': 0,
            'active_only': False
        }
        # Reset UI
        for subview in self.subviews:
            if isinstance(subview, ui.SegmentedControl):
                subview.selected_index = 0
            elif isinstance(subview, ui.Switch):
                subview.value = False
            elif isinstance(subview, ui.Slider):
                subview.value = 0
        lbl = self['logistics_label']
        if lbl:
            lbl.text = 'Min Logistics Score: 0'

        if self.filter_callback:
            self.filter_callback(self.filters)

# ==================================================
# MAIN DASHBOARD
# ==================================================

class EnhancedAggregateDashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.name = 'Aggregate Production'
        self.data_engine = AggregateDataEngine()
        self.current_data = None
        self.filtered_sites = []
        self.detail_popup = None
        self.filter_panel = None
        self.data_loaded = False

    def did_load(self):
        if not self.data_loaded:
            self.refresh_data(None)

    def refresh_data(self, sender):
        print("🔄 REFRESHING AGGREGATE DATA...")
        self.current_data = self.data_engine.get_aggregate_snapshot()
        self.filtered_sites = self.current_data['sites']
        self.data_loaded = True
        self.rebuild_ui()
        print("✅ REFRESH COMPLETE")

    def rebuild_ui(self):
        for subview in list(self.subviews):
            self.remove_subview(subview)
        self.layout()

    def apply_filters(self, filters):
        """Apply filters to site list"""
        sites = self.current_data['sites']

        if filters.get('state'):
            sites = [s for s in sites if s['state'] == filters['state']]

        if filters.get('active_only'):
            sites = [s for s in sites if s['is_active']]

        if filters.get('min_logistics', 0) > 0:
            sites = [s for s in sites if s['logistics_score'] >= filters['min_logistics']]

        self.filtered_sites = sites
        self.rebuild_ui()

    def show_site_detail(self, site):
        """Show detailed popup for a site"""
        if self.detail_popup:
            self.remove_subview(self.detail_popup)

        self.detail_popup = SiteDetailPopup(site, self.close_detail_popup, self.current_data['sites'])
        self.detail_popup.frame = (0, 0, self.width, self.height)
        self.detail_popup.flex = 'WH'
        self.add_subview(self.detail_popup)
        self.detail_popup.bring_to_front()

    def close_detail_popup(self):
        if self.detail_popup:
            self.remove_subview(self.detail_popup)
            self.detail_popup = None

    def toggle_filters(self, sender):
        """Show/hide filter panel"""
        if self.filter_panel and self.filter_panel.superview:
            self.remove_subview(self.filter_panel)
            self.filter_panel = None
            sender.title = '⚙️ Filters'
        else:
            self.filter_panel = FilterPanel(self.current_data, self.apply_filters)
            self.filter_panel.frame = (0, 50, self.width, 300)
            self.filter_panel.corner_radius = 10
            self.add_subview(self.filter_panel)
            sender.title = '✕ Close'

    def layout(self):
        # Load data if not already loaded
        if not self.data_loaded and self.width > 0 and self.height > 0:
            self.refresh_data(None)
            return

        if not self.current_data:
            # Show loading message
            loading = ui.Label(frame=(0, 0, self.width, self.height))
            loading.text = 'Loading...'
            loading.alignment = ui.ALIGN_CENTER
            loading.text_color = THEME['text']
            loading.font = ('<system>', 20)
            self.add_subview(loading)
            return

        w = self.width
        h = self.height

        # Top control bar
        control_bar = ui.View(frame=(0, 0, w, 50))
        control_bar.background_color = '#1a1a1a'
        self.add_subview(control_bar)

        # Title
        title = ui.Label(frame=(15, 10, w-200, 30))
        title.text = f"🏗️ AGGREGATE SITES ({len(self.filtered_sites)})"
        title.font = ('<system-bold>', 18)
        title.text_color = THEME['total']
        control_bar.add_subview(title)

        # Filter button
        filter_btn = ui.Button(frame=(w-180, 7, 80, 36))
        filter_btn.title = '⚙️ Filters'
        filter_btn.background_color = THEME['stone']
        filter_btn.tint_color = 'white'
        filter_btn.corner_radius = 6
        filter_btn.action = self.toggle_filters
        control_bar.add_subview(filter_btn)

        # Refresh button
        refresh_btn = ui.Button(frame=(w-90, 7, 80, 36))
        refresh_btn.title = '🔄 Refresh'
        refresh_btn.background_color = THEME['bull']
        refresh_btn.tint_color = 'white'
        refresh_btn.corner_radius = 6
        refresh_btn.action = self.refresh_data
        control_bar.add_subview(refresh_btn)

        # Main content - Interactive Map
        map_view = InteractiveMapView(self.filtered_sites, self.show_site_detail)
        map_view.frame = (0, 50, w, h-50)
        map_view.flex = 'WH'
        self.add_subview(map_view)

        # Legend
        legend_y = h - 70
        legend_items = [
            (THEME['bull'], 'Score 75+'),
            (THEME['warn'], 'Score 50-74'),
            (THEME['bear'], 'Score <50'),
            (THEME['sub'], 'Inactive')
        ]

        legend_x = 15
        for color, label in legend_items:
            dot = ui.View(frame=(legend_x, legend_y, 12, 12))
            dot.background_color = color
            dot.corner_radius = 6
            self.add_subview(dot)

            lbl = ui.Label(frame=(legend_x + 18, legend_y - 3, 80, 18))
            lbl.text = label
            lbl.font = ('<system>', 10)
            lbl.text_color = THEME['text']
            self.add_subview(lbl)

            legend_x += 95

        # Force layout of map
        map_view.set_needs_display()

# ==================================================
# MAIN
# ==================================================

if __name__ == '__main__':
    plt.style.use('dark_background')
    v = EnhancedAggregateDashboard()
    v.present('fullscreen')
