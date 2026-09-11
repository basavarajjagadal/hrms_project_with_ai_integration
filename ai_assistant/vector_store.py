

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from .schema_extractor import extract_schema_documents
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# Path to store Chroma DB
PERSIST_DIR = "chroma_db"

# Optional: configure chunking
# CHUNK_SIZE = 500        # tokens/characters per chunk
# CHUNK_OVERLAP = 50      # overlap between chunks

def create_vector_store():
    """
    Create and persist vector database from schema documents
    Uses HuggingFaceEmbeddings (local, free)
    """
    # Step 1: Extract schema documents
    documents = extract_schema_documents()

    # Step 2: Split long documents into chunks
    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=CHUNK_SIZE,
    #     chunk_overlap=CHUNK_OVERLAP
    # )

    # chunked_docs = []
    # for doc in documents:
    #     splits = splitter.split_text(doc.page_content)
    #     for i, chunk in enumerate(splits):
    #         chunked_docs.append(
    #             doc.__class__(
    #                 page_content=chunk,
    #                 metadata={
    #                     **doc.metadata,       # keep original metadata (table, type)
    #                     "chunk_index": i      # optional: track chunk order
    #                 }
    #             )
    #         )

    # Step 3: Initialize embeddings (local, free)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Step 4: Create Chroma vector store
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    print(f" Vector DB created and saved to '{PERSIST_DIR}'")
    return vectordb


def load_vector_store():
    """ 
    Load existing vector database
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )
    return vectordb


