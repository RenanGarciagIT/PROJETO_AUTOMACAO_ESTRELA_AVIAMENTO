import sqlite3
import subprocess
import tempfile

# ---------------- CONEXÃO ----------------

def conectar_db():
    return sqlite3.connect("ordem_servico.db")

# ---------------- BUSCAR OS ----------------

def buscar_ordens(cursor):
    cursor.execute("""
        SELECT
            id_os,
            numero_os,
            tipo_os,
            status,
            data_abertura,
            data_fechamento
        FROM ordem_servico
        ORDER BY id_os
    """)
    return cursor.fetchall()

# ---------------- BUSCAR SERVIÇOS ----------------

def buscar_servicos(cursor, id_os):
    cursor.execute("""
        SELECT
            descricao_servico,
            tecnico,
            tempo_horas,
            custo_servico
        FROM servico_os
        WHERE id_os = ?
    """, (id_os,))
    return cursor.fetchall()

# ---------------- SALVAR NA REG_AUTOMACAO ----------------

def salvar_reg_automacao(cursor, os_dados):
    cursor.execute("""
        INSERT INTO reg_automacao (
            id_os,
            numero_os,
            tipo_os,
            status,
            data_abertura,
            data_fechamento
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, os_dados)

# ---------------- GERAR TEXTO ----------------

def gerar_texto(os_dados, servicos):
    (
        id_os,
        numero_os,
        tipo_os,
        status,
        data_abertura,
        data_fechamento
    ) = os_dados

    linhas = [
        f"OS: {numero_os}",
        f"Tipo: {tipo_os}",
        f"Status: {status}",
        f"Data Abertura: {data_abertura}",
        f"Data Fechamento: {data_fechamento}",
        "Serviços:"
    ]

    if not servicos:
        linhas.append("  - Nenhum serviço vinculado")

    for i, s in enumerate(servicos, start=1):
        descricao, tecnico, tempo, custo = s
        linhas.append(
            f"  {i} - {descricao} | Técnico: {tecnico} | "
            f"Tempo: {tempo}h | Custo: {custo}"
        )

    linhas.append("-" * 60)
    linhas.append("")

    return "\n".join(linhas)

# ---------------- APAGAR REGISTROS ----------------

def apagar_os(cursor, id_os):
    cursor.execute("DELETE FROM servico_os WHERE id_os = ?", (id_os,))
    cursor.execute("DELETE FROM ordem_servico WHERE id_os = ?", (id_os,))

# ---------------- BLOCO DE NOTAS ----------------

def abrir_bloco_notas(texto):
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt",
        mode="w",
        encoding="utf-8"
    ) as f:
        f.write(texto)
        caminho = f.name

    subprocess.Popen(["notepad.exe", caminho])

# ---------------- EXECUÇÃO ----------------

def executar():
    conn = conectar_db()
    cursor = conn.cursor()

    texto_final = ""
    ordens = buscar_ordens(cursor)

    if not ordens:
        print("Nenhuma OS encontrada.")
        return

    for os_dados in ordens:
        id_os = os_dados[0]

        servicos = buscar_servicos(cursor, id_os)

        # salva histórico
        salvar_reg_automacao(cursor, os_dados)

        # gera texto
        texto_final += gerar_texto(os_dados, servicos)

        # apaga OS e serviços
        apagar_os(cursor, id_os)

    conn.commit()
    conn.close()

    abrir_bloco_notas(texto_final)

# ---------------- START ----------------

if __name__ == "__main__":
    executar()
