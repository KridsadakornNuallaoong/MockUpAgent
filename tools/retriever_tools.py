from typing import Any

from langchain.tools import tool
from langchain_core.documents import Document
from pydantic import BaseModel, ConfigDict
from qdrant_client.models import FieldCondition, Filter, MatchValue

from vector.cli import vector_store


class filter_type(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    key: str
    value: Any

filter = filter_type(key="metadata.page", value=1)

@tool(
    "semantic_search",
    description="""
        Retrieve documents similar to the query using semantic search.
        Args:
            query (str): The search query.
            top_k (int): The number of top similar documents to retrieve. you need to specify top_k.
            filter (filter_type, optional): An optional filter to narrow down the search results.

            filter_type is a Pydantic model with the following structure:
            class filter_type(BaseModel):
                key: str
                value: any

            example filter:
            'filter': {'key': 'metadata.page', 'value': 1} or 
            'filter': {'key': 'metadata.source', 'value': 'example.pdf'}
        
        Returns:
            list[Document]: A list of similar documents.
    """,
    # return_direct=True,
)
def semantic_search(query: str, top_k: int = 5, filter: filter_type = None) -> list[Document]:
    """
        Retrieve documents similar to the query using semantic search.
        Args:
            query (str): The search query.
            top_k (int): The number of top similar documents to retrieve.
            filter (filter_type, optional): An optional filter to narrow down the search results.

            filter_type is a Pydantic model with the following structure:
            class filter_type(BaseModel):
                key: str
                value: any

            example filter:
            'filter': {'key': 'metadata.page', 'value': 1} or 
            'filter': {'key': 'metadata.source', 'value': 'example.pdf'}
        
        Returns:
            list[Document]: A list of similar documents.
    """
    try:
        results = vector_store.similarity_search(
            query, k=top_k, filter=Filter(must=[FieldCondition(key=filter.key, match=MatchValue(value=filter.value))]) if filter is not None else None)
        
        return results
    except Exception as e:
        return [Document(page_content=f"Error during semantic search: {str(e)}")]