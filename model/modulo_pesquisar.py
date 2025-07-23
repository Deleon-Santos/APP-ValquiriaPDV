import customtkinter as ctk
from tkinter import ttk, messagebox

# Inicializa a lista padrão e a lista de pesquisa
defaut = ['0', '0']
pesquisa = []

# Função para realizar a pesquisa no dicionário e exibir os resultados
def pesquisar(dic):
    # Função para capturar a seleção da linha e concluir a pesquisa
    def concluir():
        try:
            # Pega a linha selecionada
            linha_selecionada = tree.selection()[0]  # Pega a primeira linha selecionada
            escolha = tree.item(linha_selecionada, 'values')  # Valores da linha selecionada
            janela_pesquisa.destroy()
            return escolha[1], escolha[2]  # Retorna EAN e descrição do item
        except IndexError:
            messagebox.showwarning("Aviso", "Nenhum item selecionado!")
            janela_pesquisa.destroy()
            return defaut[0], defaut[1]  # Retorna os valores padrão

    # Janela principal
    janela_pesquisa = ctk.CTk()
    janela_pesquisa.title("PESQUISA POR ITEM")
    janela_pesquisa.geometry("826x420+696+142")  # Definindo o tamanho da janela_pesquisa
    janela_pesquisa.focus_force()
    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("database/themas.txt")  # Tema de cores azul-escuru  
    

     # Estilo para personalizar a Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # Configura a fonte dos cabeçalhos
    style.configure("Treeview", font=("Arial", 11))  # Configura a fonte dos valores

   

    # Frame para a tabela e botões
    frame = ctk.CTkFrame(janela_pesquisa)
    frame.pack(pady=(20,10), padx=10, fill="both", expand=True)

    # Títulos das colunas
    titulos = [" Cod ", "   EAN    ", "   Descrição do Produto   "]

    # Variável para a lista de pesquisa (pesquisa contém os dados da tabela)
    pesquisa.clear()
    for item in dic:
        cod = item['cod']
        ean = item['ean']
        desc = item['item']
        pesquisa.append([cod, ean, desc])

    # Criação da Tabela (Treeview) para exibir os dados
    tree = ttk.Treeview(frame, columns=titulos, show='headings', height=10)
    tree.pack(side="top", fill="both", expand=True)

    # Definir cabeçalhos e alinhar ao centro
    for i, titulo in enumerate(titulos):
        tree.heading(i, text=titulo)
        tree.column(i, anchor="center", width=200)

    # Inserir os dados da lista de pesquisa na tabela
    for linha in pesquisa:
        tree.insert("", "end", values=linha)

    # Botão "CONCLUIR" para finalizar a pesquisa
    btn_concluir = ctk.CTkButton(janela_pesquisa, text="CONCLUIR", command=janela_pesquisa.quit)  # Fecha a janela_pesquisa ao clicar
    btn_concluir.pack(pady=10)

    # Iniciar a janela_pesquisa e aguardar o comando

    janela_pesquisa.mainloop()
    
    return concluir()
    
    
    
    
