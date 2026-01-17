"""
Sentinel V2 - Advanced AST-based code analysis.

Ports advanced verification logic from legacy sentinel_enhanced.py.
Detects broken imports, complexity, dead code, and architectural violations.
Integrates Bandit for security scanning.
"""

import ast
import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class SentinelReport:
    """Extended verification report with AST analysis results."""

    def __init__(
        self,
        broken_imports: list[str] | None = None,
        complexity_violations: list[str] | None = None,
        dead_code: list[str] | None = None,
        architectural_violations: list[str] | None = None,
        security_violations: list[str] | None = None,
    ):
        """Initialize Sentinel report."""
        self.broken_imports = broken_imports or []
        self.complexity_violations = complexity_violations or []
        self.dead_code = dead_code or []
        self.architectural_violations = architectural_violations or []
        self.security_violations = security_violations or []


class SentinelV2:
    """
    Sentinel V2 - Advanced AST-based code analyzer.

    Detects:
    - Broken imports
    - Logic complexity (Cyclomatic complexity)
    - Dead code
    - Architectural violations (e.g., importing from legacy in new core)
    - Security vulnerabilities (via Bandit: eval, hardcoded secrets, etc.)
    """

    def __init__(self, max_complexity: int = 10):
        """
        Initialize Sentinel V2.

        Args:
            max_complexity: Maximum allowed cyclomatic complexity
        """
        self.max_complexity = max_complexity
        self.restricted_imports = ["os.system", "shutil.rmtree", "subprocess.call"]
        self.legacy_paths = ["src/agentic", "legacy"]

    def analyze(self, file_path: Path, project_root: Path) -> SentinelReport:
        """
        Analyze a Python file using AST.

        Args:
            file_path: Path to Python file
            project_root: Project root directory

        Returns:
            SentinelReport with analysis results
        """
        broken_imports = []
        complexity_violations = []
        dead_code = []
        architectural_violations = []

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))

            # Check for broken imports
            broken_imports = self._check_imports(tree, file_path, project_root)

            # Check complexity
            complexity_violations = self._check_complexity(tree, file_path)

            # Check for dead code
            dead_code = self._check_dead_code(tree, file_path)

            # Check architectural violations
            architectural_violations = self._check_architectural_violations(
                tree, file_path, project_root
            )
            security_violations = self._check_sensitive_env_exposure(tree, file_path)
            architectural_violations.extend(security_violations)

            # 📋 Adamakıllı Protocols (Restoration additions)
            type_hint_violations = self._check_missing_type_hints(tree, file_path)
            complexity_violations.extend(type_hint_violations)

            emoji_violations = self._check_prohibited_patterns(content, file_path)
            architectural_violations.extend(emoji_violations)

        except SyntaxError as e:
            broken_imports.append(f"Syntax error: {e}")
        except Exception as e:
            broken_imports.append(f"Analysis error: {e}")

        return SentinelReport(
            broken_imports=broken_imports,
            complexity_violations=complexity_violations,
            dead_code=dead_code,
            architectural_violations=architectural_violations,
            security_violations=[],  # Bandit is run separately via run_bandit_scan
        )

    def _check_imports(self, tree: ast.AST, file_path: Path, project_root: Path) -> list[str]:
        """
        Check for broken or restricted imports.

        Args:
            tree: AST tree
            file_path: File being analyzed
            project_root: Project root

        Returns:
            List of import errors
        """
        errors = []
        imports = []

        # Extract all imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        # Check for restricted imports
        for imp in imports:
            for restricted in self.restricted_imports:
                if restricted in imp:
                    errors.append(f"Restricted import detected: {imp}")

        # Check for external API dependencies (constitution violation)
        external_apis = {
            "openai": "OpenAI API requires OPENAI_API_KEY - use Ollama/LiteLLM for local-first",
            "anthropic": "Anthropic API requires API key - use Ollama for local-first",
            "google.generativeai": "Google AI requires API key - use Ollama for local-first",
        }

        for imp in imports:
            if imp in external_apis:
                errors.append(f"CONSTITUTION VIOLATION: {external_apis[imp]}")

        return errors

    def _check_complexity(self, tree: ast.AST, file_path: Path) -> list[str]:
        """
        Check cyclomatic complexity of functions.

        Args:
            tree: AST tree
            file_path: File being analyzed

        Returns:
            List of complexity violations
        """
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > self.max_complexity:
                    violations.append(
                        f"{file_path.name}:{node.lineno} - Function '{node.name}' "
                        f"has complexity {complexity} (max: {self.max_complexity})"
                    )

        return violations

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """
        Calculate cyclomatic complexity of a function.

        Args:
            node: Function definition node

        Returns:
            Complexity score
        """
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            # Count decision points
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)) or isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _check_dead_code(self, tree: ast.AST, file_path: Path) -> list[str]:
        """
        Check for dead code (unreachable statements).

        Args:
            tree: AST tree
            file_path: File being analyzed

        Returns:
            List of dead code warnings
        """
        dead_code = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for unreachable code after return statements
                has_return = False
                for stmt in node.body:
                    if isinstance(stmt, ast.Return) and has_return:
                        # Code after return is dead
                        dead_code.append(
                            f"{file_path.name}:{stmt.lineno} - "
                            f"Unreachable code after return in '{node.name}'"
                        )
                    if isinstance(stmt, ast.Return):
                        has_return = True

        return dead_code

    def _check_architectural_violations(self, tree: ast.AST, file_path: Path, project_root: Path) -> list[str]:
        """
        Check for architectural violations (e.g., importing from legacy in new core).

        Args:
            tree: AST tree
            file_path: File being analyzed
            project_root: Project root

        Returns:
            List of architectural violations
        """
        violations = []

        # Check if file is in new core (src/ybis)
        file_str = str(file_path)
        is_new_core = "src/ybis" in file_str

        if is_new_core:
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        # Check if importing from legacy
                        for legacy_path in self.legacy_paths:
                            if legacy_path.replace("/", ".") in node.module or legacy_path in node.module:
                                violations.append(
                                    f"{file_path.name}:{node.lineno} - "
                                    f"Architectural violation: Importing from legacy '{node.module}' "
                                    f"in new core code"
                                )

        return violations

    def _check_sensitive_env_exposure(self, tree: ast.AST, file_path: Path) -> list[str]:
        """Detect explicit environment variable dumping via subprocess or os.environ."""
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if self._is_subprocess_run(node) and self._call_uses_env_command(node):
                    violations.append(
                        f"{file_path.name}:{node.lineno} - SECURITY: subprocess.run('env') exposes environment variables"
                    )
                if self._is_os_system(node) and self._call_uses_env_command(node):
                    violations.append(
                        f"{file_path.name}:{node.lineno} - SECURITY: os.system('env') exposes environment variables"
                    )
                if self._prints_os_environ(node):
                    violations.append(
                        f"{file_path.name}:{node.lineno} - SECURITY: printing os.environ exposes environment variables"
                    )
            if self._uses_os_environ(node):
                violations.append(
                    f"{file_path.name}:{node.lineno} - SECURITY: os.environ access exposes environment variables"
                )

        return violations

    def _is_subprocess_run(self, node: ast.Call) -> bool:
        func = node.func
        return (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "subprocess"
            and func.attr == "run"
        )

    def _is_os_system(self, node: ast.Call) -> bool:
        func = node.func
        return (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "os"
            and func.attr == "system"
        )

    def _call_uses_env_command(self, node: ast.Call) -> bool:
        for arg in node.args:
            if isinstance(arg, ast.Constant) and arg.value == "env":
                return True
            if isinstance(arg, (ast.List, ast.Tuple)):
                for elt in arg.elts:
                    if isinstance(elt, ast.Constant) and elt.value == "env":
                        return True
        return False

    def _prints_os_environ(self, node: ast.Call) -> bool:
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "print"):
            return False
        for arg in node.args:
            if (
                isinstance(arg, ast.Attribute)
                and isinstance(arg.value, ast.Name)
                and arg.value.id == "os"
                and arg.attr == "environ"
            ):
                return True
        return False

    def _check_missing_type_hints(self, tree: ast.AST, file_path: Path) -> list[str]:
        """Verify that all function definitions have type hints for arguments and return values."""
        violations = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip __init__ return hint as it's often omitted, but check args
                if not node.returns and node.name != "__init__":
                    violations.append(
                        f"{file_path.name}:{node.lineno} - Missing return type hint in function '{node.name}'"
                    )

                # Check arguments (except 'self' and 'cls')
                for arg in node.args.args:
                    if arg.arg in ("self", "cls"):
                        continue
                    if not arg.annotation:
                        violations.append(
                            f"{file_path.name}:{node.lineno} - Missing type hint for argument '{arg.arg}' in function '{node.name}'"
                        )
        return violations

    def _check_prohibited_patterns(self, content: str, file_path: Path) -> list[str]:
        """Bans emojis and other non-industrial patterns in code/comments."""
        violations = []
        # Check for emojis (Basic range check)
        emoji_pattern = re.compile(r"[\U00010000-\U0010ffff]", flags=re.UNICODE)
        if emoji_pattern.search(content):
            violations.append(
                f"{file_path.name} - CONSTITUTION VIOLATION: Emojis are prohibited in industrial codebases. Use clear text."
            )

        # Check for placeholder strings
        placeholders = ["TODO: TASK-", "FIXME: AGENT", "PLACEHOLDER"]
        for p in placeholders:
            if p in content:
                 violations.append(f"{file_path.name} - PROHIBITED: Found persistent placeholder '{p}'")

        return violations

    def _uses_os_environ(self, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "os"
            and node.attr == "environ"
        )

    @staticmethod
    def run_bandit_scan(project_root: Path, target_path: Path | None = None) -> list[str]:
        """
        Run Bandit security scanner and return high-severity vulnerabilities.

        Args:
            project_root: Project root directory
            target_path: Optional specific path to scan (defaults to project root)

        Returns:
            List of high-severity security violations
        """
        violations = []
        scan_target = Path(target_path) if target_path else project_root
        if not scan_target.exists():
            return violations

        scan_path = str(scan_target)

        try:
            # Run bandit with JSON output
            if scan_target.is_file():
                command = ["bandit", "-f", "json", "-ll", scan_path]
            else:
                command = ["bandit", "-r", scan_path, "-f", "json", "-ll"]  # -ll = low and medium severity

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=str(project_root),
                timeout=60,  # 60 second timeout
            )

            if result.stdout:
                try:
                    bandit_data = json.loads(result.stdout)
                    # Check for high-severity issues
                    high_severity_codes = ["B601", "B602", "B307", "B104"]  # eval, exec, shell injection, hardcoded secrets
                    for result_item in bandit_data.get("results", []):
                        test_id = result_item.get("test_id", "")
                        severity = result_item.get("issue_severity", "").upper()
                        confidence = result_item.get("issue_confidence", "").upper()

                        # Block on HIGH severity or specific dangerous patterns
                        if severity == "HIGH" or test_id in high_severity_codes:
                            file_path = result_item.get("filename", "unknown")
                            line_num = result_item.get("line_number", 0)
                            issue_text = result_item.get("issue_text", "")
                            violations.append(
                                f"SECURITY: {file_path}:{line_num} - {test_id} - {issue_text} "
                                f"(Severity: {severity}, Confidence: {confidence})"
                            )
                except json.JSONDecodeError:
                    # If JSON parsing fails, check stderr for errors
                    if result.stderr:
                        violations.append(f"Bandit execution error: {result.stderr[:200]}")
            elif result.returncode != 0 and result.stderr:
                violations.append(f"Bandit execution error: {result.stderr[:200]}")
        except FileNotFoundError:
            # Bandit not installed, skip silently (optional dependency)
            pass
        except subprocess.TimeoutExpired:
            violations.append("Bandit scan timed out (>60s)")
        except Exception as e:
            violations.append(f"Bandit scan error: {e!s}")

        return violations

