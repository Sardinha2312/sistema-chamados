"""Interface de terminal do Sistema de Chamados."""

from chamados import database as db

MENU = """
========== SISTEMA DE CHAMADOS ==========
1 - Abrir novo chamado
2 - Listar todos os chamados
3 - Listar chamados por status
4 - Atualizar status de um chamado
5 - Ver detalhes de um chamado
6 - Excluir chamado
7 - Resumo por status
0 - Sair
=========================================
"""


def ler_opcao(mensagem, opcoes):
    """Pede ao usuário que escolha uma das opções numeradas."""
    for i, opcao in enumerate(opcoes, start=1):
        print(f"  {i} - {opcao}")
    while True:
        escolha = input(mensagem).strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return opcoes[int(escolha) - 1]
        print("Opção inválida, tente novamente.")


def ler_id(mensagem="ID do chamado: "):
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit():
            return int(valor)
        print("Digite um número válido.")


def imprimir_tabela(chamados):
    if not chamados:
        print("\nNenhum chamado encontrado.")
        return
    print(f"\n{'ID':<5}{'TÍTULO':<32}{'SOLICITANTE':<18}{'PRIORIDADE':<12}{'STATUS':<14}")
    print("-" * 81)
    for c in chamados:
        titulo = c["titulo"] if len(c["titulo"]) <= 30 else c["titulo"][:27] + "..."
        print(
            f"{c['id']:<5}{titulo:<32}{c['solicitante'][:16]:<18}"
            f"{c['prioridade']:<12}{c['status']:<14}"
        )


def abrir_chamado(conexao):
    print("\n--- Novo chamado ---")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    solicitante = input("Solicitante: ")
    print("Prioridade:")
    prioridade = ler_opcao("Escolha: ", list(db.PRIORIDADES_VALIDAS))
    novo_id = db.criar_chamado(conexao, titulo, solicitante, descricao, prioridade)
    print(f"\nChamado #{novo_id} aberto com sucesso!")


def listar_por_status(conexao):
    print("\nFiltrar por qual status?")
    status = ler_opcao("Escolha: ", list(db.STATUS_VALIDOS))
    imprimir_tabela(db.listar_chamados(conexao, status))


def mudar_status(conexao):
    chamado_id = ler_id()
    chamado = db.buscar_chamado(conexao, chamado_id)
    if not chamado:
        print(f"Chamado #{chamado_id} não encontrado.")
        return
    print(f"Status atual: {chamado['status']}")
    print("Novo status:")
    novo = ler_opcao("Escolha: ", list(db.STATUS_VALIDOS))
    db.atualizar_status(conexao, chamado_id, novo)
    print(f"Chamado #{chamado_id} atualizado para '{novo}'.")


def ver_detalhes(conexao):
    chamado = db.buscar_chamado(conexao, ler_id())
    if not chamado:
        print("Chamado não encontrado.")
        return
    print()
    for campo, valor in chamado.items():
        print(f"{campo.replace('_', ' ').capitalize():<15}: {valor}")


def excluir(conexao):
    chamado_id = ler_id()
    confirmacao = input(f"Confirma a exclusão do chamado #{chamado_id}? (s/n): ")
    if confirmacao.strip().lower() == "s":
        db.excluir_chamado(conexao, chamado_id)
        print("Chamado excluído.")
    else:
        print("Exclusão cancelada.")


def mostrar_resumo(conexao):
    resumo = db.resumo_por_status(conexao)
    print("\n--- Resumo por status ---")
    for status, total in resumo.items():
        print(f"{status:<15}: {total}")
    print(f"{'total':<15}: {sum(resumo.values())}")


ACOES = {
    "1": abrir_chamado,
    "2": lambda con: imprimir_tabela(db.listar_chamados(con)),
    "3": listar_por_status,
    "4": mudar_status,
    "5": ver_detalhes,
    "6": excluir,
    "7": mostrar_resumo,
}


def main():
    conexao = db.conectar()
    try:
        while True:
            print(MENU)
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "0":
                print("Até logo!")
                break
            acao = ACOES.get(opcao)
            if not acao:
                print("Opção inválida.")
                continue
            try:
                acao(conexao)
            except (ValueError, LookupError) as erro:
                print(f"Erro: {erro}")
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
