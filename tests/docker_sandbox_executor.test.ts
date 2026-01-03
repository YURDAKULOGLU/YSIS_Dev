import { DockerSandboxExecutor } from '../src/docker_sandbox_executor';

describe('DockerSandboxExecutor', () => {
    let executor: DockerSandboxExecutor;

    beforeEach(() => {
        executor = new DockerSandboxExecutor();
    });

    it('should run a simple Python script successfully', async () => {
        const code = 'print("Hello, World!")';
        const result = await executor.runCode(code);
        expect(result).toBe('Hello, World!\n');
    });

    it('should handle errors in the executed code', async () => {
        const code = 'raise ValueError("Test error")';
        try {
            await executor.runCode(code);
            fail('Expected an error to be thrown');
        } catch (error) {
            expect(error.message).toContain('ValueError: Test error');
        }
    });
});
