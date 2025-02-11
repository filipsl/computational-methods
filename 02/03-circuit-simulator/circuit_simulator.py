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
        for row in reader:
            if not G.has_edge(int(row[0]), int(row[1])):
                G.add_edge(int(row[0]), int(row[1]), r=abs(float(row[2])), sem=0, id=j + 1)
                j += 1
    csv_file.close()
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
            sem[-1] += edge_data.get('sem') if node_a > node_b else -edge_data.get('sem')
        a.append(row)
    return a, sem


def compute_i(G):
    a1, sem1 = first_kirchhoff_law(G)
    a2, sem2 = second_kirchhoff_law(G)
    print('np.linalg.lstsq begins...')
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


def verify_first_kirchhoff_law(G, i_array):
    eps = 1e-10
    for node in G.nodes:
        sum_of_current = 0
        for edge in G.edges(node):
            edge_id = G.get_edge_data(*edge).get('id')
            sum_of_current += i_array[edge_id] if edge[0] > edge[1] else -i_array[edge_id]
        if sum_of_current > eps:
            return False
    return True


def verify_second_kirchhoff_law(G, i_array):
    eps = 1e-10
    for cycle in nx.cycle_basis(G):
        sem_sum = 0
        voltage_sum = 0
        for i in range(len(cycle)):
            node_a = cycle[i]
            node_b = cycle[(i + 1) % len(cycle)]
            edge_data = G.get_edge_data(node_a, node_b)
            r = edge_data.get('r') if node_a > node_b else -edge_data.get('r')
            voltage_sum += r * i_array[edge_data.get('id')]
            sem_sum += edge_data.get('sem') if node_a > node_b else -edge_data.get('sem')
        if abs(sem_sum - voltage_sum) > eps:
            return False
    return True


##################################################################################

# BIG GRAPHS TEST

##################################################################################
def run_big_tests():
    big_graph_names = ('BIG_1000_random_graph.csv',
                       'BIG_2000_random_graph.csv',
                       'BIG_4000_3_regular_graph.csv',
                       'BIG_2000_graph_with_bridge.csv',
                       'BIG_3600_2D_grid_var_r.csv')

    for graph_name in big_graph_names:
        G = import_data_from_csv('./graphs_csv/' + graph_name)
        print('\nimported: ' + graph_name)
        if graph_name == 'BIG_1000_random_graph.csv':
            add_sem(G, 250, 500, 30)
        else:
            add_sem(G, 500, 1500, 30)
        i_array = compute_i(G)
        print('Verifying ' + graph_name)
        print('I Kirchhoff\'s law', verify_first_kirchhoff_law(G, i_array))
        print('II Kirchhoff\'s law', verify_second_kirchhoff_law(G, i_array))


##################################################################################

# DATA PROCESSING AND VISUALISING

##################################################################################

# random graph

graph_name = 'random_graph.csv'
sem_a = 10
sem_b = 27

G = import_data_from_csv('./graphs_csv/' + graph_name)
add_sem(G, sem_a, sem_b, 30)
i_array = compute_i(G)

print('Verifying ' + graph_name)
print('I Kirchhoff\'s law', verify_first_kirchhoff_law(G, i_array))
print('II Kirchhoff\'s law', verify_second_kirchhoff_law(G, i_array))

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
pos = nx.spring_layout(G_di)

nodes_color_map = []
nodes_size_map = []

for node in G_di.nodes():
    if node == sem_a or node == sem_b:
        nodes_color_map.append('red')
        nodes_size_map.append(40)
    else:
        nodes_color_map.append('black')
        nodes_size_map.append(10)

options = {
    'node_color': nodes_color_map,
    'node_size': nodes_size_map,
    'width': 3,
    'font_size': 8
}

nx.draw(G_di, pos, edges=edges_di, with_labels=False, edge_color=i_array,
        edge_cmap=plt.cm.Reds, **options)
labels = nx.get_edge_attributes(G_di, 'i')
round_labels(labels)
nx.draw_networkx_edge_labels(G_di, pos, edge_labels=labels, font_size=5)
fig.suptitle('Random graph, SEM = 30V, R = 1 Ohm')
plt.show()
fig.savefig('./graphs_png/random_graph.png', dpi=300)

# 3-regular graph

graph_name = '3_regular_graph.csv'
sem_a = 10
sem_b = 27

G = import_data_from_csv('./graphs_csv/' + graph_name)
add_sem(G, sem_a, sem_b, 30)
i_array = compute_i(G)

print('Verifying ' + graph_name)
print('I Kirchhoff\'s law', verify_first_kirchhoff_law(G, i_array))
print('II Kirchhoff\'s law', verify_second_kirchhoff_law(G, i_array))

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
pos = nx.shell_layout(G_di)

nodes_color_map = []
nodes_size_map = []

for node in G_di.nodes():
    if node == sem_a or node == sem_b:
        nodes_color_map.append('red')
        nodes_size_map.append(40)
    else:
        nodes_color_map.append('black')
        nodes_size_map.append(10)

options = {
    'node_color': nodes_color_map,
    'node_size': nodes_size_map,
    'width': 3,
    'font_size': 8
}

nx.draw(G_di, pos, edges=edges_di, with_labels=False, edge_color=i_array,
        edge_cmap=plt.cm.Reds, **options)
