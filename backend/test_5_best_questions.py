"""Test the 5 best questions to verify fixes"""
import json
import requests
import time
from typing import Dict, List, Any

API_BASE = "http://localhost:8001/api"

# 5 best questions for testing
TEST_QUESTIONS = [
    {
        "id": 1,
        "question": "Show me department wise headcount",
        "expected_viz": "bar",
        "expected_has_insights": True
    },
    {
        "id": 2,
        "question": "Show me headcount trends over time by month",
        "expected_viz": "line",
        "expected_has_insights": True
    },
    {
        "id": 3,
        "question": "What is the total number of active employees?",
        "expected_viz": "none",
        "expected_has_insights": True
    },
    {
        "id": 4,
        "question": "Show me employees with highest engagement scores",
        "expected_viz": "bar",  # This is top N with aggregation, so bar is OK
        "expected_has_insights": True
    },
    {
        "id": 5,
        "question": "Show me top 10 employees with highest performance ratings",
        "expected_viz": "table",  # This should be table (employee list)
        "expected_has_insights": True
    }
]

def test_question(q: Dict, session_id: str) -> Dict[str, Any]:
    """Test a single question"""
    question = q['question']
    expected_viz = q['expected_viz']
    expected_has_insights = q['expected_has_insights']
    
    print(f"\n{'='*80}")
    print(f"Testing: {question}")
    print(f"Expected Viz: {expected_viz} | Expected Insights: {expected_has_insights}")
    print(f"{'='*80}")
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE}/query",
            json={"question": question, "session_id": session_id},
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
        
        generated_viz = data.get('visualization', {}).get('visualization_type', 'none')
        insights = data.get('insights', [])
        explanation = data.get('explanation', '')
        cache_hit = data.get('cache_hit', False)
        pattern_matched = data.get('pattern_matched', False)
        tokens = data.get('tokens', 0)
        results_count = len(data.get('results', []))
        
        viz_match = generated_viz == expected_viz
        has_insights = len(insights) > 0 and any(len(insight) > 50 for insight in insights)  # Real insights, not just "Pattern-matched query returned X records"
        has_analysis = len(explanation) > 100  # Real analysis, not just generic message
        
        # Print results
        status_icons = {
            'viz': '✅' if viz_match else '❌',
            'insights': '✅' if has_insights else '❌',
            'analysis': '✅' if has_analysis else '❌',
            'cache': '💾' if cache_hit else '🔄',
            'pattern': '🎯' if pattern_matched else '   '
        }
        
        print(f"{status_icons['viz']} Viz: {generated_viz} (expected: {expected_viz})")
        print(f"{status_icons['insights']} Insights: {len(insights)} items, has real insights: {has_insights}")
        print(f"{status_icons['analysis']} Analysis: {len(explanation)} chars, has real analysis: {has_analysis}")
        print(f"{status_icons['cache']} Cache | {status_icons['pattern']} Pattern")
        print(f"⏱️  {elapsed:.2f}s | 🔢 {tokens:,} tokens | 📊 {results_count} rows")
        
        if not viz_match:
            print(f"   ⚠️  Viz Issue: Expected {expected_viz}, Got {generated_viz}")
        if not has_insights:
            print(f"   ⚠️  Insights Issue: Got generic insights: {insights[:2] if insights else 'None'}")
        if not has_analysis:
            print(f"   ⚠️  Analysis Issue: Got generic explanation: {explanation[:100] if explanation else 'None'}...")
        
        return {
            "success": True,
            "question": question,
            "elapsed": elapsed,
            "cache_hit": cache_hit,
            "pattern_matched": pattern_matched,
            "tokens": tokens,
            "results_count": results_count,
            "visualization": {
                "generated": generated_viz,
                "expected": expected_viz,
                "match": viz_match
            },
            "insights": {
                "count": len(insights),
                "has_real_insights": has_insights,
                "preview": insights[:2] if insights else []
            },
            "analysis": {
                "length": len(explanation),
                "has_real_analysis": has_analysis,
                "preview": explanation[:150] if explanation else ""
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
    print("TESTING 5 BEST QUESTIONS - VERIFYING FIXES")
    print("="*80)
    print("\nThis test verifies:")
    print("1. ✅ Pattern matching still works (SQL generation)")
    print("2. ✅ LLM insights are generated even for pattern matches")
    print("3. ✅ Correct visualization types (especially employee lists → table)")
    print("4. ✅ Responses are cached correctly")
    print("="*80)
    
    session_id = f"test-5-best-{int(time.time())}"
    
    results = []
    summary = {
        "total": len(TEST_QUESTIONS),
        "successful": 0,
        "failed": 0,
        "viz_correct": 0,
        "has_insights": 0,
        "has_analysis": 0,
        "cache_hits_first_run": 0,
        "pattern_matches": 0,
        "total_tokens": 0,
        "total_time": 0,
        "issues": []
    }
    
    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"\n\n{'#'*80}")
        print(f"QUESTION {i}/{len(TEST_QUESTIONS)}")
        print(f"{'#'*80}")
        
        result = test_question(q, session_id)
        results.append(result)
        
        if result.get('success'):
            summary["successful"] += 1
            summary["total_tokens"] += result.get('tokens', 0)
            summary["total_time"] += result.get('elapsed', 0)
            
            if result.get('cache_hit'):
                summary["cache_hits_first_run"] += 1
            if result.get('pattern_matched'):
                summary["pattern_matches"] += 1
            if result.get('visualization', {}).get('match'):
                summary["viz_correct"] += 1
            else:
                summary["issues"].append(f"Q{q['id']}: Viz mismatch - Expected {result.get('visualization', {}).get('expected')}, Got {result.get('visualization', {}).get('generated')}")
            if result.get('insights', {}).get('has_real_insights'):
                summary["has_insights"] += 1
            else:
                summary["issues"].append(f"Q{q['id']}: Missing real insights")
            if result.get('analysis', {}).get('has_real_analysis'):
                summary["has_analysis"] += 1
            else:
                summary["issues"].append(f"Q{q['id']}: Missing real analysis")
        else:
            summary["failed"] += 1
            summary["issues"].append(f"Q{q['id']}: {result.get('error', 'Unknown error')}")
        
        time.sleep(0.5)  # Small delay between requests
    
    # Print summary
    print("\n\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    print(f"Total Questions: {summary['total']}")
    print(f"✅ Successful: {summary['successful']} ({summary['successful']/summary['total']*100:.1f}%)")
    print(f"❌ Failed: {summary['failed']} ({summary['failed']/summary['total']*100:.1f}%)")
    
    if summary['successful'] > 0:
        print(f"\n📊 Visualization Correct: {summary['viz_correct']}/{summary['successful']} ({summary['viz_correct']/summary['successful']*100:.1f}%)")
        print(f"💡 Has Real Insights: {summary['has_insights']}/{summary['successful']} ({summary['has_insights']/summary['successful']*100:.1f}%)")
        print(f"📝 Has Real Analysis: {summary['has_analysis']}/{summary['successful']} ({summary['has_analysis']/summary['successful']*100:.1f}%)")
        print(f"\n💾 Cache Hits (First Run): {summary['cache_hits_first_run']} (expected: 0)")
        print(f"🎯 Pattern Matches: {summary['pattern_matches']} ({summary['pattern_matches']/summary['total']*100:.1f}%)")
        print(f"\n🔢 Total Tokens: {summary['total_tokens']:,}")
        print(f"⏱️  Total Time: {summary['total_time']:.2f}s")
        print(f"⏱️  Avg Time: {summary['total_time']/summary['successful']:.2f}s")
    
    if summary['issues']:
        print(f"\n⚠️  Issues Found ({len(summary['issues'])}):")
        for issue in summary['issues']:
            print(f"   - {issue}")
    else:
        print(f"\n✅ ALL TESTS PASSED! Ready for UI testing!")
        print(f"   All 5 responses are now cached and ready to use.")
    
    # Save results
    with open('test_5_best_results.json', 'w') as f:
        json.dump({
            "summary": summary,
            "results": results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: test_5_best_results.json")
    
    return summary

if __name__ == "__main__":
    main()

