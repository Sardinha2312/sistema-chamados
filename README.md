# 🎫 Sistema de Chamados

Sistema simples de **controle de chamados de suporte técnico (help desk)**, feito em **Python** com banco de dados **SQLite** e interface no terminal.

O objetivo do projeto é simular o fluxo básico de um setor de suporte: um usuário abre um chamado, a equipe acompanha e atualiza o andamento até o chamado ser fechado.

## Funcionalidades

- Abrir chamado (título, descrição, solicitante e prioridade)
- Listar todos os chamados ou filtrar por status
- Atualizar o status: `aberto` → `em andamento` → `fechado`
- Ver detalhes de um chamado (incluindo data de criação e última atualização)
- Excluir chamado (com confirmação)
- Resumo com a quantidade de chamados por status
- Validação de entradas (título obrigatório, status e prioridade válidos)

## Tecnologias

- Python 3 (somente biblioteca padrão, sem dependências externas)
- SQLite (`sqlite3`)
- SQL (CREATE, INSERT, SELECT, UPDATE, DELETE, GROUP BY)

## Como rodar

Pré-requisito: Python 3.10 ou superior.

```bash
git clone https://github.com/Sardinha2312/sistema-chamados.git
cd sistema-chamados
python main.py
```

O banco `chamados.db` é criado automaticamente na primeira execução.

## Estrutura do projeto

```
sistema-chamados/
├── chamados/
│   ├── __init__.py
│   └── database.py     # acesso ao banco (SQL) e regras de validação
├── main.py             # menu e interação no terminal
└── README.md
```

A lógica de banco fica separada da interface: `database.py` não sabe nada de menu ou `input()`, o que deixa o código mais organizado e facilita trocar a interface no futuro.

## Exemplo de uso

```
========== SISTEMA DE CHAMADOS ==========
1 - Abrir novo chamado
2 - Listar todos os chamados
...
ID   TÍTULO                          SOLICITANTE       PRIORIDADE  STATUS
---------------------------------------------------------------------------------
1    Impressora não liga             Ana               alta        em andamento
2    Sem internet                    Bruno             media       aberto
```

## Próximos passos

- [ ] Exportar chamados para CSV
- [ ] Registrar histórico de mudanças de status
- [ ] Criar uma API REST (Flask/FastAPI) sobre a mesma camada de banco

---

Desenvolvido por **Lucas Sardinha** — estudante de Sistemas de Informação (UVV).
