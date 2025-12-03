#!/usr/bin/env python3
"""
Quick test script to verify database and Ollama connections
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.database import postgres_engine, execute_sql_query
from langchain_ollama import ChatOllama

def test_database():
    """Test PostgreSQL connection"""
    print("🔍 Testing PostgreSQL connection...")
    try:
        with postgres_engine.connect() as conn:
            result = conn.execute("SELECT 1")
            result.fetchone()
        print("✅ Database connection successful!")
        
        # Test query
        print("🔍 Testing sample query...")
        result = execute_sql_query("SELECT COUNT(*) as count FROM employees.employee_master")
        if result:
            print(f"✅ Sample query successful! Found {result[0].get('count', 'N/A')} records")
        else:
            print("✅ Sample query successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_ollama():
    """Test Ollama connection"""
    print("\n🔍 Testing Ollama connection...")
    try:
        llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0.1
        )
        response = llm.invoke("Say 'Hello' if you can hear me.")
        print(f"✅ Ollama connection successful!")
        print(f"   Response: {response.content[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print(f"   Make sure Ollama is running: ollama serve")
        print(f"   And model is available: ollama pull {settings.OLLAMA_MODEL}")
        return False

def test_sqlite():
    """Test SQLite for conversations"""
    print("\n🔍 Testing SQLite conversation storage...")
    try:
        from app.database import sqlite_conn
        cursor = sqlite_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✅ SQLite connection successful! Found {len(tables)} tables")
        return True
    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("HR Analytics - Connection Test")
    print("=" * 50)
    
    db_ok = test_database()
    ollama_ok = test_ollama()
    sqlite_ok = test_sqlite()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"  Database: {'✅' if db_ok else '❌'}")
    print(f"  Ollama:   {'✅' if ollama_ok else '❌'}")
    print(f"  SQLite:   {'✅' if sqlite_ok else '❌'}")
    print("=" * 50)
    
    if db_ok and ollama_ok and sqlite_ok:
        print("\n🎉 All systems ready! You can start the application.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

