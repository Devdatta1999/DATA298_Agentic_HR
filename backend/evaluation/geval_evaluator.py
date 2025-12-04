"""
G-Eval Evaluation Module
Uses LLM to evaluate reasoning quality of agent responses
"""

import json
import re
from typing import Dict, List, Any, Optional
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings


class GEvalEvaluator:
    """G-Eval evaluator using LLM for meta-evaluation"""
    
    def __init__(self):
        try:
            self.llm = ChatOllama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
                temperature=0.3  # Lower temperature for more consistent evaluation
            )
            self.output_parser = StrOutputParser()
        except Exception as e:
            print(f"Warning: G-Eval LLM initialization failed: {e}")
            self.llm = None
    
    def evaluate_sql_reasoning(
        self, 
        question: str, 
        predicted_sql: str, 
        ground_truth_sql: str,
        predicted_tables: List[str],
        ground_truth_tables: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluate SQL generation reasoning quality using G-Eval
        
        Returns: {
            "score": float (1-5),
            "explanation": str,
            "reasoning_steps": List[str]
        }
        """
        if not self.llm:
            # Fallback if LLM not available
            return {
                "score": 3.0,
                "explanation": "G-Eval LLM not available",
                "reasoning_steps": []
            }
        
        prompt_template = """
You are an expert SQL evaluator. Evaluate the reasoning quality of SQL generation for an HR analytics question.

Question: {question}

Predicted SQL: {predicted_sql}

Ground Truth SQL: {ground_truth_sql}

Predicted Tables: {predicted_tables}
Ground Truth Tables: {ground_truth_tables}

Evaluation Criteria:
1. Does the predicted SQL correctly understand the question intent?
2. Are the correct tables selected?
3. Are the correct columns used?
4. Is the query structure appropriate (JOINs, GROUP BY, etc.)?
5. Even if not exact match, is the reasoning sound?

Step-by-step analysis:
1. Analyze question intent: [Your analysis]
2. Check table selection: [Your analysis]
3. Check column selection: [Your analysis]
4. Check query structure: [Your analysis]
5. Overall reasoning quality: [Your analysis]

Output format (JSON):
{{
    "score": <float 1-5>,
    "explanation": "<brief explanation>",
    "reasoning_steps": ["<step1>", "<step2>", ...]
}}

Score Guide:
- 5: Perfect reasoning, correct SQL
- 4: Minor issues, mostly correct
- 3: Some reasoning errors, partially correct
- 2: Major reasoning errors
- 1: Completely wrong reasoning

Output only valid JSON, no markdown formatting.
"""
        
        try:
            prompt = ChatPromptTemplate.from_template(prompt_template)
            chain = prompt | self.llm | self.output_parser
            
            response = chain.invoke({
                "question": question,
                "predicted_sql": predicted_sql,
                "ground_truth_sql": ground_truth_sql,
                "predicted_tables": ", ".join(predicted_tables),
                "ground_truth_tables": ", ".join(ground_truth_tables)
            })
            
            # Parse JSON response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    "score": float(result.get("score", 3.0)),
                    "explanation": result.get("explanation", ""),
                    "reasoning_steps": result.get("reasoning_steps", [])
                }
            else:
                # Fallback: extract score from text
                score_match = re.search(r'score["\']?\s*[:=]\s*([0-9.]+)', response, re.IGNORECASE)
                score = float(score_match.group(1)) if score_match else 3.0
                return {
                    "score": score,
                    "explanation": response[:200],
                    "reasoning_steps": []
                }
        except Exception as e:
            print(f"G-Eval SQL reasoning evaluation failed: {e}")
            return {
                "score": 3.0,
                "explanation": f"Evaluation error: {str(e)}",
                "reasoning_steps": []
            }
    
    def evaluate_visualization_reasoning(
        self,
        question: str,
        predicted_viz: Dict,
        ground_truth_viz: str,
        result_columns: List[str],
        result_count: int
    ) -> Dict[str, Any]:
        """
        Evaluate visualization selection reasoning quality
        
        Returns: {
            "score": float (1-5),
            "explanation": str
        }
        """
        if not self.llm:
            return {
                "score": 3.0,
                "explanation": "G-Eval LLM not available"
            }
        
        predicted_type = predicted_viz.get("visualization_type", "unknown") if predicted_viz else "unknown"
        
        prompt_template = """
You are an expert data visualization evaluator. Evaluate the reasoning quality of visualization type selection.

Question: {question}

Predicted Visualization Type: {predicted_type}
Ground Truth Visualization Type: {ground_truth_viz}

Result Columns: {result_columns}
Result Count: {result_count}

Evaluation Criteria:
1. Is the visualization type appropriate for the question?
2. Does it match the data characteristics (categorical, time-series, distribution)?
3. Is the reasoning sound even if not exact match?

Output format (JSON):
{{
    "score": <float 1-5>,
    "explanation": "<brief explanation>"
}}

Score Guide:
- 5: Perfect choice, matches data and question
- 4: Good choice, minor issues
- 3: Acceptable but not optimal
- 2: Poor choice
- 1: Completely inappropriate

Output only valid JSON, no markdown formatting.
"""
        
        try:
            prompt = ChatPromptTemplate.from_template(prompt_template)
            chain = prompt | self.llm | self.output_parser
            
            response = chain.invoke({
                "question": question,
                "predicted_type": predicted_type,
                "ground_truth_viz": ground_truth_viz,
                "result_columns": ", ".join(result_columns),
                "result_count": result_count
            })
            
            # Parse JSON response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    "score": float(result.get("score", 3.0)),
                    "explanation": result.get("explanation", "")
                }
            else:
                score_match = re.search(r'score["\']?\s*[:=]\s*([0-9.]+)', response, re.IGNORECASE)
                score = float(score_match.group(1)) if score_match else 3.0
                return {
                    "score": score,
                    "explanation": response[:200]
                }
        except Exception as e:
            print(f"G-Eval visualization reasoning evaluation failed: {e}")
            return {
                "score": 3.0,
                "explanation": f"Evaluation error: {str(e)}"
            }
    
    def evaluate_overall_reasoning(
        self,
        question: str,
        agent_response: Dict,
        ground_truth: Dict
    ) -> Dict[str, Any]:
        """
        Evaluate overall reasoning quality across all steps
        
        Returns: {
            "score": float (1-5),
            "explanation": str,
            "step_scores": Dict
        }
        """
        sql_reasoning = self.evaluate_sql_reasoning(
            question,
            agent_response.get("sql_query", ""),
            ground_truth.get("sql", ""),
            agent_response.get("tables", []),
            ground_truth.get("tables", [])
        )
        
        viz_reasoning = self.evaluate_visualization_reasoning(
            question,
            agent_response.get("visualization", {}),
            ground_truth.get("visualization_type", ""),
            agent_response.get("result_columns", []),
            len(agent_response.get("results", []))
        )
        
        # Overall score is weighted average
        overall_score = (sql_reasoning["score"] * 0.7 + viz_reasoning["score"] * 0.3)
        
        return {
            "overall_score": overall_score,
            "sql_reasoning_score": sql_reasoning["score"],
            "visualization_reasoning_score": viz_reasoning["score"],
            "explanation": f"SQL: {sql_reasoning['explanation']}; Viz: {viz_reasoning['explanation']}",
            "step_scores": {
                "sql": sql_reasoning["score"],
                "visualization": viz_reasoning["score"]
            }
        }


def aggregate_geval_scores(all_scores: List[Dict]) -> Dict[str, Any]:
    """Aggregate G-Eval scores across all test cases"""
    if not all_scores:
        return {}
    
    sql_scores = [s.get("sql_reasoning_score", 3.0) for s in all_scores if "sql_reasoning_score" in s]
    viz_scores = [s.get("visualization_reasoning_score", 3.0) for s in all_scores if "visualization_reasoning_score" in s]
    overall_scores = [s.get("overall_score", 3.0) for s in all_scores if "overall_score" in s]
    
    return {
        "sql_reasoning": {
            "mean": sum(sql_scores) / len(sql_scores) if sql_scores else 0,
            "min": min(sql_scores) if sql_scores else 0,
            "max": max(sql_scores) if sql_scores else 0
        },
        "visualization_reasoning": {
            "mean": sum(viz_scores) / len(viz_scores) if viz_scores else 0,
            "min": min(viz_scores) if viz_scores else 0,
            "max": max(viz_scores) if viz_scores else 0
        },
        "overall_reasoning": {
            "mean": sum(overall_scores) / len(overall_scores) if overall_scores else 0,
            "min": min(overall_scores) if overall_scores else 0,
            "max": max(overall_scores) if overall_scores else 0
        },
        "total_evaluations": len(all_scores)
    }

