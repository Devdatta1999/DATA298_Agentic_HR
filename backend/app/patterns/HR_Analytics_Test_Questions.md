# HR Analytics Agent - Test Questions

**Total Questions:** 100
**Created:** 2024-12-XX

---

## EASY Questions (29)

### Q1: Show me department wise headcount

- **Pattern Type:** `headcount_by_department`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY headcount DESC
```

---

### Q2: What is the gender distribution of employees?

- **Pattern Type:** `distribution`
- **Tables:** employees.employee_master
- **Visualization:** `pie`
- **SQL:**
```sql
SELECT "Gender", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Gender"
```

---

### Q3: Show me headcount trends over time by month

- **Pattern Type:** `time_series_trend`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `line`
- **SQL:**
```sql
SELECT "MonthEnd", SUM("Headcount") AS Total_Headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

---

### Q4: Give me Top 3 Employees with highest salary

- **Pattern Type:** `top_n_ranking`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL ORDER BY "Salary" DESC LIMIT 3
```

---

### Q5: Show me top 5 highest paid employees

- **Pattern Type:** `top_n_ranking`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL ORDER BY "Salary" DESC LIMIT 5
```

---

### Q6: What is the average salary by department?

- **Pattern Type:** `aggregation_by_group`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC
```

---

### Q8: What is the total number of active employees?

- **Pattern Type:** `single_value_count`
- **Tables:** employees.employee_master
- **Visualization:** `none`
- **SQL:**
```sql
SELECT COUNT(*) AS total_employees FROM employees.employee_master WHERE "Status" = 'Active'
```

---

### Q9: Show me employees by job title

- **Pattern Type:** `group_by_category`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "JobTitle", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "JobTitle" ORDER BY count DESC
```

---

### Q15: Show me monthly hiring trends

- **Pattern Type:** `time_series_trend`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `line`
- **SQL:**
```sql
SELECT "MonthEnd", SUM("Hires") AS total_hires FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

---

### Q20: What skills are most common in the organization?

- **Pattern Type:** `group_by_category`
- **Tables:** employees.skills_inventory
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "SkillName", COUNT(*) AS count FROM employees.skills_inventory GROUP BY "SkillName" ORDER BY count DESC
```

---

### Q22: What is the total number of training courses completed?

- **Pattern Type:** `single_value_count`
- **Tables:** employees.training_records
- **Visualization:** `none`
- **SQL:**
```sql
SELECT COUNT(*) AS total_completed FROM employees.training_records WHERE "Status" = 'Completed'
```

---

### Q23: Show me employees hired in the last year

- **Pattern Type:** `date_filter`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "HireDate" FROM employees.employee_master WHERE "HireDate" >= CURRENT_DATE - INTERVAL '1 year' AND "Status" = 'Active' ORDER BY "HireDate" DESC
```

---

### Q25: Show me top 10 employees with highest performance ratings

- **Pattern Type:** `top_n_ranking`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "PerformanceRating" FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" IS NOT NULL ORDER BY "PerformanceRating" DESC LIMIT 10
```

---

### Q28: What is the average manager feedback score?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.engagement_surveys
- **Visualization:** `none`
- **SQL:**
```sql
SELECT ROUND(AVG("ManagerFeedbackScore"), 2) AS avg_manager_feedback FROM employees.engagement_surveys WHERE "ManagerFeedbackScore" IS NOT NULL
```

---

### Q32: What is the employee count by status?

- **Pattern Type:** `group_by_category`
- **Tables:** employees.employee_master
- **Visualization:** `pie`
- **SQL:**
```sql
SELECT "Status", COUNT(*) AS count FROM employees.employee_master GROUP BY "Status"
```

---

