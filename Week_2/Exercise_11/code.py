import numpy as np
import sys
diagonal = np.array([float(x) for x in sys.argv[1:]])
matrix = np.zeros((len(diagonal), len(diagonal)))
np.fill_diagonal(matrix, diagonal)
np.save('diagonal.npy', matrix)