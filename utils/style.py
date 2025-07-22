import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
/* --- FONTES E BASE --- */

/**
 * @import
 * Importa duas fontes do Google Fonts para um visual mais sofisticado:
 * - 'Inter': Uma fonte sans-serif limpa e moderna para o corpo do texto.
 * - 'Playfair Display': Uma fonte serifada elegante para títulos.
 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500;600&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');

/**
 * Seletor Universal (*)
 * Define a fonte padrão para todos os elementos da página como 'Inter'.
 * Isso garante uma base de texto consistente.
 */
* {
    font-family: 'Libre Baskerville', sans-serif;
}

/**
 * Estilização de Títulos (h1, h2, h3)
 * Aplica a fonte 'Playfair Display' para dar um toque de elegância aos títulos.
 * A cor e o peso são definidos para combinar com a paleta de cores "orgânica".
 * '!important' é usado para garantir que essas regras sobreponham os estilos padrão do Streamlit.
 */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #2F3A1F !important; /* Verde musgo escuro */
    font-weight: 500 !important;
}

/* --- LAYOUT PRINCIPAL --- */

/**
 * Background da Área Principal (.main > div)
 * Seleciona o contêiner principal da aplicação Streamlit.
 * Aplica um gradiente linear suave com tons de bege e areia para criar uma
 * textura de fundo que remete a papel antigo ou papiro.
 */
.main > div {
    background: linear-gradient(135deg, 
        #E7DBCB 0%, 
        #E8DCC0 30%, 
        #DDD2B8 70%, 
        #D2C7A8 100%) !important;
}
                
/* --- BARRA LATERAL (SIDEBAR) --- */

/**
 * Estilo da Barra Lateral ([data-testid="stSidebar"])
 * Usa um seletor de atributo para encontrar a sidebar do Streamlit.
 * Aplica um gradiente vertical com tons de verde oliva para um visual natural.
 * Adiciona uma borda direita em tom de couro para separar visualmente do conteúdo principal.
 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, 
        #666F43 0%, 
        #5A5E38 50%, 
        #4E522D 100%) !important;
    border-right: 3px solid #9B643B !important; /* Tom de couro */
}

/**
 * Espaçamento Interno da Sidebar
 * Ajusta o padding para dar mais respiro aos elementos dentro da sidebar.
 */
[data-testid="stSidebar"] > div {
    padding: 1rem 1.5rem !important;
}

/**
 * Título/Logo na Sidebar
 * Estiliza o título principal (h1) dentro da sidebar.
 * A cor clara contrasta com o fundo escuro.
 * A sombra de texto (text-shadow) adiciona profundidade.
 */
[data-testid="stSidebar"] h1 {
    color: #E7DBCB !important; /* Bege claro */
    text-align: center;
    font-size: 2.2rem !important;
    margin-bottom: 2rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

/* --- COMPONENTES EXPANSÍVEIS (EXPANDERS) --- */

/**
 * Estilo do Expander ([data-testid="stExpander"])
 * O expander (acordeão) ganha um fundo verde, bordas arredondadas e uma sombra suave.
 * `backdrop-filter: blur(10px)` cria um efeito de vidro fosco se houver elementos atrás.
 * `transition` suaviza todas as mudanças de estilo (ex: no hover).
 */
[data-testid="stExpander"] {
    background: #666f43 !important; /* Verde oliva */
    border: 2px solid #B2976B !important; /* Tom de madeira clara */
    border-radius: 16px !important;
    margin: 1rem 0 !important;
    box-shadow: 0 4px 12px rgba(155, 100, 59, 0.15) !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.3s ease !important;
}

/**
 * Efeito Hover no Expander
 * Ao passar o mouse, a sombra aumenta e o expander se move levemente para cima,
 * criando um efeito de "flutuação" que indica interatividade.
 */
[data-testid="stExpander"]:hover {
    box-shadow: 0 6px 20px rgba(155, 100, 59, 0.25) !important;
    transform: translateY(-2px) !important;
}

/**
 * Título do Expander (summary)
 * Estiliza o texto do título clicável do expander.
 */
[data-testid="stExpander"] summary {
    color: #B2976B !important; /* Tom de madeira clara */
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 1rem 1.5rem !important;
}

/**
 * Efeito Hover no Título do Expander
 * Muda a cor do texto ao passar o mouse para um tom mais claro, melhorando o feedback.
 */
[data-testid="stExpander"] summary:hover {
    color: #E7DBCB !important; /* Bege claro */
}

/**
 * Conteúdo do Expander
 * O contêiner que guarda o conteúdo do expander recebe um fundo semitransparente
 * e cantos arredondados na parte inferior para se alinhar com o contêiner pai.
 */
[data-testid="stExpander"] > div > div {
    background: rgba(246, 239, 221, 0.8) !important;
    border-radius: 0 0 16px 16px !important;
    padding: 1.5rem !important;
}
                
/* --- WIDGETS (COMPONENTES DE UI) --- */

/**
 * Caixa de Seleção (Selectbox)
 * Estiliza o widget de dropdown com fundo verde, bordas em tom de couro e sombra interna.
 */
[data-testid="stSelectbox"] > div {
    background: rgba(102, 111, 67, 0.9) !important;
    border: 2px solid #9B643B !important;
    border-radius: 12px !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1) !important;
    transition: all 0.3s ease !important;
}

