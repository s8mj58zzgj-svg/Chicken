# 📱 PROTEIN MARKETS PRO - COMPLETE GUIDE

## 🚀 What's New in PRO Version

**Protein Markets PRO** is the enhanced version with advanced analytics and features:

### ✨ NEW FEATURES

1. **📈 Price Trend Charts** - Historical price graphs for visual analysis
2. **🔔 Price Alerts** - Set custom thresholds and get notifications
3. **📥 Export to CSV** - Download market data for spreadsheet analysis
4. **🌾 Grains & Feed** - New tab for corn, soybeans, wheat, oats, rice
5. **📊 Price Forecasting** - 3-month predictions using linear regression
6. **📉 Visual Analytics** - Beautiful charts with 24-month history
7. **⚡ Enhanced Performance** - Faster data loading and caching

---

## 📋 WHAT'S INCLUDED

### Commodity Coverage

**7 TABBED SECTIONS:**

1. **🥩 Beef & Dairy** (with charts)
   - Beef retail prices + historical chart
   - Cattle markets (live, feeder)
   - Milk, cheese, butter + historical chart
   - Feed costs

2. **🐔 Poultry**
   - Broiler production metrics
   - Pricing matrix (breast, wings, legs, tenders)
   - Biological performance indicators

3. **🥚 Eggs**
   - Layer flock status
   - Production systems breakdown
   - Retail pricing by type
   - HPAI risk tracking

4. **🥓 Pork**
   - Bellies & bacon markets
   - Hams & primals
   - Hog supply metrics
   - Cold storage

5. **🦃 Turkey**
   - Production statistics
   - State-by-state breakdown
   - Pricing (whole, processed)
   - Cold storage levels

6. **🌾 Grains & Feed** (NEW! with charts)
   - Corn prices + 24-month chart
   - Soybeans + 24-month chart
   - Wheat, oats, rice
   - Feed cost impact analysis

7. **📊 Price Forecasts** (NEW!)
   - Beef 3-month forecast
   - Corn 3-month forecast
   - Trend indicators
   - Forecast disclaimer

---

## 🎯 HOW TO USE NEW FEATURES

### 📈 Viewing Price Charts

Charts appear automatically in these tabs:
- **Beef & Dairy**: Beef retail price, Milk price
- **Grains**: Corn price, Soybean price

**What charts show:**
- 24 months of historical data
- Month-by-month price movements
- Visual trend identification
- Color-coded by commodity

**How to use:**
1. Navigate to Beef or Grains tab
2. Scroll down to see charts
3. Charts update when you tap 🔄 Refresh

---

### 🔔 Setting Up Price Alerts

Price alerts notify you when commodities hit your target prices.

**How to set an alert:**

1. Edit `protein_markets_pro.py`
2. Add this code near line 750 (in the `main()` function):

```python
# Set custom alerts
app.alert_mgr.set_alert('beef', 'retail', 8.50, 'above')  # Alert when beef > $8.50
app.alert_mgr.set_alert('corn', 'price', 4.00, 'below')   # Alert when corn < $4.00
app.alert_mgr.set_alert('eggs', 'retail', 3.50, 'above')  # Alert when eggs > $3.50
```

**Alert parameters:**
- **commodity**: 'beef', 'corn', 'eggs', 'pork', etc.
- **price_type**: 'retail', 'wholesale', 'price'
- **threshold**: Dollar amount
- **direction**: 'above' or 'below'

**Viewing active alerts:**
- Tap the 🔔 button (top left)
- Shows all active alerts and their thresholds

**How alerts work:**
- App checks prices on each refresh
- If threshold is crossed, you get a HUD notification
- Alerts persist across app restarts (saved to file)

---

### 📥 Exporting Data to CSV

Export current market data for analysis in Excel, Google Sheets, etc.

**How to export:**

1. Tap the **📥 Export button** (top left)
2. Data is saved to: `~/Documents/protein_markets_YYYYMMDD_HHMMSS.csv`
3. Success notification appears

