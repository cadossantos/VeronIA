import streamlit as st

def criar_header_fixo():
    """Renderiza um cabeçalho fixo com informações do modelo de IA."""
    modelo = st.session_state.get('modelo_nome', 'Modelo não carregado')

    st.markdown(f"""
    <div class="fixed-header">
        <div class="fixed-header-content">
            <div style="text-align: center;">
                <br>
                <small>{modelo}</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
