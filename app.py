from dotenv import load_dotenv
import os
import time
import streamlit as st

from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

from db.db_sqlite import *
from utils.configs import *

load_dotenv()

def criar_header_fixo():
    """Renderiza um cabeçalho fixo com informações do modelo de IA."""
    modelo = st.session_state.get('modelo_nome', 'Modelo não carregado')

    st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 1;
        right: 0;
        z-index: 999;
        background: linear-gradient(90deg, #667eea, #764ba2);
        padding: 15px 10px 0px 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-radius: 30%;
        margin-top: 10px;
    }

    .fixed-header small {
        display: block;
        margin: 10% 0;
        font-size: 16px;
        color: #eeeeee;
    }

    .fixed-header-content {
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-family: sans-serif;
    }

    .chat-main-area {
        margin-top: 100px; /* Ajustado para compensar o padding maior */
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="fixed-header">
        <div class="fixed-header-content">
            <div style="text-align: center;">
                <br>
                <small>{modelo}</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# INICIALIZAÇÃO ==================================================
def inicializacao():
    """Prepara o ambiente da aplicação na inicialização.

    Esta função é crucial e executa duas tarefas principais:
    1.  `init_database()`: Garante que o banco de dados e suas tabelas
        estejam prontos para uso, criando-os se necessário.
    2.  Popula o `st.session_state`: O `session_state` é o mecanismo
        do Streamlit para manter dados persistentes entre as interações
        do usuário. Esta função define valores padrão para chaves essenciais
        (como 'memoria', 'chain', 'conversa_atual') na primeira vez que o
        usuário abre a aplicação, evitando que o estado seja perdido a cada
        ação na UI.
    """
    
    # 1. Primeiro, inicializa o banco
    try:
        init_database()
    except Exception as e:
        st.error(f"❌ Erro ao inicializar banco de dados: {e}")
        # Não usamos st.stop() aqui para permitir que o app continue, mas com erro visível.
        # O usuário precisará resolver o problema do banco para usar a funcionalidade.
        return # Sai da função inicializacao se houver erro no banco
    
    # 2. Configurações padrão do session state
    defaults = {
        'mensagens': [],
        'conversa_atual': '',
        'api_key': os.getenv("OPENAI_API_KEY", ""),
        'memoria': None, # A memória será inicializada na página do agente
        'chain': None, # A chain será inicializada na página do agente
        'modelo_nome': 'Nenhum modelo carregado',
        'provedor': 'OpenAI',  # Provedor padrão
        'modelo': 'gpt-4o-mini'  # Modelo padrão
    }
    
    # 3. Aplica os valores padrão apenas se não existirem
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    print("✅ Inicialização concluída")

def carrega_modelo(provedor, modelo, api_key=None):
    """Configura e instancia o modelo de linguagem selecionado pelo usuário."""
    system_prompt = f'''
        Você é um assistente atencioso aos detalhes.
        '''

    template = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])

    chat_class = config_modelos[provedor]['chat']
    
    if provedor == 'Ollama':
        chat = chat_class(model=modelo)
    else:
        api_key = os.getenv(f"{provedor.upper()}_API_KEY")
        if not api_key:
            st.error(f"API key para {provedor} não encontrada no .env.")
        chat = chat_class(model=modelo, api_key=api_key)
    
    chain = template | chat
    st.session_state['chain'] = chain
    st.session_state['modelo_nome'] = f"{provedor} - {modelo}"

def inicia_nova_conversa():
    """Cria e carrega uma nova sessão de conversa."""
    memoria = ConversationBufferMemory(return_messages=True)
    st.session_state['memoria'] = memoria

    provedor = st.session_state.get('provedor', 'Groq')
    modelo = st.session_state.get('modelo', 'llama-3.1-8b-instant')
    conversa_id = criar_conversa('Nova conversa', provedor, modelo)

    st.session_state['conversa_atual'] = conversa_id

    if 'titulo_atualizado' in st.session_state:
        del st.session_state['titulo_atualizado']

def inicializa_jiboia():
    """Inicializa modelo padrão, mas não cria conversa até o usuário interagir."""
    if not st.session_state.get('chain'):
        provedor = 'Groq'
        modelo = 'llama-3.1-8b-instant'
        st.session_state['provedor'] = provedor
        st.session_state['modelo'] = modelo
        try:
            carrega_modelo(provedor, modelo)
        except Exception as e:
            pass


def seleciona_conversa(conversa_id):
    """Carrega o histórico de uma conversa existente para a memória."""
    mensagens = carregar_mensagens(conversa_id)

    memoria = ConversationBufferMemory(return_messages=True)
    for m in mensagens:
        if m['role'] == 'user':
            memoria.chat_memory.add_user_message(m['content'])
        else:
            memoria.chat_memory.add_ai_message(m['content'])

    st.session_state['memoria'] = memoria
    st.session_state['conversa_atual'] = conversa_id

def tab_conversas(tab):
    """Renderiza a aba de gerenciamento de conversas na barra lateral."""
    tab.button('➕ Nova conversa', on_click=inicia_nova_conversa, use_container_width=True)
    tab.markdown('')

    conversas = listar_conversas()
    for id, titulo in conversas:
        if len(titulo) == 30:
            titulo += '...'
        tab.button(
            titulo,
            key=f"conversa_{id}",
            on_click=seleciona_conversa,
            args=(id,),
            disabled=id == st.session_state.get('conversa_atual'),
            use_container_width=True
        )
    


