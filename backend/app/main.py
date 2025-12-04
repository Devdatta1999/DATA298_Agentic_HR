from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import router
import uvicorn

app = FastAPI(
    title="HR Analytics Agent API (RAG + Semantic Cache)",
    description="AI-powered HR analytics with RAG and semantic caching",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    return {
        "message": "HR Analytics Agent API (RAG + Semantic Cache)",
        "version": "2.0.0",
        "features": ["RAG", "Semantic Caching", "Custom HR Terms"],
        "docs": "/docs"
    }


if __name__ == "__main__":
    # Run on port 8001 for RAG branch (main branch uses 8000)
    uvicorn.run(app, host="0.0.0.0", port=8001)


