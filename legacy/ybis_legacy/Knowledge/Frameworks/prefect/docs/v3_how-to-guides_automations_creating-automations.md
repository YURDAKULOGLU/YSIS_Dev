How to create automations - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Automations

How to create automations

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

* [Create an automation](#create-an-automation)
* [Create automations with the CLI](#create-automations-with-the-cli)
* [Single automation example](#single-automation-example)
* [Multiple automations example](#multiple-automations-example)
* [Create automations with the Python SDK](#create-automations-with-the-python-sdk)

## [​](#create-an-automation) Create an automation

On the **Automations** page, select the **+** icon to create a new automation. You’ll be prompted to configure:

* A [trigger](/v3/concepts/automations#triggers) condition that causes the automation to execute.
* One or more [actions](/v3/concepts/automations#actions) carried out by the automation.
* Details about the automation, such as a name and description.

You can manage automations with the Prefect CLI, Terraform provider, or Prefect API.

### [​](#create-automations-with-the-cli) Create automations with the CLI

You can create automations from YAML or JSON files using the Prefect CLI:

Copy

```
# Create from a YAML file
prefect automation create --from-file automation.yaml
# or use the short form
prefect automation create -f automation.yaml

# Create from a JSON file  
prefect automation create --from-file automation.json

# Create from a JSON string
prefect automation create --from-json '{"name": "my-automation", "trigger": {...}, "actions": [...]}'
# or use the short form
prefect automation create -j '{"name": "my-automation", "trigger": {...}, "actions": [...]}'
```

#### [​](#single-automation-example) Single automation example

Here’s an example YAML file that creates an automation to cancel long-running flows:

Copy

```
name: Cancel Long Running Flows
description: Cancels flows running longer than 5 minutes
enabled: true
trigger:
  type: event
  posture: Proactive
  expect:
    - prefect.flow-run.Completed
  threshold: 1
  within: 300  # 5 minutes
  for_each:
    - prefect.resource.id
actions:
  - type: cancel-flow-run
```

#### [​](#multiple-automations-example) Multiple automations example

You can also create multiple automations at once by using the `automations:` key. If any automation fails to create, the command will continue with the remaining automations and report both successes and failures:

Copy

```
automations:
  - name: Cancel Long Running Flows
    description: Cancels flows running longer than 30 minutes
    enabled: true
    trigger:
      type: event
      posture: Reactive
      expect:
        - prefect.flow-run.Running
      threshold: 1
      for_each:
        - prefect.resource.id
    actions:
      - type: cancel-flow-run
        
  - name: Notify on Flow Failure
    description: Send notification when flows fail
    enabled: true
    trigger:
      type: event
      posture: Reactive
      expect:
        - prefect.flow-run.Failed
      threshold: 1
    actions:
      - type: send-notification
        subject: "Flow Failed: {{ event.resource.name }}"
        body: "Flow run {{ event.resource.name }} has failed."
```

Or as a JSON array:

Copy

```
[
  {
    "name": "First Automation",
    "trigger": {...},
    "actions": [...]
  },
  {
    "name": "Second Automation", 
    "trigger": {...},
    "actions": [...]
  }
]
```

### [​](#create-automations-with-the-python-sdk) Create automations with the Python SDK

You can create and access any automation with the Python SDK’s `Automation` class and its methods.

Copy

```
from prefect.automations import Automation
from prefect.events.schemas.automations import EventTrigger
from prefect.events.actions import CancelFlowRun

# creating an automation
automation = Automation(
    name="woodchonk",
    trigger=EventTrigger(
        expect={"animal.walked"},
        match={
            "genus": "Marmota",
            "species": "monax",
        },
        posture="Reactive",
        threshold=3,
    ),
    actions=[CancelFlowRun()],
).create()

# reading the automation
automation = Automation.read(id=automation.id)
# or by name
automation = Automation.read(name="woodchonk")
```

Was this page helpful?

YesNo

[Manage settings](/v3/how-to-guides/configuration/manage-settings)[Create Deployment Triggers](/v3/how-to-guides/automations/creating-deployment-triggers)

⌘I