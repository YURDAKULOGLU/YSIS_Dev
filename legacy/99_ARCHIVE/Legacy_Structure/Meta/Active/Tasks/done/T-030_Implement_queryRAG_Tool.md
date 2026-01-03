# Task ID: T-030

- **Source Document:** `RELEASE_READINESS_ASSESSMENT.md`, `docs/epics/7.rag-system.md`
- **Title:** (P0) Implement queryRAG AI Tool for Document Search
- **Description:**
  Implement the missing `queryRAG` tool to complete the AI Tool Calling System (Epic 8). This tool allows the AI to search user-uploaded documents using semantic search (pgvector) and retrieve relevant context for answering questions.

  **Current Status:**
  - ✅ RAG infrastructure exists (pgvector, documents/chunks tables)
  - ✅ Document upload and embedding pipeline exists
  - ✅ Semantic search capability exists
  - ❌ queryRAG tool missing from CORE_TOOLS
  - ❌ queryRAG implementation missing in toolExecutor
  - ❌ queryRAG service function missing

  **Requirements:**
  1. Add `queryRAG` tool definition to `apps/mobile/src/services/ai/tools.ts`
  2. Implement `queryRAG` service function in `apps/mobile/src/services/data/toolServiceFunctions.ts`
  3. Add `queryRAG` case to `apps/mobile/src/services/ai/toolExecutor.ts`
  4. Tool should:
     - Accept a query string parameter
     - Use RAG system to find relevant document chunks (semantic search)
     - Return top-k results (default: 5) with source citations
     - Handle cases where no relevant documents found
     - Support filtering by document type/source if needed

  **Technical Notes:**
  - RAG system uses pgvector with OpenAI text-embedding-3-small (1536 dimensions)
  - Documents stored in `documents` table, chunks in `chunks` table with embeddings
  - Similarity search uses cosine distance
  - See `supabase/migrations/009_rag_system_setup.sql` for schema
  - See `docs/rag/RAG_ARCHITECTURE.md` for architecture details

  **Acceptance Criteria:**
  - [ ] `queryRAG` tool defined in CORE_TOOLS array
  - [ ] Tool accepts `query` parameter (string, required)
  - [ ] Tool accepts optional `limit` parameter (number, default: 5)
  - [ ] Service function implements semantic search via database
  - [ ] Tool executor handles queryRAG case
  - [ ] Returns formatted results with document sources
  - [ ] Handles empty results gracefully
  - [ ] Tested end-to-end: AI can call queryRAG and get results

- **Priority:** P0 (Critical - Blocks Epic 8 completion)
- **Assigned To:** @ClaudeCode
- **Related Tasks:**
  - Epic 8: AI Tool Calling System
  - Epic 7: RAG System (infrastructure already exists)
- **Estimated Effort:** 2-3 hours
- **Dependencies:**
  - RAG infrastructure (✅ already exists)
  - Database access (✅ already exists)
  - OpenAI embeddings (✅ already exists)
