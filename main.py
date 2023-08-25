from functions import Functions

col_politicians = ['congressman', 'party', 'votes']
col_graph = ['congressman1', 'congressman2', 'weight']

f = Functions(col_politicians, col_graph)

parties_to_filter = []

year = int(input("Informe o ano a considerar (de 2001 a 2023) : "))
threshold = input("Informe o percentual mínimo de concordância (ex . 0.9) : ")
analyse_partys = input("Informe os partidos a analisar, separados por espaço (ex . PT MDB PL) : ").upper().split()
#parties_to_filter = analyse_partys.split()

f.get_data(year, threshold, analyse_partys)
f.add_node()
f.add_edge()
f.plot_bar_chart()
f.plot_graph()
f.plot_heatmap()