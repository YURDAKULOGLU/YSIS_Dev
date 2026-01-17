How to run Prefect on Windows - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Self-hosted

How to run Prefect on Windows

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

* [Overview](/v3/how-to-guides)

##### Workflows

* [Write and run a workflow](/v3/how-to-guides/workflows/write-and-run)
* [Use assets to track workflow outputs](/v3/how-to-guides/workflows/assets)
* [Automatically rerun a workflow when it fails](/v3/how-to-guides/workflows/retries)
* [Manually retry a flow run](/v3/how-to-guides/workflows/retry-flow-runs)
* [Customize workflow metadata](/v3/how-to-guides/workflows/custom-metadata)
* [Pass inputs to a workflow](/v3/how-to-guides/workflows/pass-inputs)
* [Add logging](/v3/how-to-guides/workflows/add-logging)
* [Access runtime information](/v3/how-to-guides/workflows/access-runtime-info)
* [Run work concurrently](/v3/how-to-guides/workflows/run-work-concurrently)
* [Cache workflow step outputs](/v3/how-to-guides/workflows/cache-workflow-steps)
* [Run background tasks](/v3/how-to-guides/workflows/run-background-tasks)
* [Respond to state changes](/v3/how-to-guides/workflows/state-change-hooks)
* [Create Artifacts](/v3/how-to-guides/workflows/artifacts)
* [Test workflows](/v3/how-to-guides/workflows/test-workflows)
* [Apply global concurrency and rate limits](/v3/how-to-guides/workflows/global-concurrency-limits)
* [Limit concurrent task runs with tags](/v3/how-to-guides/workflows/tag-based-concurrency-limits)

##### Deployments

* [Create Deployments](/v3/how-to-guides/deployments/create-deployments)
* [Trigger ad-hoc deployment runs](/v3/how-to-guides/deployments/run-deployments)
* [Create Deployment Schedules](/v3/how-to-guides/deployments/create-schedules)
* [Manage Deployment schedules](/v3/how-to-guides/deployments/manage-schedules)
* [Deploy via Python](/v3/how-to-guides/deployments/deploy-via-python)
* [Define deployments with YAML](/v3/how-to-guides/deployments/prefect-yaml)
* [Retrieve code from storage](/v3/how-to-guides/deployments/store-flow-code)
* [Version Deployments](/v3/how-to-guides/deployments/versioning)
* [Override Job Configuration](/v3/how-to-guides/deployments/customize-job-variables)

##### Configuration

* [Store secrets](/v3/how-to-guides/configuration/store-secrets)
* [Share configuration between workflows](/v3/how-to-guides/configuration/variables)
* [Manage settings](/v3/how-to-guides/configuration/manage-settings)

##### Automations

* [Create Automations](/v3/how-to-guides/automations/creating-automations)
* [Create Deployment Triggers](/v3/how-to-guides/automations/creating-deployment-triggers)
* [Chain Deployments with Events](/v3/how-to-guides/automations/chaining-deployments-with-events)
* [Access parameters in templates](/v3/how-to-guides/automations/access-parameters-in-templates)
* [Pass event payloads to flows](/v3/how-to-guides/automations/passing-event-payloads-to-flows)

##### Workflow Infrastructure

* [Manage Work Pools](/v3/how-to-guides/deployment_infra/manage-work-pools)
* [Run Flows in Local Processes](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes)
* [Run flows on Prefect Managed infrastructure](/v3/how-to-guides/deployment_infra/managed)
* [Run flows on serverless compute](/v3/how-to-guides/deployment_infra/serverless)
* [Run flows in Docker containers](/v3/how-to-guides/deployment_infra/docker)
* [Run flows in a static container](/v3/how-to-guides/deployment_infra/serve-flows-docker)
* [Run flows on Kubernetes](/v3/how-to-guides/deployment_infra/kubernetes)
* [Run flows on Modal](/v3/how-to-guides/deployment_infra/modal)
* [Run flows on Coiled](/v3/how-to-guides/deployment_infra/coiled)

##### Prefect Cloud

