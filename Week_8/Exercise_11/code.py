import zarr
import sys
import numpy as np
import multiprocessing as mp

def mandelbrot_escape_time(c, max_iter=100):
    z = 0
    for i in range(max_iter):
        z = z**2 + c
        if abs(z) > 2.0:
            return i
    return max_iter

def process_chunk(args):
    """Process a single chunk of the Mandelbrot set"""
    i, j, C, N, xmin, xmax, ymin, ymax, zar_path = args
    
    # Calculate chunk boundaries
    i_end = min(i + C, N)
    j_end = min(j + C, N)
    
    # Get the values for this chunk
    val1 = np.linspace(xmin, xmax, N)
    val2 = np.linspace(ymin, ymax, N)
    
    chunk = np.zeros((i_end - i, j_end - j), dtype=np.int32)
    for ii, x in enumerate(val1[i:i_end]):  
        for jj, y in enumerate(val2[j:j_end]): 
            chunk[ii, jj] = mandelbrot_escape_time(complex(x, y))
    
    # Open the Zarr array in each process to write the chunk
    mandelbrot_array = zarr.open(zar_path, mode="r+")
    mandelbrot_array[i:i_end, j:j_end] = chunk
    
    return (i, j)

if __name__ == "__main__":
    N = int(sys.argv[1])
    C = int(sys.argv[2])

    xmin, xmax = -2, 2
    ymin, ymax = -2, 2

    zar = "mandelbrot.zarr"
    mandelbrot_array = zarr.open(zar, mode="w", shape=(N, N), chunks=(C, C), dtype=np.int32)
    
    chunk_coords = []
    for i in range(0, N, C):
        for j in range(0, N, C):
            chunk_coords.append((i, j, C, N, xmin, xmax, ymin, ymax, zar))
    
    # Determine number of processes (using all available cores)
    num_workers = mp.cpu_count()
    num_chunks = len(chunk_coords)
    print(f"Processing {num_chunks} chunks using {num_workers} processes")

    with mp.Pool(processes=num_workers) as pool:
        for idx, (i, j) in enumerate(pool.imap_unordered(process_chunk, chunk_coords)):
            print(f"Completed chunk ({i},{j}) - {idx+1}/{num_chunks}")
    
    print("All chunks processed successfully")