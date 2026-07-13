-- create database for gold layer
CREATE DATABASE IF NOT EXISTS mart_gold;

-- create aggregation salary by role table
CREATE TABLE IF NOT EXISTS mart_gold.agg_salary_by_role(
    job_title_short String,
    total_postings UInt64,
    avg_salary_year Float64,
    avg_salary_hour Float64,
    updated_at DateTIme DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY job_title_short;