"""
main.py
-------
Ponto de entrada do programa. É aqui que o usuário interage, através
de um menu no terminal. Esse arquivo só cuida da "conversa" com o
usuário (mostrar menu, ler o que ele digita) — quem faz o trabalho de
verdade são as funções em operacoes.py.

Para rodar:
    python3 main.py
"""

import database
import operacoes


def limpar_tela():
    print("\n" * 2)


def pausar():
    input("\nPressione ENTER para continuar...")


def exibir_menu():
    print("=" * 50)
    print("   SISTEMA DE CONTROLE DE PÁTIO DE CONTÊINERES")
    print("=" * 50)
    print("1. Cadastrar novo container")
    print("2. Listar containers")
    print("3. Buscar container por número")
    print("4. Atualizar status de um container")
    print("5. Mover container (bloco/fileira/andar)")
    print("6. Estatísticas do pátio")
    print("0. Sair")
    print("=" * 50)


def tela_cadastrar():
    print("\n--- CADASTRAR NOVO CONTAINER ---")
    numero = input("Número do container (ex: MSKU1234567): ").strip()
    tipo = input("Tipo (ex: 20' Dry, 40' Reefer, 40' HC): ").strip()
    cliente_navio = input("Cliente / Navio: ").strip()
    bloco = input("Bloco (ex: A, B, C): ").strip()
    fileira = input("Fileira (ex: 01, 02): ").strip()
    andar = input("Andar (ex: 1, 2, 3): ").strip()
    observacoes = input("Observações (opcional): ").strip()

    if not numero or not tipo or not bloco:
        print("\n⚠ Número, tipo e bloco são obrigatórios.")
        return

    sucesso, mensagem = operacoes.cadastrar_container(
        numero, tipo, cliente_navio, bloco, fileira, andar, observacoes
    )
    simbolo = "✔" if sucesso else "⚠"
    print(f"\n{simbolo} {mensagem}")


def imprimir_container(c):
    print("-" * 50)
    print(f"Número:      {c['numero_container']}")
    print(f"Tipo:        {c['tipo']}")
    print(f"Cliente/Navio: {c['cliente_navio']}")
    print(f"Posição:     Bloco {c['bloco']} / Fileira {c['fileira']} / Andar {c['andar']}")
    print(f"Status:      {c['status']}")
    print(f"Entrada:     {c['data_entrada']}")
    print(f"Saída:       {c['data_saida'] or '-'}")
    if c["observacoes"]:
        print(f"Obs:         {c['observacoes']}")


def tela_listar():
    print("\n--- LISTAR CONTAINERS ---")
    print("Filtrar por status? (deixe em branco pra listar todos)")
    print(f"Opções: {', '.join(operacoes.STATUS_VALIDOS)}")
    status = input("Status: ").strip()
    status = status if status else None

    resultados = operacoes.listar_containers(status=status)

    if not resultados:
        print("\nNenhum container encontrado.")
        return

    print(f"\n{len(resultados)} container(s) encontrado(s):")
    for c in resultados:
        imprimir_container(c)
    print("-" * 50)


def tela_buscar():
    print("\n--- BUSCAR CONTAINER ---")
    numero = input("Número do container: ").strip()
    resultado = operacoes.buscar_container(numero)

    if resultado is None:
        print(f"\n⚠ Container {numero.upper()} não encontrado.")
        return

    print()
    imprimir_container(resultado)
    print("-" * 50)


def tela_atualizar_status():
    print("\n--- ATUALIZAR STATUS ---")
    numero = input("Número do container: ").strip()
    print(f"Status disponíveis: {', '.join(operacoes.STATUS_VALIDOS)}")
    novo_status = input("Novo status: ").strip()

    sucesso, mensagem = operacoes.atualizar_status(numero, novo_status)
    simbolo = "✔" if sucesso else "⚠"
    print(f"\n{simbolo} {mensagem}")


def tela_mover():
    print("\n--- MOVER CONTAINER ---")
    numero = input("Número do container: ").strip()
    bloco = input("Novo bloco: ").strip()
    fileira = input("Nova fileira: ").strip()
    andar = input("Novo andar: ").strip()

    sucesso, mensagem = operacoes.atualizar_posicao(numero, bloco, fileira, andar)
    simbolo = "✔" if sucesso else "⚠"
    print(f"\n{simbolo} {mensagem}")


def tela_estatisticas():
    print("\n--- ESTATÍSTICAS DO PÁTIO ---")
    dados = operacoes.estatisticas()

    print(f"\nTotal de containers cadastrados: {dados['total']}")

    print("\nPor status:")
    for linha in dados["por_status"]:
        print(f"  {linha['status']:<20} {linha['quantidade']}")

    print("\nOcupação por bloco (containers ainda no pátio):")
    if not dados["por_bloco"]:
        print("  Nenhum container ativo no pátio.")
    for linha in dados["por_bloco"]:
        print(f"  Bloco {linha['bloco']:<10} {linha['quantidade']}")


def main():
    # Garante que o banco de dados e a tabela existem antes de começar
    database.criar_tabela()

    while True:
        limpar_tela()
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            tela_cadastrar()
            pausar()
        elif opcao == "2":
            tela_listar()
            pausar()
        elif opcao == "3":
            tela_buscar()
            pausar()
        elif opcao == "4":
            tela_atualizar_status()
            pausar()
        elif opcao == "5":
            tela_mover()
            pausar()
        elif opcao == "6":
            tela_estatisticas()
            pausar()
        elif opcao == "0":
            print("\nAté logo! 👋")
            break
        else:
            print("\n⚠ Opção inválida.")
            pausar()


if __name__ == "__main__":
    main()