**What gets exported:**
- Commodity name
- Metric (e.g., "Retail Price")
- Current value
- Unit ($/lb, $/bu, etc.)
- Timestamp

**CSV format example:**
```
Commodity,Metric,Value,Unit,Timestamp
Beef,Retail Price,8.15,$/lb,2026-01-30 14:35:22
Grains,Corn,4.25,$/bu,2026-01-30 14:35:22
Dairy,Milk,3.89,$/gal,2026-01-30 14:35:22
```

**Accessing exported files:**
1. Open **Files** app on iOS
2. Navigate to **On My iPad/iPhone** → **Pythonista** → **Documents**
3. Find `protein_markets_*.csv` files
4. Tap to open in Numbers, Excel, or share via email

---

### 📊 Using Price Forecasts

The **Forecast tab** uses linear regression to predict prices 3 months ahead.

**What you'll see:**
- Current price
- Month +1, +2, +3 forecasts
- Trend indicator (Rising 📈, Falling 📉, Stable ➡️)

**Commodities forecasted:**
- **Beef** retail prices
- **Corn** prices
- More commodities can be added

**How forecasts are calculated:**
1. Takes last 12 months of historical data
2. Fits a linear trend line
3. Projects 3 months forward
4. Shows percentage change

**⚠️ IMPORTANT:**
- These are **simple statistical projections**
- **NOT financial advice**
- Actual prices affected by many factors (weather, disease, policy, demand)
- Use for **general trend awareness** only

---

### 🌾 Grains & Feed Tab

Critical for understanding **feed costs** that drive protein prices.

**Why grains matter:**
- **Poultry feed**: 60% corn, 30% soybeans
- **Swine feed**: 70% corn, 20% soybeans
- **Cattle**: Corn-heavy diets in feedlots

**What's tracked:**
- Corn ($/bushel) + 24-month chart
- Soybeans ($/bushel) + 24-month chart
- Wheat ($/bushel)
- Oats ($/bushel)
- Rice ($/ton)

**How to use:**
- Rising corn = higher poultry/pork costs ahead
- Compare grain trends to protein prices
- Identify margin pressure for producers

---

## 🛠️ BUTTONS & CONTROLS

### Top Bar (Left to Right)

**📥 Export** - Export current data to CSV file

**🔔 Alerts** - View active price alerts

**PROTEIN MARKETS PRO** - App title

**🔄 Refresh** - Clear cache and reload all data

### Tab Bar

Tap any tab to switch views:
- 🥩 Beef
- 🐔 Poultry
- 🥚 Eggs
- 🥓 Pork
- 🦃 Turkey
- 🌾 Grains
- 📊 Forecast

---

## 📱 ADD TO HOME SCREEN

Same as basic version:

1. Open **Pythonista**
2. Find `protein_markets_pro.py`
3. Tap **wrench icon** ⚙️
4. Select **"Home Screen"**
5. Choose icon (📊 or 📈 recommended for PRO)
6. Tap **"Add"**

Now you have PRO version on your home screen!

---

## 🔧 CUSTOMIZATION

### Adding More Forecasts

Edit the `ForecastTab` class around line 500:

```python
# Add eggs forecast
eggs, eggs_history = self.data.fetch_fred('APU0000708111', limit=12)
if eggs_history:
    forecasts = self.forecaster.linear_forecast(eggs_history, periods_ahead=3)
    # ... create card ...
```

### Changing Chart Colors

Edit `THEME` dictionary (line 30):

```python
THEME = {
    'beef': '#FF0000',      # Change beef to bright red
    'grains': '#00FF00',    # Change grains to bright green
    # ... etc
}
```

### Adding More Alerts

In `main()` function, add:

```python
app.alert_mgr.set_alert('milk', 'retail', 4.00, 'above')
app.alert_mgr.set_alert('turkey', 'wholesale', 1.50, 'below')
```

### Adjusting Forecast Window

Change `periods_ahead` parameter:

```python
forecasts = self.forecaster.linear_forecast(beef_history, periods_ahead=6)  # 6 months instead of 3
```

---

