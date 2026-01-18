import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- FUNÇÃO DE NAVEGAÇÃO ----------------

def mudar_tela(frame):
    frame.tkraise()

# ---------------- CONEXÃO DB ----------------

def conectar_db():
    return sqlite3.connect("ordem_servico.db")

# ================= FUNÇÕES CADASTRO =================

def adicionar_servico():
    descricao = entry_descricao.get()
    tecnico = entry_tecnico.get()
    tempo = entry_tempo.get()
    custo = entry_custo.get()

    if descricao == "" or tecnico == "":
        return

    tabela_servicos.insert("", "end", values=(descricao, tecnico, tempo, custo))

    entry_descricao.delete(0, tk.END)
    entry_tecnico.delete(0, tk.END)
    entry_tempo.delete(0, tk.END)
    entry_custo.delete(0, tk.END)


def salvar_os_e_servicos():
    if not tabela_servicos.get_children():
        messagebox.showwarning("Atenção", "Adicione pelo menos um serviço.")
        return

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ordem_servico (
            numero_os, tipo_os, status, data_abertura, data_fechamento
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        entry_numero_os.get(),
        entry_tipo_os.get(),
        entry_status.get(),
        entry_data_abertura.get(),
        entry_data_fechamento.get()
    ))

    id_os = cursor.lastrowid

    for item in tabela_servicos.get_children():
        descricao, tecnico, tempo, custo = tabela_servicos.item(item)["values"]

        cursor.execute("""
            INSERT INTO servico_os (
                id_os, descricao_servico, tecnico, tempo_horas, custo_servico
            ) VALUES (?, ?, ?, ?, ?)
        """, (id_os, descricao, tecnico, tempo, custo))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Ordem de Serviço salva com sucesso!")
    limpar_tela()
    mudar_tela(tela_inicial)


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

# ================= FUNÇÕES LISTAGEM =================

def carregar_os_cadastradas():
    for item in tabela_os.get_children():
        tabela_os.delete(item)

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_os, numero_os, tipo_os, status, data_abertura, data_fechamento
        FROM ordem_servico
        ORDER BY id_os DESC
        LIMIT 100
    """)

    for i, row in enumerate(cursor.fetchall()):
        lixo = "🗑" if i < 10 else ""
        tabela_os.insert("", "end", values=(
            row[0], row[1], row[2], row[3], row[4], row[5], lixo
        ))

    conn.close()
    mudar_tela(tela_lista_os)


def abrir_servicos(event):
    item = tabela_os.selection()
    if not item:
        return

    id_os = tabela_os.item(item)["values"][0]
    carregar_servicos_os(id_os)
    mudar_tela(tela_servicos_os)


def carregar_servicos_os(id_os):
    for item in tabela_servicos_os.get_children():
        tabela_servicos_os.delete(item)

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT descricao_servico, tecnico, tempo_horas, custo_servico
        FROM servico_os
        WHERE id_os = ?
    """, (id_os,))

    for row in cursor.fetchall():
        tabela_servicos_os.insert("", "end", values=row)

    conn.close()


def clicar_lixeira(event):
    item = tabela_os.identify_row(event.y)
    coluna = tabela_os.identify_column(event.x)

    if not item or coluna != "#7":
        return

    id_os = tabela_os.item(item)["values"][0]

    if not messagebox.askyesno("Confirmação", "Deseja excluir esta OS?"):
        return

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM servico_os WHERE id_os = ?", (id_os,))
    cursor.execute("DELETE FROM ordem_servico WHERE id_os = ?", (id_os,))

    conn.commit()
    conn.close()

    carregar_os_cadastradas()

# ================= JANELA PRINCIPAL =================

janela = tk.Tk()
janela.title("Registro de Ordem de Serviço")
janela.state("zoomed")

container = tk.Frame(janela)
container.pack(fill="both", expand=True)

# ---------------- TELAS ----------------

tela_inicial = tk.Frame(container)
tela_cadastro = tk.Frame(container)
tela_lista_os = tk.Frame(container)
tela_servicos_os = tk.Frame(container)

for tela in (tela_inicial, tela_cadastro, tela_lista_os, tela_servicos_os):
    tela.place(relwidth=1, relheight=1)

# ================= TELA INICIAL =================

