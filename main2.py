from functions import Functions

col_politicians = ['congressman', 'party', 'votes']
col_graph = ['congressman1', 'congressman2', 'weight']

f = Functions(col_politicians, col_graph)


f.get_data()
f.add_node()
f.add_edge()
f.plot_bar_chart()
f.plot_graph()
f.plot_heatmap()