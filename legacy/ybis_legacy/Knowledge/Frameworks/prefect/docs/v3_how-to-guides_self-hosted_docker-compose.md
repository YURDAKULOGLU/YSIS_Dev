How to run the Prefect Server via Docker Compose - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Self-hosted

How to run the Prefect Server via Docker Compose

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

* [Docker Compose file](#docker-compose-file)
* [Running the stack](#running-the-stack)
* [Notes](#notes)
* [Troubleshooting](#troubleshooting)

This guide shows how to run a complete self-hosted Prefect server environment using Docker Compose. This setup includes the following services:

* `postgres`: PostgreSQL database
* `redis`: Redis message broker
* `prefect-server`: Prefect server
* `prefect-services`: Prefect background services
* `prefect-worker`: Prefect worker

## [​](#docker-compose-file) Docker Compose file

Create a `compose.yml` file with the following contents:

Copy

```
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: prefect
      POSTGRES_PASSWORD: prefect
      POSTGRES_DB: prefect
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U prefect"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD-SHELL", "redis-cli ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  prefect-server:
    image: prefecthq/prefect:3-latest
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      PREFECT_API_DATABASE_CONNECTION_URL: postgresql+asyncpg://prefect:prefect@postgres:5432/prefect
      PREFECT_SERVER_API_HOST: 0.0.0.0
      PREFECT_MESSAGING_BROKER: prefect_redis.messaging
      PREFECT_MESSAGING_CACHE: prefect_redis.messaging
      PREFECT_REDIS_MESSAGING_HOST: redis
      PREFECT_REDIS_MESSAGING_PORT: 6379
      PREFECT_REDIS_MESSAGING_DB: 0
    command: prefect server start --no-services
    ports:
      - "4200:4200"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request as u; u.urlopen('http://localhost:4200/api/health', timeout=1)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  prefect-services:
    image: prefecthq/prefect:3-latest
    depends_on:
      prefect-server:
        condition: service_healthy
    environment:
      PREFECT_API_DATABASE_CONNECTION_URL: postgresql+asyncpg://prefect:prefect@postgres:5432/prefect
      PREFECT_MESSAGING_BROKER: prefect_redis.messaging
      PREFECT_MESSAGING_CACHE: prefect_redis.messaging
      PREFECT_REDIS_MESSAGING_HOST: redis
      PREFECT_REDIS_MESSAGING_PORT: 6379
      PREFECT_REDIS_MESSAGING_DB: 0
    command: prefect server services start

  prefect-worker:
    image: prefecthq/prefect:3-latest
    depends_on:
      prefect-server:
        condition: service_healthy
    environment:
      PREFECT_API_URL: http://prefect-server:4200/api
    command: prefect worker start --pool local-pool
    restart: on-failure

volumes:
  postgres_data:
  redis_data:
```

## [​](#running-the-stack) Running the stack

1. Save the `compose.yml` file to your local machine.
2. From the directory containing the file, start the stack by running:

Copy

```
docker compose up -d
```

3. Wait for all services to start (it may take a few moments).
4. Open your browser and navigate to <http://localhost:4200> to access the Prefect UI.
5. To stop the stack, run:

Copy

```
docker compose down
```

## [​](#notes) Notes

* The PostgreSQL database is preconfigured with user and database `prefect`.
* Redis is not strictly required but is recommended as the messaging broker when [scaling a Prefect server installation](/v3/advanced/self-hosted).
* The Prefect worker automatically registers a pool named `local-pool`.
* The Prefect server exposes the API on port 4200; ensure this port is free.
* Use `docker compose logs -f` to view live logs for all services.
* This `compose.yml` does not configure authentication. See the [authentication guide](/v3/advanced/security-settings#basic-authentication) for more information.

## [​](#troubleshooting) Troubleshooting

* If the UI does not load, verify that port 4200 is not occupied by another process.
* Check container logs for errors with:

Copy

```
docker compose logs -f
```

* Make sure Docker and Docker Compose are installed and up to date.

---

For more information, see the official [Prefect documentation](https://docs.prefect.io).


---

Was this page helpful?

YesNo

[Run Prefect on Windows](/v3/how-to-guides/self-hosted/server-windows)[Use the Prefect MCP server](/v3/how-to-guides/ai/use-prefect-mcp-server)

⌘I