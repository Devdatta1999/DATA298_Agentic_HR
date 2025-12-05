# Best 25 Questions for Demo

This document contains the 25 best questions selected from the comprehensive 100-question dataset. These questions are diverse, representative, and cover all major query types and visualizations.

## Selection Criteria

- **Diverse Visualizations:** Bar (16), Line (5), Pie (2), None (1), Scatter (1)
- **Mixed Complexity:** Easy (12), Medium (12), Tricky (1)
- **14 Unique Patterns:** Covering all major query types
- **All 7 Tables:** Comprehensive coverage

## Questions List

### Easy Questions (12)

1. **Show me department wise headcount** (Bar Chart)
   - Pattern: headcount_by_department
   - SQL: `SELECT "Department", COUNT(*) AS headcount FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Department" ORDER BY headcount DESC`

2. **What is the gender distribution of employees?** (Pie Chart)
   - Pattern: distribution
   - SQL: `SELECT "Gender", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "Gender"`

3. **Show me headcount trends over time by month** (Line Chart)
   - Pattern: time_series_trend
   - SQL: `SELECT "MonthEnd", SUM("Headcount") AS Total_Headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"`

4. **Give me Top 3 Employees with highest salary** (Bar Chart)
   - Pattern: top_n_ranking
   - SQL: `SELECT "EmployeeID", "FullName", "Department", "Salary" FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL ORDER BY "Salary" DESC LIMIT 3`

5. **What is the average salary by department?** (Bar Chart)
   - Pattern: aggregation_by_group
   - SQL: `SELECT "Department", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC`

6. **Show me monthly hiring trends** (Line Chart)
   - Pattern: time_series_trend
   - SQL: `SELECT "MonthEnd", SUM("Hires") AS total_hires FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"`

7. **What is the total number of active employees?** (None - Single Value)
   - Pattern: single_value_count
   - SQL: `SELECT COUNT(*) AS total_employees FROM employees.employee_master WHERE "Status" = 'Active'`

8. **Show me employees by job title** (Bar Chart)
   - Pattern: group_by_category
   - SQL: `SELECT "JobTitle", COUNT(*) AS count FROM employees.employee_master WHERE "Status" = 'Active' GROUP BY "JobTitle" ORDER BY count DESC`

9. **What skills are most common in the organization?** (Bar Chart)
   - Pattern: group_by_category
   - SQL: `SELECT "SkillName", COUNT(*) AS count FROM employees.skills_inventory GROUP BY "SkillName" ORDER BY count DESC`

10. **Show me top 10 employees with highest performance ratings** (Bar Chart)
    - Pattern: top_n_ranking
    - SQL: `SELECT "EmployeeID", "FullName", "Department", "PerformanceRating" FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" IS NOT NULL ORDER BY "PerformanceRating" DESC LIMIT 10`

11. **What is the employee count by status?** (Pie Chart)
    - Pattern: group_by_category
    - SQL: `SELECT "Status", COUNT(*) AS count FROM employees.employee_master GROUP BY "Status"`

12. **Show me top 5 departments by average salary** (Bar Chart)
    - Pattern: top_n_aggregation
    - SQL: `SELECT "Department", ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Department" ORDER BY avg_salary DESC LIMIT 5`

### Medium Questions (12)

13. **Show me monthly attrition rate trends** (Line Chart)
    - Pattern: time_series_trend
    - SQL: `SELECT "MonthEnd", AVG("AttritionRate") AS avg_attrition_rate FROM employees.headcount_attrition_summary GROUP BY "MonthEnd" ORDER BY "MonthEnd"`

14. **What is the average performance rating by department?** (Bar Chart)
    - Pattern: aggregation_by_group
    - SQL: `SELECT "Department", ROUND(AVG("PerformanceRating"), 2) AS avg_rating FROM employees.employee_master WHERE "Status" = 'Active' AND "PerformanceRating" IS NOT NULL GROUP BY "Department" ORDER BY avg_rating DESC`

