import streamlit as st
import os
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from utils.configs import config_modelos # Importar config_modelos

# Constantes para configuração
VECTOR_STORE_BASE_DIR = "smartwiki/data/vector_store"
EMBEDDING_MODEL = "text-embedding-3-small"

@st.cache_resource
def get_rag_chain(collection_name: str = "default"):
    """
    Cria e cacheia uma ConversationalRetrievalChain para uma coleção de documentos específica.

    Args:
        collection_name (str): O nome da coleção (subdiretório) a ser carregada.

    Returns:
        A `ConversationalRetrievalChain` configurada.
    """
    persist_directory = os.path.join(VECTOR_STORE_BASE_DIR, collection_name if collection_name != "default" else "")

    if not os.path.exists(persist_directory) or not os.path.isdir(persist_directory):
        st.error(f"A coleção '{collection_name}' não foi encontrada no diretório esperado.")
        return None

    # 1. Inicializar o modelo de embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    # 2. Carregar o Vector Store a partir do disco
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory,
        collection_name="smartwiki_docs" # Este nome parece ser fixo na sua ingestão
    )

    # 3. Criar o retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    # 4. Configurar a memória da conversa
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # 5. Inicializar o LLM usando as configurações da sidebar
    provedor = st.session_state.get('provedor', 'Groq')
    modelo = st.session_state.get('modelo', 'llama-3.1-8b-instant')

    chat_class = config_modelos[provedor]['chat']
    
    if provedor == 'Ollama':
        llm = chat_class(model=modelo)
    else:
        api_key = os.getenv(f"{provedor.upper()}_API_KEY")
        if not api_key:
            st.error(f"API key para {provedor} não encontrada no ambiente.")
            return None
        llm = chat_class(model=modelo, api_key=api_key, temperature=0)

    # 6. Montar a chain de RAG
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        output_key="answer",
        verbose=False # Mantenha False para não poluir os logs
    )

    return qa_chain
