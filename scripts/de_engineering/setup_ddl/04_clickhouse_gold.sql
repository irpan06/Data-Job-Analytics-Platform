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

-- create aggregation skill demand monthly table
CREATE TABLE IF NOT EXISTS mart_gold.agg_skill_demand_monthly(
    posted_year UInt16,
    posted_month UInt8,
    job_title_short String,
    skill String,
    total_jobs UInt64,
    updated_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (posted_year, posted_month, job_title_short, skill);