from langchain_core.documents import Document

from app.agents.rag.retrieval import Retrieval
from app.agents.rag.context_document import ContextDocument


class RAGService:
    """
    Responsável por duas operações no Qdrant:
    - search: recupera contexto relevante para o agente (RAG)
    - index:  armazena novos turnos de conversa para RAG futuro
    
    NÃO é responsável por invocar agentes — isso é papel do BoardService.
    """

    def __init__(self) -> None:
        self.retrieval: Retrieval = Retrieval()
        self.context_document: ContextDocument = ContextDocument()

    async def search(
        self,
        query: str,
        filter: dict | None = None,
        top_k: int = 5,
    ):
        """
        Busca documentos relevantes no Qdrant por similaridade semântica.
        Retorna lista de Document (LangChain) com page_content e metadata.
        """
        return await self.retrieval.search(
            query=query,
            filter=filter,
            top_k=top_k,
        )

    async def index(self, text: str, metadata: dict) -> None:
        """
        Indexa um chunk de texto no Qdrant.
        Chamado pelo BoardService ao final de cada turno de conversa.
        """
        doc = Document(page_content=text, metadata=metadata)
        await self.retrieval.vectorstore.aadd_documents([doc])