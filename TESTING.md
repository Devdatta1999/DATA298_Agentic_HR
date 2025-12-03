# Testing Guide

## Prerequisites Check

Before testing, ensure you have:

1. ✅ **Ollama installed and running**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # If not, start Ollama
   ollama serve
   
   # Verify model is available
   ollama list
   # Should show: llama3.1:8b
   ```

2. ✅ **Python 3.9+ installed**
   ```bash
   python3 --version
   ```

3. ✅ **Node.js 18+ installed**
   ```bash
   node --version
   npm --version
   ```

4. ✅ **Database connectivity**
   - Your IP should be whitelisted in AWS RDS security groups
   - Test connection:
   ```bash
   psql -h hrdatamanagement.cf8wa4yas0vz.us-west-2.rds.amazonaws.com -U postgres -d hrdatamanagement
   # Password: data298a
   ```

## Step-by-Step Testing

### Step 1: Start Ollama (if not running)

```bash
# In a terminal, start Ollama
ollama serve

# In another terminal, verify model
ollama pull llama3.1:8b
ollama list
```

### Step 2: Start Backend Server

```bash
cd backend

# Create virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test backend health:**
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy","service":"HR Analytics Agent"}
```

### Step 3: Start Frontend Server

Open a **new terminal**:

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start the dev server
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 4: Test the Application

1. **Open browser**: Navigate to `http://localhost:3000`

2. **You should see:**
   - Welcome screen with example questions
   - Token counter showing 0 tokens
   - Input field at the bottom

3. **Test Query 1: Simple Headcount**
   ```
   Show me department wise headcount
   ```
   
   **Expected behavior:**
   - Query processes (may take 10-30 seconds)
   - SQL query is generated
   - Results displayed in a bar chart
   - Insights and explanation shown
   - Sidebar shows tables/columns and SQL query
   - Token count increases

4. **Test Query 2: Average Salary**
   ```
   What is the average salary by department?
   ```
   
   **Expected behavior:**
   - Follow-up question in same session
   - Uses conversation context
   - Shows bar chart with average salaries
   - Token count continues from previous query

5. **Test Query 3: Time Series**
   ```
   Show me headcount trends over time
   ```
   
   **Expected behavior:**
   - Line chart for time series data
   - Shows monthly trends

6. **Test Sidebar:**
   - Click on any assistant message with visualization
   - Sidebar should show:
     - Tables used
     - Columns used
     - Generated SQL query

## Troubleshooting

### Issue: "Connection refused" to Ollama

**Solution:**
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Issue: Database connection error

**Solution:**
1. Check AWS RDS security group allows your IP
2. Test connection manually:
   ```bash
   psql -h hrdatamanagement.cf8wa4yas0vz.us-west-2.rds.amazonaws.com -U postgres -d hrdatamanagement
   ```
3. Verify credentials in `backend/app/config.py`

### Issue: Frontend can't connect to backend

**Solution:**
1. Verify backend is running on port 8000
2. Check CORS settings in `backend/app/config.py`
3. Check browser console for errors
4. Verify proxy settings in `frontend/vite.config.ts`

### Issue: SQL generation errors

**Solution:**
1. Check Ollama model is loaded: `ollama list`
2. Check backend logs for LLM errors
3. Try simpler queries first
4. Verify database schema is accessible

### Issue: No visualizations showing

**Solution:**
1. Check browser console for errors
2. Verify data is returned (check Network tab)
3. Check if results array is not empty
4. Verify Recharts is installed: `npm list recharts`

## Quick Test Script

Run this to test all components:

```bash
# Test 1: Ollama
echo "Testing Ollama..."
curl -s http://localhost:11434/api/tags | grep -q "llama3.1" && echo "✅ Ollama OK" || echo "❌ Ollama not running"

# Test 2: Backend
echo "Testing Backend..."
curl -s http://localhost:8000/api/health | grep -q "healthy" && echo "✅ Backend OK" || echo "❌ Backend not running"

# Test 3: Frontend
echo "Testing Frontend..."
curl -s http://localhost:3000 | grep -q "html" && echo "✅ Frontend OK" || echo "❌ Frontend not running"
```

## Expected Query Examples

Here are some queries you can test:

1. **Department Analysis:**
   - "Show me department wise headcount"
   - "What is the average salary by department?"
   - "Which department has the highest attrition rate?"

2. **Employee Analysis:**
   - "Show employees with highest performance ratings"
   - "List employees by job title"
   - "Show gender distribution"

3. **Time-based Analysis:**
   - "Show headcount trends over time"
   - "What is the monthly attrition rate?"
   - "Show hiring trends by month"

4. **Performance Analysis:**
   - "Show average performance scores by department"
   - "Which employees have completed training?"
   - "Show engagement survey results"

## Performance Notes

- First query may take 20-40 seconds (model loading)
- Subsequent queries: 10-20 seconds
- Token counting updates after each query
- Session persists across page refreshes (stored in SQLite)

## Next Steps After Testing

If everything works:
1. ✅ Try more complex queries
2. ✅ Test multi-turn conversations
3. ✅ Verify token counting accuracy
4. ✅ Check visualization types (bar, line, pie, table)

If issues occur:
1. Check logs in both terminals
2. Check browser console (F12)
3. Verify all prerequisites
4. Review error messages carefully

