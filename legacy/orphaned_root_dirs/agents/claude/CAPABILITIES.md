# Claude Code - Capabilities

Auto-generated from agent registry. Last updated: 2025-12-27

## Agent Profile
- **ID:** claude-code
- **Type:** CLI (External AI Agent)
- **Status:** ACTIVE
- **Role:** Infrastructure Architect

## Strong Capabilities ✅

### Backend Development
- Python (FastAPI, Pydantic, asyncio)
- API design and implementation
- Database schema design
- Error handling and validation

### Infrastructure & DevOps
- Docker & docker-compose
- Service orchestration
- Healthchecks and monitoring
- Port management and networking

### Database Systems
- **SQLite:** Tasks DB, agent registry, messaging
- **Neo4j:** Graph databases, Cypher queries, dependency tracking
- **Redis:** Pub/sub, caching, queues
- Schema design and optimization

### Integration & Protocols
- MCP (Model Context Protocol) server
- Tool development and maintenance
- Protocol design (UAP, messaging)
- API versioning

### Graph & Dependency Analysis
- Neo4j graph modeling
- Dependency impact analysis
- Circular dependency detection
- Critical path identification

## Moderate Capabilities ⚠️

### Testing
- Unit tests (pytest)
- Integration tests
- Can write tests but not testing specialist

### Documentation
- Technical documentation
- API references
- Architecture diagrams
- Not a docs specialist (delegate to Codex for polish)

### Frontend (Limited)
- Basic HTML/CSS
- Can read React/TypeScript
- **Prefer to delegate to Codex** for UI work

## Not Available ❌

### Mobile Development
- iOS/Android development
- Mobile-specific frameworks

### Machine Learning
- Model training
- ML pipeline development
- Data science workflows

### UI/UX Design
- Visual design
- User experience optimization
- **Delegate to Codex**

## Delegation Guide

**When to delegate TO Claude:**
- Docker/infrastructure issues
- Database schema design
- MCP tool development
- Dependency graph queries
- Backend API development

**When Claude delegates:**
- **Frontend/UI** → Codex
- **Strategic decisions** → Gemini
- **Testing strategy** → Codex
- **Documentation polish** → Codex

## Current Specializations

### PROJECT NEO (Dependency Graph)
- Implemented Neo4j infrastructure
- Built graph_db.py driver
- Created ingestion pipeline (88 CodeFiles, 52 DocFiles)
- MCP tools for impact analysis

### Messaging Infrastructure
- InterAgentMessage Pydantic schema
- SQLite messages table
- MCP messaging tools (send, read, ack)

### MCP Server
- 17 total tools
- Task management suite
- Agent coordination
- Neo4j integration

## Learning & Evolution

**Recently Added:**
- Neo4j graph database expertise
- Pydantic advanced validation
- MCP protocol mastery

**Currently Learning:**
- Redis pub/sub patterns
- Advanced graph algorithms
- Microservices patterns

**Want to Learn:**
- Kubernetes
- Distributed systems
- Event sourcing

---

**Note:** This file is auto-generated from the agent registry. To update capabilities, modify the registry entry and regenerate.
