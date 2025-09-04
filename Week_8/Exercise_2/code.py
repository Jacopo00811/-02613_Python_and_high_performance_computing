import pandas as pd
import sys

path = sys.argv[1]
chunk_size = int(sys.argv[2])

df = pd.read_csv(path, chunksize=chunk_size)

precipitation = 0
for chunk in df:
    precipitation += chunk.loc[chunk['parameterId'] == 'precip_past10min', 'value'].sum()

print(precipitation)