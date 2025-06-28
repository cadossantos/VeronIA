
import streamlit as st
import os
from langchain.prompts import ChatPromptTemplate
from utils.configs import config_modelos

@st.cache_resource
def carregar_modelo_cache(provedor, modelo):
    """Carrega e cacheia o modelo de linguagem."""
    system_prompt = f'''
        Você é um assistente atencioso aos detalhes.
        '''

    template = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chat_class = config_modelos[provedor]['chat']
    
    if provedor == 'Ollama':
        chat = chat_class(model=modelo)
    else:
        api_key = os.getenv(f"{provedor.upper()}_API_KEY")
        if not api_key:
            st.error(f"API key para {provedor} não encontrada no .env.")
            return None
        chat = chat_class(model=modelo, api_key=api_key)
    
    return template | chat
