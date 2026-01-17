# 🧠 YBIS Master Cheat Sheet (v5.0 - 2026)

This document contains local documentation for core libraries to ensure agents can utilize them effectively.

---

## 1. LlamaIndex (Agentic RAG & Workflows)
**Location:** `Knowledge/Frameworks/LlamaIndex`

### Key Workflow:
```python
from llama_index.core.workflow import AgentWorkflow
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

# 1. Ingest
docs = SimpleDirectoryReader("Knowledge/Context").load_data()
index = VectorStoreIndex.from_documents(docs)

# 2. Setup Agent
workflow = AgentWorkflow.from_tools_or_functions(
    [query_engine_tool], 
    llm=ollama_llm
)
```

### Core Components:
- `AgentWorkflow`: Orchestrates multi-agent handoffs.
- `LlamaParse`: High-accuracy parsing for complex PDFs.

---

## 2. PydanticAI (Production-Grade Agents)
**Location:** `Knowledge/Frameworks/PydanticAI`

### Key Pattern:
```python
from pydantic import BaseModel
from pydantic_ai import Agent

class SuccessResponse(BaseModel):
    is_success: bool
    details: str

agent = Agent('ollama:qwen2.5-coder', result_type=SuccessResponse)

@agent.tool
async def get_repo_status(ctx: RunContext[None]) -> str:
    return "Ready"

result = await agent.run("Check repo status")
print(result.data.is_success)
```

---

## 3. Ragas (Evaluation)
**Location:** `Knowledge/Frameworks/Ragas`

### Core Metrics:
- `Faithfulness`: Factual consistency with context.
- `Answer Relevancy`: How well the answer addresses the question.
- `Tool Call Accuracy`: Precision of agent tool invocations.

### Usage:
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

results = evaluate(dataset, metrics=[faithfulness, answer_relevancy])
```

---

## 4. Unstructured (Document Processing)
- Use `unstructured` to parse diverse formats (PDF, DOCX, HTML).
- Essential for ingesting new expansion pack documentation.

---

**Rules:** 
1. Always check this file before implementing new features.
2. Use `PydanticAI` for all new agent definitions to ensure type safety.
3. Every RAG change MUST be evaluated with `Ragas`.
