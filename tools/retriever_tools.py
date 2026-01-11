from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

from vector.cli import embeddings, vector_store


@tool
def semantic_search(query: str, top_k: int = 5) -> list[Document]:
    """
        Retrieve documents similar to the query using semantic search.
        Args:
            query (str): The search query.
            top_k (int): The number of top similar documents to retrieve.
        
        Returns:
            list[Document]: A list of similar documents.
    """
    try:
        results = vector_store.similarity_search(query, k=top_k)
        return results
    except Exception as e:
        return [Document(page_content=f"Error during semantic search: {str(e)}")]