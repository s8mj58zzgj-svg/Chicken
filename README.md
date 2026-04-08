# 🐔🥚 Market Intelligence Platform

**Professional-grade market analysis and price forecasting for protein and agricultural commodities**

Built for Pythonista on iPad | Real-time USDA & FRED API integration

---

## 🎯 Overview

This repository contains **TWO SEPARATE** market intelligence platforms:

### 1️⃣ CEO Market Intelligence (Chicken-Focused)
**Launch:** `python launcher.py`

- **Poultry Market Dashboard**: Broilers, processed products, 90-day forecasts
- **Egg Market Dashboard**: Layer operations, retail pricing, HPAI risk analysis
- **Cold Storage**: Inventory tracking
- **Consumer Economics**: Food service & retail trends
- **Focus**: Deep analysis of chicken/egg markets

### 2️⃣ Protein Markets Intelligence (Multi-Commodity) ⭐ NEW
**Launch:** `python launch_protein_markets.py`

- **7 Market Categories**: Beef, Dairy, Poultry, Eggs, Pork, Turkey, Grains
- **16+ API Endpoints**: Comprehensive FRED & USDA data integration
- **PRO Features**: Charts, forecasting, alerts, export capabilities
- **Focus**: Comparative analysis across all protein markets

> 📖 **See [PROTEIN_MARKETS_SETUP.md](PROTEIN_MARKETS_SETUP.md) for complete protein markets documentation**

---

## 🚀 Quick Start

### For Chicken/Egg Markets:
```python
python launcher.py
```

### For Protein Markets (All Commodities):
```python
python launch_protein_markets.py
# Choose PRO or Standard dashboard
```

---

## 📁 Project Structure

```
Chicken/
├── main.py                 # Main navigation & entry point
├── config.py               # API keys, theme configuration
├── data_engine.py          # Data fetching, caching, API management
├── ui_components.py        # Reusable UI components
├── poultry_dashboard.py    # Poultry/chicken market dashboard
├── egg_dashboard.py        # Egg market dashboard
└── README.md               # This file
```

### Module Breakdown

#### `config.py`
- API credentials (USDA, FRED)
- Color theme definitions
- FRED series ID mappings for all market indicators

#### `data_engine.py`
- Centralized data fetching engine
- API caching (5-minute TTL for performance)
- Error handling and fallback values
- Market snapshot aggregation

#### `ui_components.py`
- `InsightCard`: Reusable metric display cards
- `ForecastCard`: Price forecast cards with charts
- `HeaderLabel`: Section headers
- `render_chart()`: Matplotlib chart generation

#### `poultry_dashboard.py`
- 8 major analysis sections:
  1. Macro Arbitrage & Protein Competition
  2. Global Risk & Trade Flow
  3. Biological Funnel & Supply Dynamics
  4. Feed & Logistics Costs
  5. Processing & Labor Dynamics
  6. Cold Storage Inventory
  7. Price Matrix & Forecasts (8 product cuts)
  8. Analyst Verdict

#### `egg_dashboard.py`
- 7 major analysis sections:
  1. Layer Flock Status
  2. HPAI & Biosecurity Risk
  3. Feed & Production Costs
  4. Market Structure & Pricing
  5. Cold Storage Inventory
  6. Price Forecasts (5 product segments)
  7. Analyst Verdict

#### `main.py`
- Navigation interface
- Market selector screen
- Dashboard launcher

---

## 🚀 Getting Started

### Prerequisites

**For Pythonista (iPad):**
- Pythonista 3 app installed
- Internet connection (for API calls)
- Modules required: `ui`, `requests`, `matplotlib` (all included in Pythonista)

### Installation

1. Copy all `.py` files to your Pythonista directory
2. Open `main.py` in Pythonista
3. Tap the ▶️ Run button

### API Keys

The app comes with embedded API keys:
- **USDA NASS**: `lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC`
- **FRED**: `bffd29d45a9a9eb8e0ab3dabf716b586`

**Note**: These are your personal keys. Keep them secure. For production use, consider moving them to environment variables.

---

## 📊 Dashboard Features

### Poultry Market Dashboard

**Key Metrics Tracked:**
- **Macro Indicators**: Beef/pork spreads, dining premiums, QSR traffic
- **Biology**: Hatchability rates, placements, feed conversion
- **Trade Risk**: Export volumes, Brazil competition, HPAI outbreaks
- **Processing**: Capacity utilization, labor shortages, automation
- **Storage**: Breast, legs, wings, whole bird inventories
- **Price Forecasts**:
  - Whole Bird (WOG)
  - Boneless/Skinless Breast
  - Boneless/Skinless Thighs
  - Jumbo Wings
  - Leg Quarters
  - Mechanically Separated Chicken (MSC)
  - Paws/Feet (Export)
  - Tenders (Premium)

### Egg Market Dashboard

**Key Metrics Tracked:**
- **Layer Flock**: Total inventory, cage-free %, productivity
- **HPAI Risk**: Bird flu threats, biosecurity costs, supply vulnerability
- **Production Costs**: Feed costs, cage-free conversion economics
- **Market Segments**: Conventional, cage-free, organic, breaking stock
- **Storage**: Shell eggs, frozen products, dried products
- **Price Forecasts**:
  - Conventional (Large)
  - Cage-Free
  - Organic
  - Breaking Stock (Liquid)
  - Export Dried/Frozen

---

## 🎨 UI/UX Features

