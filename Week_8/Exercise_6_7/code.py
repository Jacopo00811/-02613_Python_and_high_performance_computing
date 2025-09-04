import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import sys

def mandelbrot_escape_time(c):
    z = 0
    for i in range(100):
        z = z**2 + c
        if np.abs(z) > 2.0:
            return i
    return 100

def calculate_chunk(args):
    start_idx, end_idx, points, filename, shape = args
    # Create or open the memory-mapped file
    result_array = np.memmap(filename, dtype=np.int32, mode='r+', shape=shape)
    
    # Calculate for this chunk
    for i in range(start_idx, end_idx):
        x_idx = i // shape[1]
        y_idx = i % shape[1]
        result_array[x_idx, y_idx] = mandelbrot_escape_time(points[i])
    
    # Flush changes to disk
    result_array.flush()
    return None

def generate_mandelbrot_set(points, num_processes, width, height):
    # Create a memory-mapped file for results
    filename = 'mandelbrot_data.raw'

    # Create a new memory-mapped file
    result_array = np.memmap(filename, dtype=np.int32, mode='w+', shape=(width, height))
    # Initialize with zeros
    result_array.fill(0)
    result_array.flush()
    
    # Split the work into chunks for each process
    points_count = len(points)
    chunk_size = points_count // num_processes
    chunks = []
    
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else points_count
        chunks.append((start, end, points, filename, (width, height)))
    
    # Process the chunks in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(calculate_chunk, chunks)
    
    # Return the memory-mapped array
    return np.memmap(filename, dtype=np.int32, mode='r', shape=(width, height))

def plot_mandelbrot(escape_times):
    plt.imshow(escape_times, cmap='hot', extent=(-2, 2, -2, 2))
    plt.axis('off')
    plt.savefig('mandelbrot.png', bbox_inches='tight', pad_inches=0)

if __name__ == "__main__":
    # Parse command line arguments
    N = int(sys.argv[1])
    
    width = N
    height = N
    xmin, xmax = -2, 2
    ymin, ymax = -2, 2
    num_processes = 4
    # Precompute points
    x_values = np.linspace(xmin, xmax, width)
    y_values = np.linspace(ymin, ymax, height)
    points = np.array([complex(x, y) for x in x_values for y in y_values])

    # Generate the Mandelbrot set using memory-mapped array
    escape_times = generate_mandelbrot_set(points, num_processes, width, height)
    
    # Plot and save the result
    # plot_mandelbrot(escape_times)
    
    print(f"Mandelbrot set generated with {num_processes} processes")
    print(f"Array size: {N}x{N}")
    print("Results saved to 'mandelbrot.png' and 'mandelbrot_data.raw'")