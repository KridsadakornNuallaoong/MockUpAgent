from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

embeddings = OllamaEmbeddings()

client = QdrantClient(
    url="http://localhost:6333",
)

client.create_collection(
    collection_name="helloworld",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="helloworld",
    embedding=embeddings,
)

retriever = vector_store.as_retriever()