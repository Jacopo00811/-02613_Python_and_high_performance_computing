import os
import pandas as pd
from time import perf_counter

path = '/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip'

initial_time = perf_counter()
# Unzip and load
os.system(f'unzip -o {path} -d /zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_1/')
df = pd.read_csv('/zhome/f9/0/168881/Desktop/PyHPC/Week_7/Exercise_1/2023_01.csv')
print("Time unzip + load: ", perf_counter() - initial_time)

# Load zipped
initial_time = perf_counter()
df = pd.read_csv(path)
print("Time load zipped: ", perf_counter() - initial_time)