15. **Show me employees with highest engagement scores** (Bar Chart)
    - Pattern: top_n_join
    - SQL: `SELECT em."FullName", em."Department", AVG(es."OverallSatisfaction") AS avg_satisfaction FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."EmployeeID", em."FullName", em."Department" ORDER BY avg_satisfaction DESC LIMIT 10`

16. **What is the average work-life balance score by department?** (Bar Chart)
    - Pattern: aggregation_join
    - SQL: `SELECT em."Department", ROUND(AVG(es."WorkLifeBalanceScore"), 2) AS avg_worklife_score FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_worklife_score DESC`

17. **What is the department with highest attrition rate?** (Bar Chart)
    - Pattern: top_n_aggregation
    - SQL: `SELECT "Department", AVG("AttritionRate") AS avg_attrition FROM employees.headcount_attrition_summary GROUP BY "Department" ORDER BY avg_attrition DESC LIMIT 1`

18. **What is the average performance score by department?** (Bar Chart)
    - Pattern: aggregation_join
    - SQL: `SELECT em."Department", ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_performance DESC`

19. **Show me training completion rates by department** (Bar Chart)
    - Pattern: aggregation_join
    - SQL: `SELECT em."Department", COUNT(CASE WHEN tr."Status" = 'Completed' THEN 1 END) * 100.0 / COUNT(tr."TrainingID") AS completion_rate FROM employees.employee_master em JOIN employees.training_records tr ON em."EmployeeID" = tr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"`

20. **What is the salary distribution by gender?** (Bar Chart)
    - Pattern: distribution
    - SQL: `SELECT "Gender", COUNT(*) AS count, ROUND(AVG("Salary"), 2) AS avg_salary FROM employees.employee_master WHERE "Status" = 'Active' AND "Salary" IS NOT NULL GROUP BY "Gender"`

21. **Show me department headcount over time** (Line Chart)
    - Pattern: time_series_grouped
    - SQL: `SELECT "MonthEnd", "Department", SUM("Headcount") AS headcount FROM employees.headcount_attrition_summary GROUP BY "MonthEnd", "Department" ORDER BY "MonthEnd", "Department"`

22. **Show me department with highest engagement scores** (Bar Chart)
    - Pattern: top_n_aggregation
    - SQL: `SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department" ORDER BY avg_engagement DESC LIMIT 1`

23. **What is the retention rate by department?** (Bar Chart)
    - Pattern: calculated_metric
    - SQL: `SELECT "Department", COUNT(CASE WHEN "Status" = 'Active' THEN 1 END) * 100.0 / COUNT(*) AS retention_rate FROM employees.employee_master GROUP BY "Department"`

### Complex Questions (1)

24. **Show me salary changes over time for a specific employee** (Line Chart)
    - Pattern: time_series_join
    - SQL: `SELECT ch."ChangeDate", ch."OldSalary", ch."NewSalary", ch."Reason", em."FullName" FROM employees.compensation_history ch JOIN employees.employee_master em ON ch."EmployeeID" = em."EmployeeID" WHERE em."EmployeeID" = 'PNR-1001' ORDER BY ch."ChangeDate"`

25. **What is the correlation between engagement and performance?** (Scatter Chart)
    - Pattern: correlation_analysis
    - SQL: `SELECT em."Department", ROUND(AVG(es."OverallSatisfaction"), 2) AS avg_engagement, ROUND(AVG(pr."OverallScore"), 2) AS avg_performance FROM employees.employee_master em JOIN employees.engagement_surveys es ON em."EmployeeID" = es."EmployeeID" JOIN employees.performance_reviews pr ON em."EmployeeID" = pr."EmployeeID" WHERE em."Status" = 'Active' GROUP BY em."Department"`

## Usage

After running the test script successfully, all 25 questions will have correct responses cached. You can then use these for your demo with confidence that they will:
- Return quickly (cache hits)
- Show correct SQL
- Display appropriate visualizations
- Provide accurate insights

## Test Command

```bash
cd backend
python3 test_demo_25_questions.py
```

