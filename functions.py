import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Functions:
    def __init__(self, col_politicians, col_graph):
        self.col_politicians = col_politicians
        self.col_graph = col_graph
        self.threshold = 0
        self.G = nx.Graph()
        self.politicians_data = None
        self.graph_data = None
        self.parties_to_filter = []

    def get_data(self):
        try:
            year = int(input("Informe o ano a considerar (de 2001 a 2023) : "))
            if year < 2001 or year > 2023:
                raise ValueError
        except ValueError:
            print("ERRO! Ano inválido!")
        
        self.politicians_data = pd.read_csv(f"datasets/politicians{year}.csv", encoding='utf-8', delimiter=';', header=None, names=self.col_politicians, engine='python')
        self.graph_data = pd.read_csv(f"datasets/graph{year}.csv", encoding='utf-8', delimiter=';', header=None, names=self.col_graph, engine='python')

        try:
            self.threshold = float(input("Informe o percentual mínimo de concordância (ex . 0.9) : "))
            if self.threshold < 0 or self.threshold > 1:
                raise ValueError
        except ValueError:
            print("ERRO! Threshold inválido!")

        analyse_partys = input("Informe os partidos a analisar, separados por espaco (ex . PT MDB PL) : ").upper()
        self.parties_to_filter = analyse_partys.split()

        return self.politicians_data, self.graph_data, self.parties_to_filter
    
    def is_in_parties_to_filter(self):
        filtered_partys = self.politicians_data[self.politicians_data['party'].isin(self.parties_to_filter)] 
        return filtered_partys

    def normalization(self, weight, min_edges_vote):
        normalization = weight / min_edges_vote
        return normalization
    
    def inversion(self, weight, min_edges_vote):
        normalization = self.normalization(weight, min_edges_vote)
        inversion = 1 - normalization
        return inversion

    def add_node(self):
        # Iterating over the column of deputies after filtering parties
        for dept in self.is_in_parties_to_filter()['congressman']: 
            party = self.is_in_parties_to_filter().loc[self.is_in_parties_to_filter()['congressman'] == dept, 'party'].values[0]
            self.G.add_node(dept, party=party)

    def add_edge(self):
        #Iterando as informações do graph_data
        for index, row in self.graph_data.iterrows():
            c1 = row.congressman1
            c2 = row.congressman2
            w = row.weight

            if c1 in self.is_in_parties_to_filter()['congressman'].values and c2 in self.is_in_parties_to_filter()['congressman'].values:
                min_vote = min(self.politicians_data.loc[self.politicians_data['congressman'] == c1, 'votes'].values[0], 
                               self.politicians_data.loc[self.politicians_data['congressman'] == c2, 'votes'].values[0])     
                normalization = self.normalization(w, min_vote)  

                if normalization >= self.threshold:
                    inversion = self.inversion(w, min_vote)
                    self.G.add_edge(c1, c2, weight=inversion)         
    
    def betwenness(self):
        betwenness = nx.betweenness_centrality(self.G) 
        nodes = list(betwenness.keys()) #gera uma lista pega as chaves(nós) do dicionário que foi retornado para o betweness.
        centralities = list(betwenness.values()) #gera uma lista que pega as values(centralidade) do dicionário que foi retornado para o betweness.
        return nodes, centralities

    def plot_bar_chart(self):
        nodes, centralities = self.betwenness()
        nodes_sorted, centralities_sorted = zip(*sorted(zip(nodes, centralities), key=lambda x: x[1]))
        plt.bar(nodes_sorted, centralities_sorted)
        plt.xlabel('Deputados')
        plt.xticks(rotation=75)
        plt.ylabel('Betweenness')
        plt.title("Gráfico de Barras de Relações Políticas")
        plt.show()

    def plot_graph(self):
        pos = nx.spring_layout(self.G, k=0.3)  # Define a posição dos nós no layout
        nx.draw_networkx(self.G, pos, with_labels=True)  # Plota o grafo
        plt.title("Grafo de Relações Políticas")
        plt.show()

    def plot_heatmap(self):
        rows = []
        columns = []
        values = []

        for edge in self.G.edges(data=True):
            c1 = edge[0]
            c2 = edge[1]
            weight = edge[2]['weight']

            min_vote = min(self.politicians_data.loc[self.politicians_data['congressman'] == c1, 'votes'].values[0],
                        self.politicians_data.loc[self.politicians_data['congressman'] == c2, 'votes'].values[0])
            normalization = self.normalization(weight, min_vote)

            rows.append(c1)
            columns.append(c2)
            values.append(normalization)

        heatmap_data = pd.DataFrame({'row': rows, 'column': columns, 'value': values})
        heatmap_matrix = heatmap_data.pivot(index='row', columns='column', values='value')

        plt.figure(figsize=(10, 8))
        plt.imshow(heatmap_matrix, cmap='coolwarm', aspect='auto')

        # Adicione rótulos às linhas e colunas
        plt.xticks(range(len(heatmap_matrix.columns)), heatmap_matrix.columns)
        plt.yticks(range(len(heatmap_matrix.index)), heatmap_matrix.index)

        plt.colorbar()

        plt.title("Heatmap de Relações Políticas")
        plt.xlabel("Deputados")
        plt.ylabel("Deputados")
        plt.show()