class RetrievalArgumentGeneration:
    
    def embedding_query(self, query: str):
        ...
        
    
    def vectory_search(self, query_embedding, vector_store):
        ...
        
        
    def hybrid_serach(self, query_embedding, vector_store):
        ...
        
        
    def re_rank(self, result_vector_search):
        ...
        
    
    def metadata_filter(self, documents, query):
        ...
        
    
    def namespace_filter(self):
        ...
        
    
    def format_context(self, documents):
        ...
        
    
    def compress_context(self, documents, query):
        ...