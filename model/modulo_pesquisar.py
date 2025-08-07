import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

import model.modulo_arquivar as arquivar

defaut = ['0', '0']

def pesquisar():
    # === função que devolve o item selecionado ===
    def concluir():
        try:
            linha_selecionada = tree.selection()[0]
            escolha = tree.item(linha_selecionada, 'values')
            janela_pesquisa.destroy()
            return escolha[0], escolha[1]
        except IndexError:
            messagebox.showwarning("Aviso", "Nenhum item selecionado!")
            janela_pesquisa.destroy()
            return defaut[0], defaut[1]

    janela_pesquisa = ctk.CTk()
    janela_pesquisa.title("PESQUISA POR ITEM")
    janela_pesquisa.geometry("826x420+696+142")
    janela_pesquisa.focus_force()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("database/themas.txt")

    

    frame = ctk.CTkFrame(janela_pesquisa)
    frame.pack(pady=(20,10), padx=10, fill="both", expand=True)
    
    
    # estilo da Treeview
    style= ttk.Style()
    style.configure("Set.Treeview.Heading", font=("Arial", 14, "bold"))
    style.configure("Set.Treeview", font=("Courier", 18))

    titulos_pesquisar = ["Cod", "EAN", "Descrição"]
    tree = ttk.Treeview(frame, columns=titulos_pesquisar, show='headings', height=15 ,style="Set.Treeview")
   
    tree.heading("Cod", text="Item")
    tree.column("Cod", anchor=tk.E, width=20)
    tree.heading("EAN", text="EAN")
    tree.column("EAN", anchor=tk.W, width=40)
    tree.heading("Descrição", text="  Descrição  ")
    tree.column("Descrição", anchor=tk.W, width=500)
    # tree.heading("Preço", text="Preço R$")
    # tree.column("Preço", anchor=tk.E, width=100)

    for i, titulo in enumerate(titulos_pesquisar):
        tree.heading(i, text=titulo)
        tree.column(i, anchor="center", width=200)

    tree.pack(side="top", fill="both", expand=True)
    
    frame_buttons = ctk.CTkFrame(janela_pesquisa, fg_color="transparent")
    frame_buttons.pack(pady=(0,20), padx=10, fill="x")

    # Configura as colunas do grid
    frame_buttons.columnconfigure(0, weight=1)  # coluna expansiva (entry)
    frame_buttons.columnconfigure(1, weight=0)  # coluna do botão

    entry_pesquisa = ctk.CTkEntry(frame_buttons, placeholder_text="Descrição", width=800, font=("Courier", 20))
    entry_pesquisa.grid(row=0, column=0, pady=10, sticky="w")  # coluna 0 → lado esquerdo

    btn_concluir = ctk.CTkButton(janela_pesquisa, text="ADICIONAR", command=janela_pesquisa.quit,font=("Helvetica", 16))
    btn_concluir.pack(pady=10)    # coluna 1 → lado direito


    # === função de busca dinâmica (agora entry_pesquisa já existe!) ===
    def buscar(event=None):
        texto = entry_pesquisa.get()
        busca_sql = f"%{texto}%"
        resultados = arquivar.release(busca_sql)

        # limpa tree
        for item in tree.get_children():
            tree.delete(item)

        # carrega resultados na tree
        for r in resultados:
            tree.insert("", "end", values=r)

    # carrega tudo inicialmente
    #buscar()

    entry_pesquisa.bind("<KeyRelease>", buscar)

    janela_pesquisa.mainloop()
    return concluir()
#pesquisar()