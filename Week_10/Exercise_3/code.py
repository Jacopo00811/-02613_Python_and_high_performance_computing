import numpy as np
from numba import cuda
import math

# Reduction kernel using shared memory
@cuda.jit
def reduction_kernel(input_array, output_array):
    # Thread and block indices
    tx = cuda.threadIdx.x
    bx = cuda.blockIdx.x
    bDimX = cuda.blockDim.x
    
    # Allocate shared memory for the block
    shared_array = cuda.shared.array(shape=1024, dtype=np.float32)
    
    # Global index for this thread
    i = tx + bx * bDimX
    
    # Initialize shared memory with zeros
    shared_array[tx] = 0.0
    
    # Load data from global to shared memory
    if i < input_array.size:
        shared_array[tx] = input_array[i]
    
    # Ensure all threads have loaded their data
    cuda.syncthreads()
    
    # Perform reduction in shared memory
    s = bDimX // 2
    while s > 0:
        if tx < s:
            shared_array[tx] += shared_array[tx + s]
        cuda.syncthreads()
        s //= 2
    
    # Write the result for this block back to global memory
    if tx == 0:
        output_array[bx] = shared_array[0]

# Example usage
def run_reduction():
    # Create input data
    data_size = 1_000_000
    data = np.ones(data_size, dtype=np.float32)
    
    # Calculate grid and block dimensions
    threads_per_block = 1024
    blocks_per_grid = math.ceil(data_size / threads_per_block)
    
    # Allocate memory for output
    d_output = np.zeros(blocks_per_grid, dtype=np.float32)
    
    # Copy data to device
    d_data = cuda.to_device(data)
    d_output = cuda.to_device(d_output)
    
    # Launch the kernel
    reduction_kernel[blocks_per_grid, threads_per_block](d_data, d_output)
    
    # If we need further reduction for multiple blocks
    while blocks_per_grid > 1:
        # Update sizes for the next reduction
        threads_per_block = min(blocks_per_grid, 1024)
        new_blocks = math.ceil(blocks_per_grid / threads_per_block)
        
        # Create new output array
        new_output = np.zeros(new_blocks, dtype=np.float32)
        new_output = cuda.to_device(new_output)
        
        # Launch kernel for the next level of reduction
        reduction_kernel[new_blocks, threads_per_block](d_output, new_output)
        
        # Update for next iteration
        blocks_per_grid = new_blocks
        d_output = new_output
    
    # Get final result
    result = d_output.copy_to_host()[0]
    print(f"Sum: {result} (expected: {data_size})")

if __name__ == "__main__":
    run_reduction()
