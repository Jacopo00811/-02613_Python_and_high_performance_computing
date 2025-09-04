import numpy as np
from time import perf_counter
import matplotlib.pyplot as plt

SIZES = np.logspace(1, 4.5, num=50, dtype=int)
row_performance = []
column_performance = []
matrix_sizes_kb = []

for SIZE in SIZES:
    mat = np.random.rand(SIZE, SIZE)
    matrix_size_kb = (mat.nbytes) / 1024
    matrix_sizes_kb.append(matrix_size_kb)

    start = perf_counter()
    for _ in range(1000):
        double_row = 2 * mat[0, :]
    end = perf_counter()
    row_time = end - start
    row_mflops = (2 * SIZE * 1000) / (row_time * 1e6)
    row_performance.append(row_mflops)

    start = perf_counter()
    for _ in range(1000):
        double_column = 2 * mat[:, 0]
    end = perf_counter()
    column_time = end - start
    column_mflops = (2 * SIZE * 1000) / (column_time * 1e6)
    column_performance.append(column_mflops)

# Plotting the performance
plt.figure(figsize=(10, 6))
plt.loglog(matrix_sizes_kb, row_performance, label='Row', marker='o')
plt.loglog(matrix_sizes_kb, column_performance, label='Column', marker='x')
plt.xlabel('Matrix Size (KB)')
plt.ylabel('Performance (MFLOP/s)')
plt.title('Performance of Row and Column Increasing Matrix Size')
plt.legend()
plt.savefig('performance.png')

# Plotting the ratio of MFLOPS/s
ratio = np.array(row_performance) / np.array(column_performance)
plt.figure(figsize=(10, 6))
plt.loglog(matrix_sizes_kb, ratio, label='Row/Column Performance Ratio', marker='s')
plt.xlabel('Matrix Size (KB)')
plt.ylabel('Performance Ratio (Row/Column)')
plt.title('Ratio of Row to Column Increasing Performance')
plt.legend()
plt.savefig('ratio.png')
