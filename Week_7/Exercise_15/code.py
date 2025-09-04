import pandas as pd
from pyarrow import csv
import sys
from time import perf_counter

def total_precip_no_index(df):
    """Calculate total precipitation using standard filtering"""
    start = perf_counter()
    total = df.loc[df['parameterId'] == 'precip_past10min', 'value'].sum()
    execution_time = perf_counter() - start
    return total, execution_time

def setup_index(df):
    """Create an index on parameterId column"""
    start = perf_counter()
    df_indexed = df.set_index('parameterId')
    index_time = perf_counter() - start
    return df_indexed, index_time

def total_precip_with_index(df_indexed):
    """Calculate total precipitation using index"""
    start = perf_counter()
    # Access rows where index equals 'precip_past10min'
    total = df_indexed.loc['precip_past10min', 'value'].sum()
    execution_time = perf_counter() - start
    return total, execution_time

if __name__ == '__main__':
    path = sys.argv[1]
    
    # Read the CSV file
    print("Loading data...")
    load_start = perf_counter()
    df = csv.read_csv(path).to_pandas()
    load_time = perf_counter() - load_start
    print(f"Data loaded in {load_time:.4f} seconds")
    
    # Method 1: No index
    print("\n--- Method 1: Without Index ---")
    result_no_index, time_no_index = total_precip_no_index(df)
    print(f"Total precipitation: {result_no_index}")
    print(f"Execution time: {time_no_index:.4f} seconds")
    
    # Method 2: With index
    print("\n--- Method 2: With Index ---")
    df_indexed, index_time = setup_index(df)
    result_with_index, time_with_index = total_precip_with_index(df_indexed)
    print(f"Total precipitation: {result_with_index}")
    print(f"Time to build index: {index_time:.4f} seconds")
    print(f"Execution time (excluding index creation): {time_with_index:.4f} seconds")
    print(f"Execution time (including index creation): {index_time + time_with_index:.4f} seconds")
    
    # Comparison
    print("\n--- Comparison ---")
    speedup_excluding_index = time_no_index / time_with_index
    speedup_including_index = time_no_index / (time_with_index + index_time)
    print(f"Speedup (excluding index creation): {speedup_excluding_index:.2f}x")
    print(f"Speedup (including index creation): {speedup_including_index:.2f}x")