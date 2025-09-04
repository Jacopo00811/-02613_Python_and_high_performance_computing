import numpy as np
from time import perf_counter
import sys

SIZES = np.logspace(1, 4.5, num=10, dtype=int)

for SIZE in SIZES:
    mat = np.random.rand(SIZE, SIZE)
    start = perf_counter()
    if sys.argv[1] == 'row':
        for _ in range(1000):
            double_row = 2 * mat[0, :]

    elif sys.argv[1] == 'column':
        for _ in range(1000):
            double_column = 2 * mat[:, 0]

    end = perf_counter()
    print(f'Time taken: {end - start} seconds for size {SIZE}')
