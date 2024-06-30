import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

but_brc_files = glob.glob('../../but_brc_metrics/*.csv')
descriptors = ['Calinski-Harabasz Index', 'Davies-Bouldin Index', 'Dunn Index']

if not os.path.exists('descriptor_sim'):
    os.makedirs('descriptor_sim')
plt.rcParams.update({'font.size': 14, 'font.weight': 'bold'})

for but_brc_file in but_brc_files:
    base_name = os.path.basename(but_brc_file)
    base_name = base_name.split('\\')[-1].split('.csv')[0]
    if not os.path.exists(f'descriptor_sim/{base_name}'):
        os.makedirs(f'descriptor_sim/{base_name}')
    
    data = pd.read_csv(but_brc_file)
    for idx, descriptor in enumerate(descriptors):
        if idx == 0:
            cols = [4, 5]
        elif idx == 1:
            cols = [6, 7]
        elif idx == 2:
            cols = [8, 9]
    
        unique_values = np.unique(data['sim_threshold'])
        n_unique_values = len(unique_values)
        dict_values = {}

        keys = dict_values.keys()
        n_items = [len(dict_values[key]) for key in keys]
        for i, each in enumerate(unique_values):
            dict_values[each] = []
            for j, row in enumerate(data.values):
                if row[0] == each:
                    dict_values[each].append(row)
            dict_values[each] = np.array(dict_values[each])
        
        # find the mean of the descriptor values
        mean_values_but = []
        mean_values_brc = []
        std_values_but = []
        std_values_brc = []
        
        # find mean and std dev for each similarity threshold
        for key in keys:
            mean_values_but.append(np.mean(dict_values[key][:, cols[0]]))
            mean_values_brc.append(np.mean(dict_values[key][:, cols[1]]))
            std_values_but.append(np.std(dict_values[key][:, cols[0]]))
            std_values_brc.append(np.std(dict_values[key][:, cols[1]]))
        
        # plot the mean values and std dev with a filled area
        fig, ax = plt.subplots()
        ax.plot(keys, mean_values_but, c='#005cde', label='Taylor-Butina', linewidth=2.5, 
                linestyle='--')
        ax.fill_between(keys, np.array(mean_values_but) - np.array(std_values_but),
                        np.array(mean_values_but) + np.array(std_values_but), color='#005cde', alpha=0.2)
        ax.plot(keys, mean_values_brc, c='#f96900', label='BitBirch', alpha=0.8, linewidth=2.5)
        ax.fill_between(keys, np.array(mean_values_brc) - np.array(std_values_brc),
                        np.array(mean_values_brc) + np.array(std_values_brc), color='#f93f00', alpha=0.23)
        
        ax.set_xlabel('Similarity Threshold', fontsize=14, fontweight='bold')
        ax.set_ylabel(descriptor, fontsize=14, fontweight='bold')
        ax.set_xlim(0.3, 0.8)
        if idx == 0:
            # x_data is all the keys
            x_data = np.array(list(keys))
            y_data = np.array(mean_values_but) 
            y1_data = np.array(mean_values_brc) 
            filtered_y_data = y_data[(x_data >= 0.3) & (x_data <= 0.8)]
            filtered_y1_data = y1_data[(x_data >= 0.3) & (x_data <= 0.8)]
            
            # figure which y_data is the largest
            if max(filtered_y_data) > max(filtered_y1_data):
                max_y = max(filtered_y_data)
            else:
                max_y = max(filtered_y1_data)
            if min(filtered_y_data) < min(filtered_y1_data):
                min_y = min(filtered_y_data)
            else:
                min_y = min(filtered_y1_data)
            ax.set_ylim(min_y - 50, max_y + (0.2 * max_y))
        
        ax.tick_params(axis='both', which='major', length=8, width=2)
        ax.legend(fontsize=14, frameon=False)
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(2)
        plt.savefig(f'descriptor_sim/{base_name}/avg_{descriptor}.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close()