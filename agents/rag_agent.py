import os
from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate

# (Opcional: confirmar versão do LangChain)
from langchain import __version__ as langchain_version
print(f"LangChain v{langchain_version}")

# 1. Carregar variáveis de ambiente
load_dotenv()

# 2. Constantes
VECTOR_STORE_DIR = "db/vector_store"
COLLECTION_NAME = "smartwiki_docs"
EMBEDDING_MODEL = "text-embedding-3-small"

class RagQueryEngine:
    def __init__(self, vector_store_dir, collection_name, embedding_model):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectordb = Chroma(
            embedding_function=self.embeddings,
            persist_directory=vector_store_dir,
            collection_name=collection_name
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.llm = OpenAI(temperature=0.0)
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": 5})

        _template = """
        DEBUG CONTEXT: {context} 
        Use o seguinte contexto para responder à pergunta no final. Se você não souber a resposta,
        apenas diga que não sabe, não tente inventar uma resposta.

        {context}

        Pergunta: {question}
        Resposta útil:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(_template)

        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
            """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Question: {question}
Standalone question:"""
        )

        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            output_key="answer",
            condense_question_prompt=CONDENSE_QUESTION_PROMPT,
            combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

    def query(self, pergunta: str):
        # Get the standalone question from the chat history
        standalone_question = self.qa_chain.question_generator.invoke({"chat_history": self.memory.buffer_as_messages, "question": pergunta})["text"]
        print(f"Pergunta autônoma gerada: {standalone_question}")

        # Retrieve documents based on the standalone question
        retrieved_docs = self.retriever.get_relevant_documents(standalone_question)
        print(f"Documentos recuperados pelo retriever: {[doc.metadata.get('title', 'N/A') for doc in retrieved_docs]}")

        # Pass the retrieved documents and the original question to the combine_docs_chain
        resultado = self.qa_chain.combine_docs_chain.invoke({"input_documents": retrieved_docs, "question": pergunta})
        resposta = resultado["output_text"]
        fontes = retrieved_docs # The source documents are the ones retrieved by the retriever
        print(f"Documentos de origem recuperados: {[doc.metadata.get('title', 'N/A') for doc in fontes]}")
        return resposta, fontes

# 6. Função principal de consulta
def perguntar_ao_agent(pergunta: str):
    # 1. Carregar variáveis de ambiente
    load_dotenv()

    # 2. Constantes
    VECTOR_STORE_DIR = "db/vector_store"
    COLLECTION_NAME = "smartwiki_docs"
    EMBEDDING_MODEL = "text-embedding-3-small"

    engine = RagQueryEngine(VECTOR_STORE_DIR, COLLECTION_NAME, EMBEDDING_MODEL)
    return engine.query(pergunta)
