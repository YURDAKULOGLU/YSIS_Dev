"""Test all Docker services"""
import redis
import requests
from neo4j import GraphDatabase

print('=== SERVICE HEALTH CHECK ===')
print()

# Redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('[OK] Redis: Connected')
except Exception as e:
    print(f'[FAIL] Redis: {e}')

# Neo4j
try:
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'ybis-graph-2025'))
    with driver.session() as session:
        result = session.run('RETURN 1 as test')
        result.single()
    driver.close()
    print('[OK] Neo4j: Connected')
except Exception as e:
    print(f'[FAIL] Neo4j: {e}')

# ChromaDB
try:
    response = requests.get('http://localhost:8000/api/v1/heartbeat', timeout=2)
    if response.status_code == 200:
        print('[OK] ChromaDB: Connected')
    else:
        print(f'[FAIL] ChromaDB: Status {response.status_code}')
except Exception as e:
    print(f'[FAIL] ChromaDB: {e}')

# Ollama (host)
try:
    response = requests.get('http://localhost:11434/api/tags', timeout=2)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f'[OK] Ollama: Connected ({len(models)} models)')
    else:
        print(f'[FAIL] Ollama: Status {response.status_code}')
except Exception as e:
    print(f'[FAIL] Ollama: {e}')

print()
print('[DONE]')

