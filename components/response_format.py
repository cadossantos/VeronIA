import streamlit as st

def render_response_format_selector():
    st.selectbox(
        "Estilo da Resposta",
        ["Curta", "Detalhada", "Lista com bullets", "Código", "Resumo executivo"],
        key="response_style"
    )
