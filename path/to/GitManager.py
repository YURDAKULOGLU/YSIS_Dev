from src.agentic.core.logger import log


class GitManager:
    def __init__(self):
        self.logger = log.bind(task_id="git_manager")

    def run_git(self, args: list) -> str:
        self.logger.info(f"Running git command: {' '.join(args)}")
        # Existing code...
