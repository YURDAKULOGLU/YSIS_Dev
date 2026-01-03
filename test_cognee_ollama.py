"""
Cognee + Neo4j + Ollama integration test
"""
import os
import asyncio

# Configure Cognee to use Ollama (local LLM)
os.environ['LLM_PROVIDER'] = 'ollama'
os.environ['LLM_MODEL'] = 'llama3.1:latest'
os.environ['LLM_API_BASE'] = 'http://localhost:11434'

# Neo4j configuration
os.environ['GRAPH_DATABASE_PROVIDER'] = 'neo4j'
os.environ['GRAPH_DATABASE_URL'] = 'bolt://localhost:7687'
os.environ['GRAPH_DATABASE_USERNAME'] = 'neo4j'
os.environ['GRAPH_DATABASE_PASSWORD'] = 'ybis-graph-2025'

# Disable multi-user mode for testing
os.environ['ENABLE_BACKEND_ACCESS_CONTROL'] = 'false'

async def test_cognee():
    try:
        import cognee
        print("[OK] Cognee v0.5.1 imported")
        print("[CONFIG] LLM: Ollama (llama3.1:latest at localhost:11434)")
        print("[CONFIG] Graph DB: Neo4j (bolt://localhost:7687)")

        # Reset state
        await cognee.prune.prune_data()
        print("[INFO] Data cleaned")

        # Test data
        test_data = """
        YBIS is a self-propagating AI development system.
        It uses Neo4j for dependency tracking.
        It uses SQLite for task management.
        Agents communicate via MCP messaging tools.
        """

        print("[INFO] Adding test data...")
        await cognee.add(test_data)

        print("[INFO] Running cognify (graph+vector processing)...")
        await cognee.cognify()

        print("[INFO] Testing search...")
        results = await cognee.search("What databases does YBIS use?")

        print(f"\n[RESULTS]")
        print(results)

        print("\n[SUCCESS] Cognee + Neo4j + Ollama integration works!")
        return True

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print(" Cognee Integration Test with YBIS Stack")
    print("="*60)
    success = asyncio.run(test_cognee())
    print("="*60)
    exit(0 if success else 1)
