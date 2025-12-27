---
title: "YBIS Stable V2 Roadmap: Project Builder Transformation"
date: 2025-12-28
status: DRAFT
priority: CRITICAL
---

# YBIS Stable V2: From Self-Modifier to Project Builder

## Vision

**Current State**: YBIS modifies itself
**Target State**: YBIS builds OTHER projects end-to-end

**User Request**: "Make me a snake game"
**System Output**: Complete, deployable snake game

## Market Research (Dec 2025)

### 1. MCP Ecosystem

**Available Now**:
- 16,000+ MCP servers in marketplace
- Official repo: https://github.com/modelcontextprotocol/servers
- Awesome collections: https://github.com/punkpeye/awesome-mcp-servers
- Linux Foundation managed (Dec 2025)

**Key Servers We Can Integrate**:
- File system access (read/write projects)
- Database connections (PostgreSQL, MySQL, MongoDB)
- API integrations (GitHub, GitLab, deployment services)
- Browser automation (Playwright, Puppeteer)
- Testing frameworks (pytest, jest, playwright)

**What We're Missing**:
- File system MCP server (we only have internal tools)
- Git operations MCP server (we have git_manager but not MCP-exposed)
- Deployment MCP servers (Vercel, Netlify, Railway)
- Testing MCP servers (automated test generation)

### 2. End-to-End Project Builders

**Bolt.new**:
- Browser-based full-stack development
- Supabase backend integration
- Zero-setup environment
- Multi-framework (React, Vue, Angular, React Native)
- Pricing: ~$20-40/month

**Lovable**:
- Fastest MVP builder ($0→$20M ARR in 60 days!)
- Bidirectional GitHub sync (!)
- Supabase Cloud integration
- Design + code + deploy in one place
- Pricing: $25/month

**v0 by Vercel**:
- UI component generation (React + Tailwind)
- Production-ready code
- Next.js ecosystem integration
- SOC 2 Type II compliant
- NO backend/database (UI only)

**What They Have That We Don't**:
1. **Instant scaffolding**: Bolt/Lovable create full app structure in seconds
2. **Integrated deployment**: Push to production with one click
3. **Live preview**: See changes instantly in browser
4. **Backend automation**: Supabase integration for database + auth
5. **GitHub sync**: Bidirectional code sync (Lovable)

### 3. Agentic Frameworks

**AutoGen/AG2**:
- Multi-agent conversations
- Code execution
- We already evaluated (Frankenstein debate)

**CrewAI**:
- Task-based agent coordination
- We have bridge: src/agentic/bridges/crewai_bridge.py

**LangGraph**:
- Workflow orchestration
- We use: OrchestratorGraph based on LangGraph

## Gap Analysis: YBIS vs Market Leaders

| Capability | Bolt/Lovable | v0 | YBIS Current | YBIS Needs |
|------------|--------------|-----|--------------|------------|
| Project Scaffolding | ✅ Instant | ✅ UI only | ⚠️ Manual (Aider) | **Auto-scaffold** |
| Code Generation | ✅ Full-stack | ✅ UI components | ✅ Via Aider | **Structure aware** |
| Backend/DB | ✅ Supabase | ❌ | ⚠️ Manual | **Auto-provision** |
| Deployment | ✅ 1-click | ✅ Vercel | ❌ | **CI/CD pipeline** |
| Live Preview | ✅ Browser | ✅ Browser | ❌ | **Dev server** |
| GitHub Sync | ✅ Bidirectional | ✅ Push | ⚠️ Manual git | **Auto-sync** |
| Testing | ⚠️ Basic | ❌ | ⚠️ pytest exists | **Auto-generate tests** |
| Multi-agent | ❌ | ❌ | ✅ Council+CrewAI | **Unique advantage!** |
| Memory | ❌ | ❌ | ✅ Cognee+Neo4j | **Unique advantage!** |
| Dependency Graph | ❌ | ❌ | ✅ Neo4j | **Unique advantage!** |

## YBIS Unique Advantages

What we have that Bolt/Lovable/v0 DON'T:

1. **Multi-LLM Council**: Consensus decision-making
2. **Persistent Memory**: Learn from every project (Cognee)
3. **Dependency Graph**: Understand code relationships (Neo4j)
4. **Self-modifying**: Can improve own scaffolding logic
5. **Multi-agent**: Different specialists for different tasks
6. **Local-first**: No cloud lock-in (Ollama + local tools)

## Roadmap: Stable V2 (Project Builder)

### Phase 1: Essential MCP Servers (Week 1)

**Integrate from marketplace**:
```
1. File System Server
   - Source: modelcontextprotocol/servers/src/filesystem
   - Purpose: Read/write project files safely

2. Git Server
   - Source: modelcontextprotocol/servers/src/git
   - Purpose: Automated git operations

3. GitHub Server
   - Source: modelcontextprotocol/servers/src/github
   - Purpose: Repo creation, PR management

4. PostgreSQL Server (Optional)
   - Source: modelcontextprotocol/servers/src/postgres
   - Purpose: Database provisioning
```

### Phase 2: Project Scaffolding Engine (Week 2)

**Create: ProjectScaffolder**
```python
class ProjectScaffolder:
    """
    Generate complete project structure from high-level description.

    Example:
        scaffolder.create_project(
            "snake game in Python with Pygame",
            tech_stack=["python", "pygame"],
            features=["score tracking", "high scores", "levels"]
        )
    """

    def create_project(self, description: str, **kwargs):
        # 1. Ask council: "What's the best architecture for this?"
        architecture = ask_council(f"Best architecture for: {description}")

        # 2. Generate file structure
        structure = self._generate_structure(architecture)

        # 3. For each file, use Aider to generate code
        for file_path, spec in structure.items():
            self._generate_file(file_path, spec)

        # 4. Create tests
        self._generate_tests()

        # 5. Create README, setup.py, requirements.txt
        self._generate_meta_files()

        # 6. Initialize git repo
        self._init_git()

        # 7. Add to memory: "I built a snake game with pygame"
        add_to_memory(f"Project: {description}. Architecture: {architecture}")

        return project_path
```

