'''  
    python -m venv nome_do_ambiente
    nome_do_ambiente\Scripts\Activate

'''
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from tkinter.filedialog import askopenfilename
import json
import vender as venda


# Função para autenticar o usuário
def autenticar():
    usuario = combo_usuario.get()
    senha = entry_senha.get()
    data = entry_data.get()
    empresa = combo_empresa.get()

    if not usuario or not senha or not data or not empresa:
        messagebox.showerror("Erro", "Usuário, Senha ou Data não devem ser nulos")
        return

    autenticado = False
    for user in dados_usuario:
        if user['nome'] == usuario and user['senha'] == senha:
            root.destroy()
            venda.sistema(usuario, data, empresa)
            autenticado = True
            break

    if not autenticado:
        messagebox.showerror("Erro", "Usuário ou Senha Incorretos")


# Função para abrir o arquivo de suporte
def abrir_suporte():
    try:
        with open('usuarios.txt', 'r') as legenda:
            arquivo = legenda.read()
            messagebox.showinfo("AJUDA", arquivo)
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo 'comanda.txt' não foi encontrado.\nVerifique o caminho ou crie o arquivo.")


# Início do código principal
try:
    with open('usuarios.txt', 'r') as bd:
        dados_usuario = json.load(bd)
except FileNotFoundError:
    messagebox.showerror("Erro", "O arquivo 'dados/usuarios.txt' não foi encontrado. Verifique o caminho ou crie o arquivo.")

root = tk.Tk()
root.title("LOGIN VENDAS")

# Estilo
style = ttk.Style()
style.configure('TButton', font=('Any', 10, 'bold'))
style.configure('TLabel', font=('Any', 12))
style.configure('TCombobox', font=('Any', 18))
style.configure('TEntry', font=('Any', 18))

# Layout
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Imagem (você precisará de um caminho para uma imagem válida)
image = tk.PhotoImage(file="imagem_login.png")
label_image = ttk.Label(frame, image=image)
label_image.grid(row=0, column=0, rowspan=5, padx=(0, 20))

# Empresa
label_empresa = ttk.Label(frame, text="Empresa")
label_empresa.grid(row=0, column=1, sticky=tk.W)
combo_empresa = ttk.Combobox(frame, values=["Tem De Tudo ME"], state="readonly")
combo_empresa.set("Tem De Tudo ME")
combo_empresa.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Usuário
label_usuario = ttk.Label(frame, text="Usuário")
label_usuario.grid(row=2, column=1, sticky=tk.W)
combo_usuario = ttk.Combobox(frame, values=["Administrador", "Operador do Turno 1", "Operador do Turno 2"], state="readonly")
combo_usuario.set("Administrador")
combo_usuario.grid(row=3, column=1, sticky=(tk.W, tk.E))

# Senha
label_senha = ttk.Label(frame, text="Senha")
label_senha.grid(row=4, column=1, sticky=tk.W)
entry_senha = ttk.Entry(frame, show="*")
entry_senha.grid(row=5, column=1, sticky=(tk.W, tk.E))
entry_senha.insert(0, "1234")

# Data
label_data = ttk.Label(frame, text="Data")
label_data.grid(row=6, column=1, sticky=tk.W)
entry_data = ttk.Entry(frame)
entry_data.grid(row=7, column=1, sticky=(tk.W, tk.E))
entry_data.insert(0, "2024-03-21 17:41:22")

# Botões
button_frame = ttk.Frame(frame)
button_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
button_ok = ttk.Button(button_frame, text="OK", command=autenticar)
button_ok.grid(row=0, column=0, padx=5)
button_sair = ttk.Button(button_frame, text="SAIR", command=root.quit)
button_sair.grid(row=0, column=1, padx=5)
button_suporte = ttk.Button(button_frame, text="SUPORTE", command=abrir_suporte)
button_suporte.grid(row=0, column=2, padx=5)

root.mainloop()
