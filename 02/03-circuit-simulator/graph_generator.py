# Created by Filip Slazyk
# MOwNiT 2
# 2018/2019

import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt

# Random graph n=30 r = 1
G = nx.erdos_renyi_graph(30, 0.2)
edges = G.edges()
with open('./graphs_csv/random_graph.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for edge in edges:
        writer.writerow(edge + (1,))
writeFile.close()

# 3-regular graph n=50 r = 1
G = nx.random_regular_graph(3, 50)
# nx.draw_spring(G, with_labels=True)
# plt.show()
edges = G.edges()
with open('./graphs_csv/3_regular_graph.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for edge in edges:
        writer.writerow(edge + (1,))
writeFile.close()

# Graph with bridge n=40 r in (0,10)
G = nx.erdos_renyi_graph(20, 0.2)
edges = G.edges()
with open('./graphs_csv/graph_with_bridge.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for edge in edges:
        writer.writerow(edge + (1,))
    G = nx.erdos_renyi_graph(20, 0.2)
    edges = G.edges()
    for edge in edges:
        writer.writerow((edge[0] + 20,) + (edge[1] + 20,) + (np.random.rand() * 10,))
    writer.writerow((10, 30, np.random.rand() * 10))  # add bridge
writeFile.close()

# 2D GRID r = 1
G = nx.grid_graph(dim=[10, 10])
edges = G.edges()
with open('./graphs_csv/2D_grid_const_r.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for edge in edges:
        writer.writerow(tuple(map(lambda x: x[0] * 10 + x[1], edge)) + (1,))
writeFile.close()

# 2D GRID r in (0,10)
G = nx.grid_graph(dim=[10, 10])
edges = G.edges()
with open('./graphs_csv/2D_grid_var_r.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for edge in edges:
        writer.writerow(tuple(map(lambda x: x[0] * 10 + x[1], edge))
                        + (np.random.rand() * 10,))
writeFile.close()

# G = nx.random_partition_graph([10, 10], 0.4, 0.1)
#
# edges = G.edges()
#
# with open('./graphs_csv/graph2.csv', 'w') as writeFile:
#     writer = csv.writer(writeFile)
#     for edge in edges:
#         writer.writerow(edge)
#
# writeFile.close()
#
# nx.draw_spring(G, with_labels=True)
# plt.show()