### Q39: Show me top 5 departments by average salary

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC LIMIT 5
```

---

### Q46: What is the average number of skills per employee?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.employee_master, employees.skills_inventory
- **Visualization:** `none`
- **SQL:**
```sql
SELECT ROUND(AVG(skill_count), 2) AS avg_skills_per_employee FROM (SELECT COUNT(si."SkillID") AS skill_count FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID") AS skill_counts
```

---

### Q51: Show me top 3 lowest paid employees

- **Pattern Type:** `top_n_ranking`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL ORDER BY "Salary" ASC LIMIT 3
```

---

### Q56: What is the average salary increase amount?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.compensation_history
- **Visualization:** `none`
- **SQL:**
```sql
SELECT ROUND(AVG("NewSalary" - "OldSalary"), 2) AS avg_increase FROM employees.compensation_history WHERE "OldSalary" IS NOT NULL AND "NewSalary" IS NOT NULL
```

---

### Q57: Show me department headcount comparison

- **Pattern Type:** `group_by_category`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY headcount DESC
```

---

### Q58: What is the employee distribution by job title?

- **Pattern Type:** `distribution`
- **Tables:** employees.employee_master
- **Visualization:** `pie`
- **SQL:**
```sql
SELECT "JobTitle", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "JobTitle" ORDER BY count DESC
```

---

### Q66: What is the total compensation budget?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.employee_master
- **Visualization:** `none`
- **SQL:**
```sql
SELECT SUM("Salary") AS total_budget FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL
```

---

### Q67: Show me employees with performance rating above 4

- **Pattern Type:** `filter`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "PerformanceRating" FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" > 4 ORDER BY "PerformanceRating" DESC
```

---

### Q68: What is the average tenure in years?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.employee_master
- **Visualization:** `none`
- **SQL:**
```sql
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (CURRENT_DATE - "HireDate")) / 365.25), 2) AS avg_tenure_years FROM employees.employee_master WHERE "Status" = 'Active' AND "HireDate" IS NOT NULL
```

---

### Q69: Show me top 10 departments by headcount

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY headcount DESC LIMIT 10
```

---

### Q85: Show me top 5 skills in demand

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.skills_inventory
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "SkillName", COUNT(*) AS demand_count FROM employees.skills_inventory GROUP BY "SkillName" ORDER BY demand_count DESC LIMIT 5
```

---

### Q90: What is the total number of active employees by department?

- **Pattern Type:** `group_by_category`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", COUNT(*) AS active_count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY active_count DESC
```

---

### Q98: What is the total number of compensation changes this year?

- **Pattern Type:** `date_filtered_count`
- **Tables:** employees.compensation_history
- **Visualization:** `none`
- **SQL:**
```sql
SELECT COUNT(*) AS total_changes FROM employees.compensation_history WHERE EXTRACT(YEAR FROM "ChangeDate") = EXTRACT(YEAR FROM CURRENT_DATE)
```

---

### Q100: What is the overall employee satisfaction score?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.engagement_surveys
- **Visualization:** `none`
- **SQL:**
```sql
SELECT ROUND(AVG("OverallSatisfaction"), 2) AS overall_satisfaction FROM employees.engagement_surveys WHERE "OverallSatisfaction" IS NOT NULL
```

---

## MEDIUM Questions (57)

### Q7: Show me monthly attrition rate trends

- **Pattern Type:** `time_series_trend`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `line`
- **SQL:**
```sql
SELECT "MonthEnd", AVG("AttritionRate") AS avg_attrition_rate FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

---

### Q10: What is the average performance rating by department?

- **Pattern Type:** `aggregation_by_group`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", ROUND(AVG("PerformanceRating"), 2) AS avg_rating FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" IS NOT NULL GROUP BY "Department" ORDER BY avg_rating DESC
```

---

### Q11: Show me salary changes over time for a specific employee

- **Pattern Type:** `time_series_join`
- **Tables:** employees.employee_master, employees.compensation_history
- **Visualization:** `line`
- **SQL:**
```sql
SELECT ch."ChangeDate", ch."OldSalary", ch."NewSalary", ch."Reason", em."FullName" FROM employees.compensation_history ch JOIN employees.employee_master em ON ch."EmployeeID" = em."EmployeeID" WHERE em."EmployeeID" = 'PNR-1001' ORDER BY ch."ChangeDate"
```

---

### Q12: What is the average salary increase percentage?

- **Pattern Type:** `calculated_metric`
- **Tables:** employees.compensation_history
- **Visualization:** `none`
- **SQL:**
```sql
SELECT ROUND(AVG(((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100), 2) AS avg_increase_percent FROM employees.compensation_history ch WHERE ch."OldSalary" IS NOT NULL AND ch."NewSalary" IS NOT NULL
```

---

### Q13: Show me employees with highest engagement scores

- **Pattern Type:** `top_n_join`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY avg_satisfaction DESC LIMIT 10
```

---

### Q14: What is the average work-life balance score by department?

- **Pattern Type:** `aggregation_join`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", ROUND(AVG(es."WorkLifeBalanceScore"), 2) AS avg_worklife_score FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_worklife_score DESC
```

---

### Q16: What is the department with highest attrition rate?

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", AVG("AttritionRate") AS avg_attrition FROM employees.headcount_attrition_summary GROUP BY "Department" ORDER BY avg_attrition DESC LIMIT 1
```

---

### Q17: Show me employees with their performance review scores

- **Pattern Type:** `join_display`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."FullName", em."Department", pr."ReviewDate", pr."OverallScore", pr."Communication", pr."Teamwork", pr."ProblemSolving" FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' ORDER BY pr."ReviewDate" DESC
```

---

### Q18: What is the average performance score by department?

- **Pattern Type:** `aggregation_join`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_performance DESC
```

---

### Q19: Show me employees with most skills

- **Pattern Type:** `top_n_join`
- **Tables:** employees.employee_master, employees.skills_inventory
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."FullName", em."Department", COUNT(si."SkillID") AS skill_count FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY skill_count DESC LIMIT 10
```

---

### Q21: Show me training completion rates by department

- **Pattern Type:** `aggregation_join`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", COUNT(CASE WHEN tr."Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(tr."TrainingID") AS completion_rate FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"
```

---

### Q24: What is the average tenure of employees by department?

- **Pattern Type:** `calculated_metric`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", ROUND(AVG(EXTRACT(EPOCH FROM (CURRENT_DATE - "HireDate")) / 365.25), 2) AS avg_tenure_years FROM employees.employee_master WHERE "Status" = 'Active' AND "HireDate" IS NOT NULL GROUP BY "Department" ORDER BY avg_tenure_years DESC
```

---

### Q26: What is the salary distribution by gender?

- **Pattern Type:** `distribution`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Gender", COUNT(*) AS count, ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Gender"
```

---

### Q27: Show me monthly termination trends

- **Pattern Type:** `time_series_trend`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `line`
- **SQL:**
```sql
SELECT "MonthEnd", SUM("Terminations") AS total_terminations FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"
```

---

### Q29: Show me employees with salary above average

- **Pattern Type:** `filter_above_average`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" > (SELECT AVG("Salary") FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL) ORDER BY "Salary" DESC
```

---

### Q30: What is the total compensation change amount this year?

- **Pattern Type:** `date_filtered_aggregation`
- **Tables:** employees.compensation_history
- **Visualization:** `none`
- **SQL:**
```sql
SELECT SUM("NewSalary" - "OldSalary") AS total_change FROM employees.compensation_history WHERE EXTRACT(YEAR FROM "ChangeDate") = EXTRACT(YEAR FROM CURRENT_DATE)
```

---

### Q31: Show me department headcount over time

- **Pattern Type:** `time_series_grouped`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `line`
- **SQL:**
```sql
SELECT "MonthEnd", "Department", SUM("Headcount") AS headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd", "Department" ORDER BY "MonthEnd", "Department"
```

---

### Q33: Show me employees with their latest performance review

- **Pattern Type:** `latest_record_join`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `table`
- **SQL:**
```sql
SELECT DISTINCT ON (em."EmployeeID") em."FullName", em."Department", pr."ReviewDate", pr."OverallScore" FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' ORDER BY em."EmployeeID", pr."ReviewDate" DESC
```

---

### Q34: What is the average training score by course?

- **Pattern Type:** `aggregation_by_group`
- **Tables:** employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "CourseName", ROUND(AVG("Score"), 2) AS avg_score FROM employees.training_records WHERE "Status" = 'Completed' AND "Score" IS NOT NULL GROUP BY "CourseName" ORDER BY avg_score DESC
```

---

### Q35: Show me skill proficiency distribution

- **Pattern Type:** `distribution`
- **Tables:** employees.skills_inventory
- **Visualization:** `pie`
- **SQL:**
```sql
SELECT "ProficiencyLevel", COUNT(*) AS count FROM employees.skills_inventory GROUP BY "ProficiencyLevel"
```

---

### Q36: What is the total headcount change this month?

- **Pattern Type:** `monthly_comparison`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `none`
- **SQL:**
```sql
SELECT SUM("Headcount") - LAG(SUM("Headcount")) OVER (ORDER BY "MonthEnd") AS headcount_change FROM employees.headcount_attrition_summary WHERE "MonthEnd" >= CURRENT_DATE - INTERVAL '2 months' GROUP BY "MonthEnd" ORDER BY "MonthEnd" DESC LIMIT 1
```

---

### Q37: Show me employees with multiple performance reviews

- **Pattern Type:** `having_clause`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."FullName", em."Department", COUNT(pr."ReviewID") AS review_count FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING COUNT(pr."ReviewID") > 1 ORDER BY review_count DESC
```

---

### Q40: What is the employee turnover rate?

- **Pattern Type:** `calculated_metric`
- **Tables:** employees.employee_master
- **Visualization:** `none`
- **SQL:**
```sql
SELECT COUNT(CASE WHEN "Status" = 'Terminated' THEN 1 END) * 100.0 / COUNT(*) AS turnover_rate FROM employees.employee_master
```

---

### Q41: Show me employees who completed training in the last 6 months

- **Pattern Type:** `date_filter_join`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."FullName", em."Department", tr."CourseName", tr."CompletionDate", tr."Score" FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' AND tr."CompletionDate" >= CURRENT_DATE - INTERVAL '6 months' ORDER BY tr."CompletionDate" DESC
```

---

### Q43: Show me department with highest engagement scores

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_engagement DESC LIMIT 1
```

---

### Q44: What is the percentage of employees with advanced skills?

- **Pattern Type:** `calculated_percentage`
- **Tables:** employees.employee_master, employees.skills_inventory
- **Visualization:** `none`
- **SQL:**
```sql
SELECT COUNT(DISTINCT CASE WHEN si."ProficiencyLevel" = 'Advanced' OR si."ProficiencyLevel" = 'Expert' THEN em."EmployeeID" END) * 100.0 / COUNT(DISTINCT em."EmployeeID") AS advanced_skill_percentage FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active'
```

---

### Q45: Show me monthly compensation changes

- **Pattern Type:** `time_series_join`
- **Tables:** employees.compensation_history
- **Visualization:** `line`
- **SQL:**
```sql
SELECT DATE_TRUNC('month', "ChangeDate") AS month, COUNT(*) AS change_count, SUM("NewSalary" - "OldSalary") AS total_increase FROM employees.compensation_history GROUP BY DATE_TRUNC('month', "ChangeDate") ORDER BY month
```

---

### Q47: Show me employees with no performance reviews

- **Pattern Type:** `left_join_null`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."EmployeeID", em."FullName", em."Department" FROM employees.employee_master em LEFT JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' AND pr."ReviewID" IS NULL
```

---

### Q48: What is the department with most terminations?

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", SUM("Terminations") AS total_terminations FROM employees.headcount_attrition_summary GROUP BY "Department" ORDER BY total_terminations DESC LIMIT 1
```

---

### Q49: Show me employees with salary increases above 10%

- **Pattern Type:** `calculated_filter`
- **Tables:** employees.compensation_history, employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."FullName", em."Department", ch."ChangeDate", ch."OldSalary", ch."NewSalary", ROUND(((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100, 2) AS increase_percent FROM employees.compensation_history ch JOIN employees.employee_master em ON ch."EmployeeID" = em."EmployeeID" WHERE ((ch."NewSalary" - ch."OldSalary") / NULLIF(ch."OldSalary", 0)) * 100 > 10 ORDER BY increase_percent DESC
```

---

### Q50: What is the retention rate by department?

- **Pattern Type:** `calculated_metric`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", COUNT(CASE WHEN "Status" = 'Active' THEN 1 END) * 100.0 / COUNT(*) AS retention_rate FROM employees.employee_master GROUP BY "Department"
```

---

### Q53: Show me employees with engagement scores below 3

- **Pattern Type:** `filter_join`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."FullName", em."Department", es."OverallSatisfaction" FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' AND es."OverallSatisfaction" < 3 ORDER BY es."OverallSatisfaction"
```

---

### Q54: What is the total training hours completed?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.training_records
- **Visualization:** `none`
- **SQL:**
```sql
SELECT COUNT(*) AS total_training_records FROM employees.training_records WHERE "Status" = 'Completed'
```

---

### Q55: Show me employees with multiple salary changes

- **Pattern Type:** `having_clause`
- **Tables:** employees.employee_master, employees.compensation_history
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."FullName", em."Department", COUNT(ch."ChangeID") AS change_count FROM employees.employee_master em JOIN employees.compensation_history ch ON em."EmployeeID" = ch."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING COUNT(ch."ChangeID") > 1 ORDER BY change_count DESC
```

---

### Q60: What is the most common reason for salary changes?

- **Pattern Type:** `group_by_category`
- **Tables:** employees.compensation_history
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Reason", COUNT(*) AS count FROM employees.compensation_history WHERE "Reason" IS NOT NULL GROUP BY "Reason" ORDER BY count DESC LIMIT 1
```

---

### Q61: Show me employees with highest training scores

- **Pattern Type:** `top_n_join`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."FullName", em."Department", AVG(tr."Score") AS avg_score FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' AND tr."Score" IS NOT NULL GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY avg_score DESC LIMIT 10
```

---

### Q62: What is the average number of training courses per employee?

- **Pattern Type:** `single_value_aggregation`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `none`
- **SQL:**
```sql
SELECT ROUND(AVG(course_count), 2) AS avg_courses FROM (SELECT COUNT(tr."TrainingID") AS course_count FROM employees.employee_master em LEFT JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID") AS course_counts
```

---

### Q63: Show me employees with no skills recorded

- **Pattern Type:** `left_join_null`
- **Tables:** employees.employee_master, employees.skills_inventory
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."EmployeeID", em."FullName", em."Department" FROM employees.employee_master em LEFT JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' AND si."SkillID" IS NULL
```

---

### Q64: What is the department with highest average engagement?

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_engagement DESC LIMIT 1
```

---

### Q65: Show me monthly average engagement scores

- **Pattern Type:** `time_series_join`
- **Tables:** employees.engagement_surveys
- **Visualization:** `line`
- **SQL:**
```sql
SELECT DATE_TRUNC('month', "SurveyDate") AS month, ROUND(AVG("OverallSatisfaction"), 2) AS avg_satisfaction FROM employees.engagement_surveys GROUP BY DATE_TRUNC('month', "SurveyDate") ORDER BY month
```

---

### Q70: What is the employee count by gender and department?

- **Pattern Type:** `multi_group_by`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "Department", "Gender", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department", "Gender" ORDER BY "Department", "Gender"
```

---

### Q71: Show me employees with manager information

- **Pattern Type:** `self_join`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT e."EmployeeID", e."FullName" AS employee_name, e."Department", m."FullName" AS manager_name FROM employees.employee_master e LEFT JOIN employees.employee_master m ON e."ManagerID" = m."EmployeeID" WHERE e."Status" = 'Active'
```

---

### Q73: Show me employees with pending training

- **Pattern Type:** `filter_join`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."FullName", em."Department", tr."CourseName", tr."Status" FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'In Progress' OR tr."Status" = 'Not Started'
```

---

### Q74: What is the completion rate for each training course?

- **Pattern Type:** `calculated_percentage`
- **Tables:** employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "CourseName", COUNT(CASE WHEN "Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(*) AS completion_rate FROM employees.training_records GROUP BY "CourseName" ORDER BY completion_rate DESC
```

---

### Q75: Show me employees with low engagement scores

- **Pattern Type:** `filter_join`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING AVG(es."OverallSatisfaction") < 3 ORDER BY avg_satisfaction
```

---

### Q76: What is the salary range by department?

- **Pattern Type:** `range_aggregation`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "Department", MIN("Salary") AS min_salary, MAX("Salary") AS max_salary, ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC
```

---

### Q77: Show me employees with highest number of completed trainings

- **Pattern Type:** `top_n_join`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."FullName", em."Department", COUNT(tr."TrainingID") AS training_count FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY training_count DESC LIMIT 10
```

---

### Q81: Show me employees with no engagement surveys

- **Pattern Type:** `left_join_null`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."EmployeeID", em."FullName", em."Department" FROM employees.employee_master em LEFT JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' AND es."SurveyResponseID" IS NULL
```

---

### Q82: What is the average training score by department?

- **Pattern Type:** `aggregation_join`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", ROUND(AVG(tr."Score"), 2) AS avg_training_score FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' AND tr."Score" IS NOT NULL GROUP BY em."Department" ORDER BY avg_training_score DESC
```

---

### Q83: Show me monthly compensation budget changes

- **Pattern Type:** `time_series_calculated`
- **Tables:** employees.compensation_history
- **Visualization:** `line`
- **SQL:**
```sql
SELECT DATE_TRUNC('month', "ChangeDate") AS month, SUM("NewSalary" - "OldSalary") AS budget_change FROM employees.compensation_history GROUP BY DATE_TRUNC('month', "ChangeDate") ORDER BY month
```

---

### Q84: What is the employee count by status and department?

- **Pattern Type:** `multi_group_by`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "Department", "Status", COUNT(*) AS count FROM employees.employee_master GROUP BY "Department", "Status" ORDER BY "Department", "Status"
```

---

### Q88: What is the department with highest average training completion?

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.employee_master, employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", COUNT(CASE WHEN tr."Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(tr."TrainingID") AS completion_rate FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY completion_rate DESC LIMIT 1
```

---

### Q92: What is the average engagement score by job title?

- **Pattern Type:** `aggregation_join`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."JobTitle", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."JobTitle" ORDER BY avg_engagement DESC
```

---

### Q94: What is the department with most skills diversity?

- **Pattern Type:** `top_n_aggregation`
- **Tables:** employees.employee_master, employees.skills_inventory
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."Department", COUNT(DISTINCT si."SkillName") AS unique_skills FROM employees.employee_master em JOIN employees.skills_inventory si ON em."EmployeeID" = si."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY unique_skills DESC LIMIT 1
```

---

### Q95: Show me monthly average headcount by department

- **Pattern Type:** `time_series_grouped`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `line`
- **SQL:**
```sql
SELECT "MonthEnd", "Department", AVG("Headcount") AS avg_headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd", "Department" ORDER BY "MonthEnd", "Department"
```

---

### Q96: What is the average salary by gender and department?

- **Pattern Type:** `multi_group_by`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "Department", "Gender", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department", "Gender" ORDER BY "Department", "Gender"
```

---

### Q97: Show me employees with manager and their performance

- **Pattern Type:** `self_join_with_other`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `table`
- **SQL:**
```sql
SELECT e."FullName" AS employee, e."Department", m."FullName" AS manager, pr."OverallScore" FROM employees.employee_master e LEFT JOIN employees.employee_master m ON e."ManagerID" = m."EmployeeID" LEFT JOIN employees.performance_reviews pr ON e."EmployeeID" = pr."EmployeeID" WHERE e."Status" = 'Active'
```

---

## TRICKY Questions (14)

### Q38: What is the correlation between engagement and performance?

- **Pattern Type:** `correlation_analysis`
- **Tables:** employees.employee_master, employees.engagement_surveys, employees.performance_reviews
- **Visualization:** `scatter`
- **SQL:**
```sql
SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"
```

---

### Q42: What is the average time between performance reviews?

- **Pattern Type:** `window_function`
- **Tables:** employees.performance_reviews
- **Visualization:** `none`
- **SQL:**
```sql
SELECT "EmployeeID", AVG(EXTRACT(EPOCH FROM ("ReviewDate" - LAG("ReviewDate") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate"))) / 86400) AS avg_days_between_reviews FROM employees.performance_reviews GROUP BY "EmployeeID" HAVING COUNT(*) > 1
```

---

### Q52: What is the average age of employees by department?

- **Pattern Type:** `calculated_metric`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "Department", ROUND(AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM "HireDate")), 2) AS avg_years_since_hire FROM employees.employee_master WHERE "Status" = 'Active' AND "HireDate" IS NOT NULL GROUP BY "Department"
```

---

### Q59: Show me performance trends over time

- **Pattern Type:** `time_series_join`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `line`
- **SQL:**
```sql
SELECT DATE_TRUNC('month', pr."ReviewDate") AS month, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY DATE_TRUNC('month', pr."ReviewDate") ORDER BY month
```

---

### Q72: What is the average number of direct reports per manager?

- **Pattern Type:** `self_join_aggregation`
- **Tables:** employees.employee_master
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT m."FullName" AS manager_name, COUNT(e."EmployeeID") AS direct_reports FROM employees.employee_master m LEFT JOIN employees.employee_master e ON m."EmployeeID" = e."ManagerID" WHERE m."Status" = 'Active' GROUP BY m."EmployeeID", m."FullName" HAVING COUNT(e."EmployeeID") > 0 ORDER BY direct_reports DESC
```

---

### Q78: What is the average performance score improvement over time?

- **Pattern Type:** `window_function`
- **Tables:** employees.performance_reviews
- **Visualization:** `none`
- **SQL:**
```sql
SELECT "EmployeeID", AVG("OverallScore" - LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate")) AS avg_improvement FROM employees.performance_reviews GROUP BY "EmployeeID" HAVING COUNT(*) > 1
```

---

### Q79: Show me departments with increasing headcount

- **Pattern Type:** `trend_analysis`
- **Tables:** employees.headcount_attrition_summary
- **Visualization:** `line`
- **SQL:**
```sql
SELECT "Department", "MonthEnd", SUM("Headcount") AS headcount FROM employees.headcount_attrition_summary GROUP BY "Department", "MonthEnd" ORDER BY "Department", "MonthEnd"
```

---

### Q80: What is the correlation between salary and performance?

- **Pattern Type:** `correlation_analysis`
- **Tables:** employees.employee_master, employees.performance_reviews
- **Visualization:** `scatter`
- **SQL:**
```sql
SELECT em."Department", ROUND(AVG(em."Salary"), 2) AS avg_salary, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' AND em."Salary" IS NOT NULL GROUP BY em."Department"
```

---

### Q86: What is the average time to complete training?

- **Pattern Type:** `calculated_metric`
- **Tables:** employees.training_records
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT "CourseName", AVG(EXTRACT(EPOCH FROM ("CompletionDate" - "TrainingID"::timestamp)) / 86400) AS avg_days FROM employees.training_records WHERE "Status" = 'Completed' AND "CompletionDate" IS NOT NULL GROUP BY "CourseName"
```

---

### Q87: Show me employees with declining performance

- **Pattern Type:** `window_function`
- **Tables:** employees.performance_reviews
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "EmployeeID", "ReviewDate", "OverallScore", LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate") AS previous_score FROM employees.performance_reviews WHERE "OverallScore" < LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate")
```

---

### Q89: Show me employees with all three engagement metrics above average

- **Pattern Type:** `complex_filter`
- **Tables:** employees.employee_master, employees.engagement_surveys
- **Visualization:** `table`
- **SQL:**
```sql
SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction, AVG(es."WorkLifeBalanceScore") AS avg_worklife, AVG(es."ManagerFeedbackScore") AS avg_manager FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" HAVING AVG(es."OverallSatisfaction") > (SELECT AVG("OverallSatisfaction") FROM employees.engagement_surveys) AND AVG(es."WorkLifeBalanceScore") > (SELECT AVG("WorkLifeBalanceScore") FROM employees.engagement_surveys) AND AVG(es."ManagerFeedbackScore") > (SELECT AVG("ManagerFeedbackScore") FROM employees.engagement_surveys)
```

---

### Q91: Show me employees with salary in top 10 percentile

- **Pattern Type:** `percentile_filter`
- **Tables:** employees.employee_master
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" >= (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY "Salary") FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL) ORDER BY "Salary" DESC
```

---

### Q93: Show me employees with performance improvement

- **Pattern Type:** `window_function`
- **Tables:** employees.performance_reviews
- **Visualization:** `table`
- **SQL:**
```sql
SELECT "EmployeeID", "ReviewDate", "OverallScore", "OverallScore" - LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate") AS improvement FROM employees.performance_reviews WHERE "OverallScore" > LAG("OverallScore") OVER (PARTITION BY "EmployeeID" ORDER BY "ReviewDate")
```

---

### Q99: Show me employees with highest engagement and performance scores

- **Pattern Type:** `multi_join_top_n`
- **Tables:** employees.employee_master, employees.engagement_surveys, employees.performance_reviews
- **Visualization:** `bar`
- **SQL:**
```sql
SELECT em."FullName", em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY (AVG(es."OverallSatisfaction") + AVG(pr."OverallScore")) / 2 DESC LIMIT 10
```

---

## Summary by Pattern Type

| Pattern Type | Count |
|--------------|-------|
| top_n_aggregation | 9 |
| single_value_aggregation | 8 |
| group_by_category | 6 |
| calculated_metric | 6 |
| aggregation_join | 5 |
| distribution | 4 |
| time_series_trend | 4 |
| top_n_ranking | 4 |
| time_series_join | 4 |
| top_n_join | 4 |
| window_function | 4 |
| aggregation_by_group | 3 |
| left_join_null | 3 |
| filter_join | 3 |
| multi_group_by | 3 |
| single_value_count | 2 |
| time_series_grouped | 2 |
| having_clause | 2 |
| correlation_analysis | 2 |
| calculated_percentage | 2 |
| headcount_by_department | 1 |
| join_display | 1 |
| date_filter | 1 |
| filter_above_average | 1 |
| date_filtered_aggregation | 1 |
| latest_record_join | 1 |
| monthly_comparison | 1 |
| date_filter_join | 1 |
| calculated_filter | 1 |
| filter | 1 |
| self_join | 1 |
| self_join_aggregation | 1 |
| range_aggregation | 1 |
| trend_analysis | 1 |
| time_series_calculated | 1 |
| complex_filter | 1 |
| percentile_filter | 1 |
| self_join_with_other | 1 |
| date_filtered_count | 1 |
| multi_join_top_n | 1 |
