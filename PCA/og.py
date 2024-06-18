from isim_birch import Birch
from isim_comp import calculate_isim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# Read the fingerprints
fps = np.load('chembl_33_np.npy', mmap_mode='r')
print(fps.shape)

# Create 5 white spaces for subplots
fig, axs = plt.subplots(1, 5, figsize=(20, 4))

for i, t in enumerate([0.2, 0.35, 0.5, 0.65, 0.8]):
    # Fit the Birch model
    brc = Birch(n_clusters=None, branching_factor=50, threshold=t)
    brc.fit(fps)

    # Get the centroids fingerprints
    centroids = brc.get_centroids()

    # Fit the centroids to PCA
    pca = PCA(n_components=2)
    pca.fit(centroids)

    # Get the PCA scores for each fingerprint
    pca = pd.DataFrame(pca.transform(centroids), columns=['PCA1', 'PCA2'])

    # Get the cluster labels
    clusters = brc.get_cluster_mol_ids()

    n_threshold = 100
    # Get the clusters with more than 50 elements
    big_clusters = [len(cluster) > n_threshold for cluster in clusters]

    pca = pca[big_clusters]
    num_elements = [len(cluster) for cluster in clusters if len(cluster) > 100]

    # Get color labels
    color_labels = []
    for j, cluster in enumerate(clusters):
        if big_clusters[j]:
            fps_cluster = fps[cluster]
            isim = calculate_isim(fps_cluster, n_ary='JT')
            color_labels.append(isim)


    # Plot the PCA components, make each point size proportional to the number of elements in the cluster
    ax = axs[i]

    # Set the x axis in range [-10, 30]
    ax.set_xlim(-10, 30)

    # Set the y axis in range [-10, 30]
    ax.set_ylim(-10, 30)

    scatter = ax.scatter(pca['PCA1'], pca['PCA2'], c=color_labels, cmap='rainbow', alpha=0.5, s=num_elements)

    # Add a colorbar only to the last plot
    if i == 4:
        fig.colorbar(scatter, ax=ax)
    
    # Annotate the number of elements in the 5 most populated clusters
    pca_ = pca.copy()
    big_5 = np.argsort(num_elements)[-5:]
    pca_n = pca_.iloc[big_5]
    num_elements = np.array(num_elements)[big_5]

    for i in range(5):
        ax.text(pca_n.iloc[i, 0], pca_n.iloc[i, 1], str(num_elements[i]), fontsize=12, c='black')

    ax.set_title(f'Threshold: {t}')
plt.show()