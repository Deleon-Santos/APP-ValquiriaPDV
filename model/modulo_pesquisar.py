import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

import model.modulo_arquivar as arquivar

defaut = ['0', '0']

def pesquisar(pesquisa_aberta):
    
    if pesquisa_aberta:
        return defaut[0], defaut[1] 
    pesquisa_aberta = True
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

    titulos_pesquisar = ["Cod", "Descrição", "Preço"]
    tree = ttk.Treeview(frame, columns=titulos_pesquisar, show='headings', height=15 ,style="Set.Treeview")
   
    tree.heading("Cod", text="Item")
    tree.column("Cod", anchor=tk.E, width=20)
    tree.heading("Descrição", text="Descrição")
    tree.column("Descrição", anchor=tk.W, width=500)
    tree.heading("Preço", text="  Preço  ")
    tree.column("Preço", anchor=tk.W, width=100)

    for i, titulo in enumerate(titulos_pesquisar):
        tree.heading(i, text=titulo)
        tree.column(i, anchor="center")
    tree.pack(side="top", fill="both", expand=True)
 
    entry_pesquisa = ctk.CTkEntry(janela_pesquisa, placeholder_text="Descrição", width=800, font=("Courier", 20))
    entry_pesquisa.pack( pady=(10, 0), padx=10, fill="x")
    frame_buttons = ctk.CTkFrame(janela_pesquisa, fg_color="transparent")
    frame_buttons.pack(pady=(0,20), padx=10)
 
    btn_concluir = ctk.CTkButton(frame_buttons, text="ADICIONAR", command=janela_pesquisa.quit,font=("Helvetica", 16))
    btn_concluir.grid(row= 0, column= 0,pady=(10,0), padx=10)  
    btn_sair = ctk.CTkButton(frame_buttons, text="SAIR", command=janela_pesquisa.quit,font=("Helvetica", 16), fg_color="red")
    btn_sair.grid(row= 0, column= 1,pady=(10,0), padx=10)  

    def buscar(event=None):
        texto = entry_pesquisa.get()
        busca_sql = f"%{texto}%"
        resultados = arquivar.release(busca_sql)

        for item in tree.get_children():
            tree.delete(item)

        for r in resultados:
            tree.insert("", "end", values=r)
    entry_pesquisa.bind("<KeyRelease>", buscar)
    janela_pesquisa.after(100, lambda: entry_pesquisa.focus_set())
    janela_pesquisa.mainloop()
    pesquisa_aberta = False
    return concluir()