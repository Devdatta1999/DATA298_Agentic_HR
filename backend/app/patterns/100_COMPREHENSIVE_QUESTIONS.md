# 100 Comprehensive HR Analytics Questions

This document contains all 100 questions from the comprehensive test dataset.

## Metadata
- **Total Questions**: 100
- **Created**: 2024-12-XX
- **Description**: Comprehensive HR Analytics Questions Dataset - All 7 Tables Coverage

## Coverage by Table
- **employee_master**: 30 questions
- **compensation_history**: 15 questions
- **engagement_surveys**: 12 questions
- **headcount_attrition_summary**: 15 questions
- **performance_reviews**: 12 questions
- **skills_inventory**: 8 questions
- **training_records**: 8 questions

## Query Types
- **single_table**: 40 questions
- **two_table_join**: 35 questions
- **three_table_join**: 15 questions
- **aggregation**: 45 questions
- **time_series**: 20 questions
- **ranking**: 15 questions
- **distribution**: 10 questions
- **comparison**: 10 questions

## Questions by Category

### Easy Questions (29))

1. **Show me department wise headcount**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the gender distribution of employees?**
   - Visualization: pie
   - Tables: employees.employee_master

1. **Show me headcount trends over time by month**
   - Visualization: line
   - Tables: employees.headcount_attrition_summary

1. **Give me Top 3 Employees with highest salary**
   - Visualization: bar
   - Tables: employees.employee_master

1. **Show me top 5 highest paid employees**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the average salary by department?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the total number of active employees?**
   - Visualization: none
   - Tables: employees.employee_master

1. **Show me employees by job title**
   - Visualization: bar
   - Tables: employees.employee_master

1. **Show me monthly hiring trends**
   - Visualization: line
   - Tables: employees.headcount_attrition_summary

1. **What skills are most common in the organization?**
   - Visualization: bar
   - Tables: employees.skills_inventory

1. **What is the total number of training courses completed?**
   - Visualization: none
   - Tables: employees.training_records

1. **Show me employees hired in the last year**
   - Visualization: table
   - Tables: employees.employee_master

1. **Show me top 10 employees with highest performance ratings**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the average manager feedback score?**
   - Visualization: none
   - Tables: employees.engagement_surveys

1. **What is the employee count by status?**
   - Visualization: pie
   - Tables: employees.employee_master

1. **Show me top 5 departments by average salary**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the average number of skills per employee?**
   - Visualization: none
   - Tables: employees.employee_master, employees.skills_inventory

1. **Show me top 3 lowest paid employees**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the average salary increase amount?**
   - Visualization: none
   - Tables: employees.compensation_history

1. **Show me department headcount comparison**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the employee distribution by job title?**
   - Visualization: pie
   - Tables: employees.employee_master

1. **What is the total compensation budget?**
   - Visualization: none
   - Tables: employees.employee_master

1. **Show me employees with performance rating above 4**
   - Visualization: table
   - Tables: employees.employee_master

1. **What is the average tenure in years?**
   - Visualization: none
   - Tables: employees.employee_master

1. **Show me top 10 departments by headcount**
   - Visualization: bar
   - Tables: employees.employee_master

1. **Show me top 5 skills in demand**
   - Visualization: bar
   - Tables: employees.skills_inventory

1. **What is the total number of active employees by department?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the total number of compensation changes this year?**
   - Visualization: none
   - Tables: employees.compensation_history

1. **What is the overall employee satisfaction score?**
   - Visualization: none
   - Tables: employees.engagement_surveys


### Medium Questions (57))

1. **Show me monthly attrition rate trends**
   - Visualization: line
   - Tables: employees.headcount_attrition_summary

1. **What is the average performance rating by department?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **Show me salary changes over time for a specific employee**
   - Visualization: line
   - Tables: employees.employee_master, employees.compensation_history

1. **What is the average salary increase percentage?**
   - Visualization: none
   - Tables: employees.compensation_history

1. **Show me employees with highest engagement scores**
   - Visualization: bar
   - Tables: employees.employee_master, employees.engagement_surveys

1. **What is the average work-life balance score by department?**
   - Visualization: bar
   - Tables: employees.employee_master, employees.engagement_surveys

1. **What is the department with highest attrition rate?**
   - Visualization: bar
   - Tables: employees.headcount_attrition_summary

1. **Show me employees with their performance review scores**
   - Visualization: table
   - Tables: employees.employee_master, employees.performance_reviews

1. **What is the average performance score by department?**
   - Visualization: bar
   - Tables: employees.employee_master, employees.performance_reviews

1. **Show me employees with most skills**
   - Visualization: bar
   - Tables: employees.employee_master, employees.skills_inventory

1. **Show me training completion rates by department**
   - Visualization: bar
   - Tables: employees.employee_master, employees.training_records

1. **What is the average tenure of employees by department?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the salary distribution by gender?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **Show me monthly termination trends**
   - Visualization: line
   - Tables: employees.headcount_attrition_summary

1. **Show me employees with salary above average**
   - Visualization: table
   - Tables: employees.employee_master

1. **What is the total compensation change amount this year?**
   - Visualization: none
   - Tables: employees.compensation_history

1. **Show me department headcount over time**
   - Visualization: line
   - Tables: employees.headcount_attrition_summary

1. **Show me employees with their latest performance review**
   - Visualization: table
   - Tables: employees.employee_master, employees.performance_reviews

1. **What is the average training score by course?**
   - Visualization: bar
   - Tables: employees.training_records

1. **Show me skill proficiency distribution**
   - Visualization: pie
   - Tables: employees.skills_inventory

1. **What is the total headcount change this month?**
   - Visualization: none
   - Tables: employees.headcount_attrition_summary

