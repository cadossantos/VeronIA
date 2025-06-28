# TODO & Pontos de Melhoria - VeronIA

Este documento serve como um backlog de tarefas, bugs e sugestões de refatoração para o projeto VeronIA. A ideia é que ele guie o desenvolvimento e aprimoramento contínuo da aplicação.

## 🐞 Bugs e Inconsistências

-   **[BUG] Conexões de Banco de Dados Ineficientes**: Em `db/db.py`, uma nova conexão com o PostgreSQL é criada e fechada para **cada** operação (ex: `salvar_mensagem`, `listar_conversas`). Isso é extremamente ineficiente e pode levar a problemas de performance e esgotamento de conexões. A função `get_conn()` é chamada repetidamente.
-   **[BUG] Redundância na Inicialização do DB**: Existem dois scripts que inicializam o banco de dados: `db/init_db.py` (standalone) e a função `init_database()` em `db/db.py`. Eles possuem esquemas ligeiramente diferentes (e.g., `TEXT` vs `VARCHAR`). Isso precisa ser unificado para evitar inconsistências.
-   **[INCONSISTÊNCIA] Gerenciamento de Dependências**: O projeto contém tanto um `pyproject.toml` (para Poetry) quanto um `requirements.txt`. As versões das bibliotecas entre eles são conflitantes (ex: `openai` está na `0.28.1` em um e `>=1.84.0` em outro). É crucial definir uma única fonte de verdade (preferencialmente `pyproject.toml`) e remover o arquivo obsoleto.

## 🚀 Melhorias de Funcionalidade

-   **[FUNCIONALIDADE] Upload de Arquivos**: A UI sugere a possibilidade de interagir com arquivos (PDF, CSV, etc.), mas a lógica (`carrega_arquivo`) está comentada ou incompleta. Implementar o fluxo de upload e processamento de documentos seria uma grande adição.
-   **[FUNCIONALIDADE] Feedback de Carregamento**: Adicionar indicadores de carregamento (`st.spinner`) mais granulares, especialmente durante a inicialização do modelo e o carregamento de conversas longas.
-   **[FUNCIONALIDADE] Deleção de Conversas**: Permitir que o usuário delete conversas antigas a partir da interface.
-   **[FUNCIONALIDADE] Busca em Conversas**: Implementar uma barra de busca para filtrar conversas pelo título.

## 🛠️ Refatoração e Qualidade de Código

-   **[REATORAÇÃO] Otimizar Gerenciamento de Conexão (Connection Pooling)**: Substituir o padrão atual de abrir/fechar conexões por um pool de conexões (ex: usando `psycopg.pool`). A conexão poderia ser estabelecida no início da sessão do usuário e reutilizada.
-   **[REATORAÇÃO] Desacoplar Lógica de DB da UI**: A função `get_conn()` em `db/db.py` chama `st.error()` e `st.stop()`, acoplando o módulo de banco de dados diretamente ao Streamlit. O ideal é que o módulo de DB levante exceções (`raise Exception`) e o `app.py` (a camada de UI) as capture e exiba a mensagem de erro para o usuário.
-   **[REATORAÇÃO] Otimizar Atualização de Título**: O título da conversa é atualizado no banco a cada nova mensagem após a primeira. A lógica pode ser otimizada para garantir que a atualização ocorra apenas uma vez, na primeira interação.
-   **[REATORAÇÃO] Cache de Modelos**: A função `carrega_modelo` é chamada a cada clique no botão "Iniciar Oráculo". Utilizar o cache do Streamlit (`@st.cache_resource`) para carregar o modelo apenas uma vez pode economizar tempo e recursos.
-   **[REATORAÇÃO] Cache de Conversas**: Da mesma forma, usar `@st.cache_data` para carregar a lista de conversas pode evitar chamadas desnecessárias ao banco de dados a cada recarregamento da página.
-   **[LIMPEZA] Remover Código Morto**: Remover as funções comentadas em `utils/configs.py` (`retorna_resposta_modelo`, `retorna_embedding`) e as variáveis globais não utilizadas (`tipo_arquivo`, `documento`).
-   **[LIMPEZA] Remover Expander de Debug**: Remover o `st.expander` de debug em `app.py` quando a aplicação for considerada estável.

## 📝 Documentação

-   **[DOCUMENTAÇÃO] Comentários no Código**: Adicionar mais docstrings e comentários em `app.py` para explicar a lógica de gerenciamento do `session_state` e o fluxo de renderização da página.
-   **[DOCUMENTAÇÃO] README.md**: Melhorar o `README.md` com instruções claras de como configurar o ambiente, as variáveis de ambiente (`.env`) e como executar a aplicação e os testes.

## ✅ Testes

-   **[TESTES] Implementar Testes Unitários**: Criar testes para as funções puras, como as de manipulação de dados em `db/db.py` (usando um banco de dados de teste).
-   **[TESTES] Implementar Testes de Integração**: Criar testes que simulem o fluxo do usuário, desde a configuração do modelo até o envio de uma mensagem.
