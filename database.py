"""
database.py
------------
Responsável por tudo que envolve o banco de dados:
- Criar a conexão com o SQLite
- Criar a tabela (se ainda não existir)

Por que separar isso em um arquivo próprio?
Porque assim, se um dia você quiser trocar o SQLite por outro banco
(ex: PostgreSQL), só precisa mexer aqui — o resto do programa não muda.
"""

import sqlite3
import os

# Caminho do arquivo do banco de dados (fica na mesma pasta do projeto)
DB_PATH = os.path.join(os.path.dirname(__file__), "patio.db")


def conectar():
    """
    Abre e retorna uma conexão com o banco de dados SQLite.
    row_factory = sqlite3.Row permite acessar colunas pelo nome,
    ex: linha["numero_container"], em vez de só pelo índice linha[0].
    """
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    """
    Cria a tabela 'containers' caso ela ainda não exista.
    Isso é seguro de rodar toda vez que o programa inicia —
    "IF NOT EXISTS" evita apagar dados já existentes.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS containers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_container TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            cliente_navio TEXT,
            bloco TEXT,
            fileira TEXT,
            andar TEXT,
            status TEXT NOT NULL DEFAULT 'Aguardando',
            data_entrada TEXT NOT NULL,
            data_saida TEXT,
            observacoes TEXT
        )
    """)

    conexao.commit()
    conexao.close()
