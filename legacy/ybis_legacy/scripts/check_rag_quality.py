from src.agentic.tools.local_rag import LocalRAG
rag = LocalRAG()
print("Searching for: 'Implement Weather Stats Utility'")
results = rag.search("Implement Weather Stats Utility", limit=3)
print(f"Results:\n{results}")
