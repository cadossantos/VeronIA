import streamlit as st
import os
import json
import subprocess
import tempfile
from services.conversation_service import (
    inicia_nova_conversa_service,
    seleciona_conversa_service,
    listar_conversas_cached,
    renomear_conversa_service,
    excluir_conversa_service
)
from services.upload_service import carrega_arquivo
from utils.configs import config_modelos

def toggle_rag_mode():
    """Ativa ou desativa o modo RAG e limpa o histórico de chat."""
    st.session_state.rag_mode = not st.session_state.get('rag_mode', False)
    st.session_state.historico = []
    status = "ativado" if st.session_state.rag_mode else "desativado"
    st.toast(f"Modo RAG {status}.")

def train_rag_agent():
    """Inicia o processo de ingestão de um documento carregado."""
    if 'documento_carregado' not in st.session_state or not st.session_state.documento_carregado:
        st.warning("Nenhum documento carregado para treinar.")
        return

    with st.spinner("Processando e treinando o agente com a nova fonte..."):
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json', encoding='utf-8') as temp_file:
                document_data = {
                    "title": st.session_state.get('upload_tipo', 'Documento'),
                    "url": st.session_state.get('upload_url', ''),
                    "content": st.session_state.documento_carregado
                }
                json.dump(document_data, temp_file)
                temp_filepath = temp_file.name
            
            process = subprocess.run(
                ["python", "scripts/run_ingest.py", temp_filepath],
                capture_output=True, text=True, check=True
            )
            st.success("Agente treinado com sucesso!")
            st.info(process.stdout)
        except subprocess.CalledProcessError as e:
            st.error(f"Falha ao treinar o agente: {e.stderr}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
        finally:
            if 'temp_filepath' in locals() and os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            if 'documento_carregado' in st.session_state:
                del st.session_state['documento_carregado']

def render_sidebar():
    """Renderiza a barra lateral com todas as opções da aplicação."""
    with st.sidebar:
        st.title("VerônIA")
        st.markdown("Sua assistente de IA versátil.")

        tab_conversas, tab_opcoes = st.tabs(["Conversas", "Opções"])

        with tab_conversas:
            if st.button("＋ Nova Conversa", use_container_width=True):
                inicia_nova_conversa_service()
            
            conversas = listar_conversas_cached()
            for conv in conversas:
                col1, col2, col3 = st.columns([4, 1, 1])
                with col1:
                    if st.button(f"{conv['titulo']}", key=f"conv_{conv['id']}", use_container_width=True):
                        seleciona_conversa_service(conv['id'])
                with col2:
                    if st.button("✏️", key=f"edit_{conv['id']}"):
                        st.session_state.renaming_conv_id = conv['id']
                with col3:
                    if st.button("🗑️", key=f"del_{conv['id']}"):
                        excluir_conversa_service(conv['id'])

                if st.session_state.get('renaming_conv_id') == conv['id']:
                    novo_titulo = st.text_input("Novo título:", value=conv['titulo'], key=f"new_title_{conv['id']}")
                    if st.button("Salvar", key=f"save_{conv['id']}"):
                        renomear_conversa_service(conv['id'], novo_titulo)
                        st.session_state.renaming_conv_id = None
                        st.rerun()

        with tab_opcoes:
            st.header("Fonte de Dados (RAG)")
            arquivos_validos = ['Site', 'YouTube', 'PDF', 'CSV', 'TXT']
            tipo_arquivo = st.selectbox('Selecione o tipo de fonte', arquivos_validos, key='upload_tipo')
            
            arquivo_input = None
            if tipo_arquivo in ['Site', 'YouTube']:
                arquivo_input = st.text_input(f'Digite a URL do {tipo_arquivo}', key='upload_url')
            else:
                arquivo_input = st.file_uploader('Faça o upload do arquivo', type=[tipo_arquivo.lower()], key='upload_file')

            if st.button("Processar Fonte", use_container_width=True):
                if arquivo_input:
                    conteudo = carrega_arquivo(tipo_arquivo, arquivo_input)
                    if conteudo:
                        st.session_state['documento_carregado'] = conteudo
                        st.success("Fonte de dados carregada com sucesso!")
                else:
                    st.warning("Por favor, forneça um arquivo ou URL.")

            with st.expander("Configurações Gerais"):
                st.selectbox(
                    "Provedor", 
                    options=config_modelos.keys(), 
                    key='provedor',
                    index=list(config_modelos.keys()).index(st.session_state.get('provedor', 'Groq'))
                )
                st.selectbox(
                    "Modelo", 
                    options=config_modelos[st.session_state.get('provedor', 'Groq')]['modelos'], 
                    key='modelo',
                    index=config_modelos[st.session_state.get('provedor', 'Groq')]['modelos'].index(st.session_state.get('modelo', 'llama-3.3-70b-versatile'))
                )
                st.radio(
                    "Modo de Operação",
                    options=["Normal", "Post-it", "Redator", "Tradutor", "WebSearch"],
                    key='operation_mode',
                    horizontal=True
                )
                st.selectbox(
                    "Formato da Resposta",
                    options=["Normal", "Curta", "Detalhada", "Lista", "Código", "Resumo Executivo"],
                    key='response_format'
                )

            with st.expander("Agente RAG"):
                rag_button_text = "Desativar Agente RAG" if st.session_state.get('rag_mode', False) else "Ativar Agente RAG"
                if st.button(rag_button_text, use_container_width=True):
                    toggle_rag_mode()
                if st.button("Treinar Agente com Fonte Carregada", use_container_width=True):
                    train_rag_agent()