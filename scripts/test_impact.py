"""Test impact analysis with the improved graph"""
import sys
sys.path.insert(0, 'src')
from agentic.infrastructure.graph_db import GraphDB

db = GraphDB()

print("=" * 60)
print("IMPACT ANALYSIS TESTS")
print("=" * 60)

# Test 1: What happens if protocols.py changes?
print("\n1. If src\\agentic\\core\\protocols.py changes:")
impact = db.impact_analysis("src\\agentic\\core\\protocols.py", max_depth=2)
print(f"   {len(impact)} files would be affected")
for item in impact[:10]:
    print(f"   - {item.get('path')} (distance: {item.get('distance')})")
if len(impact) > 10:
    print(f"   ... and {len(impact) - 10} more")

# Test 2: What happens if model_router.py changes?
print("\n2. If src\\agentic\\core\\plugins\\model_router.py changes:")
impact = db.impact_analysis("src\\agentic\\core\\plugins\\model_router.py", max_depth=2)
print(f"   {len(impact)} files would be affected")
for item in impact[:10]:
    print(f"   - {item.get('path')} (distance: {item.get('distance')})")

# Test 3: Critical nodes (most dependents)
print("\n3. Critical files (change these = high impact):")
critical = db.get_critical_nodes(min_dependents=3, limit=10)
for item in critical:
    print(f"   - {item.get('path')}: {item.get('dependents')} dependents")

# Test 4: Show some REFERENCES
print("\n4. Sample doc-to-code REFERENCES:")
with db.driver.session() as session:
    result = session.run("""
        MATCH (d:DocFile)-[r:REFERENCES]->(c:CodeFile)
        RETURN d.path as doc, c.path as code
        LIMIT 10
    """)
    for r in result:
        print(f"   {r['doc']} --> {r['code']}")

db.close()
print("\n[DONE]")

