# Data Engineering

## Overview
> _This section documents the complete data engineering implementation of the project, covering data preparation, warehouse design, ETL development, orchestration, and monitoring._


> **TL;DR for Engineering Reviewers:**
> * **Decoupled Architecture:** Staged raw CSVs in **PostgreSQL (OLTP)** and modeled analytics in **ClickHouse (OLAP)**.
> * **Medallion & Star Schema:** Implemented Bronze ➔ Silver ➔ Gold layers with a dedicated **Bridge Table** for many-to-many skill relationships.
> * **Production Ready:** Optimized with 64-bit integer hashing (`job_hash`), dual-channel Python logging, and automated **Apache Airflow** orchestration.

**Note:** This document details the **Data Engineering** module of the [End-to-End Data Job Analytics Platform](../README.md).

## Dataset & Acknowledgments

This project utilizes a comprehensive job posting dataset originally scraped and curated by **Luke Barousse** for his [Data Engineering course](https://github.com/lukebarousse/SQL_Data_Engineering_Course). 

While the foundational dataset and core Star Schema modeling concept (Fact, Company Dim, Skill Dim, and Bridge Table) were adapted from his tutorial, **the overall data architecture and ETL pipeline have been significantly extended and re-engineered for OLAP performance and production readiness.**

### Key Engineering Extensions & Modifications
To elevate the project from a local tutorial implementation to a production-grade data platform, several key enhancements were introduced:
* **Engine Migration (DuckDB ➔ ClickHouse):** Replaced file-based local storage with **ClickHouse**, a high-performance columnar OLAP data warehouse.
* **Medallion Architecture:** Expanded the direct transformation into a layered data pipeline (Bronze ➔ Silver ➔ Gold) with pre-aggregated business data marts.
* **Schema & Deduplication Enhancement:** Introduced a calendar dimension (`dim_date`) for time-series analytics and implemented a 64-bit integer hash (`job_hash`) in the Bronze layer for high-speed deduplication.
* **Production Orchestration & Observability:** Integrated dual-channel Python logging, automated row-count validation, and workflow orchestration via **Apache Airflow**.

> 🙏 **Credit:** Special thanks to [Luke Barousse](https://www.youtube.com/@LukeBarousse) for making the raw dataset publicly available to the data community.


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

## Key Technical Decisions & Engineering Highlights

To ensure optimal query performance, data integrity, and pipeline reliability, several production-grade engineering practices were implemented:

* **Decoupled OLTP & OLAP Architecture:** Established a strict architectural boundary by utilizing **PostgreSQL** purely as a reliable operational staging area for raw CSV ingestion, and **ClickHouse** as the high-performance columnar analytical warehouse. This isolates write-heavy operational workloads from read-heavy analytical dashboards.
* **High-Speed OLAP Deduplication & Sorting:** Because scraped datasets lack reliable primary keys, a 64-bit unsigned integer hash (`job_hash` - `UInt64`) is generated in the Bronze layer for instant, memory-efficient deduplication. Furthermore, ClickHouse tables leverage `MergeTree` engines with query-driven sorting keys (e.g., `ORDER BY (job_title_short, avg_salary_year DESC)` in the Gold layer) to guarantee sub-second dashboard read latency.
* **Advanced SQL Array Parsing & Star Schema Modeling:** Job skills embedded as flat Python-style strings (`['SQL', 'Python']`) are parsed and exploded dynamically within SQL using ClickHouse's native `replaceRegexpAll`, `splitByChar`, and `arrayJoin()` table functions. This normalized data is structured into a Star Schema with a dedicated **Bridge Table (`wh_silver.bridge_skill_job`)**, cleanly resolving complex Many-to-Many skill relationships without data redundancy.
* **Production-Grade Observability & Modular Orchestration:** The ETL execution script (`run_etl.py`) incorporates dual-channel logging (`StreamHandler`/`FileHandler`), execution profiling via `perf_counter`, and automated fail-fast row validation that instantly halts execution if landing tables are empty. The entire pipeline is orchestrated using **Apache Airflow** (`bronze >> silver >> gold`) via modular `PythonOperator` tasks, keeping core processing logic decoupled and independently testable.

## Directory Structure
The **de_engineering** module contains all components required to build the data engineering pipeline, from source data preparation to data warehouse creation and ETL execution.
```text
de_engineering/
│
├── README.md                   # Data Engineering technical documentation
│
├── data_preparation/           # Source data preparation & PostgreSQL staging
│   ├── create_potgres.py       # DDL script to initialize PostgreSQL staging table
│   ├── download_dataset.py     # Utility to fetch or partition raw CSV datasets
│   ├── ingest_to_postgres.py   # Batch loader moving CSV data into PostgreSQL
│   └── prepare_data.py         # Data cleansing and preprocessing utilities
│
├── setup_ddl/                  # ClickHouse warehouse DDL definitions
│   ├── clickhouse_bronze.sql   # Creates src_bronze database and raw_data table
│   ├── clickhouse_silver.sql   # Creates wh_silver database, star schema & bridge tables
│   ├── clickhouse_gold.sql     # Creates mart_gold database and analytical data marts
│   └── clickhouse_reset.sql    # Utility script to drop and reset warehouse schemas
│
├── etl_dml/                    # SQL DML transformation scripts
│   ├── load_bronze.sql         # Extracts from Postgres/CSV and populates Bronze layer
│   ├── transform_silver.sql    # Cleanses, deduplicates, and populates Star Schema
│   └── aggregation_gold.sql    # Computes business metrics and populates Gold data marts
│
└── scripts/                    # Orchestration and automation entry points
    ├── build_warehouse.py      # Executes all DDL scripts to initialize ClickHouse schemas
    ├── run_etl.py              # Executes sequential DML transformations across layers
    ├── full_pipeline.py        # End-to-end wrapper running preparation, DDL, and ETL
    └── reset_rebuild_wh.py     # Reset and rebuild utility for testing and debugging
```


### Directory Description

| Directory | Description |
|----------|-------------|
| **data_preparation** | Prepares the raw dataset by downloading, splitting, creating the PostgreSQL database, and ingesting CSV files into the operational database. |
| **setup_ddl** | Contains SQL Data Definition Language (DDL) scripts used to create the ClickHouse warehouse schema, including Bronze, Silver, and Gold layers. |
| **etl_dml** | Contains SQL Data Manipulation Language (DML) scripts that implement the ETL process across the Medallion Architecture. |
| **scripts** | Provides Python entry-point scripts to build the warehouse and execute the end-to-end ETL pipeline. |

### SQL Scripts Reference

The pipeline relies on modular SQL DDL (Data Definition Language) and DML (Data Manipulation Language) scripts to define schemas and execute data transformations across the Medallion Architecture:

| Folder | File Name | Target Layer / DB | Purpose & Description |
| :--- | :--- | :--- | :--- |
| **`setup_ddl/`** | `clickhouse_bronze.sql` | `src_bronze` | Creates the raw landing database and the `raw_data` table with 64-bit integer hashing (`job_hash`). |
| | `clickhouse_silver.sql` | `wh_silver` | Creates the Star Schema structure: dimension tables (`dim_company`, `dim_date`, `dim_skill`), the central fact table (`fact_job_postings`), and the bridge table (`bridge_skill_job`). |
| | `clickhouse_gold.sql` | `mart_gold` | Creates the pre-aggregated analytical data marts: `agg_salary_by_role`, `agg_skill_demand_monthly`, and `agg_top_paying_skills`. |
| | `clickhouse_reset.sql` | *All Layers* | Utility script to drop and reset all ClickHouse databases for testing or clean re-runs. |
| **`etl_dml/`** | `load_bronze.sql` | `src_bronze` | Extracts operational data from PostgreSQL staging and loads it into the ClickHouse Bronze raw table. |
| | `transform_silver.sql` | `wh_silver` | Cleanses strings, deduplicates via `job_hash`, parses flat Python skill arrays into individual rows using `arrayJoin()`, and populates the Star Schema. |
| | `aggregation_gold.sql` | `mart_gold` | Computes analytical aggregations (e.g., salary distributions and monthly skill demand) and populates the Gold data marts. |

## Execution Guide

This guide provides step-by-step instructions to initialize the databases, build the analytical data warehouse, and execute the end-to-end ETL pipeline.

### Prerequisites & Environment Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/irpan06/Data-Job-Analytics-Platform.git
   cd Data-Job-Analytics-Platform
2. **Install Dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. **Configure Environment Variables:**
    Create a .env file in the root project directory and define your connection credentials for both PostgreSQL and ClickHouse:  
    ``` bash
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=job_market_oltp
    POSTGRES_TABLE=job_postings
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_password

    CLICKHOUSE_HOST=localhost
    CLICKHOUSE_PORT=9000
    CLICKHOUSE_USER=default
    CLICKHOUSE_PASSWORD=your_password
    ```
### Option 1: Standalone CLI Execution (Step-by-Step)
You can execute the pipeline modularly using the Python scripts provided in the `de_engineering/scripts` directory

#### Step 1: Download Dataset & Initialize Operational Staging (PostgreSQL)
Download the raw CSV datasets, initialize the PostgreSQL staging table, and ingest the batch files into the transactional database:
```bash
python de_engineering/data_preparation/download_dataset.py
python de_engineering/data_preparation/create_potgres.py
python de_engineering/data_preparation/ingest_to_postgres.py
```

#### Step 2: Build Analytical Warehouse Schemas (Clickhouse)
Execute the DDL scripts to generate the Medallion Architecture databases (`src_bronze`, `wh_silver`, `mart_gold`) and analytical tables in Clickhouse:
```bash
python de_engineering/scripts/build_warehouse.py
```

#### Step 3: Run the Medallion ETL Pipeline
Execute the transformation pipeline that extracts data from PostgreSQL, loads it into Bronze layer, standardizes it into Silver Star Schema, and aggregates business metrcis into the Gold data marts:
```bash
python de_engineering/scripts/run_etl.py
```
Note: _Execution progress, sub-second layer duration, and automated row validation metrics will be streamed directly to your terminal and logged persistently to_ `logs/pipeline.log`

```log
2026-07-15 14:36:03 | INFO | ============================================================
2026-07-15 14:36:03 | INFO |                    DATA WAREHOUSE ETL PIPELINE
2026-07-15 14:36:03 | INFO | ============================================================
2026-07-15 14:36:03 | INFO | 
2026-07-15 14:36:03 | INFO | Bronze
2026-07-15 14:36:03 | INFO | ------------------------------------------------------------
2026-07-15 14:36:03 | INFO | Running load_bronze.sql
2026-07-15 14:36:07 | INFO | Bronze rows : 1615930
2026-07-15 14:36:07 | INFO | Duration    : 4.17 sec
2026-07-15 14:36:07 | INFO | 
2026-07-15 14:36:07 | INFO | Silver
2026-07-15 14:36:07 | INFO | ------------------------------------------------------------
2026-07-15 14:36:07 | INFO | Running transform_silver.sql
2026-07-15 14:36:15 | INFO | Fact Job     : 1615930
2026-07-15 14:36:15 | INFO | Dim Company  : 215938
2026-07-15 14:36:15 | INFO | Dim Skill    : 255
2026-07-15 14:36:15 | INFO | Dim Date     : 912
2026-07-15 14:36:15 | INFO | Bridge       : 7099772
2026-07-15 14:36:15 | INFO | Duration     : 7.65 sec
2026-07-15 14:36:15 | INFO | 
2026-07-15 14:36:15 | INFO | Gold
2026-07-15 14:36:15 | INFO | ------------------------------------------------------------
2026-07-15 14:36:15 | INFO | Running aggregation_gold.sql
2026-07-15 14:36:18 | INFO | Salary Mart   : 10
2026-07-15 14:36:18 | INFO | Skill Demand  : 51385
2026-07-15 14:36:18 | INFO | Top Paying    : 1716
2026-07-15 14:36:18 | INFO | Duration      : 3.19 sec
2026-07-15 14:36:18 | INFO | 
2026-07-15 14:36:18 | INFO | ============================================================
2026-07-15 14:36:18 | INFO |           Pipeline completed in 15.00 sec
2026-07-15 14:36:18 | INFO | ============================================================

```

#### Shortcut: One-Click Full Pipeline Execution
if you wish to run all the setup, DDL initialization, and DML transformations sequentially in a single command, use the end-to-end automation wrapper:
```bash
python de_engineering/scripts/full_pipeline.py
```

### Option 2: Automated Orchestration via Apache Airflow
If you have an active Apache Airflow environmnent, you can run the pipeline using the provided DAG:
1. **Deploy the DAG**:
    Copy or link the project's DAG folder (`airflow/airflow_home/dags/`) and the project root path to your Airflow environment.
2. **Trigger the Pipeline**:
    Locate the `job_market_etl` DAG in the Airflow UI. Since `schedule=None` is configured for portofolio demonstration purposes, manually trigger the DAG.
3. **Monitor Execution**:
    Watch the sequential progression of the Medallion pipeline (`load_bronze >> transform_silver >> build_gold`). If any validation check fails (such as empty Bronze table), Airflow will automatically halt downstream tasks to protect data integrity.
