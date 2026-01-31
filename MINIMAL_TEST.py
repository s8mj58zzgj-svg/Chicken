"""
ABSOLUTE MINIMUM TEST - If this doesn't work, nothing will
"""
import ui

class MinimalView(ui.View):
    def __init__(self):
        super().__init__()
        self.background_color = 'red'  # RED so you know it loaded

        # Add label IMMEDIATELY in __init__ (not did_load)
        label = ui.Label()
        label.text = "HELLO WORLD"
        label.font = ('<system-bold>', 40)
        label.text_color = 'white'
        label.frame = (50, 200, 300, 100)
        self.add_subview(label)

        print("MinimalView created and label added")

# Create and show immediately
v = MinimalView()
v.present('fullscreen')
print("View presented")
