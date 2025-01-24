import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import customtkinter as ctk
from PIL import Image ,ImageTk
from datetime import datetime
import modulo_pagar as pagar
import modulo_pesquisar as pesquisar
import modulo_cadastrar as cadastrar
import modulo_adicionar as adicionar
import modulo_visualizar_cupom as visualizar
import modulo_arquivar as arquivar
import testando_cpf

# Entrada no sistema
def sistema(usuario, empresa):
    data=""
    carrinho = []
    cupom=1000 
    num_item = 0
    valor_pagar = 0
    cnpj = '45.333.0001/45'
    cpf= ''

    def nova_compra():
        nonlocal cupom, cpf
        count = arquivar.gerar_cupom()  # Verifica e atualiza o número do cupom
        cupom += cupom + int(count) 
        cpf = testando_cpf.cpf()
        
        label_titulo.configure(text="CAIXA ABERTO", font=("Arial", 30, 'bold'))  # Atualiza o texto da label 
        entry_cupom.delete(0, ctk.END)  
        entry_cupom.insert(0, str(cupom))  # Insere o valor atualizado do cupom
        return cupom, cpf
        
    def adicionar_item():
        nonlocal num_item, valor_pagar, cpf, cupom, dic
       
        # Validação e tratamento dos erros
        material = entry_cod.get()
        try:
            qtd = int(entry_qtd.get())
            if qtd < 1 or qtd > 99 or qtd is None:
                messagebox.showerror("Erro", "Erro no campo Quantidade!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Erro no campo Quantidade!")
            return   
        if not cpf:
            messagebox.showerror("Erro", "Click em Novo, Nova Compra para inicia uma compra!")
            return
        if not material:
            messagebox.showerror("Erro", "Erro no campo material ou descrição!")
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
                str_preco = f"{preco:.2f}"
                valor_pagar += preco
                produto = [num_item, plu_pro, ean, material, qtd, preco_unitario, str_preco]
                carrinho.append(produto)
                tree.insert("", "end", values=produto)

                # Atualizar os campos visuais (Entries)
                entry_descricao.delete(0, ctk.END)  
                entry_descricao.insert(0, material)  
                entry_pre_unit.delete(0, ctk.END)  
                entry_pre_unit.insert(0, f" {preco_unitario:.2f}") 
                entry_pre_comb.delete(0, ctk.END)  
                entry_pre_comb.insert(0, f" {preco:.2f}") 
                entry_pre_total.delete(0, ctk.END) 
                entry_pre_total.insert(0, f" {valor_pagar:.2f}")  

            # Limpar os campos após a adição
            entry_cod.delete(0, ctk.END)
            entry_qtd.delete(0, ctk.END)
            entry_qtd.insert(0, "1")  

    def deletar():
        nonlocal valor_pagar, carrinho, num_item
        try:
            # Pega a linha selecionada
            linha_selecionada = tree.selection()[0]  
            escolha = tree.item(linha_selecionada, 'values')  # Valores da linha selecionada
            novo_valor_pagar = float(escolha[6])
            valor_pagar -= novo_valor_pagar

            # Incrementa o contador de itens
            num_item += 1
            escolha = list(escolha)  # Transforma a tupla em lista para manipulação
            escolha[0] = num_item  # Define o número do item
            escolha[6] = f'-{novo_valor_pagar:.2f}'  # Atualiza o valor do item selecionado como negativo
            carrinho.append(escolha)
            
            # Atualiza a árvore com o novo item
            tree.insert("", "end", values=escolha)
            entry_pre_total.delete(0, ctk.END)
            entry_pre_total.insert(0,f" {valor_pagar:.2f}")

            return valor_pagar , num_item  # Retorna EAN e item
        except IndexError:
            messagebox.showwarning("Aviso", "Nenhum item selecionado!")
            return
                       
    def pagar_items():
        try:
            nonlocal valor_pagar, carrinho, data

            if valor_pagar > 0:
                v_pago = f"{valor_pagar:.2f}"  # Valor pago formatado
                print(f'Retorno antes de pagar: {valor_pagar}')
                               
                valor_pagar = pagar.pagar(valor_pagar)# Chama a função de pagamento e atualiza o valor
                print(f'Retorno da função pagar: {valor_pagar}')
                
                if valor_pagar == 0:# Verifica se o pagamento foi concluído com sucesso
                    arquivar.arquivo(cupom, data, usuario, cnpj, cpf, v_pago, empresa, carrinho)

                    voltar() # limpa os campos com valores residuais

                else:
                    messagebox.showwarning("Pagamento Incompleto", f"Ainda resta um valor de R$ {valor_pagar:.2f} para ser pago.")
            else:
                messagebox.showerror("Erro", "Clique em 'Novo' e depois 'Nova Compra' para iniciar uma compra!")
                return

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar pagamento: {e}")

    def voltar():
        try:
            nonlocal valor_pagar, num_item, cupom, cpf, carrinho
            valor_pagar= 0,0
            num_item = 0
            cupom = 1000
            cpf = ""
            carrinho.clear()    
            limpar_campos()#Limpa os campos de entrada e o carrinho

            tree.delete(*tree.get_children())  # Remove todos os itens da Treeview
            label_titulo.configure(text="CAIXA FECHADO", font=("Arial", 30, 'bold'))
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
        ean, material=pesquisar.pesquisar(dic)
        if ean !='0' and material !='0':
        
            entry_cod.delete(0, ctk.END)
            entry_cod.insert(0, ean)
            entry_descricao.delete(0, ctk.END)
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
            with open('dependencias/ajuda.txt', 'r') as legenda:
                arquivo = legenda.read()
                messagebox.showinfo("Ajuda", arquivo)
        except FileNotFoundError:
            messagebox.showerror("Erro", "O arquivo 'SUPORTE' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")

    def atualizar_dic():
        nonlocal dic
        try:
            with open('dependencias/bd_itens.txt', 'r') as adic:
                dic = json.load(adic)
        except FileNotFoundError:
            messagebox.showerror("Erro", "O arquivo 'bd.txt' não foi encontrado!")
    
    def atualizar_data():
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data_label.configure(text=f"Data: {data_atual}")
        janela_principal.after(1000, atualizar_data)

    def sair(janela_principal):
        resposta = messagebox.askyesno("Encerrar", "Deseja encerrar o programa?")
        
        if resposta:
            janela_principal.destroy()  # Certifique-se de que está chamando a função corretamente com parênteses
        else:
            return  # Caso contrário, não faz nada
    

    ############################################ Inicio da Interface Grafica ##########################################
    
    janela_principal = ctk.CTk()
    janela_principal.title("ENTRADA E PEDIDO")
    janela_principal.geometry("1280x700")
    janela_principal.iconbitmap("dependencias/img5.ico")
    # Configuração inicial do tema visual da interface
    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("themas.txt")  # Tema de cores azul-escuru

    # opções de menu
    menu_bar = tk.Menu(janela_principal)

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
    menu_fechar.add_command(label="Fechar", command=lambda: sair(janela_principal))
    menu_bar.add_cascade(label=" Fechar ", menu=menu_fechar) 
    janela_principal.config(menu=menu_bar)# posicionamento do menu
    
    # Cupom
    frame_topo = ctk.CTkFrame(janela_principal)
    frame_topo.pack(fill="x",padx=40,pady=(10,0))  # Expande o frame para toda a largura da janela

    # Label do título centralizado
    label_titulo = ctk.CTkLabel(frame_topo, text="CAIXA FECHADO", font=("Arial", 30, 'bold'))
    label_titulo.grid(row=0, column=0, padx=(10,500), pady=5)
    frame_topo.grid_columnconfigure(0, weight=1)  # Centraliza o título ao expandir a coluna

    # Frame do cupom alinhado à direita
    frame_cupon = ctk.CTkFrame(frame_topo,fg_color='transparent')
    frame_cupon.grid(row=0, column=1, padx=(0,30), sticky="e")  # 'sticky="e"' alinha à direita

    # Label e Entry do cupom
    label_cupom = ctk.CTkLabel(frame_cupon, text="Cupom N°:", font=('Arial', 30, 'bold'))
    label_cupom.grid(row=0, column=0, padx=(0,20), pady=0)

    entry_cupom = ctk.CTkEntry(frame_cupon, font=("Arial", 20), width=145, height=30, justify="right")
    entry_cupom.grid(row=0, column=1, padx=(0,20), pady=0)
    # Frame principal
    frame_master = ctk.CTkFrame(janela_principal)
    frame_master.pack(fill="x",padx=40, pady=(10,5))
    
    # Frame la esquerdo
    frame_esquerda = ctk.CTkFrame(frame_master,fg_color='transparent')
    frame_esquerda.grid(row=0, column=0, padx=(30,15), pady=(0,20) )

    image_baner = "dependencias/banner.png" # Carregar a imagem usando PIL (precisa da biblioteca Pillow)
    image = ctk.CTkImage(dark_image=Image.open(image_baner), size=(500, 255))
    label = ctk.CTkLabel(frame_esquerda, image=image, text="")  # Definir text como vazio para mostrar apenas a imagem
    label.pack(pady=(18,20))

    imagem_p = Image.open("dependencias/buscar.png")# Carregar a imagem do botão "P"
    imagem_p_resized = imagem_p.resize((35, 35))  # Ajustar o tamanho da imagem conforme necessário
    imagem_p_ctk = ImageTk.PhotoImage(imagem_p_resized )
     
    # Informações do Produto
    frame_inputs = ctk.CTkFrame(frame_esquerda) 
    frame_inputs.pack(pady=0, padx=0)
    
    # Declaração de labels de imputs
    frame_inputs_label = ctk.CTkFrame(frame_inputs,width=200,fg_color="transparent")
    frame_inputs_label.grid(row=0, column=0, padx=(0,0), pady=0, sticky="e")
    frame_inputs_entry1 = ctk.CTkFrame(frame_inputs,fg_color="transparent")
    frame_inputs_entry1.grid(row=1, column=0, padx=(0,100), pady=0, sticky="w")
    frame_inputs_entry2 = ctk.CTkFrame(frame_inputs,fg_color="transparent")
    frame_inputs_entry2.grid(row=1, column=0, padx=(0,0), pady=0, sticky="e")
    
    # Inputs e Label's
    label_cod = ctk.CTkLabel(frame_inputs_label, text="Código do Produto",width=100)
    entry_cod = ctk.CTkEntry(frame_inputs_entry1, font=("Arial", 25),width=200,height=50)
    label_qtd = ctk.CTkLabel(frame_inputs_label, text="Qtd",width=30) 
    entry_qtd = ctk.CTkEntry(frame_inputs_entry2, font=("Arial", 25), width=60,height=50) 
    
    entry_qtd.insert(0, "1")  # Definindo o valor padrão como 1
    
    label_descricao = ctk.CTkLabel(frame_inputs, text="Descrição do Produto")  
    entry_descricao = ctk.CTkEntry(frame_inputs, font=("Arial", 25),width=500,height=50)
     
    # Posicionamento de imputs
    label_cod.grid(row=0, column=0, padx=(0,200), pady=(10,0),sticky='w')
    entry_cod.grid(row=1, column=0, padx=(0,0), pady=0)
    label_qtd.grid(row=0, column=1, padx=(165,0), pady=(10,0),sticky='e')
    entry_qtd.grid(row=1, column=2, padx=(0,0), pady=0)
    label_descricao.grid(row=2, column=0, padx=(0,0), pady=(30,0),sticky='w')
    entry_descricao.grid(row=3, column=0, padx=(0,0), pady=0)
    
    button_pesquisar = ctk.CTkButton(frame_inputs_entry1, image=imagem_p_ctk,text="", command=lambda: nova_pesquisa(),width=30,height=50,fg_color="#fff",border_color='black',border_width=1,)   
    button_pesquisar.grid(row=1, column=1, padx=(10,10), pady=0)

    # Botões
    frame_butons = ctk.CTkFrame(frame_esquerda )
    frame_butons.pack(pady=(15,0), padx= 0)

    button_adicionar = ctk.CTkButton(frame_butons, text="ADICIONAR",font=('Ariel',16,'bold'),height=50, command=lambda: adicionar_item())
    button_deletar = ctk.CTkButton(frame_butons, text="DELETE",font=('Ariel',16,'bold'), height=50, command=lambda: deletar())
    button_pagar = ctk.CTkButton(frame_butons, text="PAGAR",font=('Ariel',16,'bold'), height=50, command=lambda: pagar_items())
    button_voltar = ctk.CTkButton(frame_butons, text="VOLTAR", font=('Ariel',16,'bold'),height=50, command=lambda: voltar())
    
    # Posicionamento de 4 botões
    button_adicionar.grid(row=0, column=0, padx=(0,110), pady=(15,15))
    button_deletar.grid(row=0, column=1, padx=(108,0), pady=(15,15))
    button_pagar.grid(row=1, column=0, padx= (0,110), pady=(15,0))
    button_voltar.grid(row=1, column=1, padx=(108,0), pady=(15,0))
    janela_principal.bind_all("<Control-a>", lambda event: adicionar_item())
    janela_principal.bind_all("<Control-d>", lambda event: deletar())
    janela_principal.bind_all("<Control-p>", lambda event: pagar_items())
    janela_principal.bind_all("<Control-v>", lambda event: voltar())
    janela_principal.bind_all("<Control-b>",lambda event: nova_pesquisa())
    janela_principal.bind_all("<F1>", lambda event: nova_compra())
    janela_principal.bind_all("<F2>",lambda event: nova_pesquisa())
    janela_principal.bind_all("<F3>",lambda event: novo_item())
    janela_principal.bind_all("<F4>",lambda event: sair(janela_principal))
    janela_principal.bind_all("<F5>",lambda event: venda_cupom())
    
    # Componentes do frame direito
    frame_direita = ctk.CTkFrame(frame_master,fg_color="transparent")
    frame_direita.grid(row=0, column=1, padx=(15,30), pady=(0,20))
    
    style = ttk.Style()# Estilo da tabela Treeview
    style.configure("Treeview.Heading", font=("Arial", 14,))  # Aumenta o tamanho da fonte do cabeçalho
    style.configure("Treeview", font=("Arial", 16))  # Configura a fonte dos valores
    
    # Colunas da Tabela
    columns = ["Item", "Cod", "EAN", "Descrição", "Qtd", "PUni R$", "Preço R$"]
    tree = ttk.Treeview(frame_direita, columns=columns, show="headings", height=27)
    
    # Definindo os cabeçalhos e as larguras das colunas
    tree.heading("Item", text="Item",)
    tree.column("Item", anchor=tk.CENTER, width=50)  
    tree.heading("Cod", text="Cod")
    tree.column("Cod", anchor=tk.CENTER, width=80) 
    tree.heading("EAN", text="EAN")
    tree.column("EAN", anchor=tk.CENTER, width=200)  
    tree.heading("Descrição", text="Descrição")
    tree.column("Descrição", anchor=tk.CENTER, width=450)  
    tree.heading("Qtd", text="Qtd")
    tree.column("Qtd", anchor=tk.CENTER, width=50) 
    tree.heading("PUni R$", text="PUni R$")
    tree.column("PUni R$", anchor=tk.CENTER, width=100)  
    tree.heading("Preço R$", text="Preço R$")
    tree.column("Preço R$", anchor=tk.CENTER, width=100)  

    # Podicionamneto da janela_principal
    tree.pack(fill=ctk.BOTH, expand=True,padx=(20,20),pady=20)

    # Valore unitario e totais
    frame_valores= ctk.CTkFrame(frame_direita)
    frame_valores.pack(fill="x", expand=True)

    label_pre_unit = ctk.CTkLabel(frame_valores, text="Preço Unitario R$: ")
    entry_pre_unit = ctk.CTkEntry(frame_valores, font=("Arial", 40),width=270,justify='right',fg_color='#FFFFE0')
    label_pre_comb = ctk.CTkLabel(frame_valores, text="Preço Combinado R$:")
    entry_pre_comb = ctk.CTkEntry(frame_valores, font=("Arial", 40),width=300,justify='right',fg_color='#FFFFE0')
    label_pre_total = ctk.CTkLabel(frame_valores, text="Valor Total R$:")
    entry_pre_total = ctk.CTkEntry(frame_valores, font=("Arial", 40),width=300,justify='right',fg_color='#FFFFE0')
    
    # Posicionamento
    label_pre_unit.grid(row=0, column=0,  pady=1,padx=(15,420),sticky="w")
    entry_pre_unit.grid(row=1, column=0, pady=1,padx=(15,0),sticky="w")
    label_pre_comb.grid(row=0, column=1,  pady=1,sticky="e")
    entry_pre_comb.grid(row=1, column=1,  pady=1,sticky="e")
    label_pre_total.grid(row=2, column=1,  pady=1,sticky="e")
    entry_pre_total.grid(row=3, column=1, pady=1,sticky="e")

    # Labels de usuarios e datas
    frame_userdates= ctk.CTkFrame(frame_valores,fg_color='transparent')
    frame_userdates.grid(row=3, column=0,pady=0, padx=15,sticky="w")

    usuario_label = ctk.CTkLabel(frame_userdates, text=f"Operador: {usuario}", font=("Any", 14,"bold"))
    data_label = ctk.CTkLabel(frame_userdates, text=f"Data: {data}", font=("Any", 14,"bold"))
    usuario_label.grid(row=0, column=0, padx=(0,100), pady=(20,0))
    data_label.grid(row=0, column=1, padx=(0,50), pady=(20,0))

    dic={}
    data=atualizar_data()
    atualizar_dic()

    janela_principal.mainloop()

#usuario, data, empresa = "Administrador", '2024-03-21 17:00', "Tem De Tudo ME"
#sistema(usuario, data, empresa)
    """entry_cod.configure(state="normal")  # Habilita a entrada temporariamente
    entry_cod.delete(0, "end")           # Limpa o conteúdo atual
    entry_cod.insert(0, novo_texto)      # Insere o novo conteúdo
    entry_cod.configure(state="readonly")  # Define novamente como somente leitura
"""