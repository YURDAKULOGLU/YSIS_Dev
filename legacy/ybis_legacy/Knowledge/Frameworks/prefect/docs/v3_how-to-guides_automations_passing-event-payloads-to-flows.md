How to pass event payloads to flows - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Automations

How to pass event payloads to flows

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

* [Define a flow that accepts payload data](#define-a-flow-that-accepts-payload-data)
* [Emit a custom event with payload](#emit-a-custom-event-with-payload)
* [Configure the automation trigger](#configure-the-automation-trigger)
* [Configure the action to pass the payload](#configure-the-action-to-pass-the-payload)
* [Define everything in Python](#define-everything-in-python)
* [Alternative: Pass individual payload fields](#alternative%3A-pass-individual-payload-fields)

When you emit custom events with payloads, you can pass that payload data to flows triggered by automations. This is useful for event-driven workflows where external systems or APIs send structured data that your flows need to process.

## [​](#define-a-flow-that-accepts-payload-data) Define a flow that accepts payload data

Create a flow that accepts a dictionary payload:

Copy

```
from typing import Any

from prefect import flow


@flow(log_prints=True)
def process_webhook(payload: dict[str, Any]):
    """Process data from a custom event"""
    print(f"User: {payload.get('user_id')}")
    print(f"Action: {payload.get('action')}")
    print(f"Full payload: {payload}")


if __name__ == "__main__":
    process_webhook.serve(
        name="webhook-processor",
        tags=["webhook", "event-driven"],
    )
```

## [​](#emit-a-custom-event-with-payload) Emit a custom event with payload

Emit custom events with structured payloads using the Prefect CLI:

Copy

```
prefect event emit api.webhook.received \
  --resource-id custom.webhook.handler \
  --payload '{
    "user_id": "123",
    "action": "created",
    "resource_type": "order",
    "timestamp": "2024-01-15T10:30:00Z"
  }'
```

Or using the Python SDK:

Copy

```
from prefect.events import emit_event

emit_event(
    event="api.webhook.received",
    resource={
        "prefect.resource.id": "custom.webhook.handler",
        "prefect.resource.role": "api"
    },
    payload={
        "user_id": "123",
        "action": "created",
        "resource_type": "order",
        "timestamp": "2024-01-15T10:30:00Z"
    }
)
```

## [​](#configure-the-automation-trigger) Configure the automation trigger

Create a new automation from the Automations page. In the trigger configuration, set it to listen for your custom event. The trigger definition should look like this in the `JSON` tab:

Copy

```
{
  "type": "event",
  "match": {
    "prefect.resource.id": [
      "custom.webhook.handler"
    ]
  },
  "match_related": {},
  "after": [],
  "expect": [
    "api.webhook.received"
  ],
  "for_each": [],
  "posture": "Reactive",
  "threshold": 1,
  "within": 0
}
```

**Finding your custom events**You can view all events, including your custom events, in the Event Feed in the Prefect UI. This helps you verify the exact event names and payload structure to use in your automation configuration.

## [​](#configure-the-action-to-pass-the-payload) Configure the action to pass the payload

Add a “Run a deployment” action and configure it to pass the event payload as a dictionary to your flow.
In the UI, you’ll need to use “custom JSON” mode for the `payload` parameter and enter:

Copy

```
{
  "__prefect_kind": "json",
  "value": {
    "__prefect_kind": "jinja",
    "template": "{{ event.payload | tojson }}"
  }
}
```

This nested structure:

1. Renders the Jinja template `{{ event.payload | tojson }}` to a JSON string
2. Automatically parses the JSON string back to a dictionary using the `json` handler

This allows your flow to receive the payload as a `dict` type rather than a string.

## [​](#define-everything-in-python) Define everything in Python

You can define the flow and trigger entirely in Python using `DeploymentEventTrigger`:

event\_payload\_example.py

Copy

```
from typing import Any

from prefect import flow, serve
from prefect.events import DeploymentEventTrigger


@flow(log_prints=True)
def process_webhook(payload: dict[str, Any]):
    """Process data from a custom event"""
    print(f"User: {payload.get('user_id')}")
    print(f"Action: {payload.get('action')}")
    print(f"Full payload: {payload}")


if __name__ == "__main__":
    deployment = process_webhook.to_deployment(
        name="webhook-processor",
        triggers=[
            DeploymentEventTrigger(
                expect={"api.webhook.received"},
                parameters={
                    "payload": {
                        "__prefect_kind": "json",
                        "value": {
                            "__prefect_kind": "jinja",
                            "template": "{{ event.payload | tojson }}",
                        }
                    }
                },
            )
        ],
    )

    serve(deployment)
```

Start the serve process:

Copy

```
python event_payload_example.py
```

Get the deployment ID from the output, then emit an event targeting that deployment:

Copy

```
prefect event emit api.webhook.received \
  --resource-id prefect.deployment.<deployment-id> \
  --payload '{"user_id": "123", "action": "created", "resource_type": "order"}'
```

**Targeting the deployment**When using `DeploymentEventTrigger`, events must target the deployment’s resource ID (`prefect.deployment.<deployment-id>`). You can find the deployment ID in the serve output or with `prefect deployment ls`.

## [​](#alternative:-pass-individual-payload-fields) Alternative: Pass individual payload fields

If you only need specific fields from the payload, you can access them individually using Jinja templates for each parameter:

Copy

```
from prefect import flow, serve
from prefect.events import DeploymentEventTrigger


@flow(log_prints=True)
def process_webhook(user_id: str, action: str, resource_type: str):
    """Process individual fields from a custom event"""
    print(f"Processing {action} for user {user_id}")
    print(f"Resource type: {resource_type}")


if __name__ == "__main__":
    deployment = process_webhook.to_deployment(
        name="webhook-processor-fields",
        triggers=[
            DeploymentEventTrigger(
                expect={"api.webhook.received"},
                parameters={
                    "user_id": {
                        "__prefect_kind": "jinja",
                        "template": "{{ event.payload.user_id }}",
                    },
                    "action": {
                        "__prefect_kind": "jinja",
                        "template": "{{ event.payload.action }}",
                    },
                    "resource_type": {
                        "__prefect_kind": "jinja",
                        "template": "{{ event.payload.resource_type }}",
                    },
                },
            )
        ],
    )

    serve(deployment)
```

This approach is useful when your flow expects specific typed parameters (like strings or integers) rather than a generic dictionary. Each field from the event payload is extracted and passed as a separate parameter to your flow.

Was this page helpful?

YesNo

[Access parameters in templates](/v3/how-to-guides/automations/access-parameters-in-templates)[Manage Work Pools](/v3/how-to-guides/deployment_infra/manage-work-pools)

⌘I