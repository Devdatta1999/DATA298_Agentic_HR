#!/usr/bin/env python3
"""Quick test script for RAG and Cache functionality"""

import requests
import json
import time

BASE_URL = "http://localhost:8001/api"

def test_rag_query():
    """Test RAG with a custom term"""
    print("\n" + "="*60)
    print("TEST 1: RAG Query (Custom Term)")
    print("="*60)
    
    question = "Calculate Internal Mobility Rate by department"
    print(f"Question: {question}")
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "question": question,
            "session_id": "test-rag-1"
        }
    )
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Response time: {elapsed:.2f}s")
        print(f"   RAG Used: {data.get('rag_used', False)}")
        print(f"   Cache Hit: {data.get('cache_hit', False)}")
        print(f"   SQL Query: {data.get('sql_query', '')[:100]}...")
        print(f"   Results: {len(data.get('results', []))} rows")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_cache_query():
    """Test cache with similar query"""
    print("\n" + "="*60)
    print("TEST 2: Cache Query (Similar Question)")
    print("="*60)
    
    question = "Show me internal mobility rate by department"
    print(f"Question: {question}")
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "question": question,
            "session_id": "test-cache-1"
        }
    )
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Response time: {elapsed:.2f}s")
        print(f"   RAG Used: {data.get('rag_used', False)}")
        print(f"   Cache Hit: {data.get('cache_hit', False)}")
        if data.get('cache_hit'):
            print(f"   🚀 CACHE HIT! Much faster!")
        print(f"   SQL Query: {data.get('sql_query', '')[:100]}...")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_standard_query():
    """Test standard query (no RAG needed)"""
    print("\n" + "="*60)
    print("TEST 3: Standard Query (No RAG)")
    print("="*60)
    
    question = "Show me department wise headcount"
    print(f"Question: {question}")
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "question": question,
            "session_id": "test-standard-1"
        }
    )
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Response time: {elapsed:.2f}s")
        print(f"   RAG Used: {data.get('rag_used', False)}")
        print(f"   Cache Hit: {data.get('cache_hit', False)}")
        print(f"   Results: {len(data.get('results', []))} rows")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    print("🧪 Testing RAG and Semantic Cache")
    print("Make sure the server is running on http://localhost:8001")
    print()
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8001/", timeout=2)
        print("✅ Server is running")
    except:
        print("❌ Server is not running. Please start it first:")
        print("   cd backend && ./start_rag.sh")
        exit(1)
    
    # Run tests
    results = []
    results.append(test_rag_query())
    time.sleep(1)
    results.append(test_cache_query())
    time.sleep(1)
    results.append(test_standard_query())
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Passed: {sum(results)}/{len(results)}")
    if all(results):
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed")

