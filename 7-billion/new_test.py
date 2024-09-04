import pickle as pkl

import numpy as np

populated_clusters = np.load('../../data/clustered_ids_10000_populated_parallel.pkl', allow_pickle=True)
print(len(populated_clusters))
# get number of objects in each list
populated_clusters = [len(cluster) for cluster in populated_clusters]
np.savetxt('../../data/populated_clusters_10000_parallel.csv', populated_clusters)