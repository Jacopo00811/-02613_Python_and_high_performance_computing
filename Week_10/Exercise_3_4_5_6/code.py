from numba import cuda
import sys 
import numpy as np

TPB = 128  # Threads per block

@cuda.jit
def reduce_kernel(data, out, n):
    # Get the 1D grid and block indices
    tid = cuda.threadIdx.x
    i = cuda.grid(1)
    
    # Declare shared memory for the thread block
    shared = cuda.shared.array(shape=TPB, dtype=np.float32)
    
    # Load data into shared memory
    if i < n:
        shared[tid] = data[i]
    else:
        shared[tid] = 0
    
    cuda.syncthreads()  # Ensure all threads have loaded data
    
    # Do reduction in shared memory using strided indices to avoid warp divergence
    stride = cuda.blockDim.x // 2
    while stride > 0:
        if tid < stride:
            shared[tid] += shared[tid + stride]
        cuda.syncthreads()
        stride //= 2
    
    # Write result for this block to global memory
    if tid == 0:
        out[cuda.blockIdx.x] = shared[0]

def get_grid(n, tpb):
    return (n + (tpb - 1)) // tpb  # Blocks per grid

def reduce(x):
    n = len(x)
    bpg = get_grid(n, TPB)
    out = cuda.device_array(bpg, dtype=x.dtype)
    while bpg > 1:
        reduce_kernel[bpg, TPB](x, out, n)
        n = bpg
        bpg = get_grid(n, TPB)
        x[:n] = out[:n]
    reduce_kernel[bpg, TPB](x, out, n)
    return out


n = int(sys.argv[1])
x = np.random.rand(n).astype(np.float32)
x_device = cuda.to_device(x)
out = reduce(x_device).copy_to_host()
print(out[0])