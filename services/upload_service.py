import os
import streamlit as st
import tempfile
from dotenv import load_dotenv

from langchain_community.document_loaders import (
    WebBaseLoader,
    YoutubeLoader,
    CSVLoader,
    PyPDFLoader,
    TextLoader
)

load_dotenv()

def _carrega_site(url):
    """Carrega o conteúdo de uma URL de site."""
    loader = WebBaseLoader(url)
    documentos = loader.load()
    conteudo = '\n\n'.join([doc.page_content for doc in documentos])
    return conteudo.replace("{", "").replace("}", "")

def _carrega_youtube(url):
    """Carrega a transcrição de uma URL do YouTube."""
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False, language=['pt'])
    documentos = loader.load()
    return '\n\n'.join([doc.page_content for doc in documentos])

def _carrega_pdf(caminho_arquivo):
    """Carrega o conteúdo de um arquivo PDF."""
    loader = PyPDFLoader(caminho_arquivo)
    documentos = loader.load()
    return '\n\n'.join([doc.page_content for doc in documentos])

def _carrega_csv(caminho_arquivo):
    """Carrega o conteúdo de um arquivo CSV."""
    loader = CSVLoader(caminho_arquivo)
    documentos = loader.load()
    return '\n\n'.join([doc.page_content for doc in documentos])

def _carrega_txt(caminho_arquivo):
    """Carrega o conteúdo de um arquivo TXT."""
    loader = TextLoader(caminho_arquivo, encoding='utf-8')
    documentos = loader.load()
    return '\n\n'.join([doc.page_content for doc in documentos])

def carrega_arquivo(tipo_arquivo, arquivo):
    """
    Gerencia o carregamento de um arquivo ou URL com base no tipo selecionado,
    processa o conteúdo e o retorna como uma string.

    Args:
        tipo_arquivo (str): O tipo da fonte ('Site', 'YouTube', 'PDF', 'CSV', 'TXT').
        arquivo: O objeto do arquivo (para uploads) ou a string da URL.

    Returns:
        str ou None: O conteúdo processado ou None em caso de erro.
    """
    try:
        if tipo_arquivo in ['Site', 'YouTube']:
            if not arquivo or not arquivo.strip():
                st.warning('Por favor, insira uma URL válida.')
                return None
            with st.spinner(f"Carregando conteúdo de {arquivo}..."):
                if tipo_arquivo == 'Site':
                    return _carrega_site(arquivo)
                else:
                    return _carrega_youtube(arquivo)

        elif tipo_arquivo in ['PDF', 'CSV', 'TXT']:
            if not arquivo:
                st.warning(f'Por favor, faça o upload do arquivo {tipo_arquivo}.')
                return None
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{tipo_arquivo.lower()}") as temp_file:
                temp_file.write(arquivo.read())
                caminho_temp = temp_file.name

            with st.spinner(f"Processando arquivo {arquivo.name}..."):
                if tipo_arquivo == 'PDF':
                    conteudo = _carrega_pdf(caminho_temp)
                elif tipo_arquivo == 'CSV':
                    conteudo = _carrega_csv(caminho_temp)
                else: # TXT
                    conteudo = _carrega_txt(caminho_temp)
            
            os.remove(caminho_temp)
            return conteudo
        else:
            st.warning(f'Tipo de arquivo não suportado: {tipo_arquivo}')
            return None

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o conteúdo: {e}")
        return None
