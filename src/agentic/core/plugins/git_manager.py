from __future__ import annotations

import os
import subprocess
from pathlib import Path
from src.agentic.core.utils.logging_utils import get_log_path, log_event


class GitWorktreeManager:
    """
    Manage per-task Git worktrees for isolated agent execution.
    """

    def __init__(self, repo_root: Path, worktrees_root: Path | None = None, base_branch: str | None = None) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.worktrees_root = (
            Path(worktrees_root).resolve()
            if worktrees_root
            else self.repo_root / "workspaces" / "worktrees"
        )
        self.base_branch = base_branch or self._detect_base_branch()

    def _run_git(
        self,
        args: list[str],
        cwd: Path | None = None,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=str(cwd or self.repo_root),
            capture_output=True,
            text=True,
            input=input_text,
            check=False,
        )

    def _get_current_branch(self) -> str:
        result = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Failed to detect current branch")
        return result.stdout.strip()

    def _detect_base_branch(self) -> str:
        env_branch = os.getenv("DEFAULT_BRANCH")
        if env_branch:
            result = self._run_git(["rev-parse", "--verify", env_branch])
            if result.returncode == 0:
                return env_branch

        for candidate in ["main", "master"]:
            result = self._run_git(["rev-parse", "--verify", candidate])
            if result.returncode == 0:
                return candidate

        current = self._get_current_branch()
        log_event("Warning: Could not find 'main' or 'master' branch.", component="git_manager", level="warning")
        log_event(f"Warning: Using current branch '{current}' as base for worktree.", component="git_manager", level="warning")
        log_event("Tip: Set DEFAULT_BRANCH=your-branch to avoid this.", component="git_manager")
        return current

    def _branch_exists(self, branch_name: str) -> bool:
        result = self._run_git(["show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"])
        return result.returncode == 0

    def ensure_worktree(self, task_id: str, branch_prefix: str = "task") -> tuple[Path, str]:
        self.worktrees_root.mkdir(parents=True, exist_ok=True)
        branch_name = f"{branch_prefix}/{task_id}"
        worktree_path = self.worktrees_root / task_id

        if worktree_path.exists() and (worktree_path / ".git").exists():
            return worktree_path, branch_name

        if not self._branch_exists(branch_name):
            result = self._run_git(["branch", branch_name, self.base_branch])
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or "Failed to create branch")

        if worktree_path.exists():
            if any(worktree_path.iterdir()):
                raise RuntimeError(f"Worktree path not empty: {worktree_path}")
            worktree_path.rmdir()

        result = self._run_git(["worktree", "add", str(worktree_path), branch_name])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Failed to add worktree")

        return worktree_path, branch_name

    def list_worktrees(self) -> list[Path]:
        if not self.worktrees_root.exists():
            return []
        return [entry for entry in self.worktrees_root.iterdir() if entry.is_dir()]

    def unstage_gitignored_files(self, cwd: Path | None = None) -> None:
        result = self._run_git(["diff", "--cached", "--name-only"], cwd=cwd)
        if result.returncode != 0 or not result.stdout.strip():
            return

        staged_files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if not staged_files:
            return

        ignored = self._run_git(
            ["check-ignore", "--stdin"],
            cwd=cwd,
            input_text="\n".join(staged_files),
        )
        ignored_files = set()
        if ignored.returncode == 0 and ignored.stdout.strip():
            ignored_files.update(line.strip() for line in ignored.stdout.splitlines() if line.strip())

        extra_patterns = [
            "workspaces/active/",
            "workspaces/worktrees/",
        ]

        for file_path in staged_files:
            normalized = file_path.replace("\\", "/")
            if any(normalized.startswith(pattern) for pattern in extra_patterns):
                ignored_files.add(file_path)

        for file_path in sorted(ignored_files):
            self._run_git(["reset", "HEAD", "--", file_path], cwd=cwd)

    def cleanup_worktree(
        self,
        task_id: str,
        branch_name: str | None,
        keep_branch: bool = True,
        force: bool = False,
    ) -> None:
        worktree_path = self.worktrees_root / task_id
        if worktree_path.exists():
            args = ["worktree", "remove"]
            if force:
                args.append("--force")
            args.append(str(worktree_path))
            result = self._run_git(args)
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or "Failed to remove worktree")

        if not keep_branch and branch_name:
            self._run_git(["branch", "-D", branch_name])

    def _repo_is_clean(self) -> bool:
        result = self._run_git(["status", "--porcelain"])
        return result.returncode == 0 and not result.stdout.strip()

    def merge_worktree_branch(
        self,
        task_id: str,
        branch_name: str,
        strategy: str = "squash",
        auto_commit: bool = True,
        commit_message: str | None = None,
        auto_stash: bool = True,
    ) -> None:
        if not self._branch_exists(branch_name):
            raise RuntimeError(f"Branch not found: {branch_name}")

        # Auto-stash dirty repo before merge (self-healing fix)
        stashed = False
        if not self._repo_is_clean():
            if auto_stash:
                stash_result = self._run_git(["stash", "push", "-m", f"auto-stash-before-merge-{task_id}"])
                if stash_result.returncode == 0:
                    stashed = True
                else:
                    raise RuntimeError("Repository has uncommitted changes and auto-stash failed")
            else:
                raise RuntimeError("Repository has uncommitted changes; aborting merge")

        previous_branch = self._get_current_branch()
        checkout = self._run_git(["checkout", self.base_branch])
        if checkout.returncode != 0:
            raise RuntimeError(checkout.stderr.strip() or "Failed to checkout base branch")

        try:
            if strategy == "squash":
                merge = self._run_git(["merge", "--squash", branch_name])
                if merge.returncode != 0:
                    raise RuntimeError(merge.stderr.strip() or "Squash merge failed")
                self.unstage_gitignored_files(cwd=self.repo_root)
                if auto_commit:
                    message = commit_message or f"merge: {task_id}"
                    commit = self._run_git(["commit", "-m", message, "--no-verify"])
                    if commit.returncode != 0:
                        raise RuntimeError(commit.stderr.strip() or "Commit failed")
            elif strategy == "no-ff":
                args = ["merge", "--no-ff", branch_name]
                if not auto_commit:
                    args.insert(2, "--no-commit")
                merge = self._run_git(args)
                if merge.returncode != 0:
                    raise RuntimeError(merge.stderr.strip() or "Merge failed")
            else:
                raise RuntimeError(f"Unsupported merge strategy: {strategy}")
        finally:
            self._run_git(["checkout", previous_branch])
            # Restore stashed changes if we stashed them
            if stashed:
                self._run_git(["stash", "pop"])


