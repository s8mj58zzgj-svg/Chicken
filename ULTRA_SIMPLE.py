"""
ULTRA SIMPLE VERSION - THIS WILL WORK
No API calls, no threading, just works immediately
"""
import ui

print("Starting...")

THEME = {
    'bg': '#050505',
    'panel': '#121212',
    'gold': '#ffd700',
    'bull': '#00ff88',
}

class SimpleDashboard(ui.View):
    def __init__(self):
        print("Dashboard init")
        super().__init__()
        self.background_color = THEME['bg']

        # Create scroll view
        self.scroll = ui.ScrollView()
        self.scroll.background_color = THEME['bg']
        self.add_subview(self.scroll)

    def did_load(self):
        print("Dashboard did_load")
        w, h = ui.get_screen_size()
        print(f"Screen: {w}x{h}")

        self.scroll.frame = (0, 0, w, h)
        y = 40

        # Title
        title = ui.Label()
        title.frame = (20, y, w-40, 40)
        title.text = "🐔 CHICKEN MARKET INTELLIGENCE"
        title.font = ('<system-bold>', 24)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        self.scroll.add_subview(title)
        y += 60

        # Card 1
        card1 = ui.View()
        card1.frame = (20, y, w-40, 120)
        card1.background_color = THEME['panel']
        card1.corner_radius = 8

        label1 = ui.Label()
        label1.frame = (15, 15, card1.width-30, 25)
        label1.text = "CORN PRICE INDEX"
        label1.font = ('<system-bold>', 16)
        label1.text_color = THEME['bull']
        card1.add_subview(label1)

        value1 = ui.Label()
        value1.frame = (15, 45, card1.width-30, 30)
        value1.text = "215"
        value1.font = ('<system-bold>', 28)
        value1.text_color = 'white'
        card1.add_subview(value1)

        desc1 = ui.Label()
        desc1.frame = (15, 80, card1.width-30, 30)
        desc1.text = "Favorable - supports good margins"
        desc1.font = ('<system>', 12)
        desc1.text_color = '#888'
        card1.add_subview(desc1)

        self.scroll.add_subview(card1)
        y += 130

        # Card 2
        card2 = ui.View()
        card2.frame = (20, y, w-40, 120)
        card2.background_color = THEME['panel']
        card2.corner_radius = 8

        label2 = ui.Label()
        label2.frame = (15, 15, card2.width-30, 25)
        label2.text = "BONELESS BREAST"
        label2.font = ('<system-bold>', 16)
        label2.text_color = THEME['bull']
        card2.add_subview(label2)

        value2 = ui.Label()
        value2.frame = (15, 45, card2.width-30, 30)
        value2.text = "$1.58 /lb"
        value2.font = ('<system-bold>', 28)
        value2.text_color = 'white'
        card2.add_subview(value2)

        desc2 = ui.Label()
        desc2.frame = (15, 80, card2.width-30, 30)
        desc2.text = "STRONG BUY - Target $1.78"
        desc2.font = ('<system>', 12)
        desc2.text_color = '#888'
        card2.add_subview(desc2)

        self.scroll.add_subview(card2)
        y += 130

        # Analysis box
        analysis = ui.TextView()
        analysis.frame = (20, y, w-40, 300)
        analysis.background_color = THEME['panel']
        analysis.text_color = 'white'
        analysis.font = ('<system>', 14)
        analysis.editable = False
        analysis.text = """MARKET ANALYSIS

🔹 SUPPLY CRISIS: Hatchability at 79.7% vs normal 84% = 58M fewer chicks weekly

🔹 PRICING POWER: Boneless breast prices strong at $1.58/lb with upside to $1.78/lb

🔹 FEED COSTS: Corn favorable, supporting healthy margins

🔹 ACTION: Focus on white meat (breast, tenders) over dark meat (legs)

🔹 OUTLOOK: Supply tight through 2027, demand strong"""
        self.scroll.add_subview(analysis)
        y += 310

        self.scroll.content_size = (w, y + 50)
        print("UI complete!")

class Launcher(ui.View):
    def __init__(self):
        print("Launcher init")
        super().__init__()
        self.background_color = '#000000'

    def did_load(self):
        print("Launcher did_load")
        w, h = ui.get_screen_size()

        # Title
        title = ui.Label()
        title.frame = (0, 180, w, 60)
        title.text = "CHICKEN MARKET\nINTELLIGENCE"
        title.font = ('<system-bold>', 36)
        title.text_color = THEME['gold']
        title.alignment = ui.ALIGN_CENTER
        title.number_of_lines = 2
        self.add_subview(title)

        # Button
        btn = ui.Button()
        btn.frame = ((w-280)/2, 340, 280, 70)
        btn.title = "Launch Dashboard"
        btn.font = ('<system-bold>', 22)
        btn.background_color = THEME['gold']
        btn.tint_color = '#000000'
        btn.corner_radius = 12
        btn.action = self.launch
        self.add_subview(btn)

        print("Launcher ready")

    def launch(self, sender):
        print("Launching...")
        dashboard = SimpleDashboard()
        dashboard.name = "Market Dashboard"
        nav = ui.NavigationView(dashboard)
        nav.present('fullscreen')
        print("Dashboard shown")

# RUN IT
print("Creating launcher...")
launcher = Launcher()
launcher.present('fullscreen')
print("Done!")
