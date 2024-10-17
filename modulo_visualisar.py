import customtkinter as ctk
#import modulo_imprimir as imprimir
import modulo_arquivar as arquivar

# Lista para armazenar dados da pesquisa de cupons
pesquisa_cupom = []
pesquisa = []

def formatar_valor(valor):
    """Formata o valor monetário com duas casas decimais."""
    return f"R$ {float(valor):.2f}"

def criar_tabela_cupons(parent):
    """Cria e retorna o frame da tabela de cupons."""
    frame = ctk.CTkScrollableFrame(parent)
    frame.grid_rowconfigure(0, weight=1)
    return frame

def criar_tabela_itens(parent):
    """Cria e retorna o frame da tabela de itens."""
    frame = ctk.CTkScrollableFrame(parent)
    frame.grid_rowconfigure(0, weight=1)
    return frame

def atualizar_tabela(frame, dados, titulos):
    """Atualiza o conteúdo da tabela (frame) com os dados fornecidos."""
    for widget in frame.winfo_children():
        widget.destroy()  # Limpa o frame

    # Adiciona os títulos
    for col_index, titulo in enumerate(titulos):
        ctk.CTkLabel(frame, text=titulo).grid(row=0, column=col_index, padx=5, pady=5)

    # Adiciona os dados
    for row_index, linha in enumerate(dados):
        for col_index, valor in enumerate(linha):
            ctk.CTkLabel(frame, text=valor).grid(row=row_index + 1, column=col_index, padx=5, pady=5)

def venda_cupom():
    """Função principal para a janela de venda de cupons."""
    # Criando a janela principal
    janela = ctk.CTkToplevel()
    janela.title("VENDA CUPOM")

    # Criando os frames das tabelas
    frame_cupons = criar_tabela_cupons(janela)
    frame_itens = criar_tabela_itens(janela)

    # Layout da interface
    ctk.CTkLabel(janela, text="CNPJ ", width=24).grid(row=0, column=0)
    ctk.CTkLabel(janela, text="Empresa ", width=39).grid(row=0, column=1)
    ctk.CTkLabel(janela, text="Cliente").grid(row=0, column=2)

    cnpj_entry = ctk.CTkEntry(janela, width=150)
    cnpj_entry.grid(row=1, column=0)
    
    empresa_entry = ctk.CTkEntry(janela, width=150)
    empresa_entry.grid(row=1, column=1)
    
    cliente_entry = ctk.CTkEntry(janela, width=150)
    cliente_entry.grid(row=1, column=2)

    ctk.CTkLabel(janela, text="Valor da Compra R$").grid(row=2, column=0)
    ctk.CTkLabel(janela, text="Data da Compra").grid(row=2, column=1)
    ctk.CTkLabel(janela, text="Operador").grid(row=2, column=2)
    ctk.CTkLabel(janela, text="N° Cupom").grid(row=2, column=3)

    valor_entry = ctk.CTkEntry(janela, width=70)
    valor_entry.grid(row=3, column=0)

    data_entry = ctk.CTkEntry(janela, width=100)
    data_entry.grid(row=3, column=1)

    usuario_entry = ctk.CTkEntry(janela, width=100)
    usuario_entry.grid(row=3, column=2)

    cupom_entry = ctk.CTkEntry(janela, width=50)
    cupom_entry.grid(row=3, column=3)

    # Botões
    ctk.CTkButton(janela, text="PESQUISAR", command=lambda: pesquisar_cupom(lista_dados, cupom_entry, valor_entry, data_entry, usuario_entry, cnpj_entry, empresa_entry)).grid(row=4, column=0)
    ctk.CTkButton(janela, text="IMPRIMIR", command=lambda: imprimir_cupom(cupom_entry.get(), valor_entry.get(), data_entry.get(), usuario_entry.get(), cnpj_entry.get(), empresa_entry.get())).grid(row=4, column=1)
    ctk.CTkButton(janela, text="SAIR", command=janela.destroy, fg_color='red').grid(row=4, column=2)

    # Adicionando as tabelas ao layout
    frame_cupons.grid(row=5, column=0, columnspan=4, sticky="nsew")
    frame_itens.grid(row=6, column=0, columnspan=4, sticky="nsew")

    # Configurando a grade para os frames
    janela.grid_rowconfigure(5, weight=1)
    janela.grid_rowconfigure(6, weight=1)

    # Populando a tabela de cupons
    for item in lista_dados:
        cupom, data, cliente, valor, usuario, cnpj, razao_social = item[0], item[1], item[3], formatar_valor(item[2]), item[6], item[4], item[5]
        pesquisa.append([cupom, data, cliente, valor])
        
    atualizar_tabela(frame_cupons, pesquisa, ["Cupom", "Data", "Cliente", "Valor R$"])

    # Loop principal da janela
    janela.mainloop()