1. **Show me employees with multiple performance reviews**
   - Visualization: bar
   - Tables: employees.employee_master, employees.performance_reviews

1. **What is the employee turnover rate?**
   - Visualization: none
   - Tables: employees.employee_master

1. **Show me employees who completed training in the last 6 months**
   - Visualization: table
   - Tables: employees.employee_master, employees.training_records

1. **Show me department with highest engagement scores**
   - Visualization: bar
   - Tables: employees.employee_master, employees.engagement_surveys

1. **What is the percentage of employees with advanced skills?**
   - Visualization: none
   - Tables: employees.employee_master, employees.skills_inventory

1. **Show me monthly compensation changes**
   - Visualization: line
   - Tables: employees.compensation_history

1. **Show me employees with no performance reviews**
   - Visualization: table
   - Tables: employees.employee_master, employees.performance_reviews

1. **What is the department with most terminations?**
   - Visualization: bar
   - Tables: employees.headcount_attrition_summary

1. **Show me employees with salary increases above 10%**
   - Visualization: table
   - Tables: employees.compensation_history, employees.employee_master

1. **What is the retention rate by department?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **Show me employees with engagement scores below 3**
   - Visualization: table
   - Tables: employees.employee_master, employees.engagement_surveys

1. **What is the total training hours completed?**
   - Visualization: none
   - Tables: employees.training_records

1. **Show me employees with multiple salary changes**
   - Visualization: bar
   - Tables: employees.employee_master, employees.compensation_history

1. **What is the most common reason for salary changes?**
   - Visualization: bar
   - Tables: employees.compensation_history

1. **Show me employees with highest training scores**
   - Visualization: bar
   - Tables: employees.employee_master, employees.training_records

1. **What is the average number of training courses per employee?**
   - Visualization: none
   - Tables: employees.employee_master, employees.training_records

1. **Show me employees with no skills recorded**
   - Visualization: table
   - Tables: employees.employee_master, employees.skills_inventory

1. **What is the department with highest average engagement?**
   - Visualization: bar
   - Tables: employees.employee_master, employees.engagement_surveys

1. **Show me monthly average engagement scores**
   - Visualization: line
   - Tables: employees.engagement_surveys

1. **What is the employee count by gender and department?**
   - Visualization: table
   - Tables: employees.employee_master

1. **Show me employees with manager information**
   - Visualization: table
   - Tables: employees.employee_master

1. **Show me employees with pending training**
   - Visualization: table
   - Tables: employees.employee_master, employees.training_records

1. **What is the completion rate for each training course?**
   - Visualization: bar
   - Tables: employees.training_records

1. **Show me employees with low engagement scores**
   - Visualization: table
   - Tables: employees.employee_master, employees.engagement_surveys

1. **What is the salary range by department?**
   - Visualization: table
   - Tables: employees.employee_master

1. **Show me employees with highest number of completed trainings**
   - Visualization: bar
   - Tables: employees.employee_master, employees.training_records

1. **Show me employees with no engagement surveys**
   - Visualization: table
   - Tables: employees.employee_master, employees.engagement_surveys

1. **What is the average training score by department?**
   - Visualization: bar
   - Tables: employees.employee_master, employees.training_records

1. **Show me monthly compensation budget changes**
   - Visualization: line
   - Tables: employees.compensation_history

1. **What is the employee count by status and department?**
   - Visualization: table
   - Tables: employees.employee_master

1. **What is the department with highest average training completion?**
   - Visualization: bar
   - Tables: employees.employee_master, employees.training_records

1. **What is the average engagement score by job title?**
   - Visualization: bar
   - Tables: employees.employee_master, employees.engagement_surveys

1. **What is the department with most skills diversity?**
   - Visualization: bar
   - Tables: employees.employee_master, employees.skills_inventory

1. **Show me monthly average headcount by department**
   - Visualization: line
   - Tables: employees.headcount_attrition_summary

1. **What is the average salary by gender and department?**
   - Visualization: table
   - Tables: employees.employee_master

1. **Show me employees with manager and their performance**
   - Visualization: table
   - Tables: employees.employee_master, employees.performance_reviews


### Tricky Questions (14))

1. **What is the correlation between engagement and performance?**
   - Visualization: scatter
   - Tables: employees.employee_master, employees.engagement_surveys, employees.performance_reviews

1. **What is the average time between performance reviews?**
   - Visualization: none
   - Tables: employees.performance_reviews

1. **What is the average age of employees by department?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **Show me performance trends over time**
   - Visualization: line
   - Tables: employees.employee_master, employees.performance_reviews

1. **What is the average number of direct reports per manager?**
   - Visualization: bar
   - Tables: employees.employee_master

1. **What is the average performance score improvement over time?**
   - Visualization: none
   - Tables: employees.performance_reviews

1. **Show me departments with increasing headcount**
   - Visualization: line
   - Tables: employees.headcount_attrition_summary

1. **What is the correlation between salary and performance?**
   - Visualization: scatter
   - Tables: employees.employee_master, employees.performance_reviews

1. **What is the average time to complete training?**
   - Visualization: bar
   - Tables: employees.training_records

1. **Show me employees with declining performance**
   - Visualization: table
   - Tables: employees.performance_reviews

1. **Show me employees with all three engagement metrics above average**
   - Visualization: table
   - Tables: employees.employee_master, employees.engagement_surveys

1. **Show me employees with salary in top 10 percentile**
   - Visualization: table
   - Tables: employees.employee_master

1. **Show me employees with performance improvement**
   - Visualization: table
   - Tables: employees.performance_reviews

1. **Show me employees with highest engagement and performance scores**
   - Visualization: bar
   - Tables: employees.employee_master, employees.engagement_surveys, employees.performance_reviews


## Complete Question List with SQL


### 1. Show me department wise headcount

