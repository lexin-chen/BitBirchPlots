import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
# Example distance matrix

distance_matrix = np.load('../../data/distances_billion_parallel.npy')[::100]
# Example coordinates of points
# random 10000 points
points = np.load('../../data/pca_matrix_billion_parallel.npy')[::100]
# Create a graph
G = nx.Graph()
# Add nodes with positions
for i, (x, y) in enumerate(points):
    G.add_node(i, pos=(x, y))
# Add edges with weights from the distance matrix
for i in range(len(distance_matrix)):
    for j in range(i + 1, len(distance_matrix)):
        distance = distance_matrix[i, j]
        if distance > 0:  # Add edge only if there is a non-zero distance
            G.add_edge(i, j, weight=distance)
# Get positions of nodes for plotting
pos = nx.get_node_attributes(G, 'pos')
# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_size=300)
# Draw the edges with varying opacity
for (i, j, weight) in G.edges(data='weight'):
    opacity = 1 / (1 + weight)  # Example function for opacity
    nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], alpha=opacity, width=2)
# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')
plt.title('Network with Edges Varying in Opacity Based on Distance')
plt.savefig('network.png', dpi=500, bbox_inches='tight', pad_inches=0.1)