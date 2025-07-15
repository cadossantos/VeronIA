# Documento de Requisitos de Produto (PRD): Plataforma Multi-agente VeronIA

## 1. Visão do Produto

O objetivo é transformar o VeronIA em uma plataforma multimodal centralizada, equipada com um conjunto de ferramentas inteligentes. A plataforma integrará funcionalidades de OCR, transcrição de áudio, tradução e redação institucional dentro de uma interface de chat principal, oferecendo respostas personalizáveis e mantendo agentes especialistas em páginas separadas para tarefas específicas.

## 2. Arquitetura Conceitual

A plataforma será organizada da seguinte forma:

- **Página Principal (VeronIA Multitool)**: Interface de chat principal com ferramentas integradas.
    - Upload de arquivos (PDF, imagem, áudio).
    - Funcionalidades de OCR e transcrição.
    - Modos de operação (Post-it, Redator, Tradutor, Web).
    - Personalização do formato de resposta.
    - Memória e contexto de conversa estruturados.
- **Agentes Especialistas (Páginas Separadas)**:
    - **Análise de Dados**: Para visualização e análise de dados tabulares.
    - **Gestão de Equipe**: Para processamento de formulários e avaliações.
    - **Especialista SmartSimple**: Para consultas técnicas com RAG.
- **Configurações Globais**: Para gerenciamento de modelos, provedores e chaves de API.

## 3. Requisitos Funcionais

### 3.1. Página Principal (Chat Geral)

- **Layout**: A interface será dividida em duas seções: 3/5 para o chat e 2/5 para as ferramentas.
- **Upload Inteligente**: O sistema deverá detectar o tipo de arquivo (PDF, JPG, MP3) e aplicar a função correspondente (leitura de texto, OCR, transcrição).
- **Modos de Operação**: O usuário poderá alternar entre diferentes modos que ajustam o prompt do sistema e as ferramentas disponíveis.
- **Formato de Resposta**: O usuário poderá escolher o formato da resposta (curta, detalhada, lista, código, resumo).
- **Persistência**: O histórico de conversas será salvo em um banco de dados SQLite.
- **Comandos**: O sistema deverá suportar comandos no campo de entrada (ex: `@modo`, `@traduzir`).

### 3.2. Agentes Especiais

- **Agente de Análise de Dados**: Deverá permitir a visualização interativa e a análise de arquivos CSV e outros formatos tabulares.
- **Agente de Gestão de Equipe**: Deverá facilitar o processamento estruturado de formulários e outros documentos de gestão.
- **Agente de RAG**: Deverá fornecer uma interface para recuperação de informações de uma base de conhecimento específica (SmartSimple).

## 4. Estrutura Técnica Proposta

- **`main_chat_page.py`**: Implementará a nova página principal com o layout de 3/5 + 2/5.
- **`agents/`**: Conterá a lógica dos agentes, incluindo um `multitool_agent.py` para gerenciar os modos de operação.
- **`tools/`**: Conterá as ferramentas, como `upload_processor.py` para o processamento de arquivos, `ocr_tools.py` e `audio_tools.py`.
- **`prompts/`**: Armazenará os prompts do sistema, com variações para cada modo de operação.
- **`components/`**: Incluirá os componentes da interface, como `file_uploader.py` e um novo `tools_panel.py` para a seção de ferramentas.