import numpy as np

distance_matrix = np.load('../../data/distances_billion_parallel.npy')
print(distance_matrix[:10], distance_matrix.shape)
sim_matrix = np.load('../../data/sim_billion_parallel.npy')
print(sim_matrix[:10], sim_matrix.shape)