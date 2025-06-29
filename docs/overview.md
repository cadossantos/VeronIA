# Visão Geral Técnica do Protótipo: VeronIA

## 1. Introdução

O projeto **VeronIA** é uma interface de chat interativa construída com Streamlit, projetada para permitir a comunicação com diversos modelos de linguagem grandes (LLMs). A aplicação é estruturada de forma modular, separando a lógica da interface do usuário, a configuração dos modelos e a persistência de dados.

## 2. Arquitetura

O projeto foi reestruturado para uma arquitetura modular, visando a separação de responsabilidades e a escalabilidade. Os componentes principais são:

- **`app.py`**: Ponto de entrada da aplicação Streamlit. Define a configuração geral da página e o cabeçalho principal.
- **`pages/`**: Contém as diferentes páginas da aplicação.
  - **`_Chat_Geral.py`**: É a página principal da interface de chat, onde a maior parte da interação do usuário acontece.
- **`components/`**: Módulo com os componentes visuais reutilizáveis da interface.
  - **`header.py`**: Renderiza o cabeçalho da aplicação.
  - **`sidebar.py`**: Constrói a barra lateral, responsável pela seleção e gerenciamento de conversas.
  - **`chat_display.py`**: Responsável por exibir o histórico de mensagens da conversa ativa.
- **`services/`**: Contém a lógica de negócio desacoplada da interface.
  - **`model_service.py`**: Gerencia a configuração e instanciação dos modelos de linguagem (LLMs) via LangChain.
  - **`conversation_service.py`**: Orquestra as operações relacionadas às conversas, como criar, carregar e salvar mensagens.
  - **`memory_service.py`**: Gerencia a memória da conversa (histórico).
- **`db/`**: Módulo de acesso a dados.
  - **`db_sqlite.py`**: Centraliza todas as interações com o banco de dados SQLite, como inicialização, e operações de CRUD para conversas e mensagens.
- **`utils/`**: Módulo de utilitários.
  - **`configs.py`**: Centraliza as configurações dos modelos de linguagem (Ollama, Groq, OpenAI).
  - **`session_utils.py`**: Fornece funções para gerenciar e inicializar o estado da sessão do Streamlit (`st.session_state`).

## 3. Fluxo de Dados e Interação

1.  **Inicialização**: Ao acessar a aplicação, `app.py` e `pages/_Chat_Geral.py` são executados. A função `initialize_session()` de `session_utils.py` é chamada para configurar o `st.session_state`, e `db_sqlite.init_database()` garante que o banco de dados e as tabelas existam.
2.  **Interface Principal**:
    -   `components/header.py` renderiza o título da aplicação.
    -   `components/sidebar.py` é renderizado, permitindo ao usuário selecionar uma conversa existente ou iniciar uma nova. As conversas são carregadas do banco de dados via `conversation_service`.
3.  **Seleção de Modelo**: Na barra lateral, o usuário seleciona um provedor e um modelo. Essa configuração é salva no `st.session_state`.
4.  **Interação no Chat**:
    -   A página `_Chat_Geral.py` gerencia o fluxo do chat.
    -   O histórico da conversa selecionada é carregado e exibido por `components/chat_display.py`.
    -   Quando o usuário envia uma nova mensagem, a aplicação chama `conversation_service.process_message()`.
    -   Este serviço utiliza `model_service` para obter a instância do modelo configurado e `memory_service` para gerenciar o histórico.
    -   A resposta do LLM é recebida e exibida em tempo real na interface.
    -   A nova mensagem e a resposta do assistente são salvas no banco de dados através do `conversation_service`, que por sua vez chama as funções em `db_sqlite.py`.

## 4. Persistência de Dados

-   **Banco de Dados**: SQLite.
-   **Arquivo**: O banco de dados é um arquivo local em `db/veronia.db`.
-   **Tabelas**:
    -   `conversations`: Armazena metadados de cada conversa (ID, título, data de criação).
    -   `messages`: Armazena cada mensagem (`role`, conteúdo) e a vincula a uma `conversation_id`.
-   **Módulo de Acesso**: As interações com o banco de dados são gerenciadas exclusivamente por `db/db_sqlite.py`.

## 5. Dependências Chave

-   **Streamlit**: Para a criação da interface do usuário web.
-   **LangChain**: Para a abstração e interação com os diferentes modelos de LLM.
-   **psycopg[binary]**: Driver para conexão com o PostgreSQL.
-   **python-dotenv**: Para o gerenciamento de variáveis de ambiente.
-   **openai, langchain-groq, langchain-community**: SDKs específicos para os provedores de LLM.

## 6. Pontos de Melhoria e Próximos Passos

-   **Gerenciamento de Erros**: Implementar um tratamento de erros mais robusto, especialmente para as chamadas de API e interações com o banco de dados.
-   **Upload de Arquivos**: Adicionar a funcionalidade de upload de arquivos (PDF, CSV, etc.) para análise pelo LLM.
-   **Testes**: Criar testes unitários e de integração para garantir a confiabilidade do código.
-   **Segurança**: Revisar a segurança, especialmente no que diz respeito ao manuseio de chaves de API.
-   **Containerização**: Empacotar a aplicação com Docker para facilitar o deploy.
