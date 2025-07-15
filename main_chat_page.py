import streamlit as st
from db.db_sqlite import init_database
from components.header import criar_header_fixo as render_header
from components.chat_interface import interface_chat
from components.sidebar import render_sidebar
from utils.session_utils import init_session_state
from smartwiki.agents.query import perguntar_ao_agent

def main():
    """Função principal que renderiza a página de chat."""
    st.set_page_config(page_title="VerônIA", layout="wide")
    st.cache_data.clear()
    init_database()
    init_session_state()

    render_header()
    render_sidebar()
    interface_chat(perguntar_ao_agent_func=perguntar_ao_agent)

if __name__ == '__main__':
    main()
