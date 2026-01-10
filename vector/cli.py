from os import getenv

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

embeddings = OllamaEmbeddings(model="qwen3-embedding", base_url=getenv("Base_URL"))

url = getenv("Qdrant_url")
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

doc = Document(
    page_content="This is a sample document. 1",
    metadata={"source": "sample_source.txt"}
)
vector_store.add_documents([doc])

print("Vector store initialized and sample document added.")

res = vector_store.similarity_search("sample document", k=2)
for r in res:
    print(r.page_content, r.metadata)