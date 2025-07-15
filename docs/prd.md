# Documento de Requisitos de Produto (PRD): VeronIA - Versão Ajustada

## 1. Visão do Produto

O VeronIA será uma evolução da estrutura atual, transformando-se em uma plataforma unificada que mantém a organização existente de `components/`, `services/`, e `agents/`, mas adiciona inteligência contextual e funcionalidades integradas através da interface de chat centralizada.

## 2. Arquitetura Baseada na Estrutura Atual

### 2.1 Estrutura de Pastas Ajustada
```
veronia/
├── components/
│   ├── chat_interface.py      # [MODIFICAR] Adicionar detecção de intenção
│   ├── sidebar.py             # [ATUAL] Já tem 3 abas implementadas
│   └── header.py              # [MANTER] Sem alterações
├── services/
│   ├── conversation_service.py # [MANTER] Já implementado
│   ├── model_service.py       # [MANTER] Já implementado
│   ├── memory_service.py      # [MANTER] Já implementado
│   ├── rag_service.py         # [NOVO] Integração com smartwiki
│   └── file_processor.py      # [NOVO] Processamento automático
├── agents/
│   ├── query_agent.py         # [MANTER] Já implementado
│   ├── rag_agent.py           # [MOVER] De smartwiki/rag_agent.py
│   └── (outros agents atuais) # [MANTER] Sem alterações
├── utils/
│   ├── configs.py             # [MANTER] Já implementado
│   ├── constants.py           # [MANTER] Já implementado
│   ├── session_utils.py       # [MANTER] Já implementado
│   └── intent_detector.py     # [NOVO] Detecção de intenção
├── db/
│   └── veronia.db             # [MANTER] Já implementado
├── smartwiki/                 # [GRADUALMENTE INTEGRAR]
│   ├── rag_agent.py          # [MOVER] Para agents/
│   └── vector_store/         # [MANTER] Referência externa
└── pages/
    └── redator.py             # [MANTER] Páginas específicas
```

### 2.2 Filosofia de Implementação
- **Incremental**: Construir sobre o que já existe
- **Sem Breaking Changes**: Manter funcionalidades atuais
- **Integração Gradual**: Smartwiki integrado progressivamente
- **Aproveitamento**: Usar agents existentes como processadores

## 3. Requisitos Funcionais Ajustados

### 3.1 Chat Interface (chat_interface.py)
**Modificações necessárias:**
- Adicionar detecção de intenção antes do processamento
- Integrar com `st.session_state['uploaded_files']` da sidebar
- Verificar status RAG antes de processar mensagens
- Manter compatibilidade com conversation_service existente

```python
def processar_mensagem_unificada(mensagem, arquivos=None):
    # 1. Processar arquivos se existirem
    if arquivos:
        for arquivo in arquivos:
            resultado = file_processor.processar_automatico(arquivo)
            
    # 2. Verificar se RAG está ativo
    if st.session_state.get('rag_ativo'):
        resposta = rag_service.consultar(mensagem)
        if resposta:
            return resposta
            
    # 3. Usar agent apropriado baseado na intenção
    agent = intent_detector.selecionar_agent(mensagem, arquivos)
    return agent.processar(mensagem)
```

### 3.2 Sidebar (sidebar.py) - Já Implementada
**Funcionalidades já existentes:**
- ✅ 3 abas: Conversas, Ferramentas, RAG
- ✅ Upload global com múltiplos arquivos
- ✅ Configurações de modelo e resposta
- ✅ Toggle RAG ativo/inativo
- ✅ Configurações de embedding

**Pequenos ajustes necessários:**
- Conectar toggle RAG com rag_service
- Implementar processamento real dos arquivos uploaded
- Adicionar feedback visual durante processamento

### 3.3 Funcionalidades Globais (Sempre Ativas)

#### 3.3.1 Processamento Automático de Arquivos
```python
# services/file_processor.py - NOVO
def processar_automatico(arquivo):
    """Detecta tipo e aplica processamento adequado"""
    if arquivo.type == "application/pdf":
        return extrair_texto_pdf(arquivo)
    elif arquivo.type.startswith("image/"):
        return aplicar_ocr(arquivo)
    elif arquivo.type.startswith("audio/"):
        return transcrever_audio(arquivo)
    elif arquivo.type in ["text/csv", "application/vnd.ms-excel"]:
        return analisar_dados(arquivo)
    # ... outros tipos
```

#### 3.3.2 Detecção de Intenção
```python
# utils/intent_detector.py - NOVO
def selecionar_agent(mensagem, arquivos=None):
    """Seleciona o agent apropriado baseado no contexto"""
    if arquivos:
        if any(f.type.startswith("image/") for f in arquivos):
            return agents.ocr_agent
        elif any(f.type in ["text/csv", "application/vnd.ms-excel"] for f in arquivos):
            return agents.query_agent
    
    # Análise de texto para determinar intenção
    if "gráfico" in mensagem.lower() or "visualizar" in mensagem.lower():
        return agents.query_agent
    elif "traduzir" in mensagem.lower():
        return agents.translation_agent
    
    return agents.query_agent  # Padrão
```

