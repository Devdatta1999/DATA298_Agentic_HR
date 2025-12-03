HR_DATABASE_SCHEMA = """
Database Schema for HR Analytics:

=== TABLE RELATIONSHIPS ===
- employee_master is the MAIN/CENTRAL table with EmployeeID as Primary Key
- Most tables link to employee_master via EmployeeID (one-to-many relationships)
- headcount_attrition_summary is independent (no EmployeeID, uses Department for grouping)
- When joining employee data, use: table_name."EmployeeID" = employee_master."EmployeeID"
- ManagerID in employee_master references EmployeeID in the same table (self-referential)

=== TABLES ===

Table: employees.employee_master (CENTRAL TABLE - Primary Key: EmployeeID)
Columns:
- "EmployeeID" (varchar) - PRIMARY KEY - Links to all other employee tables
- "FullName" (varchar)
- "Department" (varchar) - Use for department-based queries
- "JobTitle" (varchar)
- "Email" (varchar)
- "Gender" (varchar)
- "HireDate" (date)
- "TerminationDate" (date) - NULL for active employees
- "Salary" (numeric) - Current salary
- "ManagerID" (varchar) - References EmployeeID in same table (self-join)
- "PerformanceRating" (numeric)
- "Status" (varchar) - Active/Inactive/Terminated
JOIN Example: employee_master."EmployeeID" = other_table."EmployeeID"

Table: employees.compensation_history
Columns:
- "ChangeID" (varchar) - PRIMARY KEY
- "EmployeeID" (varchar) - FOREIGN KEY → employee_master."EmployeeID"
- "ChangeDate" (date)
- "OldSalary" (numeric)
- "NewSalary" (numeric)
- "Reason" (varchar)
JOIN: compensation_history."EmployeeID" = employee_master."EmployeeID"
Use for: Salary change history, compensation trends

Table: employees.engagement_surveys
Columns:
- "SurveyResponseID" (varchar) - PRIMARY KEY
- "EmployeeID" (varchar) - FOREIGN KEY → employee_master."EmployeeID"
- "SurveyDate" (date)
- "OverallSatisfaction" (numeric)
- "WorkLifeBalanceScore" (numeric)
- "ManagerFeedbackScore" (numeric)
JOIN: engagement_surveys."EmployeeID" = employee_master."EmployeeID"
Use for: Employee satisfaction, engagement metrics

Table: employees.headcount_attrition_summary (INDEPENDENT - No EmployeeID)
Columns:
- "RecordID" (varchar) - PRIMARY KEY
- "MonthEnd" (date) - Use for time-based analysis
- "Department" (varchar) - Links to employee_master."Department" (not EmployeeID)
- "Headcount" (numeric) - Total employees in department
- "Hires" (numeric) - New hires in period
- "Terminations" (numeric) - Terminations in period
- "AttritionRate" (numeric) - Calculated attrition percentage
JOIN: headcount_attrition_summary."Department" = employee_master."Department"
Use for: Department headcount, attrition trends, hiring patterns

Table: employees.performance_reviews
Columns:
- "ReviewID" (varchar) - PRIMARY KEY
- "EmployeeID" (varchar) - FOREIGN KEY → employee_master."EmployeeID"
- "ReviewDate" (date)
- "ReviewerID" (varchar) - References EmployeeID (could be manager)
- "OverallScore" (numeric)
- "Communication" (numeric)
- "Teamwork" (numeric)
- "ProblemSolving" (numeric)
JOIN: performance_reviews."EmployeeID" = employee_master."EmployeeID"
Use for: Performance analysis, review scores

Table: employees.skills_inventory
Columns:
- "SkillID" (varchar) - PRIMARY KEY
- "EmployeeID" (varchar) - FOREIGN KEY → employee_master."EmployeeID"
- "SkillName" (varchar)
- "ProficiencyLevel" (varchar) - Beginner/Intermediate/Advanced/Expert
JOIN: skills_inventory."EmployeeID" = employee_master."EmployeeID"
Note: One employee can have multiple skills (one-to-many)
Use for: Skills analysis, competency mapping

Table: employees.training_records
Columns:
- "TrainingID" (varchar) - PRIMARY KEY
- "EmployeeID" (varchar) - FOREIGN KEY → employee_master."EmployeeID"
- "CourseName" (varchar)
- "CompletionDate" (date)
- "Status" (varchar) - Completed/In Progress/Not Started
- "Score" (numeric)
JOIN: training_records."EmployeeID" = employee_master."EmployeeID"
Note: One employee can have multiple training records
Use for: Training completion, learning analytics
"""

