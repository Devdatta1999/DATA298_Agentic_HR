import json
import re
from typing import Dict, List, Any, Optional
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
from app.database import execute_sql_query, validate_sql_query
from app.agent.prompts import (
    SQL_GENERATION_PROMPT,
    TABLE_COLUMN_IDENTIFICATION_PROMPT,
    VISUALIZATION_RECOMMENDATION_PROMPT,
    INSIGHTS_GENERATION_PROMPT
)
from app.services.token_counter import token_counter
from app.rag.rag_retriever import RAGRetriever
from app.cache.semantic_cache import SemanticCache
import logging

logger = logging.getLogger(__name__)


class HRAgent:
    """HR Analytics Agent using LangChain and Ollama"""
    
    def __init__(self):
        try:
            self.llm = ChatOllama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
                temperature=0.1
            )
            self.output_parser = StrOutputParser()
            
            # Initialize RAG and Cache
            try:
                self.rag_retriever = RAGRetriever()
                logger.info("RAG retriever initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize RAG retriever: {e}. RAG will be disabled.")
                self.rag_retriever = None
            
            try:
                self.semantic_cache = SemanticCache()
                logger.info("Semantic cache initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize semantic cache: {e}. Caching will be disabled.")
                self.semantic_cache = None
        except Exception as e:
            raise Exception(f"Failed to initialize LLM: {str(e)}. Make sure Ollama is running at {settings.OLLAMA_BASE_URL}")
    
    def generate_sql(self, question: str, conversation_history: List[Dict] = None, rag_context: str = "") -> Dict[str, Any]:
        """Generate SQL query from natural language question
        Returns: {"sql": str, "tokens": int}
        """
        try:
            # Format conversation history
            history_text = ""
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    history_text += f"{role}: {content}\n"
            
            # Add RAG context to prompt if available
            prompt_template = SQL_GENERATION_PROMPT
            if rag_context:
                # Append RAG context to the prompt
                prompt_template = SQL_GENERATION_PROMPT + "\n\n" + rag_context
            
            prompt = ChatPromptTemplate.from_template(prompt_template)
            chain = prompt | self.llm | self.output_parser
            
            # Build full prompt for token counting
            full_prompt = prompt.format(question=question, conversation_history=history_text)
            
            response = chain.invoke({
                "question": question,
                "conversation_history": history_text
            })
            
            # Count tokens
            prompt_tokens = token_counter.count_tokens(full_prompt)
            response_tokens = token_counter.count_tokens(response)
            total_tokens = prompt_tokens + response_tokens
            
            # Extract SQL query (remove markdown code blocks if present)
            sql_query = response.strip()
            sql_query = re.sub(r'```sql\n?', '', sql_query)
            sql_query = re.sub(r'```\n?', '', sql_query)
            sql_query = sql_query.strip()
            
            if not sql_query:
                raise Exception("LLM returned empty SQL query")
            
            return {
                "sql": sql_query,
                "tokens": total_tokens
            }
        except Exception as e:
            raise Exception(f"SQL generation failed: {str(e)}")
    
    def identify_tables_columns(self, question: str, sql_query: str) -> Dict[str, Any]:
        """Identify tables and columns used in the query
        Returns: {"tables": [], "columns": {}, "tokens": int}
        """
        tokens_used = 0
        try:
            prompt = ChatPromptTemplate.from_template(TABLE_COLUMN_IDENTIFICATION_PROMPT)
            chain = prompt | self.llm | self.output_parser
            
            full_prompt = prompt.format(question=question, sql_query=sql_query)
            
            response = chain.invoke({
                "question": question,
                "sql_query": sql_query
            })
            
            # Count tokens
            tokens_used = token_counter.count_tokens(full_prompt) + token_counter.count_tokens(response)
            
            # Try to parse JSON response
            try:
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    if parsed.get("tables") and parsed.get("columns"):
                        parsed["tokens"] = tokens_used
                        return parsed
            except Exception as e:
                print(f"Warning: Failed to parse LLM response for table/column identification: {e}")
        except Exception as e:
            print(f"Warning: LLM call failed for table/column identification: {e}")
        
        # Fallback: parse from SQL query directly (improved parsing)
        tables = []
        columns = {}
        
        # Extract table names (improved pattern)
        table_pattern = r'employees\.(\w+)'
        tables_found = re.findall(table_pattern, sql_query, re.IGNORECASE)
        tables = list(set(tables_found))
        
        if not tables:
            return {"tables": [], "columns": {}}
        
        # Extract columns from SELECT clause
        select_pattern = r'SELECT\s+(.*?)\s+FROM'
        select_match = re.search(select_pattern, sql_query, re.IGNORECASE | re.DOTALL)
        select_columns = []
        if select_match:
            select_clause = select_match.group(1)
            # Extract quoted column names first
            quoted_cols = re.findall(r'"(\w+)"', select_clause)
            # Extract unquoted column names
            unquoted_cols = re.findall(r'\b(\w+)\b', select_clause)
            # Combine and filter
            all_cols = list(set(quoted_cols + unquoted_cols))
            sql_keywords = {'as', 'count', 'sum', 'avg', 'max', 'min', 'distinct', 'select', 'case', 'when', 'then', 'else', 'end'}
            select_columns = [c for c in all_cols if c.lower() not in sql_keywords and len(c) > 1]
        
        # Extract columns from WHERE, GROUP BY, ORDER BY
        where_pattern = r'WHERE\s+(.*?)(?:GROUP|ORDER|LIMIT|$)'
        where_match = re.search(where_pattern, sql_query, re.IGNORECASE | re.DOTALL)
        where_columns = []
        if where_match:
            where_clause = where_match.group(1)
            where_cols = re.findall(r'"(\w+)"', where_clause)
            where_columns.extend(where_cols)
        
        # Extract columns from JOIN clauses
        join_pattern = r'JOIN\s+employees\.(\w+)\s+.*?ON\s+.*?"(\w+)"'
        join_matches = re.findall(join_pattern, sql_query, re.IGNORECASE)
        join_columns = []
        for match in join_matches:
            join_columns.extend([m for m in match if m])
        
        # Combine all columns
        all_columns = list(set(select_columns + where_columns + join_columns))
        
        # Map columns to tables (simplified - assign to first table or all tables)
        for table in tables:
            table_full = f"employees.{table}"
            # Try to match columns that might belong to this table
            table_cols = [col for col in all_columns if col]
            columns[table_full] = table_cols if table_cols else []
        
        return {
            "tables": [f"employees.{t}" for t in tables],
            "columns": columns,
            "tokens": tokens_used
        }
    
    def recommend_visualization(self, query: str, results: List[Dict], columns: List[str]) -> Dict[str, Any]:
        """Recommend visualization type based on query results
        Returns: {"visualization_type": str, ..., "tokens": int}
        """
        tokens_used = 0
        if not results:
            return {
                "visualization_type": "none",
                "x_axis": None,
                "y_axis": None,
                "explanation": "No data to visualize",
                "tokens": 0
            }
        
        result_count = len(results)
        sample_data = json.dumps(results[:3], indent=2) if results else "[]"
        
        try:
            prompt = ChatPromptTemplate.from_template(VISUALIZATION_RECOMMENDATION_PROMPT)
            chain = prompt | self.llm | self.output_parser
            
            full_prompt = prompt.format(
                query=query,
                result_count=result_count,
                columns=", ".join(columns),
                sample_data=sample_data
            )
            
            response = chain.invoke({
                "query": query,
                "result_count": result_count,
                "columns": ", ".join(columns),
                "sample_data": sample_data
            })
            
            # Count tokens
            tokens_used = token_counter.count_tokens(full_prompt) + token_counter.count_tokens(response)
            
            # Try to parse JSON
            try:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    viz_data = json.loads(json_match.group())
                    viz_data["tokens"] = tokens_used
                    
                    # Override visualization based on query type
                    if result_columns:
                        query_lower = query.lower()
                        
                        # Check for distribution queries - force pie chart
                        is_distribution = any(keyword in query_lower for keyword in 
                            ['distribution', 'percentage', 'proportion', 'share', 'breakdown'])
                        
                        # Check for time-series - force line chart
                        has_time_column = any(
                            'month' in col.lower() or 'date' in col.lower() or 'time' in col.lower() or 'timestamp' in col.lower()
                            for col in result_columns
                        )
                        is_trend = any(keyword in query_lower for keyword in 
                            ['trend', 'over time', 'by month', 'monthly'])
                        
                        # Override based on query type
                        if is_distribution and len(result_columns) >= 2:
                            category_col = result_columns[0]
                            value_col = result_columns[1] if len(result_columns) > 1 else result_columns[0]
                            viz_data["visualization_type"] = "pie"
                            viz_data["x_axis"] = category_col
                            viz_data["y_axis"] = value_col
                            viz_data["explanation"] = "Pie chart for distribution data"
                        elif (has_time_column or is_trend) and len(result_columns) >= 2:
                            date_col = next(
                                (col for col in result_columns if 'month' in col.lower() or 'date' in col.lower() or 'time' in col.lower()),
                                result_columns[0]
                            )
                            value_col = next(
                                (col for col in result_columns if col != date_col),
                                result_columns[1] if len(result_columns) > 1 else result_columns[0]
                            )
                            viz_data["visualization_type"] = "line"
                            viz_data["x_axis"] = date_col
                            viz_data["y_axis"] = value_col
                            viz_data["explanation"] = "Line chart for time series data"
                    
                    return viz_data
            except:
                pass
        except Exception as e:
            print(f"Warning: Visualization recommendation failed: {e}")
        
        # Fallback: simple heuristic with smart detection
        if result_count == 1 and len(columns) <= 2:
            return {
                "visualization_type": "none",
                "x_axis": None,
                "y_axis": None,
                "explanation": "Single value result",
                "tokens": tokens_used
            }
        elif len(columns) >= 2:
            # Check query for keywords
            query_lower = query.lower()
            
            # Check if query asks for distribution
            is_distribution = any(keyword in query_lower for keyword in 
                ['distribution', 'percentage', 'proportion', 'share', 'breakdown'])
            
            # Check if we have a date/time column
            has_date_column = any(
                'month' in col.lower() or 'date' in col.lower() or 'time' in col.lower() or 'timestamp' in col.lower()
                for col in columns
            )
            
            # Check if query asks for trends
            is_trend = any(keyword in query_lower for keyword in 
                ['trend', 'over time', 'by month', 'monthly', 'temporal'])
            
            if is_trend and has_date_column:
                # Time series - use line chart
                date_col = next(
                    (col for col in columns if 'month' in col.lower() or 'date' in col.lower() or 'time' in col.lower()),
                    columns[0]
                )
                value_col = next(
                    (col for col in columns if col != date_col),
                    columns[1] if len(columns) > 1 else columns[0]
                )
                return {
                    "visualization_type": "line",
                    "x_axis": date_col,
                    "y_axis": value_col,
                    "explanation": "Line chart for time series data",
                    "tokens": tokens_used
                }
            elif is_distribution or (len(columns) == 2 and result_count <= 10):
                # Distribution - use pie chart
                category_col = columns[0]
                value_col = columns[1] if len(columns) > 1 else columns[0]
                return {
                    "visualization_type": "pie",
                    "x_axis": category_col,
                    "y_axis": value_col,
                    "explanation": "Pie chart for distribution/percentage data",
                    "tokens": tokens_used
                }
            else:
                # Categorical comparison - use bar chart
                return {
                    "visualization_type": "bar",
                    "x_axis": columns[0],
                    "y_axis": columns[1] if len(columns) > 1 else None,
                    "explanation": "Bar chart for categorical comparison",
                    "tokens": tokens_used
                }
        else:
            return {
                "visualization_type": "table",
                "x_axis": None,
                "y_axis": None,
                "explanation": "Table view for detailed data",
                "tokens": tokens_used
            }
    
    def generate_insights(self, query: str, results: List[Dict]) -> Dict[str, Any]:
        """Generate insights and explanation from query results
        Returns: {"insights": [], "explanation": str, "tokens": int}
        """
        tokens_used = 0
        try:
            # Limit results to reduce token usage (only send first 5-10 rows)
            results_sample = results[:5] if len(results) > 5 else results
            # Convert date/Decimal objects to strings/numbers for JSON serialization
            def convert_for_json(obj):
                if isinstance(obj, dict):
                    return {k: convert_for_json(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_for_json(item) for item in obj]
                elif hasattr(obj, 'isoformat'):  # date/datetime objects
                    return obj.isoformat()
                elif hasattr(obj, '__float__'):  # Decimal objects
                    return float(obj)
                else:
                    return obj
            results_sample_clean = convert_for_json(results_sample) if results_sample else []
            results_str = json.dumps(results_sample_clean, indent=2) if results_sample_clean else "[]"
            result_count = len(results)
            
            # Create a more concise prompt by including summary stats
            summary_stats = ""
            if results and result_count > 0:
                # Calculate basic stats to help LLM
                try:
                    numeric_cols = []
                    for col in results[0].keys():
                        try:
                            sample_val = results[0].get(col)
                            if sample_val and (isinstance(sample_val, (int, float)) or 
                                              (isinstance(sample_val, str) and sample_val.replace('.', '').replace('-', '').isdigit())):
                                numeric_cols.append(col)
                        except:
                            pass
                    
                    if numeric_cols:
                        values = [float(row.get(numeric_cols[0], 0) or 0) for row in results]
                        max_val = max(values)
                        min_val = min(values)
                        total = sum(values)
                        avg_val = total / len(values) if values else 0
                        summary_stats = f"Stats: max={max_val:.0f}, min={min_val:.0f}, total={total:.0f}, avg={avg_val:.0f}"
                except:
                    pass
            
            # Use shorter prompt template
            prompt_text = f"""Analyze this HR query and provide insights.

Query: {query}
Result Count: {result_count}
{summary_stats}
Sample Data (first {len(results_sample)} rows):
{results_str}

Provide ALL sections:

INSIGHTS:
- [Specific insight with numbers from data]
- [Another insight with numbers]
- [Third insight]

EXPLANATION:
[3-4 sentences explaining what data shows, what it means for HR, reference specific numbers]

NOTABLE PATTERNS & TRENDS:
[2-3 sentences on patterns, trends, anomalies with numbers]

ACTIONABLE RECOMMENDATIONS:
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]

Use ACTUAL numbers from the data. Avoid generic statements."""
            
            response = self.llm.invoke(prompt_text)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Count tokens
            tokens_used = token_counter.count_tokens(prompt_text) + token_counter.count_tokens(response_text)
            
            # Parse all sections from response
            insights = []
            explanation = ""
            patterns = ""
            recommendations = ""
            
            # Extract INSIGHTS section
            if "INSIGHTS:" in response_text:
                insights_section = response_text.split("INSIGHTS:")[1]
                # Stop at next section
                for delimiter in ["EXPLANATION:", "NOTABLE PATTERN", "ACTIONABLE RECOMMENDATION"]:
                    if delimiter in insights_section:
                        insights_section = insights_section.split(delimiter)[0]
                        break
                
                # Extract bullet points
                for line in insights_section.split("\n"):
                    line = line.strip()
                    if line.startswith("-") or line.startswith("•"):
                        insight = line.strip("- •").strip()
                        if insight and len(insight) > 10:  # Filter out very short insights
                            insights.append(insight)
            else:
                # If no INSIGHTS: section, try to extract from the whole response
                # Sometimes LLM doesn't follow format exactly
                print("⚠️  No INSIGHTS: section found in LLM response, trying to extract from full response")
                # Look for bullet points in the whole response
                for line in response_text.split("\n"):
                    line = line.strip()
                    if (line.startswith("-") or line.startswith("•")) and len(line) > 20:
                        insight = line.strip("- •").strip()
                        if insight and not insight.startswith("INSIGHTS") and not insight.startswith("EXPLANATION"):
                            insights.append(insight)
                            if len(insights) >= 3:  # Limit to first 3
                                break
            
            # Extract EXPLANATION section
            if "EXPLANATION:" in response_text:
                explanation_section = response_text.split("EXPLANATION:")[1]
                # Stop at next section
                for delimiter in ["NOTABLE PATTERN", "ACTIONABLE RECOMMENDATION"]:
                    if delimiter in explanation_section:
                        explanation = explanation_section.split(delimiter)[0].strip()
                        break
                else:
                    explanation = explanation_section.strip()
            
            # Extract NOTABLE PATTERNS & TRENDS section
            if "NOTABLE PATTERN" in response_text.upper():
                # Try different variations
                pattern_keywords = ["NOTABLE PATTERN", "NOTABLE PATTERNS", "PATTERNS & TRENDS", "PATTERNS AND TRENDS"]
                for keyword in pattern_keywords:
                    if keyword in response_text:
                        patterns_section = response_text.split(keyword)[1]
                        if ":" in patterns_section:
                            patterns_section = patterns_section.split(":")[1]
                        # Stop at next section
                        if "ACTIONABLE RECOMMENDATION" in patterns_section:
                            patterns = patterns_section.split("ACTIONABLE RECOMMENDATION")[0].strip()
                        else:
                            patterns = patterns_section.strip()
                        break
            
            # Extract ACTIONABLE RECOMMENDATIONS section
            if "ACTIONABLE RECOMMENDATION" in response_text.upper():
                rec_keywords = ["ACTIONABLE RECOMMENDATION", "ACTIONABLE RECOMMENDATIONS", "RECOMMENDATIONS"]
                for keyword in rec_keywords:
                    if keyword in response_text:
                        rec_section = response_text.split(keyword)[1]
                        if ":" in rec_section:
                            rec_section = rec_section.split(":")[1]
                        recommendations = rec_section.strip()
                        break
            
            # Validate insights quality - check if they're generic/fallback
            is_generic = False
            generic_phrases = [
                "query executed successfully",
                "query returned",
                "sample data",
                "data retrieved successfully",
                "records found",
                "retrieved",
                "records"
            ]
            
            if not insights:
                is_generic = True
            else:
                # Check if insights are too generic - must have actual numbers or specific findings
                insight_text = " ".join(insights).lower()
                has_numbers = any(char.isdigit() for char in insight_text)
                # More strict: if it contains generic phrases, it's ALWAYS generic (even with numbers)
                contains_generic = any(phrase in insight_text for phrase in generic_phrases)
                is_generic = contains_generic or all(len(i) < 30 for i in insights) or (not has_numbers and len(insights) > 0)
                
                if contains_generic:
                    print(f"⚠️  Detected generic insight: '{insight_text[:100]}' - will regenerate")
            
            # If insights are generic, try to generate real insights from data
            if is_generic and results and result_count > 0:
                print("Warning: LLM generated generic insights. Generating data-driven insights from results...")
                
                # Generate real insights from actual data
                if result_count == 1:
                    # Single value
                    sample_result = results[0]
                    for key, value in sample_result.items():
                        insights = [f"The {key.replace('_', ' ').title()} is {value}"]
                        break
                else:
                    # Multiple values - analyze the data
                    insights = []
                    
                    # Find highest value
                    try:
                        numeric_cols = []
                        for col in results[0].keys():
                            try:
                                # Try to find numeric columns
                                sample_val = results[0].get(col)
                                if sample_val and (isinstance(sample_val, (int, float)) or 
                                                  (isinstance(sample_val, str) and sample_val.replace('.', '').replace('-', '').isdigit())):
                                    numeric_cols.append(col)
                            except:
                                pass
                        
                        if numeric_cols:
                            # Find max value
                            max_val = 0
                            max_row = None
                            for row in results:
                                for col in numeric_cols:
                                    try:
                                        val = float(row.get(col, 0) or 0)
                                        if val > max_val:
                                            max_val = val
                                            max_row = row
                                    except:
                                        pass
                            
                            if max_row:
                                category_col = next((k for k in max_row.keys() if k not in numeric_cols), list(max_row.keys())[0])
                                insights.append(f"{max_row.get(category_col, 'Unknown')} has the highest value of {max_val:,.0f}")
                        
                        # Find lowest value
                        if len(results) > 1:
                            min_val = float('inf')
                            min_row = None
                            for row in results:
                                for col in numeric_cols:
                                    try:
                                        val = float(row.get(col, 0) or 0)
                                        if val < min_val:
                                            min_val = val
                                            min_row = row
                                    except:
                                        pass
                            
                            if min_row and min_val != float('inf'):
                                category_col = next((k for k in min_row.keys() if k not in numeric_cols), list(min_row.keys())[0])
                                insights.append(f"{min_row.get(category_col, 'Unknown')} has the lowest value of {min_val:,.0f}")
                        
                        # For time series, calculate trend; for categorical, show total
                        if numeric_cols:
                            # Check if this is time series data
                            has_time_col = any('month' in col.lower() or 'date' in col.lower() for col in results[0].keys())
                            
                            if has_time_col and len(results) > 1:
                                # Time series - calculate trend
                                first_val = float(results[0].get(numeric_cols[0], 0) or 0)
                                last_val = float(results[-1].get(numeric_cols[0], 0) or 0)
                                change = last_val - first_val
                                change_pct = (change / first_val * 100) if first_val > 0 else 0
                                
                                # Get date columns safely (handle date objects)
                                date_col = next((col for col in results[0].keys() if 'month' in col.lower() or 'date' in col.lower()), None)
                                first_date = str(results[0].get(date_col, 'start')) if date_col else 'start'
                                last_date = str(results[-1].get(date_col, 'end')) if date_col else 'end'
                                
                                if change > 0:
                                    insights.append(f"Trend: Increased by {change:,.0f} ({change_pct:.1f}%) from {first_date} to {last_date}")
                                elif change < 0:
                                    insights.append(f"Trend: Decreased by {abs(change):,.0f} ({abs(change_pct):.1f}%) from {first_date} to {last_date}")
                                else:
                                    insights.append(f"Trend: Stable at {first_val:,.0f} across the period")
                                
                                # Add average
                                avg_val = sum(float(row.get(numeric_cols[0], 0) or 0) for row in results) / len(results)
                                insights.append(f"Average value: {avg_val:,.0f}")
                                
                                # Add peak and low points
                                max_row = max(results, key=lambda r: float(r.get(numeric_cols[0], 0) or 0))
                                min_row = min(results, key=lambda r: float(r.get(numeric_cols[0], 0) or 0))
                                max_val = float(max_row.get(numeric_cols[0], 0) or 0)
                                min_val = float(min_row.get(numeric_cols[0], 0) or 0)
                                max_date = str(max_row.get(date_col, '')) if date_col else ''
                                min_date = str(min_row.get(date_col, '')) if date_col else ''
                                insights.append(f"Peak: {max_val:,.0f} in {max_date}" if max_date else f"Peak: {max_val:,.0f}")
                                insights.append(f"Low: {min_val:,.0f} in {min_date}" if min_date else f"Low: {min_val:,.0f}")
                            else:
                                # Categorical - show total
                                total = sum(float(row.get(numeric_cols[0], 0) or 0) for row in results)
                                insights.append(f"Total across all categories: {total:,.0f}")
                    except Exception as e:
                        print(f"Error generating insights from data: {e}")
                        import traceback
                        traceback.print_exc()
                        # Fallback to simple insights - ensure we always have something
                        if not insights:  # Only if no insights were generated
                            try:
                                sample_result = results[0]
                                # Convert any Decimal/date objects to strings
                                key_values = []
                                for k, v in list(sample_result.items())[:2]:
                                    if hasattr(v, 'isoformat'):
                                        key_values.append(f"{k}: {v.isoformat()}")
                                    elif hasattr(v, '__float__'):
                                        key_values.append(f"{k}: {float(v)}")
                                    else:
                                        key_values.append(f"{k}: {v}")
                                insights = [f"Query returned {result_count} records", f"Data shows: {', '.join(key_values)}"]
                            except:
                                insights = [f"Query analyzed {result_count} records"]
            
            # Validate explanation quality - must be meaningful
            if not explanation or len(explanation) < 100 or "query executed successfully" in explanation.lower():
                # Generate better explanation from actual data
                if results and result_count > 0:
                    # Analyze the data to create meaningful explanation
                    try:
                        if result_count == 1:
                            # Single value
                            key, value = list(results[0].items())[0]
                            explanation = f"This query analyzed employee data and found that {key.replace('_', ' ').title()} is {value}. "
                            explanation += "This represents the current state of this metric in the HR system."
                        else:
                            # Multiple values - analyze distribution
                            numeric_cols = []
                            category_cols = []
                            for col in results[0].keys():
                                try:
                                    sample_val = results[0].get(col)
                                    if sample_val and (isinstance(sample_val, (int, float)) or 
                                                      (isinstance(sample_val, str) and sample_val.replace('.', '').replace('-', '').isdigit())):
                                        numeric_cols.append(col)
                                    else:
                                        category_cols.append(col)
                                except:
                                    category_cols.append(col)
                            
                            if numeric_cols and category_cols:
                                # Find top category
                                top_row = max(results, key=lambda r: float(r.get(numeric_cols[0], 0) or 0))
                                top_val = float(top_row.get(numeric_cols[0], 0) or 0)
                                top_cat = top_row.get(category_cols[0], "Unknown")
                                
                                total = sum(float(r.get(numeric_cols[0], 0) or 0) for r in results)
                                
                                explanation = f"This query analyzed {result_count} records showing {category_cols[0].replace('_', ' ').title()} distribution. "
                                explanation += f"{top_cat} has the highest value of {top_val:,.0f}, representing {top_val/total*100:.1f}% of the total ({total:,.0f}). "
                                explanation += "The visualization shows the distribution across all categories."
                            elif numeric_cols:
                                # Time series or numeric data
                                values = [float(r.get(numeric_cols[0], 0) or 0) for r in results]
                                max_val = max(values)
                                min_val = min(values)
                                explanation = f"This query analyzed {result_count} data points over time. "
                                explanation += f"Values range from {min_val:,.0f} to {max_val:,.0f}. "
                                explanation += "The trend shows how this metric has changed over the period."
                            else:
                                explanation = f"This query analyzed {result_count} records. "
                                explanation += "The data shows the distribution across different categories. Review the visualization to see patterns."
                    except Exception as e:
                        print(f"Error generating explanation: {e}")
                        explanation = f"This query analyzed {result_count} records. The data shows {result_count} distinct categories or data points. Review the visualization to see the distribution and patterns."
                else:
                    explanation = f"Query executed successfully but returned no results."
            
            # Generate fallback patterns if missing
            if not patterns and results and result_count > 1:
                # Try to identify patterns from data
                if any('month' in str(col).lower() or 'date' in str(col).lower() 
                       for row in results[:3] for col in row.keys()):
                    patterns = f"The data shows trends over time with {result_count} data points. Analyze the chart to identify specific patterns."
                elif result_count <= 10:
                    # Small dataset - mention distribution
                    patterns = f"Data shows {result_count} distinct categories. Review the visualization to identify distribution patterns."
                else:
                    patterns = f"Dataset contains {result_count} records. Review the visualization to identify key patterns and trends."
            
            # Generate fallback recommendations if missing
            if not recommendations and results and result_count > 0:
                # Generic but helpful recommendations
                if any('headcount' in str(col).lower() or 'count' in str(col).lower() 
                       for row in results[:3] for col in row.keys()):
                    recommendations = "- Monitor headcount trends regularly\n- Review department staffing levels\n- Consider workforce planning based on trends"
                elif any('salary' in str(col).lower() or 'compensation' in str(col).lower() 
                         for row in results[:3] for col in row.keys()):
                    recommendations = "- Review compensation equity across departments\n- Consider market benchmarking\n- Analyze salary trends for retention"
                elif any('performance' in str(col).lower() or 'rating' in str(col).lower() 
                         for row in results[:3] for col in row.keys()):
                    recommendations = "- Identify high performers for recognition\n- Develop improvement plans for low performers\n- Review performance distribution"
                else:
                    recommendations = "- Review the data regularly\n- Use insights for strategic HR decisions\n- Monitor trends over time"
            
            # Final safety check - ensure we always have insights
            if not insights or len(insights) == 0:
                print("⚠️  No insights generated, creating fallback insights from data...")
                if results and result_count > 0:
                    try:
                        # Find numeric and date columns
                        numeric_cols = []
                        date_cols = []
                        for col in results[0].keys():
                            val = results[0].get(col)
                            # Check if numeric (handle Decimal, int, float, or numeric string)
                            try:
                                float(str(val).replace(',', ''))
                                if 'month' not in col.lower() and 'date' not in col.lower():
                                    numeric_cols.append(col)
                            except:
                                pass
                            # Check if date column
                            if 'month' in col.lower() or 'date' in col.lower() or hasattr(val, 'isoformat'):
                                date_cols.append(col)
                        
                        if numeric_cols and date_cols and len(results) > 1:
                            # Time series data
                            values = []
                            for r in results:
                                try:
                                    val = float(str(r.get(numeric_cols[0], 0) or 0).replace(',', ''))
                                    values.append(val)
                                except:
                                    pass
                            
                            if values:
                                first_val = values[0]
                                last_val = values[-1]
                                change = last_val - first_val
                                change_pct = (change / first_val * 100) if first_val > 0 else 0
                                
                                # Get dates safely
                                first_date_val = results[0].get(date_cols[0], '') if date_cols else ''
                                last_date_val = results[-1].get(date_cols[0], '') if date_cols else ''
                                first_date = str(first_date_val)[:10] if first_date_val else 'start'
                                last_date = str(last_date_val)[:10] if last_date_val else 'end'
                                
                                insights = [
                                    f"Trend: {'Increased' if change > 0 else 'Decreased' if change < 0 else 'Stable'} by {abs(change):,.0f} ({abs(change_pct):.1f}%) from {first_date} to {last_date}",
                                    f"Range: {min(values):,.0f} to {max(values):,.0f}",
                                    f"Average: {sum(values)/len(values):,.0f}"
                                ]
                            else:
                                insights = [f"Query analyzed {result_count} records"]
                        elif numeric_cols:
                            # Just numeric data
                            values = []
                            for r in results:
                                try:
                                    val = float(str(r.get(numeric_cols[0], 0) or 0).replace(',', ''))
                                    values.append(val)
                                except:
                                    pass
                            if values:
                                insights = [
                                    f"Analyzed {result_count} data points",
                                    f"Range: {min(values):,.0f} to {max(values):,.0f}",
                                    f"Average: {sum(values)/len(values):,.0f}"
                                ]
                            else:
                                insights = [f"Query analyzed {result_count} records"]
                        else:
                            insights = [f"Query analyzed {result_count} records"]
                    except Exception as e:
                        print(f"Error in final fallback: {e}")
                        insights = [f"Query analyzed {result_count} records"]
                else:
                    insights = ["No data returned"]
            
            # Combine all sections into explanation for frontend parsing
            full_explanation = explanation
            if patterns:
                full_explanation += f"\n\nNOTABLE PATTERNS & TRENDS:\n{patterns}"
            if recommendations:
                full_explanation += f"\n\nACTIONABLE RECOMMENDATIONS:\n{recommendations}"
            
            return {
                "insights": insights,
                "explanation": full_explanation,
                "tokens": tokens_used
            }
        except Exception as e:
            print(f"Warning: Insights generation failed: {e}")
            # Fallback insights
            result_count = len(results) if results else 0
            return {
                "insights": [f"Query executed successfully. Retrieved {result_count} records."],
                "explanation": f"Analysis complete. The query returned {result_count} records.",
                "tokens": tokens_used
            }
    
    def process_query(
        self,
        question: str,
        conversation_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """Process a natural language query and return complete analysis"""
        
        total_tokens = 0  # Track total LLM tokens used
        cache_hit = False
        rag_context_used = False
        
        # Step 0: Check semantic cache first
        if self.semantic_cache:
            cached_response = self.semantic_cache.get_cached_response(question)
            if cached_response:
                logger.info(f"Cache HIT for query: {question[:50]}...")
                cache_hit = True
                return {
                    "success": True,
                    "sql_query": cached_response.get("sql_query"),
                    "results": cached_response.get("results", []),
                    "tables": cached_response.get("tables", []),
                    "columns": cached_response.get("columns", {}),
                    "visualization": cached_response.get("visualization"),
                    "insights": cached_response.get("insights", []),
                    "explanation": cached_response.get("explanation", ""),
                    "tokens": 0,  # No tokens used for cached response
                    "cache_hit": True,
                    "cache_similarity": cached_response.get("cache_similarity", 0.0)
                }
        
        # Step 0.5: Retrieve RAG context if available
        rag_context = ""
        if self.rag_retriever:
            try:
                rag_results = self.rag_retriever.retrieve_relevant_context(question, top_k=3)
                if rag_results:
                    rag_context = self.rag_retriever.format_rag_context_for_prompt(rag_results)
                    rag_context_used = True
                    logger.info(f"Retrieved {len(rag_results)} RAG contexts for query")
            except Exception as e:
                logger.warning(f"RAG retrieval failed: {e}")
        
        try:
            # Step 1: Generate SQL (with RAG context if available)
            sql_result = self.generate_sql(question, conversation_history, rag_context=rag_context)
            sql_query = sql_result["sql"]
            total_tokens += sql_result.get("tokens", 0)
        except Exception as e:
            return {
                "success": False,
                "error": f"SQL generation error: {str(e)}",
                "sql_query": None,
                "tokens": total_tokens
            }
        
        # Step 2: Validate SQL
        is_valid = validate_sql_query(sql_query)
        if not is_valid:
            # Try to fix SQL (simple retry with better prompt)
            try:
                sql_result = self.generate_sql(
                    f"{question}. Make sure the SQL is valid PostgreSQL syntax.",
                    conversation_history
                )
                sql_query = sql_result["sql"]
                total_tokens += sql_result.get("tokens", 0)
                is_valid = validate_sql_query(sql_query)
            except:
                pass
        
        if not is_valid:
            return {
                "success": False,
                "error": "Could not generate valid SQL query",
                "sql_query": sql_query,
                "tokens": total_tokens
            }
        
        # Step 3: Execute SQL
        try:
            results = execute_sql_query(sql_query)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "sql_query": sql_query,
                "tokens": total_tokens
            }
        
        # Step 4: Identify tables and columns
        try:
            table_column_info = self.identify_tables_columns(question, sql_query)
            total_tokens += table_column_info.get("tokens", 0)
            # Remove tokens from return value
            table_column_info.pop("tokens", None)
        except Exception as e:
            print(f"Warning: Table/column identification failed: {e}")
            table_column_info = {"tables": [], "columns": {}}
        
        # Step 5: Get column names from results
        if not results:
            return {
                "success": True,
                "sql_query": sql_query,
                "results": [],
                "tables": table_column_info.get("tables", []),
                "columns": table_column_info.get("columns", {}),
                "visualization": {
                    "visualization_type": "none",
                    "x_axis": None,
                    "y_axis": None,
                    "explanation": "No data returned from query"
                },
                "insights": ["Query executed successfully but returned no results"],
                "explanation": "The query executed successfully but did not return any data. Please refine your question.",
                "tokens": total_tokens
            }
        
        result_columns = list(results[0].keys()) if results else []
        
        # Step 6: Recommend visualization
        # Skip LLM call for distribution/trend queries - use heuristics directly (saves tokens and time)
        try:
            query_lower = question.lower()
            is_distribution_query = any(keyword in query_lower for keyword in 
                ['distribution', 'percentage', 'proportion', 'share', 'breakdown'])
            is_trend_query = any(keyword in query_lower for keyword in 
                ['trend', 'over time', 'by month', 'monthly'])
            has_time_column = any(
                'month' in col.lower() or 'date' in col.lower() or 'time' in col.lower()
                for col in result_columns
            ) if result_columns else False
            
            # Direct assignment for common cases (saves tokens and time)
            # IMPORTANT: "department wise headcount" is a comparison, not distribution - use bar chart
            if is_distribution_query and result_columns and len(result_columns) >= 2 and 'headcount' not in query_lower:
                viz_recommendation = {
                    "visualization_type": "pie",
                    "x_axis": result_columns[0],
                    "y_axis": result_columns[1] if len(result_columns) > 1 else result_columns[0],
                    "explanation": "Pie chart for distribution data"
                }
                print("✓ Using pie chart (distribution query detected - skipped LLM)")
            elif 'headcount' in query_lower and ('department' in query_lower or 'by' in query_lower) and result_columns and len(result_columns) >= 2:
                # "department wise headcount" or "headcount by department" = bar chart (comparison)
                viz_recommendation = {
                    "visualization_type": "bar",
                    "x_axis": result_columns[0],
                    "y_axis": result_columns[1] if len(result_columns) > 1 else result_columns[0],
                    "explanation": "Bar chart for categorical comparison"
                }
                print("✓ Using bar chart (headcount comparison detected - skipped LLM)")
            elif (is_trend_query or has_time_column or 'MonthEnd' in sql_query) and result_columns and len(result_columns) >= 2:
                date_col = next(
                    (col for col in result_columns if 'month' in col.lower() or 'date' in col.lower() or 'time' in col.lower()),
                    result_columns[0]
                )
                value_col = next(
                    (col for col in result_columns if col != date_col),
                    result_columns[1] if len(result_columns) > 1 else result_columns[0]
                )
                viz_recommendation = {
                    "visualization_type": "line",
                    "x_axis": date_col,
                    "y_axis": value_col,
                    "explanation": "Line chart for time series data"
                }
                print("✓ Using line chart (trend query detected - skipped LLM)")
            else:
                # Use LLM for other cases
                try:
                    viz_recommendation = self.recommend_visualization(sql_query, results, result_columns)
                    total_tokens += viz_recommendation.get("tokens", 0)
                    viz_recommendation.pop("tokens", None)
                    
                    # Override if needed
                    if is_distribution_query and result_columns and len(result_columns) >= 2:
                        viz_recommendation["visualization_type"] = "pie"
                        viz_recommendation["x_axis"] = result_columns[0]
                        viz_recommendation["y_axis"] = result_columns[1] if len(result_columns) > 1 else result_columns[0]
                except Exception as e:
                    print(f"Warning: Visualization recommendation failed: {e}")
                    # Fallback
                    if result_columns and len(result_columns) >= 2:
                        viz_recommendation = {
                            "visualization_type": "bar",
                            "x_axis": result_columns[0],
                            "y_axis": result_columns[1],
                            "explanation": "Bar chart for categorical comparison"
                        }
                    else:
                        viz_recommendation = {
                            "visualization_type": "table",
                            "x_axis": None,
                            "y_axis": None,
                            "explanation": "Table view"
                        }
        except Exception as e:
            print(f"Warning: Visualization recommendation failed: {e}")
            # Fallback with time detection
            has_time = 'MonthEnd' in sql_query or any('month' in col.lower() for col in result_columns) if result_columns else False
            viz_recommendation = {
                "visualization_type": "line" if (has_time and len(result_columns) >= 2) else ("table" if results else "none"),
                "x_axis": result_columns[0] if result_columns and has_time else None,
                "y_axis": result_columns[1] if len(result_columns) > 1 and has_time else None,
                "explanation": "Line chart for time series" if has_time else "Visualization recommendation unavailable"
            }
        
        # Step 7: Generate insights
        try:
            insights_data = self.generate_insights(sql_query, results)
            total_tokens += insights_data.get("tokens", 0)
            insights_data.pop("tokens", None)
        except Exception as e:
            print(f"Warning: Insights generation failed: {e}")
            insights_data = {
                "insights": ["Data retrieved successfully"],
                "explanation": f"Query executed successfully. Retrieved {len(results)} records."
            }
        
        # Build response
        response = {
            "success": True,
            "sql_query": sql_query,
            "results": results,
            "tables": table_column_info.get("tables", []),
            "columns": table_column_info.get("columns", {}),
            "visualization": viz_recommendation,
            "insights": insights_data.get("insights", []),
            "explanation": insights_data.get("explanation", ""),
            "tokens": total_tokens,
            "cache_hit": cache_hit,
            "rag_used": rag_context_used
        }
        
        # Step 8: Cache the response for future similar queries
        if self.semantic_cache and not cache_hit:
            try:
                self.semantic_cache.cache_response(question, response)
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")
        
        return response


# Global agent instance
hr_agent = HRAgent()

