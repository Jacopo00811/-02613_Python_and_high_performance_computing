import sys 
from pyarrow import csv
import os
from pyarrow import parquet

if __name__ == '__main__':
    path = sys.argv[1] 
    table = csv.read_csv(path)
    parquet.write_table(table, os.getcwd() + '/output.parquet')
