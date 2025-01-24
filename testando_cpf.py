import customtkinter as ctk
from tkinter import messagebox


# Função para exibir o diálogo de entrada de CPF
def cpf():
    cpf_formatado = ''
    
    def on_confirm():
        nonlocal cpf_formatado
        cpf_value = cpf_entry.get()
        
        if not cpf_value or cpf_value is None:
            messagebox.showinfo("Aviso", "Nenhum CPF fornecido. Usando CPF padrão: 000.000.000-00")
            
            cpf_formatado="000.000.000-00"

            
            janela_cpf.destroy()  # Fechar a janela
            return cpf_formatado
            
        elif len(cpf_value) == 11 and cpf_value.isnumeric():#se for numerico e conter 11 digitos

            cpf_formatado = f"{cpf_value[:3]}.{cpf_value[3:6]}.{cpf_value[6:9]}-{cpf_value[9:]}"
            messagebox.showinfo("CPF Válido", f"CPF: {cpf_formatado}")
            janela_cpf.destroy()  # Fechar a janela
            
            
            return cpf_formatado
           
        else:
            messagebox.showerror("Erro", "CPF inválido. Informe apenas valores numéricos.")

    # Criar a janela principal com CustomTkinter
    janela_cpf = ctk.CTkToplevel()
    janela_cpf.geometry("250x130")
    janela_cpf.title("Adicionar CPF")
    janela_cpf.resizable(width=False,height=False )
    janela_cpf.iconbitmap("dependencias/img5.ico")
    
    janela_cpf.focus_force()
    janela_cpf.grab_set()
    ctk.set_appearance_mode("light")  # Modo de aparência escura
    ctk.set_default_color_theme("dark-blue")  # Tema de cores azul-escuru


    # Label para instrução
    cpf_label = ctk.CTkLabel(janela_cpf, text="Adicione um CPF:", font=('Arial', 10))
    cpf_label.pack(pady=0,padx=(0,120))

    # Caixa de entrada para o CPF
    cpf_entry = ctk.CTkEntry(janela_cpf, placeholder_text="Somente numeros", width=200, font=('Arial', 12))
    cpf_entry.pack(pady=10)

    # Botão para confirmar o CPF
    confirm_button = ctk.CTkButton(janela_cpf, text="Confirmar", command=on_confirm)
    confirm_button.pack(pady=10)
    janela_cpf.bind_all("<space>",lambda event: on_confirm())
    janela_cpf.wait_window()
    
    
    print(cpf_formatado)
    return cpf_formatado

# Chamar a função CPF
#cpf()
#print (cpf)