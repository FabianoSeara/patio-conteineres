"""
operacoes.py
------------
Aqui ficam as regras de negócio: as funções que realmente fazem o
trabalho de cadastrar, buscar, atualizar e gerar estatísticas dos
containers no pátio.

Cada função abre sua própria conexão e fecha no final. Isso é uma boa
prática para programas pequenos: evita conexões "penduradas" abertas.
"""

import sqlite3
from datetime import datetime
import database

# Status possíveis de um container no pátio.
# Usar uma lista fixa evita erro de digitação (ex: "Armazenad" sem o "o").
STATUS_VALIDOS = ["Aguardando", "Armazenado", "Em Trânsito", "Carregado/Saída"]


def hoje():
    """Retorna a data/hora atual formatada como texto."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def cadastrar_container(numero, tipo, cliente_navio, bloco, fileira, andar, observacoes=""):
    """
    Insere um novo container no pátio.
    Retorna (True, mensagem) em caso de sucesso, ou (False, mensagem) em caso de erro.
    """
    conexao = database.conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO containers
                (numero_container, tipo, cliente_navio, bloco, fileira, andar, status, data_entrada, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, 'Aguardando', ?, ?)
        """, (numero.upper(), tipo, cliente_navio, bloco.upper(), fileira.upper(), andar, hoje(), observacoes))

        conexao.commit()
        return True, f"Container {numero.upper()} cadastrado com sucesso."

    except sqlite3.IntegrityError:
        # Isso acontece se o número do container já existir (campo UNIQUE)
        return False, f"Já existe um container cadastrado com o número {numero.upper()}."

    finally:
        # 'finally' garante que a conexão sempre fecha, mesmo se der erro
        conexao.close()


def listar_containers(status=None, bloco=None):
    """
    Lista containers, com filtros opcionais por status e/ou bloco.
    Se nenhum filtro for passado, lista todos.
    """
    conexao = database.conectar()
    cursor = conexao.cursor()

    query = "SELECT * FROM containers WHERE 1=1"
    parametros = []

    if status:
        query += " AND status = ?"
        parametros.append(status)

    if bloco:
        query += " AND bloco = ?"
        parametros.append(bloco.upper())

    query += " ORDER BY data_entrada DESC"

    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    conexao.close()
    return resultados


def buscar_container(numero):
    """Busca um único container pelo número. Retorna None se não encontrar."""
    conexao = database.conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM containers WHERE numero_container = ?", (numero.upper(),))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado


def atualizar_status(numero, novo_status):
    """Atualiza o status de um container (ex: de 'Aguardando' para 'Armazenado')."""
    if novo_status not in STATUS_VALIDOS:
        return False, f"Status inválido. Use um destes: {', '.join(STATUS_VALIDOS)}"

    conexao = database.conectar()
    cursor = conexao.cursor()

    # Se o novo status for "saída", registramos também a data de saída
    if novo_status == "Carregado/Saída":
        cursor.execute("""
            UPDATE containers SET status = ?, data_saida = ?
            WHERE numero_container = ?
        """, (novo_status, hoje(), numero.upper()))
    else:
        cursor.execute("""
            UPDATE containers SET status = ?
            WHERE numero_container = ?
        """, (novo_status, numero.upper()))

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()

    if linhas_afetadas == 0:
        return False, f"Container {numero.upper()} não encontrado."
    return True, f"Status do container {numero.upper()} atualizado para '{novo_status}'."


def atualizar_posicao(numero, bloco, fileira, andar):
    """Move um container para uma nova posição no pátio."""
    conexao = database.conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE containers SET bloco = ?, fileira = ?, andar = ?
        WHERE numero_container = ?
    """, (bloco.upper(), fileira.upper(), andar, numero.upper()))

    linhas_afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()

    if linhas_afetadas == 0:
        return False, f"Container {numero.upper()} não encontrado."
    return True, f"Container {numero.upper()} movido para Bloco {bloco.upper()}, Fileira {fileira.upper()}, Andar {andar}."


def estatisticas():
    """
    Gera um resumo do pátio: total de containers por status e por bloco.
    Retorna um dicionário com essas informações.
    """
    conexao = database.conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM containers")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT status, COUNT(*) as quantidade
        FROM containers
        GROUP BY status
    """)
    por_status = cursor.fetchall()

    cursor.execute("""
        SELECT bloco, COUNT(*) as quantidade
        FROM containers
        WHERE status != 'Carregado/Saída'
        GROUP BY bloco
        ORDER BY quantidade DESC
    """)
    por_bloco = cursor.fetchall()

    conexao.close()
    return {
        "total": total,
        "por_status": por_status,
        "por_bloco": por_bloco,
    }
