import streamlit as st
import time

from db.db_sqlite import salvar_mensagem, atualizar_titulo_conversa
from services.memory_service import get_historico, reconstruir_memoria, adicionar_mensagem
from services.conversation_service import inicia_nova_conversa_service
from services import file_processor  # Importa o novo módulo
from services.rag_service import consultar_base_de_conhecimento # Importa o serviço RAG
from utils.constants import (
    HEADER_TITLE, INITIALIZING_MESSAGE, WELCOME_MESSAGE,
    USAGE_INSTRUCTIONS, CHAT_INPUT_PLACEHOLDER, TITLE_TRUNCATE_LENGTH,
    CHAT_MESSAGE_LIMIT
)


def process_uploaded_files():
    """
    Processa os arquivos carregados e retorna o contexto extraído.
    """
    uploaded_files = st.session_state.get('uploaded_files', [])
    if not uploaded_files:
        return ""
    
    contexto_arquivos = []
    
    for arquivo in uploaded_files:
        # Reset do ponteiro do arquivo para o início
        arquivo.seek(0)
        
        # Processa o arquivo usando o módulo file_processor
        conteudo = file_processor.processar_automatico(arquivo)
        
        if conteudo:
            contexto_arquivos.append(f"=== CONTEÚDO DO ARQUIVO: {arquivo.name} ===\n{conteudo}\n")
    
    return "\n".join(contexto_arquivos)


def renderiza_mensagens(historico, limite=CHAT_MESSAGE_LIMIT):
    """Renderiza as mensagens do histórico de chat."""

    for msg in historico[-limite:]:
        role = msg['role']
        content = msg['content']
        if role == 'user':
            st.markdown(f"""
            <div class="mensagem-container">
                <div class="icone-label"> <br> </div>
                <div class="mensagem-user">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mensagem-container">
                <div class="icone-label"> <br> </div>
                <div class="mensagem-assistente">{content}</div>
            </div>
            """, unsafe_allow_html=True)


def render_chat_ui():
    """Renderiza a interface básica do chat."""
    st.markdown('<div class="chat-main-area">', unsafe_allow_html=True)
    # st.header(HEADER_TITLE)
    
    if not st.session_state.get('chain'):
        st.info(INITIALIZING_MESSAGE)
    
    conversa_atual = st.session_state.get('conversa_atual')
    if not conversa_atual:
        # st.info(WELCOME_MESSAGE)
        with st.expander("Como usar"):
            st.markdown(USAGE_INSTRUCTIONS)


def process_ai_response(input_usuario, memoria, contexto_arquivos=""):
    """Processa a resposta da IA com contexto de arquivos."""
    tempo_inicial = time.time()
    
    # Constrói o prompt com contexto dos arquivos
    if contexto_arquivos:
        prompt_completo = f"""CONTEXTO DOS ARQUIVOS CARREGADOS:
{contexto_arquivos}

PERGUNTA DO USUÁRIO:
{input_usuario}

Por favor, responda considerando o contexto dos arquivos fornecidos acima."""
    else:
        prompt_completo = input_usuario
    
    with st.chat_message('ai'):
        try:
            resposta = st.write_stream(st.session_state['chain'].stream({
                'input': prompt_completo,
                'chat_history': memoria.buffer_as_messages
            }))
        except Exception as e:
            st.error(f"Erro ao processar resposta: {str(e)}")
            return None
    
    tempo_final = time.time()
    with st.sidebar:
        st.session_state['tempo_resposta'] = tempo_final - tempo_inicial
    
    return resposta


def save_conversation(conversa_atual, input_usuario, resposta):
    """Salva a conversa no banco de dados."""
    if 'titulo_atualizado' not in st.session_state:
        atualizar_titulo_conversa(conversa_atual, input_usuario[:TITLE_TRUNCATE_LENGTH])
        st.session_state['titulo_atualizado'] = True
        st.cache_data.clear()
    
    try:
        salvar_mensagem(conversa_atual, 'user', input_usuario)
        salvar_mensagem(conversa_atual, 'assistant', resposta)
    except Exception as e:
        st.error(f"Erro ao salvar mensagens: {str(e)}")


def handle_user_input(input_usuario):
    """Processa a entrada do usuário, incluindo arquivos carregados e contexto RAG."""
    conversa_atual = st.session_state.get('conversa_atual')
    historico = get_historico()

    if not conversa_atual:
        inicia_nova_conversa_service()
        conversa_atual = st.session_state.get('conversa_atual')
        historico = get_historico()

    # Processa arquivos carregados
    contexto_arquivos = process_uploaded_files()

    # Mostra feedback visual se há arquivos sendo processados
    if contexto_arquivos:
        with st.spinner("Processando arquivos carregados..."):
            time.sleep(0.5)  # Feedback visual
        st.success(f"{len(st.session_state.get('uploaded_files', []))} arquivo(s) processado(s)")

    # Processa contexto RAG (abordagem híbrida)
    rag_context = ""
    if st.session_state.get('rag_ativo', False) or st.session_state.get('use_rag_onetime', False):
        base_selecionada = st.session_state.get('rag_base_selecionada')
        if base_selecionada:
            with st.spinner(f"Consultando base de conhecimento RAG: {base_selecionada}..."):
                rag_context = consultar_base_de_conhecimento(input_usuario, base_selecionada)
            if rag_context:
                st.info("Contexto RAG adicionado.")
            # Reseta o flag de uso único após a consulta
            st.session_state['use_rag_onetime'] = False
        else:
            st.warning("Por favor, selecione uma base de conhecimento na aba RAG para usar o RAG.")

    # Constrói o input final para o modelo
    input_para_modelo = input_usuario
    if contexto_arquivos:
        input_para_modelo = f"CONTEXTO DOS ARQUIVOS CARREGADOS:\n{contexto_arquivos}\n\n{input_para_modelo}"
    if rag_context:
        input_para_modelo = f"CONTEXTO DA BASE DE CONHECIMENTO:\n{rag_context}\n\n{input_para_modelo}"

    adicionar_mensagem(historico, 'user', input_usuario) # Salva o input original do usuário no histórico
    memoria = reconstruir_memoria(historico)

    # Passa o input final (com arquivos e/ou RAG) para a IA
    resposta = process_ai_response(input_para_modelo, memoria)
    if resposta is None:
        return

    adicionar_mensagem(historico, 'assistant', resposta)
    st.session_state['historico'] = historico

    save_conversation(conversa_atual, input_usuario, resposta)

    # IMPORTANTE: Limpa os arquivos após processar para evitar reprocessamento
    st.session_state['uploaded_files'] = []

    st.rerun()


def interface_chat():
    """Interface principal de chat da JibóIA."""
    render_chat_ui()
    
    historico = get_historico()
    renderiza_mensagens(historico)
    
    input_usuario = st.chat_input(CHAT_INPUT_PLACEHOLDER)
    
    if input_usuario:
        handle_user_input(input_usuario)
    
    st.markdown('</div>', unsafe_allow_html=True)