
import streamlit as st
from langchain.memory import ConversationBufferMemory

def reconstruir_memoria(historico: list) -> ConversationBufferMemory:
    """Recria o objeto de memória a partir de um histórico em lista."""
    memoria = ConversationBufferMemory(return_messages=True)
    for msg in historico:
        if msg['role'] == 'user':
            memoria.chat_memory.add_user_message(msg['content'])
        else:
            memoria.chat_memory.add_ai_message(msg['content'])
    return memoria

def get_historico():
    """Retorna o histórico da sessão, inicializando se necessário."""
    if 'historico' not in st.session_state:
        st.session_state['historico'] = []
    return st.session_state['historico']
