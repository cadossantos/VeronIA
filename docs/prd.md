## PRD - VeronIA Multi-Agent Platform

### 1. Visão do Produto

**Transformar o VeronIA de um chat único em uma plataforma multi-agent**, onde cada página representa um especialista diferente com:
- Prompt system específico
- Ferramentas (tools) especializadas  
- Comportamento de memória personalizado
- Interface adaptada ao contexto

### 2. Arquitetura Conceitual

```
VeronIA Platform
├── 🏠 Home/Dashboard
├── 💬 Chat Geral (para uso comum cotidiano, deverá ter tool de pesquisa na internet)
├── 📝 Editor/Revisor (terá um prompt apropriado)
├── 📝 Sumarizador (terá um prompt apropriado e ocr avançado com "https://huggingface.co/nanonets/Nanonets-OCR-s" para extrair e organizar fotos de anotações manuscritas)
├── 🔍 Especialista SmartSimple (agente avançado com rag para acessar documentação técnica) 
├── 🧠 Brainstorming (prompt para desenvolvimento de ideia)
└── ⚙️ Configurações Globais
```

### 3. Especificação dos Agents

#### 3.1 Chat Geral
- **Função**: Conversação cotidiana com capacidade de pesquisa
- **Tools**: 
  - Web search integration
  - Síntese de resultados de pesquisa
- **Memória**: Conversa contínua com contexto de pesquisas
- **Interface**: Chat tradicional + indicadores de pesquisa ativa

#### 3.2 RP (Redator Profissional)
- **Função**: Escrita humanizada e geração de emails profissionais
- **Tools**:
  - Templates de email (formal, comercial, follow-up)
  - Análise de tom e estilo
  - Sugestões de melhoria de escrita
- **Memória**: Histórico de documentos criados na sessão
- **Interface**: Editor de texto + templates + preview de email

#### 3.3 Sumarizador
- **Função**: Extrair e organizar conteúdo de anotações manuscritas
- **Tools**:
  - OCR avançado (Nanonets-OCR-s via HuggingFace)
  - Upload de imagens/fotos
  - Estruturação automática de texto extraído
  - Export de resumos organizados
- **Memória**: Contexto das imagens processadas na sessão
- **Interface**: Upload de imagens + preview OCR + área de edição do texto extraído

#### 3.4 Especialista SmartSimple
- **Função**: Consultor técnico especializado com acesso à documentação
- **Tools**:
  - RAG (Retrieval-Augmented Generation)
  - Base de conhecimento técnica SmartSimple
  - Busca semântica em documentação
  - Geração de exemplos práticos
- **Memória**: Contexto técnico da consulta + documentos referenciados
- **Interface**: Chat especializado + painel de documentos citados + links para fontes

#### 3.5 Brainstorming
- **Função**: Desenvolvimento e expansão criativa de ideias
- **Tools**:
  - Técnicas de criatividade estruturadas
  - Geração de variações e derivações
  - Organização hierárquica de ideias
  - Export de mapas mentais
- **Memória**: Sessão completa de brainstorming com evolução das ideias
- **Interface**: Canvas de ideias + chat direcionado + ferramentas de organização

### 4. Arquitetura Técnica Proposta

```
veronia/
├── app.py                    # Entry point + router
├── pages/                    # Streamlit pages
│   ├── 🏠_Home.py
│   ├── 💬_Chat_Geral.py     # Migração do atual
│   ├── 📝_Editor_Revisor.py
│   ├── 📝_Sumarizador.py
│   ├── 🔍_Especialista_SmartSimple.py
│   └── 🧠_Brainstorming.py
├── agents/                   # Agent definitions
│   ├── base_agent.py        # Classe base
│   ├── chat_agent.py
│   ├── editor_agent.py
│   ├── summarizer_agent.py
│   ├── smartsimple_agent.py
│   └── brainstorm_agent.py
├── tools/                    # Agent tools
│   ├── web_tools.py         # Search, scraping
│   ├── ocr_tools.py         # Nanonets OCR integration
│   ├── rag_tools.py         # RAG para SmartSimple
│   └── creative_tools.py    # Brainstorming tools
├── db/                      # Database (mantém atual)
│   ├── db_sqlite.py
│   └── init_db.py
├── utils/                   # Utilities (mantém + expande)
│   ├── configs.py
│   ├── session_manager.py   # Gerenciar state entre pages
│   └── ui_components.py     # Componentes reutilizáveis
└── prompts/                 # System prompts por agent
    ├── chat_prompts.py
    ├── editor_prompts.py
    ├── summarizer_prompts.py
    ├── smartsimple_prompts.py
    └── brainstorm_prompts.py
```

