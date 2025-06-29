import streamlit as st
from db.db_sqlite import (
    criar_conversa,
    carregar_mensagens,
    atualizar_titulo_conversa,
    listar_conversas
)

from db.db_sqlite import excluir_conversa

@st.cache_data
def listar_conversas_cached():
    return listar_conversas()

def inicia_nova_conversa_service():
    """Cria uma nova conversa e atualiza o estado da sessão."""
    st.session_state['historico'] = []
    provedor = st.session_state.get('provedor', 'Groq')
    modelo = st.session_state.get('modelo', 'llama-3.3-70b-versatile')
    conversa_id = criar_conversa('Nova conversa', provedor, modelo)
    st.session_state['conversa_atual'] = conversa_id
    st.cache_data.clear()
    if 'titulo_atualizado' in st.session_state:
        del st.session_state['titulo_atualizado']

def seleciona_conversa_service(conversa_id):
    """Carrega uma conversa existente para o estado da sessão."""
    mensagens = carregar_mensagens(conversa_id)
    st.session_state['historico'] = mensagens
    st.session_state['conversa_atual'] = conversa_id

def renomear_conversa_service(conversa_id, novo_titulo):
    """Renomeia uma conversa e atualiza a interface."""
    if novo_titulo.strip():
        atualizar_titulo_conversa(conversa_id, novo_titulo.strip())
        st.cache_data.clear()
        st.rerun()

def excluir_conversa_service(conversa_id):
    """Exclui uma conversa do banco e reseta o estado da sessão."""
    excluir_conversa(conversa_id)
    st.session_state.pop('conversa_atual', None)
    st.session_state['historico'] = []
    st.session_state['confirmar_exclusao'] = False
    st.session_state['mostrar_input_renomear'] = False
    st.cache_data.clear()
    st.rerun()
