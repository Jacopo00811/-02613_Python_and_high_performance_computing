import numpy as np
import sys
vec = np.array([float(x) for x in sys.argv[1:]])
print(np.linalg.norm(vec))