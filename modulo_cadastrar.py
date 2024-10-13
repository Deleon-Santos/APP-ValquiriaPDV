#quero refatorar esse codigo para customtkinter aproveitando a aparencia e caracteristicas do codigo e comentando ao maximo as funcionalidades

import customtkinter as ctk
import json

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk , messagebox # Importa o Treeview do Tkinter padrão

import json
carrinho = []

# Função para adicionar novo item ao carrinho
def novo_item():
    # Carregar os dados existentes do arquivo JSON
    with open("bd.txt", 'r') as arquivo:
        dic = json.load(arquivo)

    # Função que será chamada ao clicar no botão "Cadastrar"
    def cadastrar_item():
        try:
            # Validação: verificar se os campos estão preenchidos
            if not entry_produto.get() or not entry_preco.get() or not entry_ean.get():
                messagebox.showerror(title="ERRO CADASTRO", message="Preencha os campos necessários!", icon="warning")
                return

            # Extrair os valores dos campos
            preco_material = str(entry_preco.get()).replace(",", ".").replace(" ", "0")
            descricao_material = entry_produto.get().title()
            ean_material = str(int(entry_ean.get()))  # Converte EAN para int e de volta para string
            codigo_material = str(len(dic) + 101)  # Gera o código do material baseado no tamanho do dicionário
            
            # Adicionar o item ao carrinho
            carrinho.append([codigo_material, ean_material, descricao_material, float(preco_material)])

            # Atualizar o dicionário com o novo item
            cadastro_item = {"cod": codigo_material, "ean": ean_material, "item": descricao_material, "preco": float(preco_material)}
            dic.append(cadastro_item)

            # Salvar o novo dicionário no arquivo JSON
            with open("bd.txt", 'w') as arquivo:
                json.dump(dic, arquivo, indent=4)

            # Atualizar a tabela visualmente
            atualizar_tabela()

            # Limpar os campos de entrada após o cadastro
            entry_produto.delete(0, ctk.END)
            entry_preco.delete(0, ctk.END)
            entry_ean.delete(0, ctk.END)
        
        except ValueError:
            messagebox.showerror(title="ERRO CADASTRO", message="Informe Preço ou EAN\n em valor numérico", icon="warning")

    # Função para atualizar a tabela visual
    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)  # Limpar a tabela
        for item in carrinho:
            tree.insert("", "end", values=item)  # Inserir novos valores na tabela

    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("dark-blue")  # Tema de cores azul-escuro

    # Janela principal
    janela = ctk.CTk()
    janela.title("CADASTRAR ITENS")
    janela.geometry("800x400")  # Define o tamanho da janela
    janela.resizable(width=False, height=False)
    #Frame master
    frame_marte= ctk.CTkFrame(janela,width=600)
    frame_marte.pack(pady=0,padx=0)

    #intens do cadastro
    frame_cadastro= ctk.CTkFrame(frame_marte)
    frame_cadastro.pack()

    lbl_cod = ctk.CTkLabel(frame_cadastro, text="Codigo:", width=44)
    lbl_cod.grid(row=0, column=0, padx=0, pady=0)
    
    entry_cod = ctk.CTkEntry(frame_cadastro, width=70,font=('Ariel',16))
    entry_cod.grid(row=1, column=0, padx=10, pady=10)

    # Descrição
    lbl_descricao = ctk.CTkLabel(frame_cadastro, text="Descrição:", width=44)
    lbl_descricao.grid(row=0, column=1, padx=10, pady=10)
    
    # Campo de entrada para o nome do produto
    entry_produto = ctk.CTkEntry(frame_cadastro, width=300,font=('Ariel',16))
    entry_produto.grid(row=1, column=1, padx=10, pady=10)

    # EAN
    lbl_ean = ctk.CTkLabel(frame_cadastro, text="EAN:", width=25)
    lbl_ean.grid(row=0, column=2, padx=10, pady=10)

    # Campo de entrada para o EAN
    entry_ean = ctk.CTkEntry(frame_cadastro, width=130,font=('Ariel',16))
    entry_ean.grid(row=1, column=2, padx=10, pady=10)

    # Preço
    lbl_preco = ctk.CTkLabel(frame_cadastro, text="Preço R$:", width=10)
    lbl_preco.grid(row=0, column=3, padx=10, pady=10)

    # Campo de entrada para o preço
    entry_preco = ctk.CTkEntry(frame_cadastro, width=100,font=('Ariel',16))
    entry_preco.grid(row=1, column=3, padx=10, pady=10)

    # Botão para cadastrar o item
    btn_cadastrar = ctk.CTkButton(frame_cadastro, text="CADASTRAR", command=cadastrar_item,width=40)
    btn_cadastrar.grid(row=0, column=4, padx=10, pady=10)

    # Botão para sair do programa
    btn_sair = ctk.CTkButton(frame_cadastro, text="SAIR", fg_color="red", command=janela.quit,width=90)
    btn_sair.grid(row=1, column=4, padx=10, pady=10)

    # Tabela para exibir os itens cadastrados
    style = ttk.Style()

    # Configurando o estilo do heading da Treeview
    style.configure("Treeview.Heading", font=("Arial", 13,))  # Aumenta o tamanho da fonte do cabeçalho
    style.configure("Treeview", font=("Arial", 11))  # Configura a fonte dos valores
    
    # Colunas da Tabela
    columns = ["Cod", "EAN", "Descrição", "PUni R$"]
    tree = ttk.Treeview(janela, columns=columns, show="headings", height=15)
    
    # Definindo os cabeçalhos e as larguras das colunas
   
    tree.heading("Cod", text="Cod")
    tree.column("Cod", anchor=tk.CENTER, width=50)  # Definindo largura para coluna "Cod"

    tree.heading("EAN", text="EAN")
    tree.column("EAN", anchor=tk.CENTER, width=150)  # Definindo largura para coluna "EAN"

    tree.heading("Descrição", text="Descrição")
    tree.column("Descrição", anchor=tk.CENTER, width=400)  # Definindo largura para coluna "Descrição"

    tree.heading("PUni R$", text="PUni R$")
    tree.column("PUni R$", anchor=tk.CENTER, width=150)  # Definindo largura para coluna "PUni R$"


    #posicionamneto da janela
    tree.pack(fill=ctk.BOTH, expand=False,padx=20,pady=20)

    """tree = ctk.CTkTreeview(janela, columns=("cod", "ean", "descricao", "preco"), show="headings", height=10)
    tree.pack( padx=10, pady=10)

    # Configurando cabeçalhos da tabela
    tree.heading("cod", text="Cod")
    tree.heading("ean", text="EAN")
    tree.heading("descricao", text="Descrição")
    tree.heading("preco", text="Preço R$")

    # Ajuste de largura das colunas
    tree.column("cod", width=50)
    tree.column("ean", width=100)
    tree.column("descricao", width=200)
    tree.column("preco", width=70)"""

    

    # Executar a janela
    janela.mainloop()

# Chama a função para abrir a interface de cadastro
novo_item()
