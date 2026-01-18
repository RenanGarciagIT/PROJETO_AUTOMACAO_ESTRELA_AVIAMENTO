import sqlite3

# Cria (ou abre) o banco de dados
conn = sqlite3.connect("ordem_servico.db")
cursor = conn.cursor()

# ==========================
# TABELA: ORDEM DE SERVIÇO
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS ordem_servico (
    id_os INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_os TEXT NOT NULL,
    tipo_os TEXT NOT NULL,
    status TEXT NOT NULL,
    data_abertura DATE NOT NULL,
    data_fechamento DATE
)
""")

# ==========================
# TABELA: SERVIÇOS DA OS
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS servico_os (
    id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
    id_os INTEGER NOT NULL,
    descricao_servico TEXT NOT NULL,
    tecnico TEXT NOT NULL,
    tempo_horas REAL,
    custo_servico REAL,
    FOREIGN KEY (id_os) REFERENCES ordem_servico(id_os)
)
""")


cursor.execute("""
CREATE TABLE reg_automacao (
    id_os INTEGER,
    numero_os TEXT,
    tipo_os TEXT,
    status TEXT,
    data_abertura TEXT,
    data_fechamento TEXT
);
""")

# Salva e fecha
conn.commit()
conn.close()
