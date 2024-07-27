import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

if not os.path.exists(f'../../xor_plots'):
    os.makedirs(f'../../xor_plots')

parallel_file = '../../data/francesca_birch_vs_xorfold.csv'
data = pd.read_csv(parallel_file)

descriptors = ['Number of Clusters', 'Calinski-Harabasz Index', 'Davies-Bouldin Index', 'Dunn Index', ]
plt.rcParams.update({'font.size': 12, 'font.weight': 'bold'})
    # number for column one
unique_values = np.unique(data['fold'])
n_unique_values = len(unique_values)
dict_values = {}
for i, each in enumerate(unique_values):
    dict_values[each] = []
    # append the whole row to the dictionary if each match with the unique value
    for j, row in enumerate(data.values):
        if row[1] == each:
            dict_values[each].append(row)
    dict_values[each] = np.array(dict_values[each])

for d_idx, descriptor in enumerate(descriptors):
    if descriptor == 'Number of Clusters':
        cols = [2, 3]
    elif descriptor == 'Calinski-Harabasz Index':
        cols = [4, 5]
    elif descriptor == 'Davies-Bouldin Index':
        cols = [6, 7]
    elif descriptor == 'Dunn Index':
        cols = [8, 9]
    x_labels = range(len(dict_values[unique_values[0]][:, 0])) 
    # add 1 to the number to match the CHEMBL number
    x_labels = [str(int(x)+1) for x in x_labels]
    fig, ax = plt.subplots(1, 1)
    ax.plot(x_labels, dict_values[unique_values[i]][:, cols[0]], 
            label='BitBirch', linewidth=3, c='#f99200')
    ax.plot(x_labels, dict_values[unique_values[0]][:, cols[1]], 
            label='BitBirch_1-Fold', linewidth=2, c='#9200f9', alpha=0.9)
    ax.plot(x_labels, dict_values[unique_values[1]][:, cols[1]], 
            label='BitBirch_2-Fold', linewidth=2, c='#f90067', alpha=0.8)
    ax.plot(x_labels, dict_values[unique_values[2]][:, cols[1]], 
            label='BitBirch_3-Fold', linewidth=2, c='#2a0048', alpha=0.6)
    
    ax.set_xticks(x_labels)
    ax.set_xticklabels(x_labels, rotation=45, ha='center')
    ax.tick_params(axis='both', which='major', length=6, width=1.25)  # Adjust for major ticks
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)
    ax.set_ylabel(descriptor, fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    plt.savefig(f'../../xor_plots/{descriptor}.png', dpi=500, bbox_inches='tight', pad_inches=0.1)
    plt.close()
# save first column and the corresponding x label
save_data = np.column_stack((x_labels, dict_values[unique_values[0]][:, 0]))
np.savetxt(f'../../xor_plots/lib_labels.csv', save_data, delimiter=',', fmt='%s', header='Index,Library')