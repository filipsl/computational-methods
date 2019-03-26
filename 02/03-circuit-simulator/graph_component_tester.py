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

##################################################################################

# NUMBER OF COMPONENTS

##################################################################################


def components_tester():
    big_graph_names = ('BIG_1000_random_graph.csv',
                       'BIG_2000_random_graph.csv',
                       'BIG_4000_3_regular_graph.csv',
                       'BIG_2000_graph_with_bridge.csv',
                       'BIG_3600_2D_grid_var_r.csv',
                       '2D_grid_const_r.csv',
                       '2D_grid_var_r.csv',
                       '3_regular_graph.csv',
                       'graph_with_bridge.csv',
                       'random_graph.csv',
                       )

    for graph_name in big_graph_names:
        G = import_data_from_csv('./graphs_csv/' + graph_name)
        print('\nimported: ' + graph_name)
        print('Connected components ' + str(nx.number_connected_components(G)))
        if nx.number_connected_components(G) > 1:
            graphs = list(nx.connected_component_subgraphs(G))
            for graph in graphs:
                print(graph.nodes())

##################################################################################


components_tester()