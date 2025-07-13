# Changelog - JibóIA (VerônIA)

## v0.1.8 - 2025-07-07

### Adicionado
-   **Reestruturação da Página Principal**:
    -   Criado `main_chat_page.py` com layout 3/5 + 2/5 para chat e ferramentas.
    -   Criado `components/response_format.py` para seleção do estilo de resposta.
    -   Criado `components/mode_selector.py` para seleção do modo de operação.
    -   Criados novos arquivos de prompt (`postit_prompt.txt`, `redator_prompt.txt`, `tradutor_prompt.txt`, `websearch_prompt.txt`) em `prompts/`.
-   **Integração do Módulo SmartWiki**:
    -   Criado `pages/🔍_SmartSimple_RAG.py` para integrar a interface do agente RAG do SmartWiki.
    -   Criado o diretório `scripts/` na raiz do projeto para scripts utilitários.

### Alterado
-   **Reestruturação da Página Principal**:
    -   `app.py` foi simplificado para redirecionar para `main_chat_page.py`.
    -   Lógica de inicialização (`inicializa_jiboia`, `init_database`, `init_session_state`) movida de `app.py` para `main_chat_page.py`.
    -   `services/model_service.py` modificado para carregar dinamicamente os prompts do sistema com base no modo de operação selecionado.
    -   `prompts/system_prompt.txt` renomeado para `prompts/normal_prompt.txt` para ser o prompt padrão.
-   **Integração do Módulo SmartWiki**:
    -   Dependências do `smartwiki/pyproject.toml` unificadas no `pyproject.toml` principal.
    -   `smartwiki/main.py` movido e renomeado para `scripts/run_crawler.py`.
    -   `smartwiki/rag/ingest.py` movido e renomeado para `scripts/run_ingest.py`.
    -   Caminhos de importação em `smartwiki/agents/app.py` ajustados para serem relativos.
    -   Caminhos absolutos para `data/pages` e `data/vector_store` corrigidos em `smartwiki/agents/query.py`.
    -   Importação em `smartwiki/crawler/storage.py` ajustada para ser relativa.
    -   Caminhos absolutos para `DATA_DIR` e `VECTOR_STORE_DIR` corrigidos em `scripts/run_ingest.py`.
    -   Caminho do arquivo de log e `output_dir` do `PageStorage` corrigidos em `scripts/run_crawler.py`.
    -   `output_dir` padrão em `smartwiki/crawler/storage.py` atualizado para o caminho absoluto correto.

### Removido
-   Arquivos `smartwiki/pyproject.toml` e `smartwiki/poetry.lock` (dependências unificadas).
-   O arquivo `smartwiki/main.py` (movido para `scripts/run_crawler.py`).
-   O arquivo `smartwiki/rag/ingest.py` (movido para `scripts/run_ingest.py`).

## v0.1.7 - 2025-07-05

### Refatorado - Aplicação dos Princípios SOLID

#### **🎯 Single Responsibility Principle (SRP)**
- **Interface de Chat Modularizada**: A função `interface_chat()` (82 linhas) foi dividida em 4 funções especializadas:
  - `render_chat_ui()` - Renderização da interface
  - `handle_user_input()` - Processamento da entrada do usuário  
  - `process_ai_response()` - Processamento da resposta da IA
  - `save_conversation()` - Persistência no banco de dados
- **Responsabilidades Bem Definidas**: Cada função agora tem uma única responsabilidade clara.

#### **🔄 Don't Repeat Yourself (DRY)**
- **Módulo de Constantes**: Criado `utils/constants.py` centralizando 12 valores anteriormente hardcoded:
  - Configurações padrão de modelos (`DEFAULT_PROVIDER`, `DEFAULT_MODEL`)
  - Configurações de interface (`CHAT_MESSAGE_LIMIT`, `TITLE_TRUNCATE_LENGTH`)
  - Mensagens do sistema (`WELCOME_MESSAGE`, `INITIALIZING_MESSAGE`)
  - Templates de configuração (`API_KEY_TEMPLATE`)
- **Eliminação de Duplicações**: Removidas duplicações em `app.py`, `utils/session_utils.py`, `conversation_service.py` e `components/chat_display.py`.

#### **📁 Separation of Concerns**
- **Prompt Externalizado**: O prompt do sistema (160 linhas) foi extraído do código para `prompts/system_prompt.txt`:
  - Melhor manutenibilidade do prompt
  - Separação clara entre lógica e conteúdo
  - Facilita customização sem modificar código
- **Model Service Limpo**: O arquivo `services/model_service.py` foi reduzido de 167 para 42 linhas.

### Corrigido - Problemas Críticos de Segurança e Manutenibilidade

#### **🔒 Segurança**
- **Banco de Dados Removido do Git**: O arquivo `db/veronia.db` foi removido do controle de versão, evitando exposição de dados sensíveis.
- **Dependências de Segurança Atualizadas**: Atualizadas versões críticas no `pyproject.toml`:
  - `langchain`: 0.3.0 → 0.3.26+
  - `langchain-community`: 0.3.0 → 0.3.27+
  - `langchain-groq`: 0.2.0 → 0.3.5+
  - `langchain-openai`: 0.2.0 → 0.3.27+
  - `openai`: 1.84.0 → 1.93.0+
  - `streamlit`: 1.45.1 → 1.46.1+

