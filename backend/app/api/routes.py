from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.agent.hr_agent import hr_agent
from app.services.conversation import (
    create_session,
    add_message,
    get_conversation_history,
    get_session_token_count
)
from app.services.token_counter import token_counter

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    success: bool
    session_id: str
    answer: str
    sql_query: Optional[str] = None
    results: Optional[List[Dict]] = None
    tables: Optional[List[str]] = None
    columns: Optional[Dict[str, List[str]]] = None
    visualization: Optional[Dict] = None
    insights: Optional[List[str]] = None
    explanation: Optional[str] = None
    token_count: Optional[int] = None  # Total session tokens
    query_tokens: Optional[int] = None  # Tokens for this query only
    cache_hit: Optional[bool] = None  # Whether response came from cache
    rag_used: Optional[bool] = None  # Whether RAG was used
    cache_similarity: Optional[float] = None  # Cache similarity score
    error: Optional[str] = None


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a natural language HR analytics query"""
    import time
    
    start_time = time.time()
    
    # Create or use existing session
    if not request.session_id:
        session_id = create_session()
    else:
        session_id = request.session_id
    
    # Get conversation history
    conversation_history = get_conversation_history(session_id)
    
    # Add user message
    add_message(session_id, "user", request.question)
    
    try:
        # Process query with agent
        result = hr_agent.process_query(request.question, conversation_history)
        
        if not result.get("success"):
            error_msg = result.get("error", "Unknown error")
            add_message(session_id, "assistant", f"Error: {error_msg}", {"error": True})
            return QueryResponse(
                success=False,
                session_id=session_id,
                answer=f"Error: {error_msg}",
                error=error_msg,
                sql_query=result.get("sql_query")
            )
        
        # Format response - only include brief summary if we have structured insights
        # The structured InsightsCard will display everything nicely
        if result.get("insights") and len(result.get("insights", [])) > 0:
            # Just a brief acknowledgment - InsightsCard will show the details
            answer = "Analysis complete. See insights below."
        else:
            answer = result.get("explanation", "Analysis complete")
        
        # Add assistant message
        metadata = {
            "sql_query": result.get("sql_query"),
            "tables": result.get("tables", []),
            "columns": result.get("columns", {}),
            "visualization": result.get("visualization"),
            "results_count": len(result.get("results", []))
        }
        add_message(session_id, "assistant", answer, metadata)
        
        # Get token count - use LLM tokens from result, add stored message tokens
        llm_tokens = result.get("tokens", 0)  # Tokens used for this query
        stored_message_tokens = get_session_token_count(session_id)
        # Total = LLM tokens (from this query) + stored message tokens (from previous messages)
        total_token_count = llm_tokens + stored_message_tokens
        
        response_time = int((time.time() - start_time) * 1000)  # in milliseconds
        
        return QueryResponse(
            success=True,
            session_id=session_id,
            answer=answer,
            sql_query=result.get("sql_query"),
            results=result.get("results", []),
            tables=result.get("tables", []),
            columns=result.get("columns", {}),
            visualization=result.get("visualization"),
            insights=result.get("insights", []),
            explanation=result.get("explanation"),
            token_count=total_token_count,  # Total tokens for session
            query_tokens=llm_tokens,  # Tokens for this query only
            cache_hit=result.get("cache_hit", False),  # Cache hit flag
            rag_used=result.get("rag_used", False),  # RAG usage flag
            cache_similarity=result.get("cache_similarity")  # Cache similarity score
        )
    
    except Exception as e:
        import traceback
        error_msg = f"Processing error: {str(e)}"
        error_trace = traceback.format_exc()
        print(f"Error in process_query: {error_trace}")  # Log for debugging
        add_message(session_id, "assistant", error_msg, {"error": True})
        return QueryResponse(
            success=False,
            session_id=session_id,
            answer=f"Error: {error_msg}",
            error=error_msg,
            token_count=get_session_token_count(session_id)
        )


@router.get("/conversation/{session_id}")
async def get_conversation(session_id: str):
    """Get conversation history for a session"""
    messages = get_conversation_history(session_id)
    token_count = get_session_token_count(session_id)
    
    return {
        "session_id": session_id,
        "messages": messages,
        "token_count": token_count
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "HR Analytics Agent"}


