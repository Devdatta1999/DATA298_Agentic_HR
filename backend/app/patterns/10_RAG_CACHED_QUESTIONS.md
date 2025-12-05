# 10 RAG Cached Questions for Comparison Demo

This document contains 10 impactful questions that require RAG (custom HR terms) to answer correctly.

## Purpose
These questions demonstrate the improvement of the RAG-enabled agent over the base agent. The base agent cannot answer these questions correctly because they use custom HR terminology and formulas that are not in the LLM's training data.

## Questions


### 1. Show me Internal Mobility Rate

**Custom Term:** Internal Mobility Rate

**Definition:**
The percentage of employees who have changed departments internally within a specified time period. This metric measures internal career progression and organizational flexibility.

**Why RAG is Needed:**
This question uses the custom term "Internal Mobility Rate" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
SELECT e1."Department", COUNT(DISTINCT CASE WHEN e2."Department" != e1."Department" AND e2."HireDate" < e1."HireDate" THEN e2."EmployeeID" END) AS internal_transfers, COUNT(DISTINCT e1."EmployeeID") AS total_employees, ROUND((COUNT(DISTINCT CASE WHEN e2."Department" != e1."Department" AND e2."HireDate" < e1."HireDate" THEN e2."EmployeeID" END)::numeric / NULLIF(COUNT(DISTINCT e1."EmployeeID"), 0)) * 100, 2) AS mobility_rate FROM employees.employee_master e1 LEFT JOIN employees.employee_master e2 ON e1."EmployeeID" = e2."EmployeeID" WHERE e1."Status" = 'Active' GROUP BY e1."Department" ORDER BY mobility_rate DESC;
```

**Keywords to Match:** internal mobility, mobility rate, department transfer, internal transfer, career progression

---


### 2. Show me Flight Risk Score

**Custom Term:** Flight Risk Score

**Definition:**
A composite score indicating the likelihood that an employee will leave the organization. Based on engagement scores, performance ratings, and tenure patterns.

**Why RAG is Needed:**
This question uses the custom term "Flight Risk Score" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH employee_metrics AS (SELECT e."EmployeeID", e."FullName", e."Department", e."HireDate", COALESCE(AVG(es."OverallSatisfaction"), 3.0) AS avg_engagement, COALESCE(AVG(pr."OverallScore"), 3.0) AS avg_performance, EXTRACT(YEAR FROM AGE(CURRENT_DATE, e."HireDate")) AS years_tenure FROM employees.employee_master e LEFT JOIN employees.engagement_surveys es ON e."EmployeeID" = es."EmployeeID" LEFT JOIN employees.performance_reviews pr ON e."EmployeeID" = pr."EmployeeID" WHERE e."Status" = 'Active' GROUP BY e."EmployeeID", e."FullName", e."Department", e."HireDate") SELECT "EmployeeID", "FullName", "Department", avg_engagement, avg_performance, years_tenure, CASE WHEN avg_engagement < 3.0 AND avg_performance < 3.0 AND years_tenure < 2 THEN 'High Risk' WHEN avg_engagement < 3.5 OR avg_performance < 3.5 THEN 'Medium Risk' ELSE 'Low Risk' END AS flight_risk FROM employee_metrics ORDER BY CASE WHEN avg_engagement < 3.0 AND avg_performance < 3.0 AND years_tenure < 2 THEN 1 WHEN avg_engagement < 3.5 OR avg_performance < 3.5 THEN 2 ELSE 3 END;
```

**Keywords to Match:** flight risk, retention risk, attrition risk, employee retention, risk score

---


### 3. Show me Employee Lifetime Value (ELV)

**Custom Term:** Employee Lifetime Value (ELV)

**Definition:**
The total value an employee brings to the organization over their entire tenure, calculated as cumulative salary, performance contributions, and training investments.

