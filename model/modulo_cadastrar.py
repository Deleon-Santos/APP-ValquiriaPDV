
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk , messagebox 
import model.modulo_arquivar as arquivar
ctk.set_appearance_mode("light")  # Modo de aparência escura
ctk.set_default_color_theme("database/themas.txt")  # Tema de cores azul-escuro

cadartar_aberto = False  # Variável para controlar se a janela de cadastro está aberta

def novo_item():
    global cadartar_aberto
    if cadartar_aberto:
        return
    cadartar_aberto = True
    
    def atualizar_tabela(item_cadastrado):
        tree.insert("", "end", values=item_cadastrado)  

    def cadastrar_item():
        try:
            if not entry_produto.get() or not entry_preco.get() or not entry_ean.get():
                messagebox.showerror(title="ERRO CADASTRO", message="Preencha os campos necessários!", icon="warning")
                return

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

    # Janela principal
    janela_cadastrar = ctk.CTkToplevel()
    janela_cadastrar.title("CADASTRAR ITENS")
    janela_cadastrar.geometry("826x420+696+142")  # Define o tamanho da janela_cadastrar
    janela_cadastrar.resizable(width=False, height=False)
    janela_cadastrar.focus_force()
    janela_cadastrar.grab_set()
    
    def fechar_janela():
        global cadartar_aberto
        cadartar_aberto = False
        janela_cadastrar.destroy()
    janela_cadastrar.protocol("WM_DELETE_WINDOW", fechar_janela)
    
    frame_cadastro= ctk.CTkFrame(janela_cadastrar)
    frame_cadastro.pack(padx=20,pady=10, fill=ctk.BOTH, expand=True)

    lbl_descricao = ctk.CTkLabel(frame_cadastro, text="Descrição:", width=44)
    lbl_descricao.grid(row=0, column=1, padx=(10,0), pady=(10,0),sticky='w')
    
    entry_produto = ctk.CTkEntry(frame_cadastro, width=320,font=('Helvetica',18))
    entry_produto.grid(row=1, column=1, padx=(10,30),pady=(0,10), sticky='w')

    lbl_ean = ctk.CTkLabel(frame_cadastro, text="EAN:", width=28)
    lbl_ean.grid(row=0, column=2, padx=0, pady=(10,0),sticky='w')

    entry_ean = ctk.CTkEntry(frame_cadastro, width=150,font=('Helvetica',18))
    entry_ean.grid(row=1, column=2, padx=(0,30),pady=(0,10), sticky='w')

    lbl_preco = ctk.CTkLabel(frame_cadastro, text="Preço R$:", width=10)
    lbl_preco.grid(row=0, column=3, padx=0, pady=(10,0),sticky='w')

    entry_preco = ctk.CTkEntry(frame_cadastro, width=100,font=('Helvetica',18))
    entry_preco.grid(row=1, column=3, padx=(0,30),pady=(0,10),  sticky='w')

    btn_cadastrar = ctk.CTkButton(frame_cadastro, text="CADASTRAR", command=cadastrar_item,width=90)
    btn_cadastrar.grid(row=1, column=4, padx=(0,0),pady=(0,10),  sticky='w')

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 14)) 
    style.configure("Treeview", font=("Arial", 14))  
    
    columns = ["Cod", "EAN", "Descrição", "PUni R$"]
    tree = ttk.Treeview(janela_cadastrar, columns=columns, show="headings", height=14)
   
    tree.heading("Cod", text="Cod")
    tree.column("Cod", anchor=tk.CENTER, width=20)  
    tree.heading("EAN", text="EAN")
    tree.column("EAN", anchor=tk.CENTER, width=50)
    tree.heading("Descrição", text="Descrição")
    tree.column("Descrição", anchor=tk.CENTER, width=100)  
    tree.heading("PUni R$", text="PUni R$")
    tree.column("PUni R$", anchor=tk.CENTER, width=40)  #

    tree.pack(fill=ctk.BOTH, expand=False,padx=20,pady=20)

    btn_sair = ctk.CTkButton(janela_cadastrar, text="SAIR", fg_color="red", command=fechar_janela,width=90)
    btn_sair.pack( padx=(10,0), pady=10 )

    janela_cadastrar.wait_window()