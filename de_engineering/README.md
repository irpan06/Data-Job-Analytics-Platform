# Data Engineering

## Overview
> _This section documents the complete data engineering implementation of the project, covering data preparation, warehouse design, ETL development, orchestration, and monitoring._

## Architecture
![architecture](/images/architecture.png)

The data engineering pipeline adopts the **Medallion Architecture** to progressively transform raw operational data into business-ready datasets. Raw data is first loaded into the Bronze layer, refined into analytical tables in the Silver layer, and finally aggregated into Gold data marts for reporting and analytics.


| Layer | Purpose |
|--------|---------|
| Bronze | Store raw operational data |
| Silver | Clean, standardize, and model analytical data |
| Gold | Store aggregated data marts for reporting |

## Data Modelling

![data_model](/images/data_model.png)

The Silver layer adopts a **Star Schema** to optimize analytical queries. A centralized fact table stores job posting transactions, while dimension tables provide descriptive attributes such as company, date, and skills.

This design improves query performance, simplifies analytical workloads, and provides the foundation for the Gold data marts.


## Directory Structure
The **de_engineering** module contains all components required to build the data engineering pipeline, from source data preparation to data warehouse creation and ETL execution.
```text
de_engineering
|
├── README.md
|
├── data_preparation            # Prepare source data and load it into PostgreSQL
│   ├── create_potgres.py
│   ├── download_dataset.py
│   ├── ingest_to_postgres.py
│   └── prepare_data.py
|
├── etl_dml                     # SQL transformations between Medallion layers
│   ├── aggregation_gold.sql
│   ├── load_bronze.sql
│   └── transform_silver.sql
|
├── scripts                     # Python scripts for warehouse setup and ETL execution
│   ├── build_warehouse.py
│   ├── full_pipeline.py
│   ├── reset_rebuild_wh.py
│   └── run_etl.py
|
└── setup_ddl                   # ClickHouse warehouse schema definitions
    ├── clickhouse_bronze.sql
    ├── clickhouse_gold.sql
    ├── clickhouse_reset.sql
    └── clickhouse_silver.sql
```


### Directory Description

| Directory | Description |
|----------|-------------|
| **data_preparation** | Prepares the raw dataset by downloading, splitting, creating the PostgreSQL database, and ingesting CSV files into the operational database. |
| **setup_ddl** | Contains SQL Data Definition Language (DDL) scripts used to create the ClickHouse warehouse schema, including Bronze, Silver, and Gold layers. |
| **etl_dml** | Contains SQL Data Manipulation Language (DML) scripts that implement the ETL process across the Medallion Architecture. |
| **scripts** | Provides Python entry-point scripts to build the warehouse and execute the end-to-end ETL pipeline. |
