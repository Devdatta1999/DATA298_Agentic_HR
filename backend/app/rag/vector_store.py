"""Vector store service for Qdrant operations"""
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    """Qdrant vector store client"""
    
    def __init__(self):
        try:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None
            )
            logger.info(f"Connected to Qdrant at {settings.QDRANT_URL}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
    
    def create_collection_if_not_exists(self, collection_name: str, vector_size: int = 384):
        """Create a Qdrant collection if it doesn't exist"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {collection_name}")
            else:
                logger.info(f"Collection {collection_name} already exists")
        except Exception as e:
            logger.error(f"Error creating collection {collection_name}: {e}")
            raise
    
    def upsert_points(self, collection_name: str, points: List[PointStruct]):
        """Insert or update points in a collection"""
        try:
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
            logger.info(f"Upserted {len(points)} points to {collection_name}")
        except Exception as e:
            logger.error(f"Error upserting points: {e}")
            raise
    
    def search_similar(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 3,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )
            
            # Sort by score descending (Qdrant should already do this, but ensure it)
            sorted_results = sorted(results, key=lambda x: x.score, reverse=True)
            
            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                }
                for result in sorted_results
            ]
        except Exception as e:
            logger.error(f"Error searching in {collection_name}: {e}")
            return []
    
    def delete_collection(self, collection_name: str):
        """Delete a collection (use with caution)"""
        try:
            self.client.delete_collection(collection_name=collection_name)
            logger.info(f"Deleted collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise
    
    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a collection"""
        try:
            info = self.client.get_collection(collection_name=collection_name)
            return {
                "name": collection_name,
                "points_count": getattr(info, 'points_count', 0),
                "vectors_count": getattr(info, 'vectors_count', 0)
            }
        except Exception as e:
            logger.warning(f"Could not get collection info (may be expected): {e}")
            # Try alternative method - just check if collection exists
            try:
                collections = self.client.get_collections().collections
                if any(col.name == collection_name for col in collections):
                    return {"name": collection_name, "points_count": 0, "vectors_count": 0}
            except:
                pass
            return None

