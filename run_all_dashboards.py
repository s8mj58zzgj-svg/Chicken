#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
PROTEIN MARKET INTELLIGENCE - ALL DASHBOARDS
═══════════════════════════════════════════════════════════════
Run this file to access all market dashboards in your browser
"""

import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8000

def open_browser():
    """Open browser after short delay"""
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  🥩 PROTEIN MARKET INTELLIGENCE PLATFORM")
    print("="*70)
    print("\n  Starting server...")
    print("  Opening browser automatically...")
    print(f"\n  Access at: http://localhost:{PORT}")
    print("\n  Press Ctrl+C to stop")
    print("="*70 + "\n")

    # Open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start simple HTTP server
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
