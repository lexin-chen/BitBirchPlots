import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

if not os.path.exists(f'../../parallel_plots'):
    os.makedirs(f'../../parallel_plots')

parallel_file = '../../parallel_data/francesca_birch_vs_para.csv'
data = pd.read_csv(parallel_file)

plt.rcParams.update({'font.size': 12, 'font.weight': 'bold'})
descriptor = 'scores'
cols = [11, 12]
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
# number for column one
x_labels = range(len(data.iloc[:, 0])) 
# add 1 to the number to match the CHEMBL number
x_labels = [str(int(x)+1) for x in x_labels]
# chop off first part with CHEMBL only take number
ax.plot(x_labels, data.iloc[:, cols[0]], label='Medoid Score', linestyle='-', 
        color='#f99200', linewidth=2.75)
ax.plot(x_labels, data.iloc[:, cols[1]], label='Set Score', linestyle='-.', 
        color='#4cbb17', linewidth=2.75, alpha=0.9)
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