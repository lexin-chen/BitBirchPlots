import numpy as np
import matplotlib.pyplot as plt
import matplotlib

min_val, max_val = 0.015,0.93
n = 100
cmap = plt.cm.gnuplot2
cmap_reversed = cmap.reversed()
# reverse the colors
colors = cmap_reversed(np.linspace(min_val, max_val, n))
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

fig, (ax1, ax2) = plt.subplots(2,1, figsize=(5,2))
ax1.imshow(gradient, cmap=cmap_reversed, aspect='auto')
ax1.set_title('original')
ax2.imshow(gradient, cmap=cmap, aspect='auto')
ax2.set_title('custom')
plt.tight_layout()
plt.savefig('cmap.png', dpi=500, bbox_inches='tight', pad_inches=0.1, transparent=True)