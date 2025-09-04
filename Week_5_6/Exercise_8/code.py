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

def generate_mandelbrot_set(points, num_processes):
    with multiprocessing.Pool(processes=num_processes) as pool:
        escape_times = pool.map(mandelbrot_escape_time, points)
    return np.array(escape_times)   

def plot_mandelbrot(escape_times):
    plt.imshow(escape_times, cmap='hot', extent=(-2, 2, -2, 2))
    plt.axis('off')
    plt.savefig('mandelbrot.png', bbox_inches='tight', pad_inches=0)

def measure_time(num_proc, points):
    start_time = time.time()
    mandelbrot_set = generate_mandelbrot_set(points, num_proc)
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    width = 800
    height = 800
    xmin, xmax = -2, 2
    ymin, ymax = -2, 2

    # Precompute points
    x_values = np.linspace(xmin, xmax, width)
    y_values = np.linspace(ymin, ymax, height)
    points = np.array([complex(x, y) for x in x_values for y in y_values])

    # Measure execution time for different numbers of processes
    num_processes_list = [1, 2, 4, 8, 16]
    times = []
    for num_proc in num_processes_list:
        exec_time = measure_time(num_proc, points)
        times.append(exec_time)
        print(f"Execution time with {num_proc} processes: {exec_time:.2f} seconds")

    # Plot speedup
    speedup = [times[0] / t for t in times]
    plt.figure()
    plt.plot(num_processes_list, speedup, marker='o')
    plt.xlabel('Number of Processes')
    plt.ylabel('Speedup')
    plt.title('Speedup vs Number of Processes')
    plt.grid(True)
    plt.savefig('speedup.png')
