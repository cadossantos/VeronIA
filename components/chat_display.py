import streamlit as st

def renderiza_mensagens(historico, limite=10):
    """Renderiza as mensagens do histórico de chat."""
    st.markdown("""
        <style>
            pre, code {
                white-space: pre-wrap !important;
                word-break: break-word !important;
            }
        </style>
        """, unsafe_allow_html=True)

    for i, mensagem in enumerate(historico[-limite:]):
        with st.chat_message(mensagem['role']):
            if mensagem['role'] == 'assistant':
                # Mostra a resposta em um bloco copiável
                st.code(mensagem['content'], language='markdown')
            else:
                # Mensagem do usuário sem botão de cópia
                st.markdown(mensagem['content'])

def render_chat_ui(history_key: str, on_submit_callback: callable):
    """
    Renderiza uma interface de chat completa e reutilizável.
    
    Args:
        history_key (str): A chave única no st.session_state para o histórico.
        on_submit_callback (callable): A função a ser chamada com o input do usuário.
    """
    # 1. Renderiza o histórico de mensagens existente
    renderiza_mensagens(st.session_state.get(history_key, []))

    # 2. Obtém o input do usuário
    if prompt := st.chat_input("Sua mensagem..."):
        # Adiciona a mensagem do usuário ao histórico e à UI
        historico = st.session_state.get(history_key, [])
        historico.append({"role": "user", "content": prompt})
        st.session_state[history_key] = historico
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # 3. Chama o callback para processar e obter a resposta
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                # O callback deve retornar a resposta como string
                resposta = on_submit_callback(prompt, historico)
                st.markdown(resposta)
        
        # 4. Adiciona a resposta do assistente ao histórico
        historico.append({"role": "assistant", "content": resposta})
        st.session_state[history_key] = historico
        st.rerun()
