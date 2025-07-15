# Histórico de Alterações

## v0.1.8 - 2025-07-07

### Adicionado
- **Reestruturação da Página Principal**:
    - Criação do arquivo `main_chat_page.py` com layout de 3/5 para o chat e 2/5 para ferramentas.
    - Criação do componente `components/response_format.py` para seleção de estilos de resposta.
    - Criação do componente `components/mode_selector.py` para seleção de modos de operação.
    - Adicionados novos arquivos de prompt (`postit_prompt.txt`, `redator_prompt.txt`, `tradutor_prompt.txt`, `websearch_prompt.txt`) no diretório `prompts/`.
- **Integração do Módulo SmartWiki**:
    - Criação da página `pages/🔍_SmartSimple_RAG.py` para integrar a interface do agente RAG do SmartWiki.
    - Criação do diretório `scripts/` na raiz do projeto para scripts utilitários.

### Alterado
- **Refatoração da Página Principal**:
    - O arquivo `app.py` foi simplificado para redirecionar para `main_chat_page.py`.
    - A lógica de inicialização foi movida de `app.py` para `main_chat_page.py`.
    - O serviço `services/model_service.py` foi modificado para carregar prompts de sistema dinamicamente com base no modo de operação.
    - O arquivo `prompts/system_prompt.txt` foi renomeado para `prompts/normal_prompt.txt`.
- **Ajustes no Módulo SmartWiki**:
    - As dependências do `smartwiki/pyproject.toml` foram unificadas no `pyproject.toml` principal.
    - O arquivo `smartwiki/main.py` foi movido e renomeado para `scripts/run_crawler.py`.
    - O arquivo `smartwiki/rag/ingest.py` foi movido e renomeado para `scripts/run_ingest.py`.
    - Os caminhos de importação em `smartwiki/agents/app.py` e `smartwiki/crawler/storage.py` foram ajustados para serem relativos.
    - Os caminhos absolutos para os diretórios de dados foram corrigidos em `smartwiki/agents/query.py` e `scripts/run_ingest.py`.

### Removido
- Arquivos `smartwiki/pyproject.toml` e `smartwiki/poetry.lock`, pois as dependências foram unificadas.
- Arquivo `smartwiki/main.py` (movido para `scripts/run_crawler.py`).
- Arquivo `smartwiki/rag/ingest.py` (movido para `scripts/run_ingest.py`).

## v0.1.7 - 2025-07-05

### Refatorado
- **Aplicação dos Princípios SOLID**:
    - **Princípio da Responsabilidade Única (SRP)**: A função `interface_chat()` foi dividida em quatro funções especializadas.
    - **Don't Repeat Yourself (DRY)**: Foi criado o arquivo `utils/constants.py` para centralizar valores anteriormente duplicados.
    - **Separação de Interesses**: O prompt do sistema foi externalizado para `prompts/system_prompt.txt`.

### Corrigido
- **Vulnerabilidades de Segurança**:
    - O arquivo de banco de dados `db/veronia.db` foi removido do controle de versão.
    - Dependências críticas foram atualizadas para versões seguras no `pyproject.toml`.
- **Qualidade de Código**:
    - Variáveis não utilizadas foram removidas de `utils/configs.py`.
    - A duplicação de código foi eliminada com a criação do componente `components/chat_interface.py`.

### Melhorado
- **Tratamento de Erros**: Adicionado tratamento de erros robusto para carregamento de modelos, gerenciamento de chaves de API e interações com o banco de dados.
- **Arquitetura**:
    - A modularidade foi aprimorada com novos componentes e módulos de utilitários.
    - A manutenibilidade foi melhorada através da centralização de configurações.

## v0.1.6 - 2025-06-29

### Adicionado
- **Novos Modelos**: Adicionado o modelo `o4-mini-2025-04-16` e definido `llama-3.3-70b-versatile` como padrão.
- **Página Redator**: Criada a nova página `redator.py`.
- **Relatório de Inspeção**: Adicionado o arquivo `docs/relatorio_de_inspeção.md`.

### Alterado
- **Documentação**: Atualizados os arquivos `README.md` e `docs/overview.md`.
- **Barra Lateral**: A barra lateral agora exibe o nome da aplicação e permite a exclusão de conversas.
- **Temperatura do Modelo**: A temperatura padrão do modelo foi definida como `1`.
- **Modelo Padrão**: O modelo padrão foi atualizado para `llama-3.3-70b-versatile`.

## v0.1.5 - 2025-06-28

### Refatorado
- **Arquitetura Modular**: O projeto foi reorganizado em uma estrutura modular, desacoplando responsabilidades.

### Corrigido
- **Bug de `st.rerun()`**: Corrigido um erro crítico que interrompia a execução antes da geração da resposta do modelo.

### Melhorado
- **Desempenho**: Implementado cache para carregamento de modelos e listagem de conversas, e otimizado o uso de memória.
- **Experiência do Usuário**: Centralizada a lógica da barra lateral e melhorada a interface de renomeação de conversas.

## v0.1.4 - 2025-06-28

### Adicionado
- **Inicialização Automática**: Implementada a função `inicializa_jiboia()` para carregar um modelo padrão automaticamente.
- **Página Principal Unificada**: O arquivo `app.py` agora serve como a página principal da aplicação.
- **Experiência Zero-Config**: Os usuários podem iniciar uma conversa sem configuração manual.

### Alterado
- **Nome da Aplicação**: O nome foi alterado de "VeronIA" para "JibóIA".
- **Fluxo de Inicialização**: Removidos avisos de configuração obrigatória.

### Corrigido
- **Bug de Inicialização**: Resolvido um problema que causava falha na aplicação ao abrir sem um modelo configurado.

## v0.1.3 - 2025-06-29

### Corrigido
- Prevenida a ocorrência de `AttributeError` quando nenhuma conversa estava selecionada.
- Garantida a renderização correta da barra lateral em todas as páginas.

### Alterado
- Documentação atualizada para refletir o uso exclusivo do SQLite.
- Licença no `pyproject.toml` alinhada com o arquivo `LICENSE` (GPLv3).
- Dependências centralizadas no `pyproject.toml`.

## v0.1.2 - 2025-06-28

### Problemas Conhecidos
- A barra lateral não estava sendo renderizada corretamente na página `_Chat_Geral.py`.

## v0.1.1 - 2025-06-27

### Alterado
- **Migração do Banco de Dados**: O backend de persistência foi migrado de PostgreSQL para SQLite, simplificando a configuração local.

## v0.1.0 - 2025-06-27

### Adicionado
- **Fundação do Projeto**: Configuração inicial e documentação do projeto.
- **Documentação Abrangente**: Criação de `README.md`, `docs/overview.md`, entre outros.
- **Licenciamento**: O projeto foi licenciado sob a GPLv3.
- **Funcionalidade Principal**: Implementada a estrutura inicial da aplicação com Streamlit, suportando seleção de modelos e gerenciamento de conversas.
