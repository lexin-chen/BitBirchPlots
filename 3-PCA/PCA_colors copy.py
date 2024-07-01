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
fig, axs = plt.subplots(2, 2)  # 2x2 grid of subplots, resulting in a 2D array
axs[0, 0].plot([0, 1], [0, 1])  # Correct access for 2D array
axs[0, 1].plot([0, 1], [0, 1])

for i, t in enumerate([0.35, 0.5, 0.65, 0.8]):
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
    ax = axs[i]

    # Set the x axis in range [-10, 30]
    ax.set_xlim(-10, 35)
    ax.set_ylim(-20, 10)
    if i == 0:
        ax.xaxis.set_tick_params(labelbottom=False)
    if i == 1:
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.yaxis.set_tick_params(labelleft=False)
    if i == 2:
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.yaxis.set_tick_params(labelleft=False)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Add a colorbar only to the last plot
    if i == 4:
        # give colorbar a label
        cbar = fig.colorbar(scatter, ax=ax, orientation='vertical')
        cbar.set_label('Tanimoto', rotation=270, labelpad=20)

    scatter = ax.scatter(pca['PCA1'], pca['PCA2'], c=color_labels, cmap='rainbow', 
                         alpha=0.7, s=num_elements * 0.3, edgecolors='black', linewidth=0.1)
            
    # Annotate the number of elements in the 5 most populated clusters
    pca_ = pca.copy()
    big_5 = np.argsort(num_elements)[-5:]
    pca_n = pca_.iloc[big_5]
    num_elements = np.array(num_elements)[big_5]

    texts = []
    for k in range(5):
        text = ax.text(pca_n.iloc[k, 0], pca_n.iloc[k, 1], 
                             str(num_elements[k]), fontsize=11, ha='center', fontweight='bold',
                             va='center', c='black')
        texts.append(text)
    # Use adjust_text to automatically adjust the text positions
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='black'), ax=ax)

    #for i in range(5):
    #    ax.text(pca_n.iloc[i, 0] - 2, pca_n.iloc[i, 1], str(num_elements[i]), fontsize=12, c='black')

    ax.set_title(f'Threshold: {t}')
plt.savefig('PCA_colors.png', dpi=500, bbox_inches='tight', pad_inches=0.1)