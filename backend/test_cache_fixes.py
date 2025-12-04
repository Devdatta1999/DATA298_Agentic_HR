#!/usr/bin/env python3
"""
Test script to verify cache fixes work correctly
Tests the same query multiple times to ensure cache hits
"""

import requests
import time
import json

RAG_BACKEND = "http://localhost:8001/api"

def test_query(question: str, session_id: str, description: str):
    """Test a query and return results"""
    print(f"\n{'='*80}")
    print(f"Testing: {description}")
    print(f"Question: {question}")
    print(f"{'='*80}")
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{RAG_BACKEND}/query",
            json={"question": question, "session_id": session_id},
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            cache_hit = data.get("cache_hit", False)
            cache_sim = data.get("cache_similarity")
            tokens = data.get("query_tokens", 0)
            
            print(f"✅ Success")
            print(f"⏱️  Response Time: {elapsed:.2f}s")
            print(f"💾 Cache Hit: {cache_hit}")
            if cache_sim:
                print(f"📊 Cache Similarity: {cache_sim*100:.1f}%")
            print(f"🔢 Tokens: {tokens:,}")
            
            if cache_hit:
                print(f"🚀 SPEEDUP: {elapsed:.2f}s (cached) vs expected ~50-60s (uncached)")
            
            return {
                "success": True,
                "time": elapsed,
                "cache_hit": cache_hit,
                "similarity": cache_sim,
                "tokens": tokens
            }
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text[:200]}")
            return {"success": False}
    except Exception as e:
        print(f"❌ Exception: {str(e)[:200]}")
        return {"success": False}

def main():
    print("\n" + "="*80)
    print("🧪 TESTING CACHE FIXES")
    print("="*80)
    print("\nTesting the same query with variations to verify cache hits")
    print("="*80)
    
    session_id = f"cache-test-{int(time.time())}"
    
    # Test 1: First query (should be slow, no cache)
    print("\n\n📊 TEST 1: First Query (No Cache Expected)")
    result1 = test_query(
        "Show me departmentwise headcount",
        session_id,
        "First Query - Should be slow (no cache)"
    )
    
    time.sleep(1)
    
    # Test 2: Same query (should be fast, exact cache hit)
    print("\n\n📊 TEST 2: Same Query (Exact Cache Hit Expected)")
    result2 = test_query(
        "Show me departmentwise headcount",
        session_id,
        "Second Query - Should be FAST (exact match)"
    )
    
    time.sleep(1)
    
    # Test 3: Variation with different case (should be fast, exact cache hit via normalization)
    print("\n\n📊 TEST 3: Different Case (Exact Cache Hit via Normalization)")
    result3 = test_query(
        "show me departmentwise headcount",
        session_id,
        "Third Query - Should be FAST (normalized match)"
    )
    
    time.sleep(1)
    
    # Test 4: Variation with punctuation (should be fast, exact cache hit via normalization)
    print("\n\n📊 TEST 4: With Punctuation (Exact Cache Hit via Normalization)")
    result4 = test_query(
        "Show me departmentwise headcount!",
        session_id,
        "Fourth Query - Should be FAST (normalized match)"
    )
    
    time.sleep(1)
    
    # Test 5: Semantic variation (should be fast, semantic cache hit)
    print("\n\n📊 TEST 5: Semantic Variation (Semantic Cache Hit Expected)")
    result5 = test_query(
        "what is departmentwise headcount",
        session_id,
        "Fifth Query - Should be FAST (semantic match)"
    )
    
    time.sleep(1)
    
    # Test 6: Another semantic variation
    print("\n\n📊 TEST 6: Another Semantic Variation")
    result6 = test_query(
        "display department headcount",
        session_id,
        "Sixth Query - Should be FAST (semantic match)"
    )
    
    # Summary
    print("\n\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    results = [result1, result2, result3, result4, result5, result6]
    cache_hits = sum(1 for r in results if r.get("cache_hit"))
    avg_time_cached = sum(r["time"] for r in results[1:] if r.get("cache_hit")) / max(cache_hits, 1)
    first_time = result1.get("time", 0)
    
    print(f"\n✅ Total Queries: {len(results)}")
    print(f"✅ Cache Hits: {cache_hits}/{len(results)-1} (excluding first)")
    print(f"⏱️  First Query Time: {first_time:.2f}s")
    print(f"⏱️  Avg Cached Time: {avg_time_cached:.2f}s")
    if first_time > 0 and avg_time_cached > 0:
        speedup = first_time / avg_time_cached
        print(f"🚀 Average Speedup: {speedup:.1f}x faster")
    
    print("\n" + "="*80)
    print("🎯 EXPECTED RESULTS:")
    print("="*80)
    print("✅ Test 1: Slow (no cache) - First time")
    print("✅ Test 2: FAST (exact cache hit)")
    print("✅ Test 3: FAST (normalized exact match)")
    print("✅ Test 4: FAST (normalized exact match)")
    print("✅ Test 5: FAST (semantic cache hit)")
    print("✅ Test 6: FAST (semantic cache hit)")
    print("\n" + "="*80)
    
    if cache_hits >= 4:
        print("✅✅✅ SUCCESS! Cache is working correctly!")
    elif cache_hits >= 2:
        print("⚠️  PARTIAL SUCCESS - Some cache hits working")
    else:
        print("❌ ISSUE - Cache not working as expected")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

