# ⚡ QUICK START GUIDE

## 🎯 Which App Should You Use?

You now have **TWO** protein markets apps:

### 📱 **protein_markets_app.py** (BASIC)
- ✅ Simple and fast
- ✅ 6 commodity tabs (Beef, Poultry, Eggs, Pork, Turkey, Cold Storage)
- ✅ Current prices and metrics
- ✅ Refresh button
- ⚡ Best for: Quick price checks

### 🚀 **protein_markets_pro.py** (PRO)
- ✅ Everything in Basic, PLUS:
- ✅ **7 tabs** (added Grains & Feed, Forecasting)
- ✅ **📈 Price trend charts** (24-month history)
- ✅ **🔔 Custom price alerts**
- ✅ **📥 Export to CSV**
- ✅ **📊 3-month price forecasts**
- ⚡ Best for: Deep analysis, planning, forecasting

---

## 🚀 GETTING STARTED (5 MINUTES)

### Step 1: Choose Your App

**Want simple price checking?** → Use `protein_markets_app.py`

**Want charts, forecasts, and alerts?** → Use `protein_markets_pro.py`

### Step 2: Run in Pythonista

1. Open **Pythonista** app
2. Find your chosen file
3. Tap ▶️ to run
4. App launches in fullscreen!

### Step 3: Add to Home Screen

1. In Pythonista, find your file
2. Tap **wrench icon** ⚙️ (top right)
3. Select **"Home Screen"**
4. Choose icon:
   - Basic: 🥩 or 📊
   - PRO: 📈 or 🚀
5. Tap **"Add"**
6. **Done!** Tap icon to launch directly

---

## 📚 NAVIGATION BASICS

### Top Bar Buttons

**BASIC VERSION:**
- 🔄 Refresh - Update all data

**PRO VERSION:**
- 📥 Export - Download CSV
- 🔔 Alerts - View active alerts
- 🔄 Refresh - Update all data

### Tabs (Both Versions)

Tap to switch:
- 🥩 **Beef** - Beef & dairy markets
- 🐔 **Poultry** - Broiler production & pricing
- 🥚 **Eggs** - Layer flock & egg prices
- 🥓 **Pork** - Bellies, bacon, hams, primals
- 🦃 **Turkey** - Turkey production & pricing
- ❄️ **Cold** - Cold storage inventory (Basic only)
- 🌾 **Grains** - Corn, soybeans, wheat (PRO only)
- 📊 **Forecast** - Price predictions (PRO only)

---

## 🎓 COMMON TASKS

### ✅ Check Current Beef Price
1. Open app
2. Tap **🥩 Beef** tab (default view)
3. See "Composite Retail: $X.XX/lb"

### ✅ View Price History (PRO only)
1. Open PRO app
2. Tap **🥩 Beef** or **🌾 Grains** tab
3. Scroll down to see charts
4. Charts show 24 months

### ✅ Get 3-Month Forecast (PRO only)
1. Open PRO app
2. Tap **📊 Forecast** tab
3. See predictions for beef, corn, etc.

### ✅ Export Data (PRO only)
1. Tap **📥 Export** button (top left)
2. File saved to Documents folder
3. Open **Files** app → Pythonista → Documents
4. Find `protein_markets_*.csv`

### ✅ Set Price Alert (PRO only)
1. Open `protein_markets_pro.py` in editor
2. Find `main()` function (bottom of file)
3. Add before `view.present()`:
   ```python
   app.alert_mgr.set_alert('beef', 'retail', 8.50, 'above')
   ```
4. Save and run
5. Get notified when beef > $8.50/lb

### ✅ Refresh Data
1. Tap **🔄** button (top right)
2. Wait 2-3 seconds
3. All tabs update with fresh data

---

## 📖 LEARNING MORE

### Full Documentation

- **Basic version**: See `PROTEIN_APP_INSTRUCTIONS.md`
- **PRO version**: See `PROTEIN_MARKETS_PRO_GUIDE.md`

### Understanding the Data

**Prices shown:**
- All prices are **real-time** from FRED and USDA APIs
- Updated every 5 minutes (cached)
- Tap 🔄 to force immediate update

**Production metrics:**
- Weekly slaughter numbers
- Flock/herd sizes
- Biological performance indicators
- All from USDA official reports

**Charts (PRO):**
- 24 months of historical data
- Month-by-month price movements
- Color-coded by commodity

**Forecasts (PRO):**
- Linear regression predictions
- 3-month projections
- Trend indicators
- ⚠️ Not financial advice!

---

## ❓ FAQ

**Q: Do I need internet?**
A: Yes, for initial data load. Then cached for 5 minutes.

**Q: Can I use both apps?**
A: Yes! They're separate files. Add both to home screen.

**Q: How often should I refresh?**
A: Data auto-refreshes every 5 minutes. Manual refresh if you need latest.

**Q: Where do exports save?**
A: `Files app` → `On My iPad/iPhone` → `Pythonista` → `Documents`

**Q: Can I customize alerts?**
A: Yes! Edit the PRO file and add alert setup code.

**Q: Why are some metrics static?**
A: Production metrics (slaughter, flock size) update weekly/monthly from USDA. Prices update more frequently.

**Q: Which is better for daily use?**
A: PRO has more features but both work great. Try both and decide!

---

## 🐛 TROUBLESHOOTING

**App won't load:**
- Check internet connection
- Restart Pythonista
- Try running again

**No data showing:**
- Tap 🔄 Refresh
- Check internet
- APIs may be temporarily down

**Charts not appearing (PRO):**
- Scroll down - charts are below price cards
- Ensure matplotlib installed
- Check internet connection

**Export failed:**
- Verify Documents folder exists
- Run app at least once before exporting
- Check file permissions

**Alert not triggering:**
- Verify alert code is before `view.present()`
- Check threshold and direction
- Tap 🔔 to verify alert is active

---

## 💡 PRO TIPS

1. **Start with Basic** if you're new - simpler interface
2. **Upgrade to PRO** when you want analysis features
3. **Export weekly** to build price database
4. **Set strategic alerts** at key price levels
5. **Check forecasts** before major purchases
6. **Compare grains to proteins** - grains lead prices
7. **Use landscape mode** for better chart viewing

---

## 🎯 NEXT STEPS

1. ✅ Run your chosen app
2. ✅ Add to home screen
3. ✅ Explore each tab
4. ✅ Read full documentation
5. ✅ Set up alerts (PRO)
6. ✅ Export some data (PRO)
7. ✅ Check daily/weekly for updates

---

## 📂 FILE REFERENCE

**Apps:**
- `protein_markets_app.py` - Basic version
- `protein_markets_pro.py` - PRO version ⭐

**Documentation:**
- `QUICK_START.md` - This file (start here!)
- `PROTEIN_APP_INSTRUCTIONS.md` - Basic version guide
- `PROTEIN_MARKETS_PRO_GUIDE.md` - PRO version complete guide

**Original Dashboards (still available):**
- `beef_dairy_dashboard.py`
- `poultry_dashboard.py`
- `egg_dashboard.py`
- `freshmark_pork_dashboard.py`
- `turkey_market_dashboard.py`
- And more...

---

**You're all set! Pick your app and start tracking protein markets like a pro!** 🚀📊
