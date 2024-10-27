   # Printar o import customtkinter as ctk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import tkinter
import modulo_arquivar as arquivar

# Lista de itens (exemplo)
#lista_itens = [(1001, 1, '117', '7890000000117', 'Refrigerante Coca-Cola 2+250lt', 1, 8.9, 8.9)]
lista_itens=[]
# Lista de cupons disponíveis (será preenchida pelo loop)
cupom_disponivel = []

# Lista de dados (exemplo)
#lista_info = [(1000, '2024-03-21 17:41:22', 0.0, '000.000.000-00', '45.333.0001/45', 'Tem De Tudo ME', 'Administrador')]
#lista_info =[]
cupom_select=''   

# Preencher cupom_disponivel com os números de cupom (índice 0 da lista_dados)

def venda_por_cupom(lista_dados):
    #nonlocal losta_info
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
    cupom_var = ctk.StringVar(value="1001") #declaração da keys do combobox
    cupom_combobox = ctk.CTkComboBox(frame_2, values=cupom_disponivel, variable = cupom_var,  width=100, font=('Ariel', 16))
    cupom_combobox.grid(row=3, column=3, padx=20)

    frame_botoes = ctk.CTkFrame(frame_master)
    frame_botoes.grid(row=4, column=0)

    # Botões
    ctk.CTkButton(frame_botoes, text="PESQUISAR", command=lambda: pesquisar_cupom(cupom_var,lista_dados, cnpj_entry, empresa_entry, cliente_entry, valor_entry, data_entry, usuario_entry, tree)).grid(row=4, column=0, padx=20, pady=20)
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
    #for item in lista_itens:
        #tree.insert('', 'end', values=(item[1], item[3], item[4], item[5], item[7]))

    janela.wait_window()
# Função para pesquisar cupons (ainda não implementada)

def pesquisar_cupom(cupom_var,lista_dados, cnpj_entry, empresa_entry, cliente_entry, valor_entry, data_entry, usuario_entry, tree):
     # Limpa a árvore de exibição dos itens do carrinho
    tree.delete(*tree.get_children())  # Remove todos os itens da Treeview

    lista_info = []
    
    
    cupom_select = int(cupom_var.get())

    # Printar o valor no console
    print(f"Cupom selecionado: {cupom_select}")
    
    for dado in lista_dados:
        
        if dado[0] == cupom_select:
            lista_info = dado
            print(f"lista info {lista_info}")
            
            cnpj_entry.delete(0, 'end')
            cnpj_entry.insert(0, lista_info[4])
            empresa_entry.delete(0, 'end')
            empresa_entry.insert(0, lista_info[5])
            cliente_entry.delete(0, 'end')
            cliente_entry.insert(0, lista_info[3])
            valor_entry.delete(0, 'end')
            valor_entry.insert(0, lista_info[2])
            data_entry.delete(0, 'end')
            data_entry.insert(0, lista_info[1])
            usuario_entry.delete(0, 'end')
            usuario_entry.insert(0, lista_info[6])
            break
    #lista_info.clear()
            

    # Obter itens associados ao cupom
    lista_itens = arquivar.lista_item_por_carrinho(cupom_select)
    
    # Printar a lista de itens para o cupom
    print(f"Itens do cupom {cupom_select}: {lista_itens}")
    
     # Populando a Treeview com os itens
    for item in lista_itens:
        tree.insert('', 'end', values=(item[1], item[3], item[4], item[5], item[7]))
    
    lista_itens.clear()
    print(f"lista itens e info depois do clear {lista_itens}, {lista_info}")
    return 
    

#venda_por_cupom()
