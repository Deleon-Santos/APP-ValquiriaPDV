import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

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
    
    root = tk.Tk()
    root.title("NOVO PEDIDO")
    root.geometry("1280x720")

    # Menu
    menu_bar = tk.Menu(root)
    menu_novo = tk.Menu(menu_bar, tearoff=0)
    menu_novo.add_command(label="Nova Compra", command=lambda: nova_compra())
    menu_novo.add_command(label="Nova Pesquisa", command=lambda: nova_pesquisa())
    menu_novo.add_command(label="Novo Item", command=lambda: novo_item())
    menu_bar.add_cascade(label="Novo", menu=menu_novo)

    menu_totais = tk.Menu(menu_bar, tearoff=0)
    menu_totais.add_command(label="Venda Cupom", command=lambda: venda_cupom())
    menu_bar.add_cascade(label="Totais", menu=menu_totais)

    menu_suporte = tk.Menu(menu_bar, tearoff=0)
    menu_suporte.add_command(label="Ajuda", command=lambda: mostrar_ajuda())
    menu_bar.add_cascade(label="Suporte", menu=menu_suporte)

    menu_fechar = tk.Menu(menu_bar, tearoff=0)
    menu_fechar.add_command(label="Fechar", command=lambda: root.quit())
    menu_bar.add_cascade(label="Fechar", menu=menu_fechar)

    root.config(menu=menu_bar)

    # Frames
    frame_esquerda = tk.Frame(root)
    frame_esquerda.pack(side=tk.LEFT, fill=tk.Y)

    frame_direita = tk.Frame(root)
    frame_direita.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Tabela
    columns = ["Item", "Cod", "EAN", "Descrição", "Qtd", "PUni R$", "Preço R$"]
    tree = ttk.Treeview(frame_direita, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    tree.pack(fill=tk.BOTH, expand=True)

    # Informações do Produto
    label_cod = ttk.Label(frame_esquerda, text="Código do Produto")
    label_cod.pack()
    entry_cod = ttk.Entry(frame_esquerda, font=("Arial", 14))
    entry_cod.pack()

    label_descricao = ttk.Label(frame_esquerda, text="Descrição do Produto")
    label_descricao.pack()
    entry_descricao = ttk.Entry(frame_esquerda, font=("Arial", 14))
    entry_descricao.pack()

    label_qtd = ttk.Label(frame_esquerda, text="Quantidade")
    label_qtd.pack()
    entry_qtd = ttk.Entry(frame_esquerda, font=("Arial", 14))
    entry_qtd.pack()

    # Botões
    button_adicionar = ttk.Button(frame_esquerda, text="ADICIONAR", command=lambda: adicionar_item())
    button_adicionar.pack(fill=tk.X)

    button_deletar = ttk.Button(frame_esquerda, text="DELETE", command=lambda: deletar_item())
    button_deletar.pack(fill=tk.X)

    button_pagar = ttk.Button(frame_esquerda, text="PAGAR", command=lambda: pagar_items())
    button_pagar.pack(fill=tk.X)

    button_voltar = ttk.Button(frame_esquerda, text="VOLTAR", command=lambda: voltar())
    button_voltar.pack(fill=tk.X)

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

    root.mainloop()

# Teste da função
usuario, data, empresa = "Administrador", '2024-03-21 17:41:22', "Tem De Tudo ME"
sistema(usuario, data, empresa)
