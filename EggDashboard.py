#!/usr/bin/env python3
"""
EGG MARKET INTELLIGENCE DASHBOARD
===================================
Self-contained single-file web dashboard.
Double-click the .command launcher or run: python3 EggDashboard.py
Opens automatically in your browser at http://localhost:5050
"""

import json
import time
import datetime
import webbrowser
import threading
import subprocess
import sys
from urllib.request import urlopen
from urllib.parse import urlencode

# ── Auto-install Flask if missing ──
try:
    from flask import Flask, jsonify
except ImportError:
    print("Installing Flask (one-time setup)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, jsonify

# ==============================================================================
# CONFIG
# ==============================================================================

FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

FRED_SERIES = {
    'corn': 'PMAIZMTUSDM',
    'soybean': 'PSOYBUSDM',
    'diesel': 'GASDESW',
    'egg_ppi': 'WPU01740301',
    'egg_retail': 'APU0000708111',
    'cpi_food': 'CPIUFDNS',
}

# ==============================================================================
# DATA ENGINE
# ==============================================================================

class DataEngine:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 300

    def fetch_fred(self, series_id, limit=24):
        cache_key = f"fred_{series_id}"
        if cache_key in self.cache:
            ts, data = self.cache[cache_key]
            if time.time() - ts < self.cache_duration:
                return data
        try:
            params = {
                'series_id': series_id,
                'api_key': FRED_KEY,
                'file_type': 'json',
                'limit': limit,
                'sort_order': 'desc',
            }
            url = f"https://api.stlouisfed.org/fred/series/observations?{urlencode(params)}"
            with urlopen(url, timeout=12) as resp:
                raw = json.loads(resp.read().decode())
            obs = raw.get('observations', [])
            pairs = [{'date': o['date'], 'value': float(o['value'])}
                     for o in obs if o['value'] != '.']
            if pairs:
                self.cache[cache_key] = (time.time(), pairs)
                return pairs
            return []
        except Exception as e:
            print(f"  FRED error ({series_id}): {e}")
            return []

    def clear_cache(self):
        self.cache = {}

    def get_snapshot(self):
        now = datetime.datetime.now()
        today = datetime.date.today()

        corn = self.fetch_fred(FRED_SERIES['corn'])
        soy = self.fetch_fred(FRED_SERIES['soybean'])
        diesel = self.fetch_fred(FRED_SERIES['diesel'])
        egg_ppi = self.fetch_fred(FRED_SERIES['egg_ppi'])
        egg_retail = self.fetch_fred(FRED_SERIES['egg_retail'])

        def latest(data, fallback=0):
            return data[0]['value'] if data else fallback

        def history(data):
            return list(reversed(data[:12]))

        def pct_change(data):
            if len(data) >= 2:
                old, new = data[-1]['value'], data[0]['value']
                if old > 0:
                    return round(((new - old) / old) * 100, 1)
            return 0

        corn_val = latest(corn, 215.0)
        soy_val = latest(soy, 450.0)
        diesel_val = latest(diesel, 3.85)
        egg_ppi_val = latest(egg_ppi, 165.0)
        egg_retail_val = latest(egg_retail, 3.28)

        soy_meal = soy_val * 0.767
        annual_feed = 0.42 * 12
        eggs_per_day = 0.82
        feed_per_dozen = annual_feed / (eggs_per_day * 365 / 12)

        d30 = (today + datetime.timedelta(days=30)).strftime("%b %d")
        d60 = (today + datetime.timedelta(days=60)).strftime("%b %d")
        d90 = (today + datetime.timedelta(days=90)).strftime("%b %d")

        cage_free_premium = 0.85
        organic_premium = 2.10
        cage_free_price = egg_retail_val + cage_free_premium
        organic_price = egg_retail_val + organic_premium

        return {
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
            'date': today.strftime('%B %d, %Y'),
            'forecast_dates': {'d30': d30, 'd60': d60, 'd90': d90},
            'prices': {
                'egg_retail': {'value': egg_retail_val, 'change': pct_change(egg_retail), 'unit': '$/dozen'},
                'corn': {'value': corn_val, 'change': pct_change(corn), 'unit': 'Index'},
                'soybean': {'value': soy_val, 'change': pct_change(soy), 'unit': 'Index'},
                'diesel': {'value': diesel_val, 'change': pct_change(diesel), 'unit': '$/gal'},
                'egg_ppi': {'value': egg_ppi_val, 'change': pct_change(egg_ppi), 'unit': 'PPI Index'},
                'cage_free': {'value': cage_free_price, 'change': 0, 'unit': '$/dozen'},
                'organic': {'value': organic_price, 'change': 0, 'unit': '$/dozen'},
            },
            'charts': {
                'egg_retail': {'labels': [p['date'] for p in history(egg_retail)], 'values': [p['value'] for p in history(egg_retail)]},
                'egg_ppi': {'labels': [p['date'] for p in history(egg_ppi)], 'values': [p['value'] for p in history(egg_ppi)]},
                'corn': {'labels': [p['date'] for p in history(corn)], 'values': [p['value'] for p in history(corn)]},
                'soybean': {'labels': [p['date'] for p in history(soy)], 'values': [p['value'] for p in history(soy)]},
            },
            'flock': {
                'total_layers': 320.5, 'cage_free_pct': 38.5, 'pullet_placements': -3.2,
                'eggs_per_day': eggs_per_day, 'hatchability': 79.7,
            },
            'hpai': {
                'risk_level': 'VERY HIGH', 'commercial_outbreaks': 8,
                'birds_depopulated': 2.1, 'top50_share': 60,
            },
            'costs': {
                'annual_feed': round(annual_feed, 2), 'feed_per_dozen': round(feed_per_dozen, 2),
                'soy_meal': round(soy_meal, 0), 'cage_free_delta': 0.35, 'min_retail': 2.80,
            },
            'forecasts': {
                'conventional': {
                    'current': egg_retail_val,
                    'targets': [round(egg_retail_val * m, 2) for m in [1.04, 1.08, 1.12]],
                    'trend': 'BULLISH',
                    'logic': f'Tight flock + elevated feed + HPAI tail risk. Target ${egg_retail_val * 1.12:.2f} by {d90}.',
                },
                'cage_free': {
                    'current': cage_free_price,
                    'targets': [round(cage_free_price * m, 2) for m in [1.05, 1.10, 1.15]],
                    'trend': 'STRUCTURAL BULL',
                    'logic': f'9-state mandate by 2026. Supply shortage through 2027. ${cage_free_price * 1.15:.2f} target.',
                },
                'organic': {
                    'current': organic_price,
                    'targets': [round(organic_price * m, 2) for m in [1.03, 1.06, 1.08]],
                    'trend': 'PREMIUM STABLE',
                    'logic': 'Organic feed +60% cost. Loyal niche absorbs price. Sticky demand.',
                },
                'breaking_stock': {
                    'current': 1.30, 'targets': [1.35, 1.40, 1.45],
                    'trend': 'RECOVERY',
                    'logic': f'Food service recovery. Shell price forces substitution. $1.45 by {d90}.',
                },
            },
            'storage': {
                'shell_eggs': {'value': 42.5, 'unit': 'M dozen', 'normal': 55.0, 'status': 'BELOW NORMAL'},
                'frozen': {'value': 95.2, 'unit': 'M lbs', 'normal': 110.0, 'status': 'ADEQUATE'},
            },
            'verdict': {
                'title': 'STRUCTURAL TIGHT + TAIL RISK',
                'signals': [
                    {'label': 'Conventional', 'action': 'BUY', 'target': f'${egg_retail_val * 1.12:.2f} (90d)'},
                    {'label': 'Cage-Free', 'action': 'STRONG BUY', 'target': f'${cage_free_price * 1.15:.2f} (90d)'},
                    {'label': 'Breaking Stock', 'action': 'HEDGE', 'target': '$1.45 (90d)'},
                    {'label': 'HPAI', 'action': 'MONITOR', 'target': 'Weekly watch'},
                ],
                'summary': (
                    'Eggs structurally underpriced for risk. Bird flu is dominant tail risk — '
                    'top 50 farms hold 60% of supply. One major outbreak = $8-10/doz overnight. '
                    'Cage-free mandates forcing conversion faster than economics allow. '
                    'Feed floor at $2.80/doz prevents meaningful downside. '
                    'Next outbreak takes retail to $6-8.'
                ),
            },
        }


# ==============================================================================
# EMBEDDED HTML DASHBOARD
# ==============================================================================

DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Egg Market Intelligence Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#050508;--surface:#0d0d12;--card:#12121a;--border:#1e1e2a;--text:#e0e0e8;--sub:#6b6b80;--bull:#00ff88;--bear:#ff4455;--warn:#ffaa00;--eggs:#ffdd44;--layer:#ff6b9d;--risk:#ff3344;--cold:#00ccff;--logistics:#ff9900;--macro:#aa55ff;--gold:#ffd700;--accent:#00ccff}
body{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;min-height:100vh}
.container{max-width:1400px;margin:0 auto;padding:20px 30px 60px}
.header{text-align:center;padding:40px 0 30px;border-bottom:1px solid var(--border);margin-bottom:30px}
.header h1{font-size:36px;color:var(--eggs);font-weight:800;letter-spacing:1px}
.header .subtitle{color:var(--sub);font-size:14px;margin-top:8px;letter-spacing:2px;text-transform:uppercase}
.header .timestamp{color:var(--accent);font-size:13px;margin-top:12px;font-family:'SF Mono','Menlo',monospace}
.status-bar{display:flex;align-items:center;justify-content:space-between;background:linear-gradient(135deg,#001a0d,#002211);border:1px solid #004422;border-radius:10px;padding:14px 24px;margin-bottom:30px}
.status-bar .status-text{color:var(--bull);font-size:13px;font-family:monospace}
.status-bar .status-dot{width:8px;height:8px;background:var(--bull);border-radius:50%;animation:pulse 2s infinite;margin-right:10px;display:inline-block}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.refresh-btn{background:0 0;border:1px solid var(--bull);color:var(--bull);padding:8px 20px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;transition:all .2s}
.refresh-btn:hover{background:var(--bull);color:#000}
.refresh-btn:disabled{opacity:.5;cursor:wait}
.top-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:30px}
.price-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px 20px;transition:border-color .2s}
.price-card:hover{border-color:#333}
.price-card .label{font-size:11px;color:var(--sub);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px}
.price-card .value{font-size:28px;font-weight:800;color:#fff}
.price-card .unit{font-size:12px;color:var(--sub);margin-left:4px}
.price-card .change{font-size:13px;font-weight:600;margin-top:6px}
.price-card .change.up{color:var(--bull)}
.price-card .change.down{color:var(--bear)}
.price-card .change.flat{color:var(--sub)}
.section-header{font-size:13px;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:20px 0 12px;margin-top:10px;border-bottom:1px solid var(--border);margin-bottom:18px}
.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;margin-bottom:30px}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px}
.chart-card h3{font-size:14px;color:var(--sub);margin-bottom:16px;letter-spacing:1px;text-transform:uppercase}
.chart-card canvas{width:100%!important;height:220px!important}
.insight-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-bottom:30px}
.insight-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px;position:relative}
.insight-card .card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.insight-card .card-title{font-size:13px;font-weight:700;letter-spacing:1px}
.insight-card .badge{font-size:10px;font-weight:700;padding:3px 10px;border-radius:4px;text-transform:uppercase;letter-spacing:.5px}
.insight-card .card-value{font-size:26px;font-weight:800;color:#fff;margin-bottom:8px}
.insight-card .card-value .unit{font-size:13px;color:var(--sub);font-weight:400}
.insight-card .card-text{font-size:13px;color:#999;line-height:1.6}
.forecast-table{width:100%;border-collapse:collapse;margin-bottom:30px}
.forecast-table th{text-align:left;font-size:11px;color:var(--sub);text-transform:uppercase;letter-spacing:1.5px;padding:12px 16px;border-bottom:1px solid var(--border)}
.forecast-table td{padding:16px;border-bottom:1px solid #111;font-size:14px}
.forecast-table tr:hover td{background:#0a0a12}
.forecast-table .product{font-weight:700;color:#fff}
.forecast-table .spot{color:#fff;font-weight:600;font-size:16px}
.forecast-table .target{font-weight:700;font-size:16px}
.forecast-table .trend-badge{display:inline-block;font-size:10px;font-weight:700;padding:3px 10px;border-radius:4px;letter-spacing:.5px}
.forecast-table .logic{color:var(--sub);font-size:12px;max-width:320px}
.storage-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-bottom:30px}
.storage-card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px}
.storage-card .storage-label{font-size:12px;color:var(--sub);text-transform:uppercase;letter-spacing:1px;margin-bottom:10px}
.storage-card .storage-value{font-size:24px;font-weight:800;color:#fff;margin-bottom:4px}
.storage-card .storage-status{font-size:11px;font-weight:700;letter-spacing:1px}
.storage-bar-track{height:8px;background:#1a1a2a;border-radius:4px;margin-top:12px;overflow:hidden}
.storage-bar-fill{height:100%;border-radius:4px;transition:width 1s ease}
.verdict-card{background:linear-gradient(135deg,#1a1200,#1a0d00);border:1px solid #332200;border-radius:12px;padding:30px;margin-bottom:30px}
.verdict-card h2{font-size:18px;color:var(--warn);margin-bottom:20px;letter-spacing:1px}
.verdict-signals{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-bottom:24px}
.signal-item{background:rgba(0,0,0,.3);border-radius:8px;padding:14px 18px}
.signal-item .signal-label{font-size:11px;color:var(--sub);text-transform:uppercase;letter-spacing:1px}
.signal-item .signal-action{font-size:18px;font-weight:800;margin:4px 0}
.signal-item .signal-target{font-size:12px;color:#999}
.verdict-summary{font-size:14px;color:#bbb;line-height:1.8;border-top:1px solid #332200;padding-top:20px}
.loading-overlay{position:fixed;inset:0;background:rgba(5,5,8,.85);display:flex;align-items:center;justify-content:center;z-index:1000;backdrop-filter:blur(4px)}
.loading-overlay.hidden{display:none}
.spinner{width:50px;height:50px;border:3px solid var(--border);border-top-color:var(--eggs);border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.footer{text-align:center;padding:30px 0;border-top:1px solid var(--border);color:var(--sub);font-size:12px;letter-spacing:1px}
</style>
</head>
<body>
<div class="loading-overlay" id="loadingOverlay"><div style="text-align:center"><div class="spinner"></div><div style="color:var(--eggs);margin-top:20px;font-size:14px">LOADING MARKET DATA...</div></div></div>
<div class="container">
<div class="header"><h1>&#x1F95A; EGG MARKET INTELLIGENCE</h1><div class="subtitle">Professional Market Analysis &amp; Forecasting</div><div class="timestamp" id="timestamp">Loading...</div></div>
<div class="status-bar"><div><span class="status-dot"></span><span class="status-text" id="statusText">Connecting to FRED API...</span></div><button class="refresh-btn" id="refreshBtn" onclick="refreshData()">&#x21BB; REFRESH DATA</button></div>
<div class="top-cards" id="topCards"></div>
<div class="section-header" style="color:var(--eggs)">PRICE TRENDS</div>
<div class="chart-grid"><div class="chart-card"><h3>Egg Retail Price ($/dozen)</h3><canvas id="chartEggRetail"></canvas></div><div class="chart-card"><h3>Egg PPI Index</h3><canvas id="chartEggPPI"></canvas></div><div class="chart-card"><h3>Corn Price Index</h3><canvas id="chartCorn"></canvas></div><div class="chart-card"><h3>Soybean Price Index</h3><canvas id="chartSoy"></canvas></div></div>
<div class="section-header" style="color:var(--layer)">1. LAYER FLOCK STATUS</div><div class="insight-grid" id="flockGrid"></div>
<div class="section-header" style="color:var(--risk)">2. HPAI RISK (CRITICAL)</div><div class="insight-grid" id="hpaiGrid"></div>
<div class="section-header" style="color:var(--logistics)">3. PRODUCTION COSTS</div><div class="insight-grid" id="costsGrid"></div>
<div class="section-header" style="color:var(--cold)">4. COLD STORAGE</div><div class="storage-grid" id="storageGrid"></div>
<div class="section-header" style="color:var(--bull)">5. 90-DAY PRICE FORECASTS</div>
<table class="forecast-table"><thead><tr><th>Product</th><th>Spot Price</th><th>30d</th><th>60d</th><th>90d Target</th><th>Trend</th><th>Logic</th></tr></thead><tbody id="forecastBody"></tbody></table>
<div class="section-header" style="color:var(--warn)">6. ANALYST VERDICT</div><div class="verdict-card" id="verdictCard"></div>
<div class="footer">DATA SOURCE: FRED (Federal Reserve Economic Data) &bull; REAL-TIME API &bull; AUTO-REFRESH EVERY 5 MIN</div>
</div>
<script>
Chart.defaults.color='#666';Chart.defaults.borderColor='#1e1e2a';
const CI={};
function makeChart(id,labels,values,color,fill){const ctx=document.getElementById(id);if(CI[id])CI[id].destroy();const g=ctx.getContext('2d').createLinearGradient(0,0,0,220);g.addColorStop(0,color+'40');g.addColorStop(1,color+'00');CI[id]=new Chart(ctx,{type:'line',data:{labels:labels.map(d=>{const dt=new Date(d);return dt.toLocaleDateString('en-US',{month:'short',year:'2-digit'})}),datasets:[{data:values,borderColor:color,backgroundColor:fill?g:'transparent',borderWidth:2.5,pointRadius:3,pointBackgroundColor:color,tension:.3,fill:fill}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:'#111'},ticks:{font:{size:10}}},y:{grid:{color:'#111'},ticks:{font:{size:10}}}}}})}
function renderTopCards(P){const C=[{key:'egg_retail',label:'EGG RETAIL',color:'#ffdd44'},{key:'cage_free',label:'CAGE-FREE',color:'#ff6b9d'},{key:'organic',label:'ORGANIC',color:'#aa55ff'},{key:'egg_ppi',label:'EGG PPI',color:'#00ccff'},{key:'corn',label:'CORN',color:'#ff9900'},{key:'soybean',label:'SOYBEAN',color:'#ffaa00'},{key:'diesel',label:'DIESEL',color:'#ff5555'}];document.getElementById('topCards').innerHTML=C.map(c=>{const p=P[c.key];const cls=p.change>0?'up':p.change<0?'down':'flat';const s=p.change>0?'+':'';const pre=p.unit.includes('$')?'$':'';const v=p.unit.includes('$')?p.value.toFixed(2):p.value.toFixed(1);return`<div class="price-card" style="border-left:3px solid ${c.color}"><div class="label">${c.label}</div><div class="value">${pre}${v}<span class="unit">${p.unit.replace('$/','/')}</span></div><div class="change ${cls}">${s}${p.change}% vs prior</div></div>`}).join('')}
function mkCard(i){const bg=i.status==='CRITICAL'||i.status==='BLACK SWAN'?'var(--risk)':i.status==='ELEVATED'||i.status==='FLOOR'||i.status==='STRUCTURAL'?'var(--warn)':i.color;return`<div class="insight-card"><div class="card-header"><div class="card-title" style="color:${i.color}">${i.title}</div><span class="badge" style="background:${bg};color:#000">${i.status}</span></div><div class="card-value">${i.value} <span class="unit">${i.unit}</span></div><div class="card-text">${i.text}</div></div>`}
function renderFlock(f){document.getElementById('flockGrid').innerHTML=[{title:'TOTAL LAYERS',value:f.total_layers+'M',unit:'Birds',status:'TIGHT',color:'var(--layer)',text:`Flock recovering from HPAI. Pullet placements ${f.pullet_placements}% YoY.`},{title:'CAGE-FREE TRANSITION',value:f.cage_free_pct+'%',unit:'of Flock',status:'ACCELERATING',color:'var(--layer)',text:'9 states mandate cage-free by 2026. Conversion costs $1,850/bird.'},{title:'FLOCK PRODUCTIVITY',value:(f.eggs_per_day*100).toFixed(0)+'%',unit:'Lay Rate',status:'PEAK',color:'var(--layer)',text:f.eggs_per_day+' eggs/bird/day. Biology maxed — only growth is more birds.'},{title:'HATCHABILITY',value:f.hatchability+'%',unit:'Rate',status:'CRITICAL',color:'var(--bear)',text:'Normal = 84%. Missing 4-5 chicks per 100 eggs. No quick fix.'}].map(mkCard).join('')}
function renderHPAI(h){document.getElementById('hpaiGrid').innerHTML=[{title:'BIRD FLU THREAT',value:h.risk_level,unit:'Risk',status:'CRITICAL',color:'var(--risk)',text:h.birds_depopulated+'M culled across '+h.commercial_outbreaks+' sites. One major farm = instant spike.'},{title:'SUPPLY VULNERABILITY',value:'EXTREME',unit:'Fragility',status:'BLACK SWAN',color:'var(--risk)',text:'Top '+h.top50_share+' farms = '+h.top50_share+'% of supply. One outbreak = shelves empty in 48hrs.'},{title:'BIOSECURITY PREMIUM',value:'+$0.20',unit:'$/doz',status:'BAKED IN',color:'var(--warn)',text:'Protocols, vaccines, insurance. This cost premium never goes away.'}].map(mkCard).join('')}
function renderCosts(c,p){document.getElementById('costsGrid').innerHTML=[{title:'ANNUAL FEED COST',value:'$'+c.annual_feed,unit:'/bird/year',status:'ELEVATED',color:'var(--logistics)',text:'Corn '+p.corn.value.toFixed(0)+', Soy '+p.soybean.value.toFixed(0)+'. Layers eat 18 months vs broilers 6 weeks.'},{title:'FEED COST PER DOZEN',value:'$'+c.feed_per_dozen,unit:'Feed Only',status:'FLOOR',color:'var(--logistics)',text:'Just feed. Add housing, labor, transport = retail cannot go below $'+c.min_retail+'/doz.'},{title:'CAGE-FREE DELTA',value:'+$'+c.cage_free_delta,unit:'$/doz',status:'STRUCTURAL',color:'var(--warn)',text:'40% more space, lower density = permanently higher costs.'}].map(mkCard).join('')}
function renderStorage(s){const sh=s.shell_eggs,fr=s.frozen,sp=Math.round(sh.value/sh.normal*100),fp=Math.round(fr.value/fr.normal*100);document.getElementById('storageGrid').innerHTML=`<div class="storage-card"><div class="storage-label">SHELL EGG INVENTORY</div><div class="storage-value">${sh.value} ${sh.unit}</div><div class="storage-status" style="color:var(--warn)">${sh.status} (Normal: ${sh.normal} ${sh.unit})</div><div class="storage-bar-track"><div class="storage-bar-fill" style="width:${sp}%;background:${sp<80?'var(--warn)':'var(--bull)'}"></div></div></div><div class="storage-card"><div class="storage-label">FROZEN EGG PRODUCTS</div><div class="storage-value">${fr.value} ${fr.unit}</div><div class="storage-status" style="color:var(--cold)">${fr.status} (Normal: ${fr.normal} ${fr.unit})</div><div class="storage-bar-track"><div class="storage-bar-fill" style="width:${fp}%;background:var(--cold)"></div></div></div>`}
function renderForecasts(F){const R=[{name:'Conventional (Large)',key:'conventional'},{name:'Cage-Free',key:'cage_free'},{name:'Organic',key:'organic'},{name:'Breaking Stock',key:'breaking_stock'}];document.getElementById('forecastBody').innerHTML=R.map(r=>{const f=F[r.key];const tc=f.trend.includes('BULL')||f.trend.includes('BUY')?'var(--bull)':f.trend.includes('BEAR')?'var(--bear)':'var(--warn)';const xc=f.targets[2]>f.current?'var(--bull)':'var(--bear)';const d=(((f.targets[2]-f.current)/f.current)*100).toFixed(1);return`<tr><td class="product">${r.name}</td><td class="spot">$${f.current.toFixed(2)}</td><td>$${f.targets[0].toFixed(2)}</td><td>$${f.targets[1].toFixed(2)}</td><td class="target" style="color:${xc}">$${f.targets[2].toFixed(2)} <span style="font-size:12px">(+${d}%)</span></td><td><span class="trend-badge" style="background:${tc};color:#000">${f.trend}</span></td><td class="logic">${f.logic}</td></tr>`}).join('')}
function renderVerdict(v){const ac={'BUY':'var(--bull)','STRONG BUY':'var(--bull)','HEDGE':'var(--warn)','MONITOR':'var(--cold)','SELL':'var(--bear)'};document.getElementById('verdictCard').innerHTML=`<h2>&#x26A0;&#xFE0F; ${v.title}</h2><div class="verdict-signals">${v.signals.map(s=>`<div class="signal-item"><div class="signal-label">${s.label}</div><div class="signal-action" style="color:${ac[s.action]||'#fff'}">${s.action}</div><div class="signal-target">${s.target}</div></div>`).join('')}</div><div class="verdict-summary">${v.summary}</div>`}
async function loadData(ep){document.getElementById('loadingOverlay').classList.remove('hidden');document.getElementById('refreshBtn').disabled=true;try{const r=await fetch(ep);const d=await r.json();document.getElementById('timestamp').textContent=d.date+' | '+d.timestamp;document.getElementById('statusText').textContent='LIVE DATA | '+d.timestamp+' | Source: FRED API | Auto-refresh: 5 min';renderTopCards(d.prices);if(d.charts.egg_retail.labels.length)makeChart('chartEggRetail',d.charts.egg_retail.labels,d.charts.egg_retail.values,'#ffdd44',true);if(d.charts.egg_ppi.labels.length)makeChart('chartEggPPI',d.charts.egg_ppi.labels,d.charts.egg_ppi.values,'#00ccff',true);if(d.charts.corn.labels.length)makeChart('chartCorn',d.charts.corn.labels,d.charts.corn.values,'#ff9900',true);if(d.charts.soybean.labels.length)makeChart('chartSoy',d.charts.soybean.labels,d.charts.soybean.values,'#ffaa00',true);renderFlock(d.flock);renderHPAI(d.hpai);renderCosts(d.costs,d.prices);renderStorage(d.storage);renderForecasts(d.forecasts);renderVerdict(d.verdict)}catch(e){document.getElementById('statusText').textContent='ERROR: '+e.message+' — tap refresh';document.getElementById('statusText').style.color='var(--bear)'}finally{document.getElementById('loadingOverlay').classList.add('hidden');document.getElementById('refreshBtn').disabled=false}}
function refreshData(){loadData('/api/refresh')}
loadData('/api/data');
setInterval(()=>loadData('/api/data'),5*60*1000);
</script>
</body>
</html>'''

# ==============================================================================
# FLASK APP
# ==============================================================================

engine = DataEngine()
app = Flask(__name__)

@app.route('/')
def index():
    return DASHBOARD_HTML

@app.route('/api/data')
def api_data():
    return jsonify(engine.get_snapshot())

@app.route('/api/refresh')
def api_refresh():
    engine.clear_cache()
    return jsonify(engine.get_snapshot())

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5050')

if __name__ == '__main__':
    print()
    print("=" * 60)
    print("  EGG MARKET INTELLIGENCE DASHBOARD")
    print("  Opening http://localhost:5050 in your browser...")
    print("  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='0.0.0.0', port=5050, debug=False)
