#!/usr/bin/env python3
"""
Test script to verify pie chart and insights generation
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_gender_distribution():
    """Test gender distribution query - should show pie chart"""
    print("=" * 70)
    print("TEST 1: Gender Distribution (Should show PIE chart)")
    print("=" * 70)
    
    payload = {
        "question": "What is the gender distribution of employees?"
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE}/api/query",
            json=payload,
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ Query successful (took {elapsed:.1f}s)")
                print(f"\nSQL: {data.get('sql_query', 'N/A')[:100]}...")
                print(f"\nVisualization Type: {data.get('visualization', {}).get('visualization_type', 'N/A')}")
                print(f"Expected: pie")
                
                if data.get('visualization', {}).get('visualization_type') == 'pie':
                    print("✅ CORRECT: Pie chart detected!")
                else:
                    print(f"❌ WRONG: Got {data.get('visualization', {}).get('visualization_type')} instead of pie")
                
                print(f"\nInsights count: {len(data.get('insights', []))}")
                print(f"Insights: {data.get('insights', [])[:2]}")
                print(f"\nExplanation length: {len(data.get('explanation', ''))}")
                print(f"Token count: {data.get('token_count', 0)}")
                
                return True
            else:
                print(f"❌ Query failed: {data.get('error', 'Unknown')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_monthly_trend():
    """Test monthly trend query - should show insights and analysis"""
    print("\n" + "=" * 70)
    print("TEST 2: Monthly Trend (Should show insights and analysis)")
    print("=" * 70)
    
    payload = {
        "question": "headcount trends over time by month"
    }
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE}/api/query",
            json=payload,
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"✅ Query successful (took {elapsed:.1f}s)")
                print(f"\nVisualization Type: {data.get('visualization', {}).get('visualization_type', 'N/A')}")
                print(f"Expected: line")
                
                print(f"\nInsights count: {len(data.get('insights', []))}")
                insights = data.get('insights', [])
                if insights:
                    print("Insights:")
                    for i, insight in enumerate(insights[:3], 1):
                        print(f"  {i}. {insight[:80]}...")
                else:
                    print("❌ NO INSIGHTS GENERATED")
                
                explanation = data.get('explanation', '')
                print(f"\nExplanation length: {len(explanation)}")
                if len(explanation) > 50:
                    print(f"Explanation preview: {explanation[:100]}...")
                    print("✅ Has explanation")
                else:
                    print("❌ Explanation too short or missing")
                
                print(f"\nToken count: {data.get('token_count', 0)}")
                
                return True
            else:
                print(f"❌ Query failed: {data.get('error', 'Unknown')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Check if backend is running
    try:
        health = requests.get(f"{API_BASE}/api/health", timeout=5)
        if health.status_code != 200:
            print("❌ Backend server is not running")
            exit(1)
    except:
        print("❌ Backend server is not running")
        exit(1)
    
    print("\n🧪 Testing Queries...\n")
    
    test1 = test_gender_distribution()
    test2 = test_monthly_trend()
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"  Test 1 (Gender Distribution): {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"  Test 2 (Monthly Trend): {'✅ PASS' if test2 else '❌ FAIL'}")
    print("=" * 70)

