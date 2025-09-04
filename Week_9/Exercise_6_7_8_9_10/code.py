# 2. CUDA Vector Addition
from numba import cuda
import numpy as np
import time

@cuda.jit
def add_kernel_size(x, y, out, size):
    idx = cuda.grid(1)
    if idx < size:
        out[idx] = x[idx] + y[idx]

def get_bpg(n, tpb):
    return (n+(tpb-1))//tpb

tpb = 512
size = 1000000
x = np.random.rand(size)
y = np.random.rand(size)
out = np.zeros(size)
bpg = get_bpg(size, tpb)

# ---------- EXPERIMENT 1: NORMAL ARRAYS ----------
d_x_warmup = cuda.to_device(x)
d_y_warmup = cuda.to_device(y)
d_out_warmup = cuda.to_device(out)
add_kernel_size[bpg, tpb](d_x_warmup, d_y_warmup, d_out_warmup, size)
cuda.synchronize()

# Timing normal array transfer + execution + transfer back
start = time.time()
d_x = cuda.to_device(x)
d_y = cuda.to_device(y)
d_out = cuda.to_device(out)
add_kernel_size[bpg, tpb](d_x, d_y, d_out, size)
cuda.synchronize()
result = d_out.copy_to_host()
end = time.time()
print(f"Normal kernel add (including transfers): {end-start}")

# ---------- EXPERIMENT 2: PINNED MEMORY ----------
x_pinned = cuda.pinned_array(size, dtype=np.float64)
y_pinned = cuda.pinned_array(size, dtype=np.float64)
out_pinned = cuda.pinned_array(size, dtype=np.float64)
x_pinned[:] = x
y_pinned[:] = y

# JIT warmup for pinned arrays
d_x_pinned_warmup = cuda.to_device(x_pinned)
d_y_pinned_warmup = cuda.to_device(y_pinned)
d_out_pinned_warmup = cuda.to_device(out_pinned)
add_kernel_size[bpg, tpb](d_x_pinned_warmup, d_y_pinned_warmup, d_out_pinned_warmup, size)
cuda.synchronize()

# Timing pinned memory transfer + execution + transfer back
start = time.time()
d_x_pinned = cuda.to_device(x_pinned)
d_y_pinned = cuda.to_device(y_pinned)
d_out_pinned = cuda.to_device(out_pinned)
add_kernel_size[bpg, tpb](d_x_pinned, d_y_pinned, d_out_pinned, size)
cuda.synchronize()
result_pinned = d_out_pinned.copy_to_host()
end = time.time()
print(f"Kernel with pinned memory (including transfers): {end-start}")

# ---------- EXPERIMENT 3: GPU MEMORY ONLY ----------
d_x = cuda.to_device(x)
d_y = cuda.to_device(y)
d_out = cuda.to_device(np.zeros(size))

# JIT warmup (reusing existing GPU arrays)
add_kernel_size[bpg, tpb](d_x, d_y, d_out, size)
cuda.synchronize()

# Timing ONLY kernel execution (no transfers)
start = time.time()
add_kernel_size[bpg, tpb](d_x, d_y, d_out, size)
cuda.synchronize()
end = time.time()
print(f"Kernel execution only (arrays already on GPU): {end-start}")