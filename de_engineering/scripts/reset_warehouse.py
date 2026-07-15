import os
import glob
import psycopg2
import build_warehouse
import clickhouse_connect
from pathlib import Path
from dotenv import load_dotenv

# path
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

DDL_DIR = Path(__file__).resolve().parents[1]
DDL_DIR = DDL_DIR / "setup_ddl"

# postgres connection
pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

pg_conn.autocommit = True

# clickhouse connection
ch_client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    port=int(os.getenv("CLICKHOUSE_PORT")),
    user=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
)

# run sql file
def run_postgres(sql_file):
    print(f"Running {sql_file.name}")
    with pg_conn.cursor() as cur:
        sql = sql_file.read_text(encoding="utf-8")
        cur.execute(sql)

def run_clickhouse(sql_file):
    print(f"Running {sql_file.name}")
    sql = sql_file.read_text(encoding="utf-8")
    queries = sql.split(";")
    for query in queries:
        query = query.strip()
        if query:
            ch_client.command(query)

def main():
    print("========== RESETTING POSTGRES ==========")
    run_postgres(DDL_DIR / "postgres_reset.sql")
    print()
    print("========== RESETTING CLICKHOUSE ==========")
    run_clickhouse(DDL_DIR / "clickhouse_reset.sql")
    print()
    print("REBUILDING WAREHOUSE...")
    print()
    # build_warehouse.main()

if __name__ == "__main__":
    main()