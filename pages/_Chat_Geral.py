from dotenv import load_dotenv
import os
import time
import streamlit as st

# Importa a inicialização comum do app principal
from app import inicializacao

from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

from db.db_sqlite import *

from utils.configs import *
# from utils.files import *

load_dotenv()

# Inicializa sessão e banco de dados caso esta página seja acessada diretamente
inicializacao()

# Garante que o estado necessário esteja configurado mesmo acessando esta página diretamente

def carrega_modelo(provedor, modelo, api_key=None):
    """Configura e instancia o modelo de linguagem selecionado pelo usuário.

    Esta função utiliza o padrão de design de "fábrica" para dinamicamente
    selecionar e configurar o modelo de linguagem (LLM) com base nas escolhas
    do usuário. Ela busca a classe de chat correspondente (ex: ChatOpenAI) e
    os modelos disponíveis a partir do dicionário `config_modelos`.

    Args:
        provedor (str): O nome do provedor do modelo (ex: 'OpenAI', 'Groq').
        modelo (str): O identificador do modelo específico a ser usado.
        api_key (str, optional): A chave de API para o provedor. Se não for
            fornecida, a função tentará obtê-la das variáveis de ambiente.

    Processo:
    1.  Cria um `ChatPromptTemplate` para estruturar a conversa com o LLM.
    2.  Busca a classe de chat correta em `utils.configs.config_modelos`.
    3.  Instancia a classe, passando a chave de API (se necessária).
    4.  Cria uma "chain" (LCEL) que conecta o template ao modelo.
    5.  Armazena a `chain` e o nome do modelo no `st.session_state` para uso
        posterior na aplicação.
    """

    # documento = carrega_arquivo(tipo_arquivo, arquivo)
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
            # st.stop() # Removido para permitir a renderização completa da UI
        chat = chat_class(model=modelo, api_key=api_key)
    
    chain = template | chat

    st.session_state['chain'] = chain
    st.session_state['modelo_nome'] = f"{provedor} - {modelo}"


# TABS ==================================================
def tab_conversas(tab):
    """Renderiza a aba de gerenciamento de conversas na barra lateral.

    Esta função é responsável por toda a interatividade na aba "Conversas":
    -   Exibe o botão "Nova conversa" para iniciar um novo chat.
    -   Busca e lista todas as conversas existentes do banco de dados.
    -   Cria um botão para cada conversa, permitindo ao usuário carregá-la.
    -   Desabilita o botão da conversa que já está ativa.
    -   Oferece um campo para renomear a conversa ativa.

    Args:
        tab: O objeto de aba do Streamlit onde os componentes serão desenhados.
    """

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
    
    conversa_id = st.session_state.get('conversa_atual')
    if conversa_id:
        titulo_atual = get_titulo_conversa(conversa_id)

        novo_titulo = tab.text_input("Renomear conversa", value=titulo_atual, key="input_titulo")

        if tab.button("Salvar título", use_container_width=True, key="salva_titulo"):
            if novo_titulo.strip():
                atualizar_titulo_conversa(conversa_id, novo_titulo.strip())
                seleciona_conversa(conversa_id)  # Recarrega memória
                st.rerun()



def inicia_nova_conversa():
    """Cria e carrega uma nova sessão de conversa.

    Esta função é chamada quando o usuário clica no botão '➕ Nova conversa'.
    Ela executa os seguintes passos:
    1.  Cria uma nova instância de `ConversationBufferMemory` para um histórico limpo.
    2.  Chama `criar_conversa()` para criar um novo registro no banco de dados
        com o título provisório 'Nova conversa'.
    3.  Armazena o ID da nova conversa e a nova memória no `st.session_state`,
        tornando-a a conversa ativa.
    4.  Reseta a flag `titulo_atualizado` para que o título possa ser definido
        automaticamente a partir da primeira mensagem do usuário.
    """
    memoria = ConversationBufferMemory(return_messages=True)
    st.session_state['memoria'] = memoria

    provedor = st.session_state.get('provedor', 'Desconhecido')
    modelo = st.session_state.get('modelo', 'Desconhecido')
    conversa_id = criar_conversa('Nova conversa', provedor, modelo)

    st.session_state['conversa_atual'] = conversa_id

    # 🔄 Reset flag de título
    if 'titulo_atualizado' in st.session_state:
        del st.session_state['titulo_atualizado']



def seleciona_conversa(conversa_id):
    """Carrega o histórico de uma conversa existente para a memória.

    Quando um usuário clica no botão de uma conversa salva, esta função é
    acionada para carregar o estado daquela conversa.

    Args:
        conversa_id (int): O ID da conversa a ser carregada do banco de dados.

    Processo:
    1.  Busca todas as mensagens associadas ao `conversa_id` no banco.
    2.  Cria uma nova instância de `ConversationBufferMemory`.
    3.  Itera sobre as mensagens carregadas e as adiciona à memória, recriando
        o histórico do diálogo.
    4.  Atualiza o `st.session_state` com a nova memória e o ID da conversa
        selecionada.
    """
    mensagens = carregar_mensagens(conversa_id)

    memoria = ConversationBufferMemory(return_messages=True)
    for m in mensagens:
        if m['role'] == 'user':
            memoria.chat_memory.add_user_message(m['content'])
        else:
            memoria.chat_memory.add_ai_message(m['content'])

    st.session_state['memoria'] = memoria
    st.session_state['conversa_atual'] = conversa_id

