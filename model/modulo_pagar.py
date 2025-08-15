import customtkinter as ctk
from tkinter import messagebox, simpledialog


condicao_pagamento = ['Dinheiro', 'Cartão à Vista', 'Cartão à Prazo', 'Pix']
pagamento= False
def pagar(valor_pagar):
    global pagamento
    if pagamento:
        return valor_pagar
    pagamento = True  

    def voltar():
        global  pagamento
        pagamento = False 
        
        window_pagamento.destroy()
        return valor_pagar

    def pagar_cartao_pix():
        nonlocal valor_pagar  
        if valor_pagar > 0:
            valor_entry.configure(state="normal")
            valor_entry.delete(0, ctk.END)
            valor_entry.insert(0, f" {0:.2f}")
            valor_entry.configure(state="readonly")
            recebido_entry.configure(state="normal")
            recebido_entry.delete(0, ctk.END)
            recebido_entry.insert(0, f" {valor_pagar:.2f}")
            recebido_entry.configure(state="readonly")
            autenticação.configure(text="PAGAMENTO", text_color="lightgreen")
            autenticação1.configure(text="AUTORIZADO", text_color="lightgreen")
            valor_pagar = 0.0 
            return valor_pagar
        else:
            autenticação.configure(text="PAGAMENTO", text_color="lightgreen")
            autenticação1.configure(text="AUTORIZADO", text_color="lightgreen")
            return valor_pagar  

    # Função para pagamento em Dinheiro
    def pagar_dinheiro():
        nonlocal valor_pagar 
        try:
            dinheiro_str = recebido_entry.get()
            if dinheiro_str is None or dinheiro_str.strip() == "":
                autenticação.configure(text="VALOR RECEBIDO", text_color="yellow")
                autenticação1.configure(text="INVALIDO", text_color="yellow")
                return  valor_pagar 

            dinheiro = float(dinheiro_str.replace(",", "."))
            if dinheiro < valor_pagar:                
                autenticação.configure(text="PAGAMENTO", text_color="orange")
                autenticação1.configure(text="VALOR INSUFICIENTE", text_color="orange")
                return valor_pagar 
            
            elif valor_pagar ==0:
                autenticação.configure(text="PAGAMENTO", text_color="lightgreen")
                autenticação1.configure(text="JÁ AUTORIZADO", text_color="lightgreen")
                return valor_pagar  # Retorna o valor original se o pagamento for zero
            else:
                troco = round(dinheiro - valor_pagar, 2)
                valor_entry.configure(state="normal")
                valor_entry.delete(0, ctk.END)
                valor_entry.insert(0, f"{0:.2f}")

                recebido_entry.configure(state="normal")
                recebido_entry.delete(0, ctk.END)
                recebido_entry.insert(0, f"{dinheiro:.2f}")

                troco_entry.configure(state="normal")
                troco_entry.delete(0, ctk.END)
                troco_entry.insert(0, f"{troco:.2f}")
                troco_entry.configure(state="readonly")
                autenticação.configure(text="PAGAMENTO", text_color="lightgreen")
                autenticação1.configure(text="AUTORIZADO", text_color="lightgreen")           
                valor_pagar = 0.0  
                return valor_pagar
            
        except ValueError:
            messagebox.showinfo("ERRO", "Informe um valor válido")
            return valor_pagar  # Retorna o valor original se houver erro

    # Janela principal de pagamento
    window_pagamento = ctk.CTkToplevel()
    window_pagamento.title("PAGAMENTO")
    window_pagamento.geometry("826x420+696+142")
    window_pagamento.resizable(width=False, height=False)
    window_pagamento.iconbitmap("img/img5.ico")
    window_pagamento.focus_force()
    window_pagamento.grab_set()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("database/themas.txt")

    frame_master = ctk.CTkFrame(window_pagamento)
    frame_master.pack(padx=100, pady=50)
    frame_valores = ctk.CTkFrame(frame_master, fg_color="transparent")
    frame_valores.grid(padx=20,pady=20)
    frame_botoes = ctk.CTkFrame(window_pagamento,fg_color="transparent")
    frame_botoes.pack()

    # Elementos da interface gráfica
    ctk.CTkLabel(frame_valores, text="Forma de pagamento").grid(row=1, column=2,padx=(20,0), sticky="w")
    condicao_pagamento_var = ctk.StringVar(value="Pix")
    ctk.CTkOptionMenu(frame_valores, values=condicao_pagamento, variable=condicao_pagamento_var, font=("Any", 30), width=300).grid(row=2, column=2, padx=(20,0), sticky="w")

    butom_voltar = ctk.CTkButton(frame_botoes, text="SAIR",  fg_color=('red'),command=voltar, font=("Any", 13))
    butom_voltar.grid(row = 0, column = 1,pady=0, padx=20)
    butom_pagar = ctk.CTkButton(frame_botoes, text="PAGAR", command=lambda: pagar_dinheiro() if condicao_pagamento_var.get() == "Dinheiro" else pagar_cartao_pix(), font=("Any", 13))
    butom_pagar.grid(row = 0, column = 0,pady=0,padx=20)

    # Frame para os valores
    ctk.CTkLabel(frame_valores, text="Valor da Compra R$:", font=("Any", 12)).grid(row=1, column=1, sticky="w")
    valor_entry = ctk.CTkEntry(frame_valores, font=("Any", 30), width=200, justify='right',fg_color='#FFFFE0')
    valor_entry.grid(row=2, column=1, sticky="w")
    valor_entry.insert(0, f"{valor_pagar:.2f}")
    valor_entry.configure(state="readonly") 
    ctk.CTkLabel(frame_valores, text="Valor Recebido R$:", font=("Any", 12)).grid(row=3, column=1, sticky="w")
    recebido_entry = ctk.CTkEntry(frame_valores, font=("Any", 30), width=200, justify='right',placeholder_text="0.00", fg_color='#FFFFE0')
    recebido_entry.grid(row=4, column=1, sticky="w")
    
    autenticação = ctk.CTkLabel(frame_valores, text="", font=("helvetica", 20))
    autenticação.grid(row=4, column=2, pady=(0, 10), padx=(20, 0), sticky="we")
    autenticação1 = ctk.CTkLabel(frame_valores, text="", font=("helvetica", 20))
    autenticação1.grid(row=5, column=2, pady=(0, 10), padx=(20, 0), sticky="we")

    ctk.CTkLabel(frame_valores, text="Troco Devolvido R$:", font=("Any", 12)).grid(row=5, column=1, sticky="w")
    troco_entry = ctk.CTkEntry(frame_valores, font=("Any", 30), width=200, justify='right', placeholder_text="0,00",fg_color='#FFFFE0')
    troco_entry.configure(state="readonly")  
    troco_entry.grid(row=6, column=1, sticky="w")   
    
    window_pagamento.wait_window()
    return valor_pagar

    
    #

# Exemplo de uso
# valor_pagar = 100.50
# resposta = pagar(valor_pagar)
# print(f'A resposta é: {resposta}')
