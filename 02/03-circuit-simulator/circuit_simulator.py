# Created by Filip Slazyk
# MOwNiT 2
# 2018/2019

import numpy as np
import csv
import networkx as nx
import matplotlib.pyplot as plt


def import_data_from_csv(file):
    G = nx.Graph()
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        j = 0
        for i, row in enumerate(reader):
            if not G.has_edge(int(row[0]), int(row[1])):
                G.add_edge(int(row[0]), int(row[1]), r=abs(float(row[2])), sem=0, id=j + 1, i=0)
                j += 1
    return G


def add_sem(G, node_a, node_b, sem):  # node_a -> (+)sem(-) ->node_b (positive source connected to node_a)
    if node_a > node_b:
        G.add_edge(node_a, node_b, r=0, sem=-sem, id=0, i=0)
    else:
        G.add_edge(node_a, node_b, r=0, sem=sem, id=0, i=0)


def first_kirchhoff_law(G):
    edges_number = G.size()
    sem = []
    a = []  # a - matrix of equations derived from I Kirchhoff's law
    for node in G.nodes:
        row = np.zeros(edges_number)
        sem.append(0)
        for edge in G.edges(node):
            row[G.get_edge_data(*edge).get('id')] = 1 if edge[0] > edge[1] else -1
        a.append(row)
    return a, sem


def second_kirchhoff_law(G):
    edges_number = G.size()
    sem = []
    a = []  # a - matrix of equations derived from II Kirchhoff's law
    for cycle in nx.cycle_basis(G):
        row = [0] * edges_number
        sem.append(0)
        for i in range(len(cycle)):
            node_a = cycle[i]
            node_b = cycle[(i + 1) % len(cycle)]
            edge_data = G.get_edge_data(node_a, node_b)
            row[edge_data.get('id')] = edge_data.get('r') if node_a > node_b else -edge_data.get('r')
            sem[-1] += edge_data['sem'] if node_a > node_b else -edge_data['sem']
        a.append(row)
    return a, sem


def compute_i(G):
    a1, sem1 = first_kirchhoff_law(G)
    a2, sem2 = second_kirchhoff_law(G)
    i_array = np.linalg.lstsq(a1 + a2, sem1 + sem2, rcond=None)[0]
    return i_array


class LessPrecise(float):
    def __repr__(self):
        return str(self)


def round_labels(labels):
    for label in labels:
        v = labels.get(label)
        v = LessPrecise(round(v, 2))
        labels[label] = v






G = import_data_from_csv("graph1.csv")
add_sem(G, 45, 99, 30)
i_array = compute_i(G)

G_di = nx.DiGraph()

for edge in G.edges():
    id = G.get_edge_data(*edge).get('id')
    node_a, node_b = edge[0], edge[1]
    i = i_array[id]
    if i < 0:
        G_di.add_edge(min(node_a, node_b), max(node_a, node_b), i=-i)
    else:
        G_di.add_edge(max(node_a, node_b), min(node_a, node_b), i=i)

edges_di = G_di.edges()
i_array = [G_di[u][v]['i'] for u, v in edges_di]

fig = plt.gcf()
fig.set_size_inches(10, 10)
fig.set_facecolor("red")



# pos = nx.spectral_layout(G_di)
# print(pos)
pos = {}

for node in G_di.nodes():
    pos.update([(node, (node / 10, node % 10))])

nodes_color_map = []
nodes_size_map = []

for node in G_di.nodes():
    if node == 45 or node == 99:
        nodes_color_map.append('red')
        nodes_size_map.append(40)
    else:
        nodes_color_map.append('black')
        nodes_size_map.append(10)


options = {
    'node_color': nodes_color_map,
    'node_size': nodes_size_map,
    'width': 4,
    'font_size': 8
}

nx.draw(G_di, pos, edges=edges_di, with_labels=False, edge_color=i_array,
        edge_cmap=plt.cm.OrRd, **options)
labels = nx.get_edge_attributes(G_di, 'i')
round_labels(labels)
nx.draw_networkx_edge_labels(G_di, pos, edge_labels=labels, font_size=5)
fig.suptitle('2D grid, SEM = 30V, R = 1 Ohm')
plt.show()
fig.savefig('test2png.png', dpi=300)
