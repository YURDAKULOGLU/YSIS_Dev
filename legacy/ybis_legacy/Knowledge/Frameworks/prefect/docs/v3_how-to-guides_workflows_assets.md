How to use assets to track workflow outputs - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to use assets to track workflow outputs

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

* [Basic asset materialization](#basic-asset-materialization)
* [Asset dependencies](#asset-dependencies)
* [Inferred from task graphs](#inferred-from-task-graphs)
* [External and cross-flow asset dependencies](#external-and-cross-flow-asset-dependencies)
* [Multiple asset materialization](#multiple-asset-materialization)
* [Dynamic asset materialization](#dynamic-asset-materialization)
* [Further Reading](#further-reading)

Assets in Prefect represent important outputs (such as data) that are produced by your tasks and flows. Assets can reference virtually any output such as files, dataframes, tables, dashboards, or ML models. By using the `@materialize` decorator, you can track when your workflows create, update, or reference these objects.

## [​](#basic-asset-materialization) Basic asset materialization

Use the `@materialize` decorator to mark functions that create or update assets. This decorator wraps your function similar to `@task` but specifically tracks asset creation:

Copy

```
from prefect import flow
from prefect.assets import materialize

@materialize("s3://my-bucket/processed-data.csv")
def process_data(data: dict) -> dict:
    # Your data processing logic here
    # save_to_s3(data, "s3://my-bucket/processed-data.csv")
    return data

@flow
def data_pipeline(data: dict):
    process_data(data)
```

Asset keys must be valid URIs that uniquely identify your workflow outputs. Assets are automatically grouped by type (specified by the URI prefix) and can be nested based on the URI path structure. For example, `s3://` assets are grouped separately from `postgres://` assets, and nested paths like `s3://bucket/team-a/data.csv` and `s3://bucket/team-b/data.csv` create hierarchical organization.

**`@materialize` wraps `@task`**: the `@materialize` decorator accepts all keyword arguments and configuration that the `@task` decorator accepts and can be used as a drop-in replacement.

## [​](#asset-dependencies) Asset dependencies

### [​](#inferred-from-task-graphs) Inferred from task graphs

Prefect automatically infers asset dependencies from your task graph. When materialized assets flow through your workflow, downstream materializations inherit these dependencies:

Copy

```
from prefect import flow
from prefect.assets import materialize


@materialize("file://my-local-directory/raw-data.csv")
def extract_data() -> str:
    raw_data = "name,age\nchris,21"
    with open("raw-data.csv", "w") as f:
        f.write(raw_data)
    return raw_data


@materialize("s3://my-bucket/clean-data.csv")
def transform_data(raw_data):
    # saves raw_data to s3
    pass


@flow
def etl_pipeline():
    raw_data = extract_data()
    transform_data(raw_data)  # Automatically depends on raw-data.csv
```

Running this flow produces the following asset graph:
![Asset Graph in the UI](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/assets-1.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=f94e8971f57299cd43e178177ec977e6)

### [​](#external-and-cross-flow-asset-dependencies) External and cross-flow asset dependencies

Use `asset_deps` to reference assets that are external to your current workflow. This creates dependencies on assets that may be materialized by other flows, external systems, or manual processes:

Copy

```
from prefect import flow
from prefect.assets import materialize


# Depends on asset from another Prefect flow
@materialize(
    "s3://my-bucket/downstream-data.csv",
    asset_deps=["s3://my-bucket/upstream-data.csv"]  # From different flow
)
def process_downstream_data():
    pass

# Depends on external system assets
@materialize(
    "s3://my-bucket/enriched-data.csv",
    asset_deps=[
        "postgres://db/users_table",      # External database
        "sftp://vendor/daily-feed.csv"    # External data feed
    ]
)
def enrich_user_data():
    pass

@flow
def analytics_pipeline():
    process_downstream_data()
    enrich_user_data()
```

Running this flow produces the following asset graph:
![Asset Graph in the UI](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/assets-2.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=c64f005627357c5ddaf1e46552291c71)
This approach allows you to model your complete data ecosystem, tracking dependencies even when some assets are managed outside your current workflow or outside Prefect entirely.

## [​](#multiple-asset-materialization) Multiple asset materialization

Materialize multiple related assets in a single function when they share the same upstream dependencies:

Copy

```
from prefect.assets import materialize


@materialize(
    "s3://my-bucket/summary.csv",
    "s3://my-bucket/details.csv"
)
def generate_reports():
    data = fetch_source_data()
    create_summary_report(data)
    create_detailed_report(data)
```

## [​](#dynamic-asset-materialization) Dynamic asset materialization

Use [the `with_options` pattern](/v3/api-ref/python/prefect-tasks#with-options) to dynamically change asset keys and dependencies at runtime. This is useful when you need to parameterize asset paths based on flow inputs, dates, or other runtime conditions:

Copy

```
from prefect import flow
from prefect.assets import materialize
from datetime import datetime


@materialize("s3://my-bucket/daily-report.csv")
def generate_daily_report(date: str):
    # Process and save daily report
    pass


@flow
def dynamic_reporting_pipeline():
    base_task = generate_daily_report
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Dynamically set asset key based on date
    daily_task = base_task.with_options(
        assets=[f"s3://my-bucket/reports/{today}/daily-report.csv"]
    )
    
    daily_task(today)
```

You can also dynamically modify asset dependencies alongside the materialized assets:

Copy

```
from prefect import flow
from prefect.assets import materialize


@materialize(
    "s3://my-bucket/processed-data.csv",
    asset_deps=["s3://my-bucket/raw-data.csv"]
)
def process_data(environment: str):
    pass


@flow
def environment_specific_pipeline(env: str):
    base_task = process_data
    
    # Use different assets based on environment
    env_task = base_task.with_options(
        assets=[f"s3://my-bucket/{env}/processed-data.csv"],
        asset_deps=[f"s3://my-bucket/{env}/raw-data.csv"]
    )
    
    env_task(env)
```

This pattern enables you to reuse the same processing logic across different environments, time periods, or data partitions while maintaining proper asset lineage tracking.

## [​](#further-reading) Further Reading

* [How to customize asset metadata](/v3/advanced/assets)
* [Learn about asset health and asset events](/v3/concepts/assets)

Was this page helpful?

YesNo

[Write and run a workflow](/v3/how-to-guides/workflows/write-and-run)[Automatically rerun a workflow when it fails](/v3/how-to-guides/workflows/retries)

⌘I