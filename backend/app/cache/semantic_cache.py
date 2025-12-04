"""Semantic cache for storing and retrieving query responses"""
import json
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.config import settings
from qdrant_client.models import PointStruct
import logging

logger = logging.getLogger(__name__)

class SemanticCache:
    """Semantic cache using Qdrant for similarity-based caching"""
    
    def __init__(self):
        if not settings.CACHE_ENABLED:
            logger.info("Semantic cache is disabled")
            return
        
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self._initialize_cache_collection()
    
    def _initialize_cache_collection(self):
        """Initialize cache collection in Qdrant"""
        if not settings.CACHE_ENABLED:
            return
        
        try:
            vector_size = self.embedding_service.get_embedding_dimension()
            self.vector_store.create_collection_if_not_exists(
                collection_name=settings.CACHE_COLLECTION_NAME,
                vector_size=vector_size
            )
            logger.info("Semantic cache collection initialized")
        except Exception as e:
            logger.error(f"Error initializing cache collection: {e}")
            raise
    
    def _normalize_query(self, query: str) -> str:
        """Normalize query for better semantic matching"""
        import re
        
        # Convert to lowercase
        normalized = query.lower().strip()
        
        # Remove punctuation (except spaces)
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        
        # Normalize whitespace (multiple spaces to single space)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        # Common typo corrections
        normalized = normalized.replace("departentwise", "departmentwise")
        normalized = normalized.replace("headcout", "headcount")
        normalized = normalized.replace("head count", "headcount")
        normalized = normalized.replace("dept", "department")
        
        # Handle synonyms (normalize to common form)
        synonym_map = {
            "show": "show",
            "display": "show",
            "get": "show",
            "list": "show",
            "what is": "what is",
            "what are": "what is",
            "calculate": "calculate",
            "compute": "calculate",
            "find": "show",
            "give me": "show"
        }
        
        # Simple synonym replacement (word-level, not perfect but helps)
        words = normalized.split()
        normalized_words = [synonym_map.get(word, word) for word in words]
        normalized = ' '.join(normalized_words)
        
        return normalized.strip()
    
    def _generate_cache_id(self, query: str) -> str:
        """Generate a unique ID for cache entry using normalized query"""
        # Use normalized query to avoid duplicates from slight variations
        normalized = self._normalize_query(query)
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get_cached_response(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached response if similar query exists"""
        if not settings.CACHE_ENABLED:
            return None
        
        try:
            # Normalize query for better matching
            normalized_query = self._normalize_query(query)
            
            # First, try exact match by cache ID (fastest)
            cache_id = self._generate_cache_id(query)
            try:
                # Try to get exact match by ID
                exact_match = self.vector_store.client.retrieve(
                    collection_name=settings.CACHE_COLLECTION_NAME,
                    ids=[int(cache_id[:8], 16)]
                )
                if exact_match and len(exact_match) > 0:
                    logger.info(f"Cache HIT! Exact match (ID: {cache_id[:8]})")
                    cached_data = exact_match[0].payload
                    return {
                        "sql_query": cached_data.get("sql_query"),
                        "tables": cached_data.get("tables", []),
                        "columns": cached_data.get("columns", {}),
                        "visualization": cached_data.get("visualization"),
                        "results": cached_data.get("results"),
                        "insights": cached_data.get("insights"),
                        "explanation": cached_data.get("explanation"),
                        "cache_similarity": 1.0,  # Exact match
                        "cached_query": cached_data.get("original_query")
                    }
            except Exception as e:
                # Exact match not found, continue to semantic search
                logger.debug(f"Exact match not found, trying semantic search: {e}")
            
            # Generate embedding for the normalized query
            query_embedding = self.embedding_service.embed_text(normalized_query)
            
            # Search for similar cached queries (check top 3 matches)
            results = self.vector_store.search_similar(
                collection_name=settings.CACHE_COLLECTION_NAME,
                query_vector=query_embedding,
                limit=3,  # Increased from 1 to 3 for better matching
                score_threshold=settings.CACHE_SIMILARITY_THRESHOLD
            )
            
            if results and len(results) > 0:
                # Find the best match above threshold
                for match in results:
                    if match["score"] >= settings.CACHE_SIMILARITY_THRESHOLD:
                        logger.info(f"Cache HIT! Similarity: {match['score']:.3f}")
                        cached_data = match["payload"]
                        return {
                            "sql_query": cached_data.get("sql_query"),
                            "tables": cached_data.get("tables", []),
                            "columns": cached_data.get("columns", {}),
                            "visualization": cached_data.get("visualization"),
                            "results": cached_data.get("results"),
                            "insights": cached_data.get("insights"),
                        "explanation": cached_data.get("explanation"),
                            "cache_similarity": match["score"],
                            "cached_query": cached_data.get("original_query")
                        }
            
            logger.info("Cache MISS - no similar query found")
            return None
        except Exception as e:
            logger.error(f"Error retrieving from cache: {e}")
            return None
    
    def cache_response(
        self,
        query: str,
        response: Dict[str, Any]
    ):
        """Cache a query and its response"""
        if not settings.CACHE_ENABLED:
            return
        
        try:
            # Normalize query before caching
            normalized_query = self._normalize_query(query)
            
            # Generate embedding for the normalized query
            query_embedding = self.embedding_service.embed_text(normalized_query)
            
            # Generate cache ID
            cache_id = self._generate_cache_id(query)
            
            # Create point with response data
            point = PointStruct(
                id=int(cache_id[:8], 16),  # Convert first 8 chars of hex to int
                vector=query_embedding,
                payload={
                    "original_query": query,  # Keep original for display
                    "normalized_query": normalized_query,  # Store normalized for reference
                    "sql_query": response.get("sql_query"),
                    "tables": response.get("tables", []),
                    "columns": response.get("columns", {}),
                    "visualization": response.get("visualization"),
                    "results": response.get("results"),
                    "insights": response.get("insights"),
                    "explanation": response.get("explanation"),
                    "cached_at": datetime.now().isoformat(),
                    "cache_id": cache_id
                }
            )
            
            # Upsert to cache
            self.vector_store.upsert_points(
                collection_name=settings.CACHE_COLLECTION_NAME,
                points=[point]
            )
            logger.info(f"Cached response for query (ID: {cache_id[:8]})")
        except Exception as e:
            logger.error(f"Error caching response: {e}")
            # Don't raise - caching failure shouldn't break the flow
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache"""
        if not settings.CACHE_ENABLED:
            return {"enabled": False}
        
        try:
            collection_info = self.vector_store.get_collection_info(settings.CACHE_COLLECTION_NAME)
            return {
                "enabled": True,
                "cached_queries": collection_info.get("points_count", 0) if collection_info else 0
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"enabled": True, "error": str(e)}

