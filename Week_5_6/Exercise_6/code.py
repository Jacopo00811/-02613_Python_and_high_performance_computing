import random
import multiprocessing

def sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    if x**2 + y**2 <= 1:
        return 1
    else:
        return 0

def sample_multiple(samples_partial):
    return sum(sample() for i in range(samples_partial))

if __name__ == '__main__':
    samples = 1000000
    n_proc = 10
    chunk_size = samples // n_proc

    pool = multiprocessing.Pool(n_proc)
    results = pool.map(sample_multiple, [chunk_size] * n_proc)
    hits = sum(results)
    pi = 4.0 * hits / samples
    print(f"Estimated value of Pi: {pi}")
