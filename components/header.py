import streamlit as st

def criar_header_fixo():
    """Renderiza um cabeçalho fixo com informações do modelo de IA."""
    modelo = st.session_state.get('modelo_nome', 'Modelo não carregado')

    st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 1;
        right: 0;
        z-index: 999;
        background: linear-gradient(90deg, #667eea, #764ba2);
        padding: 15px 10px 0px 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-radius: 30%;
        margin-top: 10px;
    }

    .fixed-header small {
        display: block;
        margin: 10% 0;
        font-size: 16px;
        color: #eeeeee;
    }

    .fixed-header-content {
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-family: sans-serif;
    }

    .chat-main-area {
        margin-top: 100px; /* Ajustado para compensar o padding maior */
    }
    </style>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <style>
        .menu-button {
            background-color: transparent;
            color: #ccc;
            border: none;
            font-size: 18px;
            cursor: pointer;
            padding: 0 4px;
        }
        .menu-button:hover {
            color: #fff;
        }
    </style>
    """, unsafe_allow_html=True)
