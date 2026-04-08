# Protein Markets Intelligence - Standalone Platform

## Overview
The **Protein Markets Intelligence** platform has been separated from the CEO Market Intelligence launcher into its own dedicated system. This separation provides better organization and allows the comprehensive protein markets dashboard to utilize all available API resources independently.

## Why Separate?

### Before (Nested Structure)
- CEO Market Intelligence → Market Intelligence Tabs → Protein data buried inside
- Limited API utilization
- Confusing navigation
- Protein markets treated as subset of chicken markets

### After (Standalone Structure)
- **CEO Market Intelligence** (chicken_market_launcher.py) → Focused on poultry/eggs/cold storage
- **Protein Markets Intelligence** (protein_markets_launcher.py) → Comprehensive protein analysis

## API Coverage

The Protein Markets platform now fully utilizes **all 7 API categories** from FRED & USDA:

### 1. **Grains & Feed** (3 series)
- Corn (PMAIZMTUSDM)
- Soybeans (PSOYBUSDM)
- Wheat (PWHEAMTUSDM)

### 2. **Protein Prices** (2 series)
- Beef (APU0000FC1101)
- Pork (APU0000FD3101)

### 3. **Energy & Logistics** (3 series)
- Diesel (GASDESW)
- Crude Oil (DCOILWTICO)
- Natural Gas (DHHNGSP)

### 4. **Economic Indicators** (4 series)
- CPI (CPIAUCSL)
- PPI Food (WPU02)
- Employment (PAYEMS)
- Consumer Sentiment (UMCSENT)

### 5. **Food Service** (2 series)
- Restaurant Sales (RRSFS)
- Grocery Sales (RSGASS)

### 6. **Egg Specific** (2 series)
- Egg PPI (WPU01740301)
- Egg Retail (APU0000708111)

### 7. **Additional Protein Markets**
- Live Cattle, Feeder Cattle, Dairy products, etc.

## Launch Options

### Option 1: PRO Dashboard (Recommended)
```python
python launch_protein_markets.py
```
Then select **"Launch PRO Dashboard"**

**Features:**
- ✅ Price charts with 24-month history
- ✅ Linear regression forecasting
- ✅ Price alerts & notifications
- ✅ CSV/PDF export capabilities
- ✅ All 7 API data sources
- ✅ Advanced analytics

**Tabs:**
1. 🥩 Beef & Dairy
2. 🐔 Poultry
3. 🥚 Eggs
4. 🥓 Pork
5. 🦃 Turkey
6. ❄️ Cold Storage
7. 🌾 Grains & Feed

### Option 2: Standard Dashboard
```python
python launch_protein_markets.py
```
Then select **"Launch Standard Dashboard"**

**Features:**
- ✅ Essential market data
- ✅ Real-time pricing
- ✅ Supply metrics
- ✅ Feed costs
- ⚠️ No charts or forecasting
- ⚠️ No export features

**Tabs:**
1. 🥩 Beef & Dairy
2. 🐔 Poultry
3. 🥚 Eggs
4. 🥓 Pork
5. 🦃 Turkey
6. ❄️ Cold Storage

## File Structure

```
Chicken/
├── config.py                          # Centralized API keys & config
├── data_engine.py                     # Data fetching engine
│
├── CEO MARKET INTELLIGENCE (Chicken-focused)
│   ├── launcher.py                    # Entry point
│   ├── chicken_market_launcher.py     # Launch screen
│   ├── market_intelligence_tabs.py    # Tab system
│   └── [specific dashboards...]
│
├── PROTEIN MARKETS INTELLIGENCE (Multi-commodity)
│   ├── launch_protein_markets.py      # Entry point ⭐ NEW
│   ├── protein_markets_launcher.py    # Launch screen ⭐ NEW
│   ├── protein_markets_app.py         # Standard dashboard (updated)
│   └── protein_markets_pro.py         # PRO dashboard (updated)
│
└── README.md
```

## Configuration

All API keys are centralized in `config.py`:

```python
# API Configuration
USDA_KEY = "your_key_here"
FRED_KEY = "your_key_here"

# FRED Series IDs (7 categories, 16+ endpoints)
FRED_SERIES = {
    'corn': 'PMAIZMTUSDM',
    'soybean': 'PSOYBUSDM',
    # ... etc
}
```

Both dashboards now import from this centralized config, ensuring:
- No duplicate API key management
- Easy updates to add new data series
- Consistent data access across platforms

## Migration Notes

### For Users
- **Old way:** launcher.py → Select Protein tab (if available)
- **New way:** launch_protein_markets.py → Choose PRO or Standard

### For Developers
- Both `protein_markets_app.py` and `protein_markets_pro.py` now import from `config.py`
- No more hardcoded API keys in individual files
- Easy to add new FRED series by updating `config.FRED_SERIES`

## Benefits of Separation

1. **Better Organization** - Clear separation between chicken-focused and multi-protein platforms
2. **Full API Utilization** - Protein markets now use all 7 API categories (16+ endpoints)
3. **Independent Updates** - Can enhance protein markets without affecting chicken intelligence
4. **User Choice** - Dedicated launcher offers PRO vs Standard selection
5. **Maintainability** - Centralized config makes API management easier

## Next Steps

1. Launch the protein markets: `python launch_protein_markets.py`
2. Choose PRO dashboard for full features
3. Explore all 7 tabs (including new Grains & Feed tab)
4. Set up price alerts for your commodities
5. Export data for analysis

## Support

For issues or questions:
- Check that `config.py` has valid API keys
- Ensure all dependencies are installed (matplotlib, numpy, requests)
- Verify Pythonista is up to date
