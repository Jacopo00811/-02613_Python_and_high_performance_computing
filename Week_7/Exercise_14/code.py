import pandas as pd
from pyarrow import csv
import sys


def total_precip(df):
    total = df.loc[df['parameterId'] == 'precip_past10min', 'value'].sum()
    return total

if __name__ == '__main__':
    path = sys.argv[1]
    # Read the Parquet file using PyArrow
    df = csv.read_csv(path).to_pandas()
    result = total_precip(df)
    print(result)
