import numpy as np
import pickle as pkl


def distance(x, y):
    return np.dot(x, y)/(np.dot(x, x) + np.dot(y, y) - np.dot(x, y))


# read pkl
with open('../../data/clustered_ids_billion_parallel.pkl', 'rb') as f:
    data = pkl.load(f)
    
# calculating the number of object in each key
# take only the first 10000 most populated keys
populated_keys = sorted(data.keys(), key=lambda x: len(data[x]), reverse=True)[:10000]

# write it to a file

with open('../../data/centroids_billion_parallel.pkl', 'rb') as f:
    centroids = pkl.load(f)

# only take the top 10000 keys
centroids = {key: centroids[key] for key in populated_keys}

# calculate the distance between each pair of centroids and write out a distance matrix
distances = np.zeros((10000, 10000))
for i, key1 in enumerate(populated_keys):
    for j, key2 in enumerate(populated_keys):
        distances[i, j] = distance(centroids[key1], centroids[key2])

np.save('../../data/distances_billion_parallel.npy', distances)



