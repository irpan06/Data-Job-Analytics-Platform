import os
import glob
import logging
from time import perf_counter
import clickhouse_connect
from pathlib import Path
from dotenv import load_dotenv

# path
BASE_DIR = Path(__file__).resolve().parents[2]

etl_path = Path(__file__).resolve().parents[1]
etl_dir = etl_path / 'etl_dml'

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# env
load_dotenv(BASE_DIR / ".env")

# postgres
CONFIG = {
    "PG_HOST": os.getenv("POSTGRES_HOST"),
    "PG_PORT": os.getenv("POSTGRES_PORT"),
    "PG_DATABASE": os.getenv("POSTGRES_DB"),
    "PG_TABLE": os.getenv("POSTGRES_TABLE"),
    "PG_USER": os.getenv("POSTGRES_USER"),
    "PG_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
}

# clickHouse connection
ch_client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=int(os.getenv("CLICKHOUSE_PORT")),
    user=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
)

def run_clickhouse(sql_file):
    logger.info(f"running {sql_file.name}")
    sql = sql_file.read_text(encoding="utf-8")
    queries = sql.split(";")
    for query in queries:
        query = query.strip()
        if query:
            ch_client.command(query)

def execute_sql_file(client, sql_file: Path, config: dict):
    sql_file = etl_dir / sql_file
    sql = sql_file.read_text(encoding="utf-8")
    sql = sql.format(**config)
    queries = sql.split(";")
    for query in queries:
        query = query.strip()
        if query:
            client.command(query)

def get_row_count(client, table_name):
    result = client.query(
        f"SELECT COUNT() AS total_rows FROM {table_name}"
    )
    return result.result_rows[0][0]


# --- REFACTORED FUNCTIONS ---

def load_bronze():
    logger.info('')
    logger.info('Bronze')
    logger.info("-" * 60)

    start = perf_counter()
    logger.info("Running load_bronze.sql")

    execute_sql_file(ch_client, "load_bronze.sql", CONFIG)

    bronze_rows = get_row_count(
        ch_client,
        "src_bronze.raw_data"
    )

    logger.info(f"Bronze rows : {bronze_rows}")
    logger.info('')   
    logger.info(f"Duration    : {perf_counter()-start:.2f} sec")

    if bronze_rows == 0:
        raise RuntimeError(
            "Bronze table contains 0 rows."
        )

def transform_silver():
    logger.info('')
    logger.info('Silver')
    logger.info("-" * 60)

    start = perf_counter()

    logger.info("Running transform_silver.sql")

    execute_sql_file(
        ch_client,
        "transform_silver.sql",
        CONFIG
    )

    fact = get_row_count(
        ch_client,
        "wh_silver.fact_job_postings"
    )
    
    ddate = get_row_count(
        ch_client,
        "wh_silver.dim_date"
    )

    company = get_row_count(
        ch_client,
        "wh_silver.dim_company"
    )

    skill = get_row_count(
        ch_client,
        "wh_silver.dim_skill"
    )

    bridge = get_row_count(
        ch_client,
        "wh_silver.bridge_skill_job"
    )

    logger.info(f"Fact Job     : {fact} ")
    logger.info(f"Dim Company  : {company}")
    logger.info(f"Dim Skill    : {skill}")
    logger.info(f"Dim Date     : {ddate}")
    logger.info(f"Bridge       : {bridge}")
    logger.info('')
    logger.info(f"Duration     : {perf_counter()-start:.2f} sec")

def build_gold():
    logger.info('')
    logger.info('Gold')
    logger.info("-" * 60)

    start = perf_counter()

    logger.info("Running aggregation_gold.sql")

    execute_sql_file(
        ch_client,
        "aggregation_gold.sql",
        CONFIG
    )

    salary = get_row_count(
        ch_client,
        "mart_gold.agg_salary_by_role"
    )

    demand = get_row_count(
        ch_client,
        "mart_gold.agg_skill_demand_monthly"
    )

    top = get_row_count(
        ch_client,
        "mart_gold.agg_top_paying_skills"
    )

    logger.info(f"Salary Mart   : {salary}")
    logger.info(f"Skill Demand  : {demand}")
    logger.info(f"Top Paying    : {top}")
    logger.info('')
    logger.info(f"Duration      : {perf_counter()-start:.2f} sec")
    logger.info('')


def main():
    total_start = perf_counter()

    logger.info('')
    logger.info("=" * 60)
    logger.info("                   DATA WAREHOUSE ETL PIPELINE")
    logger.info("=" * 60)

    try:
        load_bronze()
        transform_silver()
        build_gold()

        logger.info("=" * 60)
        logger.info(f"Pipeline completed in {perf_counter()-total_start:.2f} sec")
        logger.info("=" * 60)

    except Exception as e:
        logger.exception(f"Pipeline failed!: {e}")

    finally:
        ch_client.close()

if __name__ == "__main__":
    main()