**Why RAG is Needed:**
This question uses the custom term "Employee Lifetime Value (ELV)" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH employee_costs AS (SELECT e."EmployeeID", e."FullName", e."Department", e."Salary" AS current_salary, COALESCE(SUM(ch."NewSalary" - ch."OldSalary"), 0) AS total_raises, COALESCE(SUM(tr."Score"), 0) AS training_investment, EXTRACT(YEAR FROM AGE(COALESCE(e."TerminationDate", CURRENT_DATE), e."HireDate")) AS years_service FROM employees.employee_master e LEFT JOIN employees.compensation_history ch ON e."EmployeeID" = ch."EmployeeID" LEFT JOIN employees.training_records tr ON e."EmployeeID" = tr."EmployeeID" WHERE tr."Status" = 'Completed' GROUP BY e."EmployeeID", e."FullName", e."Department", e."Salary", e."HireDate", e."TerminationDate") SELECT "EmployeeID", "FullName", "Department", current_salary, years_service, (current_salary * years_service) + total_raises - training_investment AS employee_lifetime_value FROM employee_costs ORDER BY employee_lifetime_value DESC;
```

**Keywords to Match:** employee lifetime value, ELV, employee value, lifetime value, employee ROI

---


### 4. Show me Total Rewards

**Custom Term:** Total Rewards

**Definition:**
The comprehensive compensation package including base salary, bonuses, and estimated benefits value. This is a custom HR metric that combines multiple compensation elements.

**Why RAG is Needed:**
This question uses the custom term "Total Rewards" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH latest_compensation AS (SELECT "EmployeeID", "NewSalary", "ChangeDate", ROW_NUMBER() OVER (PARTITION BY "EmployeeID" ORDER BY "ChangeDate" DESC) AS rn FROM employees.compensation_history) SELECT e."EmployeeID", e."FullName", e."Department", e."Salary" AS base_salary, COALESCE(lc."NewSalary" - e."Salary", 0) AS latest_increase, COALESCE(AVG(pr."OverallScore") * 5000, 0) AS estimated_bonus, e."Salary" + COALESCE(lc."NewSalary" - e."Salary", 0) + COALESCE(AVG(pr."OverallScore") * 5000, 0) AS total_rewards FROM employees.employee_master e LEFT JOIN latest_compensation lc ON e."EmployeeID" = lc."EmployeeID" AND lc.rn = 1 LEFT JOIN employees.performance_reviews pr ON e."EmployeeID" = pr."EmployeeID" WHERE e."Status" = 'Active' GROUP BY e."EmployeeID", e."FullName", e."Department", e."Salary", lc."NewSalary" ORDER BY total_rewards DESC;
```

**Keywords to Match:** total rewards, compensation package, total compensation, rewards package

---


### 5. Show me Skills Gap Analysis

**Custom Term:** Skills Gap Analysis

**Definition:**
Identifies departments or roles where critical skills are missing or underrepresented compared to organizational needs.

**Why RAG is Needed:**
This question uses the custom term "Skills Gap Analysis" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH department_skills AS (SELECT e."Department", si."SkillName", COUNT(DISTINCT si."EmployeeID") AS employees_with_skill, COUNT(DISTINCT e."EmployeeID") AS total_employees FROM employees.employee_master e LEFT JOIN employees.skills_inventory si ON e."EmployeeID" = si."EmployeeID" WHERE e."Status" = 'Active' GROUP BY e."Department", si."SkillName"), skill_coverage AS (SELECT "Department", "SkillName", CASE WHEN total_employees > 0 THEN (employees_with_skill::numeric / total_employees) * 100 ELSE 0 END AS coverage_percentage FROM department_skills) SELECT "Department", "SkillName", coverage_percentage, CASE WHEN coverage_percentage < 30 THEN 'Critical Gap' WHEN coverage_percentage < 50 THEN 'Moderate Gap' ELSE 'Adequate' END AS gap_status FROM skill_coverage ORDER BY "Department", coverage_percentage ASC;
```

**Keywords to Match:** skills gap, skill gap analysis, missing skills, skill coverage, competency gap

---


### 6. Show me Engagement Trend Score

**Custom Term:** Engagement Trend Score

**Definition:**
A weighted score that measures the trend direction of employee engagement over time, giving more weight to recent surveys.

**Why RAG is Needed:**
This question uses the custom term "Engagement Trend Score" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH engagement_trends AS (SELECT "EmployeeID", "SurveyDate", "OverallSatisfaction", LAG("OverallSatisfaction") OVER (PARTITION BY "EmployeeID" ORDER BY "SurveyDate") AS previous_score, LEAD("OverallSatisfaction") OVER (PARTITION BY "EmployeeID" ORDER BY "SurveyDate") AS next_score FROM employees.engagement_surveys), trend_calculation AS (SELECT "EmployeeID", "SurveyDate", "OverallSatisfaction", CASE WHEN "OverallSatisfaction" > COALESCE(previous_score, "OverallSatisfaction") THEN 1 WHEN "OverallSatisfaction" < COALESCE(previous_score, "OverallSatisfaction") THEN -1 ELSE 0 END AS trend_direction FROM engagement_trends) SELECT e."EmployeeID", e."FullName", e."Department", AVG(tc."OverallSatisfaction") AS avg_engagement, SUM(tc.trend_direction) AS trend_score, CASE WHEN SUM(tc.trend_direction) > 0 THEN 'Improving' WHEN SUM(tc.trend_direction) < 0 THEN 'Declining' ELSE 'Stable' END AS engagement_trend FROM employees.employee_master e JOIN trend_calculation tc ON e."EmployeeID" = tc."EmployeeID" WHERE e."Status" = 'Active' GROUP BY e."EmployeeID", e."FullName", e."Department" ORDER BY trend_score DESC;
```

