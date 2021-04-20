import networkx as nx
import matplotlib.pyplot as plt
from gurobipy import *
from graph_parameter import graph_parameter
import pandas as pd
from pprint import pprint

def draw_graph(graph, cost): #takes in a tuplelist of arcs and a dictionary of costs

    plt.figure(figsize=(64,64))
    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph]) # combined set of all nodes - implies no dups
    # create networkx graph
    G=nx.DiGraph() #directed graph
    # add nodes
    for node in nodes:
        G.add_node(node)
    # add edges
    i=0
    for edge in graph:
        # print(edge[0], edge[1], cost[edge])
        G.add_edge(edge[0], edge[1], weight=cost[edge]) #weight is euclidean distance from dictionary
        i+=1
    # draw graph
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_size=20)
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=20)
    plt.savefig("graph") # print graph in the same directory with title "graph" so you can zoom and still see info

# data
data = graph_parameter()
commodity_quantity, nodes, arcs, commodity_source, commodity_sink, m_distance = data
arc_df = pd.read_csv("output_arcs.csv")
arcs = tuplelist([tuple(pair) for pair in arc_df.values])
# pprint(m_distance)
    
draw_graph(arcs, m_distance) # calls draw