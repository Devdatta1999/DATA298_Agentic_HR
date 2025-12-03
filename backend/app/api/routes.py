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
    token_count: Optional[int] = None
    error: Optional[str] = None


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a natural language HR analytics query"""
    
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
        
        # Format response
        answer = result.get("explanation", "Analysis complete")
        if result.get("insights"):
            insights_text = "\n".join([f"• {insight}" for insight in result["insights"]])
            answer = f"{insights_text}\n\n{answer}"
        
        # Add assistant message
        metadata = {
            "sql_query": result.get("sql_query"),
            "tables": result.get("tables", []),
            "columns": result.get("columns", {}),
            "visualization": result.get("visualization"),
            "results_count": len(result.get("results", []))
        }
        add_message(session_id, "assistant", answer, metadata)
        
        # Get token count
        token_count = get_session_token_count(session_id)
        
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
            token_count=token_count
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


