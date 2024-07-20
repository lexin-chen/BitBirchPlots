import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import re

if not os.path.exists(f'../../parallel_plots'):
        os.makedirs(f'../../parallel_plots')

parallel_file = '../../parallel_data/francesca_birch_vs_para.csv'
data = pd.read_csv(parallel_file)

descriptors = ['Number of Clusters', 'Calinski-Harabasz Index', 'Davies-Bouldin Index', 'Dunn Index', ]
plt.rcParams.update({'font.size': 12, 'font.weight': 'bold'})
for d_idx, descriptor in enumerate(descriptors):
    if descriptor == 'Number of Clusters':
        cols = [1, 2]
    elif descriptor == 'Calinski-Harabasz Index':
        cols = [3, 4]
    elif descriptor == 'Davies-Bouldin Index':
        cols = [5, 6]
    elif descriptor == 'Dunn Index':
        cols = [7, 8]
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    # number for column one
    x_labels = range(len(data.iloc[:, cols[0]])) 
    # add 1 to the number to match the CHEMBL number
    x_labels = [str(int(x)+1) for x in x_labels]
    # chop off first part with CHEMBL only take number
    ax.plot(x_labels, data.iloc[:, cols[0]], label='BitBirch', linestyle='-', 
            color='#f99200', linewidth=2.5)
    ax.plot(x_labels, data.iloc[:, cols[1]], label='BitBirch-parallel', linestyle='-.', 
            color='#4cbb17', linewidth=2.5, alpha=0.8)
    # set a tick for each data point
    ax.set_xticks(x_labels)
    ax.set_xticklabels(x_labels, rotation=45, ha='center')
    ax.tick_params(axis='both', which='major', length=6, width=1.25)  # Adjust for major ticks
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    ax.set_ylabel(descriptor, fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    plt.savefig(f'../../parallel_plots/{descriptor}.png', dpi=500, bbox_inches='tight', pad_inches=0.1)
    plt.close()