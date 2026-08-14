from langchain_core.documents import Document


class ContextDocument:
    
    def builder(self, documents: list[Document]) -> str:
        return "\n---\n".join([
        f"Fonte: {doc.metadata.get('fonte')} | Remetente: {doc.metadata.get('sender')} | Data: {doc.metadata.get('date')}\n"
        f"Conteúdo: {doc.page_content}" # Em LangChain Document, o texto fica em page_content
        for doc in documents
    ])