## 📊 DATA SOURCES

All data is **real-time** from authoritative sources:

- **FRED (Federal Reserve)**: Retail prices, economic indicators
- **USDA**: Production metrics, cold storage
- **Cache**: 5 minutes for fast loading

**Series tracked:**
- `APU0000FC1101` - Beef retail
- `APU0000703112` - Ground beef
- `APU0000709112` - Milk
- `PMAIZMTUSDM` - Corn
- `PSOYBUSDM` - Soybeans
- `PWHEAMTUSDM` - Wheat
- And 40+ more...

---

## ❓ TROUBLESHOOTING

**Charts not appearing:**
- Check internet connection
- Tap 🔄 Refresh
- Verify matplotlib is installed in Pythonista

**Alerts not triggering:**
- Make sure alerts are set up in code
- Check threshold values are correct
- Tap 🔔 to verify alerts are active

**Export fails:**
- Ensure Documents folder exists
- Check Pythonista has file permissions
- Try exporting again

**Forecasts show "No data":**
- Need at least 3 months of historical data
- Tap 🔄 to refresh data
- Some series may have limited history

**App loads slowly:**
- First load fetches 24 months of data
- Subsequent loads use cache
- Reduce chart history in code if needed

---

## 🆚 PRO vs BASIC COMPARISON

| Feature | Basic | PRO |
|---------|-------|-----|
| Commodities | 6 tabs | 7 tabs (added Grains) |
| Charts | ❌ None | ✅ 4 charts (Beef, Milk, Corn, Soy) |
| Forecasting | ❌ | ✅ 3-month predictions |
| Alerts | ❌ | ✅ Custom price alerts |
| Export | ❌ | ✅ CSV export |
| Data History | 12 months | 24 months |
| File Size | 28 KB | 40+ KB |

**Which should you use?**
- **Basic**: Simple price checking, quick loading
- **PRO**: Deep analysis, forecasting, alerts, export

You can keep both! They're separate files.

---

## 🎓 ADVANCED TIPS

### Trend Analysis Strategy

1. **Check Grains first** - Leading indicator for protein costs
2. **Compare charts** - Look for correlations
3. **Watch spreads** - Cattle, pork cuts, etc.
4. **Monitor forecasts** - Anticipate movements
5. **Set alerts** - Get notified of major moves

### Using Exports for Analysis

Export daily/weekly and:
- Track price changes over time in Excel
- Calculate your own metrics
- Create custom charts
- Share with team/clients

### Optimizing Performance

Edit line 59 to reduce cache TTL:
```python
self.cache_ttl = 180  # 3 minutes instead of 5
```

Or increase for slower updates:
```python
self.cache_ttl = 600  # 10 minutes
```

---

## 📂 FILES

- `protein_markets_pro.py` - PRO version (this file) ⭐
- `protein_markets_app.py` - Basic version (still available)
- `PROTEIN_MARKETS_PRO_GUIDE.md` - This guide
- `~/Documents/protein_alerts.json` - Saved alerts
- `~/Documents/protein_markets_*.csv` - Exported data

---

## 🔮 FUTURE ENHANCEMENTS

Possible additions:
- 📧 Email/SMS alerts
- 📄 PDF export with charts
- 🌐 More commodities (lamb, seafood, produce)
- 📉 Technical indicators (RSI, MACD)
- 🤖 Machine learning forecasts
- 📱 Widget support
- 🔗 News integration

Let me know what you want added next!

---

## 💡 TIPS & TRICKS

1. **Swipe smoothly** - Charts render fast, but scroll gently
2. **Landscape mode** - Charts look better in landscape
3. **Regular exports** - Build your own price database
4. **Alert strategically** - Set alerts at key technical levels
5. **Compare forecasts** - Check against USDA official forecasts

---

## 📞 SUPPORT

If you need help:
1. Read this guide thoroughly
2. Check the Troubleshooting section
3. Review code comments in `protein_markets_pro.py`
4. Test with basic version first if PRO has issues

---

**Enjoy your professional market intelligence platform!** 📊🚀
