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
        except Exception as e:
            raise Exception(f"Failed to initialize LLM: {str(e)}. Make sure Ollama is running at {settings.OLLAMA_BASE_URL}")
    
    def generate_sql(self, question: str, conversation_history: List[Dict] = None) -> str:
        """Generate SQL query from natural language question"""
        try:
            # Format conversation history
            history_text = ""
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    history_text += f"{role}: {content}\n"
            
            prompt = ChatPromptTemplate.from_template(SQL_GENERATION_PROMPT)
            chain = prompt | self.llm | self.output_parser
            
            response = chain.invoke({
                "question": question,
                "conversation_history": history_text
            })
            
            # Extract SQL query (remove markdown code blocks if present)
            sql_query = response.strip()
            sql_query = re.sub(r'```sql\n?', '', sql_query)
            sql_query = re.sub(r'```\n?', '', sql_query)
            sql_query = sql_query.strip()
            
            if not sql_query:
                raise Exception("LLM returned empty SQL query")
            
            return sql_query
        except Exception as e:
            raise Exception(f"SQL generation failed: {str(e)}")
    
    def identify_tables_columns(self, question: str, sql_query: str) -> Dict[str, Any]:
        """Identify tables and columns used in the query"""
        prompt = ChatPromptTemplate.from_template(TABLE_COLUMN_IDENTIFICATION_PROMPT)
        chain = prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "question": question,
            "sql_query": sql_query
        })
        
        # Try to parse JSON response
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback: parse from SQL query directly
        tables = []
        columns = {}
        cols = []
        
        # Extract table names
        table_pattern = r'employees\.(\w+)'
        tables_found = re.findall(table_pattern, sql_query, re.IGNORECASE)
        tables = list(set(tables_found))
        
        # Extract column names from SELECT clause
        select_pattern = r'SELECT\s+(.*?)\s+FROM'
        select_match = re.search(select_pattern, sql_query, re.IGNORECASE | re.DOTALL)
        if select_match:
            select_clause = select_match.group(1)
            # Extract column names (handle aliases, functions, etc.)
            col_pattern = r'["\']?(\w+)["\']?'
            cols = re.findall(col_pattern, select_clause)
            # Filter out SQL keywords
            sql_keywords = {'as', 'count', 'sum', 'avg', 'max', 'min', 'distinct', 'select'}
            cols = [c for c in cols if c.lower() not in sql_keywords and len(c) > 1]
        
        # Extract column names (basic extraction)
        for table in tables:
            columns[f"employees.{table}"] = cols if cols else []
        
        return {
            "tables": [f"employees.{t}" for t in tables],
            "columns": columns
        }
    
    def recommend_visualization(self, query: str, results: List[Dict], columns: List[str]) -> Dict[str, Any]:
        """Recommend visualization type based on query results"""
        if not results:
            return {
                "visualization_type": "none",
                "x_axis": None,
                "y_axis": None,
                "explanation": "No data to visualize"
            }
        
        result_count = len(results)
        sample_data = json.dumps(results[:3], indent=2) if results else "[]"
        
        prompt = ChatPromptTemplate.from_template(VISUALIZATION_RECOMMENDATION_PROMPT)
        chain = prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "query": query,
            "result_count": result_count,
            "columns": ", ".join(columns),
            "sample_data": sample_data
        })
        
        # Try to parse JSON
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback: simple heuristic
        if result_count == 1 and len(columns) <= 2:
            return {
                "visualization_type": "none",
                "x_axis": None,
                "y_axis": None,
                "explanation": "Single value result"
            }
        elif len(columns) >= 2:
            return {
                "visualization_type": "bar",
                "x_axis": columns[0],
                "y_axis": columns[1] if len(columns) > 1 else None,
                "explanation": "Bar chart for categorical comparison"
            }
        else:
            return {
                "visualization_type": "table",
                "x_axis": None,
                "y_axis": None,
                "explanation": "Table view for detailed data"
            }
    
    def generate_insights(self, query: str, results: List[Dict]) -> Dict[str, str]:
        """Generate insights and explanation from query results"""
        results_str = json.dumps(results[:10], indent=2) if results else "[]"
        
        prompt = ChatPromptTemplate.from_template(INSIGHTS_GENERATION_PROMPT)
        chain = prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "query": query,
            "results": results_str
        })
        
        # Parse insights and explanation
        insights = []
        explanation = ""
        
        if "INSIGHTS:" in response:
            insights_section = response.split("INSIGHTS:")[1].split("EXPLANATION:")[0]
            insights = [line.strip("- ").strip() for line in insights_section.split("\n") if line.strip().startswith("-")]
        
        if "EXPLANATION:" in response:
            explanation = response.split("EXPLANATION:")[1].strip()
        else:
            explanation = response
        
        return {
            "insights": insights if insights else ["Data retrieved successfully"],
            "explanation": explanation if explanation else "Analysis complete"
        }
    
    def process_query(
        self,
        question: str,
        conversation_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """Process a natural language query and return complete analysis"""
        
        try:
            # Step 1: Generate SQL
            sql_query = self.generate_sql(question, conversation_history)
        except Exception as e:
            return {
                "success": False,
                "error": f"SQL generation error: {str(e)}",
                "sql_query": None
            }
        
        # Step 2: Validate SQL
        is_valid = validate_sql_query(sql_query)
        if not is_valid:
            # Try to fix SQL (simple retry with better prompt)
            sql_query = self.generate_sql(
                f"{question}. Make sure the SQL is valid PostgreSQL syntax.",
                conversation_history
            )
            is_valid = validate_sql_query(sql_query)
        
        if not is_valid:
            return {
                "success": False,
                "error": "Could not generate valid SQL query",
                "sql_query": sql_query
            }
        
        # Step 3: Execute SQL
        try:
            results = execute_sql_query(sql_query)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "sql_query": sql_query
            }
        
        # Step 4: Identify tables and columns
        try:
            table_column_info = self.identify_tables_columns(question, sql_query)
        except Exception as e:
            # Fallback if identification fails
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
                "explanation": "The query executed successfully but did not return any data. Please refine your question."
            }
        
        result_columns = list(results[0].keys()) if results else []
        
        # Step 6: Recommend visualization
        try:
            viz_recommendation = self.recommend_visualization(sql_query, results, result_columns)
        except Exception as e:
            # Fallback visualization
            viz_recommendation = {
                "visualization_type": "table" if results else "none",
                "x_axis": None,
                "y_axis": None,
                "explanation": "Visualization recommendation unavailable"
            }
        
        # Step 7: Generate insights
        try:
            insights_data = self.generate_insights(sql_query, results)
        except Exception as e:
            # Fallback insights
            insights_data = {
                "insights": ["Data retrieved successfully"],
                "explanation": f"Query executed successfully. Retrieved {len(results)} records."
            }
        
        return {
            "success": True,
            "sql_query": sql_query,
            "results": results,
            "tables": table_column_info.get("tables", []),
            "columns": table_column_info.get("columns", {}),
            "visualization": viz_recommendation,
            "insights": insights_data.get("insights", []),
            "explanation": insights_data.get("explanation", "")
        }


# Global agent instance
hr_agent = HRAgent()

