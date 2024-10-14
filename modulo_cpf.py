
import tkinter as tk
from tkinter import messagebox, simpledialog

def cpf():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do tkinter

    while True:
        try:
            # Solicita o CPF com um simples diálogo
            cpf = simpledialog.askstring("CPF", "Adicione um CPF:")
            
            # Se o CPF for vazio ou o usuário cancelar, retorna o CPF zerado
            if not cpf:
                cpf = "000.000.000-00"
                return cpf
            
            # Verifica se o CPF tem 11 dígitos e é composto apenas por números
            if len(cpf) == 11 and cpf.isdigit():
                # Formata o CPF
                cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                return cpf
            else:
                messagebox.showerror("Erro", "CPF inválido. Deve ter 11 dígitos numéricos.")
                continue
        except ValueError:
            messagebox.showerror("Erro", "CPF inválido")
            continue
    