**Keywords to Match:** engagement trend, engagement trend score, engagement trajectory, satisfaction trend

---


### 7. Show me Training ROI by Department

**Custom Term:** Training ROI by Department

**Definition:**
Return on investment for training programs calculated as the improvement in performance scores post-training relative to training costs.

**Why RAG is Needed:**
This question uses the custom term "Training ROI by Department" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH training_performance AS (SELECT tr."EmployeeID", tr."CourseName", tr."CompletionDate", tr."Score" AS training_score, e."Department", pr."ReviewDate", pr."OverallScore", CASE WHEN pr."ReviewDate" > tr."CompletionDate" THEN 'Post-Training' ELSE 'Pre-Training' END AS period FROM employees.training_records tr JOIN employees.employee_master e ON tr."EmployeeID" = e."EmployeeID" LEFT JOIN employees.performance_reviews pr ON tr."EmployeeID" = pr."EmployeeID" WHERE tr."Status" = 'Completed'), performance_delta AS (SELECT "EmployeeID", "Department", "CourseName", AVG(CASE WHEN period = 'Post-Training' THEN "OverallScore" END) AS post_performance, AVG(CASE WHEN period = 'Pre-Training' THEN "OverallScore" END) AS pre_performance FROM training_performance GROUP BY "EmployeeID", "Department", "CourseName") SELECT "Department", "CourseName", COUNT(DISTINCT "EmployeeID") AS employees_trained, AVG(post_performance - COALESCE(pre_performance, 3.0)) AS performance_improvement, AVG((post_performance - COALESCE(pre_performance, 3.0)) * 1000 / NULLIF(training_score, 0)) AS estimated_roi FROM performance_delta GROUP BY "Department", "CourseName" ORDER BY estimated_roi DESC;
```

**Keywords to Match:** training ROI, training return on investment, training effectiveness, training impact

---


### 8. Show me Compensation Equity Ratio

**Custom Term:** Compensation Equity Ratio

**Definition:**
Measures pay equity across departments, roles, and demographics by comparing average compensation adjusted for experience and performance.

**Why RAG is Needed:**
This question uses the custom term "Compensation Equity Ratio" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH department_metrics AS (SELECT e."Department", AVG(e."Salary") AS dept_avg_salary, AVG(pr."OverallScore") AS dept_avg_performance, AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, e."HireDate"))) AS avg_tenure, COUNT(DISTINCT e."EmployeeID") AS employee_count FROM employees.employee_master e LEFT JOIN employees.performance_reviews pr ON e."EmployeeID" = pr."EmployeeID" WHERE e."Status" = 'Active' GROUP BY e."Department"), company_metrics AS (SELECT AVG("Salary") AS company_avg_salary, AVG(pr."OverallScore") AS company_avg_performance FROM employees.employee_master e LEFT JOIN employees.performance_reviews pr ON e."EmployeeID" = pr."EmployeeID" WHERE e."Status" = 'Active') SELECT dm."Department", dm.dept_avg_salary, cm.company_avg_salary, ROUND((dm.dept_avg_salary / NULLIF(cm.company_avg_salary, 0)) * 100, 2) AS equity_ratio, CASE WHEN (dm.dept_avg_salary / NULLIF(cm.company_avg_salary, 0)) < 0.9 THEN 'Below Market' WHEN (dm.dept_avg_salary / NULLIF(cm.company_avg_salary, 0)) > 1.1 THEN 'Above Market' ELSE 'Market Rate' END AS equity_status FROM department_metrics dm CROSS JOIN company_metrics cm ORDER BY equity_ratio DESC;
```

**Keywords to Match:** compensation equity, pay equity, salary equity, equity ratio, pay parity

