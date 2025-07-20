# Visão Geral Técnica do Protótipo: VeronIA

## 1. Introdução

O projeto **VeronIA** é uma interface de chat interativa construída com Streamlit, projetada para permitir a comunicação com diversos modelos de linguagem grandes (LLMs) e, agora, com uma robusta funcionalidade de Retrieval-Augmented Generation (RAG). A aplicação é estruturada de forma modular, separando a lógica da interface do usuário, a configuração dos modelos e a persistência de dados.

## 2. Arquitetura

O projeto foi reestruturado para uma arquitetura modular, visando a separação de responsabilidades e a escalabilidade. Os componentes principais são:

- **`app.py`**: Ponto de entrada da aplicação Streamlit. Define a configuração geral da página e o cabeçalho principal.
- **`components/`**: Módulo com os componentes visuais reutilizáveis da interface.
  - **`header.py`**: Renderiza o cabeçalho da aplicação.
  - **`sidebar.py`**: Constrói a barra lateral, responsável pela seleção e gerenciamento de conversas, configurações de modelo, e agora, gerenciamento de bases de conhecimento RAG e scraping.
  - **`chat_interface.py`**: Gerencia o fluxo principal do chat, incluindo o processamento de entrada do usuário, integração com serviços e exibição de mensagens.
- **`services/`**: Contém a lógica de negócio desacoplada da interface.
  - **`model_service.py`**: Gerencia a configuração e instanciação dos modelos de linguagem (LLMs) via LangChain.
  - **`conversation_service.py`**: Orquestra as operações relacionadas às conversas, como criar, carregar e salvar mensagens.
  - **`memory_service.py`**: Gerencia a memória da conversa (histórico).
  - **`scraping_service.py`**: **NOVO** Orquestra o processo de scraping recursivo de URLs e o salvamento de páginas, além de gerenciar a ingestão de documentos raspados no ChromaDB.
  - **`ingest_service.py`**: Responsável por carregar documentos, dividi-los em chunks e indexá-los em um vetor store (ChromaDB).
  - **`rag_service.py`**: Gerencia a criação e o acesso dinâmico a instâncias do `RagQueryEngine` (agentes RAG) para diferentes bases de conhecimento, utilizando cache para otimização.
  - **`crawler/`**: **NOVO** Módulo contendo a lógica específica para o scraping de conteúdo web (fetcher, parser, storage).
- **`agents/`**: Contém a lógica de agentes especializados.
  - **`rag_agent.py`**: Implementa o motor do RAG, responsável por recuperar documentos relevantes de uma base de conhecimento específica e combiná-los com a pergunta para gerar uma resposta contextualizada.
- **`db/`**: Módulo de acesso a dados.
  - **`db_sqlite.py`**: Centraliza todas as interações com o banco de dados SQLite para conversas e mensagens.
  - **`db/smartwiki_links.json`**: **NOVO** Arquivo JSON que armazena os links das bases de conhecimento SmartWiki e suas respectivas URLs.
  - **`db/pages/<nome_da_base>/`**: Diretórios onde os arquivos `.json` de cada página raspada são salvos.
  - **`db/vector_store/<nome_da_base>/`**: Diretórios onde o ChromaDB salva os índices vetoriais para cada base de conhecimento.
- **`utils/`**: Módulo de utilitários.
  - **`configs.py`**: Centraliza as configurações dos modelos de linguagem.
  - **`session_utils.py`**: Fornece funções para gerenciar e inicializar o estado da sessão do Streamlit.
  - **`logger.py`**: **NOVO** Módulo para logging centralizado.
- **`prompts/`**: Contém os prompts de sistema e prompts específicos para agentes.
  - **`prompts/rag_agent_prompt.txt`**: **NOVO** Prompt dedicado com instruções rigorosas para o `rag_agent`.

## 3. Fluxo de Dados e Interação

