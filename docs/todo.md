# TODO & Pontos de Melhoria - VeronIA

Este documento serve como um backlog de tarefas, bugs e sugestões de refatoração para o projeto VeronIA. A ideia é que ele guie o desenvolvimento e aprimoramento contínuo da aplicação, agora com foco na transformação para uma plataforma multi-agente.

## 🎯 Visão Geral do Projeto (Baseado no PRD)

O VeronIA está evoluindo de um chat único para uma **plataforma multi-agente**, onde cada "página" ou "especialista" terá:
- Prompt system específico
- Ferramentas (tools) especializadas
- Comportamento de memória personalizado
- Interface adaptada ao contexto

Os agentes planejados incluem: Chat Geral, RP (Redator Profissional), Sumarizador, Especialista SmartSimple e Brainstorming.

## 🐞 Bugs e Inconsistências


Travamentos

1. Uso direto e constante de ConversationBufferMemory no session_state
Ela mantém todas as mensagens da conversa na RAM, o que:

Aumenta o tempo de serialização no session_state.

Piora conforme o histórico cresce.

⚠️ Streamlit **reescreve o session_state a cada renderização**, e objetos complexos (como ConversationBufferMemory) não são otimizados para isso.

2. Ausência de @st.cache_resource ou @st.cache_data
Toda vez que você carrega modelos ou lista conversas, isso é refeito do zero.

**Falta de cache no carregamento:**

Modelos (ChatOpenAI, etc.)

Dados do banco (listar_conversas)

PromptTemplate

3. Re-renderizações completas
Usar chamadas st.rerun() em momentos errados (ou em on_click) pode causar renderizações duplas ou inesperadas.

Com interface grande, isso pesa.

4. Banco de dados SQLite sem persistência de conexão
Cada operação com get_conn() cria uma nova conexão.

Isso pode ser muito lento, especialmente em sistemas de arquivo com I/O mais fraco.

5. Carga visual acumulada
Se você exibe muitas mensagens (memoria.buffer_as_messages) como st.chat_message(...), o DOM pode ficar grande demais.

Streamlit re-renderiza tudo toda vez. Se você tem 200 mensagens, ele repinta 200 componentes sempre.

✅ Possíveis soluções práticas (curto prazo)
- A. Evitar guardar ConversationBufferMemory diretamente
python
Copiar
Editar
# Em vez de:
st.session_state['memoria'] = ConversationBufferMemory(...)

# Use algo como:
st.session_state['historico'] = [{'role': 'user', 'content': '...'}, ...]
Ou serialize apenas o .buffer e reconstrua a memória quando necessário.

- B. Usar @st.cache_resource no carregamento do modelo
Exemplo:

python
Copiar
Editar
@st.cache_resource
def carregar_modelo_cache(provedor, modelo):
    # lógica de carrega_modelo
    return chain
C. Usar @st.cache_data para listar_conversas()
python
Copiar
Editar
@st.cache_data
def listar_conversas_cached():
    return listar_conversas()
D. Limitar visualização do histórico
Mostre só as últimas 10 mensagens:

python
Copiar
Editar
mensagens = memoria.buffer_as_messages[-10:]
E. Unificar conexão SQLite por sessão
No db_sqlite.py, você pode fazer:

python
Copiar
Editar
@st.cache_resource
def get_cached_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
E alterar o código para usar get_cached_conn() quando possível.

🛠️ Solução ideal (médio prazo)
Trocar ConversationBufferMemory por estrutura mais leve (como uma lista simples).

Separar interface de lógica:

Módulo para exibição (components/)

Módulo para memória (services/memory_service.py)

Controlar crescimento do st.session_state

Considerar SessionStateProxy externo via st.session_state['x'] = None com reconstrução baseada no banco

Avaliar LangChain com ConversationSummaryMemory para não reter tudo na RAM

-   **[BUG] Sidebar não renderiza na página _Chat_Geral.py**: Após a migração para a arquitetura multipage, a sidebar contendo as abas "Conversas" e "Config" não está sendo renderizada corretamente na página `pages/_Chat_Geral.py`. Isso impede o usuário de selecionar modelos e iniciar/gerenciar conversas, tornando a página inoperável. A causa provável está na forma como o Streamlit lida com sidebars em páginas ou na inicialização do `st.session_state` para componentes da sidebar.


