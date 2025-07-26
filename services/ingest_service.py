import os
import json
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

# Carrega variáveis do .env
load_dotenv()

def load_documents(data_dir):
    docs = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                docs.append(Document(
                    page_content=data["content"],
                    metadata={
                        "title": data["title"],
                        "url": data["url"],
                        "source": filepath  # Adicionando a fonte
                    }
                ))
    return docs

def chunk_documents(documents, chunk_size=1000, overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", "|", " ", ""]
    )
    return splitter.split_documents(documents)

def ingest(data_dir, vector_store_dir, collection_name, chunk_size, overlap, embedding_model="text-embedding-3-small"):
    print(f"📥 Carregando documentos de: {data_dir}...")
    documents = load_documents(data_dir)
    print(f"🔍 Total de documentos carregados: {len(documents)}")
    if not documents:
        print("⚠️ Nenhum documento encontrado para ingestão. Pulando criação do vetor store.")
        return 0, 0

    print("✂️ Gerando chunks...")
    chunks = chunk_documents(documents, chunk_size=chunk_size, overlap=overlap)
    print(f"📦 Total de chunks gerados: {len(chunks)}")
    if not chunks:
        print("⚠️ Nenhum chunk gerado. Pulando criação do vetor store.")
        return len(documents), 0

    print(f"🔗 Conectando ao ChromaDB em {vector_store_dir} para a coleção {collection_name}...")
    embeddings = OpenAIEmbeddings(model=embedding_model)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=vector_store_dir,
        collection_name=collection_name
    )

    
    print("✅ Ingestão e persistência concluídas!")
    print(f"✅ Verificando diretório: {os.path.exists(vector_store_dir)}")
    if os.path.exists(vector_store_dir):
        print(f"✅ Conteúdo do diretório: {os.listdir(vector_store_dir)}")
    return len(documents), len(chunks)


