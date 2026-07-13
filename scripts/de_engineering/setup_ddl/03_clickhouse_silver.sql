-- create database for silver layer
CREATE DATABASE IF NOT EXISTS wh_silver;

-- create fact and dim table (star schema)
-- create a company dim table
CREATE TABLE IF NOT EXISTS wh_silver.dim_company(
    company_id UInt64,
    company_name String
)
ENGINE = MergeTree()
ORDER BY company_id;

