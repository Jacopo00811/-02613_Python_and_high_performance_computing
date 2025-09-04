import sys
import numpy as np
from PIL import Image

path = sys.argv[1]
N = int(sys.argv[2])
n = int(sys.argv[3])

mm = np.memmap(path, dtype=np.int32, mode='r', shape=(N, N))

downsample = mm[::n, ::n]
img = Image.fromarray(downsample)
img.save('downsampled.png')
