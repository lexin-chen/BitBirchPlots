import re
import numpy as np
import glob
import os

def process_line(line):
    # Split the line by commas and take up to the first 10 elements
    elements = line.split(',')[:10]
    # Attempt to convert each element to float, skip if conversion fails
    float_elements = []
    for element in elements:
        try:
            float_elements.append(float(element))
        except ValueError:
            # Optionally handle or log the error
            pass
    return float_elements

but_brc_files = glob.glob('../../but_brc_metrics/*.csv')
print(but_brc_files)
if not os.path.exists('descriptor_sim'):
        os.makedirs('descriptor_sim')
for but_brc_file in but_brc_files:
    base_name = os.path.basename(but_brc_file)
    base_name = base_name.split('\\')[-1].split('.csv')[0]
    if not os.path.exists(f'descriptor_sim/{base_name}'):
        os.makedirs(f'descriptor_sim/{base_name}')
    results = []
    with open(but_brc_file, 'r') as file:
        for line in file:
            # Check if the line starts with a digit, negative sign, or quotation mark
            
            if re.match(r'^[\d"-]', line.strip()):
                # check if it doesn't start with a space
                if not line.startswith(' '):
                    processed_line = process_line(line.strip())
                    results.append(processed_line)
    results = np.array(results)

    unique_values = np.unique(results[:, 1])

    n_unique_values = len(unique_values)
    dict_values = {}
    for i, each in enumerate(unique_values):
        dict_values[each] = []
        # append the whole row to the dictionary if each match with the unique value
        for j, row in enumerate(results):
            if row[1] == each:
                dict_values[each].append(row)
                
        dict_values[each] = np.array(dict_values[each])

    descriptors = ['Calinski-Harabasz Index', 'Davies-Bouldin Index', 'Dunn Index']
    for idx, descriptor in enumerate(descriptors):
        if idx == 0:
            cols = [4, 5]
        elif idx == 1:
            cols = [6, 7]
        elif idx == 2:
            cols = [8, 9]
        import matplotlib.pyplot as plt
        plt.rcParams.update({'font.size': 14, 'font.weight': 'bold'})

        fig, ax = plt.subplots(5, 1, figsize=(10, 20))

        for i in range(5):
            ax[i].plot(dict_values[unique_values[i]][:, 0], dict_values[unique_values[i]][:, cols[0]], 
                    label='Taylor-Butina', linewidth=8, linestyle='--', c='#005cde')
            ax[i].plot(dict_values[unique_values[i]][:, 0], dict_values[unique_values[i]][:, cols[1]], 
                    label='BitBirch', linewidth=8, c='#f99200', alpha=0.8)
            
            ax[i].set_title(f'Min size: {int(unique_values[i])}', fontsize=14, fontweight='bold')
            ax[i].set_xlim(0.3, 0.8)
            if i != 4:
                ax[i].xaxis.set_tick_params(labelbottom=False)
                ax[i].set_xticklabels(ax[i].get_xticks())
            
            if idx == 0:
                x_data = dict_values[unique_values[i]][:, 0]
                y_data = dict_values[unique_values[i]][:, cols[0]]
                y1_data = dict_values[unique_values[i]][:, cols[1]]
                filtered_y_data = y_data[(x_data >= 0.3) & (x_data <= 0.8)]
                filtered_y1_data = y1_data[(x_data >= 0.3) & (x_data <= 0.8)]
                # figure which y_data is the largest
                if max(filtered_y_data) > max(filtered_y1_data):
                    # Set the y-axis limits based on the filtered y_data
                    ax[i].set_ylim(min(filtered_y_data) - 100, max(filtered_y_data) + 100)
                else:
                    # Set the y-axis limits based on the filtered y_data
                    ax[i].set_ylim(min(filtered_y1_data) - 100, max(filtered_y1_data) + 100)
                if min(filtered_y_data) < min(filtered_y1_data):
                    ax[i].set_ylim(min(filtered_y_data) - 100, max(filtered_y1_data) + 100)

            ax[i].tick_params(axis='both', which='major', length=8, width=2)  # Adjust for major ticks
            for axis in ['top', 'bottom', 'left', 'right']:
                ax[i].spines[axis].set_linewidth(2)
        # create a legend
        fig.text(0.5, 0.07, 'Similarity Threshold', ha='center', fontsize=20, fontweight='bold')
        # one y axis label
        fig.text(0.01, 0.5, descriptor, va='center', rotation='vertical', fontsize=20, fontweight='bold')
        plt.savefig(f'descriptor_sim/{base_name}/{descriptor}.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)