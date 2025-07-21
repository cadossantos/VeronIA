import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
/* --- Estilização de Widgets e Expanders --- */

/* Fundo dos 'expanders' como "Upload de arquivos" e "Seleção de modelo" */
[data-testid="stExpander"] {
    background-color: #B2976B;
    border-radius: 12px;
    border: none !important;
}

/* Remove a cor vermelha do ícone de seta no 'expander' ao passar o mouse */
[data-testid="stExpander"] summary:hover svg {
    color: #F6EFDD !important;
}

/* Fundo das caixas de seleção (selectbox) e da área de upload */
[data-testid="stSelectbox"] > div, [data-testid="stFileUploader"] section {
    background-color: #666F43 !important; /* 🎨 Altere o fundo aqui */
    border-radius: 8px !important;
}

/* Cor do texto dentro das caixas de seleção e área de upload */
[data-testid="stSelectbox"] div[data-baseweb="select"], .st-emotion-cache-1ftuga
{
    color: #F6EFDD !important; /* Cor do texto */
}

/* --- Fim da Estilização de Widgets --- */

.mensagem-user {
    align-self: flex-end;
    background-color: #B2976B;
    color: #F6EFDD;
    border-radius: 12px;
    padding: 0.6em 1em;
}

.mensagem-assistente {
    align-self: flex-start;
    background-color: #666F43;
    color: #F6EFDD;
    border-radius: 12px;
    padding: 0.6em 1em;
}

.icone-label {
    font-size: 1.6rem;
    color: #9B643B;
    margin-bottom: 0.5em;
}

[data-testid="stSidebar"] {
    background-color: #666F43;
}

/* --- Estilização das Abas (st.tabs) --- */
button[data-baseweb="tab"] {
    background-color: transparent !important;
    color: #F6EFDD !important;
    border-radius: 6px 6px 0 0;
}
button[data-baseweb="tab"]:hover {
    color: #FAB101 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FAB101 !important;
}
/* --- Fim da Estilização das Abas --- */


/* CSS from header.py - fixed-header */
.fixed-header {
    position: fixed;
    top: 0;
    left: 1;
    right: 0;
    z-index: 999;

    /* Cor neutra com 50% de transparência */
    background-color: rgba(71, 142, 158, 0.2);

    /* Efeito de "vidro fosco" para desfocar o que está atrás ✨ */
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px); /* Suporte para o Safari */

    /* Sombra mais suave para dar profundidade */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);

    /* Estilos que você já tinha */
    padding: 15px 10px 0px 10px;
    border-radius: 30%;
    margin-top: 10px;
}

.fixed-header small {
    display: block;
    margin: 1% 0;
    font-size: 16px;
    color: #F6EFDD;
}

.fixed-header-content {
    display: flex;
    justify-content: center;
    align-items: center;
    color: #F6EFDD;
    font-family: roboto;
}

.chat-main-area {
    margin-top: 50px; /* Ajustado para compensar o padding maior */
}

/* CSS from header.py - menu-button */
.menu-button {
    background-color: transparent;
    color: #F6EFDD;
    border: none;
    font-size: 18px;
    cursor: pointer;
    padding: 0 4px;
}
.menu-button:hover {
    color: #FAB101;
}
</style>
""", unsafe_allow_html=True)