import streamlit as st
import json
import os
from pathlib import Path
from services.conversation_service import (
    listar_conversas_cached,
    seleciona_conversa_service,
    inicia_nova_conversa_service,
    renomear_conversa_service,
    excluir_conversa_service
)
from utils.configs import config_modelos
import streamlit as st
import json
import os
from pathlib import Path
from services.conversation_service import (
    listar_conversas_cached,
    seleciona_conversa_service,
    inicia_nova_conversa_service,
    renomear_conversa_service,
    excluir_conversa_service
)
from utils.configs import config_modelos
from services.scraping_service import raspar_links_e_salvar_paginas, indexar_base_de_conhecimento

# Caminho para o arquivo JSON de links
LINKS_FILE = Path("db/smartwiki_links.json")

def carregar_links():
    """Carrega os links do arquivo JSON."""
    if not LINKS_FILE.exists():
        return {"bases": {"Todos": []}}
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_links(links):
    """Salva os links no arquivo JSON."""
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, indent=2)

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

        col1, col2 = tab.columns([0.8, 0.09])
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
    with tab.expander('📁 Upload de arquivos', expanded=True):
        uploaded_files = st.file_uploader(
            "Escolha arquivos para esta sessão",
            accept_multiple_files=True,
            type=['pdf', 'jpg', 'jpeg', 'png', 'mp3', 'wav', 'csv', 'xlsx', 'docx', 'txt', 'py', 'js', 'html', 'css', 'json'],
            help="Os arquivos carregados serão processados junto com sua próxima mensagem.",
            key="session_file_uploader"
        )
        st.session_state['uploaded_files'] = uploaded_files if uploaded_files else []
        if st.session_state['uploaded_files']:
            st.success(f"✅ {len(st.session_state['uploaded_files'])} arquivo(s) pronto(s) para uso.")
            for file in st.session_state['uploaded_files']:
                st.caption(f"📄 {file.name}")

    with tab.expander('🤖 Seleção de modelo'):
        provedor = st.selectbox('Selecione o provedor', list(config_modelos.keys()))
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
                st.error("Falha ao carregar o modelo.")

    with tab.expander('⚙️ Configurações avançadas'):
        st.session_state['temperatura'] = st.slider('Temperatura', 0.0, 1.0, 0.7, 0.1)
        st.session_state['max_tokens'] = st.slider('Máximo de tokens', 100, 4000, 1000, 100)

