"""Debug REFERENCES issue"""
import sys
sys.path.insert(0, 'src')
from agentic.infrastructure.graph_db import GraphDB

db = GraphDB()

with db.driver.session() as session:
    # Check exact paths
    print("Looking for SYSTEM_STATE.md...")
    result = session.run("MATCH (d:DocFile) WHERE d.path CONTAINS 'SYSTEM_STATE' RETURN d.path")
    for r in result:
        print(f"  Found: {r['d.path']}")
    
    print("\nLooking for config.py...")
    result = session.run("MATCH (c:CodeFile) WHERE c.path CONTAINS 'config.py' RETURN c.path LIMIT 5")
    for r in result:
        print(f"  Found: {r['c.path']}")
    
    # Test with actual paths found
    print("\nTrying to match with label...")
    result = session.run("""
        MATCH (from:DocFile {path: 'SYSTEM_STATE.md'})
        MATCH (to:CodeFile {path: 'src\\\\agentic\\\\core\\\\config.py'})
        RETURN from.path, to.path
    """)
    for r in result:
        print(f"  Matched: {r['from.path']} -> {r['to.path']}")

db.close()

