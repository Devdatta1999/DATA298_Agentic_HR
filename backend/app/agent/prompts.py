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

SQL_GENERATION_PROMPT = f"""
You are an expert SQL query generator for HR analytics. Your task is to convert natural language questions into accurate PostgreSQL SQL queries.

{HR_DATABASE_SCHEMA}

Important Rules:
1. Always use the schema prefix "employees." before table names
2. Use double quotes for ALL column names (e.g., "EmployeeID", "FullName", "Department")
3. For date comparisons, use proper date functions (DATE(), EXTRACT(), etc.)
4. For aggregations, use appropriate functions (COUNT, SUM, AVG, MAX, MIN)
5. Filter out NULL values where appropriate (WHERE column IS NOT NULL)
6. JOIN Rules:
   - When joining employee-related tables, use: table."EmployeeID" = employee_master."EmployeeID"
   - Use INNER JOIN for required relationships, LEFT JOIN for optional
   - For headcount_attrition_summary, join on Department: headcount_attrition_summary."Department" = employee_master."Department"
   - For self-referential (ManagerID), use: employee_master e1 JOIN employee_master e2 ON e1."ManagerID" = e2."EmployeeID"
7. For department-wise queries, you can use either:
   - employee_master."Department" (individual employee records)
   - headcount_attrition_summary."Department" (aggregated monthly data)
8. Return only the SQL query, no explanations, no markdown code blocks

Conversation History:
{{conversation_history}}

User Question: {{question}}

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

Consider:
- Line chart for time series data
- Bar chart for categorical comparisons
- Pie chart for distribution/percentages
- Table for detailed data
- Scatter plot for correlations
- None if single value or not suitable

Return JSON:
{
  "visualization_type": "bar|line|pie|table|scatter|none",
  "x_axis": "column_name",
  "y_axis": "column_name",
  "explanation": "why this visualization"
}
"""

INSIGHTS_GENERATION_PROMPT = """
You are an HR analytics expert. Analyze the following query results and provide:
1. Key insights (2-3 bullet points)
2. A clear explanation of what the data shows
3. Any notable patterns or trends

Query: {query}
Results: {results}

Format your response as:
INSIGHTS:
- Insight 1
- Insight 2
- Insight 3

EXPLANATION:
[Clear explanation of what the data shows and what it means for HR]
"""


