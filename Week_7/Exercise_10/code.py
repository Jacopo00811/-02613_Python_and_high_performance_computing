import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from time import perf_counter

path_parquet = '/zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_9/output.parquet'
path_csv = '/zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_1/2023_01.csv'
output_parquet = '/zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_10/output.parquet'
output_csv = '/zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_10/output.csv'

def measure_csv_operations():
    # Measure reading CSV
    start = perf_counter()
    df_csv = pd.read_csv(path_csv)
    csv_read_time = perf_counter() - start
    print(f"CSV Read Time: {csv_read_time:.4f} seconds")
    
    # Measure writing CSV
    start = perf_counter()
    df_csv.to_csv(output_csv, index=False)
    csv_write_time = perf_counter() - start
    print(f"CSV Write Time: {csv_write_time:.4f} seconds")
    
    return df_csv, csv_read_time, csv_write_time

def measure_parquet_operations():
    # Measure reading Parquet
    start = perf_counter()
    df_parquet = pd.read_parquet(path_parquet)
    parquet_read_time = perf_counter() - start
    print(f"Parquet Read Time: {parquet_read_time:.4f} seconds")
    
    # Measure writing Parquet
    start = perf_counter()
    df_parquet.to_parquet(output_parquet, index=False)
    parquet_write_time = perf_counter() - start
    print(f"Parquet Write Time: {parquet_write_time:.4f} seconds")
    
    return df_parquet, parquet_read_time, parquet_write_time

def compare_file_sizes():
    import os
    csv_size = os.path.getsize(output_csv) / (1024 * 1024)
    parquet_size = os.path.getsize(output_parquet) / (1024 * 1024)
    print(f"CSV File Size: {csv_size:.2f} MB")
    print(f"Parquet File Size: {parquet_size:.2f} MB")
    print(f"Compression Ratio: {csv_size / parquet_size:.2f}x")

if __name__ == "__main__":
    print("=== CSV Operations ===")
    df_csv, csv_read_time, csv_write_time = measure_csv_operations()
    
    print("\n=== Parquet Operations ===")
    df_parquet, parquet_read_time, parquet_write_time = measure_parquet_operations()
    
    print("\n=== Performance Comparison ===")
    print(f"Read Speed Improvement: {csv_read_time / parquet_read_time:.2f}x faster with Parquet")
    print(f"Write Speed Improvement: {csv_write_time / parquet_write_time:.2f}x faster with Parquet")
    
    print("\n=== File Size Comparison ===")
    compare_file_sizes()
    
    print("\n=== Data Verification ===")
    print(f"CSV DataFrame Shape: {df_csv.shape}")
    print(f"Parquet DataFrame Shape: {df_parquet.shape}")
    
    # Check if dataframes have the same columns (might be in different order)
    csv_cols = set(df_csv.columns)
    parquet_cols = set(df_parquet.columns)
    print(f"Same columns: {csv_cols == parquet_cols}")