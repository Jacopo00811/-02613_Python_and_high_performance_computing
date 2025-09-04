import numpy as np

def distmat_1d(x, y):
    return np.abs(x[:, None] - y)