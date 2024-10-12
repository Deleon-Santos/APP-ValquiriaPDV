import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import customtkinter as ctk
from PIL import Image

# Funções dos módulos
"""import modulo_pagar as pagar
import modulo_remover as remover
import modulo_pesquisar as pesquisar
import modulo_cadastro as cadastrar
import modulo_limpar as limpar
import modulo_adicionar as adicionar
import modulo_visualisar as visualizar
import modulo_arquivar as arquivar"""
#import modulo_cpf

def sistema(usuario, data, empresa):
    carrinho = []
    cupom = int(1000)
    valor_pagar = 0
    num_item = 0

    cpf = "000.000.000-00"
    cnpj = '45.333.0001/45'
    lista_dados = []

    # ===================================== Inicio da Interface Grafica=========================================
    
    janela = ctk.CTk()
    janela.title("ENTRADA E PEDIDO")
    janela.geometry("1280x720")

    # Menu
    menu_bar = tk.Menu(janela)
    menu_novo = tk.Menu(menu_bar, tearoff=0)
    menu_novo.add_command(label="Nova Compra", command=lambda: nova_compra())
    menu_novo.add_command(label="Nova Pesquisa", command=lambda: nova_pesquisa())
    menu_novo.add_command(label="Novo Item", command=lambda: novo_item())
    menu_bar.add_cascade(label="Novo", menu=menu_novo)

    label_titulo = ctk.CTkLabel(janela, text="Sistema de Cobrança", font=("Arial", 24))
    label_titulo.pack(pady=10)
    
    

    menu_totais = tk.Menu(menu_bar, tearoff=0)
    menu_totais.add_command(label="Venda Cupom", command=lambda: venda_cupom())
    menu_bar.add_cascade(label="Totais", menu=menu_totais)

    menu_suporte = tk.Menu(menu_bar, tearoff=0)
    menu_suporte.add_command(label="Ajuda", command=lambda: mostrar_ajuda())
    menu_bar.add_cascade(label="Suporte", menu=menu_suporte)

    menu_fechar = tk.Menu(menu_bar, tearoff=0)
    menu_fechar.add_command(label="Fechar", command=lambda: janela.quit())
    menu_bar.add_cascade(label="Fechar", menu=menu_fechar)

    janela.config(menu=menu_bar)

    
    
    
    
    
    frame_esquerda = ctk.CTkFrame(janela)
      # Posição e preenchimento do frame
    frame_esquerda.pack(side=ctk.LEFT, fill=ctk.Y ,pady=0, padx=20,  expand=True )

    # Carregar a imagem usando PIL (precisa da biblioteca Pillow)
    image_baner = "tdt.png"
    image = ctk.CTkImage(dark_image=Image.open(image_baner), size=(400, 200))

    # Criar um rótulo (Label) para exibir a imagem
    label = ctk.CTkLabel(frame_esquerda, image=image, text="")  # Definir text como vazio para mostrar apenas a imagem
    label.pack(pady=20)

    frame_inputs = ctk.CTkFrame(frame_esquerda )
    frame_inputs.pack()
    # Informações do Produto
    label_cod = ctk.CTkLabel(frame_esquerda, text="Código do Produto")
    label_cod.pack(pady=0)
    entry_cod = ctk.CTkEntry(frame_esquerda, font=("Arial", 10),width=300)
    entry_cod.pack(pady=0,padx=5)

    label_descricao = ctk.CTkLabel(frame_esquerda, text="Descrição do Produto")
    label_descricao.pack(pady=0 )
    entry_descricao = ctk.CTkEntry(frame_esquerda, font=("Arial", 10),width=300)
    entry_descricao.pack(pady=0, padx=5)

    label_qtd = ctk.CTkLabel(frame_esquerda, text="Quantidade")
    label_qtd.pack(pady=0)
    entry_qtd = ctk.CTkEntry(frame_esquerda, font=("Arial", 10), width=300)
    entry_qtd.pack(pady=0, padx=5)

    # Botões
    button_adicionar = ctk.CTkButton(frame_inputs, text="ADICIONAR", command=lambda: adicionar_item())
    button_deletar = ctk.CTkButton(frame_inputs, text="DELETE", command=lambda: deletar_item())
    button_pagar = ctk.CTkButton(frame_inputs, text="PAGAR", command=lambda: pagar_items())
    button_voltar = ctk.CTkButton(frame_inputs, text="VOLTAR", command=lambda: voltar())
    
    # Criar 4 botões
    button_adicionar.grid(row=0, column=0, padx=10, pady=10)
    button_deletar.grid(row=0, column=1, padx=10, pady=10)
    button_pagar.grid(row=1, column=0, padx=10, pady=10)
    button_voltar.grid(row=1, column=1, padx=10, pady=10)

    # ***cOMPONENTES DO FRAME DA DIREITA*** 
    frame_direita = ctk.CTkFrame(janela)
    frame_direita.pack(side=ctk.LEFT, fill=ctk.Y ,pady=20, padx=20,  expand=False)
    
    # lABEL
    frame_cupon = ctk.CTkFrame(frame_direita, width=600)
    frame_cupon.pack(pady= 1, padx=1)
    
    label_cupom = ctk.CTkLabel(frame_cupon, text="Cupom N°:")
    entry_cupom = ctk.CTkEntry(frame_cupon, font=("Arial", 14),width=100)
    label_cupom.grid(row=0, column=0, padx=10, pady=10)
    entry_cupom.grid(row=0, column=1, padx=10, pady=10)


    # Tabela
    columns = ["Item", "Cod", "EAN", "Descrição", "Qtd", "PUni R$", "Preço R$"]
    tree = ttk.Treeview(frame_direita, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    tree.pack(fill=ctk.BOTH, expand=True)

    # labels de usuario s e datas
    usuario_label = ctk.CTkLabel(frame_direita, text=f"Operador: {usuario}", font=("Any", 14))
    usuario_label.pack(padx=5, pady=5)
    data_label = ctk.CTkLabel(frame_direita, text=f"Data: {data}", font=("Any", 14))
    data_label.pack( padx=10, pady=10)

   
    # Funções
    def adicionar_item():
        nonlocal num_item, valor_pagar
        material = entry_cod.get()
        descricao = entry_descricao.get()
        qtd = int(entry_qtd.get())

        if not material or not descricao:
            messagebox.showerror("Erro", "Erro no campo material ou descrição!")
            return

        if qtd < 1 or qtd > 99:
            messagebox.showerror("Erro", "Erro no campo Quantidade!")
            return

        plu_pro = adicionar.achar(material, dic)
        if not plu_pro:
            messagebox.showerror("Erro", "Erro no campo material")
            return

        for item in dic:
            if item["cod"] == plu_pro:
                num_item += 1
                ean = item["ean"]
                material = item["item"]
                preco_unitario = item["preco"]
                preco = item["preco"] * qtd
                valor_pagar += preco
                produto = [num_item, plu_pro, ean, material, qtd, preco_unitario, preco]
                carrinho.append(produto)
                tree.insert("", "end", values=produto)

        entry_cod.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)

    def deletar_item():
        nonlocal valor_pagar
        selected_item = tree.selection()[0]
        valor_pagar = remover.remover(valor_pagar, carrinho, selected_item)
        tree.delete(selected_item)

    def pagar_items():
        nonlocal valor_pagar, carrinho, num_item, cupom
        v_pago = f"{valor_pagar:.2f}"
        valor_pagar = pagar.pagar(valor_pagar)

        if valor_pagar == 0:
            arquivar.arquivo(cupom, data, usuario, cnpj, cpf, v_pago, empresa, carrinho)
            limpar.limpar_saida(carrinho, tree, num_item)
            num_item = 0
            messagebox.showinfo("Info", "Pagamento realizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Erro ao realizar pagamento!")

    def voltar():
        nonlocal valor_pagar, num_item
        limpar.limpar_saida(carrinho, tree, num_item)
        valor_pagar = 0
        num_item = 0

    def nova_compra():
        nonlocal cupom
        count = arquivar.gerar_cupom()
        cupom += count
        # Limpa os campos e reseta o carrinho
        voltar()

    def nova_pesquisa():
        pesquisar.pesquisar(dic)

    def novo_item():
        if usuario == "Administrador":
            cadastrar.novo_item()
            atualizar_dic()
        else:
            messagebox.showerror("Erro", "Seu usuário não tem permissão para cadastrar item!")

    def venda_cupom():
        lista_dados = arquivar.lista_de_vendas()
        visualizar.venda_cupom(lista_dados)

    def mostrar_ajuda():
        try:
            with open('dados/ajuda.txt', 'r') as legenda:
                arquivo = legenda.read()
                messagebox.showinfo("Ajuda", arquivo)
        except FileNotFoundError:
            messagebox.showerror("Erro", "O arquivo 'SUPORTE' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")

    def atualizar_dic():
        nonlocal dic
        try:
            with open('bd.txt', 'r') as adic:
                dic = json.load(adic)
        except FileNotFoundError:
            messagebox.showerror("Erro", "O arquivo 'bd.txt' não foi encontrado!")

    # Inicializa o dicionário de produtos
    dic={}

    atualizar_dic()

    janela.mainloop()

# Teste da função
usuario, data, empresa = "Administrador", '2024-03-21 17:41:22', "Tem De Tudo ME"
sistema(usuario, data, empresa)



