import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

but_brc_files = glob.glob('../../but_brc_metrics/CHEMBL204_Ki_fp_but_brc.csv')
descriptors = ['Calinski-Harabasz Index', 'Davies-Bouldin Index', 'Dunn Index']

if not os.path.exists('descriptor_sim'):
    os.makedirs('descriptor_sim')
plt.rcParams.update({'font.size': 16, 'font.weight': 'bold'})

for but_brc_file in but_brc_files:
    base_name = os.path.basename(but_brc_file)
    base_name = base_name.split('\\')[-1].split('.csv')[0]
    if not os.path.exists(f'descriptor_sim/{base_name}'):
        os.makedirs(f'descriptor_sim/{base_name}')
    
    data = pd.read_csv(but_brc_file)
    # unique values are in the second column
    unique_values = np.unique(data['sim_threshold'])
    n_unique_values = len(unique_values)
    dict_values = {}
    for i, each in enumerate(unique_values):
        dict_values[each] = []
        # append the whole row to the dictionary if each match with the unique value
        for j, row in enumerate(data.values):
            if row[0] == each:
                dict_values[each].append(row)
        dict_values[each] = np.array(dict_values[each])
    # get keys and number of items per key
    keys = dict_values.keys()
    n_items = [len(dict_values[key]) for key in keys]
    print(keys, n_items)
    for idx, descriptor in enumerate(descriptors):
        if idx == 0:
            cols = [4, 5]
        elif idx == 1:
            cols = [6, 7]
        elif idx == 2:
            cols = [8, 9]

        fig, ax = plt.subplots(5, 1, figsize=(10, 20))

        # find the mean of the descriptor values
        mean_values_but = []
        mean_values_brc = []
        std_values_but = []
        std_values_brc = []
        # find mean 