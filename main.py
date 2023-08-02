import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from graph import Graph

G = nx.Graph()

#dando nome para as colunas dos arquivos, afim de facilitar manipulá-las.
col_politicians = ['congressman', 'party', 'votes']
col_graph = ['congressman1', 'congressman2', 'weight']

#Primeira interação
year = int(input("Digite o ano que você deseja filtrar as informações > "))

politicians_data = pd.read_csv(f"datasets/politicians{year}.csv", encoding='utf-8', delimiter=';',header=None, names=col_politicians, engine='python')
graph_data = pd.read_csv(f"datasets/graph{year}.csv", encoding='utf-8', delimiter=';', header=None, names=col_graph, engine='python')



parties_to_filter = [] #Lista de partidos que o usuário quer filtrar



#Segunda interação
value = int(input("Você deseja filtrar por partidos? ['0' para NÃO | '1' para SIM] > "))
if value == 1:
    amount = int(input("Digite a quantidade de partidos > "))
    for _ in range(amount):
        party = input("Digite o partido > ").upper()
        parties_to_filter.append(party) 

"""     se o partido percorrido está no vetor parties_to_filter, preciso filtrar os deputados desses partidos, 
        adicionar o nó deles, as arestas entre eles e o peso        """


#verificando quais partidos do politicians estão no vetor parties_to_filter
filtered_politicians = politicians_data[politicians_data['party'].isin(parties_to_filter)] 

for dept in filtered_politicians['congressman']: #iterando sobre a coluna dos deputados após filtrar os partidos
    G.add_node(dept)

for index, row in graph_data.iterrows():
    c1 = row.congressman1 #pegando o primeiro deputado  
    c2 = row.congressman2 #pegando o segundo deputado
    w = row.weight #pegando o peso

    #pega os depurtados que estão filtrados pelos partidos em filtered_politicians
    if c1 in filtered_politicians['congressman'].values and c2 in filtered_politicians['congressman'].values: 
        G.add_edge(c1, c2, weight=w)





if value == 0:
    for index, row in politicians_data.iterrows():
        G.add_node(row['congressman'], votes=row['votes'])  #Adicionando o nó com o atributo 'votes'

    for index, row in graph_data.iterrows():
        G.add_edge(row['congressman1'], row['congressman2'], weight=row['weight'])  #Adicionando a aresta com o atributo 'weight'



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







""" plt.figure(1)
nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=True) #utilizando o layout spring
plt.show() """

print(G.number_of_nodes())
print(G.number_of_edges())

""" adj_list = nx.to_dict_of_lists(G) #converte um grafo em um dicionário de listas de adjacências. 
print(adj_list) """










