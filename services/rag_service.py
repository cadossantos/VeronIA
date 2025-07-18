import streamlit as st
from agents.rag_agent import RagQueryEngine, VECTOR_STORE_DIR, COLLECTION_NAME, EMBEDDING_MODEL

def get_rag_agent():
    """Retorna uma instância do RagQueryEngine, criando-a se não existir no session_state."""
    if 'rag_agent_instance' not in st.session_state:
        st.session_state['rag_agent_instance'] = RagQueryEngine(
            vector_store_dir=VECTOR_STORE_DIR,
            collection_name=COLLECTION_NAME,
            embedding_model=EMBEDDING_MODEL
        )
    return st.session_state['rag_agent_instance']

def consultar_base_de_conhecimento(query: str) -> str:
    """Consulta a base de conhecimento RAG e retorna a resposta."""
    agent = get_rag_agent()
    if agent is None:
        return ""
    try:
        resposta, _ = agent.query(query)
        return resposta
    except Exception as e:
        st.error(f"Erro ao consultar base de conhecimento RAG: {e}")
        return "Desculpe, não consegui consultar a base de conhecimento no momento."
