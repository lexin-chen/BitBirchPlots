# Example distance matrix
distance_matrix = np.array([
    [0, 1, 2, 3],
    [1, 0, 1, 4],
    [2, 1, 0, 5],
    [3, 4, 5, 0]
])
# Example coordinates of points
points = np.array([
    [0, 0],
    [1, 0],
    [0, 1],
    [1, 1]
])
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
plt.show()