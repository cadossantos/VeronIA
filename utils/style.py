import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
/* Importar fontes mais elegantes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500;600&display=swap');

/* --- Reset e Base --- */
* {
    font-family: 'Inter', sans-serif;
}

/* Títulos principais com fonte serif elegante */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #2F3A1F !important;
    font-weight: 500 !important;
}

/* --- Background Principal --- */
.main > div {
    background: linear-gradient(135deg, 
        #E7DBCB 0%, 
        #E8DCC0 30%, 
        #DDD2B8 70%, 
        #D2C7A8 100%) !important;
}
                


/* --- Sidebar Orgânica --- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, 
        #666F43 0%, 
        #5A5E38 50%, 
        #4E522D 100%) !important;
    border-right: 3px solid #9B643B !important;
}

[data-testid="stSidebar"] > div {
    padding: 1rem 1.5rem !important;
}

/* Logo/Título da sidebar */
[data-testid="stSidebar"] h1 {
    color: #E7DBCB !important;
    text-align: center;
    font-size: 2.2rem !important;
    margin-bottom: 2rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

/* --- Expanders Orgânicos --- */
[data-testid="stExpander"] {
    background: #666f43 !important;
    border: 2px solid #B2976B !important;
    border-radius: 16px !important;
    margin: 1rem 0 !important;
    box-shadow: 0 4px 12px rgba(155, 100, 59, 0.15) !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stExpander"]:hover {
    box-shadow: 0 6px 20px rgba(155, 100, 59, 0.25) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stExpander"] summary {
    color: #B2976B !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 1rem 1.5rem !important;
}

[data-testid="stExpander"] summary:hover {
    color: #E7DBCB !important;
}

/* Conteúdo do expander */
[data-testid="stExpander"] > div > div {
    background: rgba(246, 239, 221, 0.8) !important;
    border-radius: 0 0 16px 16px !important;
    padding: 1.5rem !important;
}
                


/* --- Widgets Refinados --- */
/* Selectbox */
[data-testid="stSelectbox"] > div {
    background: rgba(102, 111, 67, 0.9) !important;
    border: 2px solid #9B643B !important;
    border-radius: 12px !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSelectbox"] > div:hover {
    border-color: #FAB101 !important;
    box-shadow: 0 0 12px rgba(250, 177, 1, 0.3) !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    color: #E7DBCB !important;
    font-weight: 500 !important;
}

                

/* File Uploader */
[data-testid="stFileUploader"] section {
    background: rgba(178, 151, 107, 0.2) !important;
    border: 2px dashed #9B643B !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"] section:hover {
    background: rgba(178, 151, 107, 0.3) !important;
    border-color: #faaf0183 !important;
    transform: scale(1.02) !important;
}

                
/* Texto do file uploader */
[data-testid="stFileUploader"] section p {
    color: #2F3A1F !important;
    font-weight: 500 !important;
}

                
                
/* --- Sliders Orgânicos --- */
[data-testid="stSlider"] {
    padding: 1rem 0 !important;
}

[data-testid="stSlider"] > div > div {
    background: linear-gradient(90deg, #9B643B, #FAB101) !important;
}

/* --- Mensagens de Chat Sofisticadas --- */
.mensagem-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #B2976B, #9B643B) !important;
    color: #E7DBCB !important;
    border-radius: 20px 20px 5px 20px !important;
    padding: 1rem 1.5rem !important;
    margin: 0.5rem 0 !important;
    box-shadow: 0 4px 12px rgba(155, 100, 59, 0.3) !important;
    position: relative;
    max-width: 80%;
    word-wrap: break-word;
    font-weight: 400;
    line-height: 1.5;
}

.mensagem-user::after {
    content: '';
    position: absolute;
    bottom: 0;
    right: -8px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-top: 8px solid #9B643B;
    border-left: 8px solid #9B643B;
}

.mensagem-assistente {
    align-self: flex-start;
    background: linear-gradient(135deg, #666F43, #5A5E38) !important;
    color: #E7DBCB !important;
    border-radius: 20px 20px 20px 5px !important;
    padding: 1rem 1.5rem !important;
    margin: 0.5rem 0 !important;
    box-shadow: 0 4px 12px rgba(102, 111, 67, 0.3) !important;
    position: relative;
    max-width: 80%;
    word-wrap: break-word;
    font-weight: 400;
    line-height: 1.5;
}

.mensagem-assistente::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: -8px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-top: 8px solid #5A5E38;
    border-right: 8px solid #5A5E38;
}

/* --- Botões Elegantes --- */
.stButton > button {
    background: #3B421F  !important;
    color: #E7DBCB !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 0.7rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    # box-shadow: 0 4px 12px rgba(155, 100, 59, 0.3) !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 8px #666f438e !important;
}

/* --- Abas Sofisticadas --- */
button[data-baseweb="tab"] {
    background: rgba(178, 151, 107, 0.1) !important;
    color: #2F3A1F !important;
    border: none !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 1rem 1rem !important;
    font-weight: 600 !important;
    font-size: 0.7rem !important;
    margin: 0 0.25rem !important;
    transition: all 0.3s ease !important;
}

button[data-baseweb="tab"]:hover {
    background: rgba(178, 151, 107, 0.2) !important;
    color: #E7DBCB !important;
    transform: translateY(-2px) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #9B643B, #9B643B) !important;
    color: #E7DBCB !important;
    box-shadow: 0 4px 12px rgba(155, 100, 59, 0.3) !important;
}

/* --- Área de Input Refinada --- */
[data-testid="stChatInput"] {
    background: rgba(246, 239, 221, 0.9) !important;
    border: 3px solid #B2976B !important;
    border-radius: 40px !important;
    # padding: -5% !important;
    # margin: 1rem 0 !important;
    box-shadow: 0 4px 12px rgba(178, 151, 107, 0.2) !important;
    backdrop-filter: blur(10px) !important;
}

[data-testid="stChatInput"]:focus-within {
    # border-color: #F4C19F !important;
    box-shadow: 0 0 0 3px rgba(250, 177, 1, 0.2) !important;
}

/* Linha vermelha do indicador/borda */

/* Opção 1: */
[data-testid="stChatInput"] [class*="st-emotion-cache"]:not(input):not(textarea) {
    border-color: #B2976B !important;
    background-color: transparent !important;
    border-top-color: #B2976B !important;
    border-bottom-color: #B2976B !important;
}

                                
/* --- Ícones e Labels Orgânicos --- */
.icone-label {
    font-size: 1.8rem !important;
    color: #9B643B !important;
    margin-bottom: 0.8rem !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* --- Elementos de Feedback --- */
.stAlert {
    background: rgba(178, 151, 107, 0.1) !important;
    border: 1px solid #B2976B !important;
    border-radius: 12px !important;
    color: #2F3A1F !important;
}

/* --- Animações Suaves --- */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.stExpander, .mensagem-user, .mensagem-assistente {
    animation: fadeIn 0.5s ease-out !important;
}

/* --- Status Indicators --- */
[data-testid="stStatus"] {
    background: rgba(102, 111, 67, 0.9) !important;
    border-radius: 12px !important;
    color: #E7DBCB !important;
}

/* --- Scrollbar Personalizada --- */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(246, 239, 221, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #B2976B, #9B643B);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #9B643B, #FAB101);
}

/* --- Responsividade --- */
@media (max-width: 768px) {
    [data-testid="stSidebar"] > div {
        padding: 1rem !important;
    }
    
    .mensagem-user, .mensagem-assistente {
        max-width: 90% !important;
        padding: 0.8rem 1.2rem !important;
    }
    
    .stButton > button {
        padding: 0.6rem 1.5rem !important;
        font-size: 0.9rem !important;
    }
}

</style>
""", unsafe_allow_html=True)