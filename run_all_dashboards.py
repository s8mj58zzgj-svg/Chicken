#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
PROTEIN MARKET INTELLIGENCE - ALL DASHBOARDS
═══════════════════════════════════════════════════════════════
Run this file to access all market dashboards in your browser
"""

from flask import Flask, render_template_string, send_file
import webbrowser
import threading
import os
from pathlib import Path

app = Flask(__name__)

# Dashboard files
DASHBOARDS = {
    'eggs': 'EggsIntelligencePlatform.html',
    'beef': 'BeefMarketIntelligence.html',
    'dairy': 'DairyBeefIntelligencePlatform.html',
    'pork': 'PorkIntelligencePlatform.html',
    'poultry': 'PoultryIntelligencePlatform.html',
    'institutional': 'InstitutionalProteinIntelligence.html',
}

HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Protein Market Intelligence Hub</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            font-size: 48px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            color: rgba(255,255,255,0.9);
            text-align: center;
            font-size: 18px;
            margin-bottom: 50px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-decoration: none;
            color: #333;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .card h2 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #667eea;
        }
        .card p {
            color: #666;
            line-height: 1.6;
        }
        .emoji {
            font-size: 48px;
            margin-bottom: 15px;
            display: block;
        }
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🥩 Protein Market Intelligence Hub</h1>
        <p class="subtitle">Professional-grade market analytics and intelligence dashboards</p>

        <div class="grid">
            <a href="/dashboard/eggs" class="card">
                <span class="emoji">🥚</span>
                <h2>Eggs Intelligence</h2>
                <p>Comprehensive egg market analytics, pricing trends, and production data</p>
            </a>

            <a href="/dashboard/beef" class="card">
                <span class="emoji">🥩</span>
                <h2>Beef Market</h2>
                <p>Beef market intelligence with pricing, inventory, and demand metrics</p>
            </a>

            <a href="/dashboard/dairy" class="card">
                <span class="emoji">🥛</span>
                <h2>Dairy & Beef</h2>
                <p>Integrated dairy and beef market platform with cross-commodity analysis</p>
            </a>

            <a href="/dashboard/pork" class="card">
                <span class="emoji">🥓</span>
                <h2>Pork Intelligence</h2>
                <p>Comprehensive pork market data, futures, and production analytics</p>
            </a>

            <a href="/dashboard/poultry" class="card">
                <span class="emoji">🍗</span>
                <h2>Poultry Intelligence</h2>
                <p>Complete poultry market analytics including chicken and turkey markets</p>
            </a>

            <a href="/dashboard/institutional" class="card">
                <span class="emoji">📊</span>
                <h2>Institutional Protein</h2>
                <p>Institutional-grade protein intelligence platform for all commodities</p>
            </a>
        </div>

        <div class="footer">
            <p>Real-time USDA data • Professional analytics • Market intelligence</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/dashboard/<name>')
def dashboard(name):
    if name not in DASHBOARDS:
        return "Dashboard not found", 404

    file_path = Path(__file__).parent / DASHBOARDS[name]
    if not file_path.exists():
        return f"Dashboard file not found: {DASHBOARDS[name]}", 404

    return send_file(file_path)

def open_browser():
    """Open browser after short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🥩 PROTEIN MARKET INTELLIGENCE PLATFORM")
    print("="*70)
    print("\n  Starting server...")
    print("  Opening browser automatically...")
    print("\n  Access at: http://localhost:5000")
    print("\n  Press Ctrl+C to stop")
    print("="*70 + "\n")

    # Open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Flask server
    app.run(debug=False, port=5000)
