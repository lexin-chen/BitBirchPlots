import numpy as np
import pandas as pd
import glob
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

but_brc_files = glob.glob('../../but_brc_metrics/*.csv')
matrix_types = ['medoid_matrix', 'set_matrix']
plt.rcParams.update({'font.size': 16, 'font.weight': 'bold'})

min_val, max_val = 0.2, 1.0
n = 10
orig_cmap = plt.cm.get_cmap('gnuplot2')
colors = orig_cmap(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)

for but_brc_file in but_brc_files:
    base_name = os.path.basename(but_brc_file)
    
    base_name = base_name.split('\\')[-1].split('.csv')[0]
    if not os.path.exists(f'../../descriptor_sim/{base_name}'):
        os.makedirs(f'../../descriptor_sim/{base_name}')
        
    data = pd.read_csv(but_brc_file)
    # look for the row where data['sim_threshold'] == 0.65 and data['min_size'] == 10
    for i, matrix_type in enumerate(matrix_types):
        data[matrix_type] = data[matrix_type].astype(str).str.replace('\n', '', regex=False)
        matrix_row = data[(data['sim_threshold'] == 0.65) & (data['min_size'] == 10)]
        matrix_str = matrix_row[matrix_type].values[0]

        # Split the string into rows
        rows = matrix_str[2:-2].split('] [')

        # Convert each row into a list of floats
        matrix = [list(map(float, row.split())) for row in rows]

        # Convert the list of lists into a NumPy 2D array
        matrix_np = np.array(matrix)

        # Plot the matrix
        if len(matrix_np) > 1:
            print(base_name)
            sns.heatmap(matrix_np, cmap="icefire")
            # title
            plt.title(f'{base_name} medoid matrix')
            if matrix_type == 'medoid_matrix':
                plt.title(f'Medoid Comparison', fontsize=16, fontweight='bold')
            elif matrix_type == 'set_matrix':
                plt.title(f'Set Comparison', fontsize=16, fontweight='bold')

            plt.savefig(f'../../descriptor_sim/{base_name}/{matrix_type}.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)
            plt.close()