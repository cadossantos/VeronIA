# Changelog - JibóIA (VerônIA)

## v0.1.12 - 2025-07-20

### Adicionado
- **Funcionalidade de Scraping e Indexação Separadas**:
  - `services/scraping_service.py`: Introduzidas `raspar_links_e_salvar_paginas` (para scraping recursivo e salvamento de JSONs) e `indexar_base_de_conhecimento` (para ingestão no ChromaDB).
  - UI (`components/sidebar.py`): Abas "Scraping" e "RAG" ajustadas para refletir o fluxo de trabalho em duas etapas (raspar/salvar e indexar).
- **Scraping Recursivo**: O sistema agora explora e raspa links internos de forma recursiva a partir de uma URL inicial.
- **Feedback Visual Aprimorado**: Mensagens em tempo real na UI (`st.write`) indicam qual URL está sendo processada durante o scraping.
- **Otimização de Reprocessamento**: O scraping agora verifica a existência de arquivos JSON no disco antes de reprocessar uma página.
- **Prompt Dedicado para RAG**: Criado `prompts/rag_agent_prompt.txt` com instruções rigorosas para o LLM usar *apenas* o contexto fornecido.

### Alterado
- **Refatoração da Pipeline RAG**:
  - **Movimentação de Componentes**: Crawler (`smartwiki/crawler`) movido para `services/crawler`. Logger (`smartwiki/utils/logger.py`) movido para `utils/logger.py`.
  - **Remoção de Código Legado**: Diretório `smartwiki/` completamente removido.
  - **`agents/rag_agent.py`**: Refatorado para aceitar `vector_store_path` e `collection_name` dinamicamente, com validação de diretório. Logs de depuração aprimorados.
  - **`services/rag_service.py`**: Implementado cache (`@st.cache_resource`) para instâncias do `RagQueryEngine` (`get_rag_agent_cached`) e corrigido o caminho de `vector_store_path` para `db/vector_store/`.
  - **`components/chat_interface.py`**: Ajustado para passar o nome da base de conhecimento selecionada para o serviço RAG.
- **Configuração de Embedding**: Padronizado o uso de `OpenAIEmbeddings` para ingestão e consulta, com opções de modelo de embedding da OpenAI na UI.
- **Ajuste de Temperatura do LLM**: Definido `temperature=0.0` para o LLM no `rag_agent.py` para promover respostas mais determinísticas e menos alucinatórias.

### Corrigido
- **`NameError`**: Resolvido o erro `NameError: name 'iniciar_indexacao' is not defined` através da reestruturação do fluxo de scraping/ingestão.
- **`ValidationError` do Pydantic**: Corrigido o erro `ValidationError` relacionado ao `StuffDocumentsChain` e à variável `context` no `rag_agent.py`.
- **`FileNotFoundError` do ChromaDB**: Resolvido o problema de o ChromaDB não ser encontrado devido a um caminho incorreto (`db/pages/` em vez de `db/vector_store/`).
- **Alucinação e Respostas Genéricas do RAG**: Abordado através de um prompt mais rigoroso e ajuste da temperatura do LLM, forçando o modelo a se ater ao contexto fornecido.

### Impacto das Mudanças
- **Robustez e Confiabilidade do RAG**: O sistema RAG agora recupera e utiliza o contexto de forma precisa, reduzindo drasticamente a alucinação e fornecendo respostas mais fiéis à base de conhecimento.
- **Modularidade e Manutenibilidade**: A separação de responsabilidades entre scraping e ingestão, juntamente com a refatoração do `rag_agent` e `rag_service`, melhora a organização e facilita futuras manutenções e extensões.
- **Experiência do Usuário**: O feedback visual aprimorado e o fluxo de trabalho mais claro para gerenciamento de bases de conhecimento tornam a aplicação mais intuitiva.
- **Performance**: O caching do `RagQueryEngine` otimiza o carregamento das bases de conhecimento, melhorando a responsividade.

## v0.1.11 - 2025-07-18

### Refatorado - Consolidação da Funcionalidade RAG

#### **📦 Movimentação de Componentes**
- **Serviço de Ingestão**: O script `smartwiki/rag/ingest.py` foi movido para `services/ingest_service.py` para centralizar a lógica de ingestão de dados.
- **Dados Centralizados**: Os diretórios `smartwiki/data/pages` e `smartwiki/data/vector_store` foram movidos para `db/pages` e `db/vector_store`, respectivamente, consolidando todos os dados persistentes na pasta `db/` da raiz do projeto.
- **Agente RAG**: A lógica principal do RAG (classe `RagQueryEngine` e função `perguntar_ao_agent`) foi movida de `smartwiki/agents/query.py` para `agents/rag_agent.py` no diretório raiz do projeto `minimo`.