TABLE_SELECTION_GUIDELINES = """
=== CRITICAL: TABLE SELECTION RULES ===

1. HEADCOUNT QUERIES - Choose the RIGHT table:
   
   USE employee_master when question asks for:
   - "current headcount" / "show me headcount" / "department wise headcount"
   - "how many employees" / "number of employees"
   - "headcount by department" (DEFAULT - means current)
   - Real-time/current state queries
   → Query: SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department"
   
   USE headcount_attrition_summary when question asks for:
   - "historical headcount" / "headcount trends" / "headcount over time"
   - "monthly headcount" / "attrition trends" / "hiring trends"
   - Time-series/trend analysis
   → Query: SELECT "MonthEnd", SUM("Headcount") FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
   
   DEFAULT RULE: If ambiguous, prefer employee_master for current headcount

2. TIME-BASED QUERIES - CRITICAL RULES:
   
   For ANY question asking about "trends", "over time", "by month", "monthly", "temporal":
   - MUST use "MonthEnd" column from headcount_attrition_summary
   - MUST GROUP BY "MonthEnd" (NOT Department) for time trends
   - MUST ORDER BY "MonthEnd" to show chronological order
   - Use SUM() for totals, AVG() for averages
   
   Examples:
   - "headcount trends over time by month" → SELECT "MonthEnd", SUM("Headcount") AS Total_Headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
   - "monthly attrition rate" → SELECT "MonthEnd", AVG("AttritionRate") AS Avg_Attrition FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
   - "hiring trends over time" → SELECT "MonthEnd", SUM("Hires") AS Total_Hires FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
   - "headcount by department over time" → SELECT "MonthEnd", "Department", SUM("Headcount") AS Headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd", "Department" ORDER BY "MonthEnd", "Department"
   
   IMPORTANT: If question mentions "time", "trend", "monthly", "over time" → ALWAYS use MonthEnd, not Department

3. QUESTION TYPES AND REQUIRED TABLES:

   Single Table (NO JOIN):
   - Basic employee info → employee_master only
   - Current headcount → employee_master only
   - Historical trends → headcount_attrition_summary only
   
   JOIN Required (use employee_master as base):
   - Salary/compensation questions → employee_master + compensation_history
   - Satisfaction/engagement → employee_master + engagement_surveys
   - Performance questions → employee_master + performance_reviews
   - Skills questions → employee_master + skills_inventory
   - Training questions → employee_master + training_records
   
   Multi-table JOINs:
   - Performance + Salary → employee_master + performance_reviews + compensation_history
   - Engagement + Performance → employee_master + engagement_surveys + performance_reviews
   - Skills + Performance → employee_master + skills_inventory + performance_reviews

3. JOIN PATTERNS:
   - employee_master."EmployeeID" = other_table."EmployeeID" (for employee-related tables)
   - headcount_attrition_summary."Department" = employee_master."Department" (for department comparison)
   - employee_master e1 JOIN employee_master e2 ON e1."ManagerID" = e2."EmployeeID" (for manager relationships)
"""

SQL_GENERATION_PROMPT = f"""
You are an expert SQL query generator for HR analytics. Your task is to convert natural language questions into accurate PostgreSQL SQL queries.

{HR_DATABASE_SCHEMA}

{TABLE_SELECTION_GUIDELINES}

Important Rules:
1. Always use the schema prefix "employees." before table names
2. Use double quotes for ALL column names (e.g., "EmployeeID", "FullName", "Department")
3. For date comparisons, use proper date functions (DATE(), EXTRACT(), etc.)
4. For aggregations, use appropriate functions (COUNT, SUM, AVG, MAX, MIN)
5. Filter out NULL values where appropriate (WHERE column IS NOT NULL)
6. For active employees, use: WHERE "Status" = 'Active' OR "TerminationDate" IS NULL
7. JOIN Rules:
   - When joining employee-related tables, use: table."EmployeeID" = employee_master."EmployeeID"
   - Use INNER JOIN for required relationships, LEFT JOIN for optional
   - For headcount_attrition_summary, join on Department: headcount_attrition_summary."Department" = employee_master."Department"
   - For self-referential (ManagerID), use: employee_master e1 JOIN employee_master e2 ON e1."ManagerID" = e2."EmployeeID"
8. Return only the SQL query, no explanations, no markdown code blocks

Conversation History:
{{conversation_history}}

User Question: {{question}}

CRITICAL: Analyze the question type first:
- Does question mention "trends", "over time", "monthly", "by month"? → Use headcount_attrition_summary with "MonthEnd" column, GROUP BY "MonthEnd", ORDER BY "MonthEnd"
- Is this asking for CURRENT headcount? → Use employee_master
- Is this asking for HISTORICAL/TREND headcount? → Use headcount_attrition_summary with "MonthEnd"
- Does this need employee details? → Start with employee_master
- Does this need salary history? → JOIN compensation_history
- Does this need performance data? → JOIN performance_reviews
- Does this need engagement data? → JOIN engagement_surveys
- Does this need skills? → JOIN skills_inventory
- Does this need training? → JOIN training_records

REMEMBER: For time-based queries, ALWAYS use "MonthEnd" column and GROUP BY "MonthEnd", not Department!

Generate a PostgreSQL SQL query to answer this question. Return ONLY the SQL query without any markdown formatting or explanations.
"""

