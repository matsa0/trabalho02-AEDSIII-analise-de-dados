import networkx as nx
import pandas as pd
from graph import Graph
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

G = nx.Graph()
g = Graph()

# Dando nome para as colunas dos arquivos, afim de facilitar manipulá-las.
col_politicians = ['congressman', 'party', 'votes']
col_graph = ['congressman1', 'congressman2', 'weight']

# Primeira interação
year = int(input("Digite o ano que você deseja filtrar as informações > "))

politicians_data = pd.read_csv(f"datasets/politicians{year}.csv", encoding='utf-8', delimiter=';', header=None, names=col_politicians, engine='python')
graph_data = pd.read_csv(f"datasets/graph{year}.csv", encoding='utf-8', delimiter=';', header=None, names=col_graph, engine='python')


parties_to_filter = [] # Lista de partidos que o usuário quer filtrar

# Segunda interação
value = int(input("Você deseja filtrar por partidos? ['0' para NÃO || '1' para SIM] > "))
if value == 1:
    amount = int(input("Digite a quantidade de partidos > "))
    for _ in range(amount):
        party = input("Digite o partido > ").upper()
        parties_to_filter.append(party) 

threshold = float(input("Digite o threshold mínimo > "))

# Verificando quais partidos do politicians estão no vetor parties_to_filter
filtered_partys = politicians_data[politicians_data['party'].isin(parties_to_filter)] 

party_colors = {
    'PSDB': 'blue',
    'PR': 'green',
    'PT': 'red',
    'PSOL': 'yellow',
}

for dept in filtered_partys['congressman']: #Iterando sobre a coluna dos deputados após filtrar os partidos
    party = filtered_partys.loc[filtered_partys['congressman'] == dept, 'party'].values[0]
    G.add_node(dept, party=party)

for index, row in graph_data.iterrows():
    c1 = row.congressman1 # Pegando o primeiro deputado  
    c2 = row.congressman2 # Pegando o segundo deputado
    w = row.weight # Pegando o peso

    # Pegando os deputados que estão filtrados pelos partidos em filtered_partys
    if c1 in filtered_partys['congressman'].values and c2 in filtered_partys['congressman'].values: 
        if value == 1:
            min_vote = min(politicians_data.loc[politicians_data['congressman'] == c1, 'votes'].values[0],
                           politicians_data.loc[politicians_data['congressman'] == c2, 'votes'].values[0])
            
        normalization = w / min_vote

        if normalization >= threshold:
            inversion = 1 - normalization
            G.add_edge(c1, c2, weight=inversion)


if value == 0:
    for index, row in politicians_data.iterrows():
        G.add_node(row['congressman'], votes=row['votes'])  #Adicionando o nó com o atributo 'votes'
        g.add_node(row['congressman'])

    for index, row in graph_data.iterrows():
        c1 = row.congressman1  
        c2 = row.congressman2  
        w = row.weight  
        min_vote = min(G.nodes[c1]['votes'], G.nodes[c2]['votes'])  #G.nodes() permite que possamos acessar os atributos desse nó.
        normalization = w / min_vote

        if normalization >= threshold:
            inversion = 1 - normalization
            G.add_edge(c1, c2, weight=inversion)

#avalia a importância relativa de um nó com base na quantidade de caminhos mais curtos que passam por ele em um grafo. 
#retorna um dicionário onde as chaves são os nós (vértices) do grafo e os valores são as métricas de intermediação de cada nó.
betwenness = nx.betweenness_centrality(G) 

nodes = list(betwenness.keys()) #gera uma lista pega as chaves(nós) do dicionário que foi retornado para o betweness.
centralities = list(betwenness.values()) #gera uma lista pega as values(centralidade) do dicionário que foi retornado para o betweness.

nodes_sorted, centralities_sorted = zip(*sorted(zip(nodes, centralities), key=lambda x: x[1]))

plt.bar(nodes_sorted, centralities_sorted)
plt.xlabel('Deputados')
plt.xticks(rotation= 75)
plt.ylabel('Betwenness')
plt.title("Medida de Centralidade")

plt.show()
#print(betwenness)

#print(G)

plt.figure(1)
nx.draw_networkx(G, pos=nx.spring_layout(G, k=0.3), with_labels=True, node_color=[party_colors[G.nodes[n]['party']] for n in G.nodes()]) #utilizando o layout spring
legend_patches = [mpatches.Patch(color=color, label=party) for party, color in party_colors.items()]
plt.legend(handles=legend_patches, title="Partidos")

plt.show()
#pos = nx.spring_layout(G, scale=2.0)


'''
NORMALIZAÇÃO

w(u, v) = w(u, v) / min(votes(u), votes(v))    

u -> deputado 'u'
v -> deputado 'v'

1 - Para cada aresta (u, v) no grafo:
    w(u, v) -> Peso da aresta entre eles;
    votes(u) -> Número de votações que o deputado 'u' participou;
    votes(v) -> Número de votações que o deputado 'v' participou;

2 - Calculamos o mínimo entre o número de votações de u e v, representado por min(votes(u), votes(v)).
    ***Por exemplo, suponha que o deputado u participou de 50 votações e o deputado v participou de 65 votações. 
    Nesse caso, o mínimo entre o número de votações de u e v será 50, porque é o menor valor entre 50 (número de votações de u)
    e 65 (número de votações de v).
'''









""" print(G.number_of_nodes())
print(G.number_of_edges())
print(g.node_count)
print(g.edge_count)

print(g) """










