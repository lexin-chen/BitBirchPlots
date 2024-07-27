import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

parallel_file = '../../parallel_data/francesca_birch_vs_para.csv'
data = pd.read_csv(parallel_file)
matrix_types = ['medoid_matrix', 'set_matrix']
plt.rcParams.update({'font.size': 12, 'font.weight': 'bold'})

data = pd.read_csv(parallel_file)
print(len(data))
for idx in range(len(data)):
    lib_name = data.iloc[idx, 0]
    lib_name = lib_name.split('.pkl')[0]
    print(f'Processing {lib_name}, {idx}...')
    if not os.path.exists(f'../../parallel_plots/{lib_name}'):
        os.makedirs(f'../../parallel_plots/{lib_name}')
    
    for i, matrix_type in enumerate(matrix_types):
        data[matrix_type] = data[matrix_type].astype(str).str.replace('\n', '', regex=False)
        matrix_row = data.iloc[[idx]]
        matrix_str = matrix_row[matrix_type].values[0]

        # Split the string into rows
        rows = matrix_str[2:-2].split('] [')
        
        # Convert each row into a list of floats
        matrix = [list(map(float, row.split())) for row in rows]

        # Convert the list of lists into a NumPy 2D array
        matrix_np = np.array(matrix)
        
        # Plot the matrix
        sns.heatmap(matrix_np, cmap="icefire")
        # title
        plt.title(f'{lib_name} medoid matrix')
        if matrix_type == 'medoid_matrix':
            plt.title(f'Medoid Comparison', fontsize=16, fontweight='bold')
        elif matrix_type == 'set_matrix':
            plt.title(f'Set Comparison', fontsize=16, fontweight='bold')

        plt.savefig(f'../../parallel_plots/{lib_name}/{matrix_type}.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close()