/**
 * Efeito Hover na Selectbox
 * Muda a cor da borda para um tom de dourado e adiciona um brilho (box-shadow)
 * para indicar que o elemento é interativo.
 */
[data-testid="stSelectbox"] > div:hover {
    border-color: #FAB101 !important; /* Dourado */
    box-shadow: 0 0 12px rgba(250, 177, 1, 0.3) !important;
}

/**
 * Texto dentro da Selectbox
 * Garante que o texto dentro da caixa de seleção seja claro e legível.
 */
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    color: #E7DBCB !important; /* Bege claro */
    font-weight: 500 !important;
}

/**
 * Área de Upload de Arquivos (File Uploader)
 * A área de arrastar e soltar arquivos é estilizada com um fundo semitransparente,
 * borda tracejada e cantos arredondados.
 */
[data-testid="stFileUploader"] section {
    background: rgba(178, 151, 107, 0.2) !important;
    border: 2px dashed #9B643B !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}

/**
 * Efeito Hover no File Uploader
 * Ao passar o mouse, o fundo fica um pouco mais opaco e o componente aumenta
 * de tamanho sutilmente (`transform: scale(1.02)`).
 */
[data-testid="stFileUploader"] section:hover {
    background: rgba(178, 151, 107, 0.3) !important;
    transform: scale(1.02) !important;
}
                
/**
 * Texto do File Uploader
 * Estiliza o texto "Arraste e solte arquivos aqui".
 */
[data-testid="stFileUploader"] section p {
    color: #2F3A1F !important; /* Verde musgo escuro */
    font-weight: 500 !important;
}
                
/**
 * Sliders
 * A barra do slider é preenchida com um gradiente dourado.
 */
[data-testid="stSlider"] {
    padding: 1rem 0 !important;
}
[data-testid="stSlider"] > div > div {
    # background: linear-gradient(90deg, #9B643B, #FAB101) !important;
}

/* --- MENSAGENS DE CHAT --- */

/**
 * Balão de Mensagem do Usuário (.mensagem-user)
 * Estiliza o balão de chat para as mensagens enviadas pelo usuário.
 * `align-self: flex-end` alinha o balão à direita.
 * O gradiente e a sombra dão um aspecto tridimensional.
 * `border-radius` cria a forma arredondada do balão.
 */
.mensagem-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #B2976B, #9B643B) !important;
    color: #E7DBCB !important;
    border-radius: 20px 20px 5px 20px !important;
    padding: 1rem 1.5rem !important;
    margin: 0.5rem 0 !important;
    box-shadow: 0 4px 12px rgba(155, 100, 59, 0.3) !important;
    position: relative;
    max-width: 80%;
    word-wrap: break-word;
    font-weight: 400;
    line-height: 1.5;
}

