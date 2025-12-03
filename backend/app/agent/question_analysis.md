# Question Type Analysis for HR Analytics

## Question Categories by Table

### 1. employee_master (Single Table Questions)
**Question Types:**
- Current headcount by department
- Employee list by department/job title/gender
- Active vs inactive employees
- Salary statistics (avg, min, max) by department
- Employee demographics (gender distribution)
- Tenure analysis (based on HireDate)
- Manager-employee relationships

**Example Questions:**
- "Show me department wise headcount" → COUNT(*) GROUP BY Department
- "List all employees in Sales department"
- "What is the average salary by department?"
- "Show gender distribution"
- "How many active employees do we have?"

**JOIN Required:** NO (single table)

---

### 2. headcount_attrition_summary (Single Table Questions)
**Question Types:**
- Historical headcount trends over time
- Monthly attrition rates by department
- Hiring trends (Hires column)
- Termination trends (Terminations column)
- Attrition rate analysis

**Example Questions:**
- "Show headcount trends over time"
- "What is the monthly attrition rate by department?"
- "Show hiring trends by month"
- "Which department has highest attrition?"

**JOIN Required:** NO (single table, but can join with employee_master on Department for enrichment)

**IMPORTANT:** Use this for HISTORICAL/TREND analysis, NOT for current headcount

---

### 3. employee_master + compensation_history (JOIN Required)
**Question Types:**
- Salary change history for employees
- Employees who got raises
- Salary increase trends
- Compensation changes by department
- Salary change reasons

**Example Questions:**
- "Show salary change history for employee X"
- "Which employees got salary increases this year?"
- "What is the average salary increase by department?"
- "Show compensation trends"

**JOIN:** employee_master."EmployeeID" = compensation_history."EmployeeID"

---

### 4. employee_master + engagement_surveys (JOIN Required)
**Question Types:**
- Employee satisfaction by department
- Satisfaction trends over time
- Work-life balance scores
- Manager feedback scores
- Engagement by demographics

**Example Questions:**
- "Show employee satisfaction by department"
- "What is the average satisfaction score?"
- "Which department has highest engagement?"
- "Show satisfaction trends over time"

**JOIN:** employee_master."EmployeeID" = engagement_surveys."EmployeeID"

---

### 5. employee_master + performance_reviews (JOIN Required)
**Question Types:**
- Performance scores by employee/department
- Performance trends
- Communication/Teamwork/ProblemSolving scores
- High performers
- Performance by department

**Example Questions:**
- "Show performance scores by department"
- "Which employees have highest performance ratings?"
- "What is average performance score?"
- "Show performance trends"

**JOIN:** employee_master."EmployeeID" = performance_reviews."EmployeeID"

---

### 6. employee_master + skills_inventory (JOIN Required)
**Question Types:**
- Skills by employee
- Skills distribution
- Skill proficiency levels
- Employees with specific skills
- Skills by department

**Example Questions:**
- "What skills does employee X have?"
- "Show skills distribution"
- "Which employees have Python skills?"
- "Show skills by department"

**JOIN:** employee_master."EmployeeID" = skills_inventory."EmployeeID"

**Note:** One employee can have multiple skills, so may need aggregation

---

### 7. employee_master + training_records (JOIN Required)
**Question Types:**
- Training completion by employee
- Training status
- Training scores
- Training by department
- Training trends

**Example Questions:**
- "Show training completion by employee"
- "Which employees completed training X?"
- "What is the average training score?"
- "Show training status by department"

**JOIN:** employee_master."EmployeeID" = training_records."EmployeeID"

**Note:** One employee can have multiple training records

---

### 8. Multi-table JOINs (Complex Questions)
**Question Types:**
- Performance + Salary correlation
- Engagement + Performance correlation
- Training + Performance correlation
- Skills + Performance correlation
- Comprehensive employee profiles

**Example Questions:**
- "Show employees with high performance and high salary"
- "Which employees have completed training and have high performance?"
- "Show engagement vs performance correlation"
- "Employees with Python skills and their performance scores"

**JOIN:** Multiple tables joined via employee_master

---

### 9. headcount_attrition_summary + employee_master (JOIN on Department)
**Question Types:**
- Compare historical headcount with current headcount
- Attrition trends vs current employee status
- Department analysis combining both

**Example Questions:**
- "Compare current headcount with historical average"
- "Show department headcount trends vs current status"

**JOIN:** headcount_attrition_summary."Department" = employee_master."Department"

---

## Critical Decision Rules

### When to use employee_master vs headcount_attrition_summary for headcount:

1. **Use employee_master** when question asks for:
   - "current headcount"
   - "department wise headcount" (default interpretation)
   - "show me headcount" (without "historical" or "trends")
   - "how many employees"
   - Real-time/current state queries

2. **Use headcount_attrition_summary** when question asks for:
   - "historical headcount"
   - "headcount trends"
   - "headcount over time"
   - "monthly headcount"
   - "attrition trends"
   - Time-series/trend analysis

3. **Default Rule:** If ambiguous, prefer employee_master for current headcount

