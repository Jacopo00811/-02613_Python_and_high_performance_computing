import pandas as pd
import sys
from pyarrow import parquet as pq
import pyarrow as pa

input_path = sys.argv[1]
chunk_size = int(sys.argv[2])

df_iterator = pd.read_csv(input_path, chunksize=chunk_size)
first = True
writer = None
for chunk in df_iterator:
    chunk_table = pa.Table.from_pandas(chunk)
    schema = chunk_table.schema
    if first:
        writer = pq.ParquetWriter('output.parquet', schema)
        first = False
    writer.write_table(chunk_table)
writer.close()

print(f"CSV file converted to parquet chunks in output.parquet with chunk size {chunk_size}")