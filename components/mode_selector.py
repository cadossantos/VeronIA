import streamlit as st

def render_mode_selector():
    return st.selectbox(
        "Modo de Operação",
        ["Normal", "Post-it", "Redator", "Tradutor", "Web Search"],
        key="operation_mode"
    )
