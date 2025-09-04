from numba import cuda
import numpy as np
import time

# Make a CUDA kernel matmul_kernel(A, B, C) that multiplies two matrices together. Let A and B be the input matrices and C be the output matrix you write to. You may assume the dimensions of A and B match so they can be multiplied. Structure your kernel such that you use a 2D compute grid where thread (i, j) computes the value of C[i,j].
# Hint: use cuda.grid(2) to get 2D grid position of the current thread.

@cuda.jit
def matmul_kernel(A, B, C):
    # Get the 2D grid position of the current thread
    i, j = cuda.grid(2)
    if i < C.shape[0] and j < C.shape[1]:
        for k in range(A.shape[1]):
            C[i, j] += A[i, k] * B[k, j]

n = 2048
A = np.random.random((n, n)).astype(np.float32)
B = np.random.random((n, n)).astype(np.float32)
C = np.zeros((n, n), dtype=np.float32)

threads_per_block = (16, 16)
blocks_per_grid_x = (n + threads_per_block[0] - 1) // threads_per_block[0]
blocks_per_grid_y = (n + threads_per_block[1] - 1) // threads_per_block[1]
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

# Measure CUDA kernel execution time only
d_A = cuda.to_device(A)
d_B = cuda.to_device(B)
d_C = cuda.to_device(C)
start_kernel = time.time()
matmul_kernel[blocks_per_grid, threads_per_block](d_A, d_B, d_C)
cuda.synchronize()
end_kernel = time.time()
cuda_time_kernel_only = end_kernel - start_kernel
print(f"CUDA kernel execution time: {cuda_time_kernel_only:.6f} seconds")

# Measure NumPy time
start_numpy = time.time()
C_numpy = A @ B
end_numpy = time.time()
numpy_time = end_numpy - start_numpy
print(f"NumPy execution time: {numpy_time:.6f} seconds")

# Measure total time including transfers
start_total = time.time()
d_A = cuda.to_device(A)
d_B = cuda.to_device(B)
d_C = cuda.to_device(C)
matmul_kernel[blocks_per_grid, threads_per_block](d_A, d_B, d_C)
cuda.synchronize()
C_cuda = d_C.copy_to_host()
end_total = time.time()

total_time = end_total - start_total
transfer_time = total_time - cuda_time_kernel_only
transfer_fraction = transfer_time / total_time
print(f"Total time (with transfers): {total_time:.6f} seconds")
print(f"Time spent on memory transfers: {abs(transfer_time):.6f} seconds")
print(f"Fraction of time on transfers: {abs(transfer_fraction):.2%}")

# Pinned memory transfer measurements and measure total time including transfers with pinned memory
A_pinned = cuda.pinned_array((n, n), dtype=np.float32)
B_pinned = cuda.pinned_array((n, n), dtype=np.float32)
C_pinned = cuda.pinned_array((n, n), dtype=np.float32)
A_pinned[:] = np.random.random((n, n)).astype(np.float32)
B_pinned[:] = np.random.random((n, n)).astype(np.float32)
C_pinned.fill(0)

start_total_pinned = time.time()
d_A = cuda.to_device(A_pinned)
d_B = cuda.to_device(B_pinned)
d_C = cuda.to_device(C_pinned)
matmul_kernel[blocks_per_grid, threads_per_block](d_A, d_B, d_C)
cuda.synchronize()
d_C.copy_to_host(C_pinned)
end_total_pinned = time.time()

total_time_pinned = end_total_pinned - start_total_pinned
transfer_time_pinned = total_time_pinned - cuda_time_kernel_only
transfer_fraction_pinned = transfer_time_pinned / total_time_pinned

print(f"Total time (with pinned transfers): {total_time_pinned:.6f} seconds")
print(f"Time spent on pinned memory transfers: {abs(transfer_time_pinned):.6f} seconds")
print(f"Fraction of time on pinned transfers: {abs(transfer_fraction_pinned):.2%}")

# Configuration with 256x1
d_A = cuda.to_device(A)
d_B = cuda.to_device(B)
d_C = cuda.to_device(C)
d_C.copy_to_device(np.zeros((n, n), dtype=np.float32))
threads_per_block = (256, 1)
blocks_per_grid_x = (n + threads_per_block[0] - 1) // threads_per_block[0]
blocks_per_grid_y = (n + threads_per_block[1] - 1) // threads_per_block[1]
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

start = time.time()
matmul_kernel[blocks_per_grid, threads_per_block](d_A, d_B, d_C)
cuda.synchronize()
end = time.time()
print(f"Time with (256, 1) threads per block: {end - start:.6f} seconds")

# Configuration with 1x256
d_C.copy_to_device(np.zeros((n, n), dtype=np.float32))
threads_per_block = (1, 256)
blocks_per_grid_x = (n + threads_per_block[0] - 1) // threads_per_block[0]
blocks_per_grid_y = (n + threads_per_block[1] - 1) // threads_per_block[1]
blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

start = time.time()
matmul_kernel[blocks_per_grid, threads_per_block](d_A, d_B, d_C)
cuda.synchronize()
end = time.time()
print(f"Time with (1, 256) threads per block: {end - start:.6f} seconds")