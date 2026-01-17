# CREWAI DOCUMENTATION (LOCAL & OLLAMA)

## 1. Installation
`pip install crewai`

## 2. Using Local LLM (Ollama)
CrewAI relies on LiteLLM. To force local Ollama without OpenAI key:

```python
import os
from crewai import Agent, Task, Crew
from langchain_ollama import ChatOllama

# 1. Environment Variables (CRITICAL)
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_MODEL_NAME"] = "qwen2.5-coder:32b"

# 2. LLM Instance
ollama_llm = ChatOllama(
    model="qwen2.5-coder:32b",
    base_url="http://localhost:11434"
)

# 3. Agent Definition
researcher = Agent(
    role='Researcher',
    goal='Research topics',
    backstory='...',
    llm=ollama_llm, # Inject Local LLM
    verbose=True
)
```

## 3. Core Components
- **Agent:** Role, Goal, Backstory, Tools, LLM.
- **Task:** Description, Expected Output, Agent.
- **Crew:** Agents list, Tasks list, Process (Sequential/Hierarchical).

## 4. Hierarchical Process
Requires a `manager_llm`.
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.hierarchical,
    manager_llm=ollama_llm # Must provide LLM for manager
)
```
