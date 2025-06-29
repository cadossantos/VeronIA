## PRD - VeronIA Multi-Agent Platform

### 1. Visão do Produto

**Transformar o VeronIA de um chat único em uma plataforma multi-agent**, onde cada página representa um especialista diferente com:

* Prompt system específico
* Ferramentas (tools) especializadas
* Comportamento de memória personalizado
* Interface adaptada ao contexto
* Módulo de agente orientado a objetos, com `BaseAgent` e subclasses específicas

### 2. Arquitetura Conceitual

```
VeronIA Platform
├── 🏠 Chat Geral (uso cotidiano, pesquisa na web, tradução, whisper)
├── 💬 Redator Profissional (texto institucional, e-mails)
├── 📝 OCR Notas (análise de imagens com OCR e sumarização)
├── 🔍 Especialista SmartSimple (consultor técnico com RAG)
├── 📊 Análise de Dados (painéis, CSVs, LLM explicativa)
├── 👥 Gestão de Equipe (formulários, processos, avaliações)
├── 🔒 Modo Seguro (modelo local com Ollama, sem API)
└── ⚙️ Configurações Globais
```

### 3. Especificação dos Agents

Cada agente é implementado como uma classe derivada de `BaseAgent`, com métodos como `get_system_prompt()`, `get_specialized_tools()`, `initialize_memory()` e `process_message()`.

#### 3.1 Chat Geral

* **Nome**: VerônIA
* **Função**: Conversação cotidiana
* **Tools**: Web search, tradução, whisper
* **Memória**: Buffer de sessão
* **Interface**: Chat clássico

#### 3.2 Redator Profissional

* **Nome**: Redator
* **Função**: Escrita de relatórios, e-mails institucionais
* **Tools**: Templates, análise de estilo
* **Memória**: Documentos criados na sessão
* **Interface**: Editor + templates

#### 3.3 OCR Notas

* **Nome**: PostitBot
* **Função**: Extrair e organizar imagens de anotações
* **Tools**: OCR (Tesseract ou HuggingFace), sumarização, estruturação
* **Memória**: Temporária
* **Interface**: Upload + preview + editor

#### 3.4 Especialista SmartSimple

* **Nome**: RegistreRAG
* **Função**: RAG sobre base SmartSimple
* **Tools**: Vector search, markdown loader, retriever
* **Memória**: Contexto técnico e arquivos carregados
* **Interface**: Chat + painel de documentos

#### 3.5 Análise de Dados

* **Nome**: DataVerô
* **Função**: Interpretar CSVs, planilhas, gerar dashboards
* **Tools**: PandasTool, Plotly, análise interativa
* **Memória**: Persistente durante a sessão
* **Interface**: Upload + tabs de análise + chat explicativo

#### 3.6 Gestão de Equipe

* **Nome**: GestãoSábia
* **Função**: Analisar formulários e avaliar processos
* **Tools**: FormParser, ChecklistTool, PromptTemplate
* **Memória**: Estruturada
* **Interface**: Uploads + análises + recomendações

#### 3.7 Modo Seguro

* **Nome**: VerônIA Local
* **Função**: Chat local com LLM sem API
* **Tools**: PythonTool, CSVTool, OllamaClient
* **Memória**: Mínima (segurança)
* **Interface**: Chat clássico com aviso de modo local

### 4. Arquitetura Técnica

```
veronia/
├── app.py                        # Chat geral
├── pages/                        # Páginas de agentes
│   ├── 💬_Redator.py
│   ├── 📝_OCR_Notas.py
│   ├── 🔍_RAG_Específico.py
│   ├── 📊_Análise_de_Dados.py
│   ├── 👥_Gestão_Equipe.py
│   └── 🔒_Modo_Local.py
├── agents/                       # Classes de agentes
│   ├── base_agent.py
│   ├── chat_agent.py
│   ├── redator_agent.py
│   ├── ocr_agent.py
│   ├── rag_agent.py
│   ├── data_agent.py
│   ├── local_agent.py
│   └── management_agent.py
├── tools/                        # Ferramentas especializadas
│   ├── base_tools.py
│   ├── web_tools.py
│   ├── rag_tools.py
│   ├── data_tools.py
│   ├── ocr_tools.py
│   ├── local_tools.py
│   └── management_tools.py
├── prompts/                      # Prompts por agente
│   ├── chat_prompts.py
│   ├── redator_prompts.py
│   ├── ocr_prompts.py
│   ├── rag_prompts.py
│   ├── data_prompts.py
│   └── management_prompts.py
├── services/                     # Lógica de aplicação
│   ├── model_service.py
│   ├── conversation_service.py
│   ├── memory_service.py
│   ├── vector_service.py
│   └── file_service.py
├── db/                           # Banco de dados
│   ├── db_sqlite.py
│   └── veronia.db
├── components/                   # UI Reutilizável
│   ├── sidebar.py
│   ├── header.py
│   ├── chat_display.py
│   ├── file_uploader.py
│   ├── data_viewer.py
│   └── agent_selector.py
└── utils/                        # Utilidades
    ├── configs.py
    ├── session_utils.py
    ├── agent_factory.py
    └── memory_manager.py
```

### 5. Design: Memória, Contexto e Navegação

#### 5.1 Gerenciamento de Estado

* `st.session_state` por agente
* Memória via `ConversationBufferMemory` ou estrutura personalizada

#### 5.2 Contexto Global

* Perfil pessoal do usuário armazenado em `user_profile`
* Injeção condicional de contexto em `system_prompt`
* Ativação controlada por agente (`agent_context_usage`)

#### 5.3 Configurações de Modelo

* Modelo padrão global com possibilidade de override por agente

#### 5.4 Interface e Navegação

* Navegação via sidebar (Streamlit tabs)
* Cada página tem layout 3/5 + 2/5 com área de dados + chat

### 6. Fases de Implementação

#### Fase 1: Base

* Refatorar para multi-page
* Criar `BaseAgent`, `AgentFactory`

#### Fase 2: Primeiros agentes

* `Redator`, `Chat Geral`, `Modo Seguro`

#### Fase 3: Especialistas

* `DataVerô`, `OCR`, `SmartSimple`

#### Fase 4: Integração

* Dashboard, melhorias de UX, contexto global, preview de prompt
