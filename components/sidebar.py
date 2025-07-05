import streamlit as st
import os
from services.conversation_service import (
    listar_conversas_cached,
    seleciona_conversa_service,
    inicia_nova_conversa_service,
    renomear_conversa_service,
    excluir_conversa_service
)
from utils.configs import config_modelos


def render_tabs_conversas(tab, agent_type: str):
    """Renderiza a aba de gerenciamento de conversas na barra lateral."""
    tab.button('➕ Nova conversa', on_click=inicia_nova_conversa_service, args=(agent_type,), use_container_width=True)
    tab.divider()
    conversas = listar_conversas_cached()
    for id, titulo in conversas:
        if len(titulo) == 30:
            titulo += '...'

        col1, col2 = tab.columns([0.8, 0.2])
        with col1:
            col1.button(
                titulo,
                key=f"conversa_{id}",
                on_click=seleciona_conversa_service,
                args=(id, agent_type,),
                disabled=id == st.session_state.get(f'conversa_atual_{agent_type}'),
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
    provedor = tab.selectbox('Selecione o provedor', list(config_modelos.keys()))
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

def render_smartwiki_config_panel(tab):
    """Renderiza o painel de controle completo para o agente SmartWiki."""
    tab.subheader("Modo de Operação")
    # Seletor de Modo
    mode = tab.radio(
        "", # Label vazio para não duplicar o subheader
        ("Chat", "Treinamento"),
        key="smartwiki_mode"
    )

    tab.divider()

    if mode == "Chat":
        tab.subheader("Coleções de Documentos")
        collections_base_dir = "smartwiki/data/vector_store"
        collections = []

        if os.path.exists(collections_base_dir) and os.path.isdir(collections_base_dir):
            collections = [d for d in os.listdir(collections_base_dir) if os.path.isdir(os.path.join(collections_base_dir, d))]
        
        if os.path.exists(os.path.join(collections_base_dir, "chroma.sqlite3")):
            collections.insert(0, "default")

        if not collections:
            tab.warning("Nenhuma coleção encontrada. Use o modo 'Treinamento' para criar uma.")

        active_collection = tab.radio(
            "Selecione a coleção para consultar:",
            collections,
            index=collections.index(st.session_state.get('active_collection', collections[0])) if st.session_state.get('active_collection') in collections else 0
        )
        
        if st.session_state.get('active_collection') != active_collection:
            st.session_state['active_collection'] = active_collection
            st.cache_resource.clear()
            st.rerun()
    
    elif mode == "Treinamento":
        tab.info("Acesse a página do Especialista SmartSimple para treinar uma nova coleção a partir de uma URL.")

def render_tempo_resposta():
    if 'tempo_resposta' in st.session_state:
        st.caption(f'⏱️ Última resposta: {st.session_state["tempo_resposta"]:.2f}s')

def render_sidebar():
    """Renderiza toda a barra lateral, adaptando o conteúdo à página atual."""
    with st.sidebar:
        st.title("🔮 VerônIA")
        
        page_context = st.session_state.get('current_page', 'chat_geral')
        st.write(f"DEBUG: Page Context in sidebar: {page_context}") # DEBUG

        if page_context == 'smartwiki':
            st.write("DEBUG: Rendering SmartWiki Panel") # DEBUG
            tab_conv, tab_config_smartwiki = st.tabs(['💬 Conversas', '⚙️ SmartWiki'])
            render_tabs_conversas(tab_conv, page_context)
            render_smartwiki_config_panel(tab_config_smartwiki)
        else:
            st.write("DEBUG: Rendering General Tabs") # DEBUG
            # Comportamento padrão para o Chat Geral e outras futuras páginas
            tab_conv, tab_conf = st.tabs(['💬 Conversas', '⚙️ Configurações'])
            render_tabs_conversas(tab_conv, page_context)
            render_tabs_configuracoes(tab_conf)
            
        render_tempo_resposta()