* [Connect to Prefect Cloud](/v3/how-to-guides/cloud/connect-to-cloud)
* Manage accounts
* [Manage Workspaces](/v3/how-to-guides/cloud/workspaces)
* [Create a Webhook](/v3/how-to-guides/cloud/create-a-webhook)
* [Troubleshoot Prefect Cloud](/v3/how-to-guides/cloud/troubleshoot-cloud)

##### Prefect Self-hosted

* [Run a local Prefect server](/v3/how-to-guides/self-hosted/server-cli)
* [Run the Prefect server in Docker](/v3/how-to-guides/self-hosted/server-docker)
* [Run Prefect on Windows](/v3/how-to-guides/self-hosted/server-windows)
* [Run the Prefect Server via Docker Compose](/v3/how-to-guides/self-hosted/docker-compose)

##### AI

* [Use the Prefect MCP server](/v3/how-to-guides/ai/use-prefect-mcp-server)

##### Migrate

* [Migrate from Airflow](/v3/how-to-guides/migrate/airflow)
* [Upgrade to Prefect 3.0](/v3/how-to-guides/migrate/upgrade-to-prefect-3)
* [Upgrade from agents to workers](/v3/how-to-guides/migrate/upgrade-agents-to-workers)
* [Transfer resources between environments](/v3/how-to-guides/migrate/transfer-resources)

On this page

