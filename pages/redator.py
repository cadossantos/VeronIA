import streamlit as st
import time

from db.db_sqlite import salvar_mensagem, atualizar_titulo_conversa
from services.memory_service import get_historico, reconstruir_memoria, adicionar_mensagem
from services.conversation_service import inicia_nova_conversa_service
from components.header import criar_header_fixo
from components.chat_display import renderiza_mensagens

st.set_page_config(
    page_title="JibóIA - Chat Geral",
    page_icon="🔮",
    layout="wide"
)

def interface_chat():
    """Interface principal de chat da JibóIA."""
    criar_header_fixo()

    st.markdown('<div class="chat-main-area">', unsafe_allow_html=True)
    st.header('🔮 JibóIA - VerônIA', divider=True)

    if not st.session_state.get('chain'):
        st.info("🚀 **Inicializando JibóIA...** Por favor, aguarde alguns segundos.")

    conversa_atual = st.session_state.get('conversa_atual')
    historico = get_historico()

    if not conversa_atual:
        st.info("👋 Olá! Sou a JibóIA. Como posso ajudar?")
        with st.expander("❓ Como usar"):
            st.markdown("""
            **JibóIA está pronta para uso:**
            1. ✅ Modelo já carregado automaticamente!
            2. ✅ Conversa iniciada automaticamente!
            3. 🚀 Comece a conversar agora mesmo!
            
            💡 **Dica:** Use a aba 'Config' para trocar de modelo.
            """)

    renderiza_mensagens(historico)

    input_usuario = st.chat_input('Fale com a JibóIA...')

    if input_usuario:
        if not conversa_atual:
            inicia_nova_conversa_service()
            conversa_atual = st.session_state.get('conversa_atual')
            historico = get_historico()

        tempo_inicial = time.time()

        adicionar_mensagem(historico, 'user', input_usuario)

        memoria = reconstruir_memoria(historico)
        
        with st.chat_message('ai'):
            resposta = st.write_stream(st.session_state['chain'].stream({
                'input': input_usuario,
                'chat_history': memoria.buffer_as_messages
            }))

        tempo_final = time.time()
        with st.sidebar:
            st.session_state['tempo_resposta'] = tempo_final - tempo_inicial

        adicionar_mensagem(historico, 'assistant', resposta)
        st.session_state['historico'] = historico

        if 'titulo_atualizado' not in st.session_state:
            atualizar_titulo_conversa(conversa_atual, input_usuario[:30])
            st.session_state['titulo_atualizado'] = True
            st.cache_data.clear()

        salvar_mensagem(conversa_atual, 'user', input_usuario)
        salvar_mensagem(conversa_atual, 'assistant', resposta)
        
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

interface_chat()