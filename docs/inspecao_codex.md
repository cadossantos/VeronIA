# Inspeção de Resquícios e Gaps da Funcionalidade RAG

A seguir vai um levantamento dos principais “resquícios” da antiga estrutura _smartwiki_ e dos gaps de integração que ainda existem para que a funcionalidade RAG (Retrieval‑Augmented Generation) fique totalmente operacional na aplicação principal.

---

## 1) Limpeza / remoção / reorganização dos artefatos do antigo “smartwiki”

No diretório `smartwiki/` (o MVP isolado que foi criado originalmente) ainda existem diversos arquivos e pastas duplicados na raiz do projeto ou não mais utilizados:

- **Repositório Git isolado**  
  Há um sub‑`.git` completo dentro de `smartwiki/`, indicando que era um repositório independente.  
  ```text
  smartwiki/.git/HEAD
  smartwiki/.git/config
  ...
  ```

- **Ambiente virtual interno**  
  A pasta `.venv/` contém todo o ambiente Python isolado, mas não é usado pelo projeto principal.  
  ```text
  smartwiki/.venv/bin/…
  smartwiki/.venv/lib/…
  ```

- **Gerenciamento próprio de dependências**  
  Há um `pyproject.toml` dentro de `smartwiki/` com configurações legadas que conflitam com o da raiz.

- **Código duplicado ou não consumido**  
  As implementações de RAG e crawling originais (em `smartwiki/agents/`, `smartwiki/crawler/`) não são referenciadas pelos serviços atuais na raiz.

- **Pasta de testes isolada**  
  Existem testes de ingestão e consulta em `smartwiki/tests/` que não são executados junto ao restante do projeto.

**Conclusão (parte 1):**  
Remover completamente o diretório `smartwiki/` (incluindo `.git`, `.venv`, testes e crawler legado) e, caso haja módulos úteis, extrair apenas o que for reaproveitável para `services/` ou `utils/`.

---

## 2) Gaps de integração e funcionalidades RAG ainda não implementadas

Mesmo com o core de RAG presente (`agents/rag_agent.py` e `services/rag_service.py`), há lacunas no fluxo que precisam ser fechadas para um suporte completo:

- **Workflow de indexação**  
  O botão “Indexar documentos” na aba de RAG do sidebar não chama efetivamente o serviço de ingestão (`services.ingest_service.ingest`) nem gera chunks.

- **Persistência de arquivos**  
  Os arquivos enviados pelo uploader de RAG permanecem em memória e não são salvos em disco (`db/pages`), portanto o ingest_service não os encontra.

- **Parâmetros hard‑coded**  
  Valores como `VECTOR_STORE_DIR`, `EMBEDDING_MODEL`, além de `chunk_size` e `overlap`, estão fixos nos módulos em vez de serem extraídos do `session_state` configurado pela UI.

- **Seleção estática de bases**  
  A lista de bases disponíveis (ex: ‘Documentos Gerais’, ‘Base Técnica’) é estática e não mapeia para collections reais do ChromaDB.

- **Botão “Atualizar Base” sem lógica**  
  Não existe chamada para reindexação no clique desse botão; apenas exibe uma mensagem de sucesso.

- **Métricas placeholders**  
  A seção de métricas de RAG exibe valores estáticos em vez de contadores reais de documentos e chunks.

### Próximos passos sugeridos

1. **Persistir uploads** em `db/pages` e invocar `services.ingest_service.ingest` com parâmetros da UI (chunk_size, overlap, modelo_embedding).  
2. **Consumir parâmetros dinâmicos** em `ingest_service` e `RagQueryEngine`, removendo valores hard‑coded.  
3. **Vincular seleção de base** ao diretório/collection correto de ChromaDB.  
4. **Exibir feedback real** de quantos documentos/chunks foram indexados e atualizar métricas de RAG dinamicamente.  
5. **Remover o diretório `smartwiki/`** e atualizar a documentação para refletir apenas a arquitetura atual.  

---

## Resumo

- Limpeza geral dos artefatos legados do MVP isolado _smartwiki_.  
- Implementação completa do fluxo end‑to‑end de RAG: indexação, persistência, consulta e métricas.  
- Atualização da documentação e remoção de duplicidades.




# codex

A seguir um plano de alto nível para dar ao usuário a capacidade de "apontar" novos links da SmartWiki via UI, gerar dinamicamente bases de conhecimento separadas (mais uma base "Todos") e unificar o logging.

