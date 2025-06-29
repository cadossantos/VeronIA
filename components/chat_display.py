import streamlit as st

def renderiza_mensagens(historico, limite=10):
    """Renderiza as mensagens do histórico de chat."""
    for i, mensagem in enumerate(historico[-limite:]):
        with st.chat_message(mensagem['role']):
            if mensagem['role'] == 'assistant':
                # Mostra a resposta em um bloco copiável
                st.code(mensagem['content'], language='markdown')
            else:
                # Mensagem do usuário sem botão de cópia
                st.markdown(mensagem['content'])
