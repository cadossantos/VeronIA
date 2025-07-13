import streamlit as st
import os
from pathlib import Path
from langchain.prompts import ChatPromptTemplate
from utils.configs import config_modelos


@st.cache_resource
def carregar_modelo_cache(provedor, modelo):
    """Carrega e cacheia o modelo de linguagem."""
    try:
        # Define o modo de operação, com fallback para 'Normal'
        modo = st.session_state.get('operation_mode', 'Normal').lower().replace(" ", "")
        prompt_filename = f"{modo}_prompt.txt"
        prompt_path = Path(__file__).parent.parent / 'prompts' / prompt_filename

        # Fallback para o prompt normal se o arquivo do modo não existir
        if not prompt_path.is_file():
            prompt_path = Path(__file__).parent.parent / 'prompts' / 'normal_prompt.txt'

        # Carrega o prompt do arquivo externo
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()

        template = ChatPromptTemplate.from_messages([
            ('system', system_prompt),
            ('placeholder', '{chat_history}'),
            ('user', '{input}')
        ])

        if provedor not in config_modelos:
            st.error(f"Provedor '{provedor}' não configurado.")
            return None

        chat_class = config_modelos[provedor]['chat']
        
        if provedor == 'Ollama':
            chat = chat_class(model=modelo)
        else:
            api_key = os.getenv(f"{provedor.upper()}_API_KEY")
            if not api_key:
                st.error(f"API key para {provedor} não encontrada no ambiente.")
                return None
            chat = chat_class(model=modelo, api_key=api_key, temperature=1)
        
        return template | chat

    except Exception as e:
        st.error(f"Erro ao carregar modelo {provedor}/{modelo}: {str(e)}")
        return None