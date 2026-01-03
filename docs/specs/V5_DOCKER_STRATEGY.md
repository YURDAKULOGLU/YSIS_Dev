# V5 Docker Strategy
> All infrastructure services in Docker for consistency and portability

**Status:** Active  
**Date:** 2025-01-03  
**Principle:** "If it can run in Docker, it should run in Docker"

---

## 🐳 Current Docker Services

### [OK] Already in Docker

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| **Redis** | `redis:alpine` | 6379 | Event bus, pub/sub, caching |
| **Neo4j** | `neo4j:5.15-community` | 7474, 7687 | Graph database (dependencies) |
| **ChromaDB** | `chromadb/chroma:latest` | 8000 | Vector DB (RAG) |
| **Ollama** | `ollama/ollama:latest` | 11434 | Local LLM server |

### [PKG] Application Services

| Service | Purpose | Status |
|---------|---------|--------|
| **worker** | Main orchestrator worker | [OK] Docker |
| **dashboard** | Streamlit dashboard | [OK] Docker |
| **viz** | Neo4j visualization | [OK] Docker |
| **sandbox** | Code execution sandbox | [OK] Docker |

---

## [TARGET] Docker-First Benefits

### 1. **Consistency**
- [OK] Same environment everywhere (dev, staging, prod)
- [OK] No "works on my machine" issues
- [OK] Reproducible setups

### 2. **Isolation**
- [OK] Services don't conflict with host
- [OK] Easy cleanup (just `docker-compose down`)
- [OK] Resource limits per service

### 3. **Portability**
- [OK] Run anywhere Docker runs
- [OK] Easy deployment
- [OK] Version control for infrastructure

### 4. **Local-First Compliance**
- [OK] All services self-hosted (no cloud required)
- [OK] Data stays local (volumes)
- [OK] No external dependencies

---

## 📋 Service Configuration

### Redis (Event Bus)
```yaml
redis:
  image: redis:alpine
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
```

**Usage:**
- Event bus for real-time updates
- Pub/sub for debate system
- Caching layer
- Task queue (if needed)

### Neo4j (Graph DB)
```yaml
neo4j:
  image: neo4j:5.15-community
  ports:
    - "7474:7474"  # Browser UI
    - "7687:7687"  # Bolt protocol
  environment:
    NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
  volumes:
    - neo4j_data:/data
```

**Usage:**
- Dependency graph (imports, references)
- Impact analysis
- Staleness detection
- Code structure tracking

### ChromaDB (Vector DB)
```yaml
chromadb:
  image: chromadb/chroma:latest
  ports:
    - "8000:8000"
  volumes:
    - chroma_data:/chroma/chroma
```

**Usage:**
- RAG (Retrieval Augmented Generation)
- Semantic code search
- Framework documentation storage
- Lesson memory

### Ollama (Local LLM)
```yaml
ollama:
  image: ollama/ollama:latest
  ports:
    - "11434:11434"
  volumes:
    - ollama_data:/root/.ollama
```

**Usage:**
- Primary LLM provider (local-first)
- Model serving (qwen2.5-coder, etc.)
- No API keys needed
- GPU support (if available)

---

## 🔄 Migration from Host to Docker

### Before (Host-Based)
```python
# Ollama on host
OLLAMA_BASE_URL = "http://localhost:11434"

# Redis on host
REDIS_HOST = "localhost"

# ChromaDB on host (if any)
CHROMA_HOST = "localhost"
```

### After (Docker-Based)
```python
# Ollama in Docker
OLLAMA_BASE_URL = "http://ollama:11434"  # Service name

# Redis in Docker
REDIS_HOST = "redis"  # Service name

# ChromaDB in Docker
CHROMA_HOST = "chromadb"  # Service name
```

**Benefits:**
- [OK] Services always available (no manual start)
- [OK] Consistent networking
- [OK] Health checks ensure readiness
- [OK] Easy scaling

---

## [LAUNCH] Quick Start

### 1. Start All Services
```bash
docker-compose up -d
```

### 2. Check Health
```bash
docker-compose ps
```

### 3. View Logs
```bash
docker-compose logs -f redis
docker-compose logs -f ollama
```

### 4. Stop Services
```bash
docker-compose down
```

### 5. Clean Everything ([WARN]️ deletes data)
```bash
docker-compose down -v
```

---

## [CHART] Service Dependencies

```
┌─────────┐
│ worker  │
└────┬────┘
     │
     ├──► redis (events)
     ├──► neo4j (graph)
     ├──► chromadb (RAG)
     └──► ollama (LLM)

┌──────────┐
│ dashboard│
└────┬─────┘
     │
     ├──► redis (events)
     ├──► neo4j (graph)
     └──► ollama (LLM)
```

---

## [TOOL] Environment Variables

All services use environment variables for configuration:

```bash
# .env file (optional)
NEO4J_PASSWORD=ybis-graph-2025
GITHUB_TOKEN=your_token_here
OLLAMA_MODEL=qwen2.5-coder:32b
```

**Service Discovery:**
- Services find each other by Docker service name
- No need for `localhost` or IP addresses
- Automatic DNS resolution in Docker network

---

## 💾 Data Persistence

All data is persisted in Docker volumes:

| Volume | Contains |
|--------|----------|
| `redis_data` | Redis database |
| `neo4j_data` | Neo4j database |
| `neo4j_logs` | Neo4j logs |
| `neo4j_import` | Import files |
| `chroma_data` | ChromaDB vectors |
| `ollama_data` | Ollama models |

**Backup:**
```bash
# Backup volumes
docker run --rm -v ybis_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_backup.tar.gz /data
```

---

## [TARGET] Future Docker Services

### Potential Additions:
- [OK] **PostgreSQL** (if needed for structured data)
- [OK] **MinIO** (S3-compatible object storage)
- [OK] **Prometheus** (metrics collection)
- [OK] **Grafana** (metrics visualization)
- [OK] **Elasticsearch** (if needed for advanced search)

**Rule:** If a service can run in Docker and benefits the system, add it to `docker-compose.yml`.

---

## 🔐 Security Considerations

### 1. **Network Isolation**
- Services communicate via Docker network
- No external exposure unless needed (ports)

### 2. **Volume Security**
- Volumes are Docker-managed
- No host filesystem access (unless mounted)

### 3. **Environment Variables**
- Sensitive data in `.env` (gitignored)
- Never commit secrets

### 4. **Resource Limits**
- Can add `deploy.resources.limits` per service
- Prevents resource exhaustion

---

## 📚 References

- **Docker Compose:** `docker-compose.yml`
- **Dockerfiles:** `docker/Dockerfile.*`
- **Architecture:** `docs/governance/00_GENESIS/ARCHITECTURE_PRINCIPLES.md`
- **Local-First Principle:** Constitution §1.3

---

## [OK] Checklist

- [x] Redis in Docker
- [x] Neo4j in Docker
- [x] ChromaDB in Docker
- [x] Ollama in Docker
- [x] Worker in Docker
- [x] Dashboard in Docker
- [x] Health checks configured
- [x] Volumes for persistence
- [x] Environment variables set
- [x] Service dependencies defined

---

**Status:** [OK] All infrastructure services containerized and ready!

