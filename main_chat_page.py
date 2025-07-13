from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from components.chat_interface import interface_chat
from components.sidebar import render_sidebar
from components.response_format import render_response_format_selector
from components.mode_selector import render_mode_selector
from db.db_sqlite import init_database
from utils.session_utils import init_session_state
from services.model_service import carregar_modelo_cache
from utils.constants import DEFAULT_PROVIDER, DEFAULT_MODEL

def inicializa_jiboia():
    """Inicializa o modelo padrão se nenhum estiver carregado."""
    if not st.session_state.get('chain'):
        provedor = st.session_state.get('provedor', DEFAULT_PROVIDER)
        modelo = st.session_state.get('modelo', DEFAULT_MODEL)
        chain = carregar_modelo_cache(provedor, modelo)
        if chain:
            st.session_state['chain'] = chain
            st.session_state['modelo_nome'] = f"{provedor} - {modelo}"

def main():
    st.set_page_config(
        page_title="JibóIA - VerônIA",
        page_icon="🔮",
        layout="wide"
    )
    init_database()
    init_session_state()
    inicializa_jiboia()
    render_sidebar()

    col1, col2 = st.columns([5, 1])

    with col1:
        interface_chat()

    with col2:
        st.write("")
        st.header("Ferramentas")
        render_mode_selector()
        render_response_format_selector()

if __name__ == '__main__':
    main()