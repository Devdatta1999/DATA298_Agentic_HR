# Agentic HR Analytics

An AI-powered HR analytics application that enables natural language queries to analyze HR data, generate insights, and create visualizations.

## Features

- 🤖 **AI-Powered Analysis**: Natural language queries converted to SQL using Llama3.1:8B
- 📊 **Data Visualization**: Automatic chart generation based on query results
- 💬 **Conversational Interface**: Multi-turn conversations with session memory
- 🔍 **Transparency**: View SQL queries, tables, and columns used
- 📈 **Token Tracking**: Monitor token usage per conversation session
- 🎨 **Modern UI**: Clean, intuitive interface for HR professionals

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- LangChain - LLM application framework
- LangGraph - State management for agent workflows
- SQLAlchemy - Database ORM
- PostgreSQL - AWS RDS database
- SQLite - Session/conversation storage

### Frontend
- React + TypeScript
- TailwindCSS - Styling
- Chart.js / Recharts - Data visualization
- React Query - Data synchronization
- Zustand - State management

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── hr_agent.py
│   │   │   └── prompts.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── conversation.py
│   │       └── token_counter.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## Setup

See [SETUP.md](./SETUP.md) for detailed setup instructions.

### Quick Start

1. **Install Ollama and pull the model:**
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.1:8b
```

2. **Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

4. **Open the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Database Schema

The application connects to AWS RDS PostgreSQL with the following tables in the `employees` schema:

- `employee_master` - Employee basic information
- `compensation_history` - Salary change history
- `engagement_surveys` - Employee satisfaction surveys
- `headcount_attrition_summary` - Monthly headcount and attrition metrics
- `performance_reviews` - Performance evaluation records
- `skills_inventory` - Employee skills and proficiency
- `training_records` - Training completion records

## Quick Start Testing

1. **Test connections first:**
   ```bash
   cd backend
   source venv/bin/activate
   python test_connection.py
   ```

2. **Start the application:**
   ```bash
   # Terminal 1: Backend
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

3. **Open browser:** `http://localhost:3000`

4. **Try a query:** "Show me department wise headcount"

See [TESTING.md](./TESTING.md) for detailed testing instructions.

## Usage

Enter natural language queries like:
- "Show me department wise headcount"
- "What is the average salary by department?"
- "Show employee turnover trends"
- "Which employees have the highest performance ratings?"

The agent will:
- Parse your question
- Identify relevant tables and columns
- Generate and execute SQL queries
- Create appropriate visualizations
- Provide insights and explanations

