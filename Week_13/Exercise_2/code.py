from time import perf_counter as time
import numpy as np
from multiprocessing.pool import ThreadPool

def matmul_single(args):
    i, a, b = args
    return i, np.matmul(a, b)

def matmuls(A, B):
    assert A.shape[0] == B.shape[0], "A and B must hold same number of matrices"
    assert A.shape[2] == B.shape[1], "A and B must hold compatible matrices"
    n = A.shape[0]
    C = np.empty((n, A.shape[1], B.shape[2]))
    
    # Create a thread pool and distribute the matrix multiplications
    with ThreadPool() as pool:
        args = [(i, A[i], B[i]) for i in range(n)]
        results = pool.map(matmul_single, args)
    
    # Place results in the correct positions
    for i, result in results:
        C[i] = result
        
    return C

A = np.random.rand(100, 1000, 1000)
B = np.random.rand(100, 1000, 1000)
t0 = time()
C = matmuls(A, B)
t1 = time()
print(f"Execution time with multi-threading: {t1 - t0:.2f} seconds")