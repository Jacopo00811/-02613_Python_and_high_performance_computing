import random
import multiprocessing
import time
import matplotlib.pyplot as plt
import os
import numpy as np

def sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    if x**2 + y**2 <= 1:
        return 1
    else:
        return 0

def sample_multiple(samples_partial):
    return sum(sample() for _ in range(samples_partial))

def measure_time(n_proc, samples):
    chunk_size = samples // n_proc
    pool = multiprocessing.Pool(n_proc)
    results_async = [pool.apply_async(sample_multiple, (chunk_size,))
                     for i in range(n_proc)]
    hits = sum(r.get() for r in results_async)
    pool.close()
    pool.join()
    pi = 4.0 * hits / samples
    return pi

if __name__ == '__main__':
    samples = 1000000
    max_threads = os.cpu_count()
    times = []

    for n_proc in range(1, max_threads + 1):
        start_time = time.time()
        measure_time(n_proc, samples)
        end_time = time.time()
        times.append(end_time - start_time)
        print(f"n_proc: {n_proc}, time: {end_time - start_time:.4f} seconds")

    speedup = [times[0] / t for t in times]

    # Estimate parallel fraction
    P = 0.85  # Adjust this value to fit the curve
    theoretical_speedup = [1 / ((1 - P) + (P / n)) for n in range(1, max_threads + 1)]
    
    plt.plot(theoretical_speedup, marker='o', label='Theoretical Speedup', color='blue')
    plt.plot(range(1, max_threads + 1), speedup, marker='o', label='Measured Speedup', color='red')
    plt.xlabel('Number of Processes')
    plt.ylabel('Speedup')
    plt.title('Speedup and theoretical speedup vs Number of Processes')
    plt.legend()
    plt.grid(True)
    plt.savefig('speedupAndTheoreticalSpeedup.png')
    