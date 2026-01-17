# ==================================================
# CONFIGURATION - API Keys & Theme
# ==================================================

# API Configuration
USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

# Layout Constants
MARGIN = 40

# Color Theme
THEME = {
    'bg': '#050505',           # Background
    'panel': '#121212',        # Card background
    'header': '#1a1a1a',       # Header background
    'text': '#e0e0e0',         # Primary text
    'sub': '#888888',          # Secondary text
    'bull': '#00ff88',         # Green (Bullish)
    'bear': '#ff4444',         # Red (Bearish)
    'warn': '#ffaa00',         # Orange (Warning)
    'macro': '#aa00ff',        # Purple (Macro)
    'bio': '#ff0088',          # Pink (Biology)
    'cold': '#00ccff',         # Ice Blue (Storage)
    'risk': '#ff3333',         # Red (HPAI/Risk)
    'trade': '#0099ff',        # Blue (Global Trade)
    'gold': '#ffd700',         # Premium/Gold
    'logistics': '#ff9900',    # Diesel/Freight
    'eggs': '#ffdd44',         # Egg market
    'layer': '#ff6b9d',        # Layer operations
    'accent': '#00ccff',       # Accent color
    'neutral': '#888888'       # Neutral
}

# FRED Series IDs for Market Data
FRED_SERIES = {
    # Grains & Feed
    'corn': 'PMAIZMTUSDM',              # Global Corn Price Index
    'soybean': 'PSOYBUSDM',             # Soybean Price
    'wheat': 'PWHEAMTUSDM',             # Wheat Price

    # Protein Prices
    'beef': 'APU0000FC1101',            # Beef prices
    'pork': 'APU0000FD3101',            # Pork prices

    # Energy
    'diesel': 'GASDESW',                # Diesel Retail Prices
    'crude': 'DCOILWTICO',              # WTI Crude Oil
    'natgas': 'DHHNGSP',                # Natural Gas

    # Economic Indicators
    'cpi': 'CPIAUCSL',                  # Consumer Price Index
    'ppi_food': 'WPU02',                # PPI Food
    'employment': 'PAYEMS',             # Employment
    'consumer_sentiment': 'UMCSENT',    # Consumer Sentiment

    # Food Service
    'restaurant_sales': 'RRSFS',        # Restaurant Sales
    'grocery_sales': 'RSGASS',          # Grocery Store Sales

    # Egg Specific
    'egg_price_index': 'WPU01740301',   # PPI Eggs
    'egg_retail': 'APU0000708111',      # Retail Egg Prices
}
