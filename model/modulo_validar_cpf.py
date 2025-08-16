import customtkinter as ctk
from tkinter import messagebox

janela_aberta = False  

def cpf():
    global janela_aberta

    if janela_aberta:
        messagebox.showinfo("AVISO", "JANELA ABERTA!")
        return ""  

    janela_aberta = True
    cpf_formatado = ''
    
    def on_confirm():
        nonlocal cpf_formatado 
        global janela_aberta
        cpf_value = cpf_entry.get().replace(' ','')
        
        if not cpf_value:
            #janela_cpf.destroy()
            messagebox.showinfo("AVISO", "CPF:000.000.000-00")
            cpf_formatado = "000.000.000-00"
            janela_cpf.destroy()
            return
        
        if len(cpf_value) == 11 and cpf_value.isnumeric():
            cpf_formatado = f"{cpf_value[:3]}.{cpf_value[3:6]}.{cpf_value[6:9]}-{cpf_value[9:]}"  
                     
            messagebox.showinfo("AVOSO", f"CPF: {cpf_formatado}")          
            janela_cpf.destroy()
            return
        else:
            messagebox.showerror("ERRO", "CPF INVALIDO!")

    def on_close():
        global janela_aberta
        janela_aberta = False
        janela_cpf.destroy()

    # Janela principal
    janela_cpf = ctk.CTkToplevel()
    janela_cpf.geometry("250x180+700+450")
    janela_cpf.title("Adicionar CPF")
    janela_cpf.resizable(False, False)
    janela_cpf.iconbitmap("img/img5.ico")
    janela_cpf.protocol("WM_DELETE_WINDOW", on_close)

    janela_cpf.focus_force()
    janela_cpf.grab_set()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("database/themas.txt")

    # Componentes da janela
    cpf_label = ctk.CTkLabel(janela_cpf, text="Adicione um CPF:", font=('Arial', 10))
    cpf_label.pack(pady=0, padx=(0, 120))

    cpf_entry = ctk.CTkEntry(janela_cpf, placeholder_text="Somente números", width=200, font=('Arial', 12))
    cpf_entry.pack(pady=10)
    #cpf_entry.focus_set()
    desc= ctk.CTkLabel(janela_cpf, text="", font=('Arial', 8))
    desc.pack(pady=10, padx=10)

    confirm_button = ctk.CTkButton(janela_cpf, text="Confirmar", command=on_confirm)
    confirm_button.pack(pady=10)
    if janela_aberta:
        janela_cpf.after(100, lambda: cpf_entry.focus_set())
    janela_cpf.wait_window()
    janela_aberta = False  # Garante o reset do controle após fechamento
    
    return cpf_formatado
