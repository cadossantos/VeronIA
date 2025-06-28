# Visão Geral Técnica do Protótipo: VeronIA

## 1. Introdução

O projeto **VeronIA** é uma interface de chat interativa construída com Streamlit, projetada para permitir a comunicação com diversos modelos de linguagem grandes (LLMs). A aplicação é estruturada de forma modular, separando a lógica da interface do usuário, a configuração dos modelos e a persistência de dados.

## 2. Arquitetura

O sistema é composto pelos seguintes módulos principais:

- **`app.py`**: O ponto de entrada da aplicação. Responsável pela interface do usuário (UI) com Streamlit, gerenciamento de estado da sessão (`st.session_state`) e orquestração das interações entre o usuário e o backend.
- **`db/`**: Módulo de banco de dados.
  - **`db.py`**: Contém todas as funções para interagir com o banco de dados PostgreSQL, como criar e carregar conversas e mensagens.
  - **`init_db.py`**: Script para inicializar o esquema do banco de dados (criação das tabelas `conversas` e `mensagens`).
- **`utils/`**: Módulo de utilitários.
  - **`configs.py`**: Centraliza a configuração dos modelos de linguagem suportados (Ollama, Groq, OpenAI), definindo os modelos disponíveis e as classes LangChain correspondentes.
- **`.env`**: Arquivo para armazenar variáveis de ambiente, como chaves de API e credenciais do banco de dados.
- **`pyproject.toml` e `requirements.txt`**: Gerenciam as dependências do projeto.

## 3. Fluxo de Dados e Interação

1.  **Inicialização**: Ao iniciar, `app.py` chama `inicializacao()`, que:
    -   Executa `init_database()` para garantir que as tabelas do banco de dados existam.
    -   Configura o estado da sessão (`st.session_state`) com valores padrão para a conversa, memória e configurações do modelo.

2.  **Configuração do Modelo**:
    -   Na aba "Configurações", o usuário seleciona um provedor (Ollama, Groq, OpenAI) e um modelo específico.
    -   Ao clicar em "Iniciar Oráculo", a função `carrega_modelo()` é chamada.
    -   `carrega_modelo()` utiliza as configurações de `utils/configs.py` para instanciar a classe de chat apropriada do LangChain (ex: `ChatOpenAI`, `ChatGroq`).
    -   A instância do modelo, encapsulada em uma `chain` do LangChain com um prompt pré-definido, é armazenada no estado da sessão.

3.  **Gerenciamento de Conversas**:
    -   O usuário pode criar uma "Nova conversa" ou selecionar uma existente na barra lateral.
    -   **Nova Conversa**: `inicia_nova_conversa()` cria um novo registro na tabela `conversas` do banco de dados e reseta a memória da conversa no estado da sessão.
    -   **Selecionar Conversa**: `seleciona_conversa()` carrega o histórico de mensagens da conversa selecionada do banco de dados e o popula na memória (`ConversationBufferMemory`) do LangChain.

4.  **Troca de Mensagens**:
    -   O usuário envia uma mensagem através do `st.chat_input`.
    -   A aplicação envia a mensagem do usuário e o histórico da conversa (da memória) para a `chain` do LangChain.
    -   A resposta do modelo é recebida como um stream e exibida na interface.
    -   A mensagem do usuário e a resposta do modelo são salvas no banco de dados (`salvar_mensagem()`) e adicionadas à memória da sessão.

## 4. Persistência de Dados

-   **Banco de Dados**: PostgreSQL.
-   **Tabelas**:
    -   `conversas`: Armazena metadados de cada conversa (ID, título, provedor, modelo, data de criação).
    -   `mensagens`: Armazena cada mensagem, com `role` ('user' ou 'assistant'), conteúdo e um `timestamp`, vinculada a uma conversa pelo `conversa_id`.
-   **Driver**: `psycopg` é utilizado para a conexão com o banco de dados.

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
