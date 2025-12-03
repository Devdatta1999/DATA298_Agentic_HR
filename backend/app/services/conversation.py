import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from app.config import settings
from app.database import sqlite_conn


def create_session() -> str:
    """Create a new conversation session"""
    session_id = str(uuid.uuid4())
    cursor = sqlite_conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (session_id, created_at, updated_at) VALUES (?, ?, ?)",
        (session_id, datetime.now(), datetime.now())
    )
    sqlite_conn.commit()
    return session_id


def add_message(session_id: str, role: str, content: str, metadata: Optional[Dict] = None):
    """Add a message to a conversation session"""
    cursor = sqlite_conn.cursor()
    metadata_json = json.dumps(metadata) if metadata else None
    
    cursor.execute(
        "INSERT INTO messages (session_id, role, content, metadata) VALUES (?, ?, ?, ?)",
        (session_id, role, content, metadata_json)
    )
    
    # Update session updated_at
    cursor.execute(
        "UPDATE sessions SET updated_at = ? WHERE session_id = ?",
        (datetime.now(), session_id)
    )
    
    sqlite_conn.commit()


def get_conversation_history(session_id: str, limit: int = 20) -> List[Dict]:
    """Get conversation history for a session"""
    cursor = sqlite_conn.cursor()
    cursor.execute(
        """
        SELECT role, content, metadata, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY created_at ASC
        LIMIT ?
        """,
        (session_id, limit)
    )
    
    rows = cursor.fetchall()
    messages = []
    for row in rows:
        metadata = json.loads(row[2]) if row[2] else {}
        messages.append({
            "role": row[0],
            "content": row[1],
            "metadata": metadata,
            "created_at": row[3]
        })
    
    return messages


def get_session_token_count(session_id: str) -> int:
    """Get total token count for a session"""
    from app.services.token_counter import token_counter
    
    messages = get_conversation_history(session_id)
    return token_counter.count_tokens_in_messages(messages)


