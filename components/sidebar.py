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
    # Upload de arquivos global
    with tab.expander('📁 Upload de arquivos', expanded=True):
        uploaded_files = st.file_uploader(
            "Escolha arquivos para esta sessão",
            accept_multiple_files=True,
            type=['pdf', 'jpg', 'jpeg', 'png', 'mp3', 'wav', 'csv', 'xlsx', 'docx', 'txt', 'py', 'js', 'html', 'css', 'json'],
            help="Os arquivos carregados serão processados junto com sua próxima mensagem.",
            key="session_file_uploader"
        )
        # Apenas atribui os arquivos carregados ao session_state. A interface do chat irá processá-los.
        st.session_state['uploaded_files'] = uploaded_files if uploaded_files else []

        if st.session_state['uploaded_files']:
            st.success(f"✅ {len(st.session_state['uploaded_files'])} arquivo(s) pronto(s) para uso.")
            for file in st.session_state['uploaded_files']:
                st.caption(f"📄 {file.name}")

    # Seleção de modelo
    with tab.expander('🤖 Seleção de modelo'):
        provedor = st.selectbox('Selecione o provedor', config_modelos.keys())
        modelo_escolhido = st.selectbox('Selecione o modelo', config_modelos[provedor]['modelos'])

        st.session_state['modelo'] = modelo_escolhido
        st.session_state['provedor'] = provedor

        if st.button('Aplicar Modelo', use_container_width=True):
            from services.model_service import carregar_modelo_cache
            chain = carregar_modelo_cache(provedor, modelo_escolhido)
            if chain:
                st.session_state['chain'] = chain
                st.session_state['modelo_nome'] = f"{provedor} - {modelo_escolhido}"
            else:
                st.error("Falha ao carregar o modelo. Verifique as configurações e a chave de API.")

    # Formato de resposta
    with tab.expander('📝 Formato de resposta'):
        formato = st.selectbox(
            'Estilo de resposta',
            ['Padrão', 'Curta', 'Detalhada', 'Lista', 'Código', 'Resumo'],
            help="Escolha como o modelo deve formatar as respostas"
        )
        st.session_state['formato_resposta'] = formato

        tom = st.selectbox(
            'Tom da resposta',
            ['Neutro', 'Formal', 'Casual', 'Técnico', 'Amigável'],
            help="Define o tom das respostas"
        )
        st.session_state['tom_resposta'] = tom

    # Configurações avançadas
    with tab.expander('⚙️ Configurações avançadas'):
        temperatura = st.slider(
            'Temperatura',
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controla a criatividade das respostas"
        )
        st.session_state['temperatura'] = temperatura

        max_tokens = st.slider(
            'Máximo de tokens',
            min_value=100,
            max_value=4000,
            value=1000,
            step=100,
            help="Limite de tokens para as respostas"
        )
        st.session_state['max_tokens'] = max_tokens

        idioma = st.selectbox(
            'Idioma preferencial',
            ['Automático', 'Português', 'Inglês', 'Espanhol', 'Francês'],
            help="Idioma padrão para as respostas"
        )
        st.session_state['idioma_preferencial'] = idioma
        

def render_tabs_rag(tab):
    """Renderiza a aba de configurações RAG na barra lateral."""
    # Status do RAG
    rag_ativo = st.session_state.get('rag_ativo', False)
    
    if rag_ativo:
        tab.success("🟢 RAG Ativo")
        if tab.button("🔴 Desativar RAG", use_container_width=True):
            st.session_state['rag_ativo'] = False
            st.session_state['rag_base_selecionada'] = None
            # Limpar contexto aqui quando implementar
            st.rerun()
    else:
        tab.info("🔴 RAG Inativo")
        if tab.button("🟢 Ativar RAG", use_container_width=True):
            st.session_state['rag_ativo'] = True
            # Limpar contexto aqui quando implementar
            st.rerun()

    tab.divider()

    # Seleção de base de conhecimento
    with tab.expander('📚 Base de conhecimento', expanded=rag_ativo):
        # Placeholder para bases disponíveis
        bases_disponiveis = ['Documentos Gerais', 'Base Técnica', 'Manual do Usuário']
        
        base_selecionada = st.selectbox(
            'Selecione a base',
            bases_disponiveis,
            disabled=not rag_ativo
        )
        st.session_state['rag_base_selecionada'] = base_selecionada

        if st.button('Atualizar Base', disabled=not rag_ativo):
            st.info("Base atualizada com sucesso!")

    # Upload para indexação
    with tab.expander('📄 Documentos para indexação', expanded=False):
        docs_para_indexar = st.file_uploader(
            "Adicionar documentos à base",
            accept_multiple_files=True,
            type=['pdf', 'txt', 'docx'],
            disabled=not rag_ativo,
            key="rag_uploader"
        )
        
        if docs_para_indexar and rag_ativo:
            if st.button("📊 Indexar documentos"):
                st.info("Processando documentos para indexação...")
                # Lógica de indexação aqui
                st.success("Documentos indexados com sucesso!")

    # Configurações de embedding
    with tab.expander('🔧 Configurações de embedding', expanded=False):
        modelo_embedding = st.selectbox(
            'Modelo de embedding',
            ['sentence-transformers/all-MiniLM-L6-v2', 'text-embedding-ada-002'],
            disabled=not rag_ativo
        )
        st.session_state['modelo_embedding'] = modelo_embedding

        chunk_size = st.slider(
            'Tamanho do chunk',
            min_value=200,
            max_value=2000,
            value=1000,
            step=100,
            disabled=not rag_ativo
        )
        st.session_state['chunk_size'] = chunk_size

        overlap = st.slider(
            'Sobreposição',
            min_value=0,
            max_value=500,
            value=200,
            step=50,
            disabled=not rag_ativo
        )
        st.session_state['chunk_overlap'] = overlap

        relevancia_threshold = st.slider(
            'Limiar de relevância',
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            disabled=not rag_ativo
        )
        st.session_state['relevancia_threshold'] = relevancia_threshold

    # Métricas (placeholder)
    if rag_ativo:
        with tab.expander('📊 Métricas', expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documentos", "25")
                st.metric("Última consulta", "95%")
            with col2:
                st.metric("Chunks", "1.2k")
                st.metric("Relevância média", "0.85")


def render_tempo_resposta():
    """Renderiza o tempo de resposta da última consulta."""
    if 'tempo_resposta' in st.session_state:
        st.caption(f'⏱️ Última resposta: {st.session_state["tempo_resposta"]:.2f}s')


def render_sidebar():
    """Renderiza toda a barra lateral com abas e tempo de resposta."""
    with st.sidebar:
        st.title("🔮 VerônIA")
        tab1, tab2, tab3 = st.tabs(['💬 Conversas', '🛠️ Ferramentas', '🧠 RAG'])
        render_tabs_conversas(tab1)
        render_tabs_configuracoes(tab2)
        render_tabs_rag(tab3)
        render_tempo_resposta()