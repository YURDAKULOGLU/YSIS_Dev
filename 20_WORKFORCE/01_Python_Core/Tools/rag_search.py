import os
from supabase import create_client, Client
from langchain_ollama import OllamaEmbeddings

class RAGSearchTool:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print("[WARNING] Warning: SUPABASE credentials missing. RAG disabled.")
            self.client = None
        else:
            self.client: Client = create_client(url, key)
            
        # Embedding model for query vectorization
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

    def search(self, query: str, limit: int = 5):
        if not self.client:
            return "RAG Unavailable (Missing Credentials)"
            
        try:
            # 1. Vectorize query
            query_vector = self.embeddings.embed_query(query)
            
            # 2. Call Supabase RPC function (defined in migration 009)
            response = self.client.rpc(
                "search_chunks",
                {
                    "query_embedding": query_vector,
                    "match_count": limit,
                    "filter_workspace_id": None # Global search for now
                }
            ).execute()
            
            # 3. Format results
            return self._format_results(response.data)
            
        except Exception as e:
            return f"RAG Search Error: {str(e)}"

    def _format_results(self, data):
        if not data:
            return "No relevant documents found."
            
        formatted = "Found following relevant context:\n"
        for item in data:
            formatted += f"- ...{item.get('content', '')[:200]}... (Similarity: {item.get('similarity', 0):.2f})\n"
        return formatted

# Singleton
rag_tool = RAGSearchTool()
