import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# Custom formatter function
def millions_formatter(x, pos):
    val = f'${{{x * 1e-6:.1f}}} \\cdot 10^6$'
    return val
plt.rcParams.update({'font.size': 12, 'font.weight': 'bold'})
brc_times = np.loadtxt('../../data/pubchem_birch_timing.csv', delimiter=',', skiprows=1, usecols=(0, 1))
but_times = np.loadtxt('../../data/pubchem_but_time_1.csv', delimiter=',', skiprows=1, usecols=(0, 1))


plt.plot(but_times[:, 0], but_times[:, 1], label='Taylor-Butina', linewidth=5, linestyle='--',
         c='#005cde')
plt.plot(brc_times[:, 0], brc_times[:, 1], label='BitBirch', linewidth=5, c='#f99200')
plt.xlabel('Number of molecules', fontsize=14, fontweight='bold')
plt.ylabel('Time (s)', fontsize=14, fontweight='bold')
# Apply the formatter
plt.gca().xaxis.set_major_formatter(FuncFormatter(millions_formatter))
plt.legend(fontsize=14, frameon=False)
for axis in ['top','bottom','left','right']:
    plt.gca().spines[axis].set_linewidth(1.75)
plt.savefig('times.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)