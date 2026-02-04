#!/usr/bin/env python3
"""
Test API connections and data fetching
"""

from data_engine import DataEngine
import json

print("=" * 60)
print("TESTING API CONNECTIONS")
print("=" * 60)

engine = DataEngine()

# Test market snapshot
print("\n📊 Fetching Market Snapshot...")
data = engine.get_market_snapshot()

print(f"\n✅ Timestamp: {data['timestamp']}")
print(f"   Date: {data['date']}")
print(f"   Fresh Fetch: {data.get('fresh_fetch', False)}")

print("\n📈 API DATA RESULTS:")
print("-" * 60)

indicators = ['corn', 'soybean', 'diesel', 'egg_ppi', 'egg_retail']

for indicator in indicators:
    if indicator in data:
        current = data[indicator]['current']
        available = data[indicator]['available']
        history_count = len(data[indicator]['history'])

        status = "✓ OK" if available else "✗ FAILED"
        print(f"{indicator.upper():15} | {status:8} | Current: ${current:8.2f} | History: {history_count} points")

print("\n" + "=" * 60)

# Detailed output
print("\n📋 FULL DATA STRUCTURE:")
print(json.dumps({
    'corn': data['corn'],
    'soybean': data['soybean'],
    'diesel': data['diesel'],
    'egg_ppi': data['egg_ppi'],
    'egg_retail': data['egg_retail']
}, indent=2))

print("\n" + "=" * 60)

# Summary
available_count = sum(1 for ind in indicators if data[ind]['available'])
print(f"\n📊 SUMMARY: {available_count}/{len(indicators)} APIs responding")

if available_count == len(indicators):
    print("✅ ALL APIS WORKING!")
elif available_count > 0:
    print("⚠️  SOME APIS WORKING - Dashboard will show partial data")
else:
    print("❌ NO APIS WORKING - Check API keys and internet connection")

print("\n" + "=" * 60)
