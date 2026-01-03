"""Check Neo4j Graph structure and relationships."""

from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'ybis-graph-2025'))

with driver.session() as session:
    print('=' * 60)
    print('NEO4J GRAPH ANALYSIS')
    print('=' * 60)
    
    # 1. Relationship types
    print('\n=== RELATIONSHIP TYPES ===')
    result = session.run('MATCH ()-[r]->() RETURN type(r) as type, count(*) as count ORDER BY count DESC')
    for r in result:
        print(f"  {r['type']}: {r['count']}")
    
    # 2. Node types
    print('\n=== NODE TYPES ===')
    result = session.run('MATCH (n) RETURN labels(n)[0] as type, count(*) as count ORDER BY count DESC')
    for r in result:
        print(f"  {r['type']}: {r['count']}")
    
    # 3. Sample relationships
    print('\n=== SAMPLE IMPORTS (first 10) ===')
    result = session.run('''
        MATCH (a:CodeFile)-[r:IMPORTS]->(b:CodeFile)
        RETURN a.path as from_file, b.path as to_file
        LIMIT 10
    ''')
    for r in result:
        print(f"  {r['from_file']} --> {r['to_file']}")
    
    # 4. Check for DEFINES relationships
    print('\n=== DEFINES RELATIONSHIPS (file -> class/function) ===')
    result = session.run('''
        MATCH (f:CodeFile)-[:DEFINES]->(e)
        RETURN f.path as file, labels(e)[0] as entity_type, count(*) as count
        ORDER BY count DESC
        LIMIT 10
    ''')
    for r in result:
        print(f"  {r['file']} defines {r['count']} {r['entity_type']}(s)")
    
    # 5. Check DocFile references
    print('\n=== DOCFILE REFERENCES ===')
    result = session.run('''
        MATCH (d:DocFile)
        OPTIONAL MATCH (d)-[r:REFERENCES]->()
        RETURN d.path as doc, count(r) as refs
        ORDER BY refs DESC
        LIMIT 10
    ''')
    for r in result:
        print(f"  {r['doc']}: {r['refs']} outgoing refs")
    
    # 6. Most connected files
    print('\n=== MOST CONNECTED FILES (by imports) ===')
    result = session.run('''
        MATCH (n:CodeFile)
        OPTIONAL MATCH (n)-[:IMPORTS]->(imported)
        OPTIONAL MATCH (importer)-[:IMPORTS]->(n)
        WITH n, count(DISTINCT imported) as imports, count(DISTINCT importer) as importers
        RETURN n.path as file, imports, importers, imports + importers as total
        ORDER BY total DESC
        LIMIT 10
    ''')
    for r in result:
        print(f"  {r['file']}")
        print(f"    imports: {r['imports']}, imported by: {r['importers']}")
    
    # 7. Missing relationships check
    print('\n=== POTENTIAL ISSUES ===')
    
    # Check if REFERENCES exists
    result = session.run('MATCH ()-[r:REFERENCES]->() RETURN count(r) as count')
    refs_count = result.single()['count']
    print(f"  REFERENCES relationships: {refs_count}")
    if refs_count == 0:
        print("  ⚠️ NO REFERENCES! Doc-to-code links missing!")
    
    # Check if USES exists  
    result = session.run('MATCH ()-[r:USES]->() RETURN count(r) as count')
    uses_count = result.single()['count']
    print(f"  USES relationships: {uses_count}")
    if uses_count == 0:
        print("  ⚠️ NO USES! Function call tracking missing!")

driver.close()
print('\n[DONE]')

