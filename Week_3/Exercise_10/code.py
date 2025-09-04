import sys
from time import perf_counter
import os
import blosc
import numpy as np

def write_numpy(arr, file_name):
    np.save(f"{file_name}.npy", arr)
    os.sync()


def write_blosc(arr, file_name, cname="lz4"):
    b_arr = blosc.pack_array(arr, cname=cname)
    with open(f"{file_name}.bl", "wb") as w:
        w.write(b_arr)
    os.sync()


def read_numpy(file_name):
    return np.load(f"{file_name}.npy")


def read_blosc(file_name):
    with open(f"{file_name}.bl", "rb") as r:
        b_arr = r.read()
    return blosc.unpack_array(b_arr)


lst = [int(n) for n in sys.argv[1:]]
for n in lst:
    ten = np.random.randint(0, 256, size=(n, n, n), dtype='uint8')
    start = perf_counter()
    write_numpy(ten, "numpy")
    end = perf_counter()
    print(f"Write time numpy: {end - start} for {n}")

    start = perf_counter()
    write_blosc(ten, "blosc")
    end = perf_counter()
    print(f"Write time blosc: {end - start} for {n}")

    start = perf_counter()
    read_numpy("numpy")
    end = perf_counter()
    print(f"Read time numpy: {end - start}  for {n}")

    start = perf_counter()
    read_blosc("blosc")
    end = perf_counter()
    print(f"Read tim blosc: {end - start} for {n}")








