## PRD - VeronIA Multi-Agent Platform

1. Visão do Produto
Transformar o VeronIA em uma central multimodal com ferramentas inteligentes ativáveis, integrando OCR, transcrição, tradução e escrita institucional dentro de um chat principal fluido, com suporte a respostas personalizáveis, mantendo agentes especialistas como páginas separadas.

2. Arquitetura Conceitual
scss
Copiar
Editar
VeronIA Platform
├── 🧠 Página Principal - VerônIA Multitool (chat + ferramentas)
│   ├── Upload inteligente (PDF, imagem, áudio)
│   ├── OCR e Transcrição embutidos
│   ├── Modos ativáveis (Post-it, Redator, Tradutor, Web)
│   ├── Personalização da resposta (estilo Claude AI)
│   └── Memória e contexto estruturados
├── 📊 Análise de Dados (painéis, CSVs, dashboards)
├── 👥 Gestão de Equipe (formulários, processos, avaliações)
├── 🔍 Especialista SmartSimple (consultor técnico com RAG)
└── ⚙️ Configurações Globais (modelo, provedor, chave)
3. Página Principal (Chat Geral)
3.1 Layout 3/5 + 2/5
Área	Conteúdo
3/5 - Centro	Chat clássico com histórico, resposta, input
2/5 - Direita	Upload inteligente + ferramentas + seleção de modos e estilo de resposta

3.2 Funcionalidades
Upload inteligente: detecta tipo (pdf, jpg, mp3, etc.) e aplica:

PDF: leitura de texto

Imagem: OCR automático

Áudio: transcrição (Whisper local ou API)

Modos ativáveis (muda prompt e ferramentas ativas):

Normal, Post-it, Redator, Tradutor, Web Search

Formato de resposta:

Curta | Detalhada | Lista com bullets | Código | Resumo executivo

Histórico persistente com SQLite

Tempo de resposta exibido

Suporte a comandos no input (@modo, @traduzir, etc.)

4. Agentes Especiais (Permanecem como páginas)
Agente	Motivo
📊 DataVerô	Visualização interativa e análise CSV/tabular
👥 GestãoSábia	Processamento estruturado de formulários
🔍 RegistreRAG	Recuperação sobre base SmartSimple com painel de documentos

5. Estrutura Técnica Atualizada
text
Copiar
Editar
veronia/
├── app.py                      # Redireciona para página principal
├── pages/
│   ├── 📊_Análise_de_Dados.py
│   ├── 👥_Gestão_Equipe.py
│   └── 🔍_SmartSimple_RAG.py
├── main_chat_page.py           # Nova página principal com layout 3/5 + 2/5
├── agents/
│   ├── base_agent.py
│   └── multitool_agent.py      # Responsável por lidar com modos
├── tools/
│   ├── base_tools.py
│   ├── upload_processor.py     # Detecta tipo e chama OCR/transcrição/etc.
│   ├── ocr_tools.py
│   ├── audio_tools.py
│   └── response_format.py      # Módulo para controlar estilo das respostas
├── prompts/
│   ├── multitool_prompts.py    # Prompt base + variações por modo
├── components/
│   ├── header.py
│   ├── sidebar.py              # Permanece leve
│   ├── chat_display.py
│   ├── file_uploader.py
│   └── tools_panel.py          # Nova coluna 2/5 da direita
