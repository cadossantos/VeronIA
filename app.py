from dotenv import load_dotenv
load_dotenv()
import streamlit as st

from db.db_sqlite import init_database
from utils.session_utils import init_session_state
from utils.constants import DEFAULT_PROVIDER, DEFAULT_MODEL
from services.model_service import carregar_modelo_cache
from components.sidebar import render_sidebar 
from components.chat_interface import interface_chat
from utils.style import apply_custom_css


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
    """Ponto de entrada principal da aplicação Streamlit."""
    st.set_page_config(
        page_title="Jibó.ia",
        page_icon="static/favicon.png",
        layout="wide"
    )
    
    init_database()
    init_session_state()
    apply_custom_css()
    inicializa_jiboia()
    render_sidebar()
    interface_chat()
    
if __name__ == '__main__':
    main()