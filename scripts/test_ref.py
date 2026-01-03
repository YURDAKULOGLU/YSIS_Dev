"""Test REFERENCES relationship creation"""
import sys
sys.path.insert(0, 'src')
from agentic.infrastructure.graph_db import GraphDB

db = GraphDB()

# Check existing nodes
with db.driver.session() as session:
    # Check if DocFile exists
    result = session.run("MATCH (d:DocFile) RETURN d.path LIMIT 3")
    print("Sample DocFiles:")
    for r in result:
        print(f"  {r['d.path']}")
    
    # Check if CodeFile exists
    result = session.run("MATCH (c:CodeFile) RETURN c.path LIMIT 3")
    print("\nSample CodeFiles:")
    for r in result:
        print(f"  {r['c.path']}")

# Test creating a reference
print("\nTesting reference creation...")
db.create_reference('docs\\SYSTEM_STATE.md', 'src\\agentic\\core\\config.py', 'test')
print("Reference created (no error)")

# Check if it worked
with db.driver.session() as session:
    result = session.run('MATCH ()-[r:REFERENCES]->() RETURN count(r) as c')
    count = result.single()['c']
    print(f"REFERENCES count: {count}")
    
    if count > 0:
        result = session.run('MATCH (a)-[r:REFERENCES]->(b) RETURN a.path, b.path LIMIT 5')
        print("\nSample REFERENCES:")
        for r in result:
            print(f"  {r['a.path']} --> {r['b.path']}")

db.close()

