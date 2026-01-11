from os import getenv

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

embeddings = OllamaEmbeddings(model="qwen3-embedding", base_url=getenv("BASE_URL"))

url = getenv("QRANT_URL")
docs = [
]
qdrant = QdrantVectorStore.from_documents(
    docs,
    embeddings,
    url=url,
    prefer_grpc=True,
    collection_name="AgentRagCollection",
)

vector_store = qdrant