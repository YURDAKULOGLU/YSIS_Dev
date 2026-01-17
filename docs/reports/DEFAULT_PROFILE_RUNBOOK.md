# Running YBIS with the Default Profile

## Prerequisites
- Ensure that Ollama is running.
- Install the necessary Python dependencies by running:
  ```bash
  pip install -r requirements.txt
  ```

## Steps to Run a Task
1. Open your terminal or command prompt.
2. Navigate to the YBIS project root.
3. Run a task with the default profile (existing task ID):
   ```powershell
   $env:YBIS_PROFILE="default"
   python scripts/ybis_run.py <TASK_ID>
   ```
4. For a quick end-to-end smoke run (creates a simple task and executes it):
   ```powershell
   $env:YBIS_PROFILE="default"
   python scripts/create_and_run_simple_task.py
   ```

## Qdrant (Local Vector Store) Setup
- Run Qdrant using Docker with the following command:
  ```bash
  docker run -p 6333:6333 qdrant/qdrant
  ```
- Check if Qdrant is running by accessing [http://localhost:6333/ping](http://localhost:6333/ping) in your web browser or using:
  ```bash
  curl http://localhost:6333/ping
  ```

## Expected Outcomes
- The run initializes with the default profile settings and enforces policy gates and protected paths.
- Artifacts are written under `workspaces/<TASK_ID>/runs/<RUN_ID>/artifacts` (gate report, verifier report, plan).
- Typical gate results:
  - `PASS` for clean doc-only or low-risk changes.
  - `BLOCK` if lint/tests fail or protected paths are touched without approval.

## Troubleshooting
- **Ollama Not Running**: Ensure that Ollama service is properly installed and started. Check the service status using your system's service management tool.
- **Missing Dependencies**: Verify that all required dependencies are listed in `requirements.txt` and installed. You can reinstall them by running `pip install -r requirements.txt`.
- **Gate/Verifier Artifacts Location**: Gate and verifier artifacts can be found under `workspaces/<TASK_ID>/runs/<RUN_ID>/artifacts`.