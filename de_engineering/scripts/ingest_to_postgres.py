import os
import glob
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from psycopg2.extras import execute_values

# path 
BASE_DIR = Path(__file__).resolve().parents[2]
dataset_dir = BASE_DIR / "dataset"

load_dotenv(BASE_DIR / ".env")

# postgres connection
pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

def get_sorted_file(folder):
    files = glob.glob(os.path.join(folder, "jobs_*.csv"))
    files.sort() # Mengurutkan nama file secara alfabetis (Januari -> Desember)
    return files

def ingest_to_postgres(file_path): 
    print(f"read: {os.path.basename(file_path)}")
    df = pd.read_csv(file_path)
    df = df.astype(object)
    df = df.where(pd.notnull(df), None) # Null -> None

    records = df.to_records(index=False) # tuple
    list_of_tuples = [tuple(x) for x in records]

    cursor = pg_conn.cursor()
    query = """
        INSERT INTO job_postings
        (
            job_title_short, job_title, job_location, job_via,
            job_schedule_type, job_work_from_home, search_location,
            job_posted_date, job_no_degree_mention, job_health_insurance, 
            job_country, salary_rate, salary_year_avg, salary_hour_avg, company_name,
            job_skills,job_type_skills  
        )
        VALUES %s
    """

    try:
        execute_values(cursor, query, list_of_tuples)
        pg_conn.commit()
        print(f'success ingesting {len(df):,} rows into Postgresql')
    except Exception as e:
        pg_conn.rollback()
        print(f'failed ingesting for file {os.path.basename(file_path)}: {e}')
    finally:
        cursor.close()

if __name__ == "__main__":
    csv_files = get_sorted_file(dataset_dir)

    if not csv_files:
        print(f'folder empty')
    else:
        for files in csv_files:
            ingest_to_postgres(files)
        