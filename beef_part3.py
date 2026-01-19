# ==================================================
# BEEF & DAIRY MARKET INTELLIGENCE PLATFORM
# PART 3: Dashboard UI & Main Entry Point
# ==================================================

from beef_part1 import *
from beef_part2 import *

class BeefDashboard(ui.View):
    """Comprehensive Beef & Cattle Market Dashboard"""

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
        self.right_button_items = [ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh)]

    def will_appear(self):
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        self.loading.start()
        for sub in self.scroll.subviews:
            sub.remove_from_superview()
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        market_data = self.data_engine.get_market_snapshot()
        dates = self.data_engine.calculate_forecast_dates()
        analyzer = BeefMarketAnalyzer(market_data)
        self.data = analyzer.calculate_metrics(dates)
        ui.delay(self.draw_ui, 0)

    def draw_ui(self):
        self.loading.stop()
        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        self._add_label("🥩 BEEF & CATTLE MARKET", 28, THEME['beef'], y, cw, bold=True)
        y += 35
        self._add_label(f"COMPREHENSIVE SUPPLY CHAIN INTELLIGENCE | {self.data['meta']['time']}", 12, THEME['sub'], y, cw)
        y += 40

        # 1. MACRO & PROTEIN COMPETITION
        y = HeaderLabel.create(self.scroll, "1. MACRO & PROTEIN COMPETITION", THEME['macro'], y, cw)
        for k, v in self.data['macro'].items():
            card, h = InsightCard.create(k, v, THEME['macro'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 2. CATTLE SUPPLY & HERD LIQUIDATION
        y = HeaderLabel.create(self.scroll, "2. CATTLE SUPPLY & HERD LIQUIDATION (CRITICAL)", THEME['cattle'], y, cw)
        for k, v in self.data['supply'].items():
            card, h = InsightCard.create(k, v, THEME['cattle'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 3. FEEDLOT ECONOMICS
        y = HeaderLabel.create(self.scroll, "3. FEEDLOT ECONOMICS & MARGINS", THEME['grain'], y, cw)
        for k, v in self.data['feedlot'].items():
            card, h = InsightCard.create(k, v, THEME['grain'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 4. FEED COSTS & DROUGHT
        y = HeaderLabel.create(self.scroll, "4. FEED COSTS & DROUGHT CONDITIONS", THEME['grass'], y, cw)
        for k, v in self.data['feed_drought'].items():
            card, h = InsightCard.create(k, v, THEME['grass'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 5. PACKER POWER
        y = HeaderLabel.create(self.scroll, "5. PACKER POWER & PROCESSING", THEME['packer'], y, cw)
        for k, v in self.data['packer'].items():
            card, h = InsightCard.create(k, v, THEME['packer'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 6. EXPORT/IMPORT
        y = HeaderLabel.create(self.scroll, "6. EXPORT/IMPORT DYNAMICS", THEME['export'], y, cw)
        for k, v in self.data['trade'].items():
            card, h = InsightCard.create(k, v, THEME['export'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 7. COLD STORAGE
        y = HeaderLabel.create(self.scroll, "7. COLD STORAGE INVENTORY", THEME['cold'], y, cw)
        for k, v in self.data['storage'].items():
            col = THEME['bull'] if "TIGHT" in v['status'] or "CRITICAL" in v['status'] else THEME['cold']
            card, h = InsightCard.create(k, v, col, cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 8. BEEF CUT FORECASTS
        y = HeaderLabel.create(self.scroll, "8. BEEF CUT PRICE FORECASTS (90-DAY)", THEME['bull'], y, cw)
        for k, v in self.data['cuts'].items():
            card, h = ForecastCard.create(k, v, cw, y, self.data['meta']['dates'])
            self.scroll.add_subview(card)
            y += h + 15

        # 9. ANALYST VERDICT
        y = self._draw_verdict(y, cw)

        self.scroll.content_size = (w, y + 100)

    def _draw_verdict(self, y, w):
        y = HeaderLabel.create(self.scroll, "9. ANALYST VERDICT", THEME['warn'], y, w)
        h = 480
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8
        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 14)
        tv.editable = False
        tv.text = (
            "BEEF VERDICT: 'CYCLICAL LIQUIDATION INTO STRUCTURAL REBUILD'\n\n"
            "1. THE LIQUIDATION PHASE:\n"
            "Herd in liquidation (down 1.8% YoY). Heifer retention 38% vs normal 45%. "
            "Cow slaughter at record highs. Ranchers selling breeding stock due to drought + high hay costs. "
            "This means SHORT-TERM beef supply is UP (bearish), but LONG-TERM (2025-2027) will be DOWN (bullish).\n\n"
            "2. THE DROUGHT/FEED COST TRAP:\n"
            "Pastures 58% poor condition. Hay prices elevated. Ranchers can't afford to keep herds. "
            "Forced liquidation = temporary supply glut. But once rebuild starts, takes 3-5 YEARS to grow herd. "
            "Future supply shortage is baked in.\n\n"
            "3. THE PACKER OLIGOPOLY:\n"
            "4 firms = 85% of slaughter. Tyson, JBS, Cargill, National Beef have pricing power. "
            "Packer margins $285/head (elevated). Ranchers get squeezed on both ends: high feed costs, "
            "price-taker status. Political pressure building for antitrust action.\n\n"
            "4. THE EXPORT DEPENDENCY:\n"
            "13.5% of production exported. Japan, Korea, Mexico are critical. China is wild card. "
            "Dollar strength kills exports = domestic oversupply. But US ALSO imports 14.2%! "
            "Australia/NZ lean beef competes with US ground beef. Import ceiling on prices.\n\n"
            "5. THE CUT DIVERGENCE:\n"
            "Middle meats (ribeye, strip) holding premium as steakhouses recover. Ground beef under pressure "
            "from imports + cow slaughter. Brisket/short ribs = restaurant darlings, limited supply, BULLISH.\n\n"
            "6. THE DAIRY WILDCARD:\n"
            "18% of US beef comes from dairy cattle (Holstein steers + cull cows). When milk prices crash, "
            "dairy farmers cull aggressively = more beef = lower prices. Currently dairy strong = less culling.\n\n"
            "7. ACTION PLAN:\n"
            "• NEAR-TERM (6 mo): NEUTRAL ground beef (liquidation supply), BUY middle meats (restaurant recovery)\n"
            "• MEDIUM-TERM (12-18 mo): BUY premium cuts (ribeye, strip, brisket, short ribs)\n"
            "• LONG-TERM (2+ yr): STRONG BUY all beef (herd rebuild = supply shortage)\n"
            "• HEDGE: Watch feeder cattle prices (leading indicator), hay prices (stress gauge)\n\n"
            "BOTTOM LINE: We're in the eye of the hurricane. Liquidation creating temporary supply. "
            "But the rebuild will take YEARS. Position for the long-term supply squeeze. "
            "Beef prices going MUCH higher 2025-2027."
        )
        card.add_subview(tv)
        self.scroll.add_subview(card)
        return y + h + 20

    def _add_label(self, text, size, color, y, w, bold=False):
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)

class DairyDashboard(ui.View):
    """Dairy Market Dashboard (Integrated with Beef)"""

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
        self.right_button_items = [ui.ButtonItem(image=ui.Image.named('iob:ios7_refresh_empty_32'), action=self.refresh)]

    def will_appear(self):
        if self.data is None:
            self.refresh(None)

    def refresh(self, sender):
        self.loading.start()
        for sub in self.scroll.subviews:
            sub.remove_from_superview()
        threading.Thread(target=self.load_data).start()

    def load_data(self):
        market_data = self.data_engine.get_market_snapshot()
        dates = self.data_engine.calculate_forecast_dates()
        analyzer = DairyMarketAnalyzer(market_data)
        self.data = analyzer.calculate_metrics(dates)
        ui.delay(self.draw_ui, 0)

    def draw_ui(self):
        self.loading.stop()
        w, h = ui.get_screen_size()
        self.scroll.frame = (0, 0, w, h)
        cw = w - (MARGIN * 2)
        y = 40

        self._add_label("🥛 DAIRY MARKET", 28, THEME['dairy'], y, cw, bold=True)
        y += 35
        self._add_label(f"MILK, CHEESE, BUTTER + BEEF IMPACT | {self.data['meta']['time']}", 12, THEME['sub'], y, cw)
        y += 40

        # 1. DAIRY HERD
        y = HeaderLabel.create(self.scroll, "1. DAIRY HERD & BEEF IMPACT", THEME['dairy'], y, cw)
        for k, v in self.data['dairy_herd'].items():
            card, h = InsightCard.create(k, v, THEME['dairy'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 2. DAIRY PRICES
        y = HeaderLabel.create(self.scroll, "2. DAIRY PRODUCT PRICES", THEME['gold'], y, cw)
        for k, v in self.data['dairy_prices'].items():
            card, h = InsightCard.create(k, v, THEME['gold'], cw, y)
            self.scroll.add_subview(card)
            y += h + 15

        # 3. VERDICT
        y = self._draw_verdict(y, cw)

        self.scroll.content_size = (w, y + 100)

    def _draw_verdict(self, y, w):
        y = HeaderLabel.create(self.scroll, "3. DAIRY VERDICT", THEME['warn'], y, w)
        h = 320
        card = ui.View(frame=(MARGIN, y, w, h))
        card.background_color = '#222'
        card.corner_radius = 8
        tv = ui.TextView(frame=(15, 15, w-30, h-30))
        tv.background_color = '#222'
        tv.text_color = 'white'
        tv.font = ('<system>', 14)
        tv.editable = False
        tv.text = (
            "DAIRY VERDICT: 'THE BEEF WILDCARD'\n\n"
            "1. DAIRY = 18% OF BEEF SUPPLY:\n"
            "Most people don't realize dairy cattle are a HUGE beef source. "
            "Holstein steers (3.2M/year) + cull dairy cows (3.5M/year) = "
            "nearly 1/5 of US beef production!\n\n"
            "2. THE INVERSE RELATIONSHIP:\n"
            "When milk/cheese/butter prices are LOW → dairy farmers cull "
            "aggressively to cut costs → MORE beef supply → LOWER beef prices.\n"
            "When dairy prices are HIGH → keep cows in production → "
            "LESS beef supply → HIGHER beef prices.\n\n"
            "3. CURRENT STATE:\n"
            "Dairy prices currently moderate-to-strong. Cheese and butter "
            "elevated. This means dairy farmers keeping cows IN milk rather "
            "than culling. SUPPORTIVE for beef prices.\n\n"
            "4. THE WATCH:\n"
            "Monitor milk prices closely. If milk crashes below $3.50/gal, "
            "expect aggressive dairy culling = beef supply surge = price pressure.\n\n"
            "BOTTOM LINE: Dairy is the hidden lever in beef markets. "
            "Strong dairy = less beef supply = bullish for beef prices."
        )
        card.add_subview(tv)
        self.scroll.add_subview(card)
        return y + h + 20

    def _add_label(self, text, size, color, y, w, bold=False):
        f = '<system-bold>' if bold else '<system>'
        l = ui.Label(frame=(MARGIN, y, w, size+5))
        l.text = text
        l.font = (f, size)
        l.text_color = color
        l.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(l)

class MarketSelector(ui.View):
    """Main navigation screen"""

    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']
        self.data_engine = DataEngine()

    def did_load(self):
        w, h = ui.get_screen_size()
        title = ui.Label(frame=(0, 80, w, 50))
        title.text = "BEEF & DAIRY\nMARKET INTELLIGENCE"
        title.font = ('<system-bold>', 32)
        title.text_color = THEME['beef']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        subtitle = ui.Label(frame=(0, 145, w, 30))
        subtitle.text = "COMPREHENSIVE CATTLE & DAIRY ANALYSIS"
        subtitle.font = ('<system>', 12)
        subtitle.text_color = THEME['sub']
        subtitle.alignment = ui.ALIGN_CENTER
        self.add_subview(subtitle)

        btn_width = min(w - 80, 400)
        btn_x = (w - btn_width) / 2
        btn_y = 220

        beef_btn = self._create_button(
            "🥩 BEEF & CATTLE",
            "Supply Chain, Feed, Drought, Exports, Forecasts",
            THEME['beef'],
            (btn_x, btn_y, btn_width, 100)
        )
        beef_btn.action = self.show_beef
        self.add_subview(beef_btn)

        dairy_btn = self._create_button(
            "🥛 DAIRY MARKET",
            "Milk, Cheese, Butter & Beef Impact Analysis",
            THEME['dairy'],
            (btn_x, btn_y + 120, btn_width, 100)
        )
        dairy_btn.action = self.show_dairy
        self.add_subview(dairy_btn)

        footer = ui.Label(frame=(40, h - 100, w - 80, 60))
        footer.text = (
            "Real-time: USDA & FRED APIs\n"
            "Cattle inventory • Feed costs • Packer margins • Export/Import"
        )
        footer.font = ('<system>', 11)
        footer.text_color = THEME['neutral']
        footer.alignment = ui.ALIGN_CENTER
        footer.number_of_lines = 2
        self.add_subview(footer)

    def _create_button(self, title, subtitle, color, frame):
        btn = ui.Button(frame=frame)
        btn.background_color = THEME['panel']
        btn.border_color = color
        btn.border_width = 2
        btn.corner_radius = 12
        title_lbl = ui.Label()
        title_lbl.text = title
        title_lbl.font = ('<system-bold>', 24)
        title_lbl.text_color = color
        title_lbl.alignment = ui.ALIGN_CENTER
        title_lbl.frame = (10, 20, frame[2] - 20, 35)
        btn.add_subview(title_lbl)
        sub_lbl = ui.Label()
        sub_lbl.text = subtitle
        sub_lbl.font = ('<system>', 13)
        sub_lbl.text_color = THEME['sub']
        sub_lbl.alignment = ui.ALIGN_CENTER
        sub_lbl.frame = (10, 58, frame[2] - 20, 20)
        btn.add_subview(sub_lbl)
        return btn

    def show_beef(self, sender):
        dashboard = BeefDashboard(self.data_engine)
        dashboard.name = "Beef & Cattle Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')

    def show_dairy(self, sender):
        dashboard = DairyDashboard(self.data_engine)
        dashboard.name = "Dairy Market"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')

# ==================================================
# MAIN ENTRY POINT - RUN THIS!
# ==================================================
if __name__ == '__main__':
    selector = MarketSelector()
    selector.present('fullscreen')
