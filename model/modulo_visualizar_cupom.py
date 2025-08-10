import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import tkinter

import model.modulo_arquivar as arquivar
import model.modulo_imprimir as imprimir


cupom_disponivel = []

visualisar_janela = False  # Variável para controlar se a janela de visualização do cupom está aberta

def venda_por_cupom(lista_dados):
    global visualisar_janela
    if visualisar_janela:
        
        return
    visualisar_janela =True
    lista_itens = []
    lista_info = []
    cupom_disponivel.clear()
    
    for dado in lista_dados: 
        cupom_disponivel.append(str(dado[0])) 

    # Criando a janela principal
    janela = ctk.CTkToplevel()
    janela.title("VENDA CUPOM")
    janela.geometry('826x420+696+142')
    janela.iconbitmap("img/img5.ico")
    janela.focus_force()
    janela.grab_set()
    
    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("database/themas.txt") 

    def fechar_janela():
        global visualisar_janela
        visualisar_janela = False
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", fechar_janela)

    # Configuração dos frames
    frame_master = ctk.CTkFrame(janela)
    frame_master.pack(padx=10, pady=(20,0))
    frame1 = ctk.CTkFrame(frame_master,fg_color='transparent')
    frame1.grid(row=0, column=0)

    # Configuração da interface
    ctk.CTkLabel(frame1, text="CNPJ ").grid(row=0, column=0, padx=20, sticky="w")
    ctk.CTkLabel(frame1, text="Empresa ").grid(row=0, column=1, padx=20, sticky="w")
    ctk.CTkLabel(frame1, text="Cliente").grid(row=0, column=2, padx=20, sticky="w")

    cnpj_entry = ctk.CTkEntry(frame1, width=160, font=('Ariel', 18))
    cnpj_entry.grid(row=1, column=0, padx=20)

    empresa_entry = ctk.CTkEntry(frame1, width=330, font=('Ariel', 18))
    empresa_entry.grid(row=1, column=1, padx=20)

    cliente_entry = ctk.CTkEntry(frame1, width=160, font=('Ariel', 18))
    cliente_entry.grid(row=1, column=2, padx=20)

    frame_2 = ctk.CTkFrame(frame_master,fg_color='transparent')
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
    
    # ComboBox para selecionar o número do cupom
    cupom_var = ctk.StringVar(value="1001")
    cupom_combobox = ctk.CTkComboBox(frame_2, values=cupom_disponivel, variable=cupom_var, width=100, font=('Ariel', 16),)
    cupom_combobox.grid(row=3, column=3, padx=20)

    frame_botoes = ctk.CTkFrame(janela,fg_color='transparent')
    frame_botoes.pack(padx=10)

    # Botões
    ctk.CTkButton(frame_botoes, text="PESQUISAR", command=lambda: pesquisar_cupom(cupom_var, cnpj_entry, empresa_entry, cliente_entry, valor_entry, data_entry, usuario_entry, tree)).grid(row=4, column=0, padx=20, pady=20)
    ctk.CTkButton(frame_botoes, text="IMPRIMIR", command=lambda: imprimir_cupom()).grid(row=4, column=1, padx=20, pady=20)
    ctk.CTkButton(frame_botoes, text="SAIR", command=fechar_janela, fg_color='red').grid(row=4, column=2, padx=20, pady=20)

    # Configuração da Treeview para exibir os itens
    tree = ttk.Treeview(frame_master, columns=("Item", "EAN", "Descrição", "Qtd", "Valor"), show='headings', height=11)
    
    tree.heading("Item", text="Item")
    tree.heading("EAN", text="EAN")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Qtd", text="Qtd")
    tree.heading("Valor", text="Valor")

    tree.column("Item", anchor=tkinter.CENTER, width=90)
    tree.column("EAN", anchor=tkinter.CENTER, width=200)
    tree.column("Descrição", anchor=tkinter.CENTER, width=400)
    tree.column("Qtd", anchor=tkinter.CENTER, width=80)
    tree.column("Valor", anchor=tkinter.CENTER, width=150)

    tree.grid(row=6, column=0, columnspan=5, padx=20, pady=(20,10))

    def imprimir_cupom():
        nonlocal lista_itens, lista_info
        informacao = '\n'  
        
        if lista_info:
            informacao += f"Razão Social: {lista_info[5]}\n" 
            informacao += f"End: AV. Boa Vista n-1012 Santa Rosa/SP\nCNPJ: {lista_info[4]}  IE : 07.112.888/000-00\n\n"    
            informacao += f"Data: {lista_info[1]}\nCliente: {lista_info[3]}\nOperador: {lista_info[6]}\nCupom: {lista_info[0]}\nValor RS: {lista_info[2]}" 
           
            lista_itens = arquivar.lista_item_por_carrinho(lista_info[0]) # Pegar os itens do carrinho             
            gerar_pdf = imprimir.create_pdf(lista_info, lista_itens)
            
            if gerar_pdf:
                messagebox.showinfo("PDF", "IMPRESSÃO CONCLUÍDA")
            else:
                messagebox.showerror("PDF", "ERRO AO GERAR IMPRESSÃO")
        else:
            print("Erro: lista_info está vazia ou não foi preenchida corretamente.")

    
    def pesquisar_cupom(cupom_var, cnpj_entry, empresa_entry, cliente_entry, valor_entry, data_entry, usuario_entry, tree):
        nonlocal lista_info, lista_dados
        tree.delete(*tree.get_children())
        cupom_select = int(cupom_var.get())
        print(f"Cupom selecionado: {cupom_select}")
        
        for dado in lista_dados:
            if dado[0] == cupom_select:
                lista_info = dado
                
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

        lista_itens = arquivar.lista_item_por_carrinho(cupom_select)

        for item in lista_itens:
            tree.insert('', 'end', values=(item[1], item[3], item[4], item[5], f"{item[7]:.2f}")) 
        return 

    janela.wait_window()