def render_tabs_rag(tab):
    """Renderiza a aba de configurações RAG na barra lateral."""
    rag_ativo = st.session_state.get('rag_ativo', False)
    
    if rag_ativo:
        tab.success("🟢 RAG Ativo (Persistente)")
        if tab.button("🔴 Desativar RAG", use_container_width=True):
            st.session_state.update({'rag_ativo': False, 'use_rag_onetime': False, 'rag_base_selecionada': None})
            st.rerun()
    else:
        tab.info("🔴 RAG Inativo")
        if tab.button("🟢 Ativar RAG (Persistente)", use_container_width=True):
            st.session_state['rag_ativo'] = True
            st.rerun()

    tab.divider()

    if tab.button("Consultar RAG na próxima pergunta", use_container_width=True, disabled=rag_ativo):
        st.session_state['use_rag_onetime'] = True
        st.info("RAG será consultado na sua próxima pergunta.")

    tab.divider()

    with tab.expander('📚 Base de conhecimento para consulta', expanded=rag_ativo):
        bases = carregar_links()["bases"]
        st.session_state['rag_base_selecionada'] = st.selectbox(
            'Selecione a base para consulta',
            options=list(bases.keys()),
            key="base_para_consulta",
            disabled=not rag_ativo
        )

    with tab.expander('🔧 Configurações de embedding', expanded=False):
        st.session_state['modelo_embedding'] = st.selectbox('Modelo de embedding', ['text-embedding-3-small', 'text-embedding-3-large', 'text-embedding-ada-002'], disabled=not rag_ativo)
        st.session_state['chunk_size'] = st.slider('Tamanho do chunk', 200, 2000, 1000, 100, disabled=not rag_ativo)
        st.session_state['chunk_overlap'] = st.slider('Sobreposição', 0, 500, 200, 50, disabled=not rag_ativo)

    # Reintroduzindo a seção de indexação
    with tab.expander('📄 Indexar Base Raspada', expanded=True):
        # Obter lista de bases raspadas (subdiretórios em db/pages/)
        scraped_bases = [d.name for d in Path("db/pages").iterdir() if d.is_dir()]
        if "__pycache__" in scraped_bases: scraped_bases.remove("__pycache__") # Remover diretório de cache
        if not scraped_bases:
            st.info("Nenhuma base raspada encontrada em db/pages/.")
        else:
            base_para_indexar = st.selectbox(
                "Selecione a base para indexar",
                options=scraped_bases,
                key="base_para_indexar"
            )
            if st.button("📊 Indexar Base Selecionada"):
                if base_para_indexar:
                    num_docs, num_chunks = indexar_base_de_conhecimento(base_para_indexar)
                    st.session_state.update({'rag_num_docs': num_docs, 'rag_num_chunks': num_chunks})
                    st.success(f"Base '{base_para_indexar}' indexada com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, selecione uma base para indexar.")

    if rag_ativo:
        with tab.expander('📊 Métricas da Base', expanded=True):
            num_docs = st.session_state.get('rag_num_docs', 0)
            num_chunks = st.session_state.get('rag_num_chunks', 0)
            
            # Adicionar verificação direta do ChromaDB
            from services.rag_service import check_chroma_collection_count
            chroma_count = check_chroma_collection_count(st.session_state.get('rag_base_selecionada', 'Todos'))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documentos (Scraped)", num_docs)
                st.metric("Chunks (ChromaDB)", chroma_count)
            with col2:
                st.metric("Chunks (Ingested)", num_chunks)
                st.metric("Relevância média", "0.85")

def render_tabs_scraping(tab):
    """Renderiza a aba de scraping na barra lateral."""
    with tab.expander("➕ Adicionar Nova Base de Conhecimento", expanded=True):
        link = st.text_input("URL da página ou categoria SmartWiki", key="new_smartwiki_link")
        base_name = st.text_input("Nome para a nova base", key="new_base_name")
        
        if st.button("➕ Raspar e Salvar Páginas"):
            if link and base_name:
                links_data = carregar_links()
                if base_name not in links_data["bases"]:
                    links_data["bases"][base_name] = []
                
                if link not in links_data["bases"][base_name]:
                    links_data["bases"][base_name].append(link)
                if "Todos" in links_data["bases"] and link not in links_data["bases"]["Todos"]:
                    links_data["bases"]["Todos"].append(link)
                
                salvar_links(links_data)
                
                num_docs_scraped = raspar_links_e_salvar_paginas(base_name, [link])
                
                st.session_state.update({'rag_num_docs': num_docs_scraped})
                st.success(f"Scraping da base '{base_name}' concluído! {num_docs_scraped} página(s) raspada(s).")
                st.rerun()
            else:
                st.error("Por favor, preencha a URL e o nome da base.")

    st.divider()
    links = carregar_links()
    st.write("Bases de conhecimento existentes:")
    for base, urls in links["bases"].items():
        with st.expander(f"{base} ({len(urls)} links)"):
            for u in urls:
                st.write(f"- {u}")

def render_tempo_resposta():
    """Renderiza o tempo de resposta da última consulta."""
    if 'tempo_resposta' in st.session_state:
        st.caption(f'⏱️ Última resposta: {st.session_state["tempo_resposta"]:.2f}s')

def render_sidebar():
    """Renderiza toda a barra lateral com abas e tempo de resposta."""
    with st.sidebar:
        st.title("🔮 VerônIA")
        tabs = st.tabs(['💬 Conversas', '🛠️ Ferramentas', '🧠 RAG', '🕸️ Scraping'])
        render_tabs_conversas(tabs[0])
        render_tabs_configuracoes(tabs[1])
        render_tabs_rag(tabs[2])
        render_tabs_scraping(tabs[3])
        render_tempo_resposta()