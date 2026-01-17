import { exec, promises as fs } from 'child_process';
import os from 'os'; // Add this line to import the os module
import { promisify } from 'util';

const execAsync = promisify(exec);

export class DockerSandboxExecutor {
    async runCode(code: string): Promise<string> {
        try {
            // Write code to a temporary file
            const tempFilePath = `${os.tmpdir()}/temp_code.py`;
            await fs.promises.writeFile(tempFilePath, code); // Use the promise version of writeFile

            // Run the code in the Docker container
            const { stdout, stderr } = await execAsync(`docker run --rm -v ${tempFilePath}:/app/code.py python:3.12-slim python /app/code.py`);

            if (stderr) {
                throw new Error(stderr);
            }

            return stdout;
        } catch (error) {
            console.error('Error running code in Docker sandbox:', error);
            throw error;
        }
    }
}
