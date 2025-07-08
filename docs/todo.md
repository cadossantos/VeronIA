# TODO & Pontos de Melhoria - VeronIA

Este documento serve como um backlog de tarefas, bugs e sugestões de refatoração para o projeto VeronIA. A ideia é que ele guie o desenvolvimento e aprimoramento contínuo da aplicação, agora com foco na transformação para uma plataforma multi-agente e multimodal.

## 🌟 Visão Geral do Projeto (Atualizado com PRD)

O VeronIA está evoluindo de um chat único para uma **plataforma multi-agente** com um **hub principal multimodal (VerônIA Multitool)**. Esse hub centraliza ferramentas como OCR, transcrição, escrita, tradução, pesquisa web e seleção de formato de resposta. Outros agentes avançados terão páginas próprias.

Cada "agente" tem:

* Prompt system específico
* Ferramentas especializadas
* Memória e contexto personalizados
* Interface adaptada

## 🐞 Bugs e Inconsistências

### Travamentos

Causas conhecidas (resolvidas ou em andamento):

* Uso incorreto de `ConversationBufferMemory`
* Falta de cache de modelo
* `st.rerun()` excessivo
* Múltiplas conexões SQLite simultâneas
* Excesso de mensagens renderizadas

🛠️ Ações:

* [ ] Considerar SessionStateProxy para reconstrução de estado baseada no banco
* [ ] Avaliar uso de `ConversationSummaryMemory` ou memória híbrida para redução de carga

## 🚀 Melhorias de Funcionalidade (Por Agente e Global)

### Funcionalidades Globais

* [ ] **Página Inicial (Dashboard)**: Apresentar agentes disponíveis e acesso rápido
* [ ] **Configurações Globais**:

  * Perfil do usuário (nome, cargo, tom de voz preferido)
  * Configuração de modelo global
  * Controle de privacidade e exclusão de memória
* [ ] **Feedback Visual**: Adicionar `st.spinner` em carregamentos de modelo, uploads e consultas longas
* [ ] **Deleção e Renomeação de Conversas**: Já disponível, mas pode ser refinado
* [ ] **Busca em Conversas**: Filtrar por nome, palavra-chave ou data

### VerônIA (Chat Geral Multitool)

* [ ] **Nova Página Principal com Layout 3/5 + 2/5**

  * Chat na esquerda (3/5)
  * Ferramentas na direita (2/5): upload, modo, formato de resposta
* [ ] **Upload Inteligente**

  * Detecta tipo (`.pdf`, `.jpg`, `.mp3`, etc.) automaticamente
  * Encaminha para ferramenta correspondente (OCR, transcrição, leitura)
* [ ] **Modos do Agente**

  * Seletor ou comando `@modo` para ativar: `Normal`, `Post-it`, `Redator`, `Tradutor`, `Pesquisa Web`
  * Cada modo altera prompt e ferramentas disponíveis
* [ ] **Formato de Resposta** (estilo Claude AI)

  * Seletor com: Curta, Detalhada, Lista com bullets, Código, Resumo Executivo

### Agentes Avançados (com páginas próprias)

* [ ] **DataVerô**: Análise interativa de CSV com tabs e visualização Plotly
* [ ] **GestãoSábia**: Processamento de formulários e avaliação de processos internos
* [ ] **RegistreRAG**: Consultoria técnica SmartSimple com painel de documentos e RAG

### Futuro: Brainstorming Criativo

* Técnicas de criatividade, variações de ideias e exportação visual

## 🛠️ Refatoração e Qualidade de Código

* [ ] **\[ARQUITETURA] Multipage com `main_chat_page.py` e `pages/` específicas**
* [ ] **Classe `BaseAgent` e `MultitoolAgent`** para controle de modo e ferramentas
* [ ] **Modularização de Tools**:

  * `upload_processor.py`, `ocr_tools.py`, `audio_tools.py`, `response_format.py`
* [ ] **Melhoria no Gerenciamento de Memória**:

  * Substituir `buffer` por `summary` ou RAG local
* [ ] **Conexão com SQLite**:

  * Pool ou conexão persistente controlada
  * Camada de exceções desacoplada da UI
* [ ] **Limpeza de Código Morto** e `expander` de debug

## ✅ Testes

* [ ] **Testes Unitários**: Lógica de banco, parsing de uploads, modo de resposta
* [ ] **Testes de Integração**: Simular fluxo com modos, uploads, e retorno formatado

## 🗓️ Fases de Implementação

### Fase 1: Reestruturação e Página Principal

* [ ] Criar `main_chat_page.py` com layout 3/5 + 2/5
* [ ] Adicionar seletor de modo e formato de resposta
* [ ] Refatorar prompt dinâmico com base no modo

### Fase 2: Upload Inteligente e Tools

* [ ] Criar `upload_processor.py` com detecção automática
* [ ] Implementar OCR, transcrição e leitura de PDF

### Fase 3: Agentes Avançados

* [ ] Migrar agentes `DataVerô`, `GestãoSábia`, `RegistreRAG` para `pages/`
* [ ] Implementar UI própria para cada um com tabs, upload e análise

### Fase 4: Integração e Polimento

* [ ] Configurações Globais e contexto do usuário
* [ ] UX refinada e layout responsivo
* [ ] Testes finais e documentação

## ✅ Concluído (v0.1.6)

## ✅ Concluído (v0.1.5)

* [x] Otimização de memória e cache de modelos/conversas
* [x] Conexão SQLite unificada via `get_cached_conn()`
* [x] Correção de `st.rerun()` e limitação do histórico exibido
* [x] Modularização da aplicação em `components/`, `services/` e `utils/`

## ✅ Concluído (v0.1.3)

* [x] Sidebar renderiza corretamente em `_Chat_Geral.py`
* [x] Dependências centralizadas no `pyproject.toml` com remoção do `requirements.txt`

## ✅ Concluído (v0.1.0)

* [x] Docstrings em `app.py`, `db/db.py` e `utils/configs.py`
* [x] Criado `README.md`, `CHANGELOG.md`, `docs/overview.md`
* [x] Licença GPLv3 e `.gitignore` aplicados
