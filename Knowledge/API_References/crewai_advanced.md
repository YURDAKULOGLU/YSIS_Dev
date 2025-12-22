# CREWAI ADVANCED MANUAL: HIERARCHICAL PROCESS

## 1. Concept: The Manager Agent
A manager agent orchestrates the crew, divides tasks, and validates outcomes.

## 2. Setup Hierarchical Process
```python
from crewai import Agent, Crew, Process

manager = Agent(
    role='Project Manager',
    goal='Oversee research and writing',
    llm=manager_llm # Must be a capable model (e.g. qwen-32b)
)

project_crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_agent=manager
)
```

## 3. Best Practices
- Use a strong LLM for the Manager.
- Ensure `allow_delegation=True` is set appropriately.
- Tasks should have clear `expected_output` for the manager to validate.
