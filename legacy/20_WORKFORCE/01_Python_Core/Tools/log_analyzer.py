import os
import json
import subprocess
from ..Local.runner import runner

class LogAnalyzerTool:
    def __init__(self, log_dir: str = "."):
        # fetch-logs.ts saves to root dir by default
        self.log_dir = os.path.abspath(log_dir)
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Meta/Bridges/Scripts/fetch-logs.ts"))

    def fetch_logs(self):
        """Executes the TypeScript log fetcher"""
        print(f"[LogAnalyzer] Fetching logs using {self.script_path}...")
        try:
            # Run the TS script using npx tsx
            # Assumes running from project root or handles paths correctly
            result = subprocess.run(
                ["npx", "tsx", self.script_path],
                capture_output=True,
                text=True,
                cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")) # Run from Project Root
            )

            if result.returncode != 0:
                return f"Error fetching logs: {result.stderr}"

            return "Logs fetched successfully."
        except Exception as e:
            return f"Failed to execute log fetcher: {e}"

    def analyze_feedback(self, log_file: str = "logs_dump.json") -> str:
        """
        Fetches fresh logs and generates roadmap suggestions using LLM.
        """
        # 1. Fetch Fresh Logs
        fetch_status = self.fetch_logs()
        if "Error" in fetch_status:
            print(f"[WARNING] Warning: {fetch_status}. Trying to analyze existing logs.")

        # 2. Read Logs
        # The TS script saves to root/logs_dump.json
        # Check root dir first
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        file_path = os.path.join(root_path, log_file)

        if not os.path.exists(file_path):
            return f"No log file found at {file_path}. Ensure Supabase connection."

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                logs_data = json.load(f)

            # Filter logs to keep context window small (e.g., only ERRORs or last 50 logs)
            # For now, let's take last 50 logs to be safe
            recent_logs = logs_data[:50] if len(logs_data) > 50 else logs_data
            logs_str = json.dumps(recent_logs, indent=2)

            # 3. Ask LLM
            prompt = f"""
            You are a Product Manager (PM). Analyze the following Supabase application logs.

            Logs (Recent 50):
            {logs_str}

            Task:
            1. Identify recurring ERROR patterns.
            2. Identify any USER_ACTION logs that imply feature usage.
            3. Suggest specific Roadmap Items (Bug Fixes or Improvements).

            Output Format:
            - **Critical Bugs:** [List]
            - **Performance Issues:** [List]
            - **Usage Insights:** [List]
            """

            analysis = runner.invoke(
                task_type="spec_writing",
                system_prompt="You are an expert Technical Product Manager.",
                user_message=prompt
            )

            return analysis

        except Exception as e:
            return f"Error analyzing logs: {e}"

log_analyzer = LogAnalyzerTool()