def pesquisar_cupom(lista_dados, cupom_entry, valor_entry, data_entry, usuario_entry, cnpj_entry, empresa_entry):
    """Pesquisa o cupom na lista de dados e atualiza os campos da janela."""
    cupom = cupom_entry.get()
    if not cupom:
        ctk.CTkMessageBox.show_error('Cupom não localizado', title='ERRO')
        return

    try:
        cupom_int = int(cupom)
        d = False
        
        for dado in lista_dados:
            if dado[0] == cupom_int:
                d = dado
                
                # Atualiza os campos com as informações do cupom
                cupom_entry.delete(0, ctk.END)
                cupom_entry.insert(0, d[0])
                data_entry.delete(0, ctk.END)
                data_entry.insert(0, d[1])
                usuario_entry.delete(0, ctk.END)
                usuario_entry.insert(0, d[6])
                cnpj_entry.delete(0, ctk.END)
                cnpj_entry.insert(0, d[4])
                cliente_entry.delete(0, ctk.END)
                cliente_entry.insert(0, d[3])
                valor_entry.delete(0, ctk.END)
                valor_entry.insert(0, formatar_valor(d[2]))

                # Atualiza a lista de itens no cupom
                pesquisa_cupom.clear()
                lista_cupom = arquivar.lista_item_por_carrinho(cupom)
                for compra in lista_cupom:
                    pesquisa_cupom.append(compra[1:])

                atualizar_tabela(frame_itens, pesquisa_cupom, ["Item", "COD", "EAN", "Descrição do Produto", "QTD", "PUni R$", "Preço R$"])
                break

        if not d:
            ctk.CTkMessageBox.show_error('Cupom Não Localizado', title='ERRO')
            atualizar_tabela(frame_itens, [], ["Item", "COD", "EAN", "Descrição do Produto", "QTD", "PUni R$", "Preço R$"])

    except ValueError:
        ctk.CTkMessageBox.show_error('Cupom Inválido!', title='ERRO')

def imprimir_cupom(cupom, valor, data, usuario, cnpj, empresa):
    """Imprime os detalhes do cupom em PDF."""
    informacao = '\n'  # Composição da string formatada de dados de venda
    informacao += f"Razão Social: {empresa}\n"
    informacao += f"End: AV. Boa Vista n-1012 Santa Rosa/SP\n"
    informacao += f"CNPJ: {cnpj}  IE : 07.112.888/000-00\n\n"
    informacao += f"Data: {data}\n" 
    informacao += f"Cliente: {cupom}\n"               
    informacao += f"Operador: {usuario}\n"
    informacao += f"Cupom R$: {cupom}\n"
    informacao += f"Valor: {valor}"

    gerar_pdf = imprimir.create_pdf(informacao, pesquisa_cupom, "impressora.pdf")  # Chamada da função "PDF" com informação da venda e dados do cupom
    if gerar_pdf:
        ctk


# Chamada inicial da função, deve ser ajustada conforme necessário
venda_cupom()