---


### 9. Show me High Performer Retention Rate

**Custom Term:** High Performer Retention Rate

**Definition:**
The percentage of high-performing employees (top 20% by performance score) who remain with the organization over a specified period.

**Why RAG is Needed:**
This question uses the custom term "High Performer Retention Rate" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH performance_rankings AS (SELECT e."EmployeeID", e."FullName", e."Department", e."Status", AVG(pr."OverallScore") AS avg_performance, PERCENT_RANK() OVER (ORDER BY AVG(pr."OverallScore") DESC) AS performance_percentile FROM employees.employee_master e JOIN employees.performance_reviews pr ON e."EmployeeID" = pr."EmployeeID" GROUP BY e."EmployeeID", e."FullName", e."Department", e."Status"), high_performers AS (SELECT "EmployeeID", "FullName", "Department", "Status", avg_performance, CASE WHEN performance_percentile <= 0.2 THEN 'High Performer' ELSE 'Other' END AS performer_category FROM performance_rankings) SELECT "Department", COUNT(CASE WHEN performer_category = 'High Performer' AND "Status" = 'Active' THEN 1 END) AS retained_high_performers, COUNT(CASE WHEN performer_category = 'High Performer' THEN 1 END) AS total_high_performers, ROUND((COUNT(CASE WHEN performer_category = 'High Performer' AND "Status" = 'Active' THEN 1 END)::numeric / NULLIF(COUNT(CASE WHEN performer_category = 'High Performer' THEN 1 END), 0)) * 100, 2) AS retention_rate FROM high_performers WHERE performer_category = 'High Performer' GROUP BY "Department" ORDER BY retention_rate DESC;
```

**Keywords to Match:** high performer retention, top performer retention, star employee retention, talent retention

---


### 10. Show me Cross-Functional Collaboration Index

**Custom Term:** Cross-Functional Collaboration Index

**Definition:**
Measures the extent to which employees work across departments, calculated based on training participation, project assignments, and manager relationships spanning multiple departments.

**Why RAG is Needed:**
This question uses the custom term "Cross-Functional Collaboration Index" which requires specific HR domain knowledge, formulas, and SQL patterns that are not part of standard LLM training. The RAG system retrieves the correct definition, formula, and SQL example from the knowledge base.

**Expected SQL (from RAG):**
```sql
WITH cross_dept_training AS (SELECT tr."EmployeeID", e."Department" AS employee_dept, COUNT(DISTINCT e2."Department") AS training_with_depts FROM employees.training_records tr JOIN employees.employee_master e ON tr."EmployeeID" = e."EmployeeID" JOIN employees.employee_master e2 ON tr."EmployeeID" != e2."EmployeeID" AND EXISTS (SELECT 1 FROM employees.training_records tr2 WHERE tr2."EmployeeID" = e2."EmployeeID" AND tr2."CourseName" = tr."CourseName") WHERE tr."Status" = 'Completed' GROUP BY tr."EmployeeID", e."Department"), manager_cross_dept AS (SELECT e."EmployeeID", e."Department", CASE WHEN m."Department" != e."Department" THEN 1 ELSE 0 END AS cross_dept_manager FROM employees.employee_master e LEFT JOIN employees.employee_master m ON e."ManagerID" = m."EmployeeID" WHERE e."Status" = 'Active'), collaboration_scores AS (SELECT COALESCE(cdt."EmployeeID", mcd."EmployeeID") AS "EmployeeID", COALESCE(cdt.employee_dept, mcd."Department") AS "Department", COALESCE(cdt.training_with_depts, 0) AS training_collaboration, COALESCE(mcd.cross_dept_manager, 0) AS manager_collaboration, (COALESCE(cdt.training_with_depts, 0) + COALESCE(mcd.cross_dept_manager, 0)) AS collaboration_index FROM cross_dept_training cdt FULL OUTER JOIN manager_cross_dept mcd ON cdt."EmployeeID" = mcd."EmployeeID") SELECT "Department", AVG(collaboration_index) AS avg_collaboration_index, COUNT(CASE WHEN collaboration_index > 0 THEN 1 END) AS employees_collaborating, COUNT(*) AS total_employees FROM collaboration_scores GROUP BY "Department" ORDER BY avg_collaboration_index DESC;
```

**Keywords to Match:** collaboration index, cross-functional collaboration, interdepartmental collaboration, team collaboration

---

