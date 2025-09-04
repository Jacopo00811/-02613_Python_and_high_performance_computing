import numpy as np
from time import perf_counter
import matplotlib.pyplot as plt

SIZES = np.logspace(2, 8, num=10, dtype=int)
performance = []
vector_sizes_kb = []

for SIZE in SIZES:
    mat = np.random.rand(1, SIZE)
    vector_size_kb = (mat.nbytes) / 1024
    vector_sizes_kb.append(vector_size_kb)

    start = perf_counter()
    for _ in range(100):
        double_row = 2 * mat[0, :]
    end = perf_counter()
    time = end - start

    mflops = (SIZE * 100) / (time * 1e6)
    performance.append(mflops)
    print(f'Time taken: {time} seconds for size {SIZE}')

# Plotting the performance
plt.figure(figsize=(10, 6))
plt.loglog(vector_sizes_kb, performance, label='Row', marker='o')
plt.xlabel('Matrix Size (KB)')
plt.ylabel('Performance (MFLOP/s)')
plt.title('Performance of Row and Column Increasing Matrix Size')
plt.legend()
plt.savefig('performance.png')
