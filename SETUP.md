# Setup Instructions

## Prerequisites

1. **Python 3.9+** installed
2. **Node.js 18+** and npm installed
3. **Ollama** installed and running with `llama3.1:8b` model

### Installing Ollama

1. Download and install Ollama from https://ollama.ai
2. Pull the required model:
```bash
ollama pull llama3.1:8b
```
3. Verify Ollama is running:
```bash
ollama list
```

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (optional, defaults are set):
```bash
cp .env.example .env
# Edit .env if needed
```

5. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Database Connection

The application is configured to connect to AWS RDS PostgreSQL:
- Host: `hrdatamanagement.cf8wa4yas0vz.us-west-2.rds.amazonaws.com`
- Database: `hrdatamanagement`
- Username: `postgres`
- Password: `data298a`

Make sure:
1. Your IP is whitelisted in AWS RDS security groups
2. The database is accessible from your network
3. The tables exist in the `employees` schema

## Testing the Application

1. Start Ollama (if not running as a service)
2. Start the backend server
3. Start the frontend server
4. Open `http://localhost:3000` in your browser
5. Try asking questions like:
   - "Show me department wise headcount"
   - "What is the average salary by department?"
   - "Show employee turnover trends"

## Troubleshooting

### Ollama Connection Issues
- Make sure Ollama is running: `ollama serve`
- Check if the model is available: `ollama list`
- Verify the base URL in backend config matches your Ollama setup

### Database Connection Issues
- Verify your IP is whitelisted in AWS RDS
- Check network connectivity to AWS
- Verify database credentials

### Frontend Not Connecting to Backend
- Check that backend is running on port 8000
- Verify CORS settings in backend config
- Check browser console for errors


