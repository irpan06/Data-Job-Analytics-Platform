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
    WHERE company_name IS NOT NULL AND company_name != ''
)
WHERE company_name NOT IN (SELECT company_name FROM wh_silver.dim_company);