import streamlit as st
from services.conversation_service import (
    listar_conversas_cached,
    seleciona_conversa_service,
    inicia_nova_conversa_service,
    renomear_conversa_service,
    excluir_conversa_service
)
from utils.configs import config_modelos


def render_tabs_conversas(tab):
    """Renderiza a aba de gerenciamento de conversas na barra lateral."""
    tab.markdown('')
    tab.markdown('')

    tab.button('➕ Nova conversa', on_click=inicia_nova_conversa_service, use_container_width=True)
    tab.divider()
    conversas = listar_conversas_cached()
    for id, titulo in conversas:
        if len(titulo) == 30:
            titulo += '...'

        col1, col2 = tab.columns([0.8, 0.2])  # 80% título, 20% ações
        with col1:
            col1.button(
                titulo,
                key=f"conversa_{id}",
                on_click=seleciona_conversa_service,
                args=(id,),
                disabled=id == st.session_state.get('conversa_atual'),
                use_container_width=True
            )
        with col2:
            if col2.button("⋮", key=f"menu_{id}"):
                st.session_state[f"menu_aberto_{id}"] = not st.session_state.get(f"menu_aberto_{id}", False)

        if st.session_state.get(f"menu_aberto_{id}", False):
            with tab.container():
                col_ren, col_exc = st.columns(2)
                with col_ren:
                    if st.button("✏️ Editar conversa", key=f"ren_{id}"):
                        st.session_state[f"renomear_{id}"] = True
                with col_exc:
                    if st.button("🗑️ Excluir conversa", key=f"exc_{id}"):
                        excluir_conversa_service(id)

            if st.session_state.get(f"renomear_{id}"):
                novo = tab.text_input("Novo título", key=f"input_{id}")
                if tab.button("Salvar", key=f"salva_{id}") and novo.strip():
                    renomear_conversa_service(id, novo)
                    st.session_state[f"renomear_{id}"] = False


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

def render_tempo_resposta():
    if 'tempo_resposta' in st.session_state:
        st.caption(f'⏱️ Última resposta: {st.session_state["tempo_resposta"]:.2f}s')


def render_sidebar():
    """Renderiza toda a barra lateral com abas e tempo de resposta."""
    with st.sidebar:
        st.title("🔮 VerônIA")
        tab1, tab2 = st.tabs(['💬 Conversas', '⚙️ Configurações'])
        render_tabs_conversas(tab1)
        render_tabs_configuracoes(tab2)
        render_tempo_resposta()
