from src.modules.memory.RAGMemory import RAGMemory

class IntegrationService:
    def __init__(self):
        self.rag_memory = RAGMemory()

    def retrieve_data(self, query: str) -> str:
        # RAG memory sisteminden bilgi al
        return self.rag_memory.retrieve_information(query)
