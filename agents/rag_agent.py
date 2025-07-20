import os
import logging
from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Configuração de logging
logger = logging.getLogger(__name__)
load_dotenv()

class RagQueryEngine:
    def __init__(self, vector_store_path: str, collection_name: str, embedding_model: str = "text-embedding-3-small"):
        if not os.path.exists(vector_store_path):
            raise FileNotFoundError(f"Diretório da base de conhecimento não encontrado em: {vector_store_path}")

        self.vector_store_path = vector_store_path
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        logger.info(f"RagQueryEngine inicializado para base: {self.collection_name}, caminho: {self.vector_store_path}, modelo de embedding: {self.embedding_model}")

        self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
        self.vectordb = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.vector_store_path,
            collection_name=self.collection_name
        )
        logger.info(f"ChromaDB carregado. Contagem de documentos na coleção '{self.collection_name}': {self.vectordb._collection.count()}")
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.llm = OpenAI(temperature=0.0)
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": 5})

        # Carregar o prompt personalizado
        from pathlib import Path
        rag_prompt_path = Path(__file__).parent.parent / 'prompts' / 'rag_agent_prompt.txt'
        
        try:
            with open(rag_prompt_path, 'r', encoding='utf-8') as f:
                _template = f.read()
            logger.info("Prompt personalizado carregado com sucesso")
        except FileNotFoundError:
            # Fallback para um prompt padrão caso o arquivo não seja encontrado
            logger.warning(f"Arquivo de prompt não encontrado em {rag_prompt_path}. Usando prompt padrão.")
            _template = """Você é um assistente RAG especializado em documentação técnica do SmartSimple.

Contexto dos documentos:
{context}

Pergunta do usuário: {question}

Resposta baseada no contexto fornecido:"""
        
        # Criar o prompt principal - seu prompt usa {context} e {question}
        self.qa_prompt = PromptTemplate(
            template=_template,
            input_variables=["context", "question"]
        )

        # Prompt para condensar a pergunta do histórico
        self.condense_question_prompt = PromptTemplate.from_template(
            """Dado o seguinte histórico de conversa e uma pergunta de acompanhamento, reformule a pergunta de acompanhamento para ser uma pergunta independente, mantendo todo o contexto necessário.

Histórico do Chat:
{chat_history}
Pergunta de Acompanhamento: {question}
Pergunta independente:"""
        )

        # Criar as chains
        self.qa_chain = LLMChain(llm=self.llm, prompt=self.qa_prompt)
        self.condense_chain = LLMChain(llm=self.llm, prompt=self.condense_question_prompt)

    def _format_chat_history(self, messages):
        """Formatar o histórico do chat para string"""
        if not messages:
            return ""
        
        formatted = []
        for message in messages:
            if isinstance(message, HumanMessage):
                formatted.append(f"Humano: {message.content}")
            elif isinstance(message, AIMessage):
                formatted.append(f"Assistente: {message.content}")
        
        return "\n".join(formatted)

    def _combine_documents(self, docs):
        """Combinar documentos em uma string de contexto formatada para SmartSimple Wiki"""
        if not docs:
            return "Nenhum documento relevante encontrado no SmartSimple Wiki."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            # Incluir metadados do SmartSimple Wiki
            title = doc.metadata.get('title', f'Página do Wiki {i}')
            source = doc.metadata.get('source', 'SmartSimple Wiki')
            url = doc.metadata.get('url', 'https://wiki.smartsimple.com/')
            
            context_part = f"=== {title} ===\n"
            context_part += f"URL: {url}\n"
            context_part += f"Conteúdo:\n{doc.page_content}\n"
            context_parts.append(context_part)
        
        return "\n\n".join(context_parts)

    def query(self, pergunta: str):
        """Consultar o sistema RAG com uma pergunta"""
        try:
            # 1. Obter o histórico da memória
            chat_history = self.memory.buffer_as_messages
            
            # 2. Se há histórico, condensar a pergunta
            if chat_history:
                chat_history_str = self._format_chat_history(chat_history)
                standalone_question_result = self.condense_chain.invoke({
                    "chat_history": chat_history_str,
                    "question": pergunta
                })
                standalone_question = standalone_question_result["text"].strip()
                logger.info(f"Pergunta independente gerada: {standalone_question}")
            else:
                standalone_question = pergunta

            # 3. Recuperar documentos relevantes
            retrieved_docs = self.retriever.get_relevant_documents(standalone_question)
            logger.info(f"Documentos recuperados: {[doc.metadata.get('title', 'N/A') for doc in retrieved_docs]}")
            
            # 4. Combinar documentos em contexto
            context = self._combine_documents(retrieved_docs)
            
            # 5. Gerar resposta usando o prompt personalizado
            response_result = self.qa_chain.invoke({
                "context": context,
                "question": pergunta  # Usar pergunta original, não a condensada
            })
            
            resposta = response_result["text"].strip()
            
            # 6. Salvar na memória
            self.memory.save_context(
                {"input": pergunta},
                {"output": resposta}
            )
            
            logger.info(f"Resposta gerada com sucesso")
            return resposta, retrieved_docs
            
        except Exception as e:
            logger.error(f"Erro durante a consulta: {str(e)}")
            raise

    def clear_memory(self):
        """Limpar a memória da conversa"""
        self.memory.clear()
        logger.info("Memória da conversa limpa")