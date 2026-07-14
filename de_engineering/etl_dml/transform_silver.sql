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