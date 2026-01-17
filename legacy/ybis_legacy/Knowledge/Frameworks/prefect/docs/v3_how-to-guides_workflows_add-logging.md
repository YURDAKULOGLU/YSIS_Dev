How to add logging to a workflow - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to add logging to a workflow

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

* [Emit custom logs](#emit-custom-logs)
* [Log with print statements](#log-with-print-statements)
* [Access logs from the command line](#access-logs-from-the-command-line)

### [​](#emit-custom-logs) Emit custom logs

To emit custom logs, use `get_run_logger` from within a flow or task.

Copy

```
from prefect import flow, task
from prefect.logging import get_run_logger


@task(name="log-example-task")
def logger_task():
    # this logger instance will emit logs 
    # associated with both the flow run *and* the individual task run
    logger = get_run_logger()
    logger.info("INFO level log message from a task.")
    logger.debug("DEBUG level log message from a task.")


@flow(name="log-example-flow")
def logger_flow():
    # this logger instance will emit logs
    # associated with the flow run only
    logger = get_run_logger()
    logger.info("INFO level log message.")
    logger.debug("DEBUG level log message.")
    logger.error("ERROR level log message.")
    logger.critical("CRITICAL level log message.")

    logger_task()
```

The logger returned by `get_run_logger` support the [standard Python logging methods](https://docs.python.org/3/library/logging.html). Any logs emitted by the logger will be associated with the flow run or task run they are emitted from and sent to the Prefect backend. Logs sent to the Prefect backend are visible in the Prefect UI.

`get_run_logger()` can only be used in the context of a flow or task.To use a normal Python logger anywhere with your same configuration, use `get_logger()` from `prefect.logging`.The logger retrieved with `get_logger()` will **not** send log records to the Prefect API.

### [​](#log-with-print-statements) Log with print statements

To send `print` statements to the Prefect backend as logs, set the `log_prints` kwarg to `True` on the flow or task.

Copy

```
from prefect import task, flow

@task
def my_task():
    print("we're logging print statements from a task")

@flow(log_prints=True)
def my_flow():
    print("we're logging print statements from a flow")
    my_task()
```

The `log_prints` kwarg is inherited by default by nested flow runs and tasks. To opt out of logging `print` statements for a specific task or flow, set `log_prints=False` on the child flow or task.

Copy

```
from prefect import task, flow

@task(log_prints=False)
def my_task():
    print("not logging print statements in this task")

@flow(log_prints=True)
def my_flow():
    print("we're logging print statements from a flow")
    my_task()
```

You can configure the default `log_prints` setting for all Prefect flow and task runs through the
`PREFECT_LOGGING_LOG_PRINTS` setting:

Copy

```
prefect config set PREFECT_LOGGING_LOG_PRINTS=True
```

## [​](#access-logs-from-the-command-line) Access logs from the command line

You can retrieve logs for a specific flow run ID using Prefect’s CLI:

Copy

```
prefect flow-run logs MY-FLOW-RUN-ID
```

This can be particularly helpful if you want to access the logs as a local file:

Copy

```
prefect flow-run logs  MY-FLOW-RUN-ID > flow.log
```

Was this page helpful?

YesNo

[Pass inputs to a workflow](/v3/how-to-guides/workflows/pass-inputs)[Access runtime information](/v3/how-to-guides/workflows/access-runtime-info)

⌘I