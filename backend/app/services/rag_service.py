from app.agents.rag.retrieval import Retrieval
from app.agents.rag.context_document import ContextDocument
from app.agents.orchestrator import chain_agents

class RAGService:
    
    def __init__(self) -> None:
        
        self.retrieval: Retrieval = Retrieval()
        self.context_document: ContextDocument = ContextDocument()
        
    
    async def send_message_agent(self, query: str, agent_name: str, filter_dict: dict | None = None):
        
        agent_instance = chain_agents[agent_name]
        
        documentos_recuperados = await self.retrieval.search(query=query, filter=filter_dict)
        contexto_formatado = self.context_document.builder(documentos_recuperados)
        
        return await agent_instance.chain.ainvoke({
            "context": contexto_formatado,
            "question": query
        })
        
        