1.  **Inicialização**: Ao acessar a aplicação, `app.py` é executado. A função `init_session_state()` de `session_utils.py` é chamada para configurar o `st.session_state`, e `db_sqlite.init_database()` garante que o banco de dados e as tabelas existam.
2.  **Interface Principal**:
    -   `components/header.py` renderiza o título da aplicação.
    -   `components/sidebar.py` é renderizado, permitindo ao usuário gerenciar conversas, configurar modelos e interagir com as funcionalidades RAG e de scraping.
3.  **Gerenciamento de Bases de Conhecimento (Aba "Scraping")**:
    -   O usuário pode adicionar URLs de páginas ou categorias da SmartWiki e nomear uma nova base de conhecimento.
    -   Ao clicar em "Raspar e Salvar Páginas", `scraping_service.raspar_links_e_salvar_paginas()` é acionado, realizando o scraping recursivo e salvando o conteúdo em arquivos JSON em `db/pages/<nome_da_base>/`.
4.  **Indexação de Bases (Aba "RAG")**:
    -   O usuário seleciona uma base de páginas raspadas (existente em `db/pages/`) e clica em "Indexar Base Selecionada".
    -   `scraping_service.indexar_base_de_conhecimento()` é acionado, que por sua vez chama `ingest_service.ingest()` para processar os JSONs, criar chunks e indexá-los no ChromaDB em `db/vector_store/<nome_da_base>/`.
5.  **Seleção e Consulta RAG (Aba "RAG" e "Conversas")**:
    -   Na aba "RAG", o usuário seleciona a base de conhecimento desejada para consulta.
    -   Quando o usuário envia uma mensagem na aba "Conversas" e o RAG está ativo, `chat_interface.handle_user_input()` chama `rag_service.consultar_base_de_conhecimento()`.
    -   `rag_service` utiliza `get_rag_agent_cached()` para obter (ou criar e cachear) uma instância do `RagQueryEngine` específica para a base selecionada.
    -   O `RagQueryEngine` recupera os documentos relevantes do ChromaDB e os passa para o LLM (juntamente com o `rag_agent_prompt.txt`) para gerar uma resposta contextualizada.
    -   A resposta do LLM é recebida e exibida na interface.

## 4. Persistência de Dados

-   **Banco de Dados**: SQLite (`db/veronia.db`).
-   **Bases de Conhecimento**: Arquivos JSON em `db/pages/` e índices vetoriais do ChromaDB em `db/vector_store/`.
-   **Configuração de Links**: `db/smartwiki_links.json`.

## 5. Dependências Chave

-   **Streamlit**: Para a criação da interface do usuário web.
-   **LangChain**: Para a abstração e interação com os diferentes modelos de LLM e componentes de RAG.
-   **python-dotenv**: Para o gerenciamento de variáveis de ambiente.
-   **openai, langchain-openai, langchain-groq, langchain-community**: SDKs e integrações específicas para os provedores de LLM e vetor stores.
-   **PyMuPDF (fitz)**: Para extração de texto de PDFs.
-   **pandas**: Para análise de dados (CSV/Excel).
-   **python-docx**: Para extração de texto de DOCX.
-   **beautifulsoup4, requests**: Para scraping web.
-   **chromadb**: Para o banco de dados vetorial.

## 6. Pontos de Melhoria e Próximos Passos

-   **Gerenciamento de Erros Aprimorado**: Implementar um tratamento de erros mais robusto e mensagens de feedback mais claras para o usuário em todas as etapas da pipeline.
-   **Testes Automatizados**: Criar testes unitários e de integração para garantir a confiabilidade do código, especialmente para as novas funcionalidades de RAG e scraping.
-   **Otimização de Performance**: Investigar e implementar otimizações adicionais para o scraping e ingestão de grandes volumes de dados.
-   **UI/UX**: Melhorar a experiência do usuário para gerenciamento de links e bases de conhecimento (edição, exclusão).
-   **Suporte a Mais Tipos de Documentos**: Expandir o `file_processor.py` para lidar com mais formatos de arquivo (imagens com OCR, áudio com transcrição, etc.).
-   **Containerização**: Empacotar a aplicação com Docker para facilitar o deploy.