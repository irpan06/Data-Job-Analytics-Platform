-- aggregation salary by role table 
TRUNCATE TABLE mart_gold.agg_salary_by_role;

INSERT INTO mart_gold.agg_salary_by_role(
    job_title_short, total_postings, avg_salary_year, avg_salary_hour
)
SELECT
    job_title_short,
    COUNT() AS total_postings,
    AVG(salary_year_avg) AS avg_salary_year,
    AVG(salary_hour_avg) AS avg_salary_hour
FROM wh_silver.fact_job_postings
WHERE job_title_short IS NOT NULL
  AND job_title_short != ''
GROUP BY job_title_short;

-- aggregation skill demand monthly table
TRUNCATE TABLE mart_gold.agg_skill_demand_monthly;

INSERT INTO mart_gold.agg_skill_demand_monthly(
    posted_year, posted_month, job_title_short, skill, total_jobs
)
SELECT
    d.year, d.month, 
    f.job_title_short, s.skill, COUNT(DISTINCT f.job_id) AS total_jobs
FROM wh_silver.fact_job_postings f

INNER JOIN wh_silver.dim_date d
ON f.date_id = d.date_id

INNER JOIN wh_silver.bridge_skill_job b
ON f.job_id = b.job_id

INNER JOIN wh_silver.dim_skill s
ON b.skill_id = s.skill_id

WHERE job_title_short IS NOT NULL
  AND job_title_short != ''

GROUP BY
    d.year,
    d.month,
    f.job_title_short,
    skill;

-- aggregation top paying skill
TRUNCATE TABLE mart_gold.agg_top_paying_skills;

INSERT INTO mart_gold.agg_top_paying_skills(
    job_title_short, skill, avg_salary_year, total_indexed_jobs
)
SELECT
    f.job_title_short,
    s.skill,
    AVG(salary_year_avg) AS avg_salary_year,
    COUNT(DISTINCT f.job_id) AS total_indexed_jobs
FROM wh_silver.fact_job_postings f

INNER JOIN wh_silver.bridge_skill_job b
ON f.job_id = b.job_id

INNER JOIN wh_silver.dim_skill s
ON b.skill_id = s.skill_id

WHERE f.salary_year_avg IS NOT NULL 

GROUP BY
    f.job_title_short,
    s.skill;
