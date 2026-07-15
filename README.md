# Data Job Analytics Platform

## Project Overview

> An end-to-end Data Engineering and Data Analytics project that transforms raw job posting data into a modern analytical data warehouse and provides business insights through interactive dashboards.

The project demonstrates the complete data lifecycle, from data ingestion and warehouse development to analytical reporting and visualization.

## Project Objectives
- Build an end-to-end data pipeline.
- Design a dimensional data warehouse.
- Automate ETL workflows.
- Deliver analytical datasets.
- Produce business insights through dashboards.

## Project Sections
The project is divided into two major sections:

- Data Engineering focuses on building a reliable and scalable data platform.
- Data Analytics focuses on transforming curated data into actionable business insights. (Currently under development.)


```text
Project

├── Data Engineering (Completed)
│   ├── Data Preparation
│   ├── Data Warehouse
│   ├── ETL Pipeline
│   ├── Airflow
│   └── Logging
│
└── Data Analytics (Soon)
    ├── Business Questions
    ├── Dashboard
    ├── Insights
    └── Recommendations
```

## Repository Structure
```text
Data Job Analytics Platform
│
├── airflow
│
├── dataset
│   ├── jobs_month_01.csv
│   ├── jobs_month_02.csv
│   ├── jobs_month_03.csv
│   ├──    ...
│
├── da_analytics   
│   
├── de_engineering
|   |
│   ├── data_preparation
│   │   ├── create_potgres.py
│   │   ├── download_dataset.py
│   │   ├── ingest_to_postgres.py
│   │   └── prepare_data.py
|   |
│   ├── etl_dml
│   │   ├── aggregation_gold.sql
│   │   ├── load_bronze.sql
│   │   └── transform_silver.sql
|   |
│   ├── scripts
│   │   ├── build_warehouse.py
│   │   ├── full_pipeline.py
│   │   ├── reset_rebuild_wh.py
│   │   └── run_etl.py
|   |
│   └── setup_ddl
│       ├── clickhouse_bronze.sql
│       ├── clickhouse_gold.sql
│       ├── clickhouse_reset.sql
│       └── clickhouse_silver.sql
│
├── logs
│
├── README.md
│
└── requirements.txt
```