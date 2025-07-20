import customtkinter as ctk
from PIL import Image, ImageTk  
import model.interface as vendas
import json
from tkinter import messagebox


ctk.set_appearance_mode("light")  # Modo de aparência escura
ctk.set_default_color_theme("themas.txt")  # Tema de cores azul-escuro


def autenticar_usuario():
    usuario = usuario_var.get()
    senha = senha_var.get()
    empresa = empresa_var.get()

    if not usuario or not senha or not empresa:
        messagebox.showerror(
            
            "Erro", "Usuário, Senha ou Data\nnão devem ser nulos")
        return
    try:
        autenticado = False  # Inicializa o status de autenticação como falso
        for user in dados_usuario:
            if user['nome'] == usuario and user['senha'] == senha:
                janela_login.destroy()
                vendas.sistema(usuario, empresa)
                autenticado = True  
                break

        if not autenticado:  
            messagebox.showerror("Erro", "Usuário ou Senha Incorretos")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado:\n {str(e)}")

def abrir_suporte():
    try:
        with open('img/bd_usuarios.txt', 'r') as legenda:
            arquivo = legenda.read()
            messagebox.showinfo("Suporte", arquivo)
    except FileNotFoundError:
        messagebox.showerror(
            "Erro", "O arquivo 'usuarios.txt' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")

try:
    with open('img/bd_usuarios.txt', 'r') as bd:
        dados_usuario = json.load(bd)
except FileNotFoundError:
    messagebox.showerror(
        "Erro", "O arquivo 'usuarios.txt' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")


janela_login = ctk.CTk()
janela_login.geometry("740x400")  # Define o tamanho da janela_login
janela_login.resizable(width=False, height=False)
janela_login.title("LOGIN VENDAS")
janela_login.iconbitmap("img/img5.ico")

usuario_var = ctk.StringVar(value="Administrador")
senha_var = ctk.StringVar(value="1234")  
empresa_var = ctk.StringVar(value="Tem De Tudo ME")

frame = ctk.CTkFrame(master=janela_login)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Carregar a imagem usando PIL (precisa da biblioteca Pillow)
image_baner = "img/imagem_login.png"
image = ctk.CTkImage(dark_image=Image.open(image_baner), size=(100, 100))
imagem = Image.open("img/imagem_login.png")
imagem = imagem.resize((392, 270))
imagem_tk = ImageTk.PhotoImage(imagem)  

imagem_label = ctk.CTkLabel(master=frame, image=imagem_tk, text="")
imagem_label.grid(row=0, column=0, padx=(20, 0), pady=(
    20, 10))  

form_frame = ctk.CTkFrame(master=frame, fg_color='transparent')
form_frame.grid(row=0, column=1, padx=50, pady=20)

empresa_label = ctk.CTkLabel(
    master=form_frame, text="Empresa", font=('any', 12))
empresa_label.grid(row=0, column=0, sticky="w")
empresa_combo = ctk.CTkComboBox(master=form_frame, values=[
                                "Tem De Tudo ME"], variable=empresa_var, font=('any', 17), width=300)
empresa_combo.grid(row=1, column=0)

usuario_label = ctk.CTkLabel(
    master=form_frame, text="Usuário", font=('any', 12))
usuario_label.grid(row=2, column=0, sticky="w")
usuario_combo = ctk.CTkComboBox(master=form_frame, values=[
                                "Administrador", "Operador do Turno 1", "Operador do Turno 2"], variable=usuario_var, font=('any', 18), width=300)
usuario_combo.grid(row=3, column=0)

# Campo para entrada da senha
senha_label = ctk.CTkLabel(master=form_frame, text="Senha", font=('any', 12))
senha_label.grid(row=4, column=0, sticky="w")
senha_entry = ctk.CTkEntry(master=form_frame, show="*", textvariable=senha_var, font=(
    'any', 18), width=300)  
senha_entry.grid(row=5, column=0)

button_frame = ctk.CTkFrame(master=janela_login, fg_color='transparent')
button_frame.pack(pady=1)
ok_button = ctk.CTkButton(master=button_frame, text="OK",
                          command=autenticar_usuario, font=('any', 10, 'bold'), width=100)
ok_button.grid(row=0, column=0, padx=10)
sair_button = ctk.CTkButton(master=button_frame, text="SAIR", command=janela_login.quit, font=(
    'any', 10, 'bold'), fg_color="red", width=100)
sair_button.grid(row=0, column=1, padx=10, pady=20)
suporte_button = ctk.CTkButton(master=button_frame, text="SUPORTE",
                               command=abrir_suporte, font=('any', 10, 'bold'), width=100)
suporte_button.grid(row=0, column=2, padx=10, pady=20)

janela_login.mainloop()
