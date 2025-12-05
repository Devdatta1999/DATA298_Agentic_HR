"""Pattern matching system for query patterns"""
import json
import os
import re
from typing import Dict, List, Any, Optional, Tuple
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.config import settings
from qdrant_client.models import PointStruct
import logging

logger = logging.getLogger(__name__)

class PatternMatcher:
    """Matches queries to patterns and generates SQL from templates"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.patterns_file = os.path.join(
            os.path.dirname(__file__),
            "query_patterns.json"
        )
        self.patterns_data = None
        self._load_patterns()
        self._initialize_pattern_collection()
    
    def _load_patterns(self):
        """Load patterns from JSON file"""
        try:
            with open(self.patterns_file, 'r') as f:
                self.patterns_data = json.load(f)
            logger.info(f"Loaded {len(self.patterns_data.get('patterns', []))} patterns")
        except FileNotFoundError:
            logger.error(f"Patterns file not found: {self.patterns_file}")
            self.patterns_data = {"patterns": []}
        except Exception as e:
            logger.error(f"Error loading patterns: {e}")
            self.patterns_data = {"patterns": []}
    
    def _initialize_pattern_collection(self):
        """Initialize pattern collection in Qdrant"""
        try:
            vector_size = self.embedding_service.get_embedding_dimension()
            self.vector_store.create_collection_if_not_exists(
                collection_name="query_patterns",
                vector_size=vector_size
            )
            
            # Check if collection is empty, if so, load patterns
            collection_info = self.vector_store.get_collection_info("query_patterns")
            points_count = collection_info.get("points_count", 0) if collection_info else 0
            
            if points_count == 0:
                logger.info("Pattern collection is empty, loading patterns...")
                self._index_patterns()
            else:
                logger.info(f"Pattern collection already has {points_count} points")
        except Exception as e:
            logger.error(f"Error initializing pattern collection: {e}")
    
    def _index_patterns(self):
        """Index patterns in Qdrant"""
        if not self.patterns_data or not self.patterns_data.get('patterns'):
            logger.warning("No patterns to index")
            return
        
        points = []
        for idx, pattern in enumerate(self.patterns_data['patterns']):
            # Create searchable text from pattern
            searchable_text = f"{pattern['pattern_type']} {' '.join(pattern.get('keywords', []))} {' '.join(pattern.get('example_questions', [])[:2])}"
            
            # Generate embedding
            embedding = self.embedding_service.embed_text(searchable_text)
            
            # Create point
            point = PointStruct(
                id=idx,
                vector=embedding,
                payload={
                    "pattern_type": pattern["pattern_type"],
                    "keywords": pattern.get("keywords", []),
                    "tables": pattern.get("tables", []),
                    "visualization": pattern.get("visualization", "bar"),
                    "sql_template": pattern.get("sql_template", ""),
                    "example_sql": pattern.get("example_sql", ""),
                    "parameter_extraction": pattern.get("parameter_extraction", {}),
                    "example_questions": pattern.get("example_questions", []),
                    "searchable_text": searchable_text
                }
            )
            points.append(point)
        
        # Upsert all points
        if points:
            self.vector_store.upsert_points(
                collection_name="query_patterns",
                points=points
            )
            logger.info(f"Indexed {len(points)} patterns in Qdrant")
    
    def extract_parameters(self, question: str, pattern: Dict) -> Dict[str, Any]:
        """Extract parameters from question based on pattern rules"""
        params = {}
        question_lower = question.lower()
        
        # Extract N from "top N", "bottom N", etc.
        top_match = re.search(r'top\s+(\d+)', question_lower)
        bottom_match = re.search(r'bottom\s+(\d+)', question_lower)
        if top_match:
            params['n'] = int(top_match.group(1))
            params['order'] = 'DESC'
        elif bottom_match:
            params['n'] = int(bottom_match.group(1))
            params['order'] = 'ASC'
        else:
            # Default for top_n patterns
            if 'top_n' in pattern.get('pattern_type', ''):
                params['n'] = 10  # Default
                params['order'] = 'DESC'
        
        # Extract field being ranked
        if 'salary' in question_lower:
            params['field'] = 'Salary'
        elif 'performance' in question_lower or 'rating' in question_lower:
            params['field'] = 'PerformanceRating'
        elif 'engagement' in question_lower or 'satisfaction' in question_lower:
            params['field'] = 'OverallSatisfaction'
        elif 'headcount' in question_lower:
            params['field'] = 'headcount'
        
        # Extract limit for SQL
        if 'n' in params:
            params['limit'] = params['n']
        
        # Extract order field
        if 'field' in params:
            params['order_field'] = params['field']
        
        return params
    
    def generate_sql_from_template(self, template: str, params: Dict) -> str:
        """Generate SQL from template by replacing parameters"""
        sql = template
        
        # Replace {limit} with actual limit
        if 'limit' in params:
            sql = re.sub(r'\{limit\}', str(params['limit']), sql, flags=re.IGNORECASE)
        elif 'n' in params:
            sql = re.sub(r'\{limit\}', str(params['n']), sql, flags=re.IGNORECASE)
        
        # Replace {n} with actual n
        if 'n' in params:
            sql = re.sub(r'\{n\}', str(params['n']), sql)
        
        # Replace {order} with DESC or ASC
        if 'order' in params:
            sql = re.sub(r'\{order\}', params['order'], sql, flags=re.IGNORECASE)
        
        # Replace {order_field} with actual field
        if 'order_field' in params:
            sql = re.sub(r'\{order_field\}', params['order_field'], sql)
        
        return sql
    
    def match_pattern(self, question: str, similarity_threshold: float = 0.70) -> Optional[Dict[str, Any]]:
        """Match question to a pattern"""
        try:
            # Generate embedding for question
            question_embedding = self.embedding_service.embed_text(question)
            
            # Search for similar patterns
            results = self.vector_store.search_similar(
                collection_name="query_patterns",
                query_vector=question_embedding,
                limit=3,
                score_threshold=similarity_threshold
            )
            
            if results and len(results) > 0:
                # Get best match
                best_match = results[0]
                if best_match["score"] >= similarity_threshold:
                    pattern = best_match["payload"]
                    
                    # Extract parameters
                    params = self.extract_parameters(question, pattern)
                    
                    # Generate SQL from template
                    sql_template = pattern.get("sql_template", "")
                    if sql_template:
                        sql = self.generate_sql_from_template(sql_template, params)
                    else:
                        # Fallback to example SQL
                        sql = pattern.get("example_sql", "")
                    
                    return {
                        "matched": True,
                        "pattern_type": pattern.get("pattern_type"),
                        "similarity": best_match["score"],
                        "sql": sql,
                        "tables": pattern.get("tables", []),
                        "visualization": {
                            "visualization_type": pattern.get("visualization", "bar"),
                            "x_axis": None,
                            "y_axis": None,
                            "explanation": f"Pattern-matched: {pattern.get('pattern_type')}"
                        },
                        "parameters": params
                    }
            
            return None
        except Exception as e:
            logger.error(f"Error matching pattern: {e}")
            return None
    
    def get_pattern_info(self, pattern_type: str) -> Optional[Dict]:
        """Get pattern information by type"""
        if not self.patterns_data:
            return None
        
        for pattern in self.patterns_data.get('patterns', []):
            if pattern.get('pattern_type') == pattern_type:
                return pattern
        return None

