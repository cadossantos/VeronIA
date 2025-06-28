# Changelog - JibóIA (VerônIA)

## v0.1.4 - 2025-06-28

### Adicionado
-   **Inicialização Automática**: Implementada função `inicializa_jiboia()` que carrega automaticamente o modelo `Groq - llama-3.1-8b-instant`.
-   **Página Principal Unificada**: O `app.py` agora serve como página principal da aplicação com interface de chat completa integrada.
-   **Experiência Sem Configuração**: Usuários podem começar a conversar imediatamente sem precisar configurar modelo ou criar conversas manualmente.
-   **Cabeçalho Fixo do Modelo**: Adicionado cabeçalho fixo no topo da interface com o nome do modelo de IA atualmente em uso, usando CSS customizado e layout responsivo centralizado.

### Alterado
-   **Nome da Aplicação**: Renomeada de "VeronIA" para "JibóIA" refletindo a nova identidade do projeto.
-   **Fluxo de Inicialização**: Removidos avisos de configuração obrigatória, substituídos por mensagens informativas sobre inicialização automática.
-   **Interface de Usuário**: Otimizada para indicar que o sistema está pronto para uso imediato. Alguns elementos foram reposicionados para melhorar a experiência e usabilidade da aplicação.

### Corrigido
-   **Bug de Inicialização**: Resolvido problema onde aplicação quebrava ao abrir sem modelo ou memória configurados.
-   **UX de Primeiro Acesso**: Eliminada necessidade de cliques em "Iniciar Oráculo" e "Nova Conversa".
-   **Criação Redundante de Conversas**: A cada nova inicialização da aplicação, uma nova conversa vazia é criada automaticamente, mesmo que o usuário já tenha uma conversa ativa. Isso gera acúmulo desnecessário no banco e será corrigido em versões futuras.
-   **Interação inicial**:  Se iniciado um conversa diretamente do input da, o llm resposnde mas não gera nova conversa. Precisa definir que uma nova mensagem for criada se uma mensagem for enviada.

## v0.1.3 - 2025-06-29

### Corrigido
-   Evitada a exceção `AttributeError` quando nenhuma conversa está selecionada; `_Chat_Geral.py` interrompe a execução ao detectar memória ausente.
-   Sidebar passa a renderizar corretamente, com inicialização garantida e uso de `st.sidebar.tabs`.

### Alterado
-   Documentação atualizada para refletir o uso exclusivo do SQLite, removendo instruções antigas sobre PostgreSQL.
-   `pyproject.toml` agora declara a mesma licença (GPLv3) do arquivo LICENSE.
-   Dependências centralizadas apenas no `pyproject.toml`; `requirements.txt` não é mais necessário.



## v0.1.2 - 2025-06-28

### Bugs Conhecidos

-   **Sidebar não renderiza na página _Chat_Geral.py**: Após a migração para a arquitetura multipage, a sidebar contendo as abas "Conversas" e "Config" não está sendo renderizada corretamente na página `pages/_Chat_Geral.py`. Isso impede o usuário de selecionar modelos e iniciar/gerenciar conversas, tornando a página inoperável. A causa provável está na forma como o Streamlit lida com sidebars em páginas ou na inicialização do `st.session_state` para componentes da sidebar.

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