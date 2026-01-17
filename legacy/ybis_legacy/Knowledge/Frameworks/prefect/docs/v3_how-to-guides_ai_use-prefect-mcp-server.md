How to use the Prefect MCP server - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

AI

How to use the Prefect MCP server

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

* [What is the Prefect MCP server?](#what-is-the-prefect-mcp-server)
* [Security considerations](#security-considerations)
* [Installation](#installation)
* [Local installation](#local-installation)
* [Cloud deployment](#cloud-deployment)
* [Client setup](#client-setup)
* [General setup](#general-setup)
* [Credentials configuration](#credentials-configuration)
* [Default behavior](#default-behavior)
* [Environment variables](#environment-variables)
* [Credential precedence](#credential-precedence)
* [Available capabilities](#available-capabilities)
* [Monitoring & inspection](#monitoring-%26-inspection)
* [Orchestration & actions](#orchestration-%26-actions)
* [Intelligent debugging](#intelligent-debugging)
* [Documentation access](#documentation-access)
* [Prompting tips](#prompting-tips)
* [Use the prefect CLI for write operations](#use-the-prefect-cli-for-write-operations)
* [Leverage the docs proxy](#leverage-the-docs-proxy)
* [Ask diagnostic questions](#ask-diagnostic-questions)
* [Learn more](#learn-more)

The Prefect MCP server enables AI assistants to interact with your Prefect workflows and infrastructure through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). This integration allows AI tools like Claude Code, Cursor, and Codex CLI to help you monitor deployments, debug flow runs, query infrastructure, and more.

The Prefect MCP server is currently in beta. APIs, features, and behaviors may change without notice. We encourage you to try it out and provide feedback through [GitHub issues](https://github.com/PrefectHQ/prefect-mcp-server/issues).

## [​](#what-is-the-prefect-mcp-server) What is the Prefect MCP server?

The Prefect MCP server is an [MCP](https://modelcontextprotocol.io/) server that provides AI assistants with tools to:

* **Monitor & inspect**: View system health, query deployments, flow runs, task runs, work pools, and execution logs
* **Debug intelligently**: Get contextual guidance for troubleshooting failed flows and deployment issues
* **Access documentation**: Query up-to-date Prefect documentation through an integrated docs proxy

The MCP tools are primarily designed for reading data and monitoring your Prefect instance. For creating or updating resources, the integrated docs proxy provides AI assistants with current information on how to use the `prefect` CLI.

## [​](#security-considerations) Security considerations

The Prefect MCP server provides **read-only access** to your Prefect instance. It can only access information available to the account you authenticate with—it cannot access data outside those bounds.

**Important:** The MCP server does not operate in isolation. MCP clients (such as Claude Code, Cursor, or Codex CLI) may have additional capabilities beyond the MCP server’s read-only tools. For example, an AI assistant with terminal access could execute destructive CLI commands like `prefect deployment delete` independently of the MCP server.When using AI agents autonomously, consider the Prefect Role associated with your API key and what actions the agent could take through other means (CLI, SDK, etc.).

## [​](#installation) Installation

### [​](#local-installation) Local installation

Install and run the MCP server locally using `uvx`:

Copy

```
uvx --from prefect-mcp prefect-mcp-server
```

When running locally with stdio transport, the server automatically inherits credentials from your active Prefect profile (`~/.prefect/profiles.toml`).

### [​](#cloud-deployment) Cloud deployment

Deploy the MCP server to [FastMCP Cloud](https://fastmcp.cloud) for remote access:

1. Fork the [prefect-mcp-server repository](https://github.com/PrefectHQ/prefect-mcp-server) on GitHub
2. Sign in to [fastmcp.cloud](https://fastmcp.cloud)
3. Create a new server pointing to your fork:
   * Server path: `src/prefect_mcp_server/server.py`
   * Requirements: `pyproject.toml` (or leave blank)
4. Configure environment variables in the FastMCP Cloud interface:

   | Environment Variable | Prefect Cloud | Self-hosted Prefect |
   | --- | --- | --- |
   | `PREFECT_API_URL` | `https://api.prefect.cloud/api/` `accounts/[ACCOUNT_ID]/` `workspaces/[WORKSPACE_ID]` | Your Prefect server URL (e.g., `http://your-server:4200/api`) |
   | `PREFECT_API_KEY` | Your Prefect Cloud API key | Not used |
   | `PREFECT_API_AUTH_STRING` | Not used | Your authentication string (if using basic auth) |
5. Get your server URL (e.g., `https://your-server-name.fastmcp.app/mcp`)

When deploying to FastMCP Cloud, environment variables are configured on the FastMCP Cloud server itself (step 4 above), not in your client configuration. FastMCP’s authentication secures access to your MCP server, while the MCP server uses your Prefect API key to access your Prefect instance.

Prefect Cloud users on Team, Pro, and Enterprise plans can use service accounts for API authentication. Pro and Enterprise users can restrict service accounts to read-only access (only `see_*` permissions) since the Prefect MCP server requires no write permissions.

## [​](#client-setup) Client setup

Configure your AI assistant to connect to the Prefect MCP server.

### [​](#general-setup) General setup

All MCP clients need three pieces of information to connect to the Prefect MCP server:

1. **Command**: `uvx`
2. **Arguments**: `--from prefect-mcp prefect-mcp-server`
3. **Environment variables** (optional): Credentials for your Prefect instance

The configuration format varies by client. Choose your client below for specific setup instructions:

Claude Code

Add the Prefect MCP server to Claude Code using the CLI:

Copy

```
# Minimal setup - inherits from local Prefect profile
claude mcp add prefect -- uvx --from prefect-mcp prefect-mcp-server

# With explicit Prefect Cloud credentials
claude mcp add prefect \
  -e PREFECT_API_URL=https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID] \
  -e PREFECT_API_KEY=your-cloud-api-key \
  -- uvx --from prefect-mcp prefect-mcp-server

# With FastMCP Cloud deployment (HTTP transport)
claude mcp add prefect --transport http https://your-server-name.fastmcp.app/mcp
```

Cursor

Add the Prefect MCP server to Cursor by creating or editing `.cursor/mcp.json` in your project:

Copy

```
{
  "mcpServers": {
    "prefect": {
      "command": "uvx",
      "args": ["--from", "prefect-mcp", "prefect-mcp-server"]
    }
  }
}
```

To use explicit credentials, add an `env` section:

Copy

```
{
  "mcpServers": {
    "prefect": {
      "command": "uvx",
      "args": ["--from", "prefect-mcp", "prefect-mcp-server"],
      "env": {
        "PREFECT_API_URL": "https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID]",
        "PREFECT_API_KEY": "your-cloud-api-key"
      }
    }
  }
}
```

Codex CLI

Add the Prefect MCP server to Codex using the CLI:

Copy

```
# Minimal setup - inherits from local Prefect profile
codex mcp add prefect -- uvx --from prefect-mcp prefect-mcp-server

# With explicit Prefect Cloud credentials
codex mcp add prefect \
  --env PREFECT_API_URL=https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID] \
  --env PREFECT_API_KEY=your-cloud-api-key \
  -- uvx --from prefect-mcp prefect-mcp-server
```

Alternatively, edit `~/.codex/config.toml` directly:

Copy

```
[mcp.prefect]
command = "uvx"
args = ["--from", "prefect-mcp", "prefect-mcp-server"]

# For explicit credentials, add:
[mcp.prefect.env]
PREFECT_API_URL = "https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID]"
PREFECT_API_KEY = "your-cloud-api-key"
```

Gemini CLI

Add the Prefect MCP server to Gemini CLI using the CLI:

Copy

```
# STDIO transport - runs locally with uvx
gemini mcp add prefect uvx --from prefect-mcp prefect-mcp-server

# With explicit Prefect Cloud credentials
gemini mcp add prefect \
  -e PREFECT_API_URL=https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID] \
  -e PREFECT_API_KEY=your-cloud-api-key \
  uvx --from prefect-mcp prefect-mcp-server

# HTTP transport - for FastMCP Cloud deployment
gemini mcp add prefect --transport http https://your-server-name.fastmcp.app/mcp
```

Alternatively, edit `~/.gemini/settings.json` directly:**For STDIO transport (local):**

Copy

```
{
  "mcpServers": {
    "prefect": {
      "command": "uvx",
      "args": ["--from", "prefect-mcp", "prefect-mcp-server"]
    }
  }
}
```

**For STDIO transport with explicit credentials:**

Copy

```
{
  "mcpServers": {
    "prefect": {
      "command": "uvx",
      "args": ["--from", "prefect-mcp", "prefect-mcp-server"],
      "env": {
        "PREFECT_API_URL": "https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID]",
        "PREFECT_API_KEY": "your-cloud-api-key"
      }
    }
  }
}
```

**For HTTP transport (FastMCP Cloud):**

Copy

```
{
  "mcpServers": {
    "prefect": {
      "httpUrl": "https://your-server-name.fastmcp.app/mcp"
    }
  }
}
```

## [​](#credentials-configuration) Credentials configuration

The Prefect MCP server authenticates with your Prefect instance using the same configuration as the Prefect SDK.

### [​](#default-behavior) Default behavior

When running locally without environment variables, the server inherits credentials from your active Prefect profile:

* Profile configuration: `~/.prefect/profiles.toml`
* Uses the same API URL and authentication as your current `prefect` CLI commands

### [​](#environment-variables) Environment variables

Override the default credentials by setting environment variables:
**For Prefect Cloud:**

Copy

```
PREFECT_API_URL=https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID]
PREFECT_API_KEY=your-cloud-api-key
```

**For self-hosted Prefect with basic auth:**

Copy

```
PREFECT_API_URL=http://your-server:4200/api
PREFECT_API_AUTH_STRING=your-auth-string
```

Find your account ID and workspace ID in your Prefect Cloud browser URL:`https://app.prefect.cloud/account/[ACCOUNT-ID]/workspace/[WORKSPACE-ID]/dashboard`

### [​](#credential-precedence) Credential precedence

Environment variables take precedence over profile settings:

1. Environment variables (`PREFECT_API_URL`, `PREFECT_API_KEY`)
2. Active Prefect profile (`~/.prefect/profiles.toml`)

## [​](#available-capabilities) Available capabilities

The Prefect MCP server provides these main capabilities:

### [​](#monitoring-&-inspection) Monitoring & inspection

* View dashboard overviews with flow run statistics and work pool status
* Query deployments, flow runs, task runs, and work pools with advanced filtering
* Retrieve detailed execution logs from flow runs
* Track events across your workflow ecosystem
* Review automations and their configurations

### [​](#orchestration-&-actions) Orchestration & actions

* Trigger deployment runs with custom parameters and tags
* Pass dynamic configurations to workflows at runtime

### [​](#intelligent-debugging) Intelligent debugging

* Get contextual guidance for troubleshooting failed flow runs
* Diagnose deployment issues including concurrency problems
* Identify root causes of workflow failures
* Analyze rate limiting issues (Prefect Cloud only)

### [​](#documentation-access) Documentation access

The MCP server includes a built-in docs proxy that provides AI assistants with up-to-date information from the Prefect documentation. This enables your AI assistant to:

* Look up current API syntax and usage patterns
* Find the correct `prefect` CLI commands for creating and updating resources
* Access the latest best practices and examples

## [​](#prompting-tips) Prompting tips

To get the most out of the Prefect MCP server, guide your AI assistant with these patterns:

### [​](#use-the-prefect-cli-for-write-operations) Use the prefect CLI for write operations

The MCP tools are optimized for reading and monitoring. For creating or updating resources, prompt your assistant to use the `prefect` CLI:
**Example prompts:**

* “Use the `prefect` CLI to create a new deployment”
* “Show me how to update this deployment’s schedule using `prefect`”
* “Create an automation using the `prefect` CLI”

### [​](#leverage-the-docs-proxy) Leverage the docs proxy

The integrated docs proxy gives your assistant access to current Prefect documentation:
**Example prompts:**

* “Look up the latest syntax for creating a work pool”
* “Find documentation on how to configure Docker work pools”
* “What are the current best practices for deployment configuration?”

### [​](#ask-diagnostic-questions) Ask diagnostic questions

The MCP server excels at helping diagnose issues:
**Example prompts:**

* “Why is my deployment not running?”
* “Debug the last failed flow run”
* “Why are my flow runs delayed?”
* “Show me which work pools have no active workers”

## [​](#learn-more) Learn more

* [Prefect MCP Server on GitHub](https://github.com/PrefectHQ/prefect-mcp-server)
* [Model Context Protocol](https://modelcontextprotocol.io/)
* [FastMCP Cloud](https://fastmcp.cloud)

Was this page helpful?

YesNo

[Run the Prefect Server via Docker Compose](/v3/how-to-guides/self-hosted/docker-compose)[Migrate from Airflow](/v3/how-to-guides/migrate/airflow)

⌘I