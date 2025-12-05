"""Test first 25 questions and verify SQL and visualization correctness"""
import json
import requests
import time
from typing import Dict, List, Any

API_BASE = "http://localhost:8001/api"

def load_questions() -> List[Dict]:
    """Load first 25 questions"""
    with open('app/patterns/comprehensive_questions.json', 'r') as f:
        data = json.load(f)
    return data.get('questions', [])[:25]

def normalize_sql(sql: str) -> str:
    """Normalize SQL for comparison"""
    import re
    # Remove extra whitespace
    sql = ' '.join(sql.split())
    # Normalize case
    sql = sql.lower()
    # Remove schema prefix variations
    sql = sql.replace('employees.', '')
    return sql.strip()

def compare_sql(generated: str, expected: str) -> Dict[str, Any]:
    """Compare generated SQL with expected SQL"""
    gen_norm = normalize_sql(generated)
    exp_norm = normalize_sql(expected)
    
    # Exact match
    if gen_norm == exp_norm:
        return {"match": True, "type": "exact", "score": 1.0}
    
    # Check if key components match
    key_components = {
        "select": "select" in gen_norm and "select" in exp_norm,
        "from": "from" in gen_norm and "from" in exp_norm,
        "where": ("where" in gen_norm) == ("where" in exp_norm),
        "group_by": ("group by" in gen_norm) == ("group by" in exp_norm),
        "order_by": ("order by" in gen_norm) == ("order by" in exp_norm),
        "limit": ("limit" in gen_norm) == ("limit" in exp_norm),
    }
    
    match_count = sum(key_components.values())
    score = match_count / len(key_components)
    
    # Check if tables match
    import re
    gen_tables = set(re.findall(r'from\s+(\w+)', gen_norm))
    exp_tables = set(re.findall(r'from\s+(\w+)', exp_norm))
    tables_match = gen_tables == exp_tables
    
    return {
        "match": score >= 0.8 and tables_match,
        "type": "semantic" if score >= 0.8 else "mismatch",
        "score": score,
        "tables_match": tables_match,
        "components": key_components
    }

def test_question(q: Dict, session_id: str, use_unique_session: bool = True) -> Dict[str, Any]:
    """Test a single question"""
    question = q['question']
    expected_sql = q['sql']
    expected_viz = q.get('visualization', 'bar')
    
    # Use unique session ID to avoid cache hits (for testing pattern matching)
    test_session_id = f"{session_id}-q{q['id']}" if use_unique_session else session_id
    
    print(f"\n{'='*80}")
    print(f"Testing: {question}")
    print(f"Expected Pattern: {q.get('pattern_type', 'N/A')}")
    print(f"Expected Viz: {expected_viz}")
    print(f"{'='*80}")
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE}/query",
            json={"question": question, "session_id": test_session_id},
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:200]}",
                "elapsed": elapsed
            }
        
        data = response.json()
        
        if not data.get('success'):
            return {
                "success": False,
                "error": data.get('error', 'Unknown error'),
                "elapsed": elapsed
            }
        
        generated_sql = data.get('sql_query', '')
        generated_viz = data.get('visualization', {}).get('visualization_type', 'none')
        cache_hit = data.get('cache_hit', False)
        pattern_matched = data.get('pattern_matched', False)
        rag_used = data.get('rag_used', False)
        tokens = data.get('query_tokens', 0)
        results_count = len(data.get('results', []))
        
        # Compare SQL
        sql_comparison = compare_sql(generated_sql, expected_sql)
        
        # Compare visualization
        viz_match = generated_viz == expected_viz
        
        result = {
            "success": True,
            "question": question,
            "elapsed": elapsed,
            "cache_hit": cache_hit,
            "pattern_matched": pattern_matched,
            "rag_used": rag_used,
            "tokens": tokens,
            "results_count": results_count,
            "sql": {
                "generated": generated_sql,
                "expected": expected_sql,
                "comparison": sql_comparison
            },
            "visualization": {
                "generated": generated_viz,
                "expected": expected_viz,
                "match": viz_match
            }
        }
        
        # Print results
        print(f"⏱️  Time: {elapsed:.2f}s")
        print(f"💾 Cache: {'✅ HIT' if cache_hit else '❌ MISS'}")
        print(f"🎯 Pattern: {'✅ MATCHED' if pattern_matched else '❌ NOT MATCHED'}")
        print(f"🧠 RAG: {'✅ USED' if rag_used else '❌ NOT USED'}")
        print(f"🔢 Tokens: {tokens:,}")
        print(f"📊 Results: {results_count} rows")
        
        print(f"\n📝 SQL Comparison:")
        print(f"   Expected: {expected_sql[:100]}...")
        print(f"   Generated: {generated_sql[:100]}...")
        print(f"   Match: {'✅' if sql_comparison['match'] else '❌'} ({sql_comparison['type']}, score: {sql_comparison['score']:.2f})")
        
        print(f"\n📈 Visualization:")
        print(f"   Expected: {expected_viz}")
        print(f"   Generated: {generated_viz}")
        print(f"   Match: {'✅' if viz_match else '❌'}")
        
        return result
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout (>120s)",
            "elapsed": time.time() - start_time
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "elapsed": time.time() - start_time
        }