-   **[BUG] Conexões de Banco de Dados Ineficientes**: Em `db/db.py` (legado PostgreSQL) e potencialmente no `db/db_sqlite.py`, uma nova conexão com o banco de dados é criada e fechada para **cada** operação (ex: `salvar_mensagem`, `listar_conversas`). Isso é extremamente ineficiente e pode levar a problemas de performance e esgotamento de conexões. A função `get_conn()` é chamada repetidamente.

-   **[INCONSISTÊNCIA] Gerenciamento de Dependências**: O projeto contém tanto um `pyproject.toml` (para Poetry) quanto um `requirements.txt`. As versões das bibliotecas entre eles são conflitantes (ex: `openai` está na `0.28.1` em um e `>=1.84.0` em outro). É crucial definir uma única fonte de verdade (preferencialmente `pyproject.toml`) e remover o arquivo obsoleto.

## 🚀 Melhorias de Funcionalidade (Por Agente e Global)

### Funcionalidades Globais
-   **[FUNCIONALIDADE] Home/Dashboard**: Criar uma página inicial que sirva como hub para os diferentes agentes.
-   **[FUNCIONALIDADE] Configurações Globais**: Implementar uma seção para configurações gerais, incluindo:
    -   **Perfil Personalizado**: Gerenciamento de um "Contexto Global" do usuário (nome, profissão, contexto adicional, estilo de comunicação) para injeção nos prompts dos agentes.
    -   **Configurações de Modelo**: Escolha de modelo global ou por agente.
    -   **Dados e Privacidade**: Opções para limpar contexto e avisos sobre dados sensíveis.
-   **[FUNCIONALIDADE] Feedback de Carregamento**: Adicionar indicadores de carregamento (`st.spinner`) mais granulares, especialmente durante a inicialização do modelo e o carregamento de conversas longas.
-   **[FUNCIONALIDADE] Deleção de Conversas**: Permitir que o usuário delete conversas antigas a partir da interface.
-   **[FUNCIONALIDADE] Busca em Conversas**: Implementar uma barra de busca para filtrar conversas pelo título.

### Agentes Específicos
-   **[CHAT GERAL] Web Search Integration**: Implementar ferramenta de pesquisa na internet para o agente de Chat Geral.
-   **[RP] Ferramentas de Escrita Profissional**:
    -   Templates de email (formal, comercial, follow-up).
    -   Análise de tom e estilo.
    -   Sugestões de melhoria de escrita.
-   **[SUMARIZADOR] OCR Avançado e Processamento de Imagens**:
    -   Integração com Nanonets-OCR-s (via HuggingFace) para extração de texto de anotações manuscritas.
    -   Funcionalidade de upload de imagens/fotos.
    -   Estruturação automática de texto extraído e exportação de resumos organizados.
-   **[ESPECIALISTA SMARTSIMPLE] RAG e Base de Conhecimento**:
    -   Implementar Retrieval-Augmented Generation (RAG) para acesso à documentação técnica.
    -   Busca semântica em documentação e geração de exemplos práticos.
-   **[BRAINSTORMING] Ferramentas Criativas**:
    -   Técnicas de criatividade estruturadas.
    -   Geração de variações e derivações de ideias.
    -   Organização hierárquica de ideias e exportação de mapas mentais.

## 🛠️ Refatoração e Qualidade de Código

-   **[ARQUITETURA] Refatorar para Arquitetura Multipage**: Reorganizar o código para usar o sistema de páginas do Streamlit (`pages/` diretório).
-   **[ARQUITETURA] Criar Classe Base `Agent`**: Desenvolver uma classe base para agentes que encapsule lógica comum (prompt system, gerenciamento de memória, ferramentas).
-   **[ARQUITETURA] Migrar Chat Atual para Nova Estrutura**: Adaptar o `app.py` existente para se tornar o `pages/💬_Chat_Geral.py` e seguir a nova estrutura de agentes.
-   **[ARQUITETURA] Organização de Diretórios**: Implementar a estrutura de diretórios proposta no PRD (`agents/`, `tools/`, `prompts/`, `utils/session_manager.py`, `utils/ui_components.py`).
-   **[MEMÓRIA] Gerenciamento de Memória Avançado**:
    -   Implementar estratégias de memória mais eficientes (ex: `ConversationSummaryBufferMemory`, janela de mensagens, memória híbrida com RAG).
    -   Garantir que a memória não seja reiniciada ao trocar o modelo.
    -   Desenvolver um `session_manager.py` para gerenciar o estado entre as páginas e a memória dos agentes.
