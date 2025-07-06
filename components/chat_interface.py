import streamlit as st
import time

from db.db_sqlite import salvar_mensagem, atualizar_titulo_conversa
from services.memory_service import get_historico, reconstruir_memoria, adicionar_mensagem
from services.conversation_service import inicia_nova_conversa_service
from components.header import criar_header_fixo
from utils.constants import (
    HEADER_TITLE, INITIALIZING_MESSAGE, WELCOME_MESSAGE,
    USAGE_INSTRUCTIONS, CHAT_INPUT_PLACEHOLDER, TITLE_TRUNCATE_LENGTH,
    CHAT_MESSAGE_LIMIT
)


def renderiza_mensagens(historico, limite=CHAT_MESSAGE_LIMIT):
    """Renderiza as mensagens do histórico de chat."""
    st.markdown("""
    <style>
    .mensagem-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 1em;
        max-width: 80%;
    }

    .mensagem-user {
        align-self: flex-end;
        background-color: #444;
        color: white;
        border-radius: 12px;
        padding: 0.6em 1em;
    }

    .mensagem-assistente {
        align-self: flex-start;
        background-color: #222;
        color: white;
        border-radius: 12px;
        padding: 0.6em 1em;
    }

    .icone-label {
        font-size: 1.6rem;
        color: #aaa;
        margin-bottom: 0.5em;
    }
    </style>
    """, unsafe_allow_html=True)

    for msg in historico[-limite:]:
        role = msg['role']
        content = msg['content']
        if role == 'user':
            st.markdown(f"""
            <div class="mensagem-container">
                <div class="icone-label"> <br> </div>
                <div class="mensagem-user">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensagem-container">
                <div class="icone-label">🔮</div>
                <div class="mensagem-assistente">{content}</div>
            </div>
            """, unsafe_allow_html=True)


def render_chat_ui():
    """Renderiza a interface básica do chat."""
    criar_header_fixo()
    st.markdown('<div class="chat-main-area">', unsafe_allow_html=True)
    st.header(HEADER_TITLE, divider=True)
    
    if not st.session_state.get('chain'):
        st.info(INITIALIZING_MESSAGE)
    
    conversa_atual = st.session_state.get('conversa_atual')
    if not conversa_atual:
        st.info(WELCOME_MESSAGE)
        with st.expander("❓ Como usar"):
            st.markdown(USAGE_INSTRUCTIONS)


def process_ai_response(input_usuario, memoria):
    """Processa a resposta da IA."""
    tempo_inicial = time.time()
    
    with st.chat_message('ai'):
        try:
            resposta = st.write_stream(st.session_state['chain'].stream({
                'input': input_usuario,
                'chat_history': memoria.buffer_as_messages
            }))
        except Exception as e:
            st.error(f"Erro ao processar resposta: {str(e)}")
            return None
    
    tempo_final = time.time()
    with st.sidebar:
        st.session_state['tempo_resposta'] = tempo_final - tempo_inicial
    
    return resposta


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


def handle_user_input(input_usuario):
    """Processa a entrada do usuário."""
    conversa_atual = st.session_state.get('conversa_atual')
    historico = get_historico()
    
    if not conversa_atual:
        inicia_nova_conversa_service()
        conversa_atual = st.session_state.get('conversa_atual')
        historico = get_historico()
    
    adicionar_mensagem(historico, 'user', input_usuario)
    memoria = reconstruir_memoria(historico)
    
    resposta = process_ai_response(input_usuario, memoria)
    if resposta is None:
        return
    
    adicionar_mensagem(historico, 'assistant', resposta)
    st.session_state['historico'] = historico
    
    save_conversation(conversa_atual, input_usuario, resposta)
    st.rerun()


def interface_chat():
    """Interface principal de chat da JibóIA."""
    render_chat_ui()
    
    historico = get_historico()
    renderiza_mensagens(historico)
    
    input_usuario = st.chat_input(CHAT_INPUT_PLACEHOLDER)
    
    if input_usuario:
        handle_user_input(input_usuario)
    
    st.markdown('</div>', unsafe_allow_html=True)