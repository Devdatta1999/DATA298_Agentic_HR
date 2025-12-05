"""Test the best 25 demo questions and ensure they work correctly"""
import json
import requests
import time
from typing import Dict, List, Any

API_BASE = "http://localhost:8001/api"

def load_demo_questions() -> List[Dict]:
    """Load the 25 selected demo questions"""
    with open('app/patterns/demo_25_questions.json', 'r') as f:
        data = json.load(f)
    return data.get('questions', [])

def normalize_sql(sql: str) -> str:
    """Normalize SQL for comparison"""
    import re
    sql = ' '.join(sql.split())
    sql = sql.lower()
    sql = sql.replace('employees.', '')
    return sql.strip()

def compare_sql(generated: str, expected: str) -> Dict[str, Any]:
    """Compare generated SQL with expected SQL"""
    gen_norm = normalize_sql(generated)
    exp_norm = normalize_sql(expected)
    
    if gen_norm == exp_norm:
        return {"match": True, "type": "exact", "score": 1.0}
    
    # Check key components
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
    
    # Check tables
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

def test_question(q: Dict, base_session: str) -> Dict[str, Any]:
    """Test a single question"""
    question = q['question']
    expected_sql = q['sql']
    expected_viz = q.get('visualization', 'bar')
    
    print(f"\n{'='*80}")
    print(f"Testing Q{q['id']}: {question}")
    print(f"Expected: {expected_viz} chart | Pattern: {q.get('pattern_type', 'N/A')}")
    print(f"{'='*80}")
    
    start_time = time.time()
    try:
        # Use unique session per question to track individually
        # Cache matching is based on question similarity, not session
        test_session_id = f"{base_session}-q{q['id']}"
        response = requests.post(
            f"{API_BASE}/query",
            json={"question": question, "session_id": test_session_id},
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
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
        
        sql_comparison = compare_sql(generated_sql, expected_sql)
        viz_match = generated_viz == expected_viz
        
        # Print concise results
        status_icons = {
            'sql': '✅' if sql_comparison['match'] else '❌',
            'viz': '✅' if viz_match else '❌',
            'cache': '💾' if cache_hit else '🔄',
            'pattern': '🎯' if pattern_matched else '   ',
            'rag': '🧠' if rag_used else '   '
        }
        
        print(f"{status_icons['sql']} SQL | {status_icons['viz']} Viz | {status_icons['cache']} Cache | {status_icons['pattern']} Pattern | {status_icons['rag']} RAG")
        print(f"⏱️  {elapsed:.2f}s | 🔢 {tokens:,} tokens | 📊 {results_count} rows")
        
        if not sql_comparison['match']:
            print(f"   SQL Issue: Expected uses {expected_sql[:80]}...")
            print(f"              Generated: {generated_sql[:80]}...")
        if not viz_match:
            print(f"   Viz Issue: Expected {expected_viz}, Got {generated_viz}")
        
        return {
            "success": True,
            "question_id": q['id'],
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
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Timeout",
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
    print("TESTING BEST 25 DEMO QUESTIONS")
    print("="*80)
    print("\nThis test will ensure all 25 questions work correctly")
    print("After successful test, responses will be cached for demo")
    print("="*80)
    
    questions = load_demo_questions()
    # Use unique session ID per question to avoid cache interference
    # But cache will still match based on question similarity
    base_session = f"demo-25-fresh-{int(time.time())}"
    
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
        "total_time": 0,
        "issues": []
    }
    
    for i, q in enumerate(questions, 1):
        print(f"\n\n{'#'*80}")
        print(f"QUESTION {i}/{len(questions)}")
        print(f"{'#'*80}")
        
        # Use base_session for tracking, but cache matches by question similarity
        result = test_question(q, base_session)
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
            else:
                summary["issues"].append(f"Q{q['id']}: SQL mismatch")
            if result.get('visualization', {}).get('match'):
                summary["viz_correct"] += 1
            else:
                summary["issues"].append(f"Q{q['id']}: Viz mismatch - Expected {result.get('visualization', {}).get('expected')}, Got {result.get('visualization', {}).get('generated')}")
        else:
            summary["failed"] += 1
            summary["issues"].append(f"Q{q['id']}: {result.get('error', 'Unknown error')}")
        
        time.sleep(0.3)  # Small delay
    
    # Print summary
    print("\n\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    print(f"Total Questions: {summary['total']}")
    print(f"✅ Successful: {summary['successful']} ({summary['successful']/summary['total']*100:.1f}%)")
    print(f"❌ Failed: {summary['failed']} ({summary['failed']/summary['total']*100:.1f}%)")
    
    if summary['successful'] > 0:
        print(f"\n📝 SQL Correct: {summary['sql_correct']}/{summary['successful']} ({summary['sql_correct']/summary['successful']*100:.1f}%)")
        print(f"📈 Viz Correct: {summary['viz_correct']}/{summary['successful']} ({summary['viz_correct']/summary['successful']*100:.1f}%)")
        print(f"\n💾 Cache Hits: {summary['cache_hits']} ({summary['cache_hits']/summary['total']*100:.1f}%)")
        print(f"🎯 Pattern Matches: {summary['pattern_matches']} ({summary['pattern_matches']/summary['total']*100:.1f}%)")
        print(f"\n🔢 Total Tokens: {summary['total_tokens']:,}")
        print(f"⏱️  Total Time: {summary['total_time']:.2f}s")
        print(f"⏱️  Avg Time: {summary['total_time']/summary['successful']:.2f}s")
    
    if summary['issues']:
        print(f"\n⚠️  Issues Found ({len(summary['issues'])}):")
        for issue in summary['issues']:
            print(f"   - {issue}")
    else:
        print(f"\n✅ ALL QUESTIONS PASSED! Ready for demo!")
        print(f"   All 25 responses are now cached and ready to use.")
    
    # Save results
    with open('test_demo_25_results.json', 'w') as f:
        json.dump({
            "summary": summary,
            "results": results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: test_demo_25_results.json")
    
    return summary

if __name__ == "__main__":
    main()

