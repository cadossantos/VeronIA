import streamlit as st
from services.conversation_service import (
    listar_conversas_cached,
    seleciona_conversa_service,
    inicia_nova_conversa_service,
    renomear_conversa_service
)
from utils.configs import config_modelos
from db.db_sqlite import get_titulo_conversa

def render_tabs_conversas(tab):
    """Renderiza a aba de gerenciamento de conversas na barra lateral."""
    tab.button('➕ Nova conversa', on_click=inicia_nova_conversa_service, use_container_width=True)
    tab.markdown('')

    conversas = listar_conversas_cached()
    for id, titulo in conversas:
        if len(titulo) == 30:
            titulo += '...'
        tab.button(
            titulo,
            key=f"conversa_{id}",
            on_click=seleciona_conversa_service,
            args=(id,),
            disabled=id == st.session_state.get('conversa_atual'),
            use_container_width=True
        )

def render_tabs_configuracoes(tab):
    """Renderiza a aba de configurações do modelo na barra lateral."""
    provedor = tab.selectbox('Selecione o provedor', config_modelos.keys())
    modelo_escolhido = tab.selectbox('Selecione o modelo', config_modelos[provedor]['modelos'])

    st.session_state['modelo'] = modelo_escolhido
    st.session_state['provedor'] = provedor

    if tab.button('Aplicar Modelo', use_container_width=True):
        from services.model_service import carregar_modelo_cache
        chain = carregar_modelo_cache(provedor, modelo_escolhido)
        if chain:
            st.session_state['chain'] = chain
            st.session_state['modelo_nome'] = f"{provedor} - {modelo_escolhido}"
        else:
            st.error("Falha ao carregar o modelo. Verifique as configurações e a chave de API.")
    

    conversa_id = st.session_state.get('conversa_atual')
    if conversa_id:
        titulo_atual = get_titulo_conversa(conversa_id)
        novo_titulo = tab.text_input("Renomear conversa atual:", value=titulo_atual, key="input_titulo")
        if tab.button("Salvar título", use_container_width=True, key="salva_titulo"):
            renomear_conversa_service(conversa_id, novo_titulo)

def render_tempo_resposta():
    if 'tempo_resposta' in st.session_state:
        st.caption(f'⏱️ Última resposta: {st.session_state["tempo_resposta"]:.2f}s')


def render_sidebar():
    """Renderiza toda a barra lateral com abas e tempo de resposta."""
    with st.sidebar:
        st.title("🔮 JibóIA")
        tab1, tab2 = st.tabs(['💬 Conversas', '⚙️ Config'])
        render_tabs_conversas(tab1)
        render_tabs_configuracoes(tab2)
        render_tempo_resposta()
