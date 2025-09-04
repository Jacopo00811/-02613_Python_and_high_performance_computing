import numpy as np
from time import perf_counter
import sys

SIZE = 1000

mat = np.random.rand(SIZE, SIZE)
start = perf_counter()
print(f'Running {sys.argv[1]} operation')
if sys.argv[1] == 'row':
    for _ in range(1000):
        double_row = 2 * mat[0, :]
    print("Done")

elif sys.argv[1] == 'column':
    for _ in range(1000):
        double_column = 2 * mat[:, 0]
    print("Done")

end = perf_counter()
print(f'Time taken: {end - start} seconds')
