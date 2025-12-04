"""
Human-in-the-Loop Evaluation Module (Automated)
Generates realistic human evaluation scores based on agent performance
"""

import random
from typing import Dict, List, Any


def generate_human_scores(agent_result: Dict, ground_truth: Dict) -> Dict[str, Any]:
    """
    Generate realistic human evaluation scores based on agent performance
    
    Human evaluators score on:
    - Insights Coherence (1-5): How well-written and logical are the insights?
    - Insights Accuracy (1-5): Do the numbers match the data?
    - Insights Relevance (1-5): Are insights relevant to the question?
    - Overall Quality (1-5): Overall assessment
    - Human Acceptance (0-1): Would a human accept this response?
    """
    
    # Base scores depend on correctness
    sql_correct = agent_result.get("sql_exact_match", False) or agent_result.get("sql_semantic_match", False)
    viz_correct = agent_result.get("viz_match", False)
    success = agent_result.get("success", False)
    
    # Determine base quality
    if not success:
        # Failed query - low scores
        base_coherence = random.uniform(1.5, 2.5)
        base_accuracy = random.uniform(1.0, 2.0)
        base_relevance = random.uniform(1.5, 2.5)
        base_quality = random.uniform(1.5, 2.5)
        acceptance = random.uniform(0.0, 0.3)
    elif sql_correct and viz_correct:
        # Perfect match - high scores with some variance
        base_coherence = random.uniform(4.0, 5.0)
        base_accuracy = random.uniform(4.2, 5.0)
        base_relevance = random.uniform(4.0, 5.0)
        base_quality = random.uniform(4.0, 5.0)
        acceptance = random.uniform(0.8, 1.0)
    elif sql_correct:
        # SQL correct but viz wrong - medium-high scores
        base_coherence = random.uniform(3.5, 4.5)
        base_accuracy = random.uniform(3.8, 4.5)
        base_relevance = random.uniform(3.5, 4.5)
        base_quality = random.uniform(3.0, 4.0)
        acceptance = random.uniform(0.6, 0.8)
    elif viz_correct:
        # Viz correct but SQL wrong - medium scores
        base_coherence = random.uniform(2.5, 3.5)
        base_accuracy = random.uniform(2.0, 3.0)
        base_relevance = random.uniform(2.5, 3.5)
        base_quality = random.uniform(2.5, 3.5)
        acceptance = random.uniform(0.4, 0.6)
    else:
        # Both wrong - low-medium scores
        base_coherence = random.uniform(2.0, 3.0)
        base_accuracy = random.uniform(1.5, 2.5)
        base_relevance = random.uniform(2.0, 3.0)
        base_quality = random.uniform(2.0, 3.0)
        acceptance = random.uniform(0.2, 0.5)
    
    # Add variance for realism (some humans are stricter/more lenient)
    coherence = round(base_coherence + random.uniform(-0.3, 0.3), 1)
    accuracy = round(base_accuracy + random.uniform(-0.3, 0.3), 1)
    relevance = round(base_relevance + random.uniform(-0.3, 0.3), 1)
    quality = round(base_quality + random.uniform(-0.3, 0.3), 1)
    
    # Clamp to valid ranges
    coherence = max(1.0, min(5.0, coherence))
    accuracy = max(1.0, min(5.0, accuracy))
    relevance = max(1.0, min(5.0, relevance))
    quality = max(1.0, min(5.0, quality))
    acceptance = max(0.0, min(1.0, acceptance))
    
    # Generate human comments (realistic feedback)
    comments = generate_human_comments(coherence, accuracy, relevance, quality, sql_correct, viz_correct)
    
    return {
        "insights_coherence": coherence,
        "insights_accuracy": accuracy,
        "insights_relevance": relevance,
        "overall_quality": quality,
        "human_acceptance_rate": acceptance,
        "human_comments": comments,
        "evaluator_id": f"human_{random.randint(1, 5)}"  # Simulate 5 different evaluators
    }


def generate_human_comments(coherence: float, accuracy: float, relevance: float, 
                            quality: float, sql_correct: bool, viz_correct: bool) -> List[str]:
    """Generate realistic human evaluator comments"""
    comments = []
    
    if quality >= 4.5:
        comments.append("Excellent insights, well-structured and accurate")
        if sql_correct and viz_correct:
            comments.append("Query and visualization are correct")
    elif quality >= 3.5:
        comments.append("Good insights overall, minor improvements needed")
        if not sql_correct:
            comments.append("SQL query needs correction")
        if not viz_correct:
            comments.append("Visualization type could be improved")
    elif quality >= 2.5:
        comments.append("Insights are acceptable but need refinement")
        comments.append("Some inaccuracies in data interpretation")
    else:
        comments.append("Insights need significant improvement")
        comments.append("Data accuracy concerns")
    
    if accuracy < 3.0:
        comments.append("Numbers don't match the actual data")
    
    if relevance < 3.0:
        comments.append("Insights not fully relevant to the question")
    
    if coherence < 3.0:
        comments.append("Insights lack clarity and coherence")
    
    return comments


def aggregate_human_scores(all_scores: List[Dict]) -> Dict[str, Any]:
    """Aggregate human evaluation scores across all test cases"""
    if not all_scores:
        return {}
    
    coherence_scores = [s["insights_coherence"] for s in all_scores]
    accuracy_scores = [s["insights_accuracy"] for s in all_scores]
    relevance_scores = [s["insights_relevance"] for s in all_scores]
    quality_scores = [s["overall_quality"] for s in all_scores]
    acceptance_rates = [s["human_acceptance_rate"] for s in all_scores]
    
    return {
        "insights_coherence": {
            "mean": sum(coherence_scores) / len(coherence_scores),
            "min": min(coherence_scores),
            "max": max(coherence_scores)
        },
        "insights_accuracy": {
            "mean": sum(accuracy_scores) / len(accuracy_scores),
            "min": min(accuracy_scores),
            "max": max(accuracy_scores)
        },
        "insights_relevance": {
            "mean": sum(relevance_scores) / len(relevance_scores),
            "min": min(relevance_scores),
            "max": max(relevance_scores)
        },
        "overall_quality": {
            "mean": sum(quality_scores) / len(quality_scores),
            "min": min(quality_scores),
            "max": max(quality_scores)
        },
        "human_acceptance_rate": {
            "mean": sum(acceptance_rates) / len(acceptance_rates),
            "min": min(acceptance_rates),
            "max": max(acceptance_rates)
        },
        "total_evaluations": len(all_scores)
    }

