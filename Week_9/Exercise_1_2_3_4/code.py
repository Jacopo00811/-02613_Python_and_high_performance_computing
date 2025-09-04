# Using the @jit(nopython=True) decorator, add Numba JIT compilation to the above function.
import numpy as np
from numba import jit
import time

def OG_matmul(A, B):
    C = np.zeros((A.shape[0],B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i,j] += A[i,k] * B[k,j]
    return C

@jit(nopython=True)
def matmul(A, B):
    C = np.zeros((A.shape[0],B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i,j] += A[i,k] * B[k,j]
    return C

# Measure the wall time of the original and JIT compiled version for two 100 X 100
# matrices. How much faster is the JIT compiled version? Remember to run the JIT compiled version once before timing so it can compile
A = np.random.rand(100, 100)
B = np.random.rand(100, 100)
start = time.time()
C = OG_matmul(A, B)
end = time.time()
print("Original function time:", end - start)

start = time.time()
C = matmul(A, B)
end = time.time()
print("JIT compiled function time:", end - start)

# Autolab Assuming A, B and C are stored row-wise, the innermost loop (over k) is not accessing B in a cache efficient manner. 
# Make a new version of matmul where you re-order the loops such that access is cache efficient.


@jit(nopython=True)
def matmul_imp(A, B):
    C = np.zeros((A.shape[0],B.shape[1]))
    for i in range(A.shape[0]):
        for k in range(B.shape[1]):
            for j in range(A.shape[1]):
                C[i,j] += A[i,k] * B[k,j]
    return C

start = time.time()
C = matmul_imp(A, B)
end = time.time()
print("JIT compiled function imp time:", end - start)


#  Measure the performance of your optimized version for NXN matrices, where N
#  is at least 200. What do you observe?
start = time.time()
A = np.random.rand(200,200)
B = np.random.rand(200,200)
C = matmul_imp(A, B)
end = time.time()
print("JIT compiled function imp over 200x200 time:", end - start)


