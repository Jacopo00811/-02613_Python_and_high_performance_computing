from pyarrow import csv
from time import perf_counter

def pyarrow_load(fname):
    return csv.read_csv(fname).to_pandas()

if __name__ == "__main__":
    path = '/zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_1/2023_01.csv'
    initial_time = perf_counter()
    pyarrow_load(path)
    print("Time load pyarrow and convert to pandas: ", perf_counter() - initial_time)

