-- create database for silver layer (CLICKHOUSE)
CREATE DATABASE IF NOT EXISTS wh_silver;

-- create fact and dim table (star schema)
-- create a company dim table
CREATE TABLE IF NOT EXISTS wh_silver.dim_company(
    company_id Int64,
    company_name String
)
ENGINE = MergeTree()
ORDER BY company_id;

-- create skill dim table
CREATE TABLE IF NOT EXISTS wh_silver.dim_skill(
    skill_id Int64,
    skill String
)
ENGINE = MergeTree()
ORDER BY skill_id;

-- create date dim table
CREATE TABLE IF NOT EXISTS wh_silver.dim_date(
    date_id UInt32,
    full_date Date,
    day UInt8,
    month UInt8,
    quarter UInt8,
    year UInt16,
    week_of_year UInt8,
    day_of_week UInt8,
    is_weekend UInt8
)
ENGINE = MergeTree()
ORDER BY date_id;
CREATE TABLE IF NOT EXISTS wh_silver.dim_date(
    date_id UInt32,
    full_date Date,
    day UInt8,
    month UInt8,
    quarter UInt8,
    year UInt16,
    week_of_year UInt8,
    day_of_week UInt8,
    is_weekend UInt8
)
ENGINE = MergeTree()
ORDER BY date_id;

-- create job posting fact table
CREATE TABLE IF NOT EXISTS wh_silver.fact_job_postings(
    job_id Int64,
    job_hash UInt64,
    company_id Int64,
    date_id UInt32,
    job_title_short String,
    job_title String,
    job_location String,
    job_via String,
    job_schedule_type String,
    job_work_from_home UInt8,
    search_location String,
    job_no_degree_mention UInt8,
    job_health_insurance UInt8,
    job_country String,
    salary_rate String,
    salary_year_avg Nullable(Float64),
    salary_hour_avg Nullable(Float64),
    refined_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (date_id, job_title_short);

-- create brdige skill and job dim table
CREATE TABLE IF NOT EXISTS wh_silver.bridge_skill_job(
    skill_id Int64,
    job_id Int64
)
ENGINE = MergeTree()
ORDER BY (skill_id, job_id);