* [Windows support](#windows-support)
* [Database configuration and workers](#database-configuration-and-workers)
* [Security and performance considerations](#security-and-performance-considerations)
* [Production deployment as Windows service](#production-deployment-as-windows-service)
* [Troubleshooting common Windows issues](#troubleshooting-common-windows-issues)
* [Command not found errors](#command-not-found-errors)
* [Port conflicts](#port-conflicts)
* [Character encoding errors](#character-encoding-errors)
* [Permission errors](#permission-errors)
* [Additional Resources](#additional-resources)

Prefect provides first-class Windows support with native PowerShell integration and full feature parity with other platforms. This guide covers Windows-specific setup and best practices.

## [​](#windows-support) Windows support

Prefect provides comprehensive Windows support with the Windows ecosystem. Prefect automatically detects PowerShell and uses it as the default shell on Windows, allowing you to run shell commands and scripts naturally without additional configuration. The subprocess execution is fully compatible with Windows process management.
Windows path conventions are fully supported, including UNC paths for network storage. This allows you to configure Prefect to use network shares for databases, storage, and other resources, which is particularly useful in enterprise environments where shared storage is common:

Copy

```
# Configure database on network share using UNC paths
prefect config set PREFECT_HOME="\\server\share\prefect-data"

# Or use mapped drives
prefect config set PREFECT_HOME="Z:\prefect-data"

# Standard Windows paths work as expected
prefect config set PREFECT_HOME="C:\ProgramData\Prefect"
```

Environment variables work using standard Windows conventions and can be set using PowerShell syntax, either for the current session or permanently for the user:

Copy

```
# Set for current session
$env:PREFECT_API_DATABASE_TIMEOUT = "600"

# Set permanently for user
[System.Environment]::SetEnvironmentVariable("PREFECT_API_DATABASE_TIMEOUT", "600", "User")
```

Shell tasks automatically use PowerShell on Windows, providing access to the full Windows command ecosystem:

Copy

```
from prefect import flow
from prefect_shell import shell_run_command

@flow
def windows_flow():
    # This will run in PowerShell by default on Windows
    result = shell_run_command(command="Get-Process prefect")
    return result
```

## [​](#database-configuration-and-workers) Database configuration and workers

By default, Prefect uses SQLite stored at `%USERPROFILE%\.prefect\prefect.db` with no additional configuration needed. For production deployments, you can configure PostgreSQL using standard connection strings:

Copy

```
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:password@localhost:5432/prefect"
```

Prefect workers on Windows support both process execution and Docker containers. Process workers run flows directly as Windows processes. Docker workers can leverage Windows containers for isolated execution environments:

Copy

```
# Run flows as Windows processes
prefect worker start --pool my-process-pool --type process

# Use Windows containers with Docker Desktop
docker pull mcr.microsoft.com/windows/servercore:ltsc2019
prefect worker start --pool my-docker-pool --type docker
```

## [​](#security-and-performance-considerations) Security and performance considerations

Windows environments require specific security configurations for optimal Prefect operation. You’ll need to allow Prefect server through Windows Firewall and configure PowerShell execution policies. Additionally, antivirus software can significantly impact performance if not configured properly.
Configure Windows Firewall to allow Prefect server traffic on port 4200:

Copy

```
# Run as Administrator
New-NetFirewallRule -DisplayName "Prefect Server" -Direction Inbound -Port 4200 -Protocol TCP -Action Allow
```

If you encounter PowerShell execution policy errors when running scripts or deployments, configure the execution policy for the current user:

Copy

```
# Set execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

For better performance, consider adding these directories to your antivirus exclusions: `%USERPROFILE%\.prefect\`, your Python installation directory, and temporary directories used by flows. This prevents real-time scanning from interfering with Prefect operations.

## [​](#production-deployment-as-windows-service) Production deployment as Windows service

For production environments, you should run Prefect server as a Windows service to ensure it starts automatically and runs reliably. The Non-Sucking Service Manager (NSSM) is the recommended tool for this purpose. Download NSSM from [nssm.cc](https://nssm.cc) and install the service with administrator privileges:

Copy

```
# Run as Administrator
nssm install PrefectServer
nssm set PrefectServer Application "C:\Path\To\Python\python.exe"
nssm set PrefectServer AppParameters "-m prefect server start"
nssm set PrefectServer AppDirectory "C:\Path\To\Your\Project"

# Set environment variables if needed
nssm set PrefectServer AppEnvironmentExtra "PREFECT_API_URL=http://localhost:4200/api"

nssm start PrefectServer
```

This configuration ensures Prefect server starts automatically when Windows boots and provides proper service management capabilities including automatic restarts on failure.

## [​](#troubleshooting-common-windows-issues) Troubleshooting common Windows issues

Several Windows-specific issues can occur when running Prefect. The most common problems relate to PATH configuration, encoding issues, port conflicts, and permission errors.

### [​](#command-not-found-errors) Command not found errors

These typically indicate PATH issues. Verify that the Python Scripts directory is in your PATH and restart PowerShell after making changes. You can also try running `where prefect` to see if the command is found.
For example, if the `prefect` command isn’t found, you’ll need to add the Python Scripts directory to your `PATH`. This is a common issue on Windows when Python isn’t installed system-wide:

Copy

```
# Check if Scripts directory is in PATH
$env:PATH -split ';' | Select-String "Scripts"

# Add Scripts directory to PATH (replace with your Python path)
$scriptsPath = "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python39\Scripts"
$env:PATH += ";$scriptsPath"
```

### [​](#port-conflicts) Port conflicts

These can prevent the server from starting. Check what’s using port 4200 and kill the process if necessary:

Copy

```
# Check what's using port 4200
netstat -ano | findstr :4200

# Kill process if needed (replace PID with actual process ID)
taskkill /PID 1234 /F
```

Alternatively, you can configure Prefect server to use a different port by setting the `PREFECT_SERVER_API_HOST` and `PREFECT_SERVER_API_PORT` environment variables:

Copy

```
# Set server to use port 8080 instead of 4200
$env:PREFECT_SERVER_API_PORT = "8080"
prefect server start

# Update client configuration to match
prefect config set PREFECT_API_URL="http://127.0.0.1:8080/api"
```

### [​](#character-encoding-errors) Character encoding errors

Character encoding errors (particularly `'charmap' codec` errors) can occur on some Windows systems. Set the Python I/O encoding to UTF-8:

Copy

```
$env:PYTHONIOENCODING = "UTF-8"
```

### [​](#permission-errors) Permission errors

Permission errors often require running PowerShell as Administrator for system-wide changes, or checking file permissions on Prefect directories. Network connectivity issues typically involve Windows Firewall rules or corporate proxy settings.

## [​](#additional-resources) Additional Resources

For additional help with Windows-specific issues, check the [Prefect Community Slack](https://prefect.io/slack), search [GitHub Issues](https://github.com/PrefectHQ/prefect/issues) for Windows-related problems, or review PowerShell execution logs for detailed error messages.

Was this page helpful?

YesNo

[Run the Prefect server in Docker](/v3/how-to-guides/self-hosted/server-docker)[Run the Prefect Server via Docker Compose](/v3/how-to-guides/self-hosted/docker-compose)

⌘I