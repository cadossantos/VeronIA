import os
import json
import uuid
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

# Carrega variáveis do .env
load_dotenv()

DATA_DIR = "/home/claudiodossantos/dev/projetos/minimo/data/pages"
VECTOR_STORE_DIR = "/home/claudiodossantos/dev/projetos/minimo/data/vector_store"
COLLECTION_NAME = "smartwiki_docs"
EMBEDDING_MODEL = "text-embedding-3-small"

def load_documents():
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                docs.append(Document(
                    page_content=data["content"],
                    metadata={
                        "title": data["title"],
                        "url": data["url"]
                    }
                ))
    return docs

def chunk_documents(documents, chunk_size=400, overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_documents(documents)

def ingest():
    print("📥 Carregando documentos...")
    documents = load_documents()
    print(f"🔍 Total de documentos: {len(documents)}")

    print("✂️ Gerando chunks...")
    chunks = chunk_documents(documents)
    print(f"📦 Total de chunks: {len(chunks)}")

    print("🔗 Conectando ao ChromaDB via LangChain...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_DIR,
        collection_name=COLLECTION_NAME
    )

    vectordb.persist()
    print("✅ Ingestão e persistência concluídas!")

if __name__ == "__main__":
    ingest()
