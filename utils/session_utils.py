import streamlit as st
import os
from utils.constants import DEFAULT_PROVIDER, DEFAULT_MODEL

def init_session_state():
    """Inicializa o estado da sessão com valores padrão."""
    defaults = {
        'historico': [],
        'conversa_atual': '',
        'api_key': os.getenv("OPENAI_API_KEY", ""),
        'chain': None,
        'modelo_nome': 'Nenhum modelo carregado',
        'provedor': DEFAULT_PROVIDER,
        'modelo': DEFAULT_MODEL
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value