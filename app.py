import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# =============================
# CONTROLE GLOBAL
# =============================
os_em_edicao = None

# =============================
# BANCO
# =============================
def conectar():
    return sqlite3.connect("ordem_servico.db")

# =============================
# APP
# =============================
root = tk.Tk()
root.title("Sistema de Ordem de Serviço")
root.state("zoomed")

container = tk.Frame(root)
container.pack(expand=True, fill="both")

def limpar_tela():
    for w in container.winfo_children():
        w.destroy()

# =============================
# TELA INICIAL
# =============================
def tela_inicial():
    limpar_tela()

    frame = tk.Frame(container)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="Sistema de Ordem de Serviço",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    tk.Button(
        frame,
        text="Cadastrar OS",
        width=35,
        height=2,
        command=lambda: tela_os()
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Alterar OS",
        width=35,
        height=2,
        command=tela_lista_os
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Sair",
        width=35,
        height=2,
        command=root.quit
    ).pack(pady=10)

# =============================
# TELA CRIAR / EDITAR OS
# =============================
def tela_os(id_os=None):
    global os_em_edicao
    os_em_edicao = id_os

    limpar_tela()

    frame = tk.Frame(container)
    frame.pack(expand=True)

    tk.Label(
        frame,
        text="ORDEM DE SERVIÇO",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    # =============================
    # FORMULÁRIO OS
    # =============================
    form_os = tk.Frame(frame)
    form_os.pack()

    campos = ["Número OS", "Tipo OS", "Status", "Data Abertura", "Data Fechamento"]
    entradas = {}

    for i, campo in enumerate(campos):
        tk.Label(form_os, text=campo).grid(row=0, column=i, padx=5)
        entradas[campo] = tk.Entry(form_os, width=18)
        entradas[campo].grid(row=1, column=i, padx=5)

    # =============================
    # SERVIÇOS
    # =============================
    tk.Label(
        frame,
        text="SERVIÇOS",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    serv_frame = tk.Frame(frame)
    serv_frame.pack()

    headers = ["Descrição", "Técnico", "Horas", "Custo"]
    for i, h in enumerate(headers):
        tk.Label(serv_frame, text=h).grid(row=0, column=i, padx=5)

    linhas_servicos = []

    def adicionar_servico(valores=None):
        row = len(linhas_servicos) + 1

        e1 = tk.Entry(serv_frame, width=30)
        e2 = tk.Entry(serv_frame, width=20)
        e3 = tk.Entry(serv_frame, width=10)
        e4 = tk.Entry(serv_frame, width=10)

        if valores:
            e1.insert(0, valores[0])
            e2.insert(0, valores[1])
            e3.insert(0, valores[2])
            e4.insert(0, valores[3])

        e1.grid(row=row, column=0, padx=5)
        e2.grid(row=row, column=1, padx=5)
        e3.grid(row=row, column=2, padx=5)
        e4.grid(row=row, column=3, padx=5)

        linhas_servicos.append((e1, e2, e3, e4))

    adicionar_servico()

    tk.Button(
        frame,
        text="Adicionar Serviço",
        command=adicionar_servico
    ).pack(pady=5)

    # =============================
    # CARREGAR DADOS (EDIÇÃO)
    # =============================
    if id_os:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT numero_os, tipo_os, status, data_abertura, data_fechamento
            FROM ordem_servico WHERE id_os=?
        """, (id_os,))
        dados = cur.fetchone()

        for campo, valor in zip(campos, dados):
            entradas[campo].insert(0, valor)

        cur.execute("""
            SELECT descricao_servico, tecnico, tempo_horas, custo_servico
            FROM servico_os WHERE id_os=?
        """, (id_os,))

        for serv in cur.fetchall():
            adicionar_servico(serv)

        conn.close()

    # =============================
    # SALVAR OS
    # =============================
    def salvar_os():
        conn = conectar()
        cur = conn.cursor()

        valores_os = [entradas[c].get() for c in campos]

        if os_em_edicao is None:
            cur.execute("""
                INSERT INTO ordem_servico
                (numero_os, tipo_os, status, data_abertura, data_fechamento)
                VALUES (?, ?, ?, ?, ?)
            """, valores_os)
            id_atual = cur.lastrowid
        else:
            cur.execute("""
                UPDATE ordem_servico SET
                numero_os=?, tipo_os=?, status=?, data_abertura=?, data_fechamento=?
                WHERE id_os=?
            """, valores_os + [os_em_edicao])

            cur.execute(
                "DELETE FROM servico_os WHERE id_os=?",
                (os_em_edicao,)
            )
            id_atual = os_em_edicao

        for s in linhas_servicos:
            if s[0].get():
                cur.execute("""
                    INSERT INTO servico_os
                    (id_os, descricao_servico, tecnico, tempo_horas, custo_servico)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    id_atual,
                    s[0].get(),
                    s[1].get(),
                    s[2].get(),
                    s[3].get()
                ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "OS salva com sucesso!")
        tela_os()

    # =============================
    # EXCLUIR OS
    # =============================
    def excluir_os():
        if os_em_edicao is None:
            return

        if not messagebox.askyesno(
            "Confirmar Exclusão",
            "Deseja realmente excluir esta OS?\nEssa ação não pode ser desfeita."
        ):
            return

        conn = conectar()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM servico_os WHERE id_os=?",
            (os_em_edicao,)
        )
        cur.execute(
            "DELETE FROM ordem_servico WHERE id_os=?",
            (os_em_edicao,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "OS excluída com sucesso!")
        tela_inicial()

    # =============================
    # BOTÕES
    # =============================
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=20)

    tk.Button(
        btn_frame,
        text="Enviar OS",
        bg="green",
        fg="white",
        width=35,
        height=2,
        command=salvar_os
    ).pack(pady=5)

    if os_em_edicao:
        tk.Button(
            btn_frame,
            text="Excluir OS",
            bg="red",
            fg="white",
            width=35,
            height=2,
            command=excluir_os
        ).pack(pady=5)

    tk.Button(
        btn_frame,
        text="Voltar",
        width=35,
        command=tela_inicial
    ).pack(pady=5)

# =============================
# LISTA DE OS
# =============================
def tela_lista_os():
    limpar_tela()

    frame = tk.Frame(container)
    frame.pack(expand=True, fill="both")

    tabela = ttk.Treeview(
        frame,
        columns=("id", "numero", "status"),
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("numero", text="Número OS")
    tabela.heading("status", text="Status")

    tabela.pack(expand=True, fill="both", padx=20, pady=20)

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id_os, numero_os, status FROM ordem_servico")
    dados = cur.fetchall()
    conn.close()

    if not dados:
        messagebox.showinfo(
            "Nenhuma OS",
            "Não existem Ordens de Serviço cadastradas."
        )
    else:
        for row in dados:
            tabela.insert("", "end", values=row)

    def editar_os():
        item = tabela.selection()
        if item:
            id_os = tabela.item(item)["values"][0]
            tela_os(id_os)

    btn_editar = tk.Button(
        frame,
        text="Editar OS",
        width=30,
        height=2,
        command=editar_os
    )
    btn_editar.pack(pady=5)

    if not dados:
        btn_editar.config(state="disabled")

    tk.Button(
        frame,
        text="Cadastrar Nova OS",
        width=30,
        height=2,
        command=lambda: tela_os()
    ).pack(pady=5)

    tk.Button(
        frame,
        text="Voltar",
        width=30,
        height=2,
        command=tela_inicial
    ).pack(pady=5)

# =============================
# START
# =============================
tela_inicial()
root.mainloop()
