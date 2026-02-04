#!/usr/bin/env python3
"""Test script to diagnose API issues"""

import urllib.request
import urllib.parse
import json

USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
FRED_KEY = "bffd29d45a9a9eb8e0ab3dabf716b586"

# Test FRED series
FRED_SERIES = {
    'BEEF_RETAIL': 'APU0000FC1101',
    'GROUND_BEEF': 'APU0000703112',
    'BEEF_PPI': 'WPU0222',
    'FEEDER_CATTLE': 'PCTTLFDGUSDM',
    'LIVE_CATTLE': 'PCATTLEUSDM',
    'HAY': 'WPU01120501',
    'CORN': 'PMAIZMTUSDM',
    'SOY_MEAL': 'PSOYBUSDM',
    'DIESEL': 'GASDESW',
}

# Test NASS queries
NASS_QUERIES = {
    'CATTLE_INVENTORY': {
        'commodity_desc': 'CATTLE',
        'statisticcat_desc': 'INVENTORY',
        'agg_level_desc': 'NATIONAL'
    },
    'CATTLE_ON_FEED': {
        'commodity_desc': 'CATTLE',
        'class_desc': 'CATTLE, ON FEED',
        'statisticcat_desc': 'INVENTORY',
        'agg_level_desc': 'NATIONAL'
    },
}

print("=" * 60)
print("TESTING FRED API")
print("=" * 60)

for name, series_id in FRED_SERIES.items():
    try:
        params = {
            'series_id': series_id,
            'api_key': FRED_KEY,
            'file_type': 'json',
            'limit': '120',
            'sort_order': 'desc'
        }
        url = f"https://api.stlouisfed.org/fred/series/observations?{urllib.parse.urlencode(params)}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            obs = data.get('observations', [])

            # Count valid values
            valid_count = 0
            last_value = None
            for x in obs[:10]:  # Check first 10
                try:
                    v = float(x['value'])
                    if v > 0:
                        valid_count += 1
                        if last_value is None:
                            last_value = v
                except:
                    pass

            if valid_count > 0:
                print(f"✅ {name:20s} ({series_id:15s}): {valid_count} valid points, latest={last_value:.2f}")
            else:
                print(f"❌ {name:20s} ({series_id:15s}): NO VALID DATA")

    except Exception as e:
        print(f"❌ {name:20s} ({series_id:15s}): ERROR - {e}")

print("\n" + "=" * 60)
print("TESTING USDA NASS API")
print("=" * 60)

for name, query_params in NASS_QUERIES.items():
    try:
        params = {'key': USDA_KEY, 'format': 'JSON'}
        params.update(query_params)
        url = f"https://quickstats.nass.usda.gov/api/api_GET/?{urllib.parse.urlencode(params)}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            data_items = data.get('data', [])

            if data_items:
                print(f"✅ {name:20s}: {len(data_items)} records")
                # Show a sample
                if len(data_items) > 0:
                    sample = data_items[0]
                    print(f"   Sample: {sample.get('Value', 'N/A')} ({sample.get('year', 'N/A')})")
            else:
                print(f"❌ {name:20s}: NO DATA RETURNED")
                print(f"   Response: {data}")

    except Exception as e:
        print(f"❌ {name:20s}: ERROR - {e}")

print("\n" + "=" * 60)
