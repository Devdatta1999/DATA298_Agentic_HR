#!/bin/bash

# Startup script for RAG branch backend (Port 8001)

echo "🚀 Starting Backend for RAG Branch (RAG + Semantic Cache)"
echo "=========================================================="

# Check if Qdrant is running
echo "📦 Checking Qdrant connection..."
if ! curl -s http://localhost:6333/health > /dev/null 2>&1; then
    echo "⚠️  Qdrant is not running. Starting Qdrant with Docker..."
    cd "$(dirname "$0")"
    docker-compose up -d
    echo "⏳ Waiting for Qdrant to be ready..."
    sleep 5
    if ! curl -s http://localhost:6333/collections > /dev/null 2>&1; then
        echo "❌ Failed to start Qdrant. Please check Docker."
        exit 1
    fi
    echo "✅ Qdrant is running"
else
    echo "✅ Qdrant is already running"
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if Ollama is running
echo "🤖 Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running. Please start Ollama first."
    echo "   Run: ollama serve"
    exit 1
fi
echo "✅ Ollama is running"

# Start the backend server on port 8001
echo "🌐 Starting FastAPI server on port 8001..."
echo "   API docs: http://localhost:8001/docs"
echo "   Health: http://localhost:8001/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
uvicorn app.main:app --reload --port 8001 --host 0.0.0.0

