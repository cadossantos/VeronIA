import streamlit as st
from components.chat_display import render_chat_ui
from services.rag_service import get_rag_chain
from services.scraping_service import ScrapingService
from components.sidebar import render_sidebar # Importar render_sidebar

# --- Funções de Lógica da Página ---

def processar_mensagem_rag(prompt: str, historico: list) -> str:
    """
    Callback para o modo Chat. Processa a pergunta usando o serviço de RAG.
    """
    collection = st.session_state.get('active_collection', 'default')
    qa_chain = get_rag_chain(collection_name=collection)
    
    if not qa_chain:
        return "Erro: A chain de RAG não pôde ser inicializada. Verifique a coleção selecionada."

    result = qa_chain.invoke({"question": prompt, "chat_history": historico})
    resposta = result.get("answer", "Não foi possível encontrar uma resposta.")
    fontes = result.get("source_documents", [])
    
    if fontes:
        fontes_str = "\n\n---\n**Fontes Consultadas:**\n"
        for source in fontes:
            metadata = source.metadata
            fontes_str += f"- **{metadata.get('title', 'N/A')}** (URL: {metadata.get('url', '#')})\n"
        return resposta + fontes_str
    return resposta

def render_single_url_training():
    """Renderiza o formulário para treinar a partir de uma única URL."""
    st.info("Forneça a URL de uma página web e um nome para a nova base de conhecimento.")

    scraper = ScrapingService()
    
    with st.form("single_url_form"):
        url = st.text_input("URL do site:", placeholder="https://exemplo.com/pagina")
        collection_name = st.text_input("Nome da nova coleção:", placeholder="minha-colecao-url")
        submitted = st.form_submit_button("Iniciar Treinamento (URL Única)")
    
    if submitted and url and collection_name:
        with st.spinner(f"Processando e treinando a partir de {url}..."):
            result = scraper.scrape_and_ingest_website(url, collection_name)
            
            if result.get("success"):
                st.success(f"✅ Treinamento concluído! A coleção '{collection_name}' foi criada e está pronta para uso no modo Chat.")
                st.balloons()
            else:
                st.error(f"❌ Erro durante o treinamento: {result.get('error')}")

def render_category_training():
    """Renderiza o formulário para treinar a partir de uma categoria MediaWiki."""
    st.info("Forneça a URL da API do MediaWiki, o nome da categoria e um nome para a nova base de conhecimento.")
    st.warning("Este modo é específico para sites MediaWiki (como a SmartWiki). Ex: API URL: https://wiki.smartsimple.com/api.php")

    scraper = ScrapingService()

    with st.form("category_form"):
        api_url = st.text_input("URL da API MediaWiki:", placeholder="https://wiki.smartsimple.com/api.php")
        category_name = st.text_input("Nome da Categoria:", placeholder="Custom_Fields")
        collection_name = st.text_input("Nome da nova coleção:", placeholder="minha-colecao-categoria")
        submitted = st.form_submit_button("Iniciar Treinamento (Categoria)")

    if submitted and api_url and category_name and collection_name:
        with st.spinner(f"Processando e treinando a partir da categoria {category_name}..."):
            result = scraper.scrape_and_ingest_category(api_url, category_name, collection_name)

            if result.get("success"):
                st.success(f"✅ Treinamento concluído! A coleção '{collection_name}' foi criada e está pronta para uso no modo Chat.")
                st.balloons()
            else:
                st.error(f"❌ Erro durante o treinamento: {result.get('error')}")

def render_training_interface():
    """Renderiza o seletor de tipo de treinamento e o formulário correspondente."""
    st.header("Treinar Nova Coleção")
    training_type = st.radio(
        "Selecione o tipo de treinamento:",
        ("URL Única", "Categoria MediaWiki"),
        key="training_type_selector"
    )

    if training_type == "URL Única":
        render_single_url_training()
    else: # Categoria MediaWiki
        render_category_training()

# --- Renderização Principal da Página ---
st.set_page_config(page_title="Especialista SmartSimple", page_icon="🧠")

# Define o contexto para a sidebar saber qual página está ativa
st.session_state['current_page'] = 'smartwiki'

render_sidebar() # Chamada para renderizar a sidebar

# Obtém o modo de operação da sidebar (padrão é Chat)
mode = st.session_state.get("smartwiki_mode", "Chat")

st.title("🧠 Especialista SmartSimple")

# Roteador: renderiza a UI correta com base no modo selecionado
if mode == "Chat":
    st.info(
        "Modo Chat: Converse com o assistente. As respostas são baseadas na coleção de documentos selecionada na barra lateral."
    )
    render_chat_ui(
        history_key=f'historico_{st.session_state["current_page"]}',
        on_submit_callback=processar_mensagem_rag
    )
else: # mode == "Treinamento"
    render_training_interface()
