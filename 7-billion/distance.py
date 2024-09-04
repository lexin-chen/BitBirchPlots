import pickle as pkl

import numpy as np


def distance(x, y):
    return 1 - (np.dot(x, y)/(np.dot(x, x) + np.dot(y, y) - np.dot(x, y)))

with open('../../data/clustered_ids_billion_parallel.pkl', 'rb') as f:
    data = pkl.load(f)
# this is a list o
# calculating the number of object in each key
# take only the first 10000 most populated keys
populated_indices = sorted(range(len(data)), key=lambda x: len(data[x]), reverse=True)[:10000]

populated_clusters = [data[i] for i in populated_indices]
print(len(populated_clusters))
# get the number of objects in each key
populated_clusters = [len(cluster) for cluster in populated_clusters]
np.save('../../data/populated_clusters_billion_parallel.npy', populated_clusters)
"""
with open('../../data/clustered_ids_10000_populated_parallel.pkl', 'wb') as f:
    pkl.dump(populated_clusters, f)
    
# write it to a file
with open('../../data/centroids_billion_parallel.pkl', 'rb') as f:
    billion_centroids = pkl.load(f)

# only take the top 10000 keys
# centroid is a list of list: get the centroid of populated indices
centroids = [billion_centroids[i] for i in populated_indices]
with open ('../../data/10000_centroids_parallel.pkl', 'wb') as f:
    pkl.dump(centroids, f)

# calculate the distance between each pair of centroids and write out a distance matrix
distances = np.zeros((10000, 10000))
for i in range(10000):
    for j in range(i, 10000):
        distances[i, j] = distance(centroids[i], centroids[j])
        distances[j, i] = distances[i, j]

np.save('../../data/distances_billion_parallel_new.npy', distances)
"""