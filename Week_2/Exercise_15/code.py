import numpy as np
import sys
from time import perf_counter

start_time = perf_counter()

path = sys.argv[1]
p = int(sys.argv[2])

matrix = np.load(path)
result = np.linalg.matrix_power(matrix, p+1)

np.save('result.npy', result)

end_time = perf_counter()
print(end_time - start_time)
