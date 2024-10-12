# SISTEMA DE COBRANÇA EM CAIXA DE SUPERMERCADOS E AFINS
# Este sistema está em desenvolvimento em caráter acadêmico

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk  # Importa o Treeview do Tkinter padrão

import json
#import modulo_pagar as pagar
#import modulo_remover as remover
#import modulo_pesquisar as pesquisar
#import modulo_cadastro como cadastrar
#import modulo_limpar como limpar
#import modulo_adicionar como adicionar
#import modulo_visualisar como visualizar
#import modulo_arquivar como arquivar
#import modulo_cpf

# Função principal do sistema
def sistema(usuario, data, empresa):
    carrinho = []
    cupom = 1000  # Número inicial do cupom
    valor_pagar = 0
    num_item = 0
    cpf = "000.000.000-00"
    cnpj = '45.333.0001/45'
    
    # Função para fechar a janela e encerrar o sistema
    def fechar_sistema():
        if ctk.messagebox.askokcancel("Fechar", "Deseja realmente fechar o sistema?"):
            janela.destroy()
    
    # Função para adicionar itens ao carrinho
    def adicionar_item():
        material = entrada_ean.get()
        descricao = entrada_descricao.get()
        qtd = int(entrada_qtd.get())
        
        if not material:
            ctk.messagebox.showerror("Erro", "Erro no campo material!")
            return
        if qtd < 1 or qtd > 99:
            ctk.messagebox.showerror("Erro", "Erro no campo Quantidade!")
            return
        
        # Buscar produto no banco de dados
        plu_pro = adicionar.achar(material, dic)
        if plu_pro is False:
            ctk.messagebox.showerror("Erro", "Produto não encontrado!")
            return
        
        # Adicionar item ao carrinho
        for item in dic:
            if item["cod"] == plu_pro:
                nonlocal num_item, valor_pagar
                num_item += 1
                ean = item["ean"]
                material = item["item"]
                preco_unitario = item["preco"]
                preco = item['preco'] * qtd
                valor_pagar += preco
                carrinho.append([num_item, plu_pro, ean, material, qtd, preco_unitario, preco])
        
        # Atualizar a tabela e os campos de total
        tabela_carrinho.insert("", "end", values=(num_item, plu_pro, ean, material, qtd, f"{preco_unitario:.2f}", f"{preco:.2f}"))
        label_subtotal.config(text=f"R$ {valor_pagar:.2f}")

    # Configuração da janela principal usando CustomTkinter
    janela = ctk.CTk()
    janela.title("Sistema de Cobrança - Projeto Valquíria")
    janela.geometry("800x800")
    
    # Criação dos widgets
    label_titulo = ctk.CTkLabel(janela, text="Sistema de Cobrança", font=("Arial", 24))
    label_titulo.pack(pady=10)
    
    # Criando uma tabela usando o Treeview do Tkinter
    colunas = ("Item", "Cod", "EAN", "Descricao", "Qtd", "PUni R$", "Preco R$")
    tabela_carrinho = ttk.Treeview(janela, columns=colunas, show='headings')

    # Configurando os cabeçalhos das colunas
    tabela_carrinho.heading("Item", text="Item")
    tabela_carrinho.heading("Cod", text="Código")
    tabela_carrinho.heading("EAN", text="EAN")
    tabela_carrinho.heading("Descricao", text="Descrição")
    tabela_carrinho.heading("Qtd", text="Qtd")
    tabela_carrinho.heading("PUni R$", text="Preço Unitário")
    tabela_carrinho.heading("Preco R$", text="Preço")

    # Definindo o tamanho das colunas
    tabela_carrinho.column("Item", width=50)
    tabela_carrinho.column("Cod", width=100)
    tabela_carrinho.column("EAN", width=120)
    tabela_carrinho.column("Descricao", width=200)
    tabela_carrinho.column("Qtd", width=50)
    tabela_carrinho.column("PUni R$", width=100)
    tabela_carrinho.column("Preco R$", width=100)

    # Exibindo a tabela na janela
    tabela_carrinho.pack(pady=20)

    
    # Entradas de EAN, Descrição e Quantidade
    entrada_ean = ctk.CTkEntry(janela, placeholder_text="Código EAN")
    entrada_ean.pack(pady=5)
    entrada_descricao = ctk.CTkEntry(janela, placeholder_text="Descrição do Produto")
    entrada_descricao.pack(pady=5)
    entrada_qtd = ctk.CTkEntry(janela, placeholder_text="Quantidade")
    entrada_qtd.pack(pady=5)
    
    # Botão para adicionar item
    botao_adicionar = ctk.CTkButton(janela, text="Adicionar", command=adicionar_item)
    botao_adicionar.pack(pady=10)
    
    # Subtotal e pagamento
    label_subtotal = ctk.CTkLabel(janela, text=f"Total: R$ {valor_pagar:.2f}", font=("Arial", 20))
    label_subtotal.pack(pady=10)
    
    # Botão para fechar o sistema
    botao_fechar = ctk.CTkButton(janela, text="Fechar", command=fechar_sistema)
    botao_fechar.pack(pady=10)
    # Exibir dados do operador e data
    data_label = ctk.CTkLabel(janela, text=f"Data: {data}", font=("Any", 14))
    data_label.grid(row=6, column=0, padx=10, pady=10)

    usuario_label = ctk.CTkLabel(janela, text=f"Operador: {usuario}", font=("Any", 14))
    usuario_label.grid(row=6, column=1, padx=10, pady=10)
    
    # Loop principal da interface
    janela.protocol("WM_DELETE_WINDOW", fechar_sistema)
    janela.mainloop()


# Função para inicializar o sistema
usuario, data, empresa = "Administrador", '2024-03-21 17:41:22', "Tem De Tudo ME"
sistema(usuario, data, empresa)
