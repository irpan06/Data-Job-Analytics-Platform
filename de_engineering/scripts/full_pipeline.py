from run_etl import main as run_etl
from build_warehouse import main as build_wh

def main():

    print('='*60)
    print('                 DATA WAREHOUSE PIPELINE                 ')
    print('='*60)
    print()

    print("[1/2] Build Data Warehouse")
    print("-" * 60)
    build_wh()

    print("[2/2] Run ETL Pipeline")
    print("-" * 60)
    run_etl()

    print()
    print("=" * 60)
    print("Data warehouse pipeline completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()