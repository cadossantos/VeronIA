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

def inicia_nova_conversa_service(agent_type: str = 'chat_geral'):
    """Cria uma nova conversa e atualiza o estado da sessão para um tipo de agente específico."""
    st.session_state[f'historico_{agent_type}'] = []
    provedor = st.session_state.get('provedor', 'Groq')
    modelo = st.session_state.get('modelo', 'llama-3.3-70b-versatile')
    conversa_id = criar_conversa('Nova conversa', provedor, modelo)
    st.session_state[f'conversa_atual_{agent_type}'] = conversa_id
    st.cache_data.clear()
    if f'titulo_atualizado_{agent_type}' in st.session_state:
        del st.session_state[f'titulo_atualizado_{agent_type}']

def seleciona_conversa_service(conversa_id, agent_type: str = 'chat_geral'):
    """Carrega uma conversa existente para o estado da sessão para um tipo de agente específico."""
    mensagens = carregar_mensagens(conversa_id)
    st.session_state[f'historico_{agent_type}'] = mensagens
    st.session_state[f'conversa_atual_{agent_type}'] = conversa_id

def renomear_conversa_service(conversa_id, novo_titulo):
    """Renomeia uma conversa e atualiza a interface."""
    if novo_titulo.strip():
        atualizar_titulo_conversa(conversa_id, novo_titulo.strip())
        st.cache_data.clear()
        st.rerun()

def excluir_conversa_service(conversa_id):
    """Exclui uma conversa do banco e reseta o estado da sessão."""
    excluir_conversa(conversa_id)
    # Resetar o estado da sessão para todos os agentes que possam estar usando essa conversa
    for key in list(st.session_state.keys()):
        if key.startswith('conversa_atual_') and st.session_state[key] == conversa_id:
            st.session_state.pop(key, None)
        if key.startswith('historico_') and key.endswith(str(conversa_id)):
            st.session_state.pop(key, None)
    st.session_state.pop('confirmar_exclusao', None)
    st.session_state.pop('mostrar_input_renomear', None)
    st.cache_data.clear()
    st.rerun()