labels = nx.get_edge_attributes(G_di, 'i')
round_labels(labels)
nx.draw_networkx_edge_labels(G_di, pos, edge_labels=labels, font_size=5)
fig.suptitle('3-regular graph, SEM = 30V, R = 1 Ohm')
plt.show()
fig.savefig('./graphs_png/3_regular_graph.png', dpi=300)

# Graph with bridge

graph_name = 'graph_with_bridge.csv'
sem_a = 5
sem_b = 37

G = import_data_from_csv('./graphs_csv/' + graph_name)
add_sem(G, sem_a, sem_b, 30)
i_array = compute_i(G)

print('Verifying ' + graph_name)
print('I Kirchhoff\'s law', verify_first_kirchhoff_law(G, i_array))
print('II Kirchhoff\'s law', verify_second_kirchhoff_law(G, i_array))

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
pos = nx.spring_layout(G_di, k=0.25, iterations=30)

nodes_color_map = []
nodes_size_map = []

for node in G_di.nodes():
    if node == sem_a or node == sem_b:
        nodes_color_map.append('red')
        nodes_size_map.append(40)
    else:
        nodes_color_map.append('black')
        nodes_size_map.append(10)

edge_width_map = []

for i, edge in enumerate(edges_di):
    edge_width_map.append(G.get_edge_data(*edge).get('r') / 5 + 2)

options = {
    'node_color': nodes_color_map,
    'node_size': nodes_size_map,
    'width': edge_width_map,
    'font_size': 8
}

nx.draw(G_di, pos, edges=edges_di, with_labels=False, edge_color=i_array,
        edge_cmap=plt.cm.Reds, **options)
labels = nx.get_edge_attributes(G_di, 'i')
round_labels(labels)
nx.draw_networkx_edge_labels(G_di, pos, edge_labels=labels, font_size=5)
fig.suptitle('Graph with bridge, SEM = 30V, R in [0,10] Ohm')
plt.show()
fig.savefig('./graphs_png/graph_with_bridge.png', dpi=300)

# 2D grid r = 1 Ohm

graph_name = '2D_grid_const_r.csv'
sem_a = 99
sem_b = 45

G = import_data_from_csv('./graphs_csv/' + graph_name)
add_sem(G, sem_a, sem_b, 30)
i_array = compute_i(G)

print('Verifying ' + graph_name)
print('I Kirchhoff\'s law', verify_first_kirchhoff_law(G, i_array))
print('II Kirchhoff\'s law', verify_second_kirchhoff_law(G, i_array))

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

pos = {}
for node in G_di.nodes():
    pos.update([(node, (node / 10, node % 10))])

nodes_color_map = []
nodes_size_map = []

for node in G_di.nodes():
    if node == sem_a or node == sem_b:
        nodes_color_map.append('red')
        nodes_size_map.append(40)
    else:
        nodes_color_map.append('black')
        nodes_size_map.append(10)


options = {
    'node_color': nodes_color_map,
    'node_size': nodes_size_map,
    'width': 3,
    'font_size': 8
}

nx.draw(G_di, pos, edges=edges_di, with_labels=False, edge_color=i_array,
        edge_cmap=plt.cm.Reds, **options)
labels = nx.get_edge_attributes(G_di, 'i')
round_labels(labels)
nx.draw_networkx_edge_labels(G_di, pos, edge_labels=labels, font_size=5)
fig.suptitle('2D grid, SEM = 30V, R = 1 Ohm')
plt.show()
fig.savefig('./graphs_png/2D_grid_const_r.png', dpi=300)

# 2D grid r in [0,10] Ohm

graph_name = '2D_grid_var_r.csv'
sem_a = 99
sem_b = 0

G = import_data_from_csv('./graphs_csv/' + graph_name)
add_sem(G, sem_a, sem_b, 30)
i_array = compute_i(G)

print('Verifying ' + graph_name)
print('I Kirchhoff\'s law', verify_first_kirchhoff_law(G, i_array))
print('II Kirchhoff\'s law', verify_second_kirchhoff_law(G, i_array))

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

pos = {}
for node in G_di.nodes():
    pos.update([(node, (node / 10, node % 10))])

nodes_color_map = []
nodes_size_map = []

for node in G_di.nodes():
    if node == sem_a or node == sem_b:
        nodes_color_map.append('red')
        nodes_size_map.append(40)
    else:
        nodes_color_map.append('black')
        nodes_size_map.append(10)

edge_width_map = []

for i, edge in enumerate(edges_di):
    edge_width_map.append(G.get_edge_data(*edge).get('r') / 2 + 2)

options = {
    'node_color': nodes_color_map,
    'node_size': nodes_size_map,
    'width': edge_width_map,
    'font_size': 8
}

nx.draw(G_di, pos, edges=edges_di, with_labels=False, edge_color=i_array,
        edge_cmap=plt.cm.Reds, **options)
labels = nx.get_edge_attributes(G_di, 'i')
round_labels(labels)
nx.draw_networkx_edge_labels(G_di, pos, edge_labels=labels, font_size=5)
fig.suptitle('2D grid, SEM = 30V, R in [0,10] Ohm')
plt.show()
fig.savefig('./graphs_png/2D_grid_var_r.png', dpi=300)

# run_big_tests()
