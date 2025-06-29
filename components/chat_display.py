import streamlit as st

def renderiza_mensagens(historico, limite=10):
    """Renderiza as mensagens do histórico de chat."""
    for mensagem in historico[-limite:]:
        with st.chat_message(mensagem['role']):
            st.markdown(mensagem['content'])