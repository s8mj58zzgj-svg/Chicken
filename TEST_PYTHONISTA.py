"""
SIMPLE TEST VERSION - Debug the blank screen issue
"""
import ui

print("=== STARTING TEST ===")

# Test 1: Basic UI
try:
    print("Test 1: Creating basic view...")

    class TestLauncher(ui.View):
        def __init__(self):
            print("  __init__ called")
            super().__init__()
            self.background_color = '#000000'

        def did_load(self):
            print("  did_load called!")
            w, h = ui.get_screen_size()
            print(f"  Screen size: {w}x{h}")

            # Add a simple label
            label = ui.Label()
            label.frame = (50, 200, w-100, 100)
            label.text = "TEST\nIF YOU SEE THIS\nIT WORKS!"
            label.font = ('<system-bold>', 32)
            label.text_color = '#00FF00'
            label.alignment = ui.ALIGN_CENTER
            label.number_of_lines = 3
            self.add_subview(label)
            print("  Label added")

            # Add a button
            btn = ui.Button()
            btn.frame = (50, 350, w-100, 60)
            btn.title = "PRESS ME"
            btn.font = ('<system-bold>', 24)
            btn.background_color = '#FF0000'
            btn.action = self.button_pressed
            self.add_subview(btn)
            print("  Button added")

        def button_pressed(self, sender):
            print("BUTTON PRESSED!")
            import console
            console.alert("Success!", "The UI is working!", "OK", hide_cancel_button=True)

    print("Test 1: Presenting view...")
    launcher = TestLauncher()
    launcher.present('fullscreen')
    print("Test 1: COMPLETE")

except Exception as e:
    print(f"ERROR in Test 1: {e}")
    import traceback
    traceback.print_exc()
