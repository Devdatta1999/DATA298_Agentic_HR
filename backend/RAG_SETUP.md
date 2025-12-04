# RAG and Semantic Caching Setup

This branch implements **RAG (Retrieval-Augmented Generation)** and **Semantic Caching** to improve the HR Analytics Agent.

## Features

1. **RAG (Retrieval-Augmented Generation)**
   - Custom HR terms knowledge base (10 complex terms)
   - Vector similarity search using Qdrant
   - Automatic SQL example retrieval for custom terms

2. **Semantic Caching**
   - Similarity-based query caching
   - Fast response for similar queries
   - No TTL - cache persists for demo

## Architecture

- **Single Qdrant Service**: Handles both RAG and caching
  - Collection: `rag_knowledge` - Custom HR terms
  - Collection: `semantic_cache` - Cached query responses
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (local, 384 dimensions)
- **Similarity Thresholds**:
  - RAG: 0.70 (retrieve relevant context)
  - Cache: 0.85 (strict match for cache hit)

## Setup Instructions

### 1. Start Qdrant (Docker)

```bash
cd backend
docker-compose up -d
```

This will:
- Start Qdrant on ports 6333 (HTTP) and 6334 (gRPC)
- Create persistent volume `qdrant_storage` for data persistence

### 2. Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

New dependencies:
- `qdrant-client==1.7.0`
- `sentence-transformers==2.2.2`
- `numpy==1.24.3`

### 3. Start Backend (Port 8001)

```bash
cd backend
chmod +x start_rag.sh
./start_rag.sh
```

Or manually:
```bash
uvicorn app.main:app --reload --port 8001
```

### 4. Update Frontend Port

Update frontend to connect to `http://localhost:8001` instead of `8000`.

Or run frontend on port 3001:
```bash
cd frontend
PORT=3001 npm start
```

## Custom HR Terms

The knowledge base includes 10 complex custom terms:

1. **Internal Mobility Rate** - Department transfer analysis
2. **Flight Risk Score** - Employee retention prediction
3. **Employee Lifetime Value (ELV)** - Total employee value
4. **Total Rewards** - Comprehensive compensation package
5. **Skills Gap Analysis** - Missing skills identification
6. **Engagement Trend Score** - Engagement trajectory
7. **Training ROI by Department** - Training effectiveness
8. **Compensation Equity Ratio** - Pay equity analysis
9. **High Performer Retention Rate** - Top talent retention
10. **Cross-Functional Collaboration Index** - Interdepartmental work

Each term includes:
- Definition
- Formula
- Complete SQL example (with CTEs, window functions, joins)
- Keywords for matching

## How It Works

### RAG Flow
1. User asks question (e.g., "Calculate Internal Mobility Rate")
2. Question is embedded
3. Similar terms retrieved from knowledge base
4. SQL examples injected into LLM prompt
5. LLM generates SQL using provided examples

### Cache Flow
1. User asks question
2. Question is embedded
3. Similar cached queries searched (threshold: 0.85)
4. If match found → Return cached response (fast!)
5. If no match → Process normally and cache result

## Testing

### Test RAG
```bash
# These should work with RAG (won't work without RAG):
curl -X POST http://localhost:8001/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Calculate Internal Mobility Rate by department"}'
```

### Test Cache
1. Ask a question (first time - slow)
2. Ask similar question (second time - fast from cache)

## Port Configuration

- **Backend**: 8001 (main branch uses 8000)
- **Frontend**: 3001 (main branch uses 3000)
- **Qdrant**: 6333 (HTTP), 6334 (gRPC)

## Persistence

- Qdrant data persists in Docker volume `qdrant_storage`
- Cache builds up over time (no expiration)
- Knowledge base loaded on first startup

## Troubleshooting

1. **Qdrant not running**: `docker-compose up -d`
2. **Embedding model download**: First run downloads model (~90MB)
3. **Port conflicts**: Ensure ports 8001, 6333, 6334 are free
4. **Import errors**: Install dependencies: `pip install -r requirements.txt`

