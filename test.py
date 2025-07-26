# Teste importações diretas dos submódulos
test_imports = [
    "from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank",
    "from langchain_community.document_compressors.cohere_rerank import CohereRerank", 
    "from langchain_community.document_compressors.llm_lingua import LLMLinguaCompressor",
    "from langchain_community.document_compressors.sentence_transformer_rerank import SentenceTransformersRerank",
    "from langchain.retrievers.document_compressors import LLMChainExtractor",
    "from langchain.retrievers.document_compressors import LLMChainFilter",
    "from langchain.retrievers.document_compressors import EmbeddingsFilter"
]

for imp in test_imports:
    try:
        exec(imp)
        print(f"✓ {imp}")
    except ImportError as e:
        print(f"✗ {imp} - {str(e)}")