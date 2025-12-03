# 🚀 Quick Start Guide

## Prerequisites (5 minutes)

1. **Install Ollama** (if not installed):
   ```bash
   # macOS
   brew install ollama
   
   # Or download from https://ollama.ai
   ```

2. **Pull the model**:
   ```bash
   ollama pull llama3.1:8b
   ```

3. **Start Ollama** (keep this running):
   ```bash
   ollama serve
   ```

## Step 1: Test Connections (2 minutes)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python test_connection.py
```

**Expected output:**
```
✅ Database connection successful!
✅ Ollama connection successful!
✅ SQLite connection successful!
🎉 All systems ready!
```

## Step 2: Start Backend (1 minute)

**Keep Terminal 1 open:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Step 3: Start Frontend (1 minute)

**Open Terminal 2:**
```bash
cd frontend
npm install  # First time only
npm run dev
```

**You should see:**
```
➜  Local:   http://localhost:3000/
```

## Step 4: Test the App (2 minutes)

1. **Open browser:** http://localhost:3000

2. **Try your first query:**
   ```
   Show me department wise headcount
   ```

3. **Wait 10-30 seconds** (first query takes longer)

4. **You should see:**
   - ✅ SQL query generated
   - ✅ Bar chart with department headcounts
   - ✅ Insights and explanation
   - ✅ Sidebar with tables/columns and SQL
   - ✅ Token counter updated

## Troubleshooting

### ❌ "Ollama connection failed"
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, verify
ollama list
```

### ❌ "Database connection failed"
- Check your IP is whitelisted in AWS RDS security groups
- Verify credentials in `backend/app/config.py`

### ❌ Frontend can't connect
- Make sure backend is running on port 8000
- Check browser console (F12) for errors

## Next Steps

- Try more queries from the welcome screen
- Check the sidebar for SQL queries
- Monitor token usage
- Test multi-turn conversations

**Full testing guide:** See [TESTING.md](./TESTING.md)

