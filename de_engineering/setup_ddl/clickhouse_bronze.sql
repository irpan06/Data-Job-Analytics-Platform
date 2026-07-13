-- create database for bronze layer (CLICKHOUSE)
CREATE DATABASE IF NOT EXISTS src_bronze;

-- create table raw
CREATE TABLE IF NOT EXISTS src_bronze.raw_data(
    job_title_short String,
    job_title String,
    job_location String,
    job_via String,
    job_schedule_type String,
    job_work_from_home UInt8,
    search_location String,
    job_posted_date DateTime,
    job_no_degree_mention UInt8,
    job_health_insurance UInt8,
    job_country String,
    salary_rate String,
    salary_year_avg Nullable(Float64),
    salary_hour_avg Nullable(Float64),
    company_name String,
    job_skills String,
    job_type_skills String,
    inserted_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (toYYYYMM(job_posted_date), job_title_short);
