import customtkinter as ctk
from tkinter import messagebox

# Função para exibir o diálogo de entrada de CPF
def cpf():
    def on_confirm():
        cpf_value = cpf_entry.get()
        if not cpf_value or cpf_value is None:
            messagebox.showinfo("Aviso", "Nenhum CPF fornecido. Usando CPF padrão: 000.000.000-00")
            
            cpf_formatado="000.000.000-00"

            print(cpf_formatado)
            root.destroy()  # Fechar a janela
            return cpf_formatado
        
        elif len(cpf_value) == 11 and cpf_value.isdigit():
            cpf_formatado = f"{cpf_value[:3]}.{cpf_value[3:6]}.{cpf_value[6:9]}-{cpf_value[9:]}"
            messagebox.showinfo("CPF Válido", f"CPF: {cpf_formatado}")
              # Fechar a janela
            print(cpf_formatado)
            root.destroy()
            return cpf_formatado
           
        else:
            messagebox.showerror("Erro", "CPF inválido. Deve ter 11 dígitos numéricos.")
    
    # Criar a janela principal com CustomTkinter
    root = ctk.CTk()
    root.geometry("250x130")
    root.title("Adicionar CPF")
    root.resizable(width=False,height=False )
    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("dark-blue")  # Tema de cores azul-escuru


    # Label para instrução
    cpf_label = ctk.CTkLabel(root, text="Adicione um CPF:", font=('Arial', 10))
    cpf_label.pack(pady=0,padx=(0,120))

    # Caixa de entrada para o CPF
    cpf_entry = ctk.CTkEntry(root, placeholder_text="000.000.000-00", width=200, font=('Arial', 12))
    cpf_entry.pack(pady=10)

    # Botão para confirmar o CPF
    confirm_button = ctk.CTkButton(root, text="Confirmar", command=on_confirm)
    confirm_button.pack(pady=10)
    
    root.mainloop()

    #return cpf_formatado
# Chamar a função CPF
#cpf()
#print (cpf)