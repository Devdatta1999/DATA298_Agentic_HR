# Testing Instructions - Demo 25 Questions

## Current Status

✅ **25 Best Questions Selected** - Diverse, representative, ready for demo
✅ **Fixes Applied** - SQL prompts and visualization heuristics improved
⚠️ **Need Re-test** - After backend restart to load new prompts

## Issues Found in First Test

### SQL Issues (7 questions)
1. Q6, Q39: Using `compensation_history.NewSalary` instead of `employee_master.Salary`
2. Q11: Missing specific employee filter
3. Q20: Using `employee_master` instead of `skills_inventory`
4. Q31: Using `employee_master` instead of `headcount_attrition_summary` for time series
5. Q32: Wrong SQL (counting only active instead of all statuses)
6. Q50: Different calculation method

### Visualization Issues (4 questions)
1. Q11: Expected line, got none (time series)
2. Q26: Expected bar, got pie (salary distribution by gender)
3. Q31: Expected line, got bar (time series)
4. Q32: Expected pie, got none (employee count by status)

## Fixes Applied

1. ✅ **SQL Prompts Updated:**
   - Clarified: "average salary by department" → use `employee_master.Salary`
   - Clarified: "most common skills" → use `skills_inventory` table
   - Clarified: "headcount over time" → use `headcount_attrition_summary` with `MonthEnd`
   - Clarified: "employee count by status" → count ALL statuses, not just active

2. ✅ **Visualization Heuristics Updated:**
   - "salary distribution by X" → bar chart (comparison, not pie)
   - "employee count by status" → pie chart (distribution)
   - "over time" queries with date columns → line chart
   - Better time series detection

## Next Steps

### 1. Restart Backend
```bash
# Stop current backend (Ctrl+C)
# Then restart:
cd backend
source venv/bin/activate  # or your venv activation
uvicorn app.main:app --reload --port 8001
```

### 2. Run Test
```bash
cd backend
python3 test_demo_25_questions.py
```

### 3. Expected Results After Fixes

- **SQL Accuracy:** 72% → 95%+ (target)
- **Viz Accuracy:** 84% → 95%+ (target)
- **Cache Hits:** Will be lower on first run (fresh generation)
- **After successful test:** All 25 will be cached correctly

### 4. If Issues Persist

If cache still has wrong SQL:
- Option A: Clear Qdrant cache collection
- Option B: Slightly modify question phrasing in test
- Option C: Wait for cache to naturally update with correct responses

## Demo Questions File

The 25 selected questions are saved in:
- **JSON:** `backend/app/patterns/demo_25_questions.json`
- **Markdown:** `backend/app/patterns/DEMO_25_QUESTIONS.md`

## Success Criteria

✅ All 25 questions execute successfully
✅ SQL matches expected (semantic match acceptable)
✅ Visualization type matches expected
✅ Responses are cached for fast demo

Once all 25 pass, you can confidently use them for your demo!

