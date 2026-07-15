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
GROUP BY job_title_short;