def main():
    """Main test function"""
    print("="*80)
    print("TESTING FIRST 25 QUESTIONS")
    print("="*80)
    
    questions = load_questions()
    session_id = f"test-first-25-{int(time.time())}"
    
    results = []
    summary = {
        "total": len(questions),
        "successful": 0,
        "failed": 0,
        "sql_correct": 0,
        "viz_correct": 0,
        "cache_hits": 0,
        "pattern_matches": 0,
        "total_tokens": 0,
        "total_time": 0
    }
    
    for i, q in enumerate(questions, 1):
        print(f"\n\n{'#'*80}")
        print(f"QUESTION {i}/{len(questions)}")
        print(f"{'#'*80}")
        
        result = test_question(q, session_id)
        results.append(result)
        
        if result.get('success'):
            summary["successful"] += 1
            summary["total_tokens"] += result.get('tokens', 0)
            summary["total_time"] += result.get('elapsed', 0)
            
            if result.get('cache_hit'):
                summary["cache_hits"] += 1
            if result.get('pattern_matched'):
                summary["pattern_matches"] += 1
            if result.get('sql', {}).get('comparison', {}).get('match'):
                summary["sql_correct"] += 1
            if result.get('visualization', {}).get('match'):
                summary["viz_correct"] += 1
        else:
            summary["failed"] += 1
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Print summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Questions: {summary['total']}")
    print(f"Successful: {summary['successful']} ({summary['successful']/summary['total']*100:.1f}%)")
    print(f"Failed: {summary['failed']} ({summary['failed']/summary['total']*100:.1f}%)")
    print(f"\nSQL Correct: {summary['sql_correct']} ({summary['sql_correct']/summary['successful']*100:.1f}%)" if summary['successful'] > 0 else "\nSQL Correct: N/A")
    print(f"Viz Correct: {summary['viz_correct']} ({summary['viz_correct']/summary['successful']*100:.1f}%)" if summary['successful'] > 0 else "\nViz Correct: N/A")
    print(f"\nCache Hits: {summary['cache_hits']} ({summary['cache_hits']/summary['total']*100:.1f}%)")
    print(f"Pattern Matches: {summary['pattern_matches']} ({summary['pattern_matches']/summary['total']*100:.1f}%)")
    print(f"\nTotal Tokens: {summary['total_tokens']:,}")
    print(f"Total Time: {summary['total_time']:.2f}s")
    print(f"Avg Time per Query: {summary['total_time']/summary['successful']:.2f}s" if summary['successful'] > 0 else "Avg Time: N/A")
    
    # Save detailed results
    with open('test_first_25_results.json', 'w') as f:
        json.dump({
            "summary": summary,
            "results": results
        }, f, indent=2)
    
    print(f"\n✅ Detailed results saved to: test_first_25_results.json")
    
    # Identify issues
    print("\n" + "="*80)
    print("ISSUES FOUND")
    print("="*80)
    
    issues = []
    for i, result in enumerate(results, 1):
        if not result.get('success'):
            issues.append(f"Q{i}: {result.get('error', 'Unknown error')}")
        else:
            if not result.get('sql', {}).get('comparison', {}).get('match'):
                issues.append(f"Q{i}: SQL mismatch - {result.get('question', '')[:50]}")
            if not result.get('visualization', {}).get('match'):
                issues.append(f"Q{i}: Viz mismatch - Expected {result.get('visualization', {}).get('expected')}, Got {result.get('visualization', {}).get('generated')}")
    
    if issues:
        for issue in issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ No issues found!")
    
    return summary

if __name__ == "__main__":
    main()

