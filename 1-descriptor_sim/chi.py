import re
import numpy as np

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

results = []
with open('../../but_brc_metrics/CHEMBL204_Ki_fp_but_brc.csv', 'r') as file:
    for line in file:
        # Check if the line starts with a digit, negative sign, or quotation mark
        
        if re.match(r'^[\d"-]', line.strip()):
            # check if it doesn't start with a space
            if not line.startswith(' '):
                processed_line = process_line(line.strip())
                results.append(processed_line)

# At this point, `results` contains the processed lines with up to the first 10 elements from each line.
# Further processing or conversion to the desired format can be done as needed.

results = np.array(results)

# read the column 2 and separate result based on the value
# find number of unique values in column 2
unique_values = np.unique(results[:, 1])

n_unique_values = len(unique_values)
dict_values = {}
for i, each in enumerate(unique_values):
    dict_values[each] = []
    # append the whole row to the dictionary if each match with the unique value
    for j, row in enumerate(results):
        if row[1] == each:
            dict_values[each].append(row)

# if column 5 or 6 is 0, delete the row
#results = results[results[:, 4] != 0]
# graph 5 and 6
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12, 'font.weight': 'bold'})
# create subplots
fig, ax = plt.subplots(5, 1, figsize=(10, 20))

for i in range(5):
    ax[i].plot(results[:, 0], results[:, 4], label='Taylor-Butina')
    ax[i].plot(results[:, 0], results[:, 5], label='Birch')
    
    ax[i].set_title(f'Min size: {unique_values[i]}', fontsize=12, fontweight='bold')
# create a legend
ax[0].legend()
fig.text(0.5, 0.04, 'Similarity Threshold', ha='center', fontsize=12, fontweight='bold')
# one y axis label
fig.text(0.04, 0.5, 'Calinski-Harabasz Index', va='center', rotation='vertical', fontsize=12, fontweight='bold')
plt.savefig('similarity.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)
