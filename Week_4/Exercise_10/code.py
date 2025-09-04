import sys
import numpy as np

# @profile
# def distance_matrix(p1, p2):
#     p1, p2 = np.radians(p1), np.radians(p2)
#     dsin2 = np.sin(0.5 * (p1[:, np.newaxis, :] - p2[np.newaxis, :, :])) ** 2
#     cosprod = np.cos(p1[:, np.newaxis, 0]) * np.cos(p2[np.newaxis, :, 0])
#     a = dsin2[..., 0] + cosprod * dsin2[..., 1]
#     D = 2 * np.arcsin(np.sqrt(a))
#     D *= 6371  # Earth radius in km
#     return D

def distance_matrix(p1, p2):
    p1, p2 = np.radians(p1), np.radians(p2)

    cors_m = np.cos(p1[:,None, 0] )*np.cos( p2[:, 0])
    D = p1[:,None,:] - p2
    D = np.sin(0.5 * D) ** 2

    aM = D[:, :, 0] + cors_m * D[:,: ,1]
    D = 2* np.arcsin(np.sqrt(aM))
    D*=6371
    return D

@profile
def distance_matrix(p1, p2):
    # Convert to radians
    p1 = np.radians(p1)
    p2 = np.radians(p2)
    
    # Reshape for broadcasting: latitudes and longitudes.
    lat1 = p1[:, 0][:, None]  # shape (n, 1)
    lon1 = p1[:, 1][:, None]  # shape (n, 1)
    lat2 = p2[:, 0][None, :]  # shape (1, m)
    lon2 = p2[:, 1][None, :]  # shape (1, m)
    
    # Compute differences
    dlat = lat1 - lat2
    dlon = lon1 - lon2
    
    # Haversine formula
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    D = 6371 * c  # Earth radius in km
    return D


def load_points(fname):
    data = np.loadtxt(fname, delimiter=',', skiprows=1, usecols=(1, 2))
    return data


def distance_stats(D):
    # Extract upper triangular part to avoid duplicate entries
    assert D.shape[0] == D.shape[1], 'D must be square'
    idx = np.triu_indices(D.shape[0], k=1)
    distances = D[idx]
    return {
        'mean': float(distances.mean()),
        'std': float(distances.std()),
        'max': float(distances.max()),
        'min': float(distances.min()),
    }


fname = sys.argv[1]
points = load_points(fname)
D = distance_matrix(points, points)
stats = distance_stats(D)
print(stats)