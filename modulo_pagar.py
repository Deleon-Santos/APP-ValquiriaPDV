import customtkinter as ctk
from tkinter import messagebox,simpledialog


condicao_pagamento = ['Dinheiro', 'Cartão á Vista', 'Cartão á Prazo', 'Pix']

def pagar(valor_pagar):
    def voltar():
        window_pagamento.destroy()

    def pagar_cartao_pix():
        if valor_pagar > 0:
            valor_entry.configure(state="normal")
            valor_entry.delete(0, ctk.END)
            valor_entry.insert(0, f"R$ {0:.2f}")
            recebido_entry.configure(state="normal")
            recebido_entry.delete(0, ctk.END)
            recebido_entry.insert(0, f"R$ {valor_pagar:.2f}")
            messagebox.showinfo("ORDEM DE PAGAMENTO", "Pagamento Autorizado")
        else:
            messagebox.showwarning("ORDEM DE PAGAMENTO", "Informe o Valor da Compra")

    def pagar_dinheiro():
        try:
            dinheiro = float(ttk.simpledialog.askstring("ENTRADA DE VALOR", "Valor Recebido:").replace(",", "."))
            if dinheiro < valor_pagar:
                messagebox.showwarning("ORDEM DE PAGAMENTO", "Valor Insuficiente")
            else:
                troco = dinheiro - valor_pagar
                valor_entry.configure(state="normal")
                valor_entry.delete(0, ctk.END)
                valor_entry.insert(0, f"R$ {0:.2f}")
                recebido_entry.configure(state="normal")
                recebido_entry.delete(0, ctk.END)
                recebido_entry.insert(0, f"R$ {dinheiro:.2f}")
                troco_entry.configure(state="normal")
                troco_entry.delete(0, ctk.END)
                troco_entry.insert(0, f"R$ {troco:.2f}")
                messagebox.showinfo("ORDEM DE PAGAMENTO", "Pagamento Autorizado")
        except ValueError:
            messagebox.showerror("ERRO", "Informe um valor válido")

    # Janela principal
    window_pagamento = ctk.CTk()
    window_pagamento.title("PAGAMENTO")
    window_pagamento.geometry("600x400")

    # Elementos da interface
    ctk.CTkLabel(window_pagamento, text="Forma de pagamento", font=("Any", 12)).grid(row=0, column=0, pady=10)
    condicao_pagamento_var = ctk.StringVar(value="Pix")
    ctk.CTkOptionMenu(window_pagamento, values=condicao_pagamento, variable=condicao_pagamento_var, font=("Any", 22)).grid(row=0, column=1, padx=20)

    ctk.CTkButton(window_pagamento, text="VOLTAR", command=voltar, font=("Any", 13)).grid(row=0, column=2)
    ctk.CTkButton(window_pagamento, text="PAGAR", command=lambda: pagar_cartao_pix() if condicao_pagamento_var.get() != "Dinheiro" else pagar_dinheiro(), font=("Any", 13)).grid(row=1, column=2)

    # Frame valores
    ctk.CTkLabel(window_pagamento, text="Valor da Compra R$:", font=("Any", 12)).grid(row=2, column=0, pady=10)
    valor_entry = ctk.CTkEntry(window_pagamento, font=("Any", 30), width=150)
    valor_entry.grid(row=2, column=1, pady=10)
    valor_entry.insert(0, f"{valor_pagar:.2f}")

    ctk.CTkLabel(window_pagamento, text="Valor Recebido R$:", font=("Any", 12)).grid(row=3, column=0, pady=10)
    recebido_entry = ctk.CTkEntry(window_pagamento, font=("Any", 30), width=150)
    recebido_entry.grid(row=3, column=1, pady=10)
    recebido_entry.insert(0, "0.00")

    ctk.CTkLabel(window_pagamento, text="Troco Devolvido R$:", font=("Any", 12)).grid(row=4, column=0, pady=10)
    troco_entry = ctk.CTkEntry(window_pagamento, font=("Any", 30), width=150)
    troco_entry.grid(row=4, column=1, pady=10)
    troco_entry.insert(0, "0.00")

    window_pagamento.mainloop()

# Exemplo de uso
pagar(100.50)
