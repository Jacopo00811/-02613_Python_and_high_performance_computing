import cupy as cp
import sys
import time
from code import distance_matrix_oneloop, distance_matrix_noloop

def load_locations(filepath):
    """Load location data from CSV file"""
    # Using CuPy to load and process the data
    data = cp.loadtxt(filepath, delimiter=',', skiprows=1, usecols=(1, 2))
    return data

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path-to-data>")
        sys.exit(1)
    
    data_path = sys.argv[1]
    
    # Load the data
    print(f"Loading data from {data_path}...")
    locations = load_locations(data_path)
    print(f"Loaded {len(locations)} locations")
    
    # Run and time the oneloop version
    print("\nRunning distance_matrix_oneloop...")
    start_time = time.time()
    D_oneloop = distance_matrix_oneloop(locations, locations)
    end_time = time.time()
    oneloop_time = end_time - start_time
    print(f"Distance matrix shape: {D_oneloop.shape}")
    print(f"Time taken: {oneloop_time:.4f} seconds")
    
    # Run and time the noloop version
    print("\nRunning distance_matrix_noloop...")
    start_time = time.time()
    D_noloop = distance_matrix_noloop(locations, locations)
    end_time = time.time()
    noloop_time = end_time - start_time
    print(f"Distance matrix shape: {D_noloop.shape}")
    print(f"Time taken: {noloop_time:.4f} seconds")
    
    # Compare the results
    print("\nComparison:")
    print(f"Oneloop time: {oneloop_time:.4f} seconds")
    print(f"Noloop time: {noloop_time:.4f} seconds")
    print(f"Speedup: {oneloop_time/noloop_time:.2f}x")
    
    # Verify that results are the same
    max_diff = cp.abs(D_oneloop - D_noloop).max().item()
    print(f"Maximum difference between results: {max_diff:.8f}")

if __name__ == "__main__":
    main()
