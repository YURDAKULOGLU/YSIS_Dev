How to access deployment and flow run parameters - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Automations

How to access deployment and flow run parameters

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

Many of the parameters of automation actions can be defined with [Jinja2 templates](/v3/concepts/automations#templating-with-jinja). These templates have access to objects related to the event that triggered your automation, including the deployment and flow run of that event (if applicable). Here we’ll explore an example illustrating how to access their parameters in an automation action.
Let’s start with two flows, `alpha` and `beta`:

Copy

```
from prefect import flow


@flow
def alpha(name: str, value: int):
    print(name, value)


@flow
def beta(name: str, value: int, another: float):
    print(name, value, another)
```

Once a run of `alpha` completes, we’ll automate running a flow of `beta` with the same parameters:

Copy

```
from datetime import timedelta

from prefect.automations import (
    Automation,
    EventTrigger,
    Posture,
    ResourceSpecification,
    RunDeployment,
)

from .flows import alpha, beta

# Note: deploy these flows in the way you best see fit for your environment
alpha.deploy(
    name="alpha",
    work_pool_name="my-work-pool",
    image="prefecthq/prefect-client:3-latest",
)
beta_deployment_id = beta.deploy(
    name="beta",
    work_pool_name="my-work-pool",
    image="prefecthq/prefect-client:3-latest",
)

automation = Automation(
    name="Passing parameters",
    trigger=EventTrigger(
        # Here we're matching on every completion of the `alpha` flow
        expect={"prefect.flow-run.Completed"},
        match_related=ResourceSpecification(
            {
                "prefect.resource.role": "flow",
                "prefect.resource.name": "alpha"
            }
        ),
        # And we'll react to each event immediately and individually
        posture=Posture.Reactive,
        threshold=1,
        within=timedelta(0),
    ),
    actions=[
        RunDeployment(
            # We will be selecting a specific deployment (rather than attempting to
            # infer it from the event)
            source="selected",
            # The deployment we want to run is the `beta` deployment we created above
            deployment_id=beta_deployment_id,
            parameters={
                # For the "name" and "value" parameters, we tell Prefect we're using a
                # Jinja2 template by creating a nested dictionary with the special
                # `__prefect_kind` key set to "jinja".  Then we supply the `template`
                # value with any valid Jinja2 template.  This step may also be done
                # in the Prefect UI by selecting "Use Jinja input" for the parameters
                # you want to template.
                #
                # The "{{ flow_run }}" variable here is a special shortcut that gives us
                # access to the `FlowRun` object associated with this event.  There are
                # also variables like "{{ deployment }}", "{{ flow }}",
                # "{{ work_pool }}" and so on.
                #
                # In this case, the {{ flow_run }} represent the run of `alpha` that
                # emitted the `prefect.flow-run.Completed` event that triggered this
                # automation.
                "name": {
                    "template": "{{ flow_run.parameters['name'] }}",
                    "__prefect_kind": "jinja",
                },
                "value": {
                    "template": "{{ flow_run.parameters['value'] }}",
                    "__prefect_kind": "jinja",
                },
                # You can also just pass literal parameters
                "another": 1.2345,
            },
        )
    ],
).create()
```

If you are defining your automation in the Prefect web UI, you can switch the parameter input to support Jinja2 values:
![Use Jinja input for an action](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/automation-use-jinja-input.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=9609c36afc9d6d7800f75197e07767e8)

Was this page helpful?

YesNo

[Chain Deployments with Events](/v3/how-to-guides/automations/chaining-deployments-with-events)[Pass event payloads to flows](/v3/how-to-guides/automations/passing-event-payloads-to-flows)

⌘I