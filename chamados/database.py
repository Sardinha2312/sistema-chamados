"""Camada de acesso ao banco de dados (SQLite)."""

import sqlite3
from pathlib import Path

CAMINHO_PADRAO = Path(__file__).resolve().parent.parent / "chamados.db"

STATUS_VALIDOS = ("aberto", "em andamento", "fechado")
PRIORIDADES_VALIDAS = ("baixa", "media", "alta")


def conectar(caminho=CAMINHO_PADRAO):
    """Abre a conexão e garante que a tabela exista."""
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    criar_tabela(conexao)
    return conexao


def criar_tabela(conexao):
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS chamados (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo       TEXT    NOT NULL,
            descricao    TEXT,
            solicitante  TEXT    NOT NULL,
            prioridade   TEXT    NOT NULL DEFAULT 'media'
                         CHECK (prioridade IN ('baixa', 'media', 'alta')),
            status       TEXT    NOT NULL DEFAULT 'aberto'
                         CHECK (status IN ('aberto', 'em andamento', 'fechado')),
            criado_em    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            atualizado_em TEXT   NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
        """
    )
    conexao.commit()


def criar_chamado(conexao, titulo, solicitante, descricao="", prioridade="media"):
    titulo = titulo.strip()
    solicitante = solicitante.strip()
    if not titulo:
        raise ValueError("O título não pode ficar vazio.")
    if not solicitante:
        raise ValueError("Informe quem está abrindo o chamado.")
    if prioridade not in PRIORIDADES_VALIDAS:
        raise ValueError(f"Prioridade inválida. Use: {', '.join(PRIORIDADES_VALIDAS)}.")

    cursor = conexao.execute(
        "INSERT INTO chamados (titulo, descricao, solicitante, prioridade) VALUES (?, ?, ?, ?)",
        (titulo, descricao.strip(), solicitante, prioridade),
    )
    conexao.commit()
    return cursor.lastrowid


def listar_chamados(conexao, status=None):
    if status:
        if status not in STATUS_VALIDOS:
            raise ValueError(f"Status inválido. Use: {', '.join(STATUS_VALIDOS)}.")
        linhas = conexao.execute(
            "SELECT * FROM chamados WHERE status = ? ORDER BY id", (status,)
        ).fetchall()
    else:
        linhas = conexao.execute("SELECT * FROM chamados ORDER BY id").fetchall()
    return [dict(linha) for linha in linhas]


def buscar_chamado(conexao, chamado_id):
    linha = conexao.execute("SELECT * FROM chamados WHERE id = ?", (chamado_id,)).fetchone()
    return dict(linha) if linha else None


def atualizar_status(conexao, chamado_id, novo_status):
    if novo_status not in STATUS_VALIDOS:
        raise ValueError(f"Status inválido. Use: {', '.join(STATUS_VALIDOS)}.")
    cursor = conexao.execute(
        """
        UPDATE chamados
           SET status = ?, atualizado_em = datetime('now', 'localtime')
         WHERE id = ?
        """,
        (novo_status, chamado_id),
    )
    conexao.commit()
    if cursor.rowcount == 0:
        raise LookupError(f"Chamado #{chamado_id} não encontrado.")


def excluir_chamado(conexao, chamado_id):
    cursor = conexao.execute("DELETE FROM chamados WHERE id = ?", (chamado_id,))
    conexao.commit()
    if cursor.rowcount == 0:
        raise LookupError(f"Chamado #{chamado_id} não encontrado.")


def resumo_por_status(conexao):
    """Retorna a quantidade de chamados em cada status (relatório simples)."""
    linhas = conexao.execute(
        "SELECT status, COUNT(*) AS total FROM chamados GROUP BY status"
    ).fetchall()
    resumo = {status: 0 for status in STATUS_VALIDOS}
    for linha in linhas:
        resumo[linha["status"]] = linha["total"]
    return resumo
