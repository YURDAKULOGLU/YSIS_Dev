import docker
import tempfile
import shutil
from pathlib import Path

class DockerSandboxExecutor:
    """
    Executor that runs code in a Docker container.
    """

    def __init__(self, image_name: str = "python:3.12-slim"):
        self.client = docker.from_env()
        self.image_name = image_name

    async def run_code(self, code: str) -> str:
        """
        Run the given Python code in a Docker container and return the output.

        Args:
            code (str): The Python code to execute.

        Returns:
            str: The output of the executed code.
        """
        # Create a directory on the host for code execution
        temp_dir = Path(tempfile.mkdtemp())
        host_code_file_path = temp_dir / "temp_code.py"
        host_code_file_path.write_text(code, encoding='utf-8')

        try:
            container = self.client.containers.run(
                image=self.image_name,
                command="python /app/temp_code.py",
                volumes={str(temp_dir): {'bind': '/app', 'mode': 'ro'}},
                remove=True,
                stdout=True,
                stderr=True
            )
            output = container.logs().decode('utf-8')
        except docker.errors.ContainerError as e:
            output = f"Container error: {e.stderr.decode('utf-8')}"
        except Exception as e:
            output = f"An error occurred: {str(e)}"
        finally:
            # Ensure the temporary directory is deleted
            shutil.rmtree(temp_dir)

        return output