def tab_configuracoes(tab):
    """Renderiza a aba de configurações do modelo na barra lateral.

    Permite ao usuário selecionar o provedor (Ollama, Groq, OpenAI) e o modelo
    específico que deseja usar. As opções são populadas dinamicamente a partir
    do dicionário `config_modelos`.

    Ao clicar em "Iniciar Oráculo", a função `carrega_modelo` é chamada com
    as seleções feitas.

    Args:
        tab: O objeto de aba do Streamlit onde os componentes serão desenhados.
    """

    provedor = tab.selectbox('Selecione o provedor', config_modelos.keys())
    modelo_escolhido = tab.selectbox('Selecione o modelo', config_modelos[provedor]['modelos'])

    st.session_state['modelo'] = modelo_escolhido
    st.session_state['provedor'] = provedor

    if tab.button('Iniciar Oráculo', use_container_width=True):
        carrega_modelo(provedor, modelo_escolhido)


# Conteúdo principal da página _Chat_Geral.py
st.header('VeronIA', divider=True)

# Debug temporário - você pode remover depois que funcionar
with st.expander("🔍 Informações de Debug (remover depois)"):
    st.write("**Session State atual:**")
    st.write(f"- Conversa atual: {st.session_state.get('conversa_atual', 'Nenhuma')}")
    st.write(f"- Memória existe: {'memoria' in st.session_state}")
    st.write(f"- Chain existe: {'chain' in st.session_state}")
    st.write(f"- Modelo: {st.session_state.get('modelo_nome', 'Não definido')}")

# Verifica se o modelo foi configurado
chain = st.session_state.get('chain')
if not chain:
    st.warning("⚙️ **Passo 1:** Configure um modelo na aba 'Configurações' da barra lateral")
    st.warning("⚙️ **Passo 2:** Clique em 'Iniciar Oráculo'")
    st.warning("⚙️ **Passo 3:** Crie uma nova conversa na aba 'Conversas'")
    # st.stop() # Removido para permitir a renderização completa da UI

# Verifica se existe uma conversa carregada
memoria = st.session_state.get('memoria')
conversa_atual = st.session_state.get('conversa_atual')

if not conversa_atual:
    st.warning("📝 **Nenhuma conversa selecionada**")
    st.info("👈 Vá para a aba 'Conversas' na barra lateral e clique em '➕ Nova conversa'")
    # st.stop() # Removido para permitir a renderização completa da UI

if not memoria or not hasattr(memoria, "buffer_as_messages"):
    st.error("❌ Problema com a memória da conversa")
    st.stop()

# Mostra informações do modelo atual
with st.sidebar:
    st.title("🔮 VeronIA")  # Título da barra lateral para esta página
    tab1, tab2 = st.sidebar.tabs(['💬 Conversas', '⚙️ Config'])
    tab_conversas(tab1)
    tab_configuracoes(tab2)
    
    # Botão de ajuda
    with st.expander("❓ Precisa de ajuda?"):
        st.markdown("""
        **Como usar:**
        1. Configure um modelo na aba 'Config'
        2. Clique em 'Iniciar Oráculo'
        3. Crie uma nova conversa
        4. Comece a conversar!
        """)

    modelo_nome = st.session_state.get('modelo_nome', 'Desconhecido')
    st.success(f"🔮 **Modelo ativo:** {modelo_nome}")
    
    if conversa_atual:
        st.info(f"💬 **Conversa:** {get_titulo_conversa(conversa_atual)}")

# Renderiza histórico de mensagens
if memoria and hasattr(memoria, "buffer_as_messages"):
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

# Campo de entrada do usuário
input_usuario = st.chat_input('Fale com o Oráculo...')

if input_usuario:
    tempo_inicial = time.time()

    # Exibe mensagem do usuário
    chat = st.chat_message('human')
    chat.markdown(input_usuario)

    # Gera resposta da IA
    chat = st.chat_message('ai')
    chat_history = memoria.buffer_as_messages if memoria and hasattr(memoria, "buffer_as_messages") else []
    resposta = chat.write_stream(chain.stream({
        'input': input_usuario,
        'chat_history': chat_history
    }))

    # Calcula tempo de resposta
    tempo_final = time.time()
    tempo_de_resposta = tempo_final - tempo_inicial
    with st.sidebar:
        st.caption(f'⏱️ Tempo: {tempo_de_resposta:.2f}s')

    # Atualiza memória
    memoria.chat_memory.add_user_message(input_usuario)
    memoria.chat_memory.add_ai_message(resposta)
    st.session_state['memoria'] = memoria

    # Atualiza título na primeira mensagem
    if 'titulo_atualizado' not in st.session_state:
        novo_titulo = input_usuario[:30]
        atualizar_titulo_conversa(conversa_atual, novo_titulo)
        st.session_state['titulo_atualizado'] = True

    # Salva no banco
    salvar_mensagem(conversa_atual, 'user', input_usuario)
    salvar_mensagem(conversa_atual, 'assistant', resposta)
