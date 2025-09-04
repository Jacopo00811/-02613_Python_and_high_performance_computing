import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import time

def mandelbrot_escape_time(c):
    z = 0
    for i in range(100):
        z = z**2 + c
        if np.abs(z) > 2.0:
            return i
    return 100

def generate_mandelbrot_set_chunks(points, num_processes):
    chunk_size = len(points) // num_processes
    chunks = [points[i:i + chunk_size] for i in range(0, len(points), chunk_size)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(mandelbrot_escape_time_chunk, chunks)

    escape_times = np.concatenate(results)
    return escape_times

def mandelbrot_escape_time_chunk(chunk):
    return np.array([mandelbrot_escape_time(c) for c in chunk])

def plot_mandelbrot(escape_times):
    plt.imshow(escape_times, cmap='hot', extent=(-2, 2, -2, 2))
    plt.axis('off')
    plt.savefig('mandelbrot.png', bbox_inches='tight', pad_inches=0)

def measure_speedup(points, num_proc_list):
    times = []
    for num_proc in num_proc_list:
        start_time = time.time()
        generate_mandelbrot_set_chunks(points, num_proc)
        end_time = time.time()
        times.append(end_time - start_time)
    return times

def plot_speedup(num_proc_list, times):
    speedup = [times[0] / t for t in times]
    plt.figure()
    plt.plot(num_proc_list, speedup, label='Measured Speedup', marker='o')
    
    # Amdahl's Law
    parallel_fraction = 0.85
    amdahl_speedup = [1 / ((1 - parallel_fraction) + (parallel_fraction / p)) for p in num_proc_list]
    plt.plot(num_proc_list, amdahl_speedup, label='Amdahl\'s Law (85% parallel)', linestyle='--', color='blue')
    
    plt.xlabel('Number of Processes')
    plt.ylabel('Speedup')
    plt.legend()
    plt.title('Speedup vs Number of Processes')
    plt.grid(True)
    plt.savefig('speedup_plot.png')
    plt.show()

if __name__ == "__main__":
    width = 800
    height = 800
    xmin, xmax = -2, 2
    ymin, ymax = -2, 2
    num_proc_list = [1, 2, 4, 8, 16]

    # Precompute points
    x_values = np.linspace(xmin, xmax, width)
    y_values = np.linspace(ymin, ymax, height)
    points = np.array([complex(x, y) for x in x_values for y in y_values])

    # Measure speedup
    times = measure_speedup(points, num_proc_list)

    # Plot speedup
    plot_speedup(num_proc_list, times)