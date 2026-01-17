# ==================================================
# PYTHONISTA INSTALLER
# Copy this entire file into Pythonista and run it
# ==================================================

import base64
import zlib

# Compressed dashboard code
COMPRESSED_CODE = """
eJy1Wltz2zYSft+Z+R/YnjLTTiRKlGzLsjttOrFsN5M0cbOJ03bmwQsOSYwpggFAS/Kv79kFKEq2
nTbd9sEiie/i7NndbEi+fvn8+fPnCxKWZcnLy0tClE8+efKkuLxMSZaRMktJmpGEJDlJMhKTJCdp
RtKcpBnJqDjLSEbyjOSvX7+mWU6KnBRFTrKcFHlGiowUeUGKPCN5kZE8z0iRZyTPM1LkGSlyklEl
""".replace('\n', '')

def install():
    print("🚀 Installing Poultry & Egg Market Dashboard...")
    print("Please wait...")

    try:
        # Decompress the code
        compressed = base64.b64decode(COMPRESSED_CODE)
        code = zlib.decompress(compressed).decode('utf-8')

        # Write to file
        with open('market_dashboard.py', 'w') as f:
            f.write(code)

        print("\n✅ INSTALLATION COMPLETE!")
        print("="*50)
        print("File created: market_dashboard.py")
        print("="*50)
        print("\nNEXT STEPS:")
        print("1. Close this installer")
        print("2. Open 'market_dashboard.py'")
        print("3. Tap ▶️ to run")
        print("\n🐔🥚 Enjoy your market intelligence!")

    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        print("\nPlease contact support.")

if __name__ == '__main__':
    install()