-   **[DB] Otimizar Gerenciamento de Conexão**: Embora o SQLite seja mais leve, o padrão de abrir/fechar conexão para cada operação ainda pode ser otimizado. Considerar o uso de um pool de conexões ou gerenciar a conexão de forma mais centralizada (ex: usando `sqlite3.Connection` com `with` statement).
-   **[DB] Desacoplar Lógica de DB da UI**: A função `get_conn()` em `db/db.py` (legado) e `db/db_sqlite.py` não deve chamar `st.error()` e `st.stop()`. O ideal é que o módulo de DB levante exceções (`raise Exception`) e o `app.py` (a camada de UI) as capture e exiba a mensagem de erro para o usuário.
-   **[OTIMIZAÇÃO] Otimizar Atualização de Título**: O título da conversa é atualizado no banco a cada nova mensagem após a primeira. A lógica pode ser otimizada para garantir que a atualização ocorra apenas uma vez, na primeira interação.
-   **[OTIMIZAÇÃO] Cache de Modelos**: A função `carrega_modelo` é chamada a cada clique no botão "Iniciar Oráculo". Utilizar o cache do Streamlit (`@st.cache_resource`) para carregar o modelo apenas uma vez pode economizar tempo e recursos.
-   **[OTIMIZAÇÃO] Cache de Conversas**: Da mesma forma, usar `@st.cache_data` para carregar a lista de conversas pode evitar chamadas desnecessárias ao banco de dados a cada recarregamento da página.
-   **[LIMPEZA] Remover Código Morto**: Remover as funções comentadas em `utils/configs.py` (`retorna_resposta_modelo`, `retorna_embedding`) e as variáveis globais não utilizadas (`tipo_arquivo`, `documento`).
-   **[LIMPEZA] Remover Expander de Debug**: Remover o `st.expander` de debug em `app.py` quando a aplicação for considerada estável.

## ✅ Testes

-   **[TESTES] Implementar Testes Unitários**: Criar testes para as funções puras, como as de manipulação de dados em `db/db_sqlite.py` (usando um banco de dados de teste).
-   **[TESTES] Implementar Testes de Integração**: Criar testes que simulem o fluxo do usuário, desde a configuração do modelo até o envio de uma mensagem, e para a interação entre os diferentes agentes.

## 🗓️ Fases de Implementação (Baseado no PRD)

### Fase 1: Infraestrutura
-   [ ] Refatorar código atual para arquitetura multipage.
-   [ ] Criar classe base `Agent`.
-   [ ] Migrar chat atual para a nova estrutura (`pages/💬_Chat_Geral.py`).
-   [ ] Implementar a nova estrutura de diretórios (`agents/`, `tools/`, `prompts/`, `utils/session_manager.py`, `utils/ui_components.py`).
-   [ ] Resolver bugs de conexão de banco de dados e gerenciamento de dependências.

### Fase 2: Agentes Básicos
-   [ ] Implementar Chat Geral (com Web Search Integration).
-   [ ] Implementar RP (Redator Profissional) com suas ferramentas.
-   [ ] Implementar Home/Dashboard.

### Fase 3: Agentes Avançados
-   [ ] Implementar Brainstorming com suas ferramentas.
-   [ ] Implementar Sumarizador com OCR avançado e processamento de imagens.
-   [ ] Implementar Especialista SmartSimple com RAG e base de conhecimento.

### Fase 4: Integração e Polimento
-   [ ] Implementar Configurações Globais (Perfil Personalizado, Configurações de Modelo, Dados e Privacidade).
-   [ ] Otimizações de UX e UI em toda a plataforma.
-   [ ] Implementar testes unitários e de integração abrangentes.

---

## ✅ Concluído (v0.1.0)

-   **[DOCUMENTAÇÃO] Comentários no Código**: Adicionadas docstrings e comentários em `app.py`, `db/db.py` e `utils/configs.py` para explicar a lógica e o funcionamento.
-   **[DOCUMENTAÇÃO] README.md**: Criado `README.md` com instruções de setup, configuração e execução.
-   **[DOCUMENTAÇÃO] Arquivos de Projeto**: Criados `CHANGELOG.md`, `docs/overview.md` e `docs/aula_projeto.md`.
-   **[LICENÇA]**: Projeto licenciado sob a GPLv3.
-   **[CONFIG]**: Adicionado arquivo `.gitignore`.
