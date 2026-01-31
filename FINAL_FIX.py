"""
FINAL FIX - Everything in __init__, not did_load()
"""
import ui

THEME = {'bg': '#000000', 'panel': '#1a1a1a', 'gold': '#ffd700', 'green': '#00ff88'}

class Dashboard(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = THEME['bg']

        # Get screen size
        w, h = ui.get_screen_size()

        # Create scroll view
        scroll = ui.ScrollView()
        scroll.frame = (0, 0, w, h)
        scroll.background_color = THEME['bg']
        self.add_subview(scroll)

        y = 50

        # Title
        title = ui.Label()
        title.frame = (20, y, w-40, 50)
        title.text = "🐔 CHICKEN MARKET"
        title.font = ('<system-bold>', 32)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        scroll.add_subview(title)
        y += 70

        # Card
        card = ui.View()
        card.frame = (20, y, w-40, 130)
        card.background_color = THEME['panel']
        card.corner_radius = 10
        scroll.add_subview(card)

        # Card title
        ct = ui.Label()
        ct.frame = (20, 15, card.width-40, 25)
        ct.text = "BONELESS BREAST"
        ct.font = ('<system-bold>', 18)
        ct.text_color = THEME['green']
        card.add_subview(ct)

        # Card value
        cv = ui.Label()
        cv.frame = (20, 50, card.width-40, 35)
        cv.text = "$1.58 /lb"
        cv.font = ('<system-bold>', 32)
        cv.text_color = 'white'
        card.add_subview(cv)

        # Card desc
        cd = ui.Label()
        cd.frame = (20, 90, card.width-40, 30)
        cd.text = "STRONG BUY → Target $1.78"
        cd.font = ('<system>', 14)
        cd.text_color = '#999999'
        card.add_subview(cd)

        y += 150

        # Analysis
        analysis = ui.TextView()
        analysis.frame = (20, y, w-40, 280)
        analysis.background_color = THEME['panel']
        analysis.text_color = 'white'
        analysis.font = ('<system>', 15)
        analysis.editable = False
        analysis.text = """MARKET INTELLIGENCE

Supply Crisis:
• Hatchability 79.7% vs 84% normal
• Missing 58M chicks weekly
• Supply locked through 2027

Price Action:
• Breast: $1.58 → $1.78 (90 days)
• Wings: $1.68 → $2.25 (Super Bowl)
• Legs: $0.42 (avoid - export weak)

Strategy:
✓ BUY: Breast, Tenders, Thighs
✗ AVOID: Leg Quarters, Paws"""
        scroll.add_subview(analysis)
        y += 300

        scroll.content_size = (w, y + 50)

class Launcher(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = 'black'

        w, h = ui.get_screen_size()

        # Title
        title = ui.Label()
        title.frame = (0, 160, w, 80)
        title.text = "CHICKEN\nMARKET"
        title.font = ('<system-bold>', 42)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        # Button
        btn = ui.Button()
        btn.frame = ((w-260)/2, 320, 260, 80)
        btn.title = "LAUNCH"
        btn.font = ('<system-bold>', 28)
        btn.background_color = THEME['gold']
        btn.tint_color = 'black'
        btn.corner_radius = 15
        btn.action = self.go
        self.add_subview(btn)

    def go(self, sender):
        d = Dashboard()
        d.name = "Market Intel"
        nav = ui.NavigationView(d)
        nav.present('fullscreen')

# RUN
Launcher().present('fullscreen')
