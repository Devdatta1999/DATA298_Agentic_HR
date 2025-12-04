#!/bin/bash

# Startup script for RAG branch frontend (Port 3001)

echo "🚀 Starting Frontend for RAG Branch"
echo "=================================="
echo "📍 Port: 3001"
echo "📍 Backend: http://localhost:8001"
echo ""

cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Clear Vite cache
echo "🧹 Clearing Vite cache..."
rm -rf node_modules/.vite
rm -rf dist

echo "✅ Starting Vite dev server on port 3001..."
echo ""
echo "Frontend will be available at: http://localhost:3001"
echo "Press Ctrl+C to stop"
echo ""

npm run dev