tk.Label(tela_inicial, text="TELA INICIAL", font=("Arial", 20)).pack(pady=30)

tk.Button(
    tela_inicial, text="ADICIONAR OS",
    width=30, height=3,
    command=lambda: mudar_tela(tela_cadastro)
).pack(pady=10)

tk.Button(
    tela_inicial, text="OS CADASTRADAS",
    width=30, height=3,
    command=carregar_os_cadastradas
).pack(pady=10)

# ================= TELA CADASTRO =================

tk.Label(tela_cadastro, text="CADASTRO DA ORDEM DE SERVIÇO", font=("Arial", 20)).pack(pady=20)

form_os = tk.LabelFrame(tela_cadastro, text="Dados da OS", padx=20, pady=20)
form_os.pack(fill="x", padx=40)

tk.Label(form_os, text="Número OS").grid(row=0, column=0, sticky="e", padx=10)
entry_numero_os = tk.Entry(form_os, width=25)
entry_numero_os.grid(row=0, column=1)

tk.Label(form_os, text="Tipo OS").grid(row=1, column=0, sticky="e", padx=10)
entry_tipo_os = tk.Entry(form_os, width=25)
entry_tipo_os.grid(row=1, column=1)

tk.Label(form_os, text="Status").grid(row=2, column=0, sticky="e", padx=10)
entry_status = tk.Entry(form_os, width=25)
entry_status.grid(row=2, column=1)

tk.Label(form_os, text="Data Abertura").grid(row=0, column=2, sticky="e", padx=10)
entry_data_abertura = tk.Entry(form_os, width=25)
entry_data_abertura.grid(row=0, column=3)

tk.Label(form_os, text="Data Fechamento").grid(row=1, column=2, sticky="e", padx=10)
entry_data_fechamento = tk.Entry(form_os, width=25)
entry_data_fechamento.grid(row=1, column=3)

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

tk.Button(form_servico, text="Adicionar Serviço", command=adicionar_servico).grid(row=1, column=4, padx=10)

tabela_servicos = ttk.Treeview(
    tela_cadastro,
    columns=("descricao", "tecnico", "tempo", "custo"),
    show="headings"
)
for col in ("descricao", "tecnico", "tempo", "custo"):
    tabela_servicos.heading(col, text=col.capitalize())

tabela_servicos.pack(fill="both", expand=True, padx=40)

tk.Button(tela_cadastro, text="SALVAR OS", command=salvar_os_e_servicos).pack(pady=10)
tk.Button(tela_cadastro, text="VOLTAR", command=lambda: mudar_tela(tela_inicial)).pack(pady=10)

# ================= TELA LISTA OS =================

tk.Label(tela_lista_os, text="OS CADASTRADAS", font=("Arial", 20)).pack(pady=20)

tabela_os = ttk.Treeview(
    tela_lista_os,
    columns=("id", "numero", "tipo", "status", "abertura", "fechamento", "lixo"),
    show="headings"
)

for col, txt in zip(
    tabela_os["columns"],
    ["ID", "Número", "Tipo", "Status", "Abertura", "Fechamento", ""]
):
    tabela_os.heading(col, text=txt)

tabela_os.pack(fill="both", expand=True, padx=40)
tabela_os.bind("<Double-1>", abrir_servicos)
tabela_os.bind("<Button-1>", clicar_lixeira)

tk.Button(tela_lista_os, text="VOLTAR", command=lambda: mudar_tela(tela_inicial)).pack(pady=10)

# ================= TELA SERVIÇOS =================

tk.Label(tela_servicos_os, text="SERVIÇOS DA OS", font=("Arial", 20)).pack(pady=20)

tabela_servicos_os = ttk.Treeview(
    tela_servicos_os,
    columns=("descricao", "tecnico", "tempo", "custo"),
    show="headings"
)

for col in ("descricao", "tecnico", "tempo", "custo"):
    tabela_servicos_os.heading(col, text=col.capitalize())

tabela_servicos_os.pack(fill="both", expand=True, padx=40)

tk.Button(
    tela_servicos_os, text="VOLTAR",
    command=lambda: mudar_tela(tela_lista_os)
).pack(pady=10)

# ---------------- INICIAR ----------------

mudar_tela(tela_inicial)
janela.mainloop()
