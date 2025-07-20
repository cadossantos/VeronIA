import streamlit as st
from agents.rag_agent import RagQueryEngine
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

@st.cache_resource
def get_rag_agent_cached(knowledge_base_name: str):
    """
    Cria e cacheia uma instância do RagQueryEngine para uma base específica.
    """
    vector_store_path = f"db/vector_store/{knowledge_base_name}"
    embedding_model = st.session_state.get('modelo_embedding', 'text-embedding-3-small')
    
    try:
        return RagQueryEngine(
            vector_store_path=vector_store_path,
            collection_name=knowledge_base_name,
            embedding_model=embedding_model
        )
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar base de conhecimento '{knowledge_base_name}': {e}")
        return None

def check_chroma_collection_count(knowledge_base_name: str) -> int:
    """
    Verifica e retorna a contagem de documentos em uma coleção específica do ChromaDB.
    """
    vector_store_path = f"db/vector_store/{knowledge_base_name}"
    if not os.path.exists(vector_store_path):
        return 0
    try:
        # Usar um embedding function dummy se não for necessário para a contagem
        # ou carregar o mesmo que foi usado na ingestão
        embeddings = OpenAIEmbeddings(model=st.session_state.get('modelo_embedding', 'text-embedding-3-small'))
        vectordb = Chroma(persist_directory=vector_store_path, embedding_function=embeddings, collection_name=knowledge_base_name)
        return vectordb._collection.count()
    except Exception as e:
        st.error(f"Erro ao verificar contagem da coleção ChromaDB para '{knowledge_base_name}': {e}")
        return -1

def consultar_base_de_conhecimento(query: str, knowledge_base_name: str) -> str:
    """
    Consulta a base de conhecimento RAG especificada.
    """
    if not knowledge_base_name:
        st.warning("Nenhuma base de conhecimento selecionada para a consulta RAG.")
        return "Desculpe, nenhuma base selecionada para consulta."
        
    agent = get_rag_agent_cached(knowledge_base_name)
    if agent is None:
        return "Desculpe, não foi possível carregar a base de conhecimento selecionada."
    try:
        resposta, _ = agent.query(query)
        return resposta
    except Exception as e:
        st.error(f"Erro ao consultar base de conhecimento RAG: {e}")
        return "Desculpe, não consegui consultar a base de conhecimento no momento."
