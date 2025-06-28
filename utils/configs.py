"""Módulo de Configuração Central para Modelos de Linguagem.

Este arquivo serve como um "cardápio" de modelos de linguagem (LLMs)
disponíveis para a aplicação VeronIA. Ele centraliza as configurações,
facilitando a adição, remoção ou modificação de provedores e modelos sem
a necessidade de alterar a lógica principal da aplicação.

Atributos:
    config_modelos (dict): Um dicionário que mapeia nomes de provedores
        (ex: 'OpenAI', 'Groq') para suas respectivas configurações. Cada
        configuração é um dicionário contendo:
        - 'modelos' (list[str]): Uma lista de identificadores de modelos
          específicos oferecidos por aquele provedor.
        - 'chat' (class): A referência à classe do LangChain (ex: ChatOpenAI)
          responsável por interagir com a API daquele provedor.
"""

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama


arquivos_validos = ['Site', 'YouTube', 'PDF', 'CSV', 'TXT']
tipo_arquivo = None
documento = None

config_modelos = {
    'Ollama':{
        'modelos': ['llama3.1:8b', 'mistral:7b-instruct', 'qwen3:8b', 'hermes3:8b', 'codellama:7b-instruct', 'deepseek-coder:6.7b-instruct'],
        'chat': ChatOllama
    },
    'Groq': {
        'modelos':['llama-3.3-70b-versatile', 'gemma2-9b-it', 'llama-3.1-8b-instant'],
        'chat': ChatGroq
    },
    'OpenAI': {
        'modelos': ['gpt-4o-mini', 'gpt-4o', 'o1-mini'],
        'chat': ChatOpenAI
    }
}
