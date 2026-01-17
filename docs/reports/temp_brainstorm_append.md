
## 54. DSPy Signatures (Programming, Not Prompting)
- **Concept:** We stop writing English prompts like 'You are a coder...'. Instead, we define Python classes:
  ```python
  class GenerateCode(dspy.Signature):
      """Generates python code from requirements."""
      requirements = dspy.InputField()
      code = dspy.OutputField()
  ```
- **Mechanism:** DSPy's 'Teleprompter' acts as a compiler. It tests 100 variations of the prompt against a metric (e.g., 'Did the code run?') and picks the best one automatically.
- **Benefit:** Model Agnosticism. Switching from GPT-4 to Llama-3 requires zero code changes; just re-compile.

## 55. OpenAI Swarm Patterns (Routines & Handoffs)
- **Concept:** Ultra-lightweight orchestration. No heavy graphs.
- **Handoff:** Agent A says 'I am done with the database schema, transferring control to Agent B for the API endpoints'. The context is preserved perfectly.
- **Routines:** Pre-defined scripts that agents follow blindly until an exception occurs, ensuring consistency.

## 56. MetaGPT SOP (Standard Operating Procedures)
- **Philosophy:** 'Code = SOP(Team)'. The quality of the code is determined by the quality of the team's process.
- **Artifacts:**
    - **PRD (Product Requirement Document):** The 'Why'.
    - **System Design:** The 'How'.
    - **API Spec:** The 'What'.
- **Action:** We must enforce that NO code is written until these 3 artifacts exist. This is the 'Bureaucracy' that saves us from chaos.
