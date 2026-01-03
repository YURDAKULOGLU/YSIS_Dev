"""
Cognee + Neo4j async test
"""
import os
import asyncio

# Configure before import
os.environ['GRAPH_DATABASE_PROVIDER'] = 'neo4j'
os.environ['GRAPH_DATABASE_URL'] = 'bolt://localhost:7687'
os.environ['GRAPH_DATABASE_USERNAME'] = 'neo4j'
os.environ['GRAPH_DATABASE_PASSWORD'] = 'ybis-graph-2025'
os.environ['ENABLE_BACKEND_ACCESS_CONTROL'] = 'false'

async def test_cognee():
    try:
        import cognee
        print("[OK] Cognee v0.5.1 imported")

        # Reset any previous state
        await cognee.prune.prune_data()
        await cognee.prune.prune_system()

        print("[INFO] System cleaned")

        # Test data
        test_data = "YBIS uses Neo4j for dependency tracking and SQLite for task management."

        print("[INFO] Adding test data...")
        await cognee.add(test_data)

        print("[INFO] Running cognify (graph+vector processing)...")
        await cognee.cognify()

        print("[INFO] Testing search...")
        results = await cognee.search("What database does YBIS use for dependencies?")

        print(f"[RESULT] {results}")
        print("\n[SUCCESS] Cognee works!")
        print("[CONFIG]")
        print("  - Graph DB: Neo4j (bolt://localhost:7687)")
        print("  - Vector DB: LanceDB (default)")
        print("  - SQL DB: SQLite (default)")
        print("  - Version: 0.5.1")

        return True

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_cognee())
    exit(0 if success else 1)
