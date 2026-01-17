How to run flows in a long-lived Docker container - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows in a long-lived Docker container

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

* [Overview](#overview)
* [Writing the flow](#writing-the-flow)
* [Writing the Dockerfile](#writing-the-dockerfile)
* [Build and run the container](#build-and-run-the-container)
* [Build (and push) the image](#build-and-push-the-image)
* [Run the container](#run-the-container)
* [Verify the container is running](#verify-the-container-is-running)
* [View logs](#view-logs)
* [Stop the container](#stop-the-container)
* [Health checks for production deployments](#health-checks-for-production-deployments)
* [Enabling the health check webserver](#enabling-the-health-check-webserver)
* [Configuring the health check port](#configuring-the-health-check-port)
* [Docker with health checks](#docker-with-health-checks)
* [Platform-specific configurations](#platform-specific-configurations)
* [Next steps](#next-steps)

The `.serve` method allows you to easily elevate a flow to a deployment, listening for scheduled work to execute [as a local process](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes).
However, this *“local”* process does not need to be on your local machine. In this example we show how to run a flow in Docker container on your local machine, but you could use a Docker container on any machine that has [Docker installed](https://docs.docker.com/engine/install/).

## [​](#overview) Overview

In this example, you will set up:

* a simple flow that retrieves the number of stars for some GitHub repositories
* a `Dockerfile` that packages up your flow code and dependencies into a container image

## [​](#writing-the-flow) Writing the flow

Say we have a flow that retrieves the number of stars for a GitHub repository:

serve\_retrieve\_github\_stars.py

Copy

```
import httpx
from prefect import flow, task


@task(log_prints=True)
def get_stars_for_repo(repo: str) -> int:
    response = httpx.Client().get(f"https://api.github.com/repos/{repo}")
    stargazer_count = response.json()["stargazers_count"]
    print(f"{repo} has {stargazer_count} stars")
    return stargazer_count


@flow
def retrieve_github_stars(repos: list[str]) -> list[int]:
    return get_stars_for_repo.map(repos).wait()


if __name__ == "__main__":
    retrieve_github_stars.serve(
        parameters={
            "repos": ["python/cpython", "prefectHQ/prefect"],
        }
    )
```

We can serve this flow on our local machine using:

Copy

```
python serve_retrieve_github_stars.py
```

… but how can we package this up so we can run it on other machines?

## [​](#writing-the-dockerfile) Writing the Dockerfile

Assuming we have our Python requirements defined in a file:

requirements.txt

Copy

```
prefect
```

and this directory structure:

Copy

```
├── Dockerfile
├── requirements.txt
└── serve_retrieve_github_stars.py
```

We can package up our flow into a Docker container using a `Dockerfile`.

Using pip

Using uv

Copy

```
# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY serve_retrieve_github_stars.py .

# Set the command to run your application
CMD ["python", "serve_retrieve_github_stars.py"]
```

Using `pip`, the image is built in about 20 seconds, and using `uv`, the image is built in about 3 seconds.You can learn more about using `uv` in the [Astral documentation](https://docs.astral.sh/uv/guides/integration/docker/).

## [​](#build-and-run-the-container) Build and run the container

Now that we have a flow and a Dockerfile, we can build the image from the Dockerfile and run a container from this image.

### [​](#build-and-push-the-image) Build (and push) the image

We can build the image with the `docker build` command and the `-t` flag to specify a name for the image.

Copy

```
docker build -t my-flow-image .
```

At this point, you may also want to push the image to a container registry such as [Docker Hub](https://hub.docker.com/) or [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry). Please refer to each registry’s respective documentation for details on authentication and registry naming conventions.

### [​](#run-the-container) Run the container

You’ll likely want to inject some environment variables into your container, so let’s define a `.env` file:

.env

Copy

```
PREFECT_API_URL=<YOUR-API-URL>
PREFECT_API_KEY=<YOUR-API-KEY-IF-USING-PREFECT-CLOUD>
```

Then, run the container in [detached mode](https://docs.docker.com/engine/reference/commandline/run/#detached-d) (in other words, in the background):

Copy

```
docker run -d --env-file .env my-flow-image
```

#### [​](#verify-the-container-is-running) Verify the container is running

Copy

```
docker ps | grep my-flow-image
```

You should see your container in the list of running containers, note the `CONTAINER ID` as we’ll need it to view logs.

#### [​](#view-logs) View logs

Copy

```
docker logs <CONTAINER-ID>
```

You should see logs from your newly served process, with the link to your deployment in the UI.

### [​](#stop-the-container) Stop the container

Copy

```
docker stop <CONTAINER-ID>
```

## [​](#health-checks-for-production-deployments) Health checks for production deployments

When deploying to production environments like Google Cloud Run, AWS ECS, or Kubernetes, you may need to configure health checks to ensure your container is running properly. The `.serve()` method supports an optional webserver that exposes a health endpoint.

### [​](#enabling-the-health-check-webserver) Enabling the health check webserver

You can enable the health check webserver in two ways:

1. **Pass `webserver=True` to `.serve()`:**

Copy

```
if __name__ == "__main__":
    retrieve_github_stars.serve(
        parameters={
            "repos": ["python/cpython", "prefectHQ/prefect"],
        },
        webserver=True  # Enable health check webserver
    )
```

2. **Set the environment variable:**

Copy

```
PREFECT_RUNNER_SERVER_ENABLE=true
```

When enabled, the webserver exposes a health endpoint at `http://localhost:8080/health` by default.

### [​](#configuring-the-health-check-port) Configuring the health check port

You can customize the host and port using environment variables:

Copy

```
PREFECT_RUNNER_SERVER_HOST=0.0.0.0  # Allow external connections
PREFECT_RUNNER_SERVER_PORT=8080      # Port for health checks
```

### [​](#docker-with-health-checks) Docker with health checks

Add a health check to your Dockerfile:

Copy

```
# ... your existing Dockerfile content ...

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8080/health', timeout=1)"

# Set the command to run your application with webserver enabled
CMD ["python", "serve_retrieve_github_stars.py"]
```

Or if you prefer to use environment variables:

Copy

```
# ... your existing Dockerfile content ...

# Enable the health check webserver
ENV PREFECT_RUNNER_SERVER_ENABLE=true
ENV PREFECT_RUNNER_SERVER_HOST=0.0.0.0
ENV PREFECT_RUNNER_SERVER_PORT=8080

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8080/health', timeout=1)"

CMD ["python", "serve_retrieve_github_stars.py"]
```

### [​](#platform-specific-configurations) Platform-specific configurations

* Google Cloud Run
* AWS ECS/Fargate
* Kubernetes

Cloud Run requires containers to listen on a port. Configure your container to expose the health check port:

Copy

```
# In your Cloud Run configuration
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 60
  periodSeconds: 30
```

Make sure to set the container port to 8080 in Cloud Run settings.

Configure health checks in your task definition:

Copy

```
{
  "healthCheck": {
    "command": ["CMD-SHELL", "python -c \"import urllib.request as u; u.urlopen('http://localhost:8080/health', timeout=1)\""],
    "interval": 30,
    "timeout": 10,
    "retries": 3,
    "startPeriod": 60
  }
}
```

Add liveness and readiness probes to your deployment:

Copy

```
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 60
  periodSeconds: 30
  timeoutSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
```

The health endpoint returns:

* **200 OK** with `{"message": "OK"}` when the runner is healthy and polling for work
* **503 Service Unavailable** when the runner hasn’t polled recently (indicating it may be unresponsive)

## [​](#next-steps) Next steps

Congratulations! You have packaged and served a flow on a long-lived Docker container.
You may now easily deploy this container to other infrastructures, such as:

* [Modal](https://modal.com/)
* [Google Cloud Run](https://cloud.google.com/run)
* [AWS Fargate / ECS](https://aws.amazon.com/fargate/)
* Managed Kubernetes (For example: GKE, EKS, or AKS)

or anywhere else you can run a Docker container!

Was this page helpful?

YesNo

[Run flows in Docker containers](/v3/how-to-guides/deployment_infra/docker)[Run flows on Kubernetes](/v3/how-to-guides/deployment_infra/kubernetes)

⌘I