/**
 * "Rabo" do Balão do Usuário (.mensagem-user::after)
 * O pseudo-elemento `::after` é usado para criar um pequeno triângulo
 * que simula a "cauda" do balão de fala, apontando para o usuário.
 * É construído usando bordas transparentes e coloridas.
 */
.mensagem-user::after {
    content: '';
    position: absolute;
    bottom: 0;
    right: -12px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-top: 8px solid #9B643B;
    border-left: 8px solid #9B643B;
}

/**
 * Balão de Mensagem do Assistente (.mensagem-assistente)
 * Similar ao do usuário, mas alinhado à esquerda (`align-self: flex-start`)
 * e com uma paleta de cores diferente (tons de verde).
 */
.mensagem-assistente {
    align-self: flex-start;
    background: linear-gradient(135deg, #666F43, #5A5E38) !important;
    color: #E7DBCB !important;
    border-radius: 20px 20px 20px 5px !important;
    padding: 2.5rem 2.5rem !important;
    margin: 0.5rem 0 !important;
    box-shadow: 0 4px 12px rgba(102, 111, 67, 0.3) !important;
    position: relative;
    max-width: 80%;
    word-wrap: break-word;
    font-weight: 400;
    line-height: 1.5;
}

/**
 * "Rabo" do Balão do Assistente
 * Cria a cauda do balão de fala para o assistente, apontando para a esquerda.
 */
.mensagem-assistente::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: -13px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-top: 8px solid #5A5E38;
    border-right: 8px solid #5A5E38;
}

/* --- BOTÕES --- */

/**
 * Estilo Padrão de Botão (.stButton > button)
 * Define um visual consistente para todos os botões.
 * O `padding` e `font-size` foram ajustados para um visual mais compacto.
 */
.stButton > button {
    background: #3B421F  !important; /* Verde bem escuro */
    color: #E7DBCB !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 0.7rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.5px;
}

/**
 * Efeito Hover no Botão
 * Ao passar o mouse, o botão se move para cima e uma sombra aparece,
 * dando um feedback tátil ao usuário.
 */
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 3px 6px #666f438e !important;
}

/* --- ABAS (TABS) --- */

/**
 * Estilo das Abas (button[data-baseweb="tab"])
 * Estiliza as abas não selecionadas.
 * O `font-size` foi reduzido para acomodar mais abas se necessário.
 */
button[data-baseweb="tab"] {
    background: rgba(178, 151, 107, 0.1) !important;
    color: #2F3A1F !important;
    border: none !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 1rem 1rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin: 0 0.25rem !important;
    transition: all 0.4s ease !important;
}

/**
 * Efeito Hover nas Abas
 * Muda a cor de fundo e do texto ao passar o mouse.
 */
button[data-baseweb="tab"]:hover {
    background: rgba(178, 151, 107, 0.2) !important;
    color: #E7DBCB !important;
    transform: translateY(-2px) !important;
}

/**
 * Estilo da Aba Selecionada ([aria-selected="true"])
 * A aba ativa ganha um fundo sólido e uma sombra para se destacar.
 */
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #9B643B, #9B643B) !important;
    color: #E7DBCB !important;
    box-shadow: 0 4px 12px rgba(155, 100, 59, 0.3) !important;
}

/* --- ÁREA DE INPUT DE CHAT --- */

/**
 * Estilo da Caixa de Input ([data-testid="stChatInput"])
 * A caixa de texto onde o usuário digita a mensagem é estilizada com
 * bordas grossas e arredondadas e um efeito de vidro fosco.
 */
[data-testid="stChatInput"] {
    background: rgba(246, 239, 221, 0.9) !important;
    border: 3px solid #B2976B !important;
    border-radius: 40px !important;
    box-shadow: 0 4px 12px rgba(178, 151, 107, 0.2) !important;
    backdrop-filter: blur(10px) !important;
}

