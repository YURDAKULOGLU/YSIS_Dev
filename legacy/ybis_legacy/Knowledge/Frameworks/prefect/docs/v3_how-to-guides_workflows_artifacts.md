How to produce workflow artifacts - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflows

How to produce workflow artifacts

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

* [Create link artifacts](#create-link-artifacts)
* [Create progress artifacts](#create-progress-artifacts)
* [Create Markdown artifacts](#create-markdown-artifacts)
* [Create table artifacts](#create-table-artifacts)
* [Create image artifacts](#create-image-artifacts)
* [Reading artifacts](#reading-artifacts)
* [Fetching artifacts](#fetching-artifacts)
* [Delete artifacts](#delete-artifacts)

### [​](#create-link-artifacts) Create link artifacts

To create a link artifact, use the `create_link_artifact()` function.
To create multiple versions of the same artifact and/or view them on the Artifacts page of the Prefect UI,
provide a `key` argument to the `create_link_artifact()` function to track the artifact’s history over time.
Without a `key`, the artifact is only visible in the Artifacts tab of the associated flow run or task run.

Copy

```
from prefect import flow, task
from prefect.artifacts import create_link_artifact


@task
def my_first_task():
    create_link_artifact(
        key="irregular-data",
        link="https://nyc3.digitaloceanspaces.com/my-bucket-name/highly_variable_data.csv",
        description="## Highly variable data",
    )


@task
def my_second_task():
    create_link_artifact(
        key="irregular-data",
        link="https://nyc3.digitaloceanspaces.com/my-bucket-name/low_pred_data.csv",
        description="# Low prediction accuracy",
    )


@flow
def my_flow():
    my_first_task()
    my_second_task()


if __name__ == "__main__":
    my_flow()
```

**Specify multiple artifacts with the same key for artifact lineage**You can specify multiple artifacts with the same key to easily track something very specific, such as irregularities in your data pipeline.

After running flows that create artifacts, view the artifacts in the **Artifacts** page of the UI.
Click into the “irregular-data” artifact to see its versions, along with custom descriptions and links to the relevant data.
![Link artifact details with multiple versions](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/link-artifact-info.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=113a4fc91846eb134048dd79813a95de)
You can also view information about the artifact such as:

* its associated flow run or task run id
* previous and future versions of the artifact (multiple artifacts can have the same key to show lineage)
* data (in this case a Markdown-rendered link)
* an optional Markdown description
* when the artifact was created or updated

To make the links more readable for you and your collaborators, you can pass a `link_text` argument:

Copy

```
from prefect import flow
from prefect.artifacts import create_link_artifact


@flow
def my_flow():
    create_link_artifact(
        key="my-important-link",
        link="https://www.prefect.io/",
        link_text="Prefect",
    )


if __name__ == "__main__":
    my_flow()
```

In the above example, the `create_link_artifact` method is used within a flow to create a link artifact with a key of `my-important-link`.
The `link` parameter specifies the external resource to link to, and `link_text` specifies the text to display for the link.
Add an optional `description` for context.

### [​](#create-progress-artifacts) Create progress artifacts

Progress artifacts render dynamically on the flow run graph in the Prefect UI, indicating the progress of long-running tasks.
To create a progress artifact, use the `create_progress_artifact()` function. To update a progress artifact, use the `update_progress_artifact()` function.
![Progress artifact example](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/progress-artifact-example.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=3d0d6dae1173e61d198a5b3a22750d75)

Copy

```
from time import sleep

from prefect import flow, task
from prefect.artifacts import (
    create_progress_artifact,
    update_progress_artifact,
)


def fetch_batch(i: int):
    # Simulate fetching a batch of data
    sleep(2)


@task
def fetch_in_batches():
    progress_artifact_id = create_progress_artifact(
        progress=0.0,
        description="Indicates the progress of fetching data in batches.",
    )
    for i in range(1, 11):
        fetch_batch(i)
        update_progress_artifact(artifact_id=progress_artifact_id, progress=i * 10)


@flow
def etl():
    fetch_in_batches()


if __name__ == "__main__":
    etl()
```

Progress artifacts are updated with the `update_progress_artifact()` function. Prefect updates a progress artifact in place, rather than versioning it.

### [​](#create-markdown-artifacts) Create Markdown artifacts

To create a Markdown artifact, you can use the `create_markdown_artifact()` function.
To create multiple versions of the same artifact and/or view them on the Artifacts page of the Prefect UI, provide a `key` argument to the `create_markdown_artifact()` function to track an artifact’s history over time.
Without a `key`, the artifact is only visible in the Artifacts tab of the associated flow run or task run.

**Don’t indent Markdown**Don’t indent Markdown in multi-line strings. Otherwise it will be interpreted incorrectly.

Copy

```
from prefect import flow, task
from prefect.artifacts import create_markdown_artifact


@task
def markdown_task():
    na_revenue = 500000
    markdown_report = f"""# Sales Report

## Summary

In the past quarter, our company saw a significant increase in sales, with a total revenue of $1,000,000. 
This represents a 20% increase over the same period last year.

## Sales by Region

| Region        | Revenue |
|:--------------|-------:|
| North America | ${na_revenue:,} |
| Europe        | $250,000 |
| Asia          | $150,000 |
| South America | $75,000 |
| Africa        | $25,000 |

## Top Products

1. Product A - $300,000 in revenue
2. Product B - $200,000 in revenue
3. Product C - $150,000 in revenue

## Conclusion

Overall, these results are very encouraging and demonstrate the success of our sales team in increasing revenue 
across all regions. However, we still have room for improvement and should focus on further increasing sales in 
the coming quarter.
"""
    create_markdown_artifact(
        key="gtm-report",
        markdown=markdown_report,
        description="Quarterly Sales Report",
    )


@flow()
def my_flow():
    markdown_task()
    

if __name__ == "__main__":
    my_flow()
```

After running the above flow, you should see your “gtm-report” artifact in the Artifacts page of the UI.
![Markdown sales report screenshot](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/md-artifact-info.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=0daffdebede0bcf508172cd503fbe873)
You can view the associated flow run id or task run id, previous versions of the artifact, the rendered Markdown data, and the optional Markdown description.

### [​](#create-table-artifacts) Create table artifacts

Create a table artifact by calling `create_table_artifact()`.
To create multiple versions of the same artifact and/or view them on the Artifacts page of the Prefect UI, provide a `key` argument to the `create_table_artifact()` function to track an artifact’s history over time.
Without a `key`, the artifact is only visible in the artifacts tab of the associated flow run or task run.

The `create_table_artifact()` function accepts a `table` argument. Pass this as a list of lists, a list of dictionaries, or a dictionary of lists.

Copy

```
from prefect.artifacts import create_table_artifact


def my_fn():
    highest_churn_possibility = [
       {'customer_id':'12345', 'name': 'John Smith', 'churn_probability': 0.85 }, 
       {'customer_id':'56789', 'name': 'Jane Jones', 'churn_probability': 0.65 } 
    ]

    create_table_artifact(
        key="personalized-reachout",
        table=highest_churn_possibility,
        description= "# Marvin, please reach out to these customers today!"
    )


if __name__ == "__main__":
    my_fn()
```

![Table artifact with customer info](https://mintcdn.com/prefect-bd373955/rT_XiX8cZI7Bzt5c/v3/img/ui/table-artifact-info.png?fit=max&auto=format&n=rT_XiX8cZI7Bzt5c&q=85&s=8da47c36540b4b3ae89b8851bf008e9a)

### [​](#create-image-artifacts) Create image artifacts

Image artifacts render publicly available images in the Prefect UI. To create an image artifact, use the `create_image_artifact()` function.
![Image artifact example](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/image-artifact-example.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=d84414a3e83d817e77dfde0c37992e39)

Copy

```
from prefect import flow, task
from prefect.artifacts import (
    create_image_artifact,
)


@task
def create_image():
    # Do something to create an image and upload to a url
    image_url = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmQydzBjOHQ2M3BhdWJ4M3V1MGtoZGxuNmloeGh6b2dvaHhpaHg0eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3KC2jD2QcBOSc/giphy.gif"
    create_image_artifact(image_url=image_url, description="A gif.", key="gif")
    return image_url


@flow
def my_flow():
    return create_image()


if __name__ == "__main__":
    image_url = my_flow()
    print(f"Image URL: {image_url}")
```

To create an artifact that links to a private image, use the `create_link_artifact()` function instead.

### [​](#reading-artifacts) Reading artifacts

In the Prefect UI, you can view all of the latest versions of your artifacts and click into a specific artifact to see its lineage over time.
Additionally, you can inspect all versions of an artifact with a given key from the CLI by running:

Copy

```
prefect artifact inspect <my_key>
```

or view all artifacts by running:

Copy

```
prefect artifact ls
```

You can also use the [Prefect REST API](https://app.prefect.cloud/api/docs#tag/Artifacts/operation/read_artifacts_api_accounts__account_id__workspaces__workspace_id__artifacts_filter_post)
to programmatically filter your results.

### [​](#fetching-artifacts) Fetching artifacts

In Python code, you can retrieve an existing artifact with the `Artifact.get` class method:

Copy

```
from prefect.artifacts import Artifact


my_retrieved_artifact = Artifact.get("my_artifact_key")
```

### [​](#delete-artifacts) Delete artifacts

Delete an artifact in the CLI by providing a key or id:

Copy

```
prefect artifact delete <my_key>
```

Copy

```
prefect artifact delete --id <my_id>
```

Was this page helpful?

YesNo

[Respond to state changes](/v3/how-to-guides/workflows/state-change-hooks)[Test workflows](/v3/how-to-guides/workflows/test-workflows)

⌘I