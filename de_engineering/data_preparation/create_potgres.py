import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv


def main():
    # Base directory
    BASE_DIR = Path(__file__).resolve().parents[2]
    load_dotenv(BASE_DIR / ".env")

    # PostgreSQL connection
    pg_conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    cursor = pg_conn.cursor()

    try:
        print("creating PostgreSQL table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_postings (
                job_title_short TEXT,
                job_title TEXT,
                job_location TEXT,
                job_via TEXT,
                job_schedule_type TEXT,
                job_work_from_home BOOLEAN,
                search_location TEXT,
                job_posted_date TIMESTAMP,
                job_no_degree_mention BOOLEAN,
                job_health_insurance BOOLEAN,
                job_country TEXT,
                salary_rate TEXT,
                salary_year_avg DOUBLE PRECISION,
                salary_hour_avg DOUBLE PRECISION,
                company_name TEXT,
                job_skills TEXT,
                job_type_skills TEXT,
                inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_job_posted_date
            ON job_postings(job_posted_date);
        """)

        pg_conn.commit()
        print("PostgreSQL table created successfully.")
        print()

    except Exception as e:
        pg_conn.rollback()
        print(f"Failed to create PostgreSQL table: {e}")
        print()

    finally:
        cursor.close()
        pg_conn.close()


if __name__ == "__main__":
    main()