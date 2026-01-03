"""
Quick test: Cognee + Neo4j integration
Test if Cognee can connect to our existing Neo4j instance
"""
import os
import cognee

# Configure Cognee to use our Neo4j instance
os.environ['GRAPH_DATABASE_PROVIDER'] = 'neo4j'
os.environ['GRAPH_DATABASE_URL'] = 'bolt://localhost:7687'
os.environ['GRAPH_DATABASE_USERNAME'] = 'neo4j'
os.environ['GRAPH_DATABASE_PASSWORD'] = 'ybis-graph-2025'

try:
    # Test basic configuration
    print("✅ Cognee imported")

    # Try to add simple data
    test_data = "YBIS is a self-propagating AI development system with Neo4j graph database for dependency tracking."

    print("📝 Adding test data...")
    cognee.add(test_data)

    print("🧠 Running cognify (processing into graph+vector)...")
    cognee.cognify()

    print("🔍 Testing search...")
    results = cognee.search("What is YBIS?")

    print(f"✅ Search results: {results}")
    print("\n✅ SUCCESS: Cognee works with Neo4j!")

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
