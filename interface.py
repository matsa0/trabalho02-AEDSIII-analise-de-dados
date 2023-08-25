import customtkinter
from functions import Functions


col_politicians = ['congressman', 'party', 'votes']
col_graph = ['congressman1', 'congressman2', 'weight']

f = Functions(col_politicians, col_graph)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

janela = customtkinter.CTk()
janela.geometry("500x400")

def gerar():
    parties = []

    year = entry1.get()
    threshold = entry2.get()
    parties = entry3.get().upper().split()

    f.get_data(year, threshold, parties)
    f.add_node()
    f.add_edge()
    f.plot_bar_chart()
    f.plot_graph()
    f.plot_heatmap()

frame = customtkinter.CTkFrame(master=janela)
frame.pack(pady=20,padx=60,fill="both",expand=True)

label = customtkinter.CTkLabel(master=frame,text="Informe o ano a considerar (de 2001 a 2023):", font=("Roboto", 15))
label.pack(pady=7,padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Ano")
entry1.pack(pady=7,padx=10, ipadx=10, ipady=4)

label = customtkinter.CTkLabel(master=frame,text="Informe o percentual mınimo de concordancia ( threshold ) (ex. 0.9):", font=("Roboto", 11))
label.pack(pady=7,padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Threshold")
entry2.pack(pady=7,padx=10, ipadx=10, ipady=4)

label = customtkinter.CTkLabel(master=frame,text="Informe os partidos a analisar , separados por espaco (ex. PT MDB PL):", font=("Roboto", 11))
label.pack(pady=7,padx=10)

entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="Partidos")
entry3.pack(pady=7,padx=10, ipadx=10, ipady=4)

butao = customtkinter.CTkButton(master=frame, text="Gerar", font=("Roboto", 14), command=gerar)
butao.pack(pady=20, padx=10, ipadx=13, ipady=14)

janela.mainloop()