
import asyncio
import os
import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.agentic.core.llm.litellm_provider import get_provider

async def run_mission():
    provider = get_provider()
    
    print("🐍 Generating Snake Game Code...")
    prompt = """
    Write a complete, single-file Python script for a terminal-based Snake game.
    Use 'curses' library.
    It should have:
    - Snake movement
    - Food spawning
    - Score tracking
    - Game over condition
    Ensure the code is robust and handles keyboard interrupts.
    Output ONLY the python code code block.
    """
    
    response = await provider.generate(prompt, model="ollama/qwen2.5-coder:32b")
    code = response["content"]
    
    # Extract code block
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]
        
    code = code.strip()
    
    with open("src/snake_game.py", "w", encoding="utf-8") as f:
        f.write(code)
        
    print("✅ src/snake_game.py created.")
    print(f"Provider used: {response['provider']}")

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    asyncio.run(run_mission())
