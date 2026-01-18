import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- FUNÇÃO DE NAVEGAÇÃO ----------------

def mudar_tela(frame):
    frame.tkraise()

# ---------------- CONEXÃO DB ----------------

def conectar_db():
    return sqlite3.connect("ordem_servico.db")

# ---------------- FUNÇÃO ADICIONAR SERVIÇO ----------------

def adicionar_servico():
    descricao = entry_descricao.get()
    tecnico = entry_tecnico.get()
    tempo = entry_tempo.get()
    custo = entry_custo.get()

    if descricao == "" or tecnico == "":
        return

    tabela_servicos.insert(
        "",
        "end",
        values=(descricao, tecnico, tempo, custo)
    )

    entry_descricao.delete(0, tk.END)
    entry_tecnico.delete(0, tk.END)
    entry_tempo.delete(0, tk.END)
    entry_custo.delete(0, tk.END)

# ---------------- SALVAR OS + SERVIÇOS ----------------

def salvar_os_e_servicos():
    if not tabela_servicos.get_children():
        messagebox.showwarning("Atenção", "Adicione pelo menos um serviço.")
        return

    conn = conectar_db()
    cursor = conn.cursor()

    # ---------- SALVAR OS ----------
    cursor.execute("""
        INSERT INTO ordem_servico (
            numero_os,
            tipo_os,
            status,
            data_abertura,
            data_fechamento
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        entry_numero_os.get(),
        entry_tipo_os.get(),
        entry_status.get(),
        entry_data_abertura.get(),
        entry_data_fechamento.get()
    ))

    id_os = cursor.lastrowid

    # ---------- SALVAR SERVIÇOS ----------
    for item in tabela_servicos.get_children():
        descricao, tecnico, tempo, custo = tabela_servicos.item(item)["values"]

        cursor.execute("""
            INSERT INTO servico_os (
                id_os,
                descricao_servico,
                tecnico,
                tempo_horas,
                custo_servico
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            id_os,
            descricao,
            tecnico,
            tempo,
            custo
        ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Ordem de Serviço salva com sucesso!")

    limpar_tela()

# ---------------- LIMPAR TELA ----------------

def limpar_tela():
    for entry in (
        entry_numero_os,
        entry_tipo_os,
        entry_status,
        entry_data_abertura,
        entry_data_fechamento
    ):
        entry.delete(0, tk.END)

    for item in tabela_servicos.get_children():
        tabela_servicos.delete(item)

# ---------------- JANELA PRINCIPAL ----------------

janela = tk.Tk()
janela.title("Registro de Ordem de Serviço")
janela.state("zoomed")

container = tk.Frame(janela)
container.pack(fill="both", expand=True)

# ---------------- TELAS ----------------

tela_inicial = tk.Frame(container)
tela_cadastro = tk.Frame(container)

for tela in (tela_inicial, tela_cadastro):
    tela.place(relwidth=1, relheight=1)

# ---------------- TELA INICIAL ----------------

tk.Label(
    tela_inicial,
    text="TELA INICIAL",
    font=("Arial", 20)
).pack(pady=40)

tk.Button(
    tela_inicial,
    text="ADICIONAR OS",
    width=25,
    height=3,
    command=lambda: mudar_tela(tela_cadastro)
).pack(pady=10)

# ---------------- TELA CADASTRO ----------------

tk.Label(
    tela_cadastro,
    text="CADASTRO DA ORDEM DE SERVIÇO",
    font=("Arial", 20)
).pack(pady=20)

# ----------- FORMULÁRIO OS -----------

form_os = tk.LabelFrame(tela_cadastro, text="Dados da OS", padx=20, pady=20)
form_os.pack(fill="x", padx=40)

tk.Label(form_os, text="Número OS").grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_numero_os = tk.Entry(form_os, width=25)
entry_numero_os.grid(row=0, column=1)

tk.Label(form_os, text="Tipo OS").grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_tipo_os = tk.Entry(form_os, width=25)
entry_tipo_os.grid(row=1, column=1)

tk.Label(form_os, text="Status").grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_status = tk.Entry(form_os, width=25)
entry_status.grid(row=2, column=1)

tk.Label(form_os, text="Data Abertura").grid(row=0, column=2, sticky="e", padx=10, pady=5)
entry_data_abertura = tk.Entry(form_os, width=25)
entry_data_abertura.grid(row=0, column=3)

tk.Label(form_os, text="Data Fechamento").grid(row=1, column=2, sticky="e", padx=10, pady=5)
entry_data_fechamento = tk.Entry(form_os, width=25)
entry_data_fechamento.grid(row=1, column=3)

# ----------- FORMULÁRIO SERVIÇOS -----------

form_servico = tk.LabelFrame(tela_cadastro, text="Adicionar Serviço", padx=20, pady=10)
form_servico.pack(fill="x", padx=40, pady=20)

tk.Label(form_servico, text="Descrição").grid(row=0, column=0)
entry_descricao = tk.Entry(form_servico, width=30)
entry_descricao.grid(row=1, column=0, padx=5)

tk.Label(form_servico, text="Técnico").grid(row=0, column=1)
entry_tecnico = tk.Entry(form_servico, width=20)
entry_tecnico.grid(row=1, column=1, padx=5)

tk.Label(form_servico, text="Tempo (h)").grid(row=0, column=2)
entry_tempo = tk.Entry(form_servico, width=10)
entry_tempo.grid(row=1, column=2, padx=5)

tk.Label(form_servico, text="Custo").grid(row=0, column=3)
entry_custo = tk.Entry(form_servico, width=10)
entry_custo.grid(row=1, column=3, padx=5)

tk.Button(
    form_servico,
    text="Adicionar Serviço",
    width=20,
    command=adicionar_servico
).grid(row=1, column=4, padx=10)

# ----------- TABELA DE SERVIÇOS -----------

frame_tabela = tk.Frame(tela_cadastro)
frame_tabela.pack(fill="both", expand=True, padx=40)

scroll = tk.Scrollbar(frame_tabela)
scroll.pack(side="right", fill="y")

tabela_servicos = ttk.Treeview(
    frame_tabela,
    columns=("descricao", "tecnico", "tempo", "custo"),
    show="headings",
    yscrollcommand=scroll.set
)

scroll.config(command=tabela_servicos.yview)

tabela_servicos.heading("descricao", text="Descrição do Serviço")
tabela_servicos.heading("tecnico", text="Técnico")
tabela_servicos.heading("tempo", text="Tempo (h)")
tabela_servicos.heading("custo", text="Custo")

tabela_servicos.pack(fill="both", expand=True)

# ----------- BOTÕES FINAIS -----------

tk.Button(
    tela_cadastro,
    text="SALVAR OS",
    width=20,
    height=2,
    command=salvar_os_e_servicos
).pack(pady=10)

tk.Button(
    tela_cadastro,
    text="VOLTAR",
    width=20,
    height=2,
    command=lambda: mudar_tela(tela_inicial)
).pack(pady=10)

# ---------------- INICIAR ----------------

mudar_tela(tela_inicial)
janela.mainloop()
