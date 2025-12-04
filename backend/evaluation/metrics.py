"""
Evaluation Metrics Calculation Module
Calculates all objective metrics for agent evaluation
"""

import re
import statistics
from typing import Dict, List, Any, Tuple
from app.database import execute_sql_query


def normalize_sql(sql: str) -> str:
    """Normalize SQL for comparison (remove whitespace, case insensitive)"""
    # Remove extra whitespace
    sql = re.sub(r'\s+', ' ', sql.strip())
    # Convert to lowercase for comparison
    sql = sql.lower()
    # Remove trailing semicolons
    sql = sql.rstrip(';')
    return sql


def evaluate_sql_exact_match(predicted_sql: str, ground_truth_sql: str) -> bool:
    """Check if predicted SQL exactly matches ground truth (normalized)"""
    pred_normalized = normalize_sql(predicted_sql)
    gt_normalized = normalize_sql(ground_truth_sql)
    return pred_normalized == gt_normalized


def evaluate_sql_semantic_match(predicted_sql: str, ground_truth_sql: str) -> Tuple[bool, Dict]:
    """
    Check if predicted SQL produces same results as ground truth
    Returns: (match: bool, details: dict)
    """
    try:
        pred_results = execute_sql_query(predicted_sql)
        gt_results = execute_sql_query(ground_truth_sql)
        
        # Normalize results for comparison (convert to comparable format)
        pred_normalized = normalize_results(pred_results)
        gt_normalized = normalize_results(gt_results)
        
        match = pred_normalized == gt_normalized
        
        return match, {
            "predicted_rows": len(pred_results),
            "ground_truth_rows": len(gt_results),
            "match": match
        }
    except Exception as e:
        return False, {
            "error": str(e),
            "match": False
        }


def normalize_results(results: List[Dict]) -> List[Tuple]:
    """Normalize query results for comparison"""
    if not results:
        return []
    
    # Sort by all keys to ensure consistent comparison
    sorted_results = []
    for row in results:
        # Convert dict to sorted tuple of (key, value) pairs
        sorted_row = tuple(sorted(row.items()))
        sorted_results.append(sorted_row)
    
    return sorted(sorted_results)


def evaluate_sql_structure(predicted_sql: str, ground_truth_sql: str) -> Dict[str, Any]:
    """
    Compare SQL structure: tables, columns, aggregations
    Returns structure similarity score
    """
    def extract_tables(sql: str) -> set:
        # Simple extraction - look for FROM and JOIN clauses
        tables = set()
        sql_lower = sql.lower()
        # Match table names after FROM and JOIN
        matches = re.findall(r'(?:from|join)\s+([a-z_]+\.?[a-z_]+)', sql_lower)
        for match in matches:
            tables.add(match.strip())
        return tables
    
    def extract_columns(sql: str) -> set:
        # Extract column names from SELECT
        columns = set()
        sql_lower = sql.lower()
        # Match column names in SELECT
        matches = re.findall(r'select\s+(.*?)\s+from', sql_lower, re.DOTALL)
        if matches:
            cols = matches[0].split(',')
            for col in cols:
                # Remove aliases, functions, etc.
                col = re.sub(r'\s+as\s+\w+', '', col)
                col = re.sub(r'^\w+\(', '', col)  # Remove function names
                col = col.strip().strip('"').strip("'")
                if col:
                    columns.add(col)
        return columns
    
    def extract_aggregations(sql: str) -> set:
        # Extract aggregation functions
        aggs = set()
        sql_lower = sql.lower()
        agg_functions = ['count', 'sum', 'avg', 'max', 'min']
        for func in agg_functions:
            if func in sql_lower:
                aggs.add(func)
        return aggs
    
    pred_tables = extract_tables(predicted_sql)
    gt_tables = extract_tables(ground_truth_sql)
    
    pred_columns = extract_columns(predicted_sql)
    gt_columns = extract_columns(ground_truth_sql)
    
    pred_aggs = extract_aggregations(predicted_sql)
    gt_aggs = extract_aggregations(ground_truth_sql)
    
    # Calculate similarity scores
    table_match = pred_tables == gt_tables
    table_similarity = len(pred_tables & gt_tables) / len(pred_tables | gt_tables) if (pred_tables | gt_tables) else 0
    
    column_match = pred_columns == gt_columns
    column_similarity = len(pred_columns & gt_columns) / len(pred_columns | gt_columns) if (pred_columns | gt_columns) else 0
    
    agg_match = pred_aggs == gt_aggs
    agg_similarity = len(pred_aggs & gt_aggs) / len(pred_aggs | gt_aggs) if (pred_aggs | gt_aggs) else 0
    
    # Overall structure score (weighted average)
    structure_score = (table_similarity * 0.4 + column_similarity * 0.4 + agg_similarity * 0.2)
    
    return {
        "table_match": table_match,
        "table_similarity": table_similarity,
        "column_match": column_match,
        "column_similarity": column_similarity,
        "aggregation_match": agg_match,
        "aggregation_similarity": agg_similarity,
        "structure_score": structure_score
    }


