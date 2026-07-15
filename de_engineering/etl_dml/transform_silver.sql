-- company dim table 
WITH
    ifNull(
        (SELECT MAX(company_id) FROM wh_silver.dim_company), 0
    ) AS max_company_id

INSERT INTO wh_silver.dim_company
(
    company_id, company_name
)
SELECT
    max_company_id + row_number() OVER (ORDER BY company_name) AS company_id, 
    company_name
FROM(
    SELECT DISTINCT company_name 
    FROM src_bronze.raw_data
    WHERE company_name IS NOT NULL
      AND company_name != ''
)
WHERE company_name NOT IN (SELECT company_name FROM wh_silver.dim_company);

-- skill dim table
WITH 
    max_skill_id AS (
        SELECT ifNull(MAX(skill_id),0) AS max_id
        FROM wh_silver.dim_skill
    ),
    skills AS(
        SELECT DISTINCT
            trim(
                arrayJoin(
                    splitByChar(
                        ',',
                        replaceRegexpAll(job_skills, '[\\[\\]\']', '')
                    )
                )
            ) AS skill
        FROM src_bronze.raw_data
        WHERE job_skills IS NOT NULL
        AND job_skills != ''
        AND job_skills != '[]'
    )

INSERT INTO wh_silver.dim_skill(
    skill_id, skill
)
SELECT
    max_id + row_number() OVER (ORDER BY skill),
    skill
FROM max_skill_id, skills
WHERE skill NOT IN (SELECT skill FROM wh_silver.dim_skill);

--'
-- date dim table
INSERT INTO wh_silver.dim_date(
    date_id, full_date, day, month, quarter, year, week_of_year, day_of_week, is_weekend
)
SELECT DISTINCT
    toYYYYMMDD(job_posted_date) AS date_id,
    toDate(job_posted_date) AS full_date,
    toDayOfMonth(job_posted_date) AS day,
    toMonth(job_posted_date) AS month,
    toQuarter(job_posted_date) AS quarter,
    toYear(job_posted_date) AS year,
    toWeek(job_posted_date) AS week_of_year,
    toDayOfWeek(job_posted_date) AS day_of_week,
    if(toDayOfWeek(job_posted_date) IN (6,7),1,0) AS is_weekend
FROM src_bronze.raw_data
WHERE job_posted_date IS NOT NULL;

-- job posting fact table
WITH
    ifNull(
        (SELECT MAX(job_id) FROM wh_silver.fact_job_postings), 0
    ) AS max_job_id

INSERT INTO wh_silver.fact_job_postings(
    job_id, job_hash, company_id, date_id,
    job_title_short, job_title, job_location, job_via,
    job_schedule_type, job_work_from_home, search_location,
    job_no_degree_mention, job_health_insurance, job_country,
    salary_rate, salary_year_avg, salary_hour_avg
)
SELECT
    max_job_id + row_number() OVER (ORDER BY job_hash) AS job_id, b.job_hash, c.company_id, d.date_id,
    b.job_title_short, b.job_title, b.job_location, b.job_via,
    b.job_schedule_type, b.job_work_from_home, b.search_location,
    b.job_no_degree_mention, b.job_health_insurance, b.job_country,
    b.salary_rate, b.salary_year_avg, b.salary_hour_avg
FROM src_bronze.raw_data b
LEFT JOIN wh_silver.dim_company c 
ON b.company_name = c.company_name
LEFT JOIN wh_silver.dim_date d
ON toDate(b.job_posted_date) = d.full_date
WHERE b.job_hash NOT IN (
    SELECT job_hash
    FROM wh_silver.fact_job_postings
);

-- skill and job bridge dim table
WITH
    job_skill_pair AS(
        SELECT job_hash,
            trim(
                arrayJoin(
                    splitByChar(
                        ',',
                        replaceRegexpAll(job_skills, '[\\[\\]\']', '')
                    )
                )
            ) AS skill
        FROM src_bronze.raw_data
        WHERE job_skills IS NOT NULL
        AND job_skills != ''
        AND job_skills != '[]'
    ), --'
    lookup_skill AS(
        SELECT 
            jsp.job_hash, d.skill_id 
        FROM job_skill_pair jsp
        LEFT JOIN wh_silver.dim_skill d
        ON jsp.skill = d.skill
    )

INSERT INTO wh_silver.bridge_skill_job(
    skill_id, job_id
)
SELECT DISTINCT
    ls.skill_id, f.job_id
FROM lookup_skill ls
INNER JOIN wh_silver.fact_job_postings f
ON ls.job_hash = f.job_hash
WHERE (f.job_id, ls.skill_id) NOT IN (
    SELECT job_id, skill_id FROM wh_silver.bridge_skill_job
);