### 5. Questões de Design

#### 5.1 Gerenciamento de Estado
- **Pergunta**: Como manter contexto entre pages? 
- **Opções**: 
  - `st.session_state` global
  - Database para persistência
  - Cache específico por agent

#### 5.2 Memória dos Agents - Opção Híbrida com Contexto Global
- Compartilhada: Agents podem referenciar conversas de outros
- Conceito Principal
- Contexto Global Personalizável: Uma configuração que permite ao usuário definir informações pessoais/profissionais que serão automaticamente injetadas no system prompt de todos os agents.

**Possibilidades de Implementação**
- [Campo de texto livre para o usuário]
- + Tags pré-definidas:
  - #Desenvolvedor #Startup #Feminismo
  - #Gestão #Marketing #Tecnologia

Implementação Técnica
Estrutura no Banco de Dados
```sql
CREATE TABLE user_profile (
    id INTEGER PRIMARY KEY,
    name TEXT,
    profession TEXT,
    context_text TEXT,
    communication_style TEXT,
    detail_level TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```
Injeção no System Prompt
```python
def build_system_prompt(agent_type, user_profile=None):
    base_prompt = get_agent_base_prompt(agent_type)
    
    if user_profile:
        context_injection = f"""
        CONTEXTO DO USUÁRIO:
        - Nome: {user_profile.name}
        - Profissão: {user_profile.profession}
        - Contexto adicional: {user_profile.context_text}
        - Estilo de comunicação preferido: {user_profile.communication_style}
        
        Use essas informações para personalizar suas respostas de forma mais relevante e contextualizada.
        """
        return context_injection + "\n\n" + base_prompt
    
    return base_prompt
```
Boas Práticas
1. Controle Granular
   - Permitir ativar/desativar o contexto global por agent
   - Opção de "modo incógnito" temporário
   - Visualização de como o contexto será usado

2. Privacidade e Segurança
   - Dados armazenados localmente (SQLite)
   - Opção de limpar contexto facilmente
   - Avisos sobre informações sensíveis

3. UX Intuitiva
   - Interface similar ao ChatGPT (como no print)
   - Preview de como o prompt ficará
   - Exemplos e sugestões de preenchimento

4. Flexibilidade por Agent
```python
agent_context_usage = {
    'chat_geral': True,          # Usa contexto completo
    'editor': True,              # Foca em estilo de escrita
    'sumarizador': False,        # Não precisa de contexto pessoal
    'smartsimple': True,         # Usa contexto profissional
    'brainstorming': True        # Usa tudo para criatividade
}
```
Interface Proposta
Na página de Configurações Globais:
- 🔧 Configurações Globais
  - 👤 Perfil Personalizado
    - [Interface similar ao ChatGPT]
    - Preview do contexto
    - Configurações por agent
  - 🤖 Configurações de Modelo
  - 💾 Dados e Privacidade
Vantagens desta Abordagem

- Personalização Real: Cada agent conhece o usuário
- Consistência: Mesma personalidade em todos os agents
- Eficiência: Não precisa repetir contexto em cada conversa
- Flexibilidade: Pode ser ajustado por necessidade
- Privacidade: Controle total sobre os dados

#### 5.3 Configurações de Modelo
- **Pergunta**: Modelo global ou específico por agent?

  - Flexível: Usuário escolhe

#### 5.4 Interface de Navegação
- **Pergunta**: Como o usuário navega entre agents?

  - Sidebar navigation (padrão Streamlit)
  
### 6. Fases de Implementação

#### Fase 1: Infraestrutura
- Refatorar código atual para arquitetura multipage
- Criar classe base `Agent`
- Migrar chat atual para nova estrutura

#### Fase 2: Agent Básicos
- Implementar Chat Geral
- Implementar Editor/Revisor

#### Fase 3: Agents Avançados  
- Implementar Brainstorming
  - Sumarizador com OCR
  - Especialista com RAG

#### Fase 4: Integração e Polimento
- Dashboard home
- Navegação entre contexts
- Otimizações de UX

---