class GitManager:
    """
    Git commit helper for legacy orchestrator flow.
    """

    def __init__(self, project_root: str | Path | None = None) -> None:
        env_root = os.getenv("YBIS_CODE_ROOT")
        root = project_root or env_root or "."
        self.project_root = Path(root).resolve()
        self.log_file = get_log_path("git_manager")

    def _run_git(self, args: list[str]) -> str:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            log_event(f"Git Error: {exc.stderr}", component="git_manager", level="error", log_path=self.log_file)
            raise RuntimeError(f"Git command failed: {exc.stderr}") from exc

    def _normalize_path(self, path: str | Path) -> str:
        try:
            return str(Path(path).resolve().relative_to(self.project_root)).replace("\\", "/")
        except ValueError:
            return str(Path(path)).replace("\\", "/")

    async def commit_task(self, task_id: str, message: str, allowed_files: list[str] | None = None) -> bool:
        try:
            log_event(f"Cleaning up workspace for {task_id}...", component="git_manager", log_path=self.log_file)

            allowed_set: set[str] = set()
            if allowed_files:
                for file_path in allowed_files:
                    normalized = self._normalize_path(file_path)
                    allowed_set.add(normalized)
                    self._run_git(["add", "--", normalized])
            else:
                for folder in ["src", "tests", "config", "scripts", "Knowledge", "docs"]:
                    if (self.project_root / folder).exists():
                        self._run_git(["add", folder])
                self._run_git(["add", "*.md"])

            staged = [line.strip() for line in self._run_git(["diff", "--cached", "--name-only"]).splitlines() if line.strip()]
            if not staged:
                log_event("No relevant changes to commit.", component="git_manager", log_path=self.log_file)
                return True

            normalized_staged = [self._normalize_path(path) for path in staged]
            if allowed_set:
                extra_staged = [path for path in normalized_staged if path not in allowed_set]
                if extra_staged:
                    log_event("[!] Staged files outside allowed set; aborting commit.", component="git_manager", level="warning", log_path=self.log_file)
                    return False

            status_lines = [line for line in self._run_git(["status", "--porcelain"]).splitlines() if line.strip()]
            unstaged_entries: list[str] = []
            for line in status_lines:
                code = line[:2]
                if code == "??" or code[1] != " ":
                    unstaged_entries.append(line)
            if unstaged_entries:
                log_event("[!] Unstaged or untracked files detected; aborting commit.", component="git_manager", level="warning", log_path=self.log_file)
                return False

            full_message = f"AUTO-COMMIT [{task_id}]: {message}"
            self._run_git(["commit", "-m", full_message, "--no-verify"])
            log_event(f"Successfully committed: {full_message}", component="git_manager", log_path=self.log_file)
            return True
        except Exception as exc:
            log_event(f"[!] Commit failed: {exc}", component="git_manager", level="error", log_path=self.log_file)
            return False

    async def push_changes(self) -> bool:
        try:
            log_event("Pushing to remote...", component="git_manager", log_path=self.log_file)
            self._run_git(["push"])
            return True
        except Exception as exc:
            log_event(f"[!] Push failed: {exc}", component="git_manager", level="error", log_path=self.log_file)
            return False

    def name(self) -> str:
        return "Git-Giant-Manager"
