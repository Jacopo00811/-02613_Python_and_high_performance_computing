import numpy as np
import sys
path = sys.argv[1]
matrix = np.load(path)
np.save('cols.npy', matrix.mean(axis=0))
np.save('rows.npy', matrix.mean(axis=1))