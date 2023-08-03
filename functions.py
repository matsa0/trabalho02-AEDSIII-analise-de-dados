import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class Functions:

    @staticmethod
    def read_data(year):
        # Dando nome para as colunas dos arquivos, afim de facilitar manipulá-las.
        col_politicians = ['congressman', 'party', 'votes']
        col_graph = ['congressman1', 'congressman2', 'weight']

        politicians_data = pd.read_csv(f"datasets/politicians{year}.csv", encoding='utf-8', delimiter=';', header=None, names=col_politicians, engine='python')
        graph_data = pd.read_csv(f"datasets/graph{year}.csv", encoding='utf-8', delimiter=';', header=None, names=col_graph, engine='python')

        return politicians_data, graph_data
    
    @staticmethod
    def partys_filter(politicians_data, parties_to_filter):
        filtered_politicians = politicians_data[politicians_data['party'].isin(parties_to_filter)]

        return filtered_politicians
    
    @staticmethod
    def create_graph(politicians_data, graph_data, filtered_politicians):
        G = nx.Graph()

        for dept in filtered_politicians['congressman']:
            G.add_node(dept)

        for index, row in graph_data.iterrows():
            c1 = row.congressman1
            c2 = row.congressman2
            w = row.weight

            if c1 in filtered_politicians['congressman'].values and c2 in filtered_politicians['congressman'].values:
                G.add_edge(c1, c2, weight=w)

        return G

    @staticmethod
    def normalize_weights(G):
        for c1, c2, w in G.edges(data='weight'):
            min_vote = min(G.nodes[c1]['votes'], G.nodes[c2]['votes'])
            normalization = w / min_vote
            G[c1][c2]['weight'] = normalization

        return G