def tab_configuracoes(tab):
    """Renderiza a aba de configurações do modelo na barra lateral."""
    provedor = tab.selectbox('Selecione o provedor', config_modelos.keys())
    modelo_escolhido = tab.selectbox('Selecione o modelo', config_modelos[provedor]['modelos'])

    conversa_id = st.session_state.get('conversa_atual')
    if conversa_id:
        titulo_atual = get_titulo_conversa(conversa_id)
        novo_titulo = tab.text_input("Renomear conversa atual:", value=titulo_atual, key="input_titulo")
        if tab.button("Salvar título", use_container_width=True, key="salva_titulo"):
            if novo_titulo.strip():
                atualizar_titulo_conversa(conversa_id, novo_titulo.strip())
                seleciona_conversa(conversa_id)
                st.rerun()

    st.session_state['modelo'] = modelo_escolhido
    st.session_state['provedor'] = provedor

    if tab.button('Aplicar Modelo', use_container_width=True):
        carrega_modelo(provedor, modelo_escolhido)

def interface_chat():
    """Interface principal de chat da JibóIA."""
    criar_header_fixo()  # <- chama o header fixo antes de tudo

    st.markdown('<div class="chat-main-area">', unsafe_allow_html=True)
    st.header('🔮 JibóIA - VerônIA', divider=True)

    
    # Verifica se o modelo foi configurado
    chain = st.session_state.get('chain')
    if not chain:
        st.info("🚀 **Inicializando JibóIA...** Por favor, aguarde alguns segundos.")

    # Verifica se existe uma conversa ativa e memória
    memoria = st.session_state.get('memoria')
    conversa_atual = st.session_state.get('conversa_atual')

    if not conversa_atual and not memoria:
        st.info("👋 Olá! Sou a JibóIA. Me diga como posso ajudar e criarei uma nova conversa para você.")

        # Mensagem informativa sobre modelo padrão
        if st.session_state.get('modelo_nome') == 'Groq - llama-3.1-8b-instant':
            st.info("💡 Você está usando o modelo padrão (Groq - llama-3.1-8b-instant). A qualquer momento, altere na aba ⚙️ Config.")


        # Botão de ajuda
        with st.expander("❓ Como usar"):
            st.markdown("""
            **JibóIA está pronta para uso:**
            1. ✅ Modelo já carregado automaticamente!
            2. ✅ Conversa iniciada automaticamente!
            3. 🚀 Comece a conversar agora mesmo!
            
            💡 **Dica:** Use a aba 'Config' para trocar de modelo.
            """)

    else:
        if not memoria or not hasattr(memoria, "buffer_as_messages"):
            st.error("❌ Problema com a memória da conversa")
            st.stop()


    # Sidebar
    with st.sidebar:
        st.title("🔮 JibóIA")
        tab1, tab2 = st.sidebar.tabs(['💬 Conversas', '⚙️ Config'])
        tab_conversas(tab1)
        tab_configuracoes(tab2)
                

    # Renderiza histórico de mensagens
    if memoria and hasattr(memoria, "buffer_as_messages"):
        for mensagem in memoria.buffer_as_messages:
            chat = st.chat_message(mensagem.type)
            chat.markdown(mensagem.content)

    # Campo de entrada do usuário
    input_usuario = st.chat_input('Fale com a JibóIA...')

    if input_usuario:
        # Cria nova conversa e memória se ainda não existirem
        if not st.session_state.get('conversa_atual') or not st.session_state.get('memoria'):
            inicia_nova_conversa()

        memoria = st.session_state.get('memoria')
        conversa_atual = st.session_state.get('conversa_atual')

        if memoria is None:
            st.error("❌ Falha ao iniciar a memória da conversa. Tente recarregar a página.")
            st.stop()

        tempo_inicial = time.time()

        # Exibe mensagem do usuário
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        # Gera resposta da IA
        chat = st.chat_message('ai')
        chat_history = memoria.buffer_as_messages if hasattr(memoria, "buffer_as_messages") else []
        resposta = chat.write_stream(st.session_state['chain'].stream({
            'input': input_usuario,
            'chat_history': chat_history
        }))

        # Tempo de resposta
        tempo_final = time.time()
        with st.sidebar:
            st.caption(f'⏱️ Tempo: {tempo_final - tempo_inicial:.2f}s')

        # Atualiza memória
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

        # Atualiza título
        if 'titulo_atualizado' not in st.session_state:
            atualizar_titulo_conversa(conversa_atual, input_usuario[:30])
            st.session_state['titulo_atualizado'] = True

        # Persistência no banco
        salvar_mensagem(conversa_atual, 'user', input_usuario)
        salvar_mensagem(conversa_atual, 'assistant', resposta)


    st.markdown('</div>', unsafe_allow_html=True)


# MAIN ==================================================
def main():
    """Ponto de entrada principal da aplicação Streamlit.

    Configura a página (título, ícone) e organiza o layout, definindo a
    barra lateral com suas abas e chamando a `pagina_principal` para
    renderizar o conteúdo central.
    """
    st.set_page_config(
        page_title="JibóIA - VerônIA",
        page_icon="🔮",
        layout="wide"
    )
    
    # Inicializa tudo
    inicializacao()
    inicializa_jiboia()
    
    # Interface principal da JibóIA
    interface_chat()
    
if __name__ == '__main__':
    main()