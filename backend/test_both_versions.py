#!/usr/bin/env python3
"""
Comprehensive test script to compare Main Branch (port 8000) vs RAG Branch (port 8001)
Tests: Normal queries, RAG queries, Cache hits, Response times
"""

import requests
import time
import json
from typing import Dict, Any

# Configuration
MAIN_BACKEND = "http://localhost:8000/api"
RAG_BACKEND = "http://localhost:8001/api"

def test_query(backend_url: str, question: str, session_id: str, description: str) -> Dict[str, Any]:
    """Test a single query and return results"""
    print(f"\n{'='*80}")
    print(f"Testing: {description}")
    print(f"Backend: {backend_url}")
    print(f"Question: {question}")
    print(f"{'='*80}")
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{backend_url}/query",
            json={"question": question, "session_id": session_id},
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "response_time": elapsed,
                "cache_hit": data.get("cache_hit", False),
                "rag_used": data.get("rag_used", False),
                "cache_similarity": data.get("cache_similarity"),
                "query_tokens": data.get("query_tokens", 0),
                "has_results": bool(data.get("results")),
                "has_sql": bool(data.get("sql_query")),
                "sql_preview": data.get("sql_query", "")[:200] if data.get("sql_query") else None,
                "error": None
            }
        else:
            return {
                "success": False,
                "response_time": elapsed,
                "error": f"HTTP {response.status_code}: {response.text[:200]}"
            }
    except Exception as e:
        return {
            "success": False,
            "response_time": time.time() - start_time,
            "error": str(e)
        }

def print_result(result: Dict[str, Any], branch_name: str):
    """Print formatted test result"""
    print(f"\n📊 {branch_name} Results:")
    if result["success"]:
        print(f"   ✅ Success: Yes")
        print(f"   ⏱️  Response Time: {result['response_time']:.2f}s")
        print(f"   💾 Cache Hit: {result['cache_hit']}")
        if result.get('cache_similarity'):
            print(f"   📈 Cache Similarity: {result['cache_similarity']*100:.1f}%")
        print(f"   🧠 RAG Used: {result['rag_used']}")
        print(f"   🔢 Tokens: {result['query_tokens']:,}")
        print(f"   📊 Has Results: {result['has_results']}")
        print(f"   💻 Has SQL: {result['has_sql']}")
        if result.get('sql_preview'):
            print(f"   📝 SQL Preview: {result['sql_preview']}...")
    else:
        print(f"   ❌ Success: No")
        print(f"   ⏱️  Response Time: {result['response_time']:.2f}s")
        print(f"   ❌ Error: {result['error']}")

