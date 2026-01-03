from .base_agent import YBISAgent

class DocWriterAgent(YBISAgent):
    def __init__(self):
        # Use coding model because docs require technical understanding
        super().__init__(agent_id="documentation", model_name="qwen2.5-coder:14b")

    async def document_file(self, file_path: str, code_content: str) -> str:
        prompt = f"""
        You are a Technical Writer. Create a comprehensive Markdown documentation for the following code.

        File: {file_path}

        Code:
        {code_content}

        Output Requirements:
        1. Purpose of the module
        2. Class/Function signatures with explanations
        3. Usage examples
        4. Dependencies

        Output ONLY the Markdown content.
        """

        # We expect raw markdown, not JSON
        result = await self.run(prompt)

        # Cleanup if wrapped in markdown block
        text = str(result)
        if text.startswith("```markdown"):
            text = text.replace("```markdown", "", 1)
            if text.endswith("```"):
                text = text[:-3]
        elif text.startswith("```"):
            text = text.replace("```", "", 1)
            if text.endswith("```"):
                text = text[:-3]

        return text.strip()

doc_writer = DocWriterAgent()