def evaluate_visualization(predicted_viz: Dict, ground_truth_viz: str) -> bool:
    """Check if predicted visualization type matches ground truth"""
    if not predicted_viz:
        return False
    predicted_type = predicted_viz.get("visualization_type", "").lower()
    ground_truth_type = ground_truth_viz.lower()
    return predicted_type == ground_truth_type


def evaluate_table_selection(predicted_tables: List[str], ground_truth_tables: List[str]) -> Dict[str, Any]:
    """Evaluate table selection accuracy"""
    pred_set = set(predicted_tables or [])
    gt_set = set(ground_truth_tables or [])
    
    exact_match = pred_set == gt_set
    precision = len(pred_set & gt_set) / len(pred_set) if pred_set else 0
    recall = len(pred_set & gt_set) / len(gt_set) if gt_set else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "exact_match": exact_match,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "predicted_tables": list(pred_set),
        "ground_truth_tables": list(gt_set)
    }


def evaluate_column_selection(predicted_columns: Dict, ground_truth_columns: Dict) -> Dict[str, Any]:
    """Evaluate column selection accuracy"""
    if not predicted_columns or not ground_truth_columns:
        return {
            "exact_match": False,
            "precision": 0,
            "recall": 0,
            "f1_score": 0
        }
    
    # Flatten column dictionaries
    pred_all = set()
    gt_all = set()
    
    for table, cols in predicted_columns.items():
        for col in cols:
            pred_all.add(f"{table}.{col}")
    
    for table, cols in ground_truth_columns.items():
        for col in cols:
            gt_all.add(f"{table}.{col}")
    
    exact_match = pred_all == gt_all
    precision = len(pred_all & gt_all) / len(pred_all) if pred_all else 0
    recall = len(pred_all & gt_all) / len(gt_all) if gt_all else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "exact_match": exact_match,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


def calculate_latency_percentiles(latencies: List[float]) -> Dict[str, float]:
    """Calculate latency percentiles (p50, p95, p99)"""
    if not latencies:
        return {"p50": 0, "p95": 0, "p99": 0, "mean": 0, "min": 0, "max": 0}
    
    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)
    
    p50 = sorted_latencies[int(n * 0.50)] if n > 0 else 0
    p95 = sorted_latencies[int(n * 0.95)] if n > 0 else sorted_latencies[-1]
    p99 = sorted_latencies[int(n * 0.99)] if n > 0 else sorted_latencies[-1]
    mean = statistics.mean(sorted_latencies)
    min_latency = min(sorted_latencies)
    max_latency = max(sorted_latencies)
    
    return {
        "p50": p50,
        "p95": p95,
        "p99": p99,
        "mean": mean,
        "min": min_latency,
        "max": max_latency
    }


def calculate_token_statistics(tokens: List[int]) -> Dict[str, float]:
    """Calculate token usage statistics"""
    if not tokens:
        return {"mean": 0, "min": 0, "max": 0, "total": 0}
    
    return {
        "mean": statistics.mean(tokens),
        "median": statistics.median(tokens),
        "min": min(tokens),
        "max": max(tokens),
        "total": sum(tokens)
    }


def calculate_completion_rate(results: List[Dict]) -> Dict[str, Any]:
    """Calculate task completion rate"""
    total = len(results)
    successful = sum(1 for r in results if r.get("success", False))
    failed = total - successful
    
    # Categorize failures
    failure_reasons = {}
    for r in results:
        if not r.get("success", False):
            error = r.get("error", "Unknown")
            error_type = error.split(":")[0] if ":" in error else error
            failure_reasons[error_type] = failure_reasons.get(error_type, 0) + 1
    
    return {
        "completion_rate": successful / total if total > 0 else 0,
        "success_count": successful,
        "failure_count": failed,
        "total_count": total,
        "failure_reasons": failure_reasons
    }


def calculate_accuracy_by_category(results: List[Dict], category_key: str = "category") -> Dict[str, Dict]:
    """Calculate accuracy metrics grouped by category"""
    categories = {}
    
    for result in results:
        category = result.get(category_key, "unknown")
        if category not in categories:
            categories[category] = {
                "total": 0,
                "sql_exact_match": 0,
                "sql_semantic_match": 0,
                "viz_match": 0,
                "table_match": 0
            }
        
        categories[category]["total"] += 1
        
        if result.get("sql_exact_match"):
            categories[category]["sql_exact_match"] += 1
        if result.get("sql_semantic_match"):
            categories[category]["sql_semantic_match"] += 1
        if result.get("viz_match"):
            categories[category]["viz_match"] += 1
        if result.get("table_selection", {}).get("exact_match"):
            categories[category]["table_match"] += 1
    
    # Calculate percentages
    for category, metrics in categories.items():
        total = metrics["total"]
        if total > 0:
            metrics["sql_exact_match_pct"] = metrics["sql_exact_match"] / total * 100
            metrics["sql_semantic_match_pct"] = metrics["sql_semantic_match"] / total * 100
            metrics["viz_match_pct"] = metrics["viz_match"] / total * 100
            metrics["table_match_pct"] = metrics["table_match"] / total * 100
    
    return categories

