from create_potgres import main as create_table
from download_dataset import main as download_data
from ingest_to_postgres import main as ingest_data

def main():

    print("=" * 60)
    print("                 DATA PREPARATION PIPELINE                  ")
    print("=" * 60)
    print()

    print("[1/3] Create PostgreSQL Source")
    print("-" * 60)
    create_table()

    print("[2/3] Download & Split Dataset")
    print("-" * 60)
    download_data()

    print("[3/3] Ingest Dataset to PostgreSQL")
    print("-" * 60)
    ingest_data()

    print("=" * 60)
    print("         Source data preparation completed successfully!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()