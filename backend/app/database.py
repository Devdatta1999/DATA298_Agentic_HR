from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import sqlite3
from typing import Dict, List, Any

# PostgreSQL engine for HR data
postgres_engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
PostgresSession = sessionmaker(bind=postgres_engine)

# SQLite for conversation storage
sqlite_conn = sqlite3.connect(settings.SQLITE_DB_PATH, check_same_thread=False)
sqlite_conn.row_factory = sqlite3.Row

Base = declarative_base()


def get_db_schema() -> Dict[str, List[Dict[str, Any]]]:
    """Get database schema information for all tables in employees schema"""
    schema_info = {}
    
    with postgres_engine.connect() as conn:
        inspector = inspect(postgres_engine)
        tables = inspector.get_table_names(schema='employees')
        
        for table in tables:
            columns = inspector.get_columns(table, schema='employees')
            schema_info[f"employees.{table}"] = [
                {
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col["nullable"]
                }
                for col in columns
            ]
    
    return schema_info


def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """Execute SQL query and return results as list of dictionaries"""
    try:
        with postgres_engine.connect() as conn:
            result = conn.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()
            
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        raise Exception(f"SQL execution error: {str(e)}")


def validate_sql_query(query: str) -> bool:
    """Validate SQL query syntax"""
    try:
        with postgres_engine.connect() as conn:
            # Use EXPLAIN to validate without executing
            conn.execute(text(f"EXPLAIN {query}"))
            return True
    except Exception as e:
        return False


def init_conversation_db():
    """Initialize SQLite database for conversation storage"""
    cursor = sqlite_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    """)
    
    sqlite_conn.commit()


# Initialize conversation database on import
init_conversation_db()


