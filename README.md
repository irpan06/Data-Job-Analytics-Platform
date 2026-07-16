# Data Job Analytics Platform

![Architecture](images/1.png)

## Overview

> An end-to-end Data Engineering and Data Analytics project that transforms raw job posting data into a modern analytical data warehouse and provides business insights through interactive dashboards.

_The project demonstrates the complete data lifecycle, from data ingestion and warehouse development to analytical reporting and visualization._

## Objectives
- Build an end-to-end data pipeline.
- Design a dimensional data warehouse.
- Automate ETL workflows.
- Deliver analytical datasets.
- Produce business insights through dashboards.


## Sections

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
The project is divided into two major sections:
- Data Engineering focuses on building a reliable and scalable data platform.
- Data Analytics focuses on transforming curated data into actionable business insights. (under development.)


## Repository Structure
```text
Data Job Analytics Platform
│
├── airflow
│   └── airflow_home
│       ├── dags
│       └── logs
|
├── dataset
│   ├── jobs_month_01.csv
│   ├── jobs_month_02.csv
│   ├── jobs_month_03.csv
│   └──   ...
│
├── da_analytics   
│   
├── de_engineering
│   ├── data_preparation
│   ├── etl_dml
│   ├── scripts
│   └── setup_ddl
│
├── logs
│
├── README.md
│
└── requirements.txt
```