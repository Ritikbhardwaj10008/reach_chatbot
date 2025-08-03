from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from config import settings

client = QdrantClient(url=settings.QDRANT_HOST, api_key=settings.QDRANT_API_KEY)
embedding = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

vectorstore = QdrantVectorStore(
    client=client,
    collection_name=settings.COLLECTION_NAME,
    embedding=embedding
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})