### 3.4 Integração RAG (services/rag_service.py)
```python
# services/rag_service.py - NOVO
from smartwiki.rag_agent import RagAgent

def ativar_rag():
    """Ativa o modo RAG e limpa contexto"""
    if 'rag_agent' not in st.session_state:
        st.session_state['rag_agent'] = RagAgent()
    st.session_state['rag_ativo'] = True
    
    # Limpar contexto de conversa atual
    conversation_service.limpar_contexto_atual()

def desativar_rag():
    """Desativa o modo RAG"""
    st.session_state['rag_ativo'] = False
    st.session_state.pop('rag_agent', None)

def consultar_rag(query):
    """Consulta usando RAG se ativo"""
    if st.session_state.get('rag_ativo') and 'rag_agent' in st.session_state:
        return st.session_state['rag_agent'].query(query)
    return None
```

## 4. Roadmap de Implementação

### Fase 1: Processamento de Arquivos (1-2 semanas)
**Objetivo**: Tornar o upload funcional
- Implementar `services/file_processor.py`
- Conectar `st.session_state['uploaded_files']` com processamento
- Adicionar feedback visual no chat

**Arquivos a modificar:**
- `components/chat_interface.py` - adicionar verificação de arquivos
- `components/sidebar.py` - melhorar feedback de upload
- Criar `services/file_processor.py`

### Fase 2: Integração RAG (1-2 semanas)
**Objetivo**: RAG funcional através da aba
- Mover `smartwiki/rag_agent.py` para `agents/`
- Implementar `services/rag_service.py`
- Conectar toggle da sidebar com funcionalidade real

**Arquivos a modificar:**
- Mover `smartwiki/rag_agent.py` → `agents/rag_agent.py`
- Criar `services/rag_service.py`
- Modificar `components/chat_interface.py` para verificar RAG

### Fase 3: Detecção de Intenção (1 semana)
**Objetivo**: Seleção automática de agents
- Implementar `utils/intent_detector.py`
- Integrar com chat_interface.py
- Testes com diferentes tipos de input

**Arquivos a modificar:**
- Criar `utils/intent_detector.py`
- Modificar `components/chat_interface.py` para usar detecção

### Fase 4: Polimento e Otimização (1 semana)
**Objetivo**: Experiência fluida
- Melhorar indicadores visuais
- Otimizar performance
- Documentação e testes

## 5. Casos de Uso Implementados

### 5.1 Upload e Processamento (Usando estrutura atual)
1. **Usuário**: Arrasta CSV na aba Ferramentas
2. **Sistema**: Salva em `st.session_state['uploaded_files']`
3. **Chat**: Detecta arquivo e chama `file_processor.processar_automatico()`
4. **Resultado**: Usa `agents.query_agent` para análise de dados

### 5.2 Consulta RAG (Usando smartwiki existente)
1. **Usuário**: Ativa RAG na aba correspondente
2. **Sistema**: Executa `rag_service.ativar_rag()` 
3. **Chat**: Todas as mensagens passam por `rag_service.consultar_rag()`
4. **Resultado**: Resposta baseada na base de conhecimento

### 5.3 Processamento Multimodal
1. **Usuário**: Upload de imagem + pergunta
2. **Sistema**: `intent_detector` identifica imagem
3. **Chat**: Aplica OCR automaticamente
4. **Resultado**: Resposta baseada no texto extraído

## 6. Modificações Mínimas Necessárias

### 6.1 Arquivos Novos (3 arquivos)
- `services/rag_service.py` - Integração com smartwiki
- `services/file_processor.py` - Processamento automático
- `utils/intent_detector.py` - Seleção de agents

### 6.2 Arquivos Modificados (1 arquivo principal)
- `components/chat_interface.py` - Adicionar orquestração

### 6.3 Arquivos Movidos (1 arquivo)
- `smartwiki/rag_agent.py` → `agents/rag_agent.py`

## 7. Vantagens da Abordagem

### 7.1 Técnicas
- **Aproveitamento**: 90% do código atual mantido
- **Sem Breaking Changes**: Funcionalidades atuais preservadas
- **Incremental**: Implementação em fases testáveis
- **Modular**: Cada nova funcionalidade é um módulo independente

### 7.2 Produto
- **Experiência Unificada**: Uma interface, múltiplas funcionalidades
- **Controle**: Usuário mantém controle granular quando necessário
- **Flexibilidade**: Pode usar RAG, agents, ou ambos
- **Familiar**: Mantém UX atual, apenas aprimorada

## 8. Critérios de Sucesso

### 8.1 Fase 1
- ✅ Mudança de modo streamlit multipages para página única
- ✅ Upload funciona com processamento automático
- ✅ Arquivos são processados conforme tipo
- ✅ Feedback visual durante processamento

### 8.2 Fase 2
- ✅ RAG ativa/desativa 
- ✅ Consultas RAG funcionam corretamente
- ✅ Contexto é limpo na ativação

### 8.3 Fase 3
- ✅ Sistema seleciona agent apropriado automaticamente
- ✅ 90% de precisão na detecção de intenção
- ✅ Experiência fluida sem comandos explícitos

Este PRD ajustado mantém sua estrutura atual e adiciona melhorias incrementais, transformando o VeronIA numa plataforma unificada sem quebrar o que já funciona.