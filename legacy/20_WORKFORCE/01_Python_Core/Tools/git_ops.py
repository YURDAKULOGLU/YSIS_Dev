import os
from git import Repo, exc

class GitOpsTool:
    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)
        try:
            self.repo = Repo(self.repo_path)
        except exc.InvalidGitRepositoryError:
            self.repo = None
            print(f"[WARNING] {repo_path} is not a valid git repository.")

    def create_branch(self, branch_name: str) -> str:
        """Create and checkout a new branch."""
        if not self.repo: return "Git unavailable."
        
        try:
            current = self.repo.active_branch
            new_branch = self.repo.create_head(branch_name)
            new_branch.checkout()
            return f"Switched to new branch: {branch_name} (from {current.name})"
        except Exception as e:
            return f"Error creating branch: {e}"

    def commit_changes(self, message: str) -> str:
        """Stage all changes and commit."""
        if not self.repo: return "Git unavailable."
        
        try:
            self.repo.git.add(A=True)
            self.repo.index.commit(message)
            return f"Committed with message: '{message}'"
        except Exception as e:
            return f"Error committing: {e}"

    def get_diff(self) -> str:
        """Get the diff of current changes."""
        if not self.repo: return "Git unavailable."
        return self.repo.git.diff()

    def get_current_branch(self) -> str:
        if not self.repo: return "Unknown"
        return self.repo.active_branch.name

git_ops = GitOpsTool()