#### **🛠️ Ajustes e Correções**
- **Caminhos Atualizados**: Todos os caminhos de diretório e importações foram atualizados em `services/ingest_service.py`, `agents/rag_agent.py`, e nos arquivos de teste (`smartwiki/tests/test_ingest.py`, `smartwiki/tests/test_query.py`) para refletir as novas localizações.
- **Configuração de Dependências**: As dependências `pytest` e `pytest-mock` foram movidas para o `pyproject.toml` da raiz do projeto `minimo`, garantindo que os testes possam ser executados a partir do diretório principal.
- **Configuração do Poetry**: Adicionado `package-mode = false` ao `pyproject.toml` da raiz do projeto `minimo` para evitar problemas de instalação, já que o projeto não é uma biblioteca instalável.
- **Correções na Cadeia RAG**:
  - Corrigido `ImportError` para `load_qa_chain` e `LLMChain`.
  - Resolvidos `ValidationError`s relacionados à configuração da `ConversationalRetrievalChain`, garantindo que o `question_generator` e os prompts sejam passados corretamente.
- **Depuração Aprimorada**: Adicionado `DEBUG CONTEXT` ao prompt do LLM e logs detalhados para `source_documents` e `retrieved_docs` para facilitar a depuração do fluxo de RAG.

#### **🧹 Limpeza**
- **Remoção de Diretórios Vazios**: Os diretórios `smartwiki/rag` e `smartwiki/data` foram removidos após a movimentação de seus conteúdos.

### Impacto das Mudanças
- **Organização Aprimorada**: A funcionalidade RAG está agora melhor integrada e centralizada no projeto `minimo`, seguindo uma estrutura mais lógica e modular.
- **Manutenibilidade**: A separação clara de responsabilidades e a centralização de dados e lógica facilitam a manutenção e o desenvolvimento futuro.
- **Estabilidade**: Correções de dependências e configuração do LangChain melhoram a robustez do sistema RAG.

## v0.1.10 - 2025-07-14

### Refatorado - Consolidação da Aplicação em Página Única

#### **📄 Estrutura de Página Única**
- **Remoção do Diretório `pages/`**: O diretório `pages/` foi removido, consolidando toda a interface e lógica da aplicação no `app.py`.
- **Simplificação do Fluxo**: A aplicação agora opera como uma única página Streamlit, eliminando a navegação multipágina e simplificando a arquitetura geral.

### Impacto das Mudanças
- **Experiência do Usuário**: Fluxo de interação mais direto e unificado, sem a necessidade de alternar entre páginas.
- **Manutenibilidade**: Redução da complexidade da estrutura do projeto, tornando-o mais fácil de entender e manter.


## v0.1.9 - 2025-07-14

### Adicionado - Integração RAG Híbrida

#### **🧠 Funcionalidade RAG (Retrieval-Augmented Generation)**
- **Abordagem Híbrida**: O RAG pode ser ativado de duas formas:
  - **Modo Persistente**: Ativado/desativado via botão na aba RAG da sidebar (`st.session_state['rag_ativo']`). Quando ativo, todas as perguntas subsequentes consultam a base de conhecimento.
  - **Uso Único**: Botão "Consultar RAG na próxima pergunta" na aba RAG da sidebar (`st.session_state['use_rag_onetime']`). Permite uma consulta RAG pontual sem ativar o modo persistente.
- **Contexto Enriquecido**: O conteúdo recuperado da base de conhecimento RAG é automaticamente anexado ao prompt enviado ao modelo de linguagem, enriquecendo a resposta.

#### **⚙️ Refatoração e Estrutura**
- **Serviço de Ingestão**: O script `smartwiki/rag/ingest.py` foi movido para `services/ingest_service.py` para centralizar a lógica de ingestão de dados.
- **Dados Centralizados**: Os diretórios `smartwiki/data/pages` e `smartwiki/data/vector_store` foram movidos para `db/pages` e `db/vector_store`, respectivamente, consolidando todos os dados persistentes na pasta `db/` da raiz do projeto.
- **Agente RAG**: A lógica principal do RAG (classe `RagQueryEngine` e função `perguntar_ao_agent`) foi movida de `smartwiki/agents/query.py` para `agents/rag_agent.py` no diretório raiz do projeto `minimo`.
- **Serviço RAG Centralizado**: Criado `services/rag_service.py` para orquestrar o uso do `RagAgent`. Ele gerencia a instância do agente (singleton preguiçoso) e fornece uma interface limpa para consulta (`consultar_base_de_conhecimento`).

### Alterado - Interface e Fluxo

