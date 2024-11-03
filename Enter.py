import customtkinter as ctk
from PIL import Image, ImageTk  # Pillow para manipulação de imagens
import vendas_tkinter as vendas
import json
from tkinter import messagebox


# Configuração inicial do tema visual da interface
ctk.set_appearance_mode("light")  # Modo de aparência escura
ctk.set_default_color_theme("themas.txt")  # Tema de cores azul-escuro

# Função para autenticação do usuário ao sistema
def autenticar_usuario():
    usuario = usuario_var.get()
    senha = senha_var.get()
    data = data_var.get()
    empresa = empresa_var.get()

    # Verifica se todos os campos estão preenchidos
    if not usuario or not senha or not data or not empresa:
        messagebox.showerror("Erro", "Usuário, Senha ou Data\nnão devem ser nulos")
        return

    try:
        autenticado = False  # Inicializa o status de autenticação como falso
        
        for user in dados_usuario:
            if user['nome'] == usuario and user['senha'] == senha:
                janela_login.destroy()
                vendas.sistema(usuario, data, empresa)
                autenticado = True  # Autenticação bem-sucedida
                break

        if not autenticado:# Se não houver autenticação, exibe mensagem de erro
            messagebox.showerror("Erro", "Usuário ou Senha Incorretos")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado:\n {str(e)}")

# Função para exibir as informações de suporte
def abrir_suporte():
    try:
        with open('dependencias/bd_usuarios.txt', 'r') as legenda:
            arquivo = legenda.read()
            messagebox.showinfo("Suporte", arquivo)
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo 'usuarios.txt' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")

try:
    with open('dependencias/bd_usuarios.txt', 'r') as bd: # Carregamento dos dados de usuários a partir de um arquivo JSON
        dados_usuario = json.load(bd)
except FileNotFoundError:
    messagebox.showerror("Erro", "O arquivo 'usuarios.txt' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")

# Criação da janela_login principal
janela_login = ctk.CTk()  
janela_login.geometry("740x400")  # Define o tamanho da janela_login
janela_login.resizable(width=False, height=False) 
janela_login.title("LOGIN VENDAS")  

# Variáveis que armazenam os dados dos campos de entrada
usuario_var = ctk.StringVar(value="Administrador")  # Valor inicial: Administrador
senha_var = ctk.StringVar(value="1234")  # Valor inicial: 1234
data_var = ctk.StringVar(value="27/10/2024 12:00")  # Valor inicial de data
empresa_var = ctk.StringVar(value="Tem De Tudo ME")  # Empresa padrão

# Configuração do layout da interface
frame = ctk.CTkFrame(master=janela_login)  
frame.pack(pady=20, padx=20, fill="both", expand=True  )  # Posição e preenchimento do frame

# Carregar a imagem usando PIL (precisa da biblioteca Pillow)
image_baner = "dependencias/imagem_login.png"
image = ctk.CTkImage(dark_image=Image.open(image_baner), size=(100, 100))

# Carregando a imagem
imagem = Image.open("dependencias/imagem_login.png")  
imagem = imagem.resize((392, 270))  # Redimensiona a imagem para caber na interface
imagem_tk = ImageTk.PhotoImage(imagem)  # Converte 

# Coluna 1: Imagem (não há funcionalidade, mas pode ser associada a um arquivo de imagem)
imagem_label = ctk.CTkLabel(master=frame, image=imagem_tk, text="")
imagem_label.grid(row=0, column=0, padx=(20,0), pady=(20,10))  # Posição da imagem no layout

# Coluna 2: Formulário de login
form_frame = ctk.CTkFrame(master=frame,fg_color='transparent')  
form_frame.grid(row=0, column=1, padx=50, pady=20)  

# Campo para seleção da empresa
empresa_label = ctk.CTkLabel(master=form_frame, text="Empresa", font=('any', 12))  
empresa_label.grid(row=0, column=0, sticky="w")  
empresa_combo = ctk.CTkComboBox(master=form_frame, values=["Tem De Tudo ME"], variable=empresa_var, font=('any', 17), width=300)  # Combobox para empresa
empresa_combo.grid(row=1, column=0)  

# Campo para seleção do usuário
usuario_label = ctk.CTkLabel(master=form_frame, text="Usuário", font=('any', 12))  
usuario_label.grid(row=2, column=0, sticky="w")  
usuario_combo = ctk.CTkComboBox(master=form_frame, values=["Administrador", "Operador do Turno 1", "Operador do Turno 2"], variable=usuario_var, font=('any', 18), width=300)  # Combobox para usuário
usuario_combo.grid(row=3, column=0)  

# Campo para entrada da senha
senha_label = ctk.CTkLabel(master=form_frame, text="Senha", font=('any', 12))  
senha_label.grid(row=4, column=0, sticky="w")  
senha_entry = ctk.CTkEntry(master=form_frame, show="*", textvariable=senha_var, font=('any', 18), width=300)  # Campo de entrada de senha (oculta os caracteres)
senha_entry.grid(row=5, column=0)  

# Campo para entrada da data
data_label = ctk.CTkLabel(master=form_frame, text="Data", font=('any', 12))  
data_label.grid(row=6, column=0, sticky="w")  
data_entry = ctk.CTkEntry(master=form_frame, textvariable=data_var, font=('any', 16), width=300)  
data_entry.grid(row=7, column=0)  

# Criação dos botões
button_frame = ctk.CTkFrame(master=janela_login, fg_color='transparent')  
button_frame.pack(pady=1)  

# Botão OK para confirmar o login
ok_button = ctk.CTkButton(master=button_frame, text="OK", command=autenticar_usuario, font=('any', 10, 'bold'), width=100)
ok_button.grid(row=0, column=0, padx=10)  

# Botão SAIR para fechar a aplicação
sair_button = ctk.CTkButton(master=button_frame, text="SAIR", command=janela_login.quit, font=('any', 10, 'bold'), fg_color="red", width=100)
sair_button.grid(row=0, column=1, padx=10,pady=20)  

# Botão SUPORTE para abrir a janela_login de suporte
suporte_button = ctk.CTkButton(master=button_frame, text="SUPORTE", command=abrir_suporte, font=('any', 10, 'bold'), width=100)
suporte_button.grid(row=0, column=2, padx=10 ,pady=20)  # Posição do botão SUPORTE

janela_login.mainloop()  # Inicia a aplicação e mantém a janela_login aberta até que seja fechada