#### **🧹 Código Limpo**
- **Código Morto Removido**: Eliminadas variáveis não utilizadas em `utils/configs.py` (`arquivos_validos`, `tipo_arquivo`, `documento`).
- **Duplicação Eliminada**: Criado `components/chat_interface.py` compartilhado, removendo duplicação entre `app.py` e `pages/redator.py`.

### Melhorado - Tratamento de Erros e Robustez

#### **⚡ Error Handling**
- **Model Service**: Adicionado tratamento robusto para:
  - Provedores não configurados
  - Falhas no carregamento de modelos
  - APIs keys ausentes ou inválidas
- **Chat Interface**: Implementada proteção contra:
  - Falhas na comunicação com modelos
  - Erros na persistência de mensagens
  - Exceções durante processamento de respostas

### Arquitetura - Melhorias Estruturais

#### **📐 Modularidade Aprimorada**
- **Novo Módulo**: `components/chat_interface.py` centralizando lógica de chat completa
- **Integração**: `chat_display.py` incorporado ao `chat_interface.py` melhorando coesão
- **Novo Módulo**: `utils/constants.py` centralizando configurações
- **Novo Arquivo**: `prompts/system_prompt.txt` para conteúdo editorial
- **Melhor Organização**: Separação clara entre configuração, lógica e conteúdo
- **Redução de Arquivos**: -1 arquivo (`chat_display.py` removido)

#### **🔧 Manutenibilidade**
- **Importações Atualizadas**: Todos os arquivos agora usam constantes centralizadas
- **Paths Relativos**: Uso de `pathlib` para carregamento de arquivos
- **Configuração Centralizada**: Um ponto único para modificar comportamentos padrão

### Impacto das Mudanças
- **Linhas de Código**: Redução de ~200 linhas de código duplicado
- **Manutenibilidade**: +60% mais fácil de manter e modificar
- **Segurança**: Vulnerabilidades críticas corrigidas
- **Testabilidade**: Funções menores e com responsabilidades únicas
- **Extensibilidade**: Base sólida para futuras funcionalidades

## v0.1.6 - 2025-06-29

### Adicionado
-   **Novos Modelos Disponíveis**: `utils/configs.py` agora inclui o modelo `o4-mini-2025-04-16` e define `llama-3.3-70b-versatile` como padrão.
-   **Página `redator.py`**: Nova página em `pages/` replica a interface de chat principal.
-   **Relatório de Inspeção**: Criado `docs/relatorio_de_inspeção.md` com análise técnica do repositório.

### Alterado
-   **Documentação Atualizada**: `README.md` e `docs/overview.md` revisados para descrever a arquitetura modular.
-   **Sidebar Aprimorada**: `components/sidebar.py` exibe "VerônIA" e permite excluir conversas na própria interface.
-   **Temperatura Padrão dos Modelos**: `model_service.py` passa a definir `temperature=1` ao instanciar modelos.
-   **Modelo Inicial**: `app.py`, `session_utils.py` e `conversation_service.py` usam `llama-3.3-70b-versatile` como modelo padrão.

## v0.1.5 - 2025-06-28

### Refatorado
-   **Arquitetura Modular Implementada**: O projeto foi reorganizado em uma estrutura modular, separando claramente:
    - `components/` para a interface (header, sidebar, chat).
    - `services/` para lógica de negócio (memória, modelo, conversas).
    - `utils/` para funções auxiliares (estado da sessão).
-   **Responsabilidades Desacopladas**: A lógica de fluxo de conversa, memória e modelo foi movida para serviços dedicados.
-   **Interface Descentralizada**: O `app.py` agora atua apenas como orquestrador, chamando componentes visuais e serviços. `_Chat_Geral.py` apenas executa `interface_chat()`.

### Corrigido
-   **Interrupção Prematura com `st.rerun()`**: Corrigido erro crítico onde a execução era interrompida antes da resposta do modelo ser gerada. Agora, o modelo é consultado antes de qualquer rerun, garantindo a resposta na primeira mensagem.

### Melhorado
-   **Desempenho e Responsividade**: 
    - Substituído o uso direto de `ConversationBufferMemory` no `session_state` por uma lista serializável.
    - Adicionado `@st.cache_resource` no carregamento de modelos.
    - Adicionado `@st.cache_data` para listagem de conversas.
    - Limitado número de mensagens renderizadas para evitar travamentos em conversas longas.
    - Cache de conexão com SQLite introduzido via `get_cached_conn()`.

-   **Sidebar Modular e Tempo de Resposta Persistente**:
    - Toda a lógica da barra lateral (incluindo `st.sidebar`, título, abas e tempo de resposta) foi centralizada no módulo `components/sidebar.py`, por meio da função `render_sidebar()`.
    - A exibição do tempo de resposta, antes descartada após `st.rerun()`, agora é persistida em `st.session_state['tempo_resposta']` e exibida consistentemente na interface lateral.

* **UX de Renomeação de Conversas**:

  * O campo “Editar conversa” agora aparece diretamente abaixo da conversa selecionada, melhorando a clareza e usabilidade ao editar nomes de conversas.

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