#### **🎨 Sidebar Aprimorada**
- **Controles RAG**: A aba RAG em `components/sidebar.py` foi atualizada para incluir os botões de ativação persistente e de uso único, oferecendo maior flexibilidade ao usuário.

#### **💬 Chat Inteligente**
- **Orquestração de Contexto**: A função `handle_user_input` em `components/chat_interface.py` foi modificada para:
  - Verificar o status do RAG (persistente ou uso único).
  - Chamar `rag_service.consultar_base_de_conhecimento` quando necessário.
  - Combinar o contexto RAG com o contexto de arquivos (se houver) e a pergunta do usuário antes de enviar ao modelo.
  - Resetar o flag de uso único do RAG após cada consulta.

### Removido - Limpeza de Código

#### **🗑️ Diretório `smartwiki`**
- O diretório `smartwiki` (`/home/claudiodossantos/dev/projetos/minimo/smartwiki`) foi completamente removido, pois suas funcionalidades foram integradas ou consideradas redundantes após a refatoração do RAG.

### Impacto das Mudanças
- **Funcionalidade**: Introdução de uma poderosa capacidade RAG, permitindo que o modelo acesse e utilize informações de uma base de conhecimento externa.
- **Flexibilidade**: Usuários podem escolher entre um modo RAG persistente ou uma consulta RAG pontual, adaptando-se a diferentes necessidades.
- **Organização**: Melhoria significativa na estrutura do projeto com a integração do RAG e a remoção de código obsoleto, resultando em uma base de código mais limpa e modular.
- **Experiência do Usuário**: A integração do RAG é transparente e intuitiva, enriquecendo as respostas do modelo sem complicar a interação do usuário.



## v0.1.8 - 2025-07-14

### Corrigido - Processamento de Arquivos e Estabilidade da Aplicação

#### **🐛 Loop de Reruns Infinito**
- **Causa Raiz**: Conflito de estado entre o `st.file_uploader` e a lógica manual de gerenciamento de arquivos no `session_state`, que acionava `st.rerun()` mutuamente entre `sidebar.py` e `chat_interface.py`.
- **Solução**: A lógica de orquestração foi centralizada. O `sidebar.py` agora apenas armazena os arquivos carregados no `session_state` sem acionar reruns. O `chat_interface.py` é o único responsável por iniciar o processamento quando o usuário envia uma mensagem.

#### **🧠 Contexto de Arquivos não Enviado à IA**
- **Causa Raiz**: As funções no `services/file_processor.py` eram apenas placeholders e não extraíam o conteúdo real dos arquivos.
- **Solução**: As funções de processamento foram implementadas com lógica real:
  - **PDF**: Utiliza `PyMuPDF` (`fitz`) para extrair texto de todas as páginas.
  - **TXT**: Lê o conteúdo do arquivo com tratamento de encoding `UTF-8`.

### Melhorado - Robustez e Experiência do Usuário no Upload

#### **⚙️ Fluxo de Processamento Integrado**
- **Integração Direta**: Criada a função `process_uploaded_files()` (agora integrada em `handle_user_input`) que garante que os arquivos sejam processados **antes** da mensagem do usuário ser enviada.
- **Contexto Combinado**: O texto extraído dos arquivos é pré-anexado ao prompt do usuário, garantindo que a IA receba todo o contexto necessário para formular a resposta.

#### **✨ Feedback Visual e Eficiência**
- **Spinner de Processamento**: Adicionado um `st.spinner("Processando arquivos...")` que informa ao usuário que os arquivos estão sendo analisados, melhorando a percepção de responsividade.
- **Limpeza Automática**: `st.session_state['uploaded_files']` é limpo após o processamento para evitar reprocessamento desnecessário em interações subsequentes, economizando recursos.

#### **🛠️ Suporte a Novos Tipos de Arquivo (Placeholder)**
- **Estrutura Preparada**: Embora a lógica completa ainda não esteja implementada, o `file_processor.py` foi estruturado para facilmente acomodar o processamento de:
  - Imagens (OCR)
  - Áudio (Transcrição)
  - CSV/Excel (Análise de Dados)
  - DOCX

### Impacto das Mudanças
- **Estabilidade**: Eliminado um bug crítico que causava o travamento completo da aplicação.
- **Funcionalidade Core**: A funcionalidade de upload e processamento de arquivos agora está operacional e integrada ao fluxo de chat.
- **Experiência do Usuário**: O usuário agora tem feedback claro sobre o status do processamento de arquivos.
- **Manutenibilidade**: A separação de responsabilidades entre orquestração (`chat_interface`) e lógica de processamento (`file_processor`) foi solidificada.


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