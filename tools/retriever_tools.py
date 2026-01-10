from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from vector.cli import embeddings, vector_store


@tool
def retrieve_similar_documents(query: str, k: int = 5) -> list[Document]:
    """Retrieve similar documents from the vector store."""
    results = vector_store.similarity_search(query, k=k)
    return results

@tool
def add_document_to_vector_store(page_content: str, source: str) -> str:
    """Add a new document to the vector store."""
    doc = Document(
        page_content=page_content,
        metadata={"source": source}
    )
    vector_store.add_documents([doc])
    return f"Document from {source} added to vector store."

@tool
def get_embedding(text: str) -> list[float]:
    """Get the embedding vector for the given text."""
    embedding_vector = embeddings.embed_query(text)
    return embedding_vector