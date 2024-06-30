import numpy as np
import pandas as pd
import glob

but_brc_files = glob.glob('../../but_brc_metrics/*.csv')
data = pd.read_csv(but_brc_files[0])
print(data.head())