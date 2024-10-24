import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import customtkinter as ctk
from PIL import Image ,ImageTk



# Funções dos módulos
import modulo_pagar as pagar
#import modulo_remover as remover
import modulo_pesquisar as pesquisar
import modulo_cadastrar as cadastrar
#import modulo_limpar as limpar
import modulo_adicionar as adicionar
import modulo_visualizar_cupom as visualizar
import modulo_arquivar as arquivar
import testando_cpf



def sistema(usuario, data, empresa):
    carrinho = []
    cupom=1000
    cpf= ''
    num_item = 0
    valor_pagar = 0
    num_item = 0
    valor_pagar=0.0 
    cnpj = '45.333.0001/45'
    
    # ***INICIO DA FUNÇOES ***
    def nova_compra():
        nonlocal cupom, cpf
        count = arquivar.gerar_cupom()  # Verifica e atualiza o número do cupom
        count = int(count)
        cupom += count  # Atualiza o cupom com o valor gerado
        cpf = testando_cpf.cpf()
        
        # Atualiza a label e a entry
        label_titulo.configure(text="CAIXA ABERTO", font=("Arial", 25, 'bold'))  # Atualiza o texto da label 
        entry_cupom.delete(0, ctk.END)  # Limpa o campo de entrada do cupom
        entry_cupom.insert(0, str(cupom))  # Insere o valor atualizado do cupom

        # Debug opcional para verificar o CPF
        print(f"Cupom: {cupom}, CPF: {cpf}")

        return cupom, cpf
        
    def adicionar_item():
        nonlocal num_item, valor_pagar, cpf, cupom
        material = entry_cod.get()
        print( f'retorno de  cpf {cpf} e cupom{cupom}')
        if not cpf:
            messagebox.showerror("Erro", "Click em Novo, Nova Compra para inicia uma compra!")
            return

        if not material:
            messagebox.showerror("Erro", "Erro no campo material ou descrição!")
            return
        
        try:
            qtd = int(entry_qtd.get())
            if qtd < 1 or qtd > 99 or qtd is None:
                messagebox.showerror("Erro", "Erro no campo Quantidade!")
        except ValueError:
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

                # Atualizar os campos visuais (Entries)
                entry_descricao.delete(0, ctk.END)  # Limpa a entrada de descrição
                entry_descricao.insert(0, material)  # Atualiza com a descrição correta

                entry_pre_unit.delete(0, ctk.END)  # Limpa o campo de preço unitário
                entry_pre_unit.insert(0, f" {preco_unitario:.2f}")  # Atualiza o preço unitário

                entry_pre_comb.delete(0, ctk.END)  # Limpa o campo de preço combinado
                entry_pre_comb.insert(0, f" {preco:.2f}")  # Atualiza o preço combinado

                entry_pre_total.delete(0, ctk.END)  # Limpa o campo de valor total
                entry_pre_total.insert(0, f" {valor_pagar:.2f}")  # Atualiza o valor total

            # Limpar os campos após a adição
            entry_cod.delete(0, ctk.END)
            #entry_descricao.delete(0, ctk.END)
            entry_qtd.delete(0, ctk.END)
            entry_qtd.insert(0, "1")  # Definir a quantidade como 1 por padrão
                
    def pagar_items():
        try:
            nonlocal valor_pagar, carrinho, num_item

            if valor_pagar > 0:
                v_pago = f"{valor_pagar:.2f}"  # Valor pago formatado
                print(f'Retorno antes de pagar: {valor_pagar}')
                
                # Chama a função de pagamento e atualiza o valor
                valor_pagar = pagar.pagar(valor_pagar)
                print(f'Retorno da função pagar: {valor_pagar}')
                
                # Verifica se o pagamento foi concluído com sucesso
                if valor_pagar == 0:
                    # Arquiva os detalhes do pagamento
                    arquivar.arquivo(cupom, data, usuario, cnpj, cpf, v_pago, empresa, carrinho)

                    # Reseta o número de itens e limpa o carrinho
                    voltar()

                else:
                    # Caso ainda haja valor a pagar (ex.: pagamento parcial ou erro)
                    messagebox.showwarning("Pagamento Incompleto", f"Ainda resta um valor de R$ {valor_pagar:.2f} para ser pago.")
            
            else:
                messagebox.showerror("Erro", "Clique em 'Novo' e depois 'Nova Compra' para iniciar uma compra!")
                return

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar pagamento: {e}")

    def voltar():
        try:
            nonlocal valor_pagar, num_item, cupom, cpf, carrinho

            # Reseta os valores das variáveis
            valor_pagar = 0
            num_item = 0
            cupom = 1000
            cpf = ""
            carrinho.clear()
            # Limpa os campos de entrada e o carrinho
            limpar_campos()

            # Limpa a árvore de exibição dos itens do carrinho
            tree.delete(*tree.get_children())  # Remove todos os itens da Treeview

            # Atualiza a interface para indicar que a compra foi finalizada
            label_titulo.configure(text="CAIXA FECHADO", font=("Arial", 25, 'bold'))

            # Exibe uma mensagem de confirmação
            messagebox.showinfo("Compra Finalizada", "Venda concluída com sucesso!")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {e}")

    def limpar_campos():
        
        # Função para limpar os campos de entrada
        entry_descricao.delete(0, ctk.END)
        entry_pre_unit.delete(0, ctk.END)
        entry_pre_comb.delete(0, ctk.END)
        entry_pre_total.delete(0, ctk.END)
        entry_cod.delete(0, ctk.END)
        entry_cupom.delete(0, ctk.END)


    def nova_pesquisa():
        ean,material=pesquisar.pesquisar(dic)
        entry_cod.insert(0, ean)
        entry_descricao.insert(0, material)

    def novo_item():
        if usuario == "Administrador":
            cadastrar.novo_item()
            atualizar_dic()
        else:
            messagebox.showerror("Erro", "Seu usuário não tem permissão para cadastrar item!")

    def venda_cupom():
        lista_dados = arquivar.lista_de_vendas()
        print(lista_dados)
        visualizar.venda_por_cupom(lista_dados)

    def mostrar_ajuda():
        try:
            with open('ajuda.txt', 'r') as legenda:
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
    
    def sair(janela_principal):
    # Exibe uma caixa de diálogo de "Sim" ou "Não"
        resposta = messagebox.askyesno("Encerrar", "Deseja encerrar o programa?")
        
        # Se a resposta for "Sim", fecha a janela principal
        if resposta:
            janela_principal.destroy()  # Certifique-se de que está chamando a função corretamente com parênteses
        else:
            return  # Caso contrário, não faz nada
    # Inicializa o dicionário de produtos

    # ===================================== Inicio da Interface Grafica=========================================
    
    janela_princupal = ctk.CTk()
    janela_princupal.title("ENTRADA E PEDIDO")
    janela_princupal.geometry("1280x700")

    # Configuração inicial do tema visual da interface
    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("dark-blue")  # Tema de cores azul-escuru

    # Menu
    menu_bar = tk.Menu(janela_princupal)
    menu_novo = tk.Menu(menu_bar, tearoff=0)
    
    menu_novo.add_command(label="Nova Compra", command=lambda: nova_compra())
    menu_novo.add_command(label="Nova Pesquisa", command=lambda: nova_pesquisa())
    menu_novo.add_command(label="Novo Item", command=lambda: novo_item())
    menu_bar.add_cascade(label="  Novo  ", menu=menu_novo)

    menu_totais = tk.Menu(menu_bar, tearoff=0)
    menu_totais.add_command(label="Venda Cupom", command=lambda: venda_cupom())
    menu_bar.add_cascade(label=" Totais ", menu=menu_totais)

    menu_suporte = tk.Menu(menu_bar, tearoff=0)
    menu_suporte.add_command(label="Ajuda", command=lambda: mostrar_ajuda())
    menu_bar.add_cascade(label=" Suporte ", menu=menu_suporte)

    menu_fechar = tk.Menu(menu_bar, tearoff=0)
    menu_fechar.add_command(label="Fechar", command=lambda: sair(janela_princupal))
    menu_bar.add_cascade(label=" Fechar ", menu=menu_fechar)

    janela_princupal.config(menu=menu_bar)
    
    # Cupom
    label_titulo = ctk.CTkLabel(janela_princupal, text="CAIXA FECHADO", font=("Arial",24,'bold'))
    label_titulo.pack(pady=(10,0),padx=10)
    frame_cupon = ctk.CTkFrame(janela_princupal)
    frame_cupon.pack(pady= 0, padx=(1200,0))
    
    label_cupom = ctk.CTkLabel(frame_cupon, text="Cupom N°:",font=('Arial',20,'bold'))
    label_cupom.grid(row=0, column=0, padx=30, pady=0)
    entry_cupom = ctk.CTkEntry(frame_cupon, font=("Arial", 18),width=145,justify= "right")
    entry_cupom.grid(row=0, column=1, padx=0, pady=0)
    
    
    
    
    #frame principal
    frame_master = ctk.CTkFrame(janela_princupal)
    frame_master.pack(padx=10, pady=10)
    
    #frame la esquerdo
    frame_esquerda = ctk.CTkFrame(frame_master)
    frame_esquerda.grid(row=0, column=0, padx=0, pady=0 )

    # Carregar a imagem usando PIL (precisa da biblioteca Pillow)
    image_baner = "tdt.png"
    image = ctk.CTkImage(dark_image=Image.open(image_baner), size=(500, 305))

   # Carregar a imagem do botão "P"
    imagem_p = Image.open("buscar.png")
    imagem_p_resized = imagem_p.resize((35, 35))  # Ajustar o tamanho da imagem conforme necessário
    imagem_p_ctk = ImageTk.PhotoImage(imagem_p_resized )

    # Criar um rótulo (Label) para exibir a imagem
    label = ctk.CTkLabel(frame_esquerda, image=image, text="")  # Definir text como vazio para mostrar apenas a imagem
    label.pack(pady=(18,20))
    
    # Informações do Produto
    frame_inputs = ctk.CTkFrame(frame_esquerda) 
    frame_inputs.pack(pady=0, padx=0)
    
    # declaração de labels de imputs
    frame_inputs_label = ctk.CTkFrame(frame_inputs,width=200,fg_color="transparent")
    frame_inputs_label.grid(row=0, column=0, padx=(0,0), pady=0, sticky="e")

    #declaração de entryes de imputs
    frame_inputs_entry1 = ctk.CTkFrame(frame_inputs,fg_color="transparent")
    frame_inputs_entry1.grid(row=1, column=0, padx=(0,100), pady=0, sticky="w")

    frame_inputs_entry2 = ctk.CTkFrame(frame_inputs,fg_color="transparent")
    frame_inputs_entry2.grid(row=1, column=0, padx=(0,0), pady=0, sticky="e")
    
    # inputs
    label_cod = ctk.CTkLabel(frame_inputs_label, text="Código do Produto",width=100)
    entry_cod = ctk.CTkEntry(frame_inputs_entry1, font=("Arial", 25),width=200)
    label_qtd = ctk.CTkLabel(frame_inputs_label, text="Qtd",width=30) 
    entry_qtd = ctk.CTkEntry(frame_inputs_entry2, font=("Arial", 25), width=60)
    
    entry_qtd.insert(0, "1")  # Definindo o valor padrão como 1
    label_descricao = ctk.CTkLabel(frame_inputs, text="Descrição do Produto")  
    entry_descricao = ctk.CTkEntry(frame_inputs, font=("Arial", 25),width=500)
    
    button_pesquisar = ctk.CTkButton(frame_inputs_entry1, image=imagem_p_ctk,text="", command=lambda: nova_pesquisa(),width=30,height=35,fg_color="#fff",border_color='black',border_width=1)
    
    #posicionamento de imputs
    label_cod.grid(row=0, column=0, padx=(0,200), pady=(10,0),sticky='w')
    entry_cod.grid(row=1, column=0, padx=(0,0), pady=0)
    label_qtd.grid(row=0, column=1, padx=(165,0), pady=(10,0),sticky='e')
    entry_qtd.grid(row=1, column=2, padx=(0,0), pady=0)
    label_descricao.grid(row=2, column=0, padx=(0,0), pady=(30,0),sticky='w')
    entry_descricao.grid(row=3, column=0, padx=(0,0), pady=0)
    
    button_pesquisar.grid(row=1, column=1, padx=(10,10), pady=0)

    # Botões
    frame_butons = ctk.CTkFrame(frame_esquerda )
    frame_butons.pack(pady=(15,0), padx= 0)

    button_adicionar = ctk.CTkButton(frame_butons, text="ADICIONAR",font=('Ariel',16,'bold'),height=40, command=lambda: adicionar_item())
    button_deletar = ctk.CTkButton(frame_butons, text="DELETE",font=('Ariel',16,'bold'), height=40, command=lambda: deletar_item())
    button_pagar = ctk.CTkButton(frame_butons, text="PAGAR",font=('Ariel',16,'bold'), height=40, command=lambda: pagar_items())
    button_voltar = ctk.CTkButton(frame_butons, text="VOLTAR", font=('Ariel',16,'bold'),height=40, command=lambda: voltar())
    
    # posicionamento de 4 botões
    button_adicionar.grid(row=0, column=0, padx=(0,110), pady=(15,15))
    button_deletar.grid(row=0, column=1, padx=(108,0), pady=(15,15))
    button_pagar.grid(row=1, column=0, padx= (0,110), pady=(15,0))
    button_voltar.grid(row=1, column=1, padx=(108,0), pady=(15,0))

    # ***COMPONENTES DO FRAME DA DIREITA*** 
    frame_direita = ctk.CTkFrame(frame_master)
    frame_direita.grid(row=0, column=1, padx=0, pady=0)
    
    # Estilo da tabela Treeview
    style = ttk.Style()

    # Configurando o estilo do heading da Treeview
    style.configure("Treeview.Heading", font=("Arial", 14,))  # Aumenta o tamanho da fonte do cabeçalho
    style.configure("Treeview", font=("Arial", 16))  # Configura a fonte dos valores
    
    # Colunas da Tabela
    columns = ["Item", "Cod", "EAN", "Descrição", "Qtd", "PUni R$", "Preço R$"]
    tree = ttk.Treeview(frame_direita, columns=columns, show="headings", height=27)
    
    # Definindo os cabeçalhos e as larguras das colunas
    tree.heading("Item", text="Item",)
    tree.column("Item", anchor=tk.CENTER, width=50)  # Definindo largura para coluna "Item"

    tree.heading("Cod", text="Cod")
    tree.column("Cod", anchor=tk.CENTER, width=100)  # Definindo largura para coluna "Cod"

    tree.heading("EAN", text="EAN")
    tree.column("EAN", anchor=tk.CENTER, width=200)  # Definindo largura para coluna "EAN"

    tree.heading("Descrição", text="Descrição")
    tree.column("Descrição", anchor=tk.CENTER, width=500)  # Definindo largura para coluna "Descrição"

    tree.heading("Qtd", text="Qtd")
    tree.column("Qtd", anchor=tk.CENTER, width=80)  # Definindo largura para coluna "Qtd"

    tree.heading("PUni R$", text="PUni R$")
    tree.column("PUni R$", anchor=tk.CENTER, width=150)  # Definindo largura para coluna "PUni R$"

    tree.heading("Preço R$", text="Preço R$")
    tree.column("Preço R$", anchor=tk.CENTER, width=150)  # Definindo largura para coluna "Preço R$"

    #podicionamneto da janela_princupal
    tree.pack(fill=ctk.BOTH, expand=True,padx=(20,0),pady=20)

    # Valore unitario e totais
    frame_valores= ctk.CTkFrame(frame_direita)
    frame_valores.pack(pady=0, padx=0)

    label_pre_unit = ctk.CTkLabel(frame_valores, text="Preço Unitario R$: ")
    entry_pre_unit = ctk.CTkEntry(frame_valores, font=("Arial", 40),width=270,justify='right')
    label_pre_comb = ctk.CTkLabel(frame_valores, text="Preço Combinado R$:")
    entry_pre_comb = ctk.CTkEntry(frame_valores, font=("Arial", 40),width=300,justify='right')
    label_pre_total = ctk.CTkLabel(frame_valores, text="Valor Total R$:")
    entry_pre_total = ctk.CTkEntry(frame_valores, font=("Arial", 40),width=300,justify='right')
    
    #posicionamento
    label_pre_unit.grid(row=0, column=0, padx=(15,350), pady=1)
    entry_pre_unit.grid(row=1, column=0, padx=(15,190), pady=1)
    label_pre_comb.grid(row=0, column=1, padx=(395,0), pady=1)
    entry_pre_comb.grid(row=1, column=1, padx=(225,0), pady=1)
    label_pre_total.grid(row=2, column=1, padx=(440,0), pady=1)
    entry_pre_total.grid(row=3, column=1, padx=(225,0), pady=1)

    # labels de usuario s e datas
    frame_userdates= ctk.CTkFrame(janela_princupal)
    frame_userdates.pack(pady=0, padx=1)

    usuario_label = ctk.CTkLabel(frame_userdates, text=f"Operador: {usuario}", font=("Any", 14))
    data_label = ctk.CTkLabel(frame_userdates, text=f"Data: {data}", font=("Any", 14))

    usuario_label.grid(row=0, column=0, padx=100, pady=0)
    data_label.grid(row=0, column=1, padx=100, pady=0)

   
   
    dic={}

    atualizar_dic()

    janela_princupal.mainloop()

# Teste da função
#usuario, data, empresa = "Administrador", '2024-03-21 17:00', "Tem De Tudo ME"
#sistema(usuario, data, empresa)




