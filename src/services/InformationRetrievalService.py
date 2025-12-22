from src.components.memory.RAGMemory import RAGMemory

class InformationRetrievalService:
    def __init__(self):
        self.rag_memory = RAGMemory()

    def get_information(self, query: str) -> str:
        results = self.rag_memory.query(query)
        return "\n".join(results)
