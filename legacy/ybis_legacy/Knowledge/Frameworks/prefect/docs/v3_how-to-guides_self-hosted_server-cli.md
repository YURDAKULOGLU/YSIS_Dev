How to run a local Prefect server - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Self-hosted

How to run a local Prefect server

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

* [Start the server](#start-the-server)
* [Configure the server](#configure-the-server)
* [Database configuration](#database-configuration)
* [Use SQLite (default)](#use-sqlite-default)
* [Use PostgreSQL](#use-postgresql)
* [Database management commands](#database-management-commands)
* [Reset the database](#reset-the-database)
* [Manage migrations](#manage-migrations)
* [Multi-worker API server](#multi-worker-api-server)
* [Requirements for multi-worker mode](#requirements-for-multi-worker-mode)
* [Configuration example](#configuration-example)
* [Advanced configuration](#advanced-configuration)

The [Prefect CLI](/v3/get-started/install) is the easiest way to start a local instance of Prefect server.

## [​](#start-the-server) Start the server

1. Spin up a self-hosted Prefect server instance UI with the `prefect server start` CLI command in the terminal:

Copy

```
prefect server start
```

2. Open the URL for the Prefect server UI (<http://127.0.0.1:4200> by default) in a browser.

![Viewing the dashboard in the Prefect UI.](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/self-hosted-server-dashboard.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=455fc524a4713d0a15710471edc5ca63)

3. Shut down the Prefect server with ctrl + c in the terminal.

## [​](#configure-the-server) Configure the server

Go to your terminal session and run this command to set the API URL to point to a self-hosted Prefect server instance:

Copy

```
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
```

You can save the API server address in a Prefect profile.
Whenever that profile is active, the API endpoint is at that address.
See [Profiles and configuration](/v3/develop/settings-and-profiles) for more information on profiles and configurable Prefect settings.

## [​](#database-configuration) Database configuration

### [​](#use-sqlite-default) Use SQLite (default)

By default, Prefect uses a SQLite database stored at `~/.prefect/prefect.db`. No additional configuration is needed for basic use.

### [​](#use-postgresql) Use PostgreSQL

To use PostgreSQL as your database backend:

1. Set the database connection URL:

Copy

```
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:yourTopSecretPassword@localhost:5432/prefect"
```

2. Start the server:

Copy

```
prefect server start
```

For more database configuration options, see the [database settings reference](/v3/api-ref/settings-ref#database).

## [​](#database-management-commands) Database management commands

### [​](#reset-the-database) Reset the database

Clear all data and reapply the schema:

Copy

```
prefect server database reset -y
```

### [​](#manage-migrations) Manage migrations

Apply database migrations:

Copy

```
# Upgrade to the latest version
prefect server database upgrade -y

# Downgrade to the previous version
prefect server database downgrade -y -r -1

# Downgrade to a specific revision
prefect server database downgrade -y -r d20618ce678e
```

For large databases, you may need to increase the timeout:

Copy

```
export PREFECT_API_DATABASE_TIMEOUT=600
prefect server database upgrade -y
```

## [​](#multi-worker-api-server) Multi-worker API server

For high-throughput scenarios, you can run the server with multiple worker processes to handle concurrent requests more efficiently:

Copy

```
prefect server start --workers 4
```

This starts 4 worker processes to handle API and UI requests concurrently.

### [​](#requirements-for-multi-worker-mode) Requirements for multi-worker mode

Multi-worker mode has specific infrastructure requirements:

1. **PostgreSQL database** - SQLite is not supported due to database locking issues
2. **Redis messaging** - In-memory messaging doesn’t work across processes

### [​](#configuration-example) Configuration example

Copy

```
# Set PostgreSQL connection
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:password@localhost:5432/prefect"

# Configure Redis messaging
prefect config set PREFECT_SERVER_EVENTS_MESSAGING_CACHE="prefect.server.utilities.messaging.redis"
prefect config set PREFECT_SERVER_EVENTS_MESSAGING_BROKER="prefect.server.utilities.messaging.redis"

# Configure Redis messaging host and port
export PREFECT_REDIS_MESSAGING_HOST="redis"
export PREFECT_REDIS_MESSAGING_PORT="6379"

# Start server with 4 workers
prefect server start --workers 4
```

The number of workers should typically match the number of CPU cores available to your server process, but you may need to experiment to find the optimal value for your workload.

## [​](#advanced-configuration) Advanced configuration

For advanced deployment scenarios including:

* Running behind a reverse proxy
* Configuring SSL certificates
* Multi-server deployments
* Handling migration issues

See [How to scale self-hosted Prefect](/v3/advanced/self-hosted).

Was this page helpful?

YesNo

[Troubleshoot Prefect Cloud](/v3/how-to-guides/cloud/troubleshoot-cloud)[Run the Prefect server in Docker](/v3/how-to-guides/self-hosted/server-docker)

⌘I