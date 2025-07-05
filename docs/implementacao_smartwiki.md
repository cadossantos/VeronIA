# Proposta de Implementação: Agente Especialista SmartWiki (RAG)

## 1. Introdução

Este documento detalha o plano para integrar a funcionalidade de RAG (Retrieval-Augmented Generation) do módulo `smartwiki` à aplicação principal `VeronIA`. O objetivo é criar uma nova página/agente chamado **"Especialista SmartSimple"**, conforme idealizado no `prd.md`, que responderá a perguntas com base em uma base de conhecimento específica da SmartWiki.

A implementação seguirá os princípios de modularidade e separação de responsabilidades já estabelecidos no projeto `VeronIA`.

## 2. Análise da Situação Atual

-   **Aplicação `VeronIA`**: Possui uma arquitetura de chat funcional, com serviços para gerenciamento de conversas, modelos e memória. A interface é baseada em componentes reutilizáveis do Streamlit. A estrutura está pronta para ser estendida para um modelo multi-página/multi-agente.
-   **Módulo `smartwiki`**: Contém três partes principais, porém desconectadas da aplicação principal:
    1.  `crawler/`: Scripts para extrair conteúdo da wiki e salvar como JSON. **(Funcional)**
    2.  `rag/ingest.py`: Script para processar os arquivos JSON, gerar embeddings e persistir em um Vector Store (ChromaDB). **(Funcional)**
    3.  `agents/`: Um protótipo de aplicação Streamlit para interagir com o Vector Store, que é redundante e precisa ser integrado.

## 3. Proposta de Implementação

A estratégia consiste em absorver a lógica de RAG do `smartwiki` dentro da estrutura de serviços e páginas do `VeronIA`, descartando o código de UI duplicado.

### Fase 1: Reestruturação de Arquivos e Lógica

1.  **Criar a Página do Agente**:
    -   Criar um novo arquivo: `pages/2_Especialista_SmartSimple.py`. O prefixo numérico `2_` controlará a ordem de exibição na sidebar do Streamlit.
    -   Este arquivo será responsável exclusivamente pela interface do usuário do agente de RAG.

2.  **Centralizar a Lógica de RAG em um Serviço**:
    -   Criar um novo serviço: `services/rag_service.py`.
    -   Mover a lógica de `smartwiki/agents/query.py` para este novo serviço. Ele será responsável por:
        -   Carregar o Vector Store do ChromaDB.
        -   Instanciar o `retriever`.
        -   Configurar e retornar a `ConversationalRetrievalChain`.
    -   A função principal (ex: `get_rag_chain`) deve ser cacheada com `@st.cache_resource` para evitar recarregamentos custosos.

3.  **Mover Scripts Utilitários**:
    -   Criar uma pasta `scripts/` na raiz do projeto.
    -   Mover `smartwiki/rag/ingest.py` para `scripts/ingest_smartwiki.py`. Este script é para preparação de dados e não faz parte da aplicação em execução.
    -   O diretório `smartwiki/crawler` e o `smartwiki/main.py` podem ser mantidos como estão, pois compõem a ferramenta de ETL para a base de conhecimento.

4.  **Limpeza**:
    -   O diretório `smartwiki/agents/` deve ser **removido** após a migração de sua lógica, pois sua UI e estrutura são redundantes.

### Fase 2: Refatoração para Reutilização e Implementação do Agente

A implementação será focada em criar um sistema de chat reutilizável e uma interface que se adapta ao agente selecionado.