TABLE_COLUMN_IDENTIFICATION_PROMPT = f"""
Based on the following question and SQL query, identify which tables and columns are being used.

{HR_DATABASE_SCHEMA}

Question: {{question}}
SQL Query: {{sql_query}}

Return a JSON object with:
{{
  "tables": ["table1", "table2"],
  "columns": {{
    "table1": ["column1", "column2"],
    "table2": ["column3"]
  }}
}}
"""

VISUALIZATION_RECOMMENDATION_PROMPT = """
Based on the SQL query results, recommend the best visualization type.

Query: {query}
Result Count: {result_count}
Result Columns: {columns}
Sample Data: {sample_data}

CRITICAL RULES (in priority order):
1. If query contains "distribution", "percentage", "proportion", "share" → Use PIE chart
2. If query asks "what is the distribution" or "show distribution" → Use PIE chart
3. If result has date/time column (MonthEnd, date, timestamp) AND query mentions "trends" or "over time" → Use LINE chart
4. If result has 2 columns and one is date/time → Use LINE chart
5. If result shows categories with counts (Gender, Status, Department with counts) → Use PIE chart for distribution, BAR chart for comparison
6. Bar chart for categorical comparisons when NOT asking for distribution
7. Table for detailed data with many columns (>5 columns)
8. None if single value (1 row, 1-2 columns)

DECISION TREE:
- Question asks for "distribution" → PIE chart
- Question asks for "trends over time" → LINE chart  
- Question asks for "by X" (comparison) → BAR chart
- Question asks for "list" or "show all" → TABLE
- Single value result → NONE

Return JSON:
{{
  "visualization_type": "bar|line|pie|table|scatter|none",
  "x_axis": "column_name",
  "y_axis": "column_name",
  "explanation": "why this visualization"
}}

IMPORTANT: 
- "distribution" queries → ALWAYS use "pie" chart
- "trends" or "over time" queries → ALWAYS use "line" chart
- "by department/gender/etc" comparison → Use "bar" chart
"""

INSIGHTS_GENERATION_PROMPT = """
You are an HR analytics expert. Your task is to analyze query results and provide comprehensive, data-driven insights.

Query: {query}
Results: {results}
Result Count: {result_count}

CRITICAL: You MUST analyze the actual data provided and generate REAL insights. DO NOT use generic statements like "Query executed successfully" or "Data retrieved successfully". 

Look at the actual numbers in the results and provide specific insights based on them.

You MUST provide ALL 4 sections below. Each section must contain meaningful, specific content based on the actual data.

Format your response EXACTLY as follows (copy this format exactly):

INSIGHTS:
- [Look at the results data. Find the highest value, lowest value, or interesting numbers. Write: "Category X has the highest value of Y" or "The data shows X with Y records" - USE ACTUAL NUMBERS FROM RESULTS]
- [Compare values: "Category A has X while Category B has Y" - USE ACTUAL NUMBERS]
- [Identify a key finding: "Total across all categories is X" or "Average is X" - USE ACTUAL NUMBERS]

EXPLANATION:
[Write 3-4 sentences that:
1. Explain what the query was asking
2. Describe what the data actually shows (reference specific numbers)
3. Explain what this means for HR
4. Mention any important observations

Example: "This query analyzed gender distribution across employees. The results show that [Gender X] has [number] employees, representing [percentage]% of the workforce. [Gender Y] has [number] employees. This distribution suggests [HR implication]. The presence of [number] employees with 'Unknown' gender indicates potential data quality issues that should be addressed."]

NOTABLE PATTERNS & TRENDS:
[Write 2-3 sentences identifying:
- Patterns you see in the data (which categories are highest/lowest, any skewness)
- Trends if time-series data (increasing, decreasing, stable)
- Anomalies or outliers
- Comparisons between categories

Example: "The data reveals a significant skew towards [category] with [number] employees, which is [X]% higher than [other category]. The distribution shows [pattern]. Notably, [observation about the data]."]

ACTIONABLE RECOMMENDATIONS:
- [Write a specific recommendation based on the insights. Example: "Review data collection processes for [category] to improve accuracy"]
- [Write another recommendation. Example: "Consider [action] to address [issue identified in data]"]
- [Write a third recommendation if applicable. Example: "Monitor [metric] regularly to track [trend]"]

VALIDATION CHECKLIST (before responding, verify):
✓ Did I use actual numbers from the results?
✓ Did I avoid generic statements like "Query executed successfully"?
✓ Did I provide all 4 sections?
✓ Are my insights specific and data-driven?
✓ Do my recommendations relate to the actual findings?

If results are empty, write "No data found" in each section. Otherwise, ALWAYS provide real insights based on the data.
"""


