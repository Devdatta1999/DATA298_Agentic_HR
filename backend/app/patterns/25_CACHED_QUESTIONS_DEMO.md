# 25 Cached Questions for Demo

This document contains the 25 diverse questions selected for the demo, covering all chart types.

## Chart Type Distribution
- **BAR**: 8 questions
- **TABLE**: 5 questions
- **PIE**: 3 questions
- **LINE**: 3 questions
- **SCATTER**: 2 questions
- **NONE**: 2 questions
- **AREA**: 2 questions

## Questions


### 1. What is the gender distribution of employees? ⚠️ **UNCACHED (for real-time demo)**

- **Category**: easy
- **Pattern Type**: distribution
- **Visualization**: PIE
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Gender", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Gender"
```

**Expected Visualization:**
- Type: pie
- X-Axis: Gender
- Y-Axis: count

---


### 2. Show me headcount trends over time by month

- **Category**: easy
- **Pattern Type**: time_series_trend
- **Visualization**: AREA
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", SUM("Headcount") AS Total_Headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

**Expected Visualization:**
- Type: area
- X-Axis: MonthEnd
- Y-Axis: Total_Headcount

---


### 3. Show me monthly attrition rate trends

- **Category**: medium
- **Pattern Type**: time_series_trend
- **Visualization**: AREA
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", AVG("AttritionRate") AS avg_attrition_rate FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

**Expected Visualization:**
- Type: area
- X-Axis: MonthEnd
- Y-Axis: avg_attrition_rate

---


### 4. Show me employees with highest engagement scores

- **Category**: medium
- **Pattern Type**: top_n_join
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY avg_satisfaction DESC LIMIT 10
```

**Expected Visualization:**
- Type: bar
- X-Axis: FullName
- Y-Axis: avg_satisfaction

---


### 5. What is the average work-life balance score by department?

- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(es."WorkLifeBalanceScore"), 2) AS avg_worklife_score FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_worklife_score DESC
```

**Expected Visualization:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_worklife_score

---


### 6. Show me employees with their performance review scores

- **Category**: medium
- **Pattern Type**: join_display
- **Visualization**: TABLE
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."FullName", em."Department", pr."ReviewDate", pr."OverallScore", pr."Communication", pr."Teamwork", pr."ProblemSolving" FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' ORDER BY pr."ReviewDate" DESC
```

**Expected Visualization:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 7. What is the average performance score by department?

- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_performance DESC
```

**Expected Visualization:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_performance

---


### 8. Show me employees with most skills

- **Category**: medium
- **Pattern Type**: top_n_join
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.skills_inventory

**SQL Query:**
```sql
SELECT em."FullName", em."Department", COUNT(si."SkillID") AS skill_count FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY skill_count DESC LIMIT 10
```

**Expected Visualization:**
- Type: bar
- X-Axis: FullName
- Y-Axis: skill_count

---


### 9. Show me training completion rates by department

- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."Department", COUNT(CASE WHEN tr."Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(tr."TrainingID") AS completion_rate FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"
```

**Expected Visualization:**
- Type: bar
- X-Axis: Department
- Y-Axis: completion_rate

---


### 10. Show me monthly termination trends

- **Category**: medium
- **Pattern Type**: time_series_trend
- **Visualization**: LINE
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", SUM("Terminations") AS total_terminations FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

**Expected Visualization:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: total_terminations

---


### 11. Show me department headcount over time

- **Category**: medium
- **Pattern Type**: time_series_grouped
- **Visualization**: LINE
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", "Department", SUM("Headcount") AS headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd", "Department" ORDER BY "MonthEnd", "Department"
```

**Expected Visualization:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: headcount

---


### 12. What is the employee count by status? ⚠️ **UNCACHED (for real-time demo)**

- **Category**: easy
- **Pattern Type**: group_by_category
- **Visualization**: PIE
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Status", COUNT(*) AS count FROM employees.employee_master GROUP BY "Status"
```

**Expected Visualization:**
- Type: pie
- X-Axis: Status
- Y-Axis: count

---


### 13. Show me employees with their latest performance review

- **Category**: medium
- **Pattern Type**: latest_record_join
- **Visualization**: TABLE
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT DISTINCT ON (em."EmployeeID") em."FullName", em."Department", pr."ReviewDate", pr."OverallScore" FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' ORDER BY em."EmployeeID", pr."ReviewDate" DESC
```

**Expected Visualization:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 14. Show me skill proficiency distribution

- **Category**: medium
- **Pattern Type**: distribution
- **Visualization**: PIE
- **Tables**: employees.skills_inventory

**SQL Query:**
```sql
SELECT "ProficiencyLevel", COUNT(*) AS count FROM employees.skills_inventory GROUP BY "ProficiencyLevel"
```

**Expected Visualization:**
- Type: pie
- X-Axis: ProficiencyLevel
- Y-Axis: count

---


### 15. Show me employees with multiple performance reviews

- **Category**: medium
- **Pattern Type**: having_clause
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."FullName", em."Department", COUNT(pr."ReviewID") AS review_count FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING COUNT(pr."ReviewID") > 1 ORDER BY review_count DESC
```