def main():
    print("\n" + "="*80)
    print("🚀 COMPREHENSIVE TEST: Main Branch vs RAG Branch")
    print("="*80)
    print("\n📍 Main Branch: http://localhost:8000 (No RAG, No Cache)")
    print("📍 RAG Branch: http://localhost:8001 (RAG + Semantic Cache)")
    print("\n" + "="*80)
    
    # Test 1: Normal Query (should work on both)
    print("\n\n🧪 TEST 1: Normal Query - Department Headcount")
    print("-" * 80)
    main_result_1 = test_query(
        MAIN_BACKEND,
        "Show me department wise headcount",
        "test-main-1",
        "Main Branch - Normal Query"
    )
    rag_result_1 = test_query(
        RAG_BACKEND,
        "Show me department wise headcount",
        "test-rag-1",
        "RAG Branch - Normal Query"
    )
    print_result(main_result_1, "Main Branch")
    print_result(rag_result_1, "RAG Branch")
    
    # Test 2: RAG-Specific Query (custom term - should only work on RAG branch)
    print("\n\n🧪 TEST 2: RAG Query - Internal Mobility Rate (Custom Term)")
    print("-" * 80)
    main_result_2 = test_query(
        MAIN_BACKEND,
        "Calculate Internal Mobility Rate by department",
        "test-main-2",
        "Main Branch - RAG Query (should fail or give wrong answer)"
    )
    rag_result_2 = test_query(
        RAG_BACKEND,
        "Calculate Internal Mobility Rate by department",
        "test-rag-2",
        "RAG Branch - RAG Query (should use RAG)"
    )
    print_result(main_result_2, "Main Branch")
    print_result(rag_result_2, "RAG Branch")
    
    # Test 3: Cache Hit Test (ask same question twice on RAG branch)
    print("\n\n🧪 TEST 3: Cache Hit Test - Same Query Twice")
    print("-" * 80)
    print("First query (should be cache miss):")
    rag_result_3a = test_query(
        RAG_BACKEND,
        "What is the average salary by department?",
        "test-rag-cache",
        "RAG Branch - First Query (Cache Miss)"
    )
    print_result(rag_result_3a, "RAG Branch (First)")
    
    time.sleep(1)  # Small delay
    
    print("\nSecond query (should be cache hit):")
    rag_result_3b = test_query(
        RAG_BACKEND,
        "What is the average salary by department?",
        "test-rag-cache",
        "RAG Branch - Second Query (Cache Hit)"
    )
    print_result(rag_result_3b, "RAG Branch (Second)")
    
    # Test 4: Semantic Cache Test (similar but not exact query)
    print("\n\n🧪 TEST 4: Semantic Cache Test - Similar Query")
    print("-" * 80)
    print("First query:")
    rag_result_4a = test_query(
        RAG_BACKEND,
        "Show me headcount by department",
        "test-rag-semantic",
        "RAG Branch - Original Query"
    )
    print_result(rag_result_4a, "RAG Branch (Original)")
    
    time.sleep(1)
    
    print("\nSimilar query (should hit semantic cache):")
    rag_result_4b = test_query(
        RAG_BACKEND,
        "Display department headcount",
        "test-rag-semantic",
        "RAG Branch - Similar Query (Semantic Cache)"
    )
    print_result(rag_result_4b, "RAG Branch (Similar)")
    
    # Test 5: Another RAG Query
    print("\n\n🧪 TEST 5: Another RAG Query - Flight Risk Score")
    print("-" * 80)
    main_result_5 = test_query(
        MAIN_BACKEND,
        "Show me Flight Risk employees",
        "test-main-5",
        "Main Branch - Flight Risk (should fail)"
    )
    rag_result_5 = test_query(
        RAG_BACKEND,
        "Show me Flight Risk employees",
        "test-rag-5",
        "RAG Branch - Flight Risk (should use RAG)"
    )
    print_result(main_result_5, "Main Branch")
    print_result(rag_result_5, "RAG Branch")
    
    # Summary
    print("\n\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    print("\n✅ Main Branch (Port 8000):")
    print(f"   • Normal Query: {'✅' if main_result_1['success'] else '❌'}")
    print(f"   • RAG Query: {'⚠️ (Not Supported)' if not main_result_2.get('rag_used') else '✅'}")
    print(f"   • Cache: ❌ (Not Supported)")
    print(f"   • Avg Response Time: {main_result_1['response_time']:.2f}s")
    
    print("\n✅ RAG Branch (Port 8001):")
    print(f"   • Normal Query: {'✅' if rag_result_1['success'] else '❌'}")
    print(f"   • RAG Query: {'✅' if rag_result_2.get('rag_used') else '❌'}")
    print(f"   • Cache Hit: {'✅' if rag_result_3b.get('cache_hit') else '❌'}")
    print(f"   • Semantic Cache: {'✅' if rag_result_4b.get('cache_hit') else '❌'}")
    print(f"   • Avg Response Time (First): {rag_result_1['response_time']:.2f}s")
    print(f"   • Avg Response Time (Cached): {rag_result_3b['response_time']:.2f}s")
    if rag_result_3b.get('cache_hit'):
        speedup = rag_result_1['response_time'] / rag_result_3b['response_time'] if rag_result_3b['response_time'] > 0 else 0
        print(f"   • Cache Speedup: {speedup:.1f}x faster")
    
    print("\n" + "="*80)
    print("🎯 KEY DIFFERENCES:")
    print("="*80)
    print("1. Main Branch: No RAG, No Cache - Generic LLM responses only")
    print("2. RAG Branch: RAG for custom terms, Semantic Cache for speed")
    print("3. RAG Branch shows 'RAG Used' badge for custom HR terms")
    print("4. RAG Branch shows 'Cache Hit' badge for cached responses")
    print("5. RAG Branch should be faster on repeated/similar queries")
    print("\n✅ Testing Complete! Check UI at:")
    print("   • Main: http://localhost:3000")
    print("   • RAG: http://localhost:3001")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

