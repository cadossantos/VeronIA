from dotenv import load_dotenv
load_dotenv()
import os
import time
import streamlit as st

from db.db_sqlite import init_database, salvar_mensagem, atualizar_titulo_conversa
from utils.session_utils import init_session_state
from utils.constants import DEFAULT_PROVIDER, DEFAULT_MODEL
from services.model_service import carregar_modelo_cache
from services.memory_service import get_historico, reconstruir_memoria, adicionar_mensagem
from services.conversation_service import inicia_nova_conversa_service
from components.header import criar_header_fixo
from components.sidebar import render_sidebar 
from components.chat_interface import interface_chat


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
        page_title="JibóIA - VerônIA",
        page_icon="🔮",
        layout="wide"
    )
    
    init_database()
    init_session_state()
    inicializa_jiboia()
    render_sidebar()
    interface_chat()
    
if __name__ == '__main__':
    main()