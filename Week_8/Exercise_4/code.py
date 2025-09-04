import sys
import pyarrow.parquet as pq

path = sys.argv[1]

file = pq.ParquetFile(path)
precipitation = 0
for i in range(file.num_row_groups):
    chunk = file.read_row_group(i)
    precipitation += chunk.column('value').to_pandas().loc[chunk.column('parameterId').to_pandas() == 'precip_past10min'].sum()

print(precipitation)