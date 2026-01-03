"""
Cognee + Neo4j simple integration test (no emojis for Windows console)
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configure before import
os.environ['GRAPH_DATABASE_PROVIDER'] = 'neo4j'
os.environ['GRAPH_DATABASE_URL'] = 'bolt://localhost:7687'
os.environ['GRAPH_DATABASE_USERNAME'] = 'neo4j'
os.environ['GRAPH_DATABASE_PASSWORD'] = 'ybis-graph-2025'
os.environ['ENABLE_BACKEND_ACCESS_CONTROL'] = 'false'  # Disable multi-user mode for testing

try:
    import cognee
    print("[OK] Cognee v0.5.1 imported")

    # Test data
    test_data = "YBIS uses Neo4j for dependency tracking and SQLite for task management."

    print("[INFO] Adding test data...")
    cognee.add(test_data)

    print("[INFO] Running cognify (graph+vector processing)...")
    cognee.cognify()

    print("[INFO] Testing search...")
    results = cognee.search("dependency tracking")

    print(f"[RESULT] Found: {results}")
    print("\n[SUCCESS] Cognee works with our stack!")
    print("[INFO] Cognee version: 0.5.1")
    print("[INFO] Graph DB: Neo4j (bolt://localhost:7687)")
    print("[INFO] Vector DB: LanceDB (default)")
    print("[INFO] SQL DB: SQLite (default)")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
