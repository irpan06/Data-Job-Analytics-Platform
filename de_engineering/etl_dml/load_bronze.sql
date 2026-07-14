WITH
    sipHash64(
        concat(
            coalesce(company_name, ''),
            '|',
            coalesce(job_title, ''),
            '|',
            coalesce(job_location, ''),
            '|',
            coalesce(job_schedule_type, ''),
            '|',
            coalesce(toString(toDate(job_posted_date)), ''),
            '|',
            coalesce(job_country, '')
        )
    ) AS job_hash

INSERT INTO src_bronze.raw_data
(
    job_hash, job_title_short, job_title, job_location, job_via,
    job_schedule_type, job_work_from_home, search_location, job_posted_date,
    job_no_degree_mention, job_health_insurance, job_country, salary_rate,
    salary_year_avg, salary_hour_avg, company_name, job_skills, job_type_skills
)
SELECT
    job_hash, job_title_short, job_title, job_location, job_via,
    job_schedule_type, CAST(job_work_from_home AS UInt8), search_location, 
    job_posted_date, CAST(job_no_degree_mention AS UInt8), CAST(job_health_insurance AS UInt8), job_country,
    salary_rate, salary_year_avg, salary_hour_avg, company_name, job_skills, job_type_skills
FROM postgresql(
    '{PG_HOST}:{PG_PORT}',
    '{PG_DATABASE}',
    '{PG_TABLE}',
    '{PG_USER}',
    '{PG_PASSWORD}'
)
WHERE job_hash NOT IN (
    SELECT job_hash
    FROM src_bronze.raw_data
)