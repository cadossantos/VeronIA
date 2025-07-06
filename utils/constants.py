"""Constantes centralizadas para o projeto VeronIA."""

# Configurações padrão de modelos
DEFAULT_PROVIDER = 'Groq'
DEFAULT_MODEL = 'llama-3.3-70b-versatile'

# Configurações de chat
CHAT_MESSAGE_LIMIT = 10
TITLE_TRUNCATE_LENGTH = 30

# Configurações de interface
CHAT_INPUT_PLACEHOLDER = 'Fale com a JibóIA...'
HEADER_TITLE = '🔮 JibóIA - VerônIA'

# Mensagens do sistema
INITIALIZING_MESSAGE = "🚀 **Inicializando JibóIA...** Por favor, aguarde alguns segundos."
WELCOME_MESSAGE = "👋 Olá! Sou a JibóIA. Como posso ajudar?"
USAGE_INSTRUCTIONS = """
**JibóIA está pronta para uso:**
1. ✅ Modelo já carregado automaticamente!
2. ✅ Conversa iniciada automaticamente!
3. 🚀 Comece a conversar agora mesmo!

💡 **Dica:** Use a aba 'Config' para trocar de modelo.
"""

# Configurações de API
API_KEY_TEMPLATE = "{provider}_API_KEY"

# Configurações de banco de dados
DATABASE_PATH = "db/veronia.db"