## 1. Reaproveitamento do Crawler e unificação de logs

Extrair o crawler para "services/crawler/".
- Mova todos os módulos de smartwiki/crawler/ (fetcher, parser, storage, models, category_fetcher, config) para services/crawler/.
- Ajuste imports em cada arquivo (de from crawler.xxx import … para from services.crawler.xxx import …).

Unificar logger.
- Centralize o logger legadário de smartwiki/utils/logger.py em um único utils/logger.py.
- Substitua todos os prints no crawler, ingestão e RagQueryEngine por chamadas ao logger centralizado (e.g. logger.info(), logger.error()).

## 2. Fluxo de UI para "adicionar links" e criação de bases

### 2.1. Barra lateral (sidebar) – seção "Documentos para raspagem"

1. Adicionar expander "📄 Scramping".
2. Dentro dele, um campo de texto para url , um para nome da base de conhecimento + botão "➕ Iniciar Scramping".

```python
with tab.expander("📄 Scramping", expanded=False):
    link = st.text_input("URL da página / categoria SmartWiki", key="new_smartwiki_link")
    if st.button("➕ Adicionar Link"):
        # 1) Persistir esse link como é feito no arquivo smartwiki/utils/main..py
        # 2) Feedback ao usuário: "Link salvo"
```

3. Listagem dinâmica dos links já cadastrados, com opção de remover ou editar.

### 2.2. Persistência dos links e geração de bases

1.
Armazenar os links num JSON de configuração (e.g. db/smartwiki_links.json), no formato:

```json
{
  "bases": {
    "Todos": [],
    "base1": ["https://smartwiki/...", "..."],
    "base2": [        ]
  }
}
```

2.
Sempre que um link for adicionado/removido, regrave o JSON e exiba mensagem de sucesso.

3.
Opção "Todos"
- Initialize a estrutura com a base "Todos" (que agrega todos os links).
- Ao criar nova base (p.ex. "base3"), adicione-a também à "Todos" para efeito de raspagem completa.

### 2.3. Indexação (ingest) por base

1. No expander "📄 Documentos para indexação", substitua o uploader estático por:
   - Selectbox de bases disponíveis (lê as chaves do JSON db/smartwiki_links.json), incluindo "Todos".
   - Botão "📥 Indexar base selecionada".
2. Ao clicar em "Indexar base selecionada":
   - Carregue a lista de URLs daquela base.
   - Execute o crawler (services/crawler) para cada URL, gerando um JSON por página em db/pages/<nome da base>/….
   - Em seguida, invoque o serviço ingest(data_dir, vector_store_dir, collection_name, embeddings, chunk_size, overlap), usando parâmetros de chunk_size, overlap e embedding model vindos do session_state.

## 3. Parâmetros dinâmicos já disponíveis na UI

| Parâmetro UI         | Onde consumir                                                  |
|----------------------|---------------------------------------------------------------|
| Modelo de embedding  | st.session_state['modelo_embedding'] → ingest_service        |
| chunk_size, overlap  | st.session_state['chunk_size'], ['chunk_overlap'] → ingest_service |
| Relevância_threshold | pode ser usado para filtragem no retriever (opcional)        |

Na implementação do ingest(data_dir, vector_store_dir, collection_name, embeddings, chunk_size, overlap), passe estes valores em vez de usar constantes.

## 4. Métricas e feedback

1. Após cada indexação, retorne de ingest():
   - Quantidade de documentos raspados
   - Quantidade de chunks gerados
2. Atualize a seção "📊 Métricas" do sidebar (expander RAG) para exibir esses valores reais em vez dos placeholders.

## 5. Resumo do Roadmap

1. Mover e adaptar o crawler para services/crawler/ e unificar logger em utils/logger.py.
2. Persistir links da SmartWiki via UI num JSON (incluindo base "Todos").
3. Indexar bases individualmente: crawler → JSON pages → ingest → ChromaDB.
4. Consumir parâmetros dinâmicos de embedding, chunk_size e overlap.
5. Exibir métricas reais de documentos/chunks após indexação.

Com esse plano teremos um pipeline totalmente integrado: o usuário adiciona links, cria-se uma base, faz raspagem + ingestão parametrizada e, finalmente, consulta RAG com feedback de métricas. Depois de aprovado, podemos partir para a implementação.