/**
 * Efeito de Foco no Input
 * Quando o usuário clica na caixa de texto, uma sombra de brilho aparece
 * para indicar que ela está ativa.
 */
[data-testid="stChatInput"]:focus-within {
    box-shadow: 0 0 0 3px rgba(250, 177, 1, 0.2) !important;
}

/**
 * Correção de Borda do Input
 * Este seletor complexo visa um elemento interno do componente de input
 * do Streamlit para garantir que sua borda e fundo fiquem transparentes,
 * evitando que sobreponham o estilo personalizado do contêiner principal.
 */
[data-testid="stChatInput"] [class*="st-emotion-cache"]:not(input):not(textarea) {
    border-color: #B2976B !important;
    background-color: transparent !important;
    border-top-color: #B2976B !important;
    border-bottom-color: #B2976B !important;
}

/* --- ELEMENTOS DIVERSOS --- */
                                
/**
 * Ícones e Labels (.icone-label)
 * Estilo para pequenos ícones ou labels usados na interface.
 */
.icone-label {
    font-size: 1.8rem !important;
    color: #9B643B !important;
    margin-bottom: 0.8rem !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1) !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/**
 * Alertas de Feedback (.stAlert)
 * Estiliza as caixas de alerta (info, warning, error) do Streamlit.
 */
.stAlert {
    background: rgba(178, 151, 107, 0.1) !important;
    border: 1px solid #B2976B !important;
    border-radius: 12px !important;
    color: #2F3A1F !important;
}

/**
 * Animação de Fade-In (@keyframes fadeIn)
 * Define uma animação simples que faz os elementos aparecerem suavemente,
 * movendo-se de baixo para cima e de transparente para opaco.
 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/**
 * Aplicação da Animação
 * Aplica a animação `fadeIn` aos expanders e às mensagens de chat,
 * tornando a interface mais dinâmica.
 */
.stExpander, .mensagem-user, .mensagem-assistente {
    animation: fadeIn 0.5s ease-out !important;
}

/**
 * Indicadores de Status ([data-testid="stStatus"])
 * Estiliza os indicadores de status (ex: "Running...").
 */
[data-testid="stStatus"] {
    background: rgba(102, 111, 67, 0.9) !important;
    border-radius: 12px !important;
    color: #E7DBCB !important;
}

/* --- BARRA DE ROLAGEM (SCROLLBAR) --- */

/**
 * Personalização da Barra de Rolagem (para navegadores WebKit como Chrome, Safari)
 * Define a largura da barra de rolagem.
 */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

/**
 * Trilha da Barra de Rolagem
 * A parte "fixa" da barra de rolagem ganha um fundo semitransparente.
 */
::-webkit-scrollbar-track {
    background: rgba(246, 239, 221, 0.3);
    border-radius: 4px;
}

/**
 * "Polegar" da Barra de Rolagem
 * A parte móvel da barra de rolagem é estilizada com um gradiente.
 */
::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #B2976B, #9B643B);
    border-radius: 4px;
}

/**
 * Efeito Hover no "Polegar"
 * Muda a cor ao passar o mouse para um tom mais vibrante.
 */
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #9B643B, #FAB101);
}

/* --- RESPONSIVIDADE PARA TELAS MENORES --- */

/**
 * Media Query para Telas com Largura Máxima de 768px (Tablets e Celulares)
 * As regras dentro deste bloco só serão aplicadas em telas menores.
 */
@media (max-width: 768px) {
    /* Reduz o espaçamento da sidebar */
    [data-testid="stSidebar"] > div {
        padding: 1rem !important;
    }
    
    /* Aumenta a largura máxima dos balões de chat para ocupar mais espaço */
    .mensagem-user, .mensagem-assistente {
        max-width: 90% !important;
        padding: 0.8rem 1.2rem !important;
    }
    
    /* Reduz o padding e o tamanho da fonte dos botões */
    .stButton > button {
        padding: 0.6rem 1.5rem !important;
        font-size: 0.9rem !important;
    }
}

</style>
""", unsafe_allow_html=True)
