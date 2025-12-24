from typing import List

class Agent:
    def __init__(self, name: str):
        self.name = name

    def execute(self, task: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

class Coder(Agent):
    def __init__(self):
        super().__init__("Coder")

    def execute(self, task: str) -> str:
        return f"Coding task: {task}"

class Reviewer(Agent):
    def __init__(self):
        super().__init__("Reviewer")

    def execute(self, task: str) -> str:
        return f"Reviewing task: {task}"

def create_crew() -> List[Agent]:
    return [Coder(), Reviewer()]