1.  **Evoluir `components/chat_display.py` para um Componente de Chat Completo**:
    -   Adicionar uma nova função `render_chat_ui` que encapsulará toda a lógica de interação do chat: o campo de input (`st.chat_input`), o processamento do envio, a chamada a uma função de *callback* específica do agente e a atualização do histórico.
    -   A função `renderiza_mensagens` existente será usada internamente por `render_chat_ui` para exibir o histórico.

    ```python
    # Exemplo para a nova função em components/chat_display.py
    def render_chat_ui(history_key: str, on_submit_callback: callable):
        """
        Renderiza uma interface de chat completa e reutilizável.
        
        Args:
            history_key (str): A chave única no st.session_state para o histórico.
            on_submit_callback (callable): A função a ser chamada com o input do usuário.
        """
        renderiza_mensagens(st.session_state.get(history_key, []))

        if prompt := st.chat_input("Sua mensagem..."):
            historico = st.session_state.get(history_key, [])
            historico.append({"role": "user", "content": prompt})
            st.session_state[history_key] = historico
            
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Processando..."):
                    resposta = on_submit_callback(prompt, historico)
                    st.markdown(resposta)
            
            historico.append({"role": "assistant", "content": resposta})
            st.session_state[history_key] = historico
    ```

2.  **Criar o Serviço de RAG (`services/rag_service.py`)**:
    -   Este serviço conterá a lógica para carregar o Vector Store e criar a `ConversationalRetrievalChain`.
    -   A função principal, `get_rag_chain`, será cacheada e parametrizada para aceitar o nome da coleção de documentos a ser usada, permitindo a seleção dinâmica pelo usuário.

    ```python
    # Exemplo para services/rag_service.py
    @st.cache_resource
    def get_rag_chain(collection_name: str = "smartwiki_docs"):
        # ... (lógica para carregar ChromaDB com a collection_name) ...
        vectordb = Chroma(
            persist_directory=f"smartwiki/data/vector_store/{collection_name}",
            # ...
        )
        # ... (resto da configuração da chain) ...
        return qa_chain
    ```

3.  **Implementar a Página do Agente (`pages/2_Especialista_SmartSimple.py`)**:
    -   A página se tornará muito mais simples. Ela definirá seu contexto (`st.session_state['current_page'] = 'smartwiki'`) e chamará o componente de chat reutilizável.
    -   Ela fornecerá uma função de *callback* que sabe como usar o `rag_service` para obter respostas.

    ```python
    # Exemplo para pages/2_Especialista_SmartSimple.py
    import streamlit as st
    from components.chat_display import render_chat_ui
    from services.rag_service import get_rag_chain

    st.session_state['current_page'] = 'smartwiki'

    def processar_mensagem_rag(prompt: str, historico: list) -> str:
        collection = st.session_state.get('active_collection', 'smartwiki_docs')
        qa_chain = get_rag_chain(collection)
        result = qa_chain.invoke({"question": prompt, "chat_history": historico})
        # ... (formatação da resposta com fontes) ...
        return resposta_formatada

    st.title("🧠 Especialista SmartSimple")
    render_chat_ui(
        history_key="smartwiki_history",
        on_submit_callback=processar_mensagem_rag
    )
    ```

4.  **Tornar a Sidebar Dinâmica (`components/sidebar.py`)**:
    -   A função `render_sidebar` irá verificar `st.session_state.get('current_page')`.
    -   Se a página for `'smartwiki'`, ela renderizará uma aba adicional "📚 Coleções" com o seletor de coleções de documentos.
    -   Caso contrário, mostrará a aba padrão "⚙️ Configurações".

### Fase 3: Fluxo do Usuário (UX)

1.  O usuário verá "Especialista SmartSimple" como uma nova página na navegação.
2.  Ao acessá-la, a sidebar mudará, mostrando a aba "Coleções".
3.  O usuário poderá selecionar uma base de conhecimento (coleção) e interagir com o agente de RAG através da interface de chat padronizada.
4.  As respostas incluirão as fontes dos documentos consultados.

## 4. Próximos Passos e Melhorias

-   **Refatorar o Chat Geral**: Aplicar o mesmo padrão de reutilização ao `app.py`, fazendo-o usar o `render_chat_ui`.
-   **Abstração de Agente**: Implementar a `BaseAgent` sugerida no `prd.md` para formalizar a estrutura de cada agente.
-   **Gerenciamento da Base de Conhecimento**: Criar uma interface ou script para facilitar a atualização das coleções de documentos.
-   **Persistência de Conversas**: Adaptar o `db_sqlite.py` para salvar as conversas de todos os agentes, não apenas do chat geral.

```