import subprocess
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Plan:
    instructions: str

@dataclass
class CodeResult:
    success: bool
    output: str

class DockerExecutor:
    """
    Executor that runs code inside a Docker container.
    """

    def __init__(self, image_name="sandbox"):
        self.image_name = image_name

    async def execute(self, plan: Plan, sandbox_path: str, error_history: Optional[List[str]] = None, retry_count: int = 3) -> CodeResult:
        """
        Execute a plan inside a Docker container.
        """
        try:
            # Build the Docker image if it doesn't exist
            try:
                subprocess.run(["docker", "image", "inspect", self.image_name], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["docker", "build", "-t", self.image_name, "."], check=True)

            # Run the Docker container with the plan
            result = subprocess.run(
                ["docker", "run", "--rm", "-v", f"{sandbox_path}:/app/sandbox", self.image_name, "python", "-c", plan.instructions],
                capture_output=True,
                text=True,
                check=True
            )

            return CodeResult(success=True, output=result.stdout)
        except subprocess.CalledProcessError as e:
            if retry_count > 0:
                return await self.execute(plan, sandbox_path, error_history + [str(e)], retry_count - 1)
            else:
                return CodeResult(success=False, output=str(e))
