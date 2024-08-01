import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

if not os.path.exists(f'../../xor_plots'):
    os.makedirs(f'../../xor_plots')

parallel_file = '../../data/francesca_birch_vs_xorfold.csv'
data = pd.read_csv(parallel_file)

descriptors = ['Medoid Score', 'Set Score']
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
    if descriptor == 'Medoid Score':
        cols = 12
    elif descriptor == 'Set Score':
        cols = 13

    x_labels = range(len(dict_values[unique_values[0]][:, 0])) 
    # add 1 to the number to match the CHEMBL number
    x_labels = [str(int(x)+1) for x in x_labels]
    fig, ax = plt.subplots(1, 1)
    ax.plot(x_labels, dict_values[unique_values[0]][:, cols],
            label='BitBirch_1-Fold', linewidth=2, c='#9200f9', alpha=0.9)
    ax.plot(x_labels, dict_values[unique_values[1]][:, cols], 
            label='BitBirch_2-Fold', linewidth=2, c='#f90067', alpha=0.8)
    ax.plot(x_labels, dict_values[unique_values[2]][:, cols], 
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