- **ID**: 1
- **Category**: easy
- **Pattern Type**: headcount_by_department
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY headcount DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: headcount

---


### 2. What is the gender distribution of employees?

- **ID**: 2
- **Category**: easy
- **Pattern Type**: distribution
- **Visualization**: pie
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Gender", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Gender"
```

**Visualization Details:**
- Type: pie
- X-Axis: Gender
- Y-Axis: count

---


### 3. Show me headcount trends over time by month

- **ID**: 3
- **Category**: easy
- **Pattern Type**: time_series_trend
- **Visualization**: line
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", SUM("Headcount") AS Total_Headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

**Visualization Details:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: Total_Headcount

---


### 4. Give me Top 3 Employees with highest salary

- **ID**: 4
- **Category**: easy
- **Pattern Type**: top_n_ranking
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL ORDER BY "Salary" DESC LIMIT 3
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: Salary

---


### 5. Show me top 5 highest paid employees

- **ID**: 5
- **Category**: easy
- **Pattern Type**: top_n_ranking
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL ORDER BY "Salary" DESC LIMIT 5
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: Salary

---


### 6. What is the average salary by department?

- **ID**: 6
- **Category**: easy
- **Pattern Type**: aggregation_by_group
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_salary

---


### 7. Show me monthly attrition rate trends

- **ID**: 7
- **Category**: medium
- **Pattern Type**: time_series_trend
- **Visualization**: line
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", AVG("AttritionRate") AS avg_attrition_rate FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

**Visualization Details:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: avg_attrition_rate

---


### 8. What is the total number of active employees?

- **ID**: 8
- **Category**: easy
- **Pattern Type**: single_value_count
- **Visualization**: none
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT COUNT(*) AS total_employees FROM employees.employee_master WHERE "Status" = 'Active'
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 9. Show me employees by job title

- **ID**: 9
- **Category**: easy
- **Pattern Type**: group_by_category
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "JobTitle", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "JobTitle" ORDER BY count DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: JobTitle
- Y-Axis: count

---


### 10. What is the average performance rating by department?

- **ID**: 10
- **Category**: medium
- **Pattern Type**: aggregation_by_group
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", ROUND(AVG("PerformanceRating"), 2) AS avg_rating FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" IS NOT NULL GROUP BY "Department" ORDER BY avg_rating DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_rating

---


### 11. Show me salary changes over time for a specific employee

- **ID**: 11
- **Category**: medium
- **Pattern Type**: time_series_join
- **Visualization**: line
- **Tables**: employees.employee_master, employees.compensation_history

**SQL Query:**
```sql
SELECT ch."ChangeDate", ch."OldSalary", ch."NewSalary", ch."Reason", em."FullName" FROM employees.compensation_history ch JOIN employees.employee_master em ON ch."EmployeeID" = em."EmployeeID" WHERE em."EmployeeID" = 'PNR-1001' ORDER BY ch."ChangeDate"
```

**Visualization Details:**
- Type: line
- X-Axis: ChangeDate
- Y-Axis: NewSalary

---


### 12. What is the average salary increase percentage?

- **ID**: 12
- **Category**: medium
- **Pattern Type**: calculated_metric
- **Visualization**: none
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT ROUND(AVG(((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100), 2) AS avg_increase_percent FROM employees.compensation_history ch WHERE ch."OldSalary" IS NOT NULL AND ch."NewSalary" IS NOT NULL
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 13. Show me employees with highest engagement scores

- **ID**: 13
- **Category**: medium
- **Pattern Type**: top_n_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY avg_satisfaction DESC LIMIT 10
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: avg_satisfaction

---


### 14. What is the average work-life balance score by department?

- **ID**: 14
- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(es."WorkLifeBalanceScore"), 2) AS avg_worklife_score FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_worklife_score DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_worklife_score

---


### 15. Show me monthly hiring trends

- **ID**: 15
- **Category**: easy
- **Pattern Type**: time_series_trend
- **Visualization**: line
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", SUM("Hires") AS total_hires FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

**Visualization Details:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: total_hires

---


### 16. What is the department with highest attrition rate?

- **ID**: 16
- **Category**: medium
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "Department", AVG("AttritionRate") AS avg_attrition FROM employees.headcount_attrition_summary GROUP BY "Department" ORDER BY avg_attrition DESC LIMIT 1
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_attrition

---


### 17. Show me employees with their performance review scores

- **ID**: 17
- **Category**: medium
- **Pattern Type**: join_display
- **Visualization**: table
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."FullName", em."Department", pr."ReviewDate", pr."OverallScore", pr."Communication", pr."Teamwork", pr."ProblemSolving" FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' ORDER BY pr."ReviewDate" DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 18. What is the average performance score by department?

- **ID**: 18
- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_performance DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_performance

---


### 19. Show me employees with most skills

- **ID**: 19
- **Category**: medium
- **Pattern Type**: top_n_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.skills_inventory

**SQL Query:**
```sql
SELECT em."FullName", em."Department", COUNT(si."SkillID") AS skill_count FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY skill_count DESC LIMIT 10
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: skill_count

---


### 20. What skills are most common in the organization?

- **ID**: 20
- **Category**: easy
- **Pattern Type**: group_by_category
- **Visualization**: bar
- **Tables**: employees.skills_inventory

**SQL Query:**
```sql
SELECT "SkillName", COUNT(*) AS count FROM employees.skills_inventory GROUP BY "SkillName" ORDER BY count DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: SkillName
- Y-Axis: count

---


### 21. Show me training completion rates by department

- **ID**: 21
- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."Department", COUNT(CASE WHEN tr."Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(tr."TrainingID") AS completion_rate FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: completion_rate

---


### 22. What is the total number of training courses completed?

- **ID**: 22
- **Category**: easy
- **Pattern Type**: single_value_count
- **Visualization**: none
- **Tables**: employees.training_records

**SQL Query:**
```sql
SELECT COUNT(*) AS total_completed FROM employees.training_records WHERE "Status" = 'Completed'
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 23. Show me employees hired in the last year

