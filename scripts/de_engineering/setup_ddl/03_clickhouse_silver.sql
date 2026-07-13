-- create database for silver layer
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