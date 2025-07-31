
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk , messagebox # Importa o Treeview do Tkinter padrão
import json
import model.modulo_arquivar as arquivar


def novo_item():
    def atualizar_tabela(item_cadastrado):
        tree.insert("", "end", values=item_cadastrado)  

    def cadastrar_item():
        try:
            if not entry_produto.get() or not entry_preco.get() or not entry_ean.get():
                messagebox.showerror(title="ERRO CADASTRO", message="Preencha os campos necessários!", icon="warning")
                return

            # Extrair os valores dos campos
            preco_material = str(entry_preco.get()).replace(",", ".").replace(" ", "0")
            descricao_material = entry_produto.get().title()
            ean_material = str(int(entry_ean.get()))  # Converte EAN para int e de volta para string
            
            item_cadastrado=arquivar.salvar_novo_item(novo_item=( ean_material, descricao_material, float(preco_material)))                    
            atualizar_tabela(item_cadastrado)
            
            entry_produto.delete(0, ctk.END)
            entry_preco.delete(0, ctk.END)
            entry_ean.delete(0, ctk.END)
        
        except ValueError:
            messagebox.showerror(title="ERRO CADASTRO", message="Informe Preço ou EAN\n em valor numérico", icon="warning")

    
    
    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("database/themas.txt")  # Tema de cores azul-escuro

    # Janela principal
    janela_cadastrar = ctk.CTkToplevel()
    janela_cadastrar.title("CADASTRAR ITENS")
    janela_cadastrar.geometry("826x420+696+142")  # Define o tamanho da janela_cadastrar
    janela_cadastrar.resizable(width=False, height=False)
    janela_cadastrar.focus_force()
    janela_cadastrar.grab_set()
    
    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("database/themas.txt")  # Tema de cores azul-escuro

    #Frame master
    frame_marte= ctk.CTkFrame(janela_cadastrar)
    frame_marte.pack(pady=(20,10),padx=0)

    #intens do cadastro
    frame_cadastro= ctk.CTkFrame(frame_marte,fg_color='transparent')
    frame_cadastro.pack(padx=10,pady=10)

    # Descrição
    lbl_descricao = ctk.CTkLabel(frame_cadastro, text="Descrição:", width=44)
    lbl_descricao.grid(row=0, column=1, padx=30, pady=(20,0),sticky='w')
    
    # Campo de entrada para o nome do produto
    entry_produto = ctk.CTkEntry(frame_cadastro, width=300,font=('Ariel',16))
    entry_produto.grid(row=1, column=1, padx=10, sticky='w')

    # EAN
    lbl_ean = ctk.CTkLabel(frame_cadastro, text="EAN:", width=25)
    lbl_ean.grid(row=0, column=2, padx=10, pady=(20,0),sticky='w')

    # Campo de entrada para o EAN
    entry_ean = ctk.CTkEntry(frame_cadastro, width=130,font=('Ariel',16))
    entry_ean.grid(row=1, column=2, padx=10, sticky='w')

    # Preço
    lbl_preco = ctk.CTkLabel(frame_cadastro, text="Preço R$:", width=10)
    lbl_preco.grid(row=0, column=3, padx=10, pady=(20,0),sticky='w')

    # Campo de entrada para o preço
    entry_preco = ctk.CTkEntry(frame_cadastro, width=100,font=('Ariel',16))
    entry_preco.grid(row=1, column=3, padx=10,  sticky='w')

    # Botão para cadastrar o item
    btn_cadastrar = ctk.CTkButton(frame_cadastro, text="CADASTRAR", command=cadastrar_item,width=40)
    btn_cadastrar.grid(row=0, column=4, padx=(10,0), pady=10)

    # Botão para sair do programa
    btn_sair = ctk.CTkButton(frame_cadastro, text="SAIR", fg_color="red", command=janela_cadastrar.destroy,width=90)
    btn_sair.grid(row=1, column=4, padx=(10,0), )

    # Tabela para exibir os itens cadastrados
    style = ttk.Style()

    # Configurando o estilo do heading da Treeview
    style.configure("Treeview.Heading", font=("Arial", 14)) 
    style.configure("Treeview", font=("Arial", 14))  
    
    # Colunas da Tabela
    columns = ["Cod", "EAN", "Descrição", "PUni R$"]
    tree = ttk.Treeview(janela_cadastrar, columns=columns, show="headings", height=14)
    
    # Definindo os cabeçalhos e as larguras das colunas
   
    tree.heading("Cod", text="Cod")
    tree.column("Cod", anchor=tk.CENTER, width=20)  

    tree.heading("EAN", text="EAN")
    tree.column("EAN", anchor=tk.CENTER, width=50)

    tree.heading("Descrição", text="Descrição")
    tree.column("Descrição", anchor=tk.CENTER, width=100)  

    tree.heading("PUni R$", text="PUni R$")
    tree.column("PUni R$", anchor=tk.CENTER, width=40)  #

    tree.pack(fill=ctk.BOTH, expand=False,padx=20,pady=20)

    janela_cadastrar.wait_window()

# Chama a função para abrir a interface de cadastro
#novo_item()
