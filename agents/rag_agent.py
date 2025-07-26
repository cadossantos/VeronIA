

import os
import logging
from dotenv import load_dotenv
from pathlib import Path

from langchain.retrievers import MergerRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import ChatMessageHistory

# Configuração de logging
logger = logging.getLogger(__name__)
load_dotenv()

class RagQueryEngine:
    def __init__(self, llm: BaseChatModel, vector_store_root: str = "db/vector_store", collection_names: list[str] | None = None, embedding_model: str = "text-embedding-3-small", k: int = 5):
        self.llm = llm
        self.vector_store_root = vector_store_root
        self.embedding_model = embedding_model
        self.k = k  # k agora controla o número final de documentos após o re-ranking
        self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
        
        # --- Configuração da Memória ---
        self.memory = ConversationBufferMemory(
            chat_memory=ChatMessageHistory(),
            memory_key="chat_history",
            input_key="question",
            output_key="answer",
            return_messages=True
        )

        # --- Descoberta de Coleções ---
        if collection_names:
            self.collection_names = collection_names
        else:
            self.collection_names = [d.name for d in os.scandir(self.vector_store_root) if d.is_dir()]
            logger.info(f"Nenhuma coleção especificada. Usando todas as coleções encontradas: {self.collection_names}")

        if not self.collection_names:
            raise ValueError("Nenhuma base de conhecimento (coleção ChromaDB) encontrada ou especificada.")

        # --- Configuração do Retriever Base (Busca Ampla) ---
        base_retrievers = []
        for col_name in self.collection_names:
            vector_store_path = os.path.join(self.vector_store_root, col_name)
            if not os.path.exists(vector_store_path):
                logger.warning(f"Diretório da base de conhecimento não encontrado para '{col_name}' em: {vector_store_path}. Pulando.")
                continue
            try:
                vectordb = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=vector_store_path,
                    collection_name=col_name
                )
                # Busca inicial mais ampla (fetch_k) para o re-ranker
                base_retrievers.append(vectordb.as_retriever(search_kwargs={"k": 20}))
                logger.info(f"ChromaDB carregado para coleção '{col_name}'. Contagem de docs: {vectordb._collection.count()}")
            except Exception as e:
                logger.error(f"Erro ao carregar ChromaDB para coleção '{col_name}': {e}")

        if not base_retrievers:
            raise ValueError("Nenhum retriever pôde ser inicializado.")
        
        lotr = MergerRetriever(retrievers=base_retrievers)

        # --- Configuração do Compressor e Re-ranker ---
        compressor = FlashrankRerank(top_n=self.k)
        self.retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=lotr,
            k=self.k # Define o número final de documentos a serem retornados
        )
        logger.info(f"RagQueryEngine inicializado com {len(self.collection_names)} base(s) e re-ranking ativado.")

        # --- Carregamento e Configuração dos Prompts ---
        self._load_prompts()

        # --- Construção da Chain com LCEL (LangChain Expression Language) ---
        self._build_rag_chain()

    def _load_prompts(self):
        try:
            rag_prompt_path = Path(__file__).parent.parent / 'prompts' / 'rag_agent_prompt.txt'
            with open(rag_prompt_path, 'r', encoding='utf-8') as f:
                _template = f.read()
            logger.info("Prompt personalizado carregado com sucesso.")
        except FileNotFoundError:
            logger.warning(f"Arquivo de prompt não encontrado. Usando prompt padrão.")
            _template = """Você é um assistente RAG especializado em documentação técnica do SmartSimple.

Contexto dos documentos:
{context}

Pergunta do usuário: {question}

Resposta baseada no contexto fornecido:"""

        self.qa_prompt = PromptTemplate(template=_template, input_variables=["context", "question"])
        
        self.condense_question_prompt = PromptTemplate.from_template(
            """Dado o seguinte histórico de conversa e uma pergunta de acompanhamento, reformule a pergunta de acompanhamento para ser uma pergunta independente, mantendo todo o contexto necessário.

Histórico do Chat:
{chat_history}
Pergunta de Acompanhamento: {question}
Pergunta independente:"""
        )

    def _build_rag_chain(self):
        # Chain para gerar a pergunta independente
        standalone_question_chain = RunnableParallel(
            question=RunnablePassthrough()
        ) | {
            "chat_history": lambda x: self._format_chat_history(self.memory.load_memory_variables({})['chat_history']),
            "question": lambda x: x['question']
        } | self.condense_question_prompt | self.llm | StrOutputParser()

        # Chain principal do RAG
        rag_chain = RunnableParallel(
            context=(standalone_question_chain | self.retriever | self._combine_documents),
            question=RunnablePassthrough()
        ) | self.qa_prompt | self.llm | StrOutputParser()
        
        self.chain = rag_chain

    def _format_chat_history(self, messages):
        if not messages:
            return ""
        return "\n".join([f"Humano: {msg.content}" if isinstance(msg, HumanMessage) else f"Assistente: {msg.content}" for msg in messages])

    def _combine_documents(self, docs):
        if not docs:
            return "Nenhum documento relevante encontrado no SmartSimple Wiki."
        
        # Log para depuração
        logger.info(f"Documentos recuperados e re-rankeados: {[doc.metadata.get('title', 'N/A') for doc in docs]}")
        for doc in docs:
            logger.info(f"Doc: {doc.metadata.get('source', 'Unknown')} | Preview: {doc.page_content[:200]}...")

        return "\n\n".join([f"DOCUMENTO {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

    def query(self, pergunta: str):
        try:
            # Carrega o histórico da memória
            inputs = self.memory.load_memory_variables({})
            chat_history = inputs.get('chat_history', [])

            # Determina a pergunta a ser usada (original ou condensada)
            if chat_history:
                standalone_question = (self.condense_question_prompt | self.llm | StrOutputParser()).invoke({
                    "chat_history": self._format_chat_history(chat_history),
                    "question": pergunta
                })
                logger.info(f"Pergunta independente gerada: {standalone_question}")
            else:
                standalone_question = pergunta

            # Recupera documentos relevantes com base na pergunta (condensada ou não)
            retrieved_docs = self.retriever.invoke(standalone_question)
            
            # Combina os documentos em um contexto
            context = self._combine_documents(retrieved_docs)

            # Gera a resposta
            answer = (self.qa_prompt | self.llm | StrOutputParser()).invoke({
                "context": context,
                "question": standalone_question
            })

            # Salva a interação na memória
            self.memory.save_context({"question": pergunta}, {"answer": answer})
            
            logger.info("Resposta gerada com sucesso")
            return answer, retrieved_docs

        except Exception as e:
            logger.error(f"Erro durante a consulta: {str(e)}", exc_info=True)
            raise

    def clear_memory(self):
        self.memory.clear()
        logger.info("Memória da conversa limpa")
