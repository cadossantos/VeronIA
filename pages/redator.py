import streamlit as st
import time

from db.db_sqlite import salvar_mensagem, atualizar_titulo_conversa
from services.memory_service import reconstruir_memoria
from services.conversation_service import inicia_nova_conversa_service
from components.header import criar_header_fixo
from components.chat_display import render_chat_ui
from services.model_service import carregar_modelo_cache # Importar para carregar o modelo
from components.sidebar import render_sidebar # Importar render_sidebar

# Configuração da página
st.set_page_config(
    page_title="JibóIA - Redator Profissional",
    page_icon="✍️",
    layout="wide"
)

st.session_state['current_page'] = 'redator' # Movido para o início do arquivo

render_sidebar() # Chamada para renderizar a sidebar

def inicializa_redator():
    """Inicializa o modelo padrão para o redator se nenhum estiver carregado."""
    if not st.session_state.get('chain_redator'): # Usar uma chave diferente para o redator
        provedor = st.session_state.get('provedor', 'Groq')
        modelo = st.session_state.get('modelo', 'llama-3.3-70b-versatile')
        # Carregar o modelo com um prompt específico para o redator
        chain = carregar_modelo_cache(provedor, modelo, agent_type='redator')
        if chain:
            st.session_state['chain_redator'] = chain
            st.session_state['modelo_nome_redator'] = f"{provedor} - {modelo} (Redator)"

def processar_mensagem_redator(prompt: str, historico: list) -> str:
    """
    Callback para processar a mensagem do usuário no chat do Redator.
    """
    conversa_atual = st.session_state.get('conversa_atual_redator') # Usar conversa_atual_redator
    if not conversa_atual:
        # Iniciar uma nova conversa específica para o redator
        inicia_nova_conversa_service(agent_type='redator')
        conversa_atual = st.session_state.get('conversa_atual_redator')

    tempo_inicial = time.time()

    memoria = reconstruir_memoria(historico)
    
    # Invoca o modelo específico do redator
    resposta_final = st.write_stream(st.session_state['chain_redator'].stream({
        'input': prompt,
        'chat_history': memoria.buffer_as_messages
    }))

    tempo_final = time.time()
    with st.sidebar:
        st.session_state['tempo_resposta_redator'] = tempo_final - tempo_inicial

    # Salva a conversa no banco de dados (adaptar para o redator)
    if 'titulo_atualizado_redator' not in st.session_state:
        atualizar_titulo_conversa(conversa_atual, prompt[:30])
        st.session_state['titulo_atualizado_redator'] = True
        st.cache_data.clear()

    salvar_mensagem(conversa_atual, 'user', prompt)
    salvar_mensagem(conversa_atual, 'assistant', resposta_final)
    
    return resposta_final

def interface_chat():
    """Interface principal de chat do Redator Profissional."""
    
    criar_header_fixo() # Pode ser adaptado para o redator

    st.markdown('<div class="chat-main-area">', unsafe_allow_html=True)
    st.header('✍️ Redator Profissional', divider=True)

    inicializa_redator()

    if not st.session_state.get('chain_redator'):
        st.info("🚀 **Inicializando Redator...** Por favor, aguarde alguns segundos.")

    if not st.session_state.get('conversa_atual_redator'):
        st.info("👋 Olá! Sou o Redator Profissional. Como posso ajudar?")
        with st.expander("❓ Como usar"):
            st.markdown("""
            **Redator Profissional está pronto para uso:**
            1. ✅ Modelo já carregado automaticamente!
            2. ✅ Conversa iniciada automaticamente!
            3. 🚀 Comece a conversar agora mesmo!
            
            💡 **Dica:** Use a aba 'Config' para trocar de modelo.
            """)

    render_chat_ui(
        history_key=f'historico_{st.session_state["current_page"]}',
        on_submit_callback=processar_mensagem_redator
    )

    st.markdown('</div>', unsafe_allow_html=True)

interface_chat()
