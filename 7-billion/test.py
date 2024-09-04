import numpy as np

matrix = np.load('../../data/10000_centroids_parallel.pkl', allow_pickle=True)

# get pca of the matrix
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(matrix)

# get the pca matrix
pca_matrix = pca.transform(matrix)
np.save('../../data/pca_matrix_billion_parallel.npy', pca_matrix)

print(pca_matrix.shape)