import streamlit as st
import time
from db.db_sqlite import salvar_mensagem, atualizar_titulo_conversa
from services.memory_service import get_historico, reconstruir_memoria, adicionar_mensagem
from services.conversation_service import inicia_nova_conversa_service
from utils.constants import (
    HEADER_TITLE, INITIALIZING_MESSAGE, WELCOME_MESSAGE,
    USAGE_INSTRUCTIONS, CHAT_INPUT_PLACEHOLDER, TITLE_TRUNCATE_LENGTH,
    CHAT_MESSAGE_LIMIT
)

def renderiza_mensagens(historico, limite=CHAT_MESSAGE_LIMIT):
    """Renderiza as mensagens do histórico de chat."""
    for msg in historico[-limite:]:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

def render_chat_ui():
    """Renderiza a interface básica do chat."""
    st.header(HEADER_TITLE, divider=True)
    if not st.session_state.get('chain') and not st.session_state.get('rag_mode', False):
        st.info(INITIALIZING_MESSAGE)
    
    conversa_atual = st.session_state.get('conversa_atual')
    if not conversa_atual and not st.session_state.get('rag_mode', False):
        st.info(WELCOME_MESSAGE)
        with st.expander("❓ Como usar"):
            st.markdown(USAGE_INSTRUCTIONS)

def process_normal_response(input_usuario, memoria):
    """Processa a resposta do modelo de chat normal."""
    with st.chat_message('assistant'):
        try:
            return st.write_stream(st.session_state['chain'].stream({
                'input': input_usuario,
                'chat_history': memoria.buffer_as_messages
            }))
        except Exception as e:
            st.error(f"Erro ao processar resposta: {str(e)}")
            return None

def process_rag_response(input_usuario, rag_func):
    """Processa a resposta do agente RAG."""
    with st.chat_message('assistant'):
        try:
            resposta, _ = rag_func(input_usuario)
            st.markdown(resposta)
            return resposta
        except Exception as e:
            st.error(f"Erro ao consultar o agente RAG: {str(e)}")
            return None

def handle_user_input(input_usuario, rag_func=None):
    """Processa a entrada do usuário, decidindo entre o modo normal e RAG."""
    tempo_inicial = time.time()
    rag_mode = st.session_state.get('rag_mode', False)

    adicionar_mensagem(st.session_state.historico, 'user', input_usuario)
    
    if rag_mode:
        if not rag_func:
            st.error("Função do agente RAG não fornecida.")
            return
        resposta = process_rag_response(input_usuario, rag_func)
    else:
        conversa_atual = st.session_state.get('conversa_atual')
        if not conversa_atual:
            inicia_nova_conversa_service()
            st.session_state.conversa_atual = st.session_state.get('conversa_atual')
        memoria = reconstruir_memoria(st.session_state.historico)
        resposta = process_normal_response(input_usuario, memoria)

    if resposta is None:
        return

    adicionar_mensagem(st.session_state.historico, 'assistant', resposta)
    
    if not rag_mode:
        save_conversation(st.session_state.conversa_atual, input_usuario, resposta)

    tempo_final = time.time()
    with st.sidebar:
        st.session_state['tempo_resposta'] = tempo_final - tempo_inicial
    
    st.rerun()

def save_conversation(conversa_atual, input_usuario, resposta):
    """Salva a conversa no banco de dados."""
    if 'titulo_atualizado' not in st.session_state:
        atualizar_titulo_conversa(conversa_atual, input_usuario[:TITLE_TRUNCATE_LENGTH])
        st.session_state['titulo_atualizado'] = True
        st.cache_data.clear()
    
    try:
        salvar_mensagem(conversa_atual, 'user', input_usuario)
        salvar_mensagem(conversa_atual, 'assistant', resposta)
    except Exception as e:
        st.error(f"Erro ao salvar mensagens: {str(e)}")

def interface_chat(perguntar_ao_agent_func=None):
    """Interface principal de chat da JibóIA."""
    render_chat_ui()
    
    historico = get_historico()
    renderiza_mensagens(historico)
    
    input_usuario = st.chat_input(CHAT_INPUT_PLACEHOLDER)
    
    if input_usuario:
        handle_user_input(input_usuario, rag_func=perguntar_ao_agent_func)
