import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import FieldCondition, MatchValue, Filter, Condition

from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = str(os.getenv("GOOGLE_API_KEY"))

class Retrieval:
    
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

        self.async_client = AsyncQdrantClient(
            url=str(os.getenv("QDRANT_URL")),
            api_key=str(os.getenv("QDRANT_API_KEY"))
        )
        
        self.vectorstore = QdrantVectorStore.from_existing_collection(
            embedding=self.embedding_model,
            collection_name=str(os.getenv("QDRANT_COLLECTION_NAME")),
            url=str(os.getenv("QDRANT_URL")),
            api_key=str(os.getenv("QDRANT_API_KEY")),
        )
        
        
    async def search(
        self, 
        query,
        filter: dict | None = None,
        top_k: int = 10
    ):
        """Função responsável por realizar a busca vetorial"""
        
        qdrant_filter = None
        if filter:
            conditionals: list[Condition] = [
                FieldCondition(key=f"metadata.{k}", match=MatchValue(value=v))
                for k, v in filter.items()
            ]
            
            qdrant_filter = Filter(must=conditionals)
        
        return await self.vectorstore.asearch(
            query=query,
            k=top_k,
            filter=qdrant_filter,
            search_type="mmr"
        )
        
        