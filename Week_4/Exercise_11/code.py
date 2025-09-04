import sys
import numpy as np
import time
import matplotlib.pyplot as plt

def distance_matrix_loop(p1, p2):
    p1, p2 = np.radians(p1), np.radians(p2)

    D = np.empty((len(p1), len(p2)))
    for i in range(len(p1)):
        for j in range(len(p2)):
            dsin2 = np.sin(0.5 * (p1[i] - p2[j])) ** 2
            cosprod = np.cos(p1[i, 0]) * np.cos(p2[j, 0])
            a = dsin2[0] + cosprod * dsin2[1]
            D[i, j] = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    D *= 6371  # Earth radius in km
    return D

def distance_matrix(p1, p2):
    # Convert to radians
    p1 = np.radians(p1)
    p2 = np.radians(p2)
    
    # Reshape for broadcasting: latitudes and longitudes.
    lat1 = p1[:, 0][:, None]  # shape (n, 1)
    lon1 = p1[:, 1][:, None]  # shape (n, 1)
    lat2 = p2[:, 0][None, :]  # shape (1, m)
    lon2 = p2[:, 1][None, :]  # shape (1, m)
    
    # Compute differences
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    
    # Haversine formula
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    D = 6371 * c  # Earth radius in km
    return D


# Timing helper
def measure_time(func, n, n_trials=3):
    # Generate n random points (latitude in [-90,90], longitude in [-180,180])
    points = np.random.uniform(low=[-90, -180], high=[90, 180], size=(n, 2))
    # Warmup
    func(points, points)
    times = []
    for _ in range(n_trials):
        start = time.time()
        func(points, points)
        times.append(time.time() - start)
    return np.mean(times)


def load_points(fname):
    data = np.loadtxt(fname, delimiter=',', skiprows=1, usecols=(1, 2))
    return data


def distance_stats(D):
    # Extract upper triangular part to avoid duplicate entries
    assert D.shape[0] == D.shape[1], 'D must be square'
    idx = np.triu_indices(D.shape[0], k=1)
    distances = D[idx]
    return {
        'mean': float(distances.mean()),
        'std': float(distances.std()),
        'max': float(distances.max()),
        'min': float(distances.min()),
    }


# We'll vary n over a range (say, from 10 to 1000 points)
ns = np.unique(np.logspace(1, 3, num=10, dtype=int))
# Compute approximate size of the full distance matrix in kilobytes:
# Each distance is a float64 (8 bytes), so total bytes = 8*n^2, convert to KB.
sizes_kb = 8 * ns**2 / 1024

times_vec = []
times_loop = []
for n in ns:
    t_vec = measure_time(distance_matrix, n)
    t_loop = measure_time(distance_matrix_loop, n)
    times_vec.append(t_vec)
    times_loop.append(t_loop)

# Estimate MFLOP/s.
# Roughly, each distance computation does ~15 floating-point operations.
def mflops(n, t):
    flops = 15 * n**2
    return flops / (t * 1e6)

mflops_vec = [mflops(n, t) for n, t in zip(ns, times_vec)]
mflops_loop = [mflops(n, t) for n, t in zip(ns, times_loop)]

# Plot run times vs. distance matrix size (in KB) on a loglog scale.
plt.figure(figsize=(10, 6))
plt.loglog(sizes_kb, times_vec, 'o-', label='No-loop (fully vectorized)')
plt.loglog(sizes_kb, times_loop, 's-', label='Optimized single loop')
# Mark typical cache sizes (example values; these vary by CPU)
for cache_size, label in zip([32, 256, 8192], ['L1 (32KB)', 'L2 (256KB)', 'L3 (8192KB)']):
    plt.axvline(x=cache_size, color='gray', linestyle='--', label=label if cache_size==32 else None)
plt.xlabel('Distance Matrix Size (KB)')
plt.ylabel('Run time (seconds)')
plt.title('Run time vs. Matrix Size')
plt.legend()
plt.savefig('runtime.png')

# Plot MFLOP/s vs. distance matrix size.
plt.figure(figsize=(10, 6))
plt.loglog(sizes_kb, mflops_vec, 'o-', label='No-loop (fully vectorized)')
plt.loglog(sizes_kb, mflops_loop, 's-', label='Optimized single loop')
plt.xlabel('Distance Matrix Size (KB)')
plt.ylabel('Performance (MFLOP/s)')
plt.title('MFLOP/s vs. Matrix Size')
plt.legend()
plt.savefig('performance.png')