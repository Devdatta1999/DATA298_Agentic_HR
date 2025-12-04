"""RAG retriever for custom HR terms"""
import json
import os
from typing import List, Dict, Any, Optional
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.config import settings
from qdrant_client.models import PointStruct
import logging

logger = logging.getLogger(__name__)

class RAGRetriever:
    """Retrieves relevant custom HR terms and SQL examples from knowledge base"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.knowledge_base_path = os.path.join(
            os.path.dirname(__file__),
            "knowledge_base.json"
        )
        self._initialize_rag_collection()
    
    def _initialize_rag_collection(self):
        """Initialize RAG collection and load knowledge base"""
        try:
            # Create collection
            vector_size = self.embedding_service.get_embedding_dimension()
            self.vector_store.create_collection_if_not_exists(
                collection_name=settings.RAG_COLLECTION_NAME,
                vector_size=vector_size
            )
            
            # Check if collection is empty, if so, load knowledge base
            collection_info = self.vector_store.get_collection_info(settings.RAG_COLLECTION_NAME)
            points_count = collection_info.get("points_count", 0) if collection_info else 0
            if points_count == 0:
                logger.info("RAG collection is empty, loading knowledge base...")
                self._load_knowledge_base()
            else:
                logger.info(f"RAG collection already has {points_count} points")
        except Exception as e:
            logger.error(f"Error initializing RAG collection: {e}")
            raise
    
    def _load_knowledge_base(self):
        """Load knowledge base from JSON and index in Qdrant"""
        try:
            with open(self.knowledge_base_path, 'r') as f:
                knowledge_base = json.load(f)
            
            terms = knowledge_base.get("custom_terms", [])
            points = []
            
            for idx, term in enumerate(terms):
                # Create searchable text from term data
                searchable_text = f"{term['term']} {term['definition']} {' '.join(term.get('keywords', []))}"
                
                # Generate embedding
                embedding = self.embedding_service.embed_text(searchable_text)
                
                # Create point with payload
                point = PointStruct(
                    id=idx,
                    vector=embedding,
                    payload={
                        "term": term["term"],
                        "definition": term["definition"],
                        "formula": term.get("formula", ""),
                        "sql_example": term["sql_example"],
                        "keywords": term.get("keywords", []),
                        "complexity": term.get("complexity", "medium"),
                        "searchable_text": searchable_text
                    }
                )
                points.append(point)
            
            # Upsert all points
            if points:
                self.vector_store.upsert_points(
                    collection_name=settings.RAG_COLLECTION_NAME,
                    points=points
                )
                logger.info(f"Loaded {len(points)} terms into RAG collection")
        except FileNotFoundError:
            logger.error(f"Knowledge base file not found: {self.knowledge_base_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            raise
    
    def retrieve_relevant_context(self, question: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant custom terms and SQL examples for a question"""
        try:
            # Generate embedding for the question
            question_embedding = self.embedding_service.embed_text(question)
            
            # Search for similar terms
            results = self.vector_store.search_similar(
                collection_name=settings.RAG_COLLECTION_NAME,
                query_vector=question_embedding,
                limit=top_k,
                score_threshold=settings.RAG_SIMILARITY_THRESHOLD
            )
            
            if results:
                logger.info(f"Retrieved {len(results)} relevant terms for question")
                return [
                    {
                        "term": result["payload"]["term"],
                        "definition": result["payload"]["definition"],
                        "sql_example": result["payload"]["sql_example"],
                        "formula": result["payload"].get("formula", ""),
                        "similarity_score": result["score"]
                    }
                    for result in results
                ]
            else:
                logger.info("No relevant terms found in RAG for question")
                return []
        except Exception as e:
            logger.error(f"Error retrieving RAG context: {e}")
            return []
    
    def format_rag_context_for_prompt(self, context: List[Dict[str, Any]]) -> str:
        """Format retrieved context for inclusion in LLM prompt"""
        if not context:
            return ""
        
        formatted = "\n\n## Relevant Custom HR Terms and SQL Examples:\n\n"
        for idx, item in enumerate(context, 1):
            formatted += f"### {idx}. {item['term']}\n"
            formatted += f"**Definition**: {item['definition']}\n"
            if item.get('formula'):
                formatted += f"**Formula**: {item['formula']}\n"
            formatted += f"**SQL Example**:\n```sql\n{item['sql_example']}\n```\n"
            formatted += f"**Relevance Score**: {item['similarity_score']:.2f}\n\n"
        
        return formatted

