"""Constantes centralizadas para o projeto VeronIA."""

# Configurações padrão de modelos
DEFAULT_PROVIDER = 'Groq'
DEFAULT_MODEL = 'llama-3.3-70b-versatile'

# Configurações de chat
CHAT_MESSAGE_LIMIT = 10
TITLE_TRUNCATE_LENGTH = 30

# Configurações de interface
CHAT_INPUT_PLACEHOLDER = 'Fale com a JibóIA...'
HEADER_TITLE = '🔮 JibóIA'

# Mensagens do sistema
INITIALIZING_MESSAGE = "🚀 **Inicializando JibóIA...** Por favor, aguarde alguns segundos."
WELCOME_MESSAGE = "👋 Olá! Sou a JibóIA. Como posso ajudar?"
USAGE_INSTRUCTIONS = """

⚙️ **Configurações Avançadas**
Você pode ajustar as respostas da JibóIA conforme sua necessidade:

🔥 Temperatura (0.0 a 1.0):
Define o nível de criatividade das respostas.

Mais baixa (ex: 0.2): Respostas mais diretas e objetivas.

Mais alta (ex: 0.8): Respostas mais criativas e diversas.
Valor atual: 0.70 (bom equilíbrio entre coerência e criatividade).

🧮 Máximo de tokens (100 a 4000):
Controla o tamanho da resposta da IA.

Menor valor: Respostas mais curtas.

Maior valor: Respostas mais longas e detalhadas.
Valor atual: 1000 tokens (aproximadamente 750 palavras).

💡 **Dica:** Use a aba 'Config' para trocar de modelo.
"""

# Configurações de API
API_KEY_TEMPLATE = "{provider}_API_KEY"

# Configurações de banco de dados
DATABASE_PATH = "db/veronia.db"