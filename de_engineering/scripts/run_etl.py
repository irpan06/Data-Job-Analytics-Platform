import os
import glob
import clickhouse_connect
from pathlib import Path
from dotenv import load_dotenv
from build_warehouse import run_clickhouse 

# path
BASE_DIR = Path(__file__).resolve().parents[2]

etl_path = Path(__file__).resolve().parents[1]
etl_dir = etl_path / 'etl_dml'

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

def execute_sql_file(client, sql_file: Path, config: dict):
    print(f"Running {sql_file.name}")

    sql = sql_file.read_text(encoding="utf-8")

    # replace placeholder dari .env
    sql = sql.format(**config)

    # pisahkan multiple statement
    queries = [
        q.strip()
        for q in sql.split(";")
        if q.strip() and not q.strip().startswith("--")
    ]

    for query in queries:
        client.command(query)

def main():

    sql_files = [
        etl_dir / "load_bronze.sql",
        etl_dir / "transform_silver.sql",
        etl_dir / "aggregation_gold.sql",
    ]

    print("=" * 60)
    print("RUNNING ETL PIPELINE")
    print("=" * 60)

    try:
        for sql_file in sql_files:
            execute_sql_file(ch_client, sql_file, CONFIG)

        print("\nETL Pipeline completed successfully!")

    finally:
        ch_client.close()


if __name__ == "__main__":
    main()