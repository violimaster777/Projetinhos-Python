import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json as son
import os
import sys
from PIL import Image, ImageTk

# Variáveis globais
cat = None
imagem_flor_caminho = None
imagens_carregadas = {}

def recurso_relativo(caminho):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, caminho)
    return os.path.join(os.path.abspath("."), caminho)

class Flor:
    def __init__(self, nome, especie, descricao, cor, data=None, foto=None):
        self.nome = nome
        self.especie = especie
        self.descricao = descricao
        self.cor = cor
        self.data = data if data else datetime.now()
        self.foto = foto

    def to_dict(self):
        return {
            'nome': self.nome,
            'especie': self.especie,
            'descricao': self.descricao,
            'cor': self.cor,
            'data': self.data.strftime("%d/%m/%Y"),
            'foto': self.foto
        }

class Catalogo:
    def __init__(self, arquivoX):
        self.arquivoX = arquivoX
        self.flores = []
        self.carregar_flores()

    def add_flores(self, flor):
        self.flores.append(flor)
        self.salvar_flores()

    def listar_flores(self):
        return [flor.to_dict() for flor in self.flores]

    def salvar_flores(self):
        with open(f'{self.arquivoX}.json', 'w') as f:
            son.dump(self.listar_flores(), f, indent=2)

    def carregar_flores(self):
        if os.path.exists(f'{self.arquivoX}.json'):
            with open(f'{self.arquivoX}.json', 'r') as f:
                dados = son.load(f)
                for item in dados:
                    item['data'] = datetime.strptime(item['data'], '%d/%m/%Y')
                self.flores = [Flor(**item) for item in dados]

def escolher_foto():
    global imagem_flor_caminho
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])
    if caminho:
        imagem_flor_caminho = caminho
        messagebox.showinfo("Imagem selecionada", f"Imagem selecionada:\n{caminho}")

def salvar_flor():
    global cat, imagem_flor_caminho
    arquivoX = entry_arquivoX.get().strip()
    if not arquivoX:
        messagebox.showerror("Erro", "Informe o nome do arquivo.")
        return

    cat = Catalogo(arquivoX)

    nome = entry_nome.get()
    especie = entry_especie.get()
    cor = entry_cor.get()
    descricao = text_descricao.get("1.0", tk.END).strip()
    data_texto = entry_data.get()

    try:
        data = datetime.strptime(data_texto, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
        return

    nova_flor = Flor(nome, especie, descricao, cor, data, imagem_flor_caminho)
    cat.add_flores(nova_flor)
    imagem_flor_caminho = None  # Resetar após salvar
    atualizar_tabela()
    messagebox.showinfo("Sucesso", "Flor salva com sucesso!")

def carregar_flores():
    global cat
    arquivox = entry_arquivoX.get().strip()
    if not arquivox:
        messagebox.showerror("Erro", "Informe o arquivo.")
        return

    cat = Catalogo(arquivox)
    atualizar_tabela()
    messagebox.showinfo("Info", "Flores carregadas do arquivo.")

def atualizar_tabela():
    if cat is None:
        return

    for item in tree.get_children():
        tree.delete(item)

    imagens_carregadas.clear()

    for i, flor in enumerate(cat.listar_flores()):
        imagem = None
        if flor['foto'] and os.path.exists(flor['foto']):
            imagem_raw = Image.open(flor['foto']).resize((30, 30))
            imagem = ImageTk.PhotoImage(imagem_raw)
            imagens_carregadas[i] = imagem

        tree.insert('', 'end', image=imagem, values=(
            flor['nome'], flor['especie'], flor['cor'], flor['descricao'], flor['data']
        ))

# GUI
janela = tk.Tk()
janela.title("Catálogo de Flores")
janela.geometry("900x600")

imagem_fundo = Image.open(recurso_relativo("fundo.gif"))
imagem_fundo = imagem_fundo.resize((800, 600))
fundo = ImageTk.PhotoImage(imagem_fundo)

label_fundo = tk.Label(janela, image=fundo)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(janela, text="                                      ").grid(row=0, column=0, sticky="w")
tk.Label(janela, text="\n\n\n\n\n").grid(row=0, column=0, columnspan=3, sticky="n")
tk.Label(janela, text="Nome do Arquivo:").grid(row=1, column=1, sticky="w")
entry_arquivoX = tk.Entry(janela)
entry_arquivoX.grid(row=1, column=1)

tk.Label(janela, text="Nome:").grid(row=2, column=1, sticky='w')
entry_nome = tk.Entry(janela, width=30)
entry_nome.grid(row=2, column=1)

tk.Label(janela, text="Espécie:").grid(row=3, column=1, sticky='w')
entry_especie = tk.Entry(janela, width=30)
entry_especie.grid(row=3, column=1)

tk.Label(janela, text="Cor:").grid(row=4, column=1, sticky='w')
entry_cor = tk.Entry(janela, width=30)
entry_cor.grid(row=4, column=1)

tk.Label(janela, text="Data (DD/MM/AAAA):").grid(row=5, column=1, sticky='w')
entry_data = tk.Entry(janela, width=30)
entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
entry_data.grid(row=5, column=1)

tk.Label(janela, text="Descrição:").grid(row=6, column=1, sticky='nw')
text_descricao = tk.Text(janela, width=40, height=4)
text_descricao.grid(row=6, column=1, sticky='e')

btn_escolher = tk.Button(janela, text="Escolher Imagem", command=escolher_foto)
btn_escolher.grid(row=7, column=1, pady=5, sticky='w')

btn_salvar = tk.Button(janela, text="Salvar Flor", command=salvar_flor)
btn_salvar.grid(row=7, column=1, pady=5, sticky='sne')

btn_carregar = tk.Button(janela, text="Carregar Flores", command=carregar_flores)
btn_carregar.grid(row=7, column=2, pady=5, sticky='e')

tree = ttk.Treeview(janela, columns=("Nome", "Espécie", "Cor", "Descrição", "Data"), show='tree headings')
tree.heading("#0", text="Imagem")
tree.column("#0", width=60)
for col in ("Nome", "Espécie", "Cor", "Descrição", "Data"):
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=8, column=1, columnspan=2, pady=10, sticky='w')

janela.mainloop()

