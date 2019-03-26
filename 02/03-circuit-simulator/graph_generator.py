# Created by Filip Slazyk
# MOwNiT 2
# 2018/2019

import networkx as nx
import csv
import numpy as np
import matplotlib.pyplot as plt

G = nx.grid_graph(dim=[10, 10])

edges = G.edges()

with open('./graphs_csv/graph1.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for edge in edges:
        writer.writerow(tuple(map(lambda x: x[0]*10 + x[1], edge)) + (1,))

writeFile.close()


G = nx.random_partition_graph([10, 10], 0.4, 0.1)

edges = G.edges()

with open('./graphs_csv/graph2.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    for edge in edges:
        writer.writerow(edge)

writeFile.close()

nx.draw_spring(G, with_labels=True)
plt.show()
