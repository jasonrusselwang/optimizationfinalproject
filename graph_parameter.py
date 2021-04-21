from gurobipy import tuplelist
import pandas as pd
import numpy as np
from pprint import pprint

def graph_parameter(node_file="Nodes_Revised.csv", arc_file="Arcs.csv", commodities_file="Commodities.csv"):
    # data setup into pandas df's
    node_df = pd.read_csv(node_file)
    arc_df = pd.read_csv(arc_file)
    commodities_df = pd.read_csv(commodities_file)

    # comodities and quantity {commodity:quantity}
    commodity_quantity = {k: g['weight'].values[0] for k, g in commodities_df.groupby('name')}

    # nodes
    nodes = node_df['nodes'].tolist()
    # nodes = [tuple(pair[1:]) for pair in node_df.values]

    # arcs (tuplelist)
    arcs = tuplelist([tuple(pair) for pair in arc_df.values])

    # sources {commodity:source}
    commodity_source = {k: g['source'].values[0] for k, g in commodities_df.groupby('name')}

    # sinks {commodity:sink}
    commodity_sink = {k: g['sink'].values[0] for k, g in commodities_df.groupby('name')}

    # m_distance {(arc pair): euclidean distance}
    m_distance = {}
    for x,y in arcs:
        x1, y1 = node_df.loc[node_df['nodes'] == x].values[0][1:3]
        x2, y2 = node_df.loc[node_df['nodes'] == y].values[0][1:3]
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        m_distance[(x, y)] = distance

    final_list = [commodity_quantity, nodes, arcs, commodity_source, commodity_sink, m_distance]
    return final_list
if __name__ == "__main__":
    data = graph_parameter()
    pprint(data)