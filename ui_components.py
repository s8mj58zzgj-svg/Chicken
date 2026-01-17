# ==================================================
# UI COMPONENTS - Reusable UI Building Blocks
# ==================================================

import ui
import io
import matplotlib.pyplot as plt
from config import THEME, MARGIN

def render_chart(title, data, color, width=5, height=3.0):
    """Render a price trend chart"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(THEME['panel'])
    ax.set_facecolor(THEME['panel'])

    y = data['hist'] + data['fut']
    x_len = len(y)
    x = range(x_len)
    cutoff = len(data['hist']) - 1

    # Historical line
    ax.plot(x[:cutoff+1], y[:cutoff+1], color=color, linewidth=2.5, label='Actual')
    # Forecast line
    ax.plot(x[cutoff:], y[cutoff:], color=color, linestyle='--', linewidth=2.5, alpha=0.7)
    ax.scatter([x[-1]], [y[-1]], color=color, s=50, zorder=5)

    ax.grid(color='#333', linestyle=':', linewidth=0.5)
    ax.yaxis.set_visible(True)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', colors='#666', labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_color('#333')

    ax.set_xticks([0, cutoff, x_len-1])
    ax.set_xticklabels(['History', 'Now', '90 Days'], fontsize=8, color='#888')
    ax.set_title(title, fontsize=11, color='#aaa', pad=10, loc='left')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close()
    return ui.Image.from_data(buf.getvalue())


class InsightCard:
    """Reusable insight card component"""

    @staticmethod
    def create(name, data, color, width, y_pos):
        h = 130
        card = ui.View(frame=(MARGIN, y_pos, width, h))
        card.background_color = THEME['panel']
        card.corner_radius = 8
        card.border_width = 1
        card.border_color = '#222'

        # Title
        t = ui.Label(frame=(15, 12, width-20, 20))
        t.text = name
        t.font = ('<system-bold>', 14)
        t.text_color = color
        card.add_subview(t)

        # Value
        v = ui.Label(frame=(15, 35, 200, 30))
        v.text = f"{data.get('val', '--')} {data.get('unit', '')}"
        v.font = ('<system-bold>', 24)
        v.text_color = 'white'
        card.add_subview(v)

        # Status badge
        b = ui.Label(frame=(width-115, 12, 100, 20))
        b.text = data.get('status', 'N/A')
        b.font = ('<system-bold>', 10)
        b.alignment = ui.ALIGN_CENTER
        b.text_color = 'black'
        b.background_color = color
        b.corner_radius = 4
        card.add_subview(b)

        # Insight text
        txt = ui.Label(frame=(15, 70, width-30, 50))
        txt.text = f"THESIS: {data.get('insight', '')}"
        txt.font = ('<system>', 12)
        txt.text_color = '#ccc'
        txt.number_of_lines = 3
        card.add_subview(txt)

        return card, h


class ForecastCard:
    """Reusable forecast card with chart"""

    @staticmethod
    def create(name, data, width, y_pos, dates_dict):
        h = 320
        card = ui.View(frame=(MARGIN, y_pos, width, h))
        card.background_color = THEME['panel']
        card.corner_radius = 8

        # Title
        l = ui.Label(frame=(15, 10, width-30, 25))
        l.text = name
        l.font = ('<system-bold>', 16)
        l.text_color = 'white'
        card.add_subview(l)

        # Calculate metrics
        curr = data.get('current', 0)
        targ = data.get('target', 0)
        pct = ((targ - curr)/curr)*100 if curr else 0
        d90 = dates_dict.get('d90', 'Q1')

        # Stats
        ForecastCard._add_stat(card, 15, 40, "SPOT PRICE", f"${curr:.2f}")
        col = THEME['bull'] if pct > 0 else THEME['bear']
        ForecastCard._add_stat(card, 120, 40, f"TARGET ({d90})", f"${targ:.2f}", col)
        ForecastCard._add_stat(card, 240, 40, "DELTA", f"{pct:+.1f}%", col)

        # Chart
        img = ui.ImageView(frame=(15, 90, width-30, 140))
        img.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
        col_c = THEME['bull'] if "BUY" in data.get('trend', '') or "BULL" in data.get('trend', '') else THEME['warn']
        img.image = render_chart(f"{name} Trend", data, col_c)
        card.add_subview(img)

        # Logic
        lbl = ui.Label(frame=(15, 240, width-30, 60))
        lbl.text = f"LOGIC: {data.get('logic', '')}"
        lbl.font = ('<system>', 12)
        lbl.text_color = THEME['sub']
        lbl.number_of_lines = 3
        card.add_subview(lbl)

        return card, h

    @staticmethod
    def _add_stat(parent, x, y, label, val, color='#fff'):
        l = ui.Label(frame=(x, y, 100, 15))
        l.text = label
        l.font = ('<system>', 10)
        l.text_color = THEME['sub']
        parent.add_subview(l)

        v = ui.Label(frame=(x, y+15, 100, 20))
        v.text = val
        v.font = ('<system-bold>', 16)
        v.text_color = color
        parent.add_subview(v)


class HeaderLabel:
    """Section header component"""

    @staticmethod
    def create(scroll_view, text, color, y, width):
        l = ui.Label(frame=(MARGIN, y, width, 25))
        l.text = text
        l.font = ('<system-bold>', 12)
        l.text_color = color
        scroll_view.add_subview(l)
        return y + 30
