# Changelog - VeronIA

## v0.1.1 - 2025-06-27

### Alterado

-   **Migração de Banco de Dados**: O backend de persistência de dados foi migrado do PostgreSQL para o **SQLite**.
    -   Novo módulo `db/db_sqlite.py` criado, replicando a interface de `db.py` com `sqlite3`.
    -   `app.py` atualizado para utilizar `db_sqlite.py`.
    -   O arquivo do banco de dados `veronia.db` agora é criado e gerenciado automaticamente dentro da pasta `db/`.
    -   Removida a dependência de um servidor PostgreSQL externo, simplificando o setup e a execução local do projeto.

## v0.1.0 - 2025-06-27

### Adicionado

-   **O Início de Tudo!** O desenvolvedor finalmente conseguiu dedicar tempo para estruturar e documentar o projeto. Este marco representa a fundação do VeronIA, com o objetivo de criar uma ferramenta de chat robusta e extensível.
-   **Documentação Abrangente**: Foram criados múltiplos documentos para explicar o projeto:
    -   `README.md`: Guia de instalação e execução.
    -   `docs/overview.md`: Visão geral técnica da arquitetura.
    -   `docs/aula_projeto.md`: Uma análise didática de cada módulo do código.
    -   `docs/todo.md`: Um backlog de tarefas e melhorias.
-   **Licenciamento**: O projeto foi licenciado sob a **GNU General Public License v3 (GPLv3)** para garantir que ele e seus derivados permaneçam software livre.
-   **Documentação no Código**: Todas as funções e módulos principais (`app.py`, `db/db.py`, `utils/configs.py`) foram documentados com docstrings detalhadas.
-   **Controle de Versão**: Um arquivo `.gitignore` coeso foi adicionado para manter o repositório limpo.
-   **Funcionalidade Principal**: Implementada a estrutura inicial da aplicação com Streamlit, permitindo a seleção de modelos (OpenAI, Groq, Ollama), gerenciamento de conversas e persistência em banco de dados PostgreSQL.