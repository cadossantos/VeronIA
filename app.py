from dotenv import load_dotenv
load_dotenv()
import time
import streamlit as st

from db.db_sqlite import init_database, salvar_mensagem, atualizar_titulo_conversa
from utils.session_utils import init_session_state
from services.model_service import carregar_modelo_cache
from services.memory_service import reconstruir_memoria
from services.conversation_service import inicia_nova_conversa_service, seleciona_conversa_service
from components.header import criar_header_fixo
from components.sidebar import render_sidebar
from components.chat_display import render_chat_ui

def inicializa_jiboia():
    """Inicializa o modelo padrão se nenhum estiver carregado."""
    if not st.session_state.get('chain_chat_geral'):
        provedor = st.session_state.get('provedor', 'Groq')
        modelo = st.session_state.get('modelo', 'llama-3.3-70b-versatile')
        chain = carregar_modelo_cache(provedor, modelo, agent_type='chat_geral')
        if chain:
            st.session_state['chain_chat_geral'] = chain
            st.session_state['modelo_nome_chat_geral'] = f"{provedor} - {modelo}"

def processar_mensagem_chat_geral(prompt: str, historico: list) -> str:
    """
    Callback para processar a mensagem do usuário no chat geral.
    Lida com a lógica de backend: obter resposta do modelo, salvar no DB, etc.
    """
    conversa_atual = st.session_state.get('conversa_atual_chat_geral')
    if not conversa_atual:
        inicia_nova_conversa_service(agent_type='chat_geral')
        conversa_atual = st.session_state.get('conversa_atual_chat_geral')

    tempo_inicial = time.time()

    memoria = reconstruir_memoria(historico)
    
    # Invoca o modelo, transmite a resposta para a UI e retorna a string final
    resposta_final = st.write_stream(st.session_state['chain_chat_geral'].stream({
        'input': prompt,
        'chat_history': memoria.buffer_as_messages
    }))

    tempo_final = time.time()
    with st.sidebar:
        st.session_state['tempo_resposta'] = tempo_final - tempo_inicial

    # Salva a conversa no banco de dados
    if 'titulo_atualizado_chat_geral' not in st.session_state:
        atualizar_titulo_conversa(conversa_atual, prompt[:30])
        st.session_state['titulo_atualizado_chat_geral'] = True
        st.cache_data.clear()

    salvar_mensagem(conversa_atual, 'user', prompt)
    salvar_mensagem(conversa_atual, 'assistant', resposta_final)
    
    return resposta_final

def interface_chat():
    """Interface principal de chat da JibóIA."""
    st.session_state['current_page'] = 'chat_geral'
    
    criar_header_fixo()

    st.markdown('<div class="chat-main-area">', unsafe_allow_html=True)
    st.header('🔮 JibóIA - VerônIA', divider=True)

    if not st.session_state.get('chain_chat_geral'):
        st.info("🚀 **Inicializando JibóIA...** Por favor, aguarde alguns segundos.")

    if not st.session_state.get('conversa_atual_chat_geral'):
        st.info("👋 Olá! Sou a JibóIA. Como posso ajudar?")
        with st.expander("❓ Como usar"):
            st.markdown("""
            **JibóIA está pronta para uso:**
            1. ✅ Modelo já carregado automaticamente!
            2. ✅ Conversa iniciada automaticamente!
            3. 🚀 Comece a conversar agora mesmo!
            
            💡 **Dica:** Use a aba 'Config' para trocar de modelo.
            """)

    render_chat_ui(
        history_key=f'historico_{st.session_state["current_page"]}',
        on_submit_callback=processar_mensagem_chat_geral
    )

    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Ponto de entrada principal da aplicação Streamlit."""
    st.set_page_config(
        page_title="JibóIA - VerônIA",
        page_icon="🔮",
        layout="wide"
    )
    st.session_state['current_page'] = 'chat_geral' # Movido para o início da main
    
    init_database()
    init_session_state()
    inicializa_jiboia()
    render_sidebar()
    interface_chat()
    
if __name__ == '__main__':
    main()
