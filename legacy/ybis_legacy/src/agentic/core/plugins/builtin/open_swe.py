import os
from pygithub import Github
from src.agentic.core.plugins.docker_executor import DockerExecutor

class OpenSWE:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError("GitHub token is not set in the environment variables.")
        self.github_client = Github(self.github_token)
        self.docker_executor = DockerExecutor(image_name="open_swe_image", retry_count=3)

    def fetch_issues(self, repo_name: str) -> list:
        """Fetch issues from a GitHub repository."""
        repo = self.github_client.get_repo(repo_name)
        return [issue for issue in repo.get_issues(state='open')]

    def contextualize_issue(self, issue):
        """Contextualize the issue details."""
        return f"Issue #{issue.number}: {issue.title}\n{issue.body}"

    def submit_pull_request(self, repo_name: str, title: str, body: str, head: str, base: str) -> dict:
        """Submit a pull request to a GitHub repository."""
        repo = self.github_client.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return {"number": pr.number, "url": pr.html_url}

    def execute(self, operation: str, *args):
        """Execute the specified operation."""
        if operation == "fetch_issues":
            repo_name = args[0]
            issues = self.fetch_issues(repo_name)
            return [self.contextualize_issue(issue) for issue in issues]
        elif operation == "submit_pr":
            repo_name, title, body, head, base = args
            from src.agentic.core.protocols import Plan
            plan = Plan(instructions=f"git clone https://github.com/{repo_name}.git && cd {repo_name} && git checkout -b {head} && echo '{body}' > pr_body.md && git add pr_body.md && git commit -m '{title}' && git push origin {head}")
            result = self.docker_executor.execute(plan, sandbox_path="/path/to/sandbox")
            if result.success:
                return self.submit_pull_request(repo_name, title, body, head, base)
            else:
                raise ValueError(f"Failed to execute Docker plan: {result.output}")
        else:
            raise ValueError(f"Unknown operation: {operation}")
