import streamlit as st
from agents.rag_agent import RagQueryEngine
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from services.model_service import carregar_modelo_cache

@st.cache_resource
def get_rag_agent_cached(knowledge_base_name: str):
    """
    Cria e cacheia uma instância do RagQueryEngine para uma base específica ou para todas as bases.
    """
    embedding_model = st.session_state.get('modelo_embedding', 'text-embedding-3-small')
    k = st.session_state.get('rag_k', 10)
    
    # Carrega o modelo de linguagem principal da aplicação
    provedor = st.session_state.get('provedor', 'Groq')
    modelo_nome = st.session_state.get('modelo', 'llama-3.1-8b-instant')
    llm = carregar_modelo_cache(provedor, modelo_nome)

    if not llm:
        st.error("Não foi possível carregar o modelo de linguagem para o agente RAG.")
        return None

    try:
        if knowledge_base_name == "Todos":
            return RagQueryEngine(
                llm=llm,
                collection_names=None, # None para carregar todas as coleções
                embedding_model=embedding_model,
                k=k
            )
        else:
            return RagQueryEngine(
                llm=llm,
                collection_names=[knowledge_base_name],
                embedding_model=embedding_model,
                k=k
            )
    except (FileNotFoundError, ValueError) as e:
        st.error(f"Erro ao carregar base de conhecimento '{knowledge_base_name}': {e}")
        return None

def check_chroma_collection_count(knowledge_base_name: str) -> int:
    """
    Verifica e retorna a contagem de documentos em uma coleção específica do ChromaDB.
    Se knowledge_base_name for "Todos", retorna a soma das contagens de todas as coleções.
    """
    if knowledge_base_name == "Todos":
        total_count = 0
        all_bases = list_all_knowledge_bases()
        for base in all_bases:
            total_count += check_chroma_collection_count(base) # Chamada recursiva para somar
        return total_count
    
    vector_store_path = f"db/vector_store/{knowledge_base_name}"
    if not os.path.exists(vector_store_path):
        return 0
    try:
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

def get_scraped_document_count(knowledge_base_name: str) -> int:
    """
    Conta o número de documentos JSON raspados para uma base de conhecimento específica.
    Se knowledge_base_name for "Todos", retorna a soma das contagens de todas as bases raspadas.
    """
    if knowledge_base_name == "Todos":
        total_count = 0
        # Listar todos os diretórios em db/pages/ que representam bases raspadas
        scraped_bases_root = "db/pages"
        if not os.path.exists(scraped_bases_root):
            return 0
        
        for base_dir in os.scandir(scraped_bases_root):
            if base_dir.is_dir() and base_dir.name != "__pycache__":
                total_count += get_scraped_document_count(base_dir.name) # Chamada recursiva para somar
        return total_count

    data_dir = f"db/pages/{knowledge_base_name}"
    if not os.path.exists(data_dir):
        return 0
    
    count = 0
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            count += 1
    return count

def list_all_knowledge_bases() -> list[str]:
    """
    Lista todas as bases de conhecimento (coleções ChromaDB) disponíveis.
    """
    vector_store_root = "db/vector_store"
    if not os.path.exists(vector_store_root):
        return []
    
    bases = [d.name for d in os.scandir(vector_store_root) if d.is_dir()]
    return bases
