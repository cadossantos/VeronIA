import os
import json
import argparse
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

# Carrega variáveis do .env
load_dotenv()

VECTOR_STORE_DIR = "/home/claudiodossantos/dev/projetos/minimo/data/vector_store"
COLLECTION_NAME = "smartwiki_docs"
EMBEDDING_MODEL = "text-embedding-3-small"

def load_document_from_file(filepath):
    """Carrega um único documento de um arquivo JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Document(
            page_content=data["content"],
            metadata={
                "title": data.get("title", "Documento Carregado"),
                "url": data.get("url", "")
            }
        )]

def chunk_documents(documents, chunk_size=400, overlap=50):
    """Divide os documentos em chunks menores."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    return splitter.split_documents(documents)

def ingest(filepath):
    """Processa e ingere um único arquivo na base de conhecimento."""
    print(f"📥 Carregando documento de {filepath}...")
    documents = load_document_from_file(filepath)
    
    print("✂️ Gerando chunks...")
    chunks = chunk_documents(documents)
    print(f"📦 Total de chunks: {len(chunks)}")

    print("🔗 Conectando ao ChromaDB via LangChain...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    # Conecta ao ChromaDB existente ou cria um novo
    vectordb = Chroma(
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )
    
    # Adiciona os novos documentos
    vectordb.add_documents(chunks)
    
    vectordb.persist()
    print("✅ Ingestão e persistência concluídas!")

def main():
    parser = argparse.ArgumentParser(description="Ingere um documento para o RAG.")
    parser.add_argument("filepath", type=str, help="O caminho para o arquivo JSON a ser ingerido.")
    args = parser.parse_args()
    
    ingest(args.filepath)

if __name__ == "__main__":
    main()