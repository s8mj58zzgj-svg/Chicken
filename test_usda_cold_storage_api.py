#!/usr/bin/env python3
"""
Test script to discover USDA NASS Cold Storage API parameters
"""
import requests
import json

USDA_KEY = "lNNN4FgubqpCxzL6QbHjH9FSIl0DBcSpsPttMjeC"
BASE_URL = "http://quickstats.nass.usda.gov/api/api_GET/"

def test_query(description, params):
    """Test a query and print results"""
    print(f"\n{'='*80}")
    print(f"TEST: {description}")
    print(f"{'='*80}")
    print(f"Parameters: {json.dumps(params, indent=2)}")

    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
        print(f"Status Code: {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            if 'data' in data and data['data']:
                print(f"✅ SUCCESS - Found {len(data['data'])} records")
                print(f"\nFirst record:")
                print(json.dumps(data['data'][0], indent=2))

                # Show unique short_desc values
                short_descs = set(d.get('short_desc', '') for d in data['data'])
                print(f"\nUnique short_desc values ({len(short_descs)}):")
                for sd in sorted(list(short_descs)[:10]):  # Show first 10
                    print(f"  - {sd}")
                if len(short_descs) > 10:
                    print(f"  ... and {len(short_descs) - 10} more")
            else:
                print(f"❌ NO DATA RETURNED")
                if 'error' in data:
                    print(f"Error: {data['error']}")
        else:
            print(f"❌ HTTP ERROR")
            print(r.text[:500])
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

# Test 1: Basic pork query
print("\n\n" + "🔬 TESTING USDA NASS COLD STORAGE API".center(80))
print("="*80)

test_query(
    "Test 1: Basic PORK with COLD STORAGE in short_desc",
    {
        'key': USDA_KEY,
        'commodity_desc': 'PORK',
        'short_desc__LIKE': '%COLD STORAGE%',
        'freq_desc': 'MONTHLY',
        'year__GE': '2024',
        'format': 'JSON'
    }
)

test_query(
    "Test 2: PORK with STOCKS in short_desc",
    {
        'key': USDA_KEY,
        'commodity_desc': 'PORK',
        'short_desc__LIKE': '%STOCKS%',
        'freq_desc': 'MONTHLY',
        'year__GE': '2024',
        'format': 'JSON'
    }
)

test_query(
    "Test 3: PORK with INVENTORY statisticcat",
    {
        'key': USDA_KEY,
        'commodity_desc': 'PORK',
        'statisticcat_desc': 'INVENTORY',
        'freq_desc': 'MONTHLY',
        'year__GE': '2024',
        'format': 'JSON'
    }
)

test_query(
    "Test 4: Any PORK data monthly",
    {
        'key': USDA_KEY,
        'commodity_desc': 'PORK',
        'freq_desc': 'MONTHLY',
        'year__GE': '2024',
        'format': 'JSON'
    }
)

test_query(
    "Test 5: BUTTER with COLD STORAGE",
    {
        'key': USDA_KEY,
        'commodity_desc': 'BUTTER',
        'short_desc__LIKE': '%COLD STORAGE%',
        'year__GE': '2024',
        'format': 'JSON'
    }
)

test_query(
    "Test 6: CHEESE with STOCKS",
    {
        'key': USDA_KEY,
        'commodity_desc': 'CHEESE',
        'short_desc__LIKE': '%STOCKS%',
        'year__GE': '2024',
        'format': 'JSON'
    }
)

test_query(
    "Test 7: Search for any 'COLD STORAGE' data items",
    {
        'key': USDA_KEY,
        'short_desc__LIKE': '%COLD STORAGE%',
        'freq_desc': 'MONTHLY',
        'year': '2024',
        'format': 'JSON'
    }
)

print("\n\n" + "="*80)
print("TESTING COMPLETE".center(80))
print("="*80)
