import os
import pandas as pd

# output dir
output = '../../../dataset'
os.makedirs(output, exist_ok=True)

# dataset url
url  = 'https://storage.googleapis.com/sql_de/job_postings_flat.csv'

print('read csv file ...')
df = pd.read_csv(url)

date_column = "job_posted_date"

print('makesure date column correct')
df[date_column] = pd.to_datetime(df[date_column])

print('start spliting data')

for month, group in df.groupby(df[date_column].dt.month):
    name_file = f'jobs_month_{month}.csv'
    path = os.path.join(output, name_file)
    group = group.sort_values(by=date_column)
    group.to_csv(path, index=False)
    print(f'success: {name_file}')
