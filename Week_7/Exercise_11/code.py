import pandas as pd
from time import perf_counter

def total_precip(df):
    total = 0.0
    for i in range(len(df)):
        row = df.iloc[i]
        if row['parameterId'] == 'precip_past10min':
            total += row['value']
    return total

if __name__ == "__main__":
    path_csv = '/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip'
    df = pd.read_csv(path_csv)
    sample_size = 10000

    sample_df = df.sample(sample_size, random_state=42)
    start_time = perf_counter()
    result = total_precip(sample_df)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.4f} seconds")
