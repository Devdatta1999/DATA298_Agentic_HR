from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:data298a@hrdatamanagement.cf8wa4yas0vz.us-west-2.rds.amazonaws.com:5432/hrdatamanagement"
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    
    # SQLite for conversation storage
    SQLITE_DB_PATH: str = "conversations.db"
    
    # CORS - Updated for RAG branch (different ports)
    CORS_ORIGINS: list = ["http://localhost:3001", "http://localhost:5174"]
    
    # Qdrant Configuration (for RAG and Semantic Caching)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    
    # RAG Configuration
    RAG_COLLECTION_NAME: str = "rag_knowledge"
    RAG_SIMILARITY_THRESHOLD: float = 0.60  # Threshold for RAG retrieval (lowered for better matching)
    
    # Semantic Cache Configuration
    CACHE_COLLECTION_NAME: str = "semantic_cache"
    CACHE_SIMILARITY_THRESHOLD: float = 0.65  # Lowered to 0.65 for better matching with improved normalization
    CACHE_ENABLED: bool = True
    
    # Embedding Model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # Local model
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


