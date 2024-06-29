import sys
sys.path.insert(0, "../../../BIRCH")
from isim.isim_birch import Birch
from isim.isim_comp import calculate_isim, calculate_medoid
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from adjustText import adjust_text
from rdkit import Chem
from rdkit.Chem import Draw

# Read the fingerprints
fps = np.load('../../../BIRCH/data/chembl_33_np.npy', mmap_mode='r')
smiles = np.loadtxt('../../../BIRCH/data/chembl_33_np.csv', delimiter=',', usecols=1, dtype=str)
print(fps.shape, len(smiles))

# Create 5 white spaces for subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))  # 2x2 grid of subplots, resulting in a 2D array

plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'bold'
font_size = 12
fontweight = 'bold'

for i, t in enumerate([0.35, 0.5, 0.65, 0.8]):
    # Fit the Birch model
    brc = Birch(n_clusters=None, branching_factor=50, threshold=t)
    brc.fit(fps)

    # Get the centroids fingerprints
    centroids = brc.get_centroids()
    
    # get closest structure to centroid with isim
    
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
    medoid_smiles = []
    for j, cluster in enumerate(clusters):
        if big_clusters[j]:
            fps_cluster = fps[cluster]
            isim = calculate_isim(fps_cluster, n_ary='JT')
            color_labels.append(isim)
            medoid = calculate_medoid(fps_cluster, n_ary='JT')
            medoid_smiles.append(smiles[medoid])
    # visualize the smiles
    mols = [Chem.MolFromSmiles(s) for s in medoid_smiles]
    img = Draw.MolsToGridImage(mols, molsPerRow=5, subImgSize=(200, 200))
    img.save(f'cluster_{i}.png')
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
    
    if i == 0:
        ax.xaxis.set_tick_params(labelbottom=False)
    if i == 1:
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.yaxis.set_tick_params(labelleft=False)
    if i == 3:
        ax.yaxis.set_tick_params(labelleft=False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add a colorbar only to the last plot

    scatter = ax.scatter(pca['PCA1'], pca['PCA2'], c=color_labels, cmap='rainbow', 
                         alpha=0.7, s=num_elements * 0.35, edgecolors='black', linewidth=0.1)
    if i == 3:
        # adjust
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
    
plt.savefig('PCA_colors.png', dpi=500, bbox_inches='tight', pad_inches=0.1)