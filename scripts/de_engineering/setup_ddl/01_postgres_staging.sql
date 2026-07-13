-- create table 
CREATE TABLE IF NOT EXISTS job_postings (
    job_title_short TEXT,
    job_title TEXT,
    job_location TEXT,
    job_via TEXT,
    job_schedule_type TEXT,
    job_work_from_home BOOLEAN,
    search_location TEXT,
    job_posted_date TIMESTAMP,
    job_no_degree_mention BOOLEAN,
    job_health_insurance BOOLEAN,
    job_country TEXT,
    salary_rate TEXT,
    salary_year_avg DOUBLE PRECISION,
    salary_hour_avg DOUBLE PRECISION,
    company_name TEXT,
    job_skills TEXT,
    job_type_skills TEXT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- create index
CREATE INDEX IF NOT EXISTS idx_job_posted_date ON job_postings(job_posted_date);