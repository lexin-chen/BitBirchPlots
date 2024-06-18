import sys
sys.path.insert(0, "../")
from isim.isim_birch import Birch
from isim.isim_comp import calculate_isim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from adjustText import adjust_text

# Read the fingerprints
fps = np.load('../data/chembl_33_np.npy', mmap_mode='r')
print(fps.shape)

# Create 5 white spaces for subplots

fig, axs = plt.subplots(2, 2, figsize=(10, 8))  # 2x2 grid of subplots, resulting in a 2D array


plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'bold'
font_size = 12
fontweight = 'bold'

for i, t in enumerate([0.35, 0.5, 0.65, 0.8]):
    print(i, t)
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
    num_elements = np.array([len(cluster) for cluster in clusters if len(cluster) > 100])

    # Get color labels
    color_labels = []
    for j, cluster in enumerate(clusters):
        if big_clusters[j]:
            fps_cluster = fps[cluster]
            isim = calculate_isim(fps_cluster, n_ary='JT')
            color_labels.append(isim)


    # Plot the PCA components, make each point size proportional to the number of elements in the cluster
    if i == 0:  
        ax = axs[0, 0]
    elif i == 1:
        ax = axs[0, 1]
    elif i == 2:
        ax = axs[1, 0]
    elif i == 3:
        ax = axs[1, 1]

    ax.set_xlim(-8, 35)
    ax.set_ylim(-18, 9)

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
plt.savefig('colors.png')