import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv
from smartwiki.agents.query import perguntar_ao_agent
from utils.configs import config_modelos

# Carregar variáveis de ambiente
load_dotenv()

st.set_page_config(page_title="SmartSimple RAG", page_icon="🔍")

def initialize_session_state():
    """Inicializa o estado da sessão se não estiver presente."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_initialized" not in st.session_state:
        st.session_state.rag_initialized = False
    if "provedor" not in st.session_state:
        st.session_state.provedor = list(config_modelos.keys())[0]
    if "modelo" not in st.session_state:
        st.session_state.modelo = config_modelos[st.session_state.provedor]["modelos"][0]

def model_selector():
    """Cria os seletores de provedor e modelo na barra lateral."""
    provedor = st.sidebar.selectbox(
        "Selecione o provedor",
        list(config_modelos.keys()),
        index=list(config_modelos.keys()).index(st.session_state.provedor),
    )
    if provedor != st.session_state.provedor:
        st.session_state.provedor = provedor
        st.session_state.modelo = config_modelos[provedor]["modelos"][0]

    modelo = st.sidebar.selectbox(
        "Selecione o modelo",
        config_modelos[st.session_state.provedor]["modelos"],
        index=config_modelos[st.session_state.provedor]["modelos"].index(st.session_state.modelo),
    )
    if modelo != st.session_state.modelo:
        st.session_state.modelo = modelo

def setup_sidebar():
    """Configura a barra lateral com a seleção de modelo."""
    st.sidebar.header("Configurações")
    model_selector()
    st.sidebar.info(f"Modelo ativo: **{st.session_state.provedor} - {st.session_state.modelo}**")
    st.sidebar.warning("O modelo do RAG é fixo (OpenAI) e não é afetado pela seleção acima.")

def check_rag_readiness():
    """Verifica se o agente RAG está pronto para ser usado."""
    if not st.session_state.rag_initialized:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            st.session_state.rag_initialized = True
            st.sidebar.success("RAG Agent pronto para uso!")
        else:
            st.sidebar.warning("Chave da API da OpenAI não encontrada. Por favor, configure-a no arquivo .env.")
            st.session_state.rag_initialized = False
    return st.session_state.rag_initialized

def handle_user_input():
    """Processa a entrada do usuário e obtém a resposta do RAG Agent."""
    user_input = st.chat_input("Digite sua mensagem aqui...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Pensando..."):
            if st.session_state.rag_initialized:
                try:
                    response, sources = perguntar_ao_agent(user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Erro ao consultar o RAG Agent: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": "Ocorreu um erro ao processar sua solicitação."})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "RAG Agent não está inicializado. Verifique a chave da API OpenAI no .env."})

def display_chat():
    """Exibe o histórico do chat."""
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            message(msg["content"], is_user=True, key=f"msg_{i}_user")
        else:
            message(msg["content"], is_user=False, key=f"msg_{i}_assistant")

def main():
    """Função principal da aplicação."""
    st.title("🔍 SmartSimple RAG")
    st.markdown("Use o poder do RAG para obter respostas baseadas em conhecimento.")

    initialize_session_state()
    setup_sidebar()
    check_rag_readiness()

    display_chat()
    handle_user_input()

if __name__ == "__main__":
    main()