**Expected Visualization:**
- Type: bar
- X-Axis: FullName
- Y-Axis: review_count

---


### 16. What is the correlation between engagement and performance?

- **Category**: tricky
- **Pattern Type**: correlation_analysis
- **Visualization**: SCATTER
- **Tables**: employees.employee_master, employees.engagement_surveys, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"
```

**Expected Visualization:**
- Type: scatter
- X-Axis: avg_engagement
- Y-Axis: avg_performance

---


### 17. Show me employees who completed training in the last 6 months

- **Category**: medium
- **Pattern Type**: date_filter_join
- **Visualization**: TABLE
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."FullName", em."Department", tr."CourseName", tr."CompletionDate", tr."Score" FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' AND tr."CompletionDate" >= CURRENT_DATE - INTERVAL '6 months' ORDER BY tr."CompletionDate" DESC
```

**Expected Visualization:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 18. Show me department with highest engagement scores

- **Category**: medium
- **Pattern Type**: top_n_aggregation
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_engagement DESC LIMIT 1
```

**Expected Visualization:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_engagement

---


### 19. What is the percentage of employees with advanced skills?

- **Category**: medium
- **Pattern Type**: calculated_percentage
- **Visualization**: NONE
- **Tables**: employees.employee_master, employees.skills_inventory

**SQL Query:**
```sql
SELECT COUNT(DISTINCT CASE WHEN si."ProficiencyLevel" = 'Advanced' OR si."ProficiencyLevel" = 'Expert' THEN em."EmployeeID" END) * 100.0 / COUNT(DISTINCT em."EmployeeID") AS advanced_skill_percentage FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active'
```

**Expected Visualization:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 20. Show me monthly compensation changes

- **Category**: medium
- **Pattern Type**: time_series_join
- **Visualization**: LINE
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT DATE_TRUNC('month', "ChangeDate") AS month, COUNT(*) AS change_count, SUM("NewSalary" - "OldSalary") AS total_increase FROM employees.compensation_history GROUP BY DATE_TRUNC('month', "ChangeDate") ORDER BY month
```

**Expected Visualization:**
- Type: line
- X-Axis: month
- Y-Axis: change_count

---


### 21. Show me employees with no performance reviews

- **Category**: medium
- **Pattern Type**: left_join_null
- **Visualization**: TABLE
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."EmployeeID", em."FullName", em."Department" FROM employees.employee_master em LEFT JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' AND pr."ReviewID" IS NULL
```

**Expected Visualization:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 22. Show me employees with salary increases above 10%

- **Category**: medium
- **Pattern Type**: calculated_filter
- **Visualization**: TABLE
- **Tables**: employees.compensation_history, employees.employee_master

**SQL Query:**
```sql
SELECT em."FullName", em."Department", ch."ChangeDate", ch."OldSalary", ch."NewSalary", ROUND(((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100, 2) AS increase_percent FROM employees.compensation_history ch JOIN employees.employee_master em ON ch."EmployeeID" = em."EmployeeID" WHERE ((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100 > 10 ORDER BY increase_percent DESC
```

**Expected Visualization:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 23. Show me employees with multiple salary changes

- **Category**: medium
- **Pattern Type**: having_clause
- **Visualization**: BAR
- **Tables**: employees.employee_master, employees.compensation_history

**SQL Query:**
```sql
SELECT em."FullName", em."Department", COUNT(ch."ChangeID") AS change_count FROM employees.employee_master em JOIN employees.compensation_history ch ON em."EmployeeID" = ch."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING COUNT(ch."ChangeID") > 1 ORDER BY change_count DESC
```

**Expected Visualization:**
- Type: bar
- X-Axis: FullName
- Y-Axis: change_count

---


### 24. What is the average number of training courses per employee?

- **Category**: medium
- **Pattern Type**: single_value_aggregation
- **Visualization**: NONE
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT ROUND(AVG(course_count), 2) AS avg_courses FROM (SELECT COUNT(tr."TrainingID") AS course_count FROM employees.employee_master em LEFT JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID") AS course_counts
```

**Expected Visualization:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 25. What is the correlation between salary and performance?

- **Category**: tricky
- **Pattern Type**: correlation_analysis
- **Visualization**: SCATTER
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(em."Salary"), 2) AS avg_salary, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' AND em."Salary" IS NOT NULL GROUP BY em."Department"
```

**Expected Visualization:**
- Type: scatter
- X-Axis: avg_salary
- Y-Axis: avg_performance

---

