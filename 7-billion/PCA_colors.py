import sys
sys.path.insert(0, "../../../BIRCH")
from isim.isim_birch import Birch
from isim.isim_comp import calculate_isim
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from adjustText import adjust_text
import matplotlib
import pickle as pkl

# Read the fingerprints
fps = np.load('../../../BIRCH/data/chembl_33_np.npy', mmap_mode='r')

plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'bold'
font_size = 12
fontweight = 'bold'

min_val, max_val = 0.03,0.9
n = 100
cmap = plt.cm.gnuplot2
cmap_reversed = cmap.reversed()
# reverse the colors
colors = cmap_reversed(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)


# Get the centroids fingerprints
with open('../../data/10000_centroids_parallel.pkl', 'rb') as f:
    centroids = pkl.load(f)

    # get closest structure to centroid with isim
    
pca = PCA(n_components=2)
pca.fit(centroids)

    # Get the PCA scores for each fingerprint
pca = pd.DataFrame(pca.transform(centroids), columns=['PCA1', 'PCA2'])

# Get the cluster labels
with open('../../data/clustered_ids_10000_populated_parallel.pkl', 'rb') as f:
    clusters = pkl.load(f)
    
n_threshold = 100
    # Get the clusters with more than 50 elements
big_clusters = [len(cluster) > n_threshold for cluster in clusters]

pca = pca[big_clusters]
num_elements = np.array([len(cluster) for cluster in clusters])

# Get color labels
color_labels = []
medoid_smiles = []
for j, cluster in enumerate(clusters):
    if big_clusters[j]:
        fps_cluster = fps[cluster]
        isim = calculate_isim(fps_cluster, n_ary='JT')
        color_labels.append(isim)


fig, ax = plt.subplots()
    
# Add a colorbar only to the last plot

scatter = ax.scatter(pca['PCA1'], pca['PCA2'], c=color_labels, cmap=cmap, 
                        alpha=0.7, s=num_elements * 0.35, edgecolors='black', linewidth=0.1)


fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.25, 0.03, 0.5])
cbar = fig.colorbar(scatter, ax=ax, orientation='vertical', cax=cbar_ax)
cbar.set_label('Tanimoto', rotation=270, labelpad=20, fontsize=font_size, fontweight=fontweight)    
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
        # annotate the smiles images
        
    texts.append(text)
    # Use adjust_text to automatically adjust the text positions
adjust_text(texts, ax=ax)

ax.set_title(f'Threshold: {t}', fontsize=font_size, fontweight='bold')
# increase axes line thickness
ax.spines['top'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.set_xticklabels(ax.get_xticks(), fontweight=fontweight, fontsize=font_size)
ax.set_yticklabels(ax.get_yticks(), fontweight=fontweight, fontsize=font_size)
    
plt.savefig('PCA_colors.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)