#!/usr/bin/env python3
"""
Test script to verify time-based queries work correctly
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_time_based_query():
    """Test time-based headcount trends query"""
    print("🔍 Testing time-based query: 'headcount trends over time by month'")
    print("=" * 70)
    
    try:
        payload = {
            "question": "headcount trends over time by month"
        }
        
        print(f"   Sending query: {payload['question']}")
        print("   (This may take 20-40 seconds)...")
        print()
        
        response = requests.post(
            f"{API_BASE}/api/query",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Query successful!")
                print()
                print(f"   SQL Query Generated:")
                print(f"   {data.get('sql_query', 'N/A')}")
                print()
                
                # Check if query uses MonthEnd
                sql_query = data.get('sql_query', '')
                if 'MonthEnd' in sql_query:
                    print("✅ CORRECT: Query uses 'MonthEnd' column")
                else:
                    print("❌ ERROR: Query does NOT use 'MonthEnd' column")
                    print("   Expected: GROUP BY 'MonthEnd' for time trends")
                
                # Check if it groups by MonthEnd
                if 'GROUP BY "MonthEnd"' in sql_query or "GROUP BY \"MonthEnd\"" in sql_query:
                    print("✅ CORRECT: Query groups by MonthEnd")
                else:
                    print("❌ ERROR: Query does NOT group by MonthEnd")
                
                # Check if it orders by MonthEnd
                if 'ORDER BY "MonthEnd"' in sql_query or "ORDER BY \"MonthEnd\"" in sql_query:
                    print("✅ CORRECT: Query orders by MonthEnd")
                else:
                    print("⚠️  WARNING: Query does not order by MonthEnd (should add ORDER BY)")
                
                print()
                print(f"   Results count: {len(data.get('results', []))}")
                if data.get('results'):
                    print(f"   Sample result: {data.get('results', [])[0]}")
                
                print()
                print(f"   Visualization type: {data.get('visualization', {}).get('visualization_type', 'N/A')}")
                print(f"   Expected: 'line' (for time series)")
                
                print()
                print(f"   Token count: {data.get('token_count', 0)}")
                
                return True
            else:
                print(f"❌ Query failed: {data.get('error', 'Unknown error')}")
                print(f"   SQL: {data.get('sql_query', 'N/A')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Time-Based Query Test")
    print("=" * 70)
    print()
    
    # Check if backend is running
    try:
        health = requests.get(f"{API_BASE}/api/health", timeout=5)
        if health.status_code != 200:
            print("❌ Backend server is not running or not accessible")
            print("   Start it with: uvicorn app.main:app --reload --port 8000")
            exit(1)
    except:
        print("❌ Backend server is not running or not accessible")
        print("   Start it with: uvicorn app.main:app --reload --port 8000")
        exit(1)
    
    success = test_time_based_query()
    
    print()
    print("=" * 70)
    if success:
        print("✅ Test completed! Check the SQL query above.")
    else:
        print("❌ Test failed. Check errors above.")
    print("=" * 70)

