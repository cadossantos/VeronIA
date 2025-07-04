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

5 principais causas identificadas (uso de `ConversationBufferMemory`, ausência de cache, `st.rerun()` incorreto, múltiplas conexões SQLite e excesso de mensagens renderizadas) foram resolvidas nas versões recentes.

🛠️ Solução ideal (médio prazo)
Considerar SessionStateProxy externo via `st.session_state['x'] = None` com reconstrução baseada no banco

Avaliar LangChain com ConversationSummaryMemory para não reter tudo na RAM




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

## ✅ Concluído (v0.1.6)

## ✅ Concluído (v0.1.5)
- [x] Otimização de memória e cache de modelos/conversas.
- [x] Conexão SQLite unificada via `get_cached_conn()`.
- [x] Correção de `st.rerun()` e limitação do histórico exibido.
- [x] Modularização da aplicação em `components/`, `services/` e `utils/`.

## ✅ Concluído (v0.1.4)

## ✅ Concluído (v0.1.3)
- [x] Sidebar renderiza corretamente em `_Chat_Geral.py`.
- [x] Dependências centralizadas no `pyproject.toml` com remoção do `requirements.txt`.

## ✅ Concluído (v0.1.0)

-   **[DOCUMENTAÇÃO] Comentários no Código**: Adicionadas docstrings e comentários em `app.py`, `db/db.py` e `utils/configs.py` para explicar a lógica e o funcionamento.
-   **[DOCUMENTAÇÃO] README.md**: Criado `README.md` com instruções de setup, configuração e execução.
-   **[DOCUMENTAÇÃO] Arquivos de Projeto**: Criados `CHANGELOG.md`, `docs/overview.md` e `docs/aula_projeto.md`.
-   **[LICENÇA]**: Projeto licenciado sob a GPLv3.
-   **[CONFIG]**: Adicionado arquivo `.gitignore`.
