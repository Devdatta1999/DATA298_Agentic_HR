#!/usr/bin/env python3
"""
Test script to verify the API works correctly
Run this after starting the backend server
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        print("   Make sure the backend server is running on port 8000")
        return False

def test_simple_query():
    """Test a simple query"""
    print("\n🔍 Testing simple query...")
    try:
        payload = {
            "question": "Show me department wise headcount"
        }
        
        print(f"   Sending query: {payload['question']}")
        print("   (This may take 20-40 seconds for first query)...")
        
        response = requests.post(
            f"{API_BASE}/api/query",
            json=payload,
            timeout=120  # 2 minutes timeout for LLM
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Query successful!")
                print(f"   Session ID: {data.get('session_id', 'N/A')[:8]}...")
                print(f"   SQL Query: {data.get('sql_query', 'N/A')[:100]}...")
                print(f"   Results count: {len(data.get('results', []))}")
                print(f"   Token count: {data.get('token_count', 0)}")
                return True, data.get('session_id')
            else:
                print(f"❌ Query failed: {data.get('error', 'Unknown error')}")
                return False, None
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False, None
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (LLM may be slow)")
        return False, None
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False, None

def test_followup_query(session_id):
    """Test follow-up query with session"""
    print("\n🔍 Testing follow-up query...")
    try:
        payload = {
            "question": "What is the average salary?",
            "session_id": session_id
        }
        
        print(f"   Sending follow-up: {payload['question']}")
        
        response = requests.post(
            f"{API_BASE}/api/query",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Follow-up query successful!")
                print(f"   Results count: {len(data.get('results', []))}")
                print(f"   Token count: {data.get('token_count', 0)}")
                return True
            else:
                print(f"❌ Follow-up failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Follow-up error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("HR Analytics API Test")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n⚠️  Backend server is not running or not accessible")
        print("   Start it with: uvicorn app.main:app --reload --port 8000")
        exit(1)
    
    # Test 2: Simple query
    success, session_id = test_simple_query()
    
    if success and session_id:
        # Test 3: Follow-up query
        test_followup_query(session_id)
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed! The API is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 60)