- **Dark Theme**: Professional trading terminal aesthetic
- **Color-Coded Insights**:
  - 🟢 Green (Bullish)
  - 🔴 Red (Bearish/Risk)
  - 🟡 Orange (Warning)
  - 🔵 Blue (Trade/Logistics)
  - 🟣 Purple (Macro)
  - 🌸 Pink (Biology)
- **Interactive Charts**: 90-day price forecasts with historical context
- **Real-time Data**: Pull-to-refresh for latest market updates
- **Scroll Optimization**: Smooth infinite scrolling for all content
- **iPad Optimized**: Full-screen layouts for maximum information density

---

## 📡 Data Sources

### FRED (Federal Reserve Economic Data)
- Corn Price Index
- Soybean Prices
- Diesel Fuel Prices
- Egg Price Indices (PPI & Retail)
- Consumer Sentiment
- Restaurant Sales

### USDA NASS (National Agricultural Statistics Service)
- Poultry production data
- Layer flock inventories
- Hatchability statistics
- Cold storage reports

### Simulated/Industry Data
- HPAI outbreak tracking
- Export volumes (Mexico, China)
- Processing capacity utilization
- Labor market statistics
- Competitive intelligence (Brazil)

---

## 🔧 Customization

### Adding New Metrics

**Example: Add a new FRED series**

1. Edit `config.py`:
```python
FRED_SERIES = {
    ...
    'new_metric': 'FRED_SERIES_ID',
}
```

2. Fetch in `data_engine.py`:
```python
new_data, new_hist = self.fetch_fred(FRED_SERIES['new_metric'])
```

3. Display in dashboard:
```python
card, h = InsightCard.create(
    "NEW METRIC",
    {"val": value, "unit": "$/unit", "status": "STATUS", "insight": "Analysis here"},
    THEME['color'],
    width, y_pos
)
```

### Customizing Colors

Edit the `THEME` dictionary in `config.py`:
```python
THEME = {
    'bg': '#YOUR_COLOR',
    'bull': '#YOUR_BULLISH_COLOR',
    ...
}
```

---

## 📈 Understanding the Forecasts

### Forecast Methodology

The dashboard uses a **fundamental analysis approach**:

1. **Supply Factors**: Hatchability, placements, flock size
2. **Demand Factors**: Protein spreads, consumer behavior, QSR trends
3. **Cost Inputs**: Feed, energy, labor, processing
4. **Storage Levels**: Inventory tightness/abundance
5. **Risk Premiums**: HPAI, trade restrictions, weather

**Price targets** are based on:
- Historical price relationships
- Supply/demand balance
- Seasonal patterns
- Risk-adjusted expectations

### Reading the Charts

- **Solid Line**: Historical actual prices
- **Dashed Line**: 90-day forecast
- **Color**:
  - Green = Bullish trend
  - Orange/Yellow = Neutral/Warning
  - Red = Bearish trend

---

## 🔒 Data Privacy & Caching

- **Caching**: 5-minute cache for API responses (reduces load, improves speed)
- **No Storage**: No personal data stored
- **API Security**: Keys embedded in code (for personal use only)

---

## 🐛 Troubleshooting

### "No data available"
- Check internet connection
- Verify API keys are valid
- FRED/USDA may have rate limits

### Charts not rendering
- Ensure `matplotlib` is installed in Pythonista
- Check for memory constraints on older iPads

### Slow loading
- First load fetches all data (may take 10-15 seconds)
- Subsequent refreshes use cached data (much faster)
- Consider reducing `limit` parameter in FRED calls for faster response

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Turkey market dashboard
- [ ] Pork market integration
- [ ] Beef market tracker
- [ ] Global grain futures
- [ ] Weather impact modeling
- [ ] Export destination breakdown
- [ ] Historical price database
- [ ] Alert system for price thresholds
- [ ] PDF report generation
- [ ] Data export (CSV/Excel)

### Advanced Analytics
- [ ] Machine learning price predictions
- [ ] Seasonality decomposition
- [ ] Correlation analysis (protein spreads)
- [ ] Monte Carlo risk simulations
- [ ] Scenario planning tools

---

## 📝 Version History

### v2.0.0 (Current)
- ✅ Modular architecture with separate files
- ✅ Comprehensive egg market dashboard
- ✅ Enhanced poultry dashboard (8 sections)
- ✅ Real FRED API integration
- ✅ Data caching engine
- ✅ Professional UI components
- ✅ Navigation system

### v1.0.0 (Legacy)
- Single-file poultry dashboard
- Basic forecasting
- Simulated data only

---

## 📞 Support & Feedback

**Issues?**
- Check the troubleshooting section
- Review FRED API documentation: https://fred.stlouisfed.org/docs/api/
- Review USDA NASS API: https://quickstats.nass.usda.gov/api

**Feature Requests?**
- Add to the "Future Enhancements" section
- Consider contributing improvements

---

## ⚖️ License & Disclaimer

**For Educational/Personal Use Only**

This tool provides market analysis based on publicly available data. It is **not financial advice**. Always conduct your own research and consult professionals before making trading or business decisions.

**Data Sources**: USDA, Federal Reserve (FRED), industry reports
**Accuracy**: Best-effort basis. API data may have delays or errors.

---

## 🙏 Acknowledgments

- **USDA NASS**: Agricultural production data
- **Federal Reserve**: Economic indicators (FRED)
- **Pythonista**: iOS Python development platform
- **Matplotlib**: Charting and visualization

---

**Built with 🐔 for the poultry industry**

*Last Updated: 2026-01-17*
