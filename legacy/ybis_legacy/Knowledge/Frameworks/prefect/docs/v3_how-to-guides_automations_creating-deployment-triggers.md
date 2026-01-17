How to create deployment triggers - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Automations

How to create deployment triggers

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

* [Creating deployment triggers](#creating-deployment-triggers)
* [Define triggers in prefect.yaml](#define-triggers-in-prefect-yaml)
* [Scheduling delayed deployment runs](#scheduling-delayed-deployment-runs)
* [Define deployment triggers using Terraform](#define-deployment-triggers-using-terraform)
* [Define triggers in .serve and .deploy](#define-triggers-in-serve-and-deploy)
* [Pass triggers to prefect deploy](#pass-triggers-to-prefect-deploy)
* [Further reading](#further-reading)

## [​](#creating-deployment-triggers) Creating deployment triggers

To enable the simple configuration of event-driven deployments, Prefect provides **deployment triggers**—a shorthand for
creating automations that are linked to specific deployments to run them based on the presence or absence of events.

Deployment triggers are a special case of automations where the configured action is always running a deployment.

Trigger definitions for deployments are supported in `prefect.yaml`, `.serve`, and `.deploy`. At deployment time,
specified trigger definitions create linked automations triggered by events matching your chosen
[grammar](/v3/concepts/events#event-grammar). Each trigger definition may include a [jinja template](https://en.wikipedia.org/wiki/Jinja_(template_engine))
to render the triggering `event` as the `parameters` of your deployment’s flow run.

### [​](#define-triggers-in-prefect-yaml) Define triggers in `prefect.yaml`

You can include a list of triggers on any deployment in a `prefect.yaml` file:

Copy

```
deployments:
  - name: my-deployment
    entrypoint: path/to/flow.py:decorated_fn
    work_pool:
      name: my-work-pool
    triggers:
      - type: event
        enabled: true
        match:
          prefect.resource.id: my.external.resource
        expect:
          - external.resource.pinged
        parameters:
          param_1: "{{ event }}"
```

### [​](#scheduling-delayed-deployment-runs) Scheduling delayed deployment runs

You can configure deployment triggers to run after a specified delay using the `schedule_after` field. This is useful for implementing opt-out workflows or providing review windows before automated actions:

Copy

```
deployments:
  - name: campaign-execution
    entrypoint: path/to/campaign.py:execute_campaign
    work_pool:
      name: my-work-pool
    triggers:
      - type: event
        enabled: true
        match:
          prefect.resource.id: marketing.campaign
        expect:
          - campaign.proposal.created
        schedule_after: "PT2H"  # Wait 2 hours before execution
        parameters:
          campaign_id: "{{ event.resource.id }}"
```

The `schedule_after` field accepts:

* **ISO 8601 durations** (e.g., “PT2H” for 2 hours, “PT30M” for 30 minutes)
* **Seconds as integer** (e.g., 7200 for 2 hours)
* **Python timedelta objects** in code

This deployment creates a flow run when an `external.resource.pinged` event *and* an `external.resource.replied`
event have been seen from `my.external.resource`:

Copy

```
deployments:
  - name: my-deployment
    entrypoint: path/to/flow.py:decorated_fn
    work_pool:
      name: my-work-pool
    triggers:
      - type: compound
        require: all
        parameters:
          param_1: "{{ event }}"
        schedule_after: "PT1H"  # Wait 1 hour before running
        triggers:
          - type: event
            match:
              prefect.resource.id: my.external.resource
            expect:
              - external.resource.pinged
          - type: event
            match:
              prefect.resource.id: my.external.resource
            expect:
              - external.resource.replied
```

### [​](#define-deployment-triggers-using-terraform) Define deployment triggers using Terraform

You can also set up a deployment trigger via Terraform resources, specifically via the `prefect_automation` [resource](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/automation).

Copy

```
resource "prefect_deployment" "my_deployment" {
  name            = "my-deployment"
  work_pool_name  = "my-work-pool"
  work_queue_name = "default"
  entrypoint      = "path/to/flow.py:decorated_fn"
}

resource "prefect_automation" "event_trigger" {
  name = "my-automation"
  trigger = {
    event = {
      posture   = "Reactive"
      expect    = ["external.resource.pinged"]
      threshold = 1
      within    = 0
    }
  }
  actions = [
    {
      type          = "run-deployment"
      source        = "selected"
      deployment_id = prefect_deployment.my_deployment.id
      parameters = jsonencode({
        "param_1" : "{{ event }}"
      })
    },
  ]
}
```

### [​](#define-triggers-in-serve-and-deploy) Define triggers in `.serve` and `.deploy`

To create deployments with triggers in Python, the trigger types `DeploymentEventTrigger`,
`DeploymentMetricTrigger`, `DeploymentCompoundTrigger`, and `DeploymentSequenceTrigger` can be imported
from `prefect.events`:

Copy

```
from datetime import timedelta
from prefect import flow
from prefect.events import DeploymentEventTrigger


@flow(log_prints=True)
def decorated_fn(param_1: str):
    print(param_1)


if __name__=="__main__":
    decorated_fn.serve(
        name="my-deployment",
        triggers=[
            DeploymentEventTrigger(
                enabled=True,
                match={"prefect.resource.id": "my.external.resource"},
                expect=["external.resource.pinged"],
                schedule_after=timedelta(hours=1),  # Wait 1 hour before running
                parameters={
                    "param_1": "{{ event }}",
                },
            )
        ],
    )
```

As with prior examples, you must supply composite triggers with a list of underlying triggers:

Copy

```
from datetime import timedelta
from prefect import flow
from prefect.events import DeploymentCompoundTrigger


@flow(log_prints=True)
def decorated_fn(param_1: str):
    print(param_1)


if __name__=="__main__":
    decorated_fn.deploy(
        name="my-deployment",
        image="my-image-registry/my-image:my-tag",
        triggers=[
            DeploymentCompoundTrigger(
                enabled=True,
                name="my-compound-trigger",
                require="all",
                schedule_after=timedelta(minutes=30),  # Wait 30 minutes
                triggers=[
                    {
                      "type": "event",
                      "match": {"prefect.resource.id": "my.external.resource"},
                      "expect": ["external.resource.pinged"],
                    },
                    {
                      "type": "event",
                      "match": {"prefect.resource.id": "my.external.resource"},
                      "expect": ["external.resource.replied"],
                    },
                ],
                parameters={
                    "param_1": "{{ event }}",
                },
            )
        ],
        work_pool_name="my-work-pool",
    )
```

### [​](#pass-triggers-to-prefect-deploy) Pass triggers to `prefect deploy`

You can pass one or more `--trigger` arguments to `prefect deploy` as either a JSON string or a
path to a `.yaml` or `.json` file.

Copy

```
# Pass a trigger as a JSON string
prefect deploy -n test-deployment \
  --trigger '{
    "enabled": true,
    "match": {
      "prefect.resource.id": "prefect.flow-run.*"
    },
    "expect": ["prefect.flow-run.Completed"]
  }'

# Pass a trigger using a JSON/YAML file
prefect deploy -n test-deployment --trigger triggers.yaml
prefect deploy -n test-deployment --trigger my_stuff/triggers.json
```

For example, a `triggers.yaml` file could have many triggers defined:

Copy

```
triggers:
  - enabled: true
    match:
      prefect.resource.id: my.external.resource
    expect:
      - external.resource.pinged
    parameters:
      param_1: "{{ event }}"
  - enabled: true
    match:
      prefect.resource.id: my.other.external.resource
    expect:
      - some.other.event
    parameters:
      param_1: "{{ event }}"
```

Both of the above triggers would be attached to `test-deployment` after running `prefect deploy`.

**Triggers passed to `prefect deploy` will override any triggers defined in `prefect.yaml`**While you can define triggers in `prefect.yaml` for a given deployment, triggers passed to `prefect deploy`
take precedence over those defined in `prefect.yaml`.

Note that deployment triggers contribute to the total number of automations in your workspace.

## [​](#further-reading) Further reading

For more on the concepts behind deployment triggers, see the [Automations concepts](/v3/concepts/automations) page.

Was this page helpful?

YesNo

[Create Automations](/v3/how-to-guides/automations/creating-automations)[Chain Deployments with Events](/v3/how-to-guides/automations/chaining-deployments-with-events)

⌘I