**Integration Points**:
- Council: Architecture decisions
- Memory: Remember successful patterns
- Neo4j: Track project dependencies
- Aider: Code generation
- Git MCP: Version control

### Phase 3: Deployment Pipeline (Week 3)

**Create: DeploymentManager**
```python
class DeploymentManager:
    """
    Deploy projects to various platforms.
    """

    def deploy(self, project_path: str, target: str):
        if target == "vercel":
            # Use Vercel CLI via MCP
        elif target == "railway":
            # Use Railway API
        elif target == "docker":
            # Build and run container

        # Add deployment info to memory
        add_to_memory(f"Deployed {project_path} to {target}")
```

### Phase 4: Auto-Testing (Week 4)

**Enhance: TestGenerator**
```python
class TestGenerator:
    """
    Automatically generate comprehensive tests.
    """

    def generate_tests(self, project_path: str):
        # 1. Analyze codebase with Neo4j
        graph_analysis = check_dependency_impact(project_path)

        # 2. Ask council: "What tests are critical?"
        test_plan = ask_council(f"Test strategy for: {project_path}")

        # 3. Generate tests with Aider
        # 4. Run tests
        # 5. Fix failures automatically
```

### Phase 5: Live Preview (Bonus)

**Option A**: Integrate existing server
- Vite dev server for web projects
- Streamlit for Python apps
- Live reload on file changes

**Option B**: Web-based IDE (like Bolt)
- Browser interface to YBIS
- Monaco editor
- Live preview pane

## Implementation Strategy

### What to Build In-House

1. **ProjectScaffolder**: Core logic unique to YBIS
2. **Council Integration**: Our unique advantage
3. **Memory Integration**: Learn from every project
4. **Graph-aware generation**: Use Neo4j for smart scaffolding

### What to Integrate from Market

1. **MCP Servers**: File system, Git, GitHub (ready-made)
2. **Deployment**: Use existing CLIs (Vercel, Railway, Docker)
3. **Testing frameworks**: pytest, jest (existing tools)
4. **Dev servers**: Vite, Streamlit (existing tools)

### What NOT to Build

1. **UI builder**: v0 does this better (can use their API?)
2. **Database GUI**: Supabase dashboard exists
3. **Browser IDE**: Bolt.new exists (we're CLI-first)

## Success Metrics: Stable V2

**Before (Self-Modifier)**:
- User: "Add feature X to YBIS"
- YBIS: Modifies own code

**After (Project Builder)**:
- User: "Make me a snake game"
- YBIS:
  1. ✅ Scaffolds complete project structure
  2. ✅ Generates all code files
  3. ✅ Creates tests
  4. ✅ Initializes git repo
  5. ✅ (Optional) Deploys to web
  6. ✅ Remembers patterns for next time

**Test Case**:
```
Input: "Create a todo app with React frontend and FastAPI backend"

Expected Output:
- ✅ Frontend: React + Vite + Tailwind
- ✅ Backend: FastAPI + SQLite
- ✅ Tests: Jest (frontend) + pytest (backend)
- ✅ Docker: docker-compose.yml
- ✅ Git: Initialized with .gitignore
- ✅ Deploy: One command to Railway/Vercel
- ✅ Time: <5 minutes
```

## Integration Priorities

### Must Have (Stable V2 Blockers):

1. **File System MCP Server** → Read/write projects safely
2. **Git MCP Server** → Automated version control
3. **ProjectScaffolder** → Core project generation engine
4. **Test Auto-generation** → Every project needs tests

### Should Have (V2.1):

1. **GitHub MCP Server** → Auto-create repos, push
2. **DeploymentManager** → One-click deploy
3. **Database MCP Servers** → Auto-provision DBs

### Nice to Have (V2.2+):

1. **Live Preview** → See projects running
2. **UI Builder Integration** → Use v0 API for UI generation
3. **Multi-project Memory** → "Build another app like the last one"

## MCP Server Installation Plan

**Week 1 Targets**:

```bash
# 1. Clone official MCP servers repo
git clone https://github.com/modelcontextprotocol/servers.git tools/mcp-servers

# 2. Integrate file system server
# Create bridge: src/agentic/bridges/filesystem_mcp_bridge.py

# 3. Integrate git server
# Create bridge: src/agentic/bridges/git_mcp_bridge.py

# 4. Add MCP tools to mcp_server.py
@mcp.tool()
def create_file(path: str, content: str) -> str:
    # Uses filesystem MCP server

@mcp.tool()
def git_init(project_path: str) -> str:
    # Uses git MCP server
```

## References

- MCP Official: https://modelcontextprotocol.io
- MCP Servers: https://github.com/modelcontextprotocol/servers
- Awesome MCP: https://github.com/punkpeye/awesome-mcp-servers
- Bolt.new comparison: https://uibakery.io/blog/bolt-vs-lovable-vs-v0
- Lovable analysis: https://annaarteeva.medium.com/choosing-your-ai-prototyping-stack-lovable-v0-bolt-replit-cursor-magic-patterns-compared-9a5194f163e9

## Next Steps

1. **Immediate**: Clone MCP servers repo, evaluate which to integrate
2. **This Week**: Build ProjectScaffolder prototype
3. **Next Week**: Full integration test with "snake game" example
4. **Stable V2**: Release project builder capability

---

**Goal**: YBIS becomes the **most intelligent** project builder by combining Bolt's speed + Lovable's features + our unique multi-agent memory-powered approach.
