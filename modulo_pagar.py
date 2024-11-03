import customtkinter as ctk
from tkinter import messagebox, simpledialog

# Condições de pagamento
condicao_pagamento = ['Dinheiro', 'Cartão à Vista', 'Cartão à Prazo', 'Pix']

def pagar(valor_pagar):
    # Função para voltar e fechar a janela
    def voltar():
        window_pagamento.destroy()
        return valor_pagar

    # Função para pagamento com Cartão ou Pix
    def pagar_cartao_pix():
        nonlocal valor_pagar  # Refere-se à variável valor_pagar da função externa
        if valor_pagar > 0:
            valor_entry.configure(state="normal")
            valor_entry.delete(0, ctk.END)
            valor_entry.insert(0, f"R$ {0:.2f}")
            recebido_entry.configure(state="normal")
            recebido_entry.delete(0, ctk.END)
            recebido_entry.insert(0, f"R$ {valor_pagar:.2f}")
            messagebox.showinfo("ORDEM DE PAGAMENTO", "Pagamento Autorizado")
            valor_pagar = 0.0  # Define valor_pagar para 0 após o pagamento
            window_pagamento.destroy()
            return valor_pagar
        else:
            messagebox.showwarning("ORDEM DE PAGAMENTO", "Informe o Valor da Compra")
            return valor_pagar  # Retorna o valor original se o pagamento não for concluído"""

    # Função para pagamento em Dinheiro
    def pagar_dinheiro():
        nonlocal valor_pagar  # Refere-se à variável valor_pagar da função externa
        try:
            dinheiro_str = recebido_entry.get()
            if dinheiro_str is None or dinheiro_str.strip() == "":
                messagebox.showwarning("ORDEM DE PAGAMENTO", "Nenhum valor inserido!")
                return valor_pagar  # Retorna o valor original se não houver entrada

            # Converte o valor para float e lida com vírgula como separador decimal
            dinheiro = float(dinheiro_str.replace(",", "."))
            if dinheiro < valor_pagar:
                messagebox.showwarning("ORDEM DE PAGAMENTO", "Valor Insuficiente")
                return valor_pagar
            else:
                # Calcula o troco
                troco = round(dinheiro - valor_pagar, 2)

                # Atualiza os campos com os valores formatados
                valor_entry.configure(state="normal")
                valor_entry.delete(0, ctk.END)
                valor_entry.insert(0, f"{valor_pagar:.2f}")

                recebido_entry.configure(state="normal")
                recebido_entry.delete(0, ctk.END)
                recebido_entry.insert(0, f"{dinheiro:.2f}")

                troco_entry.configure(state="normal")
                troco_entry.delete(0, ctk.END)
                troco_entry.insert(0, f"{troco:.2f}")

                valor_pagar = 0.0  # Define valor_pagar para 0 após o pagamento
                messagebox.showinfo("ORDEM DE PAGAMENTO", f"Pagamento Autorizado! Troco: R$ {troco:.2f}")
                window_pagamento.destroy()  # Fecha a janela após o pagamento
                return valor_pagar

        except ValueError:
            messagebox.showerror("ERRO", "Informe um valor válido")
            return valor_pagar  # Retorna o valor original se houver erro

    # Janela principal de pagamento
    window_pagamento = ctk.CTkToplevel()
    window_pagamento.title("PAGAMENTO")
    window_pagamento.geometry("400x350")
    window_pagamento.resizable(width=False, height=False)
    window_pagamento.focus_force()
    window_pagamento.grab_set()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")

    frame_master = ctk.CTkFrame(window_pagamento)
    frame_master.grid(row=0, column=0, padx=20, pady=20)

    frame_valores = ctk.CTkFrame(frame_master)
    frame_valores.grid()
    frame_botoes = ctk.CTkFrame(frame_master)
    frame_botoes.grid(row=0, column=1, sticky='n', pady=(0, 20), padx=10)

    # Elementos da interface gráfica
    ctk.CTkLabel(frame_valores, text="Forma de pagamento", font=("Any", 12)).grid(row=0, column=0, sticky="w")
    condicao_pagamento_var = ctk.StringVar(value="Pix")
    ctk.CTkOptionMenu(frame_valores, values=condicao_pagamento, variable=condicao_pagamento_var, font=("Any", 22), width=200).grid(row=1, column=0, sticky="w")

    ctk.CTkButton(frame_botoes, text="VOLTAR", command=voltar, font=("Any", 13)).grid(row=0, column=2, pady=(0, 20))
    ctk.CTkButton(frame_botoes, text="PAGAR", command=lambda: pagar_dinheiro() if condicao_pagamento_var.get() == "Dinheiro" else pagar_cartao_pix(), font=("Any", 13)).grid(row=1, column=2)

    # Frame para os valores
    ctk.CTkLabel(frame_valores, text="Valor da Compra R$:", font=("Any", 12)).grid(row=2, column=0, sticky="w")
    valor_entry = ctk.CTkEntry(frame_valores, font=("Any", 30), width=200, justify='right')
    valor_entry.grid(row=3, column=0, sticky="w")
    valor_entry.insert(0, f"{valor_pagar:.2f}")

    ctk.CTkLabel(frame_valores, text="Valor Recebido R$:", font=("Any", 12)).grid(row=4, column=0, sticky="w")
    recebido_entry = ctk.CTkEntry(frame_valores, font=("Any", 30), width=200, justify='right')
    recebido_entry.grid(row=5, column=0, sticky="w")
    recebido_entry.insert(0, "0.00")

    ctk.CTkLabel(frame_valores, text="Troco Devolvido R$:", font=("Any", 12)).grid(row=6, column=0, sticky="w")
    troco_entry = ctk.CTkEntry(frame_valores, font=("Any", 30), width=200, justify='right')
    troco_entry.grid(row=7, column=0, sticky="w")
    
    troco_entry.insert(0, "0.00")
    
    window_pagamento.wait_window()
   
    return valor_pagar

    
    #

# Exemplo de uso
'''valor_pagar = 100.50
resposta = pagar(valor_pagar)
print(f'A resposta é: {resposta}')'''
