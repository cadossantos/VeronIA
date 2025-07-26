import os
import streamlit as st
from services.crawler.fetcher import HtmlFetcher
from services.crawler.parser import WikiParser
from services.crawler.storage import PageStorage
from services.ingest_service import ingest
import logging

logger = logging.getLogger(__name__)

def raspar_links_e_salvar_paginas(base_name: str, initial_urls: list[str]):
    """
    Realiza o scraping recursivo de links e salva as páginas como arquivos JSON.
    Retorna o número de documentos processados.
    """
    if not initial_urls:
        st.warning(f"A base '{base_name}' não possui links para raspar.")
        return 0

    st.info(f"Iniciando scraping para a base '{base_name}'...")

    data_dir = f"db/pages/{base_name}"
    os.makedirs(data_dir, exist_ok=True)

    urls_a_visitar = list(initial_urls)
    urls_visitadas = set()
    documentos_processados = 0

    try:
        fetcher = HtmlFetcher()
        parser = WikiParser(base_url="https://wiki.smartsimple.com")
        storage = PageStorage(output_dir=data_dir)

        with st.spinner("Realizando scraping recursivo..."):
            while urls_a_visitar:
                url = urls_a_visitar.pop(0)
                if url in urls_visitadas:
                    continue

                st.write(f"🔎 Raspando: {url}")
                logger.info(f"Processando URL: {url}")
                urls_visitadas.add(url)

                html = fetcher.get_html(url)
                if html:
                    page = parser.parse(url, html)
                    
                    # Verifica se o arquivo já existe antes de salvar
                    filename = storage.sanitize_filename(page.title) or "untitled"
                    filepath = storage.output_dir / f"{filename}.json"
                    if filepath.exists():
                        logger.info(f"Página já existe no disco, pulando: {url}")
                    else:
                        storage.save_page(page)
                        documentos_processados += 1

                    # Adiciona novos links encontrados à fila para visitar
                    for link in page.links:
                        if link not in urls_visitadas and link not in urls_a_visitar:
                            urls_a_visitar.append(link)
                else:
                    logger.warning(f"Não foi possível obter HTML para a URL: {url}")
        st.write(f"✅ Scraping de {documentos_processados} página(s) concluído.")
        return documentos_processados

    except Exception as e:
        st.error(f"Ocorreu um erro durante o scraping: {e}")
        logger.error(f"Erro no scraping da base '{base_name}': {e}")
        return 0

def indexar_base_de_conhecimento(base_name: str):
    """
    Realiza a ingestão dos documentos JSON de uma base para o ChromaDB.
    Retorna o número de documentos e chunks indexados.
    """
    st.info(f"Iniciando indexação para a base '{base_name}'...")

    data_dir = f"db/pages/{base_name}"
    vector_store_dir = f"db/vector_store/{base_name}"
    os.makedirs(vector_store_dir, exist_ok=True) # Garante que o diretório do vector store exista

    try:
        with st.spinner("Realizando indexação dos documentos..."):
            chunk_size = st.session_state.get('chunk_size', 500)
            overlap = st.session_state.get('chunk_overlap', 400)
            embedding_model = st.session_state.get('modelo_embedding', 'text-embedding-3-small')

            logger.info(f"Iniciando ingestão para a base '{base_name}' com chunk_size={chunk_size}, overlap={overlap}.")
            num_docs, num_chunks = ingest(
                data_dir=data_dir,
                vector_store_dir=vector_store_dir,
                collection_name=base_name,
                chunk_size=chunk_size,
                overlap=overlap,
                embedding_model=embedding_model
            )
        st.write(f"✅ Indexação concluída: {num_docs} documentos, {num_chunks} chunks.")
        logger.info(f"Ingestão da base '{base_name}' concluída com sucesso. Documentos: {num_docs}, Chunks: {num_chunks}")
        return num_docs, num_chunks
    except Exception as e:
        st.error(f"Ocorreu um erro durante a indexação: {e}")
        logger.error(f"Erro na ingestão da base '{base_name}': {e}")
        return 0, 0
