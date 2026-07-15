import os
import pandas as pd
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parents[2]
    output_dir = BASE_DIR / "dataset"
    os.makedirs(output_dir, exist_ok=True)
    url  = 'https://storage.googleapis.com/sql_de/job_postings_flat.csv'
    print('read csv file ...')
    print()
    df = pd.read_csv(url)
    date_column = "job_posted_date"
    df[date_column] = pd.to_datetime(df[date_column])
    print('start spliting data ...')
    for month, group in df.groupby(df[date_column].dt.month):
        name_file = f'jobs_month_{month:02d}.csv'
        path = os.path.join(output_dir, name_file)
        group = group.sort_values(by=date_column)
        group.to_csv(path, index=False)
        print(f'success: {name_file}')
    print()

if __name__ == '__main__':
    main()