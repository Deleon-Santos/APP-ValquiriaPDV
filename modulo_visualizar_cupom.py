import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import tkinter
import modulo_arquivar as arquivar

# Lista de itens (exemplo)
lista_itens = []

# Lista de cupons disponíveis (será preenchida pelo loop)
cupom_disponivel = []

# Lista de dados (exemplo)
lista_dados = []
   

# Preencher cupom_disponivel com os números de cupom (índice 0 da lista_dados)

# Função para pesquisar cupons (ainda não implementada)
def pesquisar_cupom(lista_dados):
    
    
    cupom_selecionado = cupom_combobox.get()
    
    # Limpar a Treeview antes de atualizar
    for item in tree.get_children():
        tree.delete(item)
    
    # Buscar dados do cupom na lista de dados
    for dado in lista_dados:
        if str(dado[0]) == cupom_selecionado:
            # Atualizar os campos de Entry
            cnpj_entry.delete(0, ctk.END)
            cnpj_entry.insert(0, dado[4])
            empresa_entry.delete(0, ctk.END)
            empresa_entry.insert(0, dado[5])
            cliente_entry.delete(0, ctk.END)
            cliente_entry.insert(0, dado[3])
            valor_entry.delete(0, ctk.END)
            valor_entry.insert(0, dado[2])
            data_entry.delete(0, ctk.END)
            data_entry.insert(0, dado[1])
            usuario_entry.delete(0, ctk.END)
            usuario_entry.insert(0, dado[6])
            break

    # Obter itens associados ao cupom
    lista_itens = arquivar.lista_itens_por_carrinho(cupom_selecionado)

    # Adicionar itens à Treeview
    for item in lista_itens:
        tree.insert('', 'end', values=(item["ITEM"], item["EAN"], item["Descrição"], item["Qtd"], item["Valor"]))
    
    messagebox.showinfo("Pesquisa", f"Resultados para o cupom {cupom_selecionado}")

# Função para imprimir o cupom
def imprimir_cupom(cupom, valor, data, usuario, cnpj, empresa):
    """Função para imprimir o cupom."""
    messagebox.showinfo("Imprimir", f"Imprimindo cupom {cupom} - Valor: {valor}, Data: {data}, Operador: {usuario}, CNPJ: {cnpj}, Empresa: {empresa}")
    print(f"Imprimindo cupom {cupom}")

def venda_por_cupom(lista_dados):
    # Preencher cupom_disponivel com os números de cupom (índice 0 da lista_dados)
    for dado in lista_dados:
        cupom_disponivel.append(str(dado[0]))  # Adiciona o número do cupom (índice [0]) à lista

    # Criando a janela principal
    janela = ctk.CTkToplevel()
    janela.title("VENDA CUPOM")
    janela.geometry('800x600')
    janela.focus_force()
    janela.grab_set()
    # Criando os frames das tabelas
    frame_master = ctk.CTkFrame(janela)
    frame_master.pack(padx=10, pady=10)
    frame1 = ctk.CTkFrame(frame_master)
    frame1.grid(row=0, column=0)

    # Layout da interface
    ctk.CTkLabel(frame1, text="CNPJ ", width=24).grid(row=0, column=0, padx=20, sticky="w")
    ctk.CTkLabel(frame1, text="Empresa ", width=39).grid(row=0, column=1, padx=20, sticky="w")
    ctk.CTkLabel(frame1, text="Cliente").grid(row=0, column=2, padx=20, sticky="w")

    cnpj_entry = ctk.CTkEntry(frame1, width=160, font=('Ariel', 18))
    cnpj_entry.grid(row=1, column=0, padx=20)

    empresa_entry = ctk.CTkEntry(frame1, width=330, font=('Ariel', 16))
    empresa_entry.grid(row=1, column=1, padx=20)

    cliente_entry = ctk.CTkEntry(frame1, width=160, font=('Ariel', 16))
    cliente_entry.grid(row=1, column=2, padx=20)

    frame_2 = ctk.CTkFrame(frame_master)
    frame_2.grid(row=2, column=0)

    ctk.CTkLabel(frame_2, text="Valor Cupom R$").grid(row=2, column=0, padx=20, sticky="w")
    ctk.CTkLabel(frame_2, text="Data da Compra").grid(row=2, column=1, padx=20, sticky="w")
    ctk.CTkLabel(frame_2, text="Operador").grid(row=2, column=2, padx=20, sticky="w")
    ctk.CTkLabel(frame_2, text="N° Cupom").grid(row=2, column=3, padx=20, sticky="w")

    valor_entry = ctk.CTkEntry(frame_2, width=110)
    valor_entry.grid(row=3, column=0, padx=20)

    data_entry = ctk.CTkEntry(frame_2, width=200)
    data_entry.grid(row=3, column=1, padx=20)

    usuario_entry = ctk.CTkEntry(frame_2, width=200)
    usuario_entry.grid(row=3, column=2, padx=20)

    # ComboBox para selecionar o número do cupom (preenchido pela lista cupom_disponivel)
    cupom_combobox = ctk.CTkComboBox(frame_2, values=cupom_disponivel, width=100, font=('Ariel', 16))
    cupom_combobox.grid(row=3, column=3, padx=20)

    frame_botoes = ctk.CTkFrame(frame_master)
    frame_botoes.grid(row=4, column=0)

    # Botões
    ctk.CTkButton(frame_botoes, text="PESQUISAR", command=lambda: pesquisar_cupom(lista_dados)).grid(row=4, column=0, padx=20, pady=20)
    ctk.CTkButton(frame_botoes, text="IMPRIMIR", command=lambda: imprimir_cupom(cupom_combobox.get(), valor_entry.get(), data_entry.get(), usuario_entry.get(), cnpj_entry.get(), empresa_entry.get())).grid(row=4, column=1, padx=20, pady=20)
    ctk.CTkButton(frame_botoes, text="SAIR", command=janela.destroy, fg_color='red').grid(row=4, column=2, padx=20, pady=20)

    # Estilos da Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 14))  # Aumenta o tamanho da fonte do cabeçalho
    style.configure("Treeview", font=("Arial", 14))  # Configura a fonte dos valores
    
    # Criando a Treeview para os itens
    tree = ttk.Treeview(frame_master, columns=("ITEM", "EAN", "Descrição", "Qtd", "Valor"), show='headings', height=20)
    tree.heading("ITEM", text="ITEM")
    tree.heading("EAN", text="EAN")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Qtd", text="Qtd")
    tree.heading("Valor", text="Valor")

    tree.column("ITEM", anchor=tkinter.CENTER, width=90)
    tree.column("EAN", anchor=tkinter.CENTER, width=200)
    tree.column("Descrição", anchor=tkinter.CENTER, width=400)
    tree.column("Qtd", anchor=tkinter.CENTER, width=80)
    tree.column("Valor", anchor=tkinter.CENTER, width=150)

    # Adicionando a Treeview ao layout
    tree.grid(row=6, column=0, columnspan=5, padx=20, pady=20)

    # Populando a Treeview com os itens
    for item in lista_itens:
        tree.insert('', 'end', values=(item["ITEM"], item["EAN"], item["Descrição"], item["Qtd"], item["Valor"]))

    # Loop principal da janela
    janela.wait_window()

#venda_por_cupom()