- **ID**: 23
- **Category**: easy
- **Pattern Type**: date_filter
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "HireDate" FROM employees.employee_master WHERE "HireDate" >= CURRENT_DATE - INTERVAL '1 year' AND "Status" = 'Active' ORDER BY "HireDate" DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 24. What is the average tenure of employees by department?

- **ID**: 24
- **Category**: medium
- **Pattern Type**: calculated_metric
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", ROUND(AVG(EXTRACT(EPOCH FROM (CURRENT_DATE - "HireDate")) / 365.25), 2) AS avg_tenure_years FROM employees.employee_master WHERE "Status" = 'Active' AND "HireDate" IS NOT NULL GROUP BY "Department" ORDER BY avg_tenure_years DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_tenure_years

---


### 25. Show me top 10 employees with highest performance ratings

- **ID**: 25
- **Category**: easy
- **Pattern Type**: top_n_ranking
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "PerformanceRating" FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" IS NOT NULL ORDER BY "PerformanceRating" DESC LIMIT 10
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: PerformanceRating

---


### 26. What is the salary distribution by gender?

- **ID**: 26
- **Category**: medium
- **Pattern Type**: distribution
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Gender", COUNT(*) AS count, ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Gender"
```

**Visualization Details:**
- Type: bar
- X-Axis: Gender
- Y-Axis: avg_salary

---


### 27. Show me monthly termination trends

- **ID**: 27
- **Category**: medium
- **Pattern Type**: time_series_trend
- **Visualization**: line
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", SUM("Terminations") AS total_terminations FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

**Visualization Details:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: total_terminations

---


### 28. What is the average manager feedback score?

- **ID**: 28
- **Category**: easy
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.engagement_surveys

**SQL Query:**
```sql
SELECT ROUND(AVG("ManagerFeedbackScore"), 2) AS avg_manager_feedback FROM employees.engagement_surveys WHERE "ManagerFeedbackScore" IS NOT NULL
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 29. Show me employees with salary above average

- **ID**: 29
- **Category**: medium
- **Pattern Type**: filter_above_average
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" > (SELECT AVG("Salary") FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL) ORDER BY "Salary" DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 30. What is the total compensation change amount this year?

- **ID**: 30
- **Category**: medium
- **Pattern Type**: date_filtered_aggregation
- **Visualization**: none
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT SUM("NewSalary" - "OldSalary") AS total_change FROM employees.compensation_history WHERE EXTRACT(YEAR FROM "ChangeDate") = EXTRACT(YEAR FROM CURRENT_DATE)
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 31. Show me department headcount over time

- **ID**: 31
- **Category**: medium
- **Pattern Type**: time_series_grouped
- **Visualization**: line
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", "Department", SUM("Headcount") AS headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd", "Department" ORDER BY "MonthEnd", "Department"
```

**Visualization Details:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: headcount

---


### 32. What is the employee count by status?

- **ID**: 32
- **Category**: easy
- **Pattern Type**: group_by_category
- **Visualization**: pie
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Status", COUNT(*) AS count FROM employees.employee_master GROUP BY "Status"
```

**Visualization Details:**
- Type: pie
- X-Axis: Status
- Y-Axis: count

---


### 33. Show me employees with their latest performance review

- **ID**: 33
- **Category**: medium
- **Pattern Type**: latest_record_join
- **Visualization**: table
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT DISTINCT ON (em."EmployeeID") em."FullName", em."Department", pr."ReviewDate", pr."OverallScore" FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' ORDER BY em."EmployeeID", pr."ReviewDate" DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 34. What is the average training score by course?

- **ID**: 34
- **Category**: medium
- **Pattern Type**: aggregation_by_group
- **Visualization**: bar
- **Tables**: employees.training_records

**SQL Query:**
```sql
SELECT "CourseName", ROUND(AVG("Score"), 2) AS avg_score FROM employees.training_records WHERE "Status" = 'Completed' AND "Score" IS NOT NULL GROUP BY "CourseName" ORDER BY avg_score DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: CourseName
- Y-Axis: avg_score

---


### 35. Show me skill proficiency distribution

- **ID**: 35
- **Category**: medium
- **Pattern Type**: distribution
- **Visualization**: pie
- **Tables**: employees.skills_inventory

**SQL Query:**
```sql
SELECT "ProficiencyLevel", COUNT(*) AS count FROM employees.skills_inventory GROUP BY "ProficiencyLevel"
```

**Visualization Details:**
- Type: pie
- X-Axis: ProficiencyLevel
- Y-Axis: count

---


### 36. What is the total headcount change this month?

- **ID**: 36
- **Category**: medium
- **Pattern Type**: monthly_comparison
- **Visualization**: none
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT SUM("Headcount") - LAG(SUM("Headcount")) OVER (ORDER BY "MonthEnd") AS headcount_change FROM employees.headcount_attrition_summary WHERE "MonthEnd" >= CURRENT_DATE - INTERVAL '2 months' GROUP BY "MonthEnd" ORDER BY "MonthEnd" DESC LIMIT 1
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 37. Show me employees with multiple performance reviews

- **ID**: 37
- **Category**: medium
- **Pattern Type**: having_clause
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."FullName", em."Department", COUNT(pr."ReviewID") AS review_count FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING COUNT(pr."ReviewID") > 1 ORDER BY review_count DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: review_count

---


### 38. What is the correlation between engagement and performance?

- **ID**: 38
- **Category**: tricky
- **Pattern Type**: correlation_analysis
- **Visualization**: scatter
- **Tables**: employees.employee_master, employees.engagement_surveys, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"
```

