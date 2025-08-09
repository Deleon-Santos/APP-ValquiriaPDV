import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime

import model.modulo_pagar as pagar
import model.modulo_pesquisar as pesquisar
import model.modulo_cadastrar as cadastrar
import model.modulo_visualizar_cupom as visualizar
import model.modulo_arquivar as arquivar
import model.modulo_validar_cpf as teste

# Entrada no sistema
def sistema(usuario, empresa):
    data = ""
    carrinho = []
    cupom = 0
    num_item = 0
    valor_pagar = 0
    cnpj = '45.333.0001/45'
    cpf = ''

    def nova_compra():
        nonlocal cupom, cpf
        count = arquivar.gerar_cupom(cupom)  # Verifica e atualiza o número do cupom
        cupom = count
        cpf = teste.cpf()
        if len(cpf) != 14: 
            return
        label_titulo.configure(text="CAIXA ABERTO", font=(
            "Arial", 30, 'bold'))  # Atualiza o texto da label
        entry_cupom.configure(state='normal')
        entry_cupom.delete(0, ctk.END)
        entry_cupom.insert(0, str(cupom))  # Insere o valor atualizado do cupom
        entry_cupom.configure(state='readonly')
        
        return cupom, cpf

    def adicionar_item():
        nonlocal num_item, valor_pagar, cpf, cupom, dic

        # Validação e tratamento dos erros
        entrada = entry_cod.get().replace(' ', '')
        try:
            qtd = int(entry_qtd.get())
            if qtd < 1 or qtd > 99 or qtd is None:
                messagebox.showerror("Erro", "Erro no campo Quantidade!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Erro no campo Quantidade!")
            return
        if not cpf:
            messagebox.showerror(
                "Erro", "Click em Novo, Nova Compra para inicia uma compra!")
            return
        if not entrada:
            messagebox.showerror(
                "Erro", "Erro no campo material ou descrição!")
            return
        
        plu, ean, descricao_produto, preco_unitario = arquivar.validar_plu(entrada)  
        if plu:      
            num_item += 1
                    
            preco = preco_unitario * qtd
            valor_pagar += preco
            str_preco = f"{preco:.2f}"
            
            produto = [num_item, plu, ean, descricao_produto, qtd, preco_unitario, str_preco]
                        
            carrinho.append(produto)
            linha1 = [f"{str(produto[0]).zfill(3)} ",f"  {produto[3]}", f"{produto[5]}  ", f"{produto[6]}  "]
            linha2 = ["",f"  {produto[2]}", f"{'x'+str(produto[4])}  ",""]

            tree.insert("", "end", values=linha1)
            tree.insert("", "end", values=linha2)

            # Atualizar os campos visuais (Entries)
            entry_descricao.configure(state='normal')
            entry_descricao.delete(0, ctk.END)
            entry_descricao.insert(0, descricao_produto)
            entry_descricao.configure(state='readonly')

            entry_pre_unit.configure(state='normal')
            entry_pre_unit.delete(0, ctk.END)
            entry_pre_unit.insert(0, f" {preco_unitario:.2f}")
            entry_pre_unit.configure(state='readonly')

            entry_pre_comb.configure(state='normal')
            entry_pre_comb.delete(0, ctk.END)
            entry_pre_comb.insert(0, f" {preco:.2f}")
            entry_pre_comb.configure(state='readonly')

            entry_pre_total.configure(state='normal')
            entry_pre_total.delete(0, ctk.END)
            entry_pre_total.insert(0, f" {valor_pagar:.2f}")
            entry_pre_total.configure(state='readonly')

            entry_cod.delete(0, ctk.END)
            entry_qtd.delete(0, ctk.END)
            entry_qtd.insert(0, "1")
        else:
            messagebox.showerror("Erro", "Produto não encontrado ou inválido!")
            
    def deletar():
        nonlocal valor_pagar, carrinho, num_item
        try:
            linha_selecionada = tree.selection()[0]
            if linha_selecionada is not None:
                escolha = tree.item(linha_selecionada, 'values')
                id= escolha[0]
                novo_valor_pagar = float(escolha[3])
                valor_pagar -= novo_valor_pagar

                num_item += 1
                item_deletado = [num_item, "", f"{str(id).zfill(3)}: Removido",  f"{escolha[1]}".strip(" "), "", escolha[2], f'-{novo_valor_pagar:.2f}']
                
                carrinho.append(item_deletado) 
                linha_escolha = [f"{str(item_deletado[0]).zfill(3)} ", f"  {item_deletado[3]}", f"{item_deletado[5]}", f"{item_deletado[6]}  "]
                linha_escolha2 = ["",f"  {str(id).zfill(4)}: Removido", "", ""]
                # Atualiza a árvore com o novo item
                tree.insert("", "end", values=linha_escolha)
                tree.insert("", "end", values=linha_escolha2)
                entry_pre_total.configure(state='normal')
                entry_pre_total.delete(0, ctk.END)
                entry_pre_total.insert(0, f" {valor_pagar:.2f}")
                entry_pre_total.configure(state='readonly')

                return valor_pagar, num_item  # Retorna EAN e item
            else:
                messagebox.showwarning("Aviso", "Nenhum item selecionado!")
        except IndexError:
            messagebox.showwarning("Aviso", "Nenhum item selecionado!")
            return

    def pagar_items():
        try:
            nonlocal valor_pagar, carrinho, usuario
            data = atualizar_data()
            print(data, usuario)
            if valor_pagar > 0:
                v_pago = f"{valor_pagar:.2f}"  # Valor pago formatado
                print(f'Retorno antes de pagar: {valor_pagar}')

                # Chama a função de pagamento e atualiza o valor
                valor_pagar = pagar.pagar(valor_pagar)
                print(f'Retorno da função pagar: {valor_pagar}')

                if valor_pagar == 0:  # Verifica se o pagamento foi concluído com sucesso
                    arquivar.arquivo(cupom, data, usuario, cnpj,
                                     cpf, v_pago, empresa, carrinho)
                    voltar()  # limpa os campos com valores residuais

                else:
                    messagebox.showwarning(
                        "Pagamento Incompleto", f"Ainda resta um valor de R$ {valor_pagar:.2f} para ser pago.")
            else:
                messagebox.showerror(
                    "Erro", " iniciar uma compra!")
                return

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar pagamento: {e}")

    def voltar():
        try:
            nonlocal valor_pagar, num_item, cupom, cpf, carrinho
            valor_pagar = 0
            num_item = 0
            cupom = 0
            cpf = ""
            carrinho.clear()
            limpar_campos()  # Limpa os campos de entrada e o carrinho

            # Remove todos os itens da Treeview
            tree.delete(*tree.get_children())
            label_titulo.configure(text="CAIXA FECHADO",
                                   font=("Arial", 30, 'bold'))
            messagebox.showinfo("Compra Finalizada",
                                "Venda concluída com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar venda: {e}")

    def limpar_campos():
        # Função para limpar os campos de entrada
        entry_descricao.configure(state='normal')
        entry_descricao.delete(0, ctk.END)
        entry_descricao.configure(state='readonly')

        entry_pre_unit.configure(state='normal')
        entry_pre_unit.delete(0, ctk.END)
        entry_pre_unit.configure(state='readonly')

        entry_pre_comb.configure(state='normal')
        entry_pre_comb.delete(0, ctk.END)
        entry_pre_comb.configure(state='readonly')

        entry_pre_total.configure(state='normal')
        entry_pre_total.delete(0, ctk.END)
        entry_pre_total.configure(state='readonly')

        entry_cod.delete(0, ctk.END)

        entry_cupom.configure(state='normal')
        entry_cupom.delete(0, ctk.END)
        entry_cupom.configure(state='readonly')

    def nova_pesquisa():
        ean, material = pesquisar.pesquisar(pesquisa_aberta=False)
        if ean != '0' and material != '0':
            entry_cod.delete(0, ctk.END)
            entry_cod.insert(0, ean)
            entry_descricao.configure(state='normal')
            entry_descricao.delete(0, ctk.END)
            entry_descricao.insert(0, material)
            entry_descricao.configure(state='readonly')

    def novo_item():
        if usuario == "Administrador":
            cadastrar.novo_item()
            #atualizar_dic()
        else:
            messagebox.showerror(
                "Erro", "Seu usuário não tem permissão para cadastrar item!")

    def venda_cupom():
        lista_dados = arquivar.lista_de_vendas()
        print(lista_dados)
        visualizar.venda_por_cupom(lista_dados)

    def mostrar_ajuda():
        try:
            with open('database/ajuda.txt', 'r') as legenda:
                arquivo = legenda.read()
                messagebox.showinfo("Ajuda", arquivo)
        except FileNotFoundError:
            messagebox.showerror(
                "Erro", "O arquivo 'SUPORTE' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")

    def sair(janela_principal):
        resposta = messagebox.askyesno(
            "Encerrar", "Deseja encerrar o programa?")

        if resposta:
            janela_principal.destroy()
        else:
            return  

    ############################################ Inicio da Interface Grafica ##########################################

    janela_principal = ctk.CTk()
    janela_principal.title("ENTRADA E PEDIDO")
    janela_principal.geometry("1920x1000+0+0")
    janela_principal.iconbitmap("img/img5.ico")

    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("database/themas.txt")  
    
    frame_topo = ctk.CTkFrame(janela_principal, fg_color='transparent')
    frame_topo.pack(fill="x", padx=80, pady=(10, 0))

    # Label do título centralizado
    label_titulo = ctk.CTkLabel(frame_topo, text="CAIXA FECHADO",
                                width=200, text_color='#fff', font=("Arial", 30, 'bold'))
    label_titulo.grid(row=0, column=0, padx=(0, 550), pady=5)
    frame_topo.grid_columnconfigure(0, weight=1)

    # Frame do cupom alinhado à direita
    frame_cupon = ctk.CTkFrame(frame_topo, fg_color='transparent')
    frame_cupon.grid(row=0, column=1, padx=(0, 0), sticky="e")

    # Label e Entry do cupom
    label_cupom = ctk.CTkLabel(
        frame_cupon, text="Cupom N°:", text_color='#fff', font=('Arial', 30, 'bold'))
    label_cupom.grid(row=0, column=0, padx=(0, 20), pady=0)

    entry_cupom = ctk.CTkEntry(frame_cupon, font=(
        "Arial", 20), width=145, height=30, justify="right", state='readonly')
    entry_cupom.grid(row=0, column=1, padx=(0, 0), pady=0)
    # Frame principal
    frame_master = ctk.CTkFrame(janela_principal)
    frame_master.pack(fill="x", padx=80, pady=(10, 5))

    # Frame la esquerdo
    frame_esquerda = ctk.CTkFrame(frame_master, fg_color='transparent')
    frame_esquerda.grid(row=0, column=0, padx=(30, 15), pady=(0, 20))

    # Carregar a imagem usando PIL (precisa da biblioteca Pillow)
    image_baner = "img/banner.png"
    image = ctk.CTkImage(dark_image=Image.open(image_baner), size=(400, 225))
    label = ctk.CTkLabel(frame_esquerda, image=image, text="")
    label.pack(pady=(18, 20))

    # Carregar a imagem do botão "P"
    imagem_p = Image.open("img/buscar.png")
    imagem_p_resized = imagem_p.resize((35, 35))
    imagem_p_ctk = ImageTk.PhotoImage(imagem_p_resized)

    # Informações do Produto
    frame_inputs = ctk.CTkFrame(frame_esquerda)
    frame_inputs.pack(pady=0, padx=0)

    # Declaração de labels de imputs
    frame_inputs_label = ctk.CTkFrame(
        frame_inputs, width=100, fg_color="transparent")
    frame_inputs_label.grid(row=0, column=0, padx=(0, 0), pady=0, sticky="e")
    frame_inputs_entry1 = ctk.CTkFrame(frame_inputs, fg_color="transparent")
    frame_inputs_entry1.grid(row=1, column=0, padx=(0, 50), pady=0, sticky="w")
    frame_inputs_entry2 = ctk.CTkFrame(frame_inputs, fg_color="transparent")
    frame_inputs_entry2.grid(row=1, column=0, padx=(0, 0), pady=0, sticky="e")

    # Inputs e Label's
    label_cod = ctk.CTkLabel(
        frame_inputs_label, text="Código do Produto", width=100)
    entry_cod = ctk.CTkEntry(frame_inputs_entry1, placeholder_text='0000000000000',
                             placeholder_text_color='#ccc', font=("Arial", 25), width=200, height=50, fg_color='#fff')
    label_qtd = ctk.CTkLabel(frame_inputs_label, text="Qtd", width=30)
    entry_qtd = ctk.CTkEntry(frame_inputs_entry2, font=(
        "Arial", 25), width=60, height=50)

    entry_qtd.insert(0, "1")  # Definindo o valor padrão como 1

    label_descricao = ctk.CTkLabel(frame_inputs, text="Descrição do Produto")
    entry_descricao = ctk.CTkEntry(frame_inputs, font=(
        "Arial", 25), width=400, height=50, fg_color='#FFFFE0', state='readonly')

    # Posicionamento de imputs
    label_cod.grid(row=0, column=0, padx=(0, 260), pady=(10, 0), sticky='e')
    entry_cod.grid(row=1, column=0, padx=(0, 0), pady=0)

    label_qtd.grid(row=0, column=1, padx=(5, 0), pady=(10, 0), sticky='e')
    entry_qtd.grid(row=1, column=2, padx=(0, 0), pady=0)
    label_descricao.grid(row=2, column=0, padx=(0, 0),
                         pady=(30, 0), sticky='w')
    entry_descricao.grid(row=3, column=0, padx=(0, 0), pady=0)

    button_pesquisar = ctk.CTkButton(frame_inputs_entry1, image=imagem_p_ctk, text="", command=lambda: nova_pesquisa(
    ), width=30, height=50, fg_color="#fff", border_color='black', border_width=1,)
    button_pesquisar.grid(row=1, column=1, padx=(10, 10), pady=0)

    # Botões
    frame_butons = ctk.CTkFrame(frame_esquerda)
    frame_butons.pack(pady=(15, 0), padx=0)

    button_adicionar = ctk.CTkButton(frame_butons, text="ADICIONAR(Ctrl+a)", font=(
        'Ariel', 16, 'bold'), height=50, width=190, command=lambda: adicionar_item())
    button_deletar = ctk.CTkButton(frame_butons, text="DELETE(Ctrl+d)", font=(
        'Ariel', 16, 'bold'), height=50, width=190, command=lambda: deletar())
    button_pagar = ctk.CTkButton(frame_butons, text="PAGAR(Ctrl+p)", font=(
        'Ariel', 16, 'bold'), height=50, width=190, command=lambda: pagar_items())
    button_voltar = ctk.CTkButton(frame_butons, text="VOLTAR(Ctrl+v)", font=(
        'Ariel', 16, 'bold'), height=50, width=190, command=lambda: voltar())

    button_adicionar.grid(row=0, column=0, padx=(0, 10),
                          pady=(15, 15), sticky='w')
    button_deletar.grid(row=0, column=1, padx=(10, 0),
                        pady=(15, 15), sticky='e')
    button_pagar.grid(row=1, column=0, padx=(0, 10), pady=(15, 0), sticky='w')

    button_voltar.grid(row=1, column=1, padx=(10, 0), pady=(15, 0), sticky='e')

    # comandos do teclado
    janela_principal.bind_all("<Control-a>", lambda event: adicionar_item())
    janela_principal.bind_all("<Control-d>", lambda event: deletar())
    janela_principal.bind_all("<Control-p>", lambda event: pagar_items())
    janela_principal.bind_all("<Control-v>", lambda event: voltar())
    janela_principal.bind_all("<Control-b>", lambda event: nova_pesquisa())
    janela_principal.bind_all("<F1>", lambda event: nova_compra())
    janela_principal.bind_all("<F2>", lambda event: nova_pesquisa())
    janela_principal.bind_all("<F3>", lambda event: novo_item())
    janela_principal.bind_all("<F4>", lambda event: sair(janela_principal))
    janela_principal.bind_all("<F5>", lambda event: venda_cupom())
    janela_principal.bind_all("<F6>", lambda event: mostrar_ajuda())

    # Componentes do frame direito
    frame_direita = ctk.CTkFrame(frame_master, fg_color="transparent")
    frame_direita.grid(row=0, column=1, padx=(15, 30), pady=(0, 20))

    style = ttk.Style()  
    style.configure("Set.Treeview.Heading", font=("Helvetica", 16, "bold"))
    style.configure("Set.Treeview", font=("Courier", 24, "normal"),justify='left', rowheight=30)

    # Colunas da Tabela
    columns = ["Item/Cod", "Descrição/EAN","PreUnitR$/Qtd", "Preço R$"]
    tree = ttk.Treeview(frame_direita, columns=columns,
                        show="headings", height=18,style="Set.Treeview")

    # Definindo os cabeçalhos e as larguras das colunas
    tree.heading("Item/Cod", text=" Item ")
    tree.column("Item/Cod", anchor=tk.E, width=40)
    tree.heading("Descrição/EAN", text="  Descrição/EAN  ")
    tree.column("Descrição/EAN", anchor=tk.W, width=600)
    tree.heading("PreUnitR$/Qtd", text=" Preço R$/Qtd ")
    tree.column("PreUnitR$/Qtd", anchor=tk.E, width=100)
    tree.heading("Preço R$", text=" Total Item R$ ")
    tree.column("Preço R$", anchor=tk.E, width=100)
    

    tree.pack(fill=ctk.BOTH, expand=True, padx=(15, 15), pady=20)

    # Valore unitario e totais
    frame_valores = ctk.CTkFrame(frame_direita)
    frame_valores.pack(fill="x", expand=True, padx=(0, 15), pady=0)

    label_pre_unit = ctk.CTkLabel(frame_valores, text="Preço Unitario R$: ")
    entry_pre_unit = ctk.CTkEntry(frame_valores, font=(
        "Arial", 40), width=270, justify='right', fg_color='#FFFFE0', state='readonly')
    label_pre_comb = ctk.CTkLabel(frame_valores, text="Sub Total R$:")
    entry_pre_comb = ctk.CTkEntry(frame_valores, font=(
        "Arial", 40), width=300, justify='right', fg_color='#FFFFE0', state='readonly')
    label_pre_total = ctk.CTkLabel(frame_valores, text="Total a Pagar R$:")
    entry_pre_total = ctk.CTkEntry(frame_valores, font=(
        "Arial", 40), width=300, justify='right', fg_color='#FFFFE0', state='readonly')

    # Posicionamento
    label_pre_unit.grid(row=0, column=0,  pady=1, padx=(15, 420), sticky="w")
    entry_pre_unit.grid(row=1, column=0, pady=1, padx=(15, 0), sticky="w")
    label_pre_comb.grid(row=0, column=1,  pady=1, sticky="e")
    entry_pre_comb.grid(row=1, column=1,  pady=1, sticky="e")
    label_pre_total.grid(row=2, column=1,  pady=1, sticky="e")
    entry_pre_total.grid(row=3, column=1, pady=1, sticky="e")

    # Labels de usuarios e datas
    frame_userdates = ctk.CTkFrame(frame_valores, fg_color='transparent')
    frame_userdates.grid(row=3, column=0, pady=0, padx=15, sticky="w")
    data_label = ctk.CTkLabel(
        frame_userdates, text=f"Data: {data}", font=("Any", 14, "bold"))# usuario_label.grid(row=0, column=0, padx=(0,100), pady=(33,0))
    data_label.grid(row=0, column=1, padx=(0, 50), pady=(33, 0))

    label_info_botoes = ctk.CTkLabel(frame_esquerda, text=f"Operador: {usuario}", font=(
        "Any", 14, "bold")).pack(fill='x', expand=True, pady=(10, 0), padx=(5, 5))
    label_info = ctk.CTkLabel(janela_principal, text_color='#fff',
                              text='F1 = Nova Compra     -     F2 = Nova Pesquisa     -     F3 = Novo Item     -     F4 = Fechar     -     F5 = Venda Cupom     -      F6 = Suporte', font=("Any", 18, "bold")).pack(fill='x', expand=True)

    def atualizar_data():
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data_label.configure(text=f"Data: {data_atual}")
        janela_principal.after(1000, atualizar_data)
        return data_atual
    dic = {}
    data = atualizar_data()
    #atualizar_dic()

    janela_principal.mainloop()
    #entry_cod.focus_set()

# usuario,  empresa = "Administrador",  "Tem De Tudo ME"
# sistema(usuario, empresa)
