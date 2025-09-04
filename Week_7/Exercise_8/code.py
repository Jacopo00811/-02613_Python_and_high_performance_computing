from pyarrow import csv
from time import perf_counter
import pyarrow as pa

def pyarrow_load(fname):
    # Create a timestamp parser that understands UTC timezone ('Z' suffix)    
    copts = csv.ConvertOptions(
        column_types={
            'created': pa.timestamp('ns', tz='UTC'),  # Specify timezone as UTC
            'observed': pa.timestamp('ns', tz='UTC'),  # Specify timezone as UTC
            'parameterId': pa.dictionary(pa.int32(), pa.string()),
            'stationId': pa.dictionary(pa.int32(), pa.string())
        }
    )
    
    table = csv.read_csv(fname, convert_options=copts)
    table_size_mb = table.nbytes / (1024 * 1024)  # Convert bytes to MB
    print(f"Table size: {table.shape}, Memory: {table_size_mb:.2f} MB")
    
    table_pandas = table.to_pandas()
    pandas_size_mb = table_pandas.memory_usage(deep=True).sum() / (1024 * 1024)  # Convert bytes to MB
    print(f"Table size pandas: {table_pandas.shape}, Memory: {pandas_size_mb:.2f} MB")
    
    return table_pandas

if __name__ == "__main__":
    path = '/zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_1/2023_01.csv'
    initial_time = perf_counter()
    pyarrow_load(path)
    print("Time load pyarrow and convert to pandas: ", perf_counter() - initial_time)