**Visualization Details:**
- Type: scatter
- X-Axis: avg_engagement
- Y-Axis: avg_performance

---


### 39. Show me top 5 departments by average salary

- **ID**: 39
- **Category**: easy
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC LIMIT 5
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_salary

---


### 40. What is the employee turnover rate?

- **ID**: 40
- **Category**: medium
- **Pattern Type**: calculated_metric
- **Visualization**: none
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT COUNT(CASE WHEN "Status" = 'Terminated' THEN 1 END) * 100.0 / COUNT(*) AS turnover_rate FROM employees.employee_master
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 41. Show me employees who completed training in the last 6 months

- **ID**: 41
- **Category**: medium
- **Pattern Type**: date_filter_join
- **Visualization**: table
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."FullName", em."Department", tr."CourseName", tr."CompletionDate", tr."Score" FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' AND tr."CompletionDate" >= CURRENT_DATE - INTERVAL '6 months' ORDER BY tr."CompletionDate" DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 42. What is the average time between performance reviews?

- **ID**: 42
- **Category**: tricky
- **Pattern Type**: window_function
- **Visualization**: none
- **Tables**: employees.performance_reviews

**SQL Query:**
```sql
SELECT "EmployeeID", AVG(EXTRACT(EPOCH FROM ("ReviewDate" - LAG("ReviewDate") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate"))) / 86400) AS avg_days_between_reviews FROM employees.performance_reviews GROUP BY "EmployeeID" HAVING COUNT(*) > 1
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 43. Show me department with highest engagement scores

- **ID**: 43
- **Category**: medium
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_engagement DESC LIMIT 1
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_engagement

---


### 44. What is the percentage of employees with advanced skills?

- **ID**: 44
- **Category**: medium
- **Pattern Type**: calculated_percentage
- **Visualization**: none
- **Tables**: employees.employee_master, employees.skills_inventory

**SQL Query:**
```sql
SELECT COUNT(DISTINCT CASE WHEN si."ProficiencyLevel" = 'Advanced' OR si."ProficiencyLevel" = 'Expert' THEN em."EmployeeID" END) * 100.0 / COUNT(DISTINCT em."EmployeeID") AS advanced_skill_percentage FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active'
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 45. Show me monthly compensation changes

- **ID**: 45
- **Category**: medium
- **Pattern Type**: time_series_join
- **Visualization**: line
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT DATE_TRUNC('month', "ChangeDate") AS month, COUNT(*) AS change_count, SUM("NewSalary" - "OldSalary") AS total_increase FROM employees.compensation_history GROUP BY DATE_TRUNC('month', "ChangeDate") ORDER BY month
```

**Visualization Details:**
- Type: line
- X-Axis: month
- Y-Axis: change_count

---


### 46. What is the average number of skills per employee?

- **ID**: 46
- **Category**: easy
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.employee_master, employees.skills_inventory

**SQL Query:**
```sql
SELECT ROUND(AVG(skill_count), 2) AS avg_skills_per_employee FROM (SELECT COUNT(si."SkillID") AS skill_count FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID") AS skill_counts
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 47. Show me employees with no performance reviews

- **ID**: 47
- **Category**: medium
- **Pattern Type**: left_join_null
- **Visualization**: table
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."EmployeeID", em."FullName", em."Department" FROM employees.employee_master em LEFT JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' AND pr."ReviewID" IS NULL
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 48. What is the department with most terminations?

- **ID**: 48
- **Category**: medium
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "Department", SUM("Terminations") AS total_terminations FROM employees.headcount_attrition_summary GROUP BY "Department" ORDER BY total_terminations DESC LIMIT 1
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: total_terminations

---


### 49. Show me employees with salary increases above 10%

- **ID**: 49
- **Category**: medium
- **Pattern Type**: calculated_filter
- **Visualization**: table
- **Tables**: employees.compensation_history, employees.employee_master

**SQL Query:**
```sql
SELECT em."FullName", em."Department", ch."ChangeDate", ch."OldSalary", ch."NewSalary", ROUND(((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100, 2) AS increase_percent FROM employees.compensation_history ch JOIN employees.employee_master em ON ch."EmployeeID" = em."EmployeeID" WHERE ((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100 > 10 ORDER BY increase_percent DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 50. What is the retention rate by department?

- **ID**: 50
- **Category**: medium
- **Pattern Type**: calculated_metric
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", COUNT(CASE WHEN "Status" = 'Active' THEN 1 END) * 100.0 / COUNT(*) AS retention_rate FROM employees.employee_master GROUP BY "Department"
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: retention_rate

---


### 51. Show me top 3 lowest paid employees

- **ID**: 51
- **Category**: easy
- **Pattern Type**: top_n_ranking
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL ORDER BY "Salary" ASC LIMIT 3
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: Salary

---


### 52. What is the average age of employees by department?

- **ID**: 52
- **Category**: tricky
- **Pattern Type**: calculated_metric
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", ROUND(AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM "HireDate")), 2) AS avg_years_since_hire FROM employees.employee_master WHERE "Status" = 'Active' AND "HireDate" IS NOT NULL GROUP BY "Department"
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_years_since_hire

---


### 53. Show me employees with engagement scores below 3

- **ID**: 53
- **Category**: medium
- **Pattern Type**: filter_join
- **Visualization**: table
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."FullName", em."Department", es."OverallSatisfaction" FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' AND es."OverallSatisfaction" < 3 ORDER BY es."OverallSatisfaction"
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 54. What is the total training hours completed?

- **ID**: 54
- **Category**: medium
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.training_records

**SQL Query:**
```sql
SELECT COUNT(*) AS total_training_records FROM employees.training_records WHERE "Status" = 'Completed'
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 55. Show me employees with multiple salary changes

- **ID**: 55
- **Category**: medium
- **Pattern Type**: having_clause
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.compensation_history

**SQL Query:**
```sql
SELECT em."FullName", em."Department", COUNT(ch."ChangeID") AS change_count FROM employees.employee_master em JOIN employees.compensation_history ch ON em."EmployeeID" = ch."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING COUNT(ch."ChangeID") > 1 ORDER BY change_count DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: change_count

---


### 56. What is the average salary increase amount?

- **ID**: 56
- **Category**: easy
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT ROUND(AVG("NewSalary" - "OldSalary"), 2) AS avg_increase FROM employees.compensation_history WHERE "OldSalary" IS NOT NULL AND "NewSalary" IS NOT NULL
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 57. Show me department headcount comparison

- **ID**: 57
- **Category**: easy
- **Pattern Type**: group_by_category
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY headcount DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: headcount

---


### 58. What is the employee distribution by job title?

- **ID**: 58
- **Category**: easy
- **Pattern Type**: distribution
- **Visualization**: pie
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "JobTitle", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "JobTitle" ORDER BY count DESC
```

**Visualization Details:**
- Type: pie
- X-Axis: JobTitle
- Y-Axis: count

---


### 59. Show me performance trends over time

- **ID**: 59
- **Category**: tricky
- **Pattern Type**: time_series_join
- **Visualization**: line
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT DATE_TRUNC('month', pr."ReviewDate") AS month, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY DATE_TRUNC('month', pr."ReviewDate") ORDER BY month
```

**Visualization Details:**
- Type: line
- X-Axis: month
- Y-Axis: avg_performance

---


### 60. What is the most common reason for salary changes?

- **ID**: 60
- **Category**: medium
- **Pattern Type**: group_by_category
- **Visualization**: bar
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT "Reason", COUNT(*) AS count FROM employees.compensation_history WHERE "Reason" IS NOT NULL GROUP BY "Reason" ORDER BY count DESC LIMIT 1
```

**Visualization Details:**
- Type: bar
- X-Axis: Reason
- Y-Axis: count

---


### 61. Show me employees with highest training scores

- **ID**: 61
- **Category**: medium
- **Pattern Type**: top_n_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."FullName", em."Department", AVG(tr."Score") AS avg_score FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' AND tr."Score" IS NOT NULL GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY avg_score DESC LIMIT 10
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: avg_score

---


### 62. What is the average number of training courses per employee?

- **ID**: 62
- **Category**: medium
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT ROUND(AVG(course_count), 2) AS avg_courses FROM (SELECT COUNT(tr."TrainingID") AS course_count FROM employees.employee_master em LEFT JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID") AS course_counts
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 63. Show me employees with no skills recorded

- **ID**: 63
- **Category**: medium
- **Pattern Type**: left_join_null
- **Visualization**: table
- **Tables**: employees.employee_master, employees.skills_inventory

**SQL Query:**
```sql
SELECT em."EmployeeID", em."FullName", em."Department" FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' AND si."SkillID" IS NULL
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 64. What is the department with highest average engagement?

- **ID**: 64
- **Category**: medium
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_engagement DESC LIMIT 1
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_engagement

---


### 65. Show me monthly average engagement scores

- **ID**: 65
- **Category**: medium
- **Pattern Type**: time_series_join
- **Visualization**: line
- **Tables**: employees.engagement_surveys

**SQL Query:**
```sql
SELECT DATE_TRUNC('month', "SurveyDate") AS month, ROUND(AVG("OverallSatisfaction"), 2) AS avg_satisfaction FROM employees.engagement_surveys GROUP BY DATE_TRUNC('month', "SurveyDate") ORDER BY month
```

**Visualization Details:**
- Type: line
- X-Axis: month
- Y-Axis: avg_satisfaction

---


### 66. What is the total compensation budget?

- **ID**: 66
- **Category**: easy
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT SUM("Salary") AS total_budget FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 67. Show me employees with performance rating above 4

- **ID**: 67
- **Category**: easy
- **Pattern Type**: filter
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "PerformanceRating" FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" > 4 ORDER BY "PerformanceRating" DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 68. What is the average tenure in years?

- **ID**: 68
- **Category**: easy
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (CURRENT_DATE - "HireDate")) / 365.25), 2) AS avg_tenure_years FROM employees.employee_master WHERE "Status" = 'Active' AND "HireDate" IS NOT NULL
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 69. Show me top 10 departments by headcount

- **ID**: 69
- **Category**: easy
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY headcount DESC LIMIT 10
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: headcount

---


### 70. What is the employee count by gender and department?

- **ID**: 70
- **Category**: medium
- **Pattern Type**: multi_group_by
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", "Gender", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department", "Gender" ORDER BY "Department", "Gender"
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 71. Show me employees with manager information

- **ID**: 71
- **Category**: medium
- **Pattern Type**: self_join
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT e."EmployeeID", e."FullName" AS employee_name, e."Department", m."FullName" AS manager_name FROM employees.employee_master e LEFT JOIN employees.employee_master m ON e."ManagerID" = m."EmployeeID" WHERE e."Status" = 'Active'
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 72. What is the average number of direct reports per manager?

- **ID**: 72
- **Category**: tricky
- **Pattern Type**: self_join_aggregation
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT m."FullName" AS manager_name, COUNT(e."EmployeeID") AS direct_reports FROM employees.employee_master m LEFT JOIN employees.employee_master e ON m."EmployeeID" = e."ManagerID" WHERE m."Status" = 'Active' GROUP BY m."EmployeeID", m."FullName" HAVING COUNT(e."EmployeeID") > 0 ORDER BY direct_reports DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: manager_name
- Y-Axis: direct_reports

---


### 73. Show me employees with pending training

- **ID**: 73
- **Category**: medium
- **Pattern Type**: filter_join
- **Visualization**: table
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."FullName", em."Department", tr."CourseName", tr."Status" FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'In Progress' OR tr."Status" = 'Not Started'
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 74. What is the completion rate for each training course?

- **ID**: 74
- **Category**: medium
- **Pattern Type**: calculated_percentage
- **Visualization**: bar
- **Tables**: employees.training_records

**SQL Query:**
```sql
SELECT "CourseName", COUNT(CASE WHEN "Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(*) AS completion_rate FROM employees.training_records GROUP BY "CourseName" ORDER BY completion_rate DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: CourseName
- Y-Axis: completion_rate

---


### 75. Show me employees with low engagement scores

- **ID**: 75
- **Category**: medium
- **Pattern Type**: filter_join
- **Visualization**: table
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING AVG(es."OverallSatisfaction") < 3 ORDER BY avg_satisfaction
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 76. What is the salary range by department?

- **ID**: 76
- **Category**: medium
- **Pattern Type**: range_aggregation
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", MIN("Salary") AS min_salary, MAX("Salary") AS max_salary, ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 77. Show me employees with highest number of completed trainings

- **ID**: 77
- **Category**: medium
- **Pattern Type**: top_n_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."FullName", em."Department", COUNT(tr."TrainingID") AS training_count FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY training_count DESC LIMIT 10
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: training_count

---


### 78. What is the average performance score improvement over time?

- **ID**: 78
- **Category**: tricky
- **Pattern Type**: window_function
- **Visualization**: none
- **Tables**: employees.performance_reviews

**SQL Query:**
```sql
SELECT "EmployeeID", AVG("OverallScore" - LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate")) AS avg_improvement FROM employees.performance_reviews GROUP BY "EmployeeID" HAVING COUNT(*) > 1
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 79. Show me departments with increasing headcount

- **ID**: 79
- **Category**: tricky
- **Pattern Type**: trend_analysis
- **Visualization**: line
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "Department", "MonthEnd", SUM("Headcount") AS headcount FROM employees.headcount_attrition_summary GROUP BY "Department", "MonthEnd" ORDER BY "Department", "MonthEnd"
```

**Visualization Details:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: headcount

---


### 80. What is the correlation between salary and performance?

- **ID**: 80
- **Category**: tricky
- **Pattern Type**: correlation_analysis
- **Visualization**: scatter
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(em."Salary"), 2) AS avg_salary, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' AND em."Salary" IS NOT NULL GROUP BY em."Department"
```

**Visualization Details:**
- Type: scatter
- X-Axis: avg_salary
- Y-Axis: avg_performance

---


### 81. Show me employees with no engagement surveys

- **ID**: 81
- **Category**: medium
- **Pattern Type**: left_join_null
- **Visualization**: table
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."EmployeeID", em."FullName", em."Department" FROM employees.employee_master em LEFT JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' AND es."SurveyResponseID" IS NULL
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 82. What is the average training score by department?

- **ID**: 82
- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."Department", ROUND(AVG(tr."Score"), 2) AS avg_training_score FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' AND tr."Score" IS NOT NULL GROUP BY em."Department" ORDER BY avg_training_score DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: avg_training_score

---


### 83. Show me monthly compensation budget changes

- **ID**: 83
- **Category**: medium
- **Pattern Type**: time_series_calculated
- **Visualization**: line
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT DATE_TRUNC('month', "ChangeDate") AS month, SUM("NewSalary" - "OldSalary") AS budget_change FROM employees.compensation_history GROUP BY DATE_TRUNC('month', "ChangeDate") ORDER BY month
```

**Visualization Details:**
- Type: line
- X-Axis: month
- Y-Axis: budget_change

---


### 84. What is the employee count by status and department?

- **ID**: 84
- **Category**: medium
- **Pattern Type**: multi_group_by
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", "Status", COUNT(*) AS count FROM employees.employee_master GROUP BY "Department", "Status" ORDER BY "Department", "Status"
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 85. Show me top 5 skills in demand

- **ID**: 85
- **Category**: easy
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.skills_inventory

**SQL Query:**
```sql
SELECT "SkillName", COUNT(*) AS demand_count FROM employees.skills_inventory GROUP BY "SkillName" ORDER BY demand_count DESC LIMIT 5
```

**Visualization Details:**
- Type: bar
- X-Axis: SkillName
- Y-Axis: demand_count

---


### 86. What is the average time to complete training?

- **ID**: 86
- **Category**: tricky
- **Pattern Type**: calculated_metric
- **Visualization**: bar
- **Tables**: employees.training_records

**SQL Query:**
```sql
SELECT "CourseName", AVG(EXTRACT(EPOCH FROM ("CompletionDate" - "TrainingID"::timestamp)) / 86400) AS avg_days FROM employees.training_records WHERE "Status" = 'Completed' AND "CompletionDate" IS NOT NULL GROUP BY "CourseName"
```

**Visualization Details:**
- Type: bar
- X-Axis: CourseName
- Y-Axis: avg_days

---


### 87. Show me employees with declining performance

- **ID**: 87
- **Category**: tricky
- **Pattern Type**: window_function
- **Visualization**: table
- **Tables**: employees.performance_reviews

**SQL Query:**
```sql
SELECT "EmployeeID", "ReviewDate", "OverallScore", LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate") AS previous_score FROM employees.performance_reviews WHERE "OverallScore" < LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate")
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 88. What is the department with highest average training completion?

- **ID**: 88
- **Category**: medium
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.training_records

**SQL Query:**
```sql
SELECT em."Department", COUNT(CASE WHEN tr."Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(tr."TrainingID") AS completion_rate FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY completion_rate DESC LIMIT 1
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: completion_rate

---


### 89. Show me employees with all three engagement metrics above average

- **ID**: 89
- **Category**: tricky
- **Pattern Type**: complex_filter
- **Visualization**: table
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction, AVG(es."WorkLifeBalanceScore") AS avg_worklife, AVG(es."ManagerFeedbackScore") AS avg_manager FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING AVG(es."OverallSatisfaction") > (SELECT AVG("OverallSatisfaction") FROM employees.engagement_surveys) AND AVG(es."WorkLifeBalanceScore") > (SELECT AVG("WorkLifeBalanceScore") FROM employees.engagement_surveys) AND AVG(es."ManagerFeedbackScore") > (SELECT AVG("ManagerFeedbackScore") FROM employees.engagement_surveys)
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 90. What is the total number of active employees by department?

- **ID**: 90
- **Category**: easy
- **Pattern Type**: group_by_category
- **Visualization**: bar
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", COUNT(*) AS active_count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY active_count DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: active_count

---


### 91. Show me employees with salary in top 10 percentile

- **ID**: 91
- **Category**: tricky
- **Pattern Type**: percentile_filter
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" >= (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY "Salary") FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL) ORDER BY "Salary" DESC
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 92. What is the average engagement score by job title?

- **ID**: 92
- **Category**: medium
- **Pattern Type**: aggregation_join
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.engagement_surveys

**SQL Query:**
```sql
SELECT em."JobTitle", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."JobTitle" ORDER BY avg_engagement DESC
```

**Visualization Details:**
- Type: bar
- X-Axis: JobTitle
- Y-Axis: avg_engagement

---


### 93. Show me employees with performance improvement

- **ID**: 93
- **Category**: tricky
- **Pattern Type**: window_function
- **Visualization**: table
- **Tables**: employees.performance_reviews

**SQL Query:**
```sql
SELECT "EmployeeID", "ReviewDate", "OverallScore", "OverallScore" - LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate") AS improvement FROM employees.performance_reviews WHERE "OverallScore" > LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate")
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 94. What is the department with most skills diversity?

- **ID**: 94
- **Category**: medium
- **Pattern Type**: top_n_aggregation
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.skills_inventory

**SQL Query:**
```sql
SELECT em."Department", COUNT(DISTINCT si."SkillName") AS unique_skills FROM employees.employee_master em JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY unique_skills DESC LIMIT 1
```

**Visualization Details:**
- Type: bar
- X-Axis: Department
- Y-Axis: unique_skills

---


### 95. Show me monthly average headcount by department

- **ID**: 95
- **Category**: medium
- **Pattern Type**: time_series_grouped
- **Visualization**: line
- **Tables**: employees.headcount_attrition_summary

**SQL Query:**
```sql
SELECT "MonthEnd", "Department", AVG("Headcount") AS avg_headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd", "Department" ORDER BY "MonthEnd", "Department"
```

**Visualization Details:**
- Type: line
- X-Axis: MonthEnd
- Y-Axis: avg_headcount

---


### 96. What is the average salary by gender and department?

- **ID**: 96
- **Category**: medium
- **Pattern Type**: multi_group_by
- **Visualization**: table
- **Tables**: employees.employee_master

**SQL Query:**
```sql
SELECT "Department", "Gender", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department", "Gender" ORDER BY "Department", "Gender"
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 97. Show me employees with manager and their performance

- **ID**: 97
- **Category**: medium
- **Pattern Type**: self_join_with_other
- **Visualization**: table
- **Tables**: employees.employee_master, employees.performance_reviews

**SQL Query:**
```sql
SELECT e."FullName" AS employee, e."Department", m."FullName" AS manager, pr."OverallScore" FROM employees.employee_master e LEFT JOIN employees.employee_master m ON e."ManagerID" = m."EmployeeID" LEFT JOIN employees.performance_reviews pr ON e."EmployeeID" = pr."EmployeeID" WHERE e."Status" = 'Active'
```

**Visualization Details:**
- Type: table
- X-Axis: None
- Y-Axis: None

---


### 98. What is the total number of compensation changes this year?

- **ID**: 98
- **Category**: easy
- **Pattern Type**: date_filtered_count
- **Visualization**: none
- **Tables**: employees.compensation_history

**SQL Query:**
```sql
SELECT COUNT(*) AS total_changes FROM employees.compensation_history WHERE EXTRACT(YEAR FROM "ChangeDate") = EXTRACT(YEAR FROM CURRENT_DATE)
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---


### 99. Show me employees with highest engagement and performance scores

- **ID**: 99
- **Category**: tricky
- **Pattern Type**: multi_join_top_n
- **Visualization**: bar
- **Tables**: employees.employee_master, employees.engagement_surveys, employees.performance_reviews

**SQL Query:**
```sql
SELECT em."FullName", em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY (AVG(es."OverallSatisfaction") + AVG(pr."OverallScore")) / 2 DESC LIMIT 10
```

**Visualization Details:**
- Type: bar
- X-Axis: FullName
- Y-Axis: avg_engagement

---


### 100. What is the overall employee satisfaction score?

- **ID**: 100
- **Category**: easy
- **Pattern Type**: single_value_aggregation
- **Visualization**: none
- **Tables**: employees.engagement_surveys

**SQL Query:**
```sql
SELECT ROUND(AVG("OverallSatisfaction"), 2) AS overall_satisfaction FROM employees.engagement_surveys WHERE "OverallSatisfaction" IS NOT NULL
```

**Visualization Details:**
- Type: none
- X-Axis: None
- Y-Axis: None

---

