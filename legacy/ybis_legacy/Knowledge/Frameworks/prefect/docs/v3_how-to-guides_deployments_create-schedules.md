How to create schedules - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

How to create schedules

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

* [Create schedules in the UI](#create-schedules-in-the-ui)
* [Create schedules in Python](#create-schedules-in-python)
* [Create schedules with the CLI](#create-schedules-with-the-cli)
* [Create schedules in YAML](#create-schedules-in-yaml)
* [Create schedules with Terraform](#create-schedules-with-terraform)
* [Associate parameters with schedules](#associate-parameters-with-schedules)
* [Schedule parameters in Python](#schedule-parameters-in-python)
* [Schedule parameters in prefect.yaml](#schedule-parameters-in-prefect-yaml)
* [See also](#see-also)

There are several ways to create a schedule for a deployment:

* Through the Prefect UI
* With the `cron`, `interval`, or `rrule` parameters if building your deployment with the
  [`serve` method](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes#serve-a-flow) of the `Flow` object or
  [the `serve` utility](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes#serve-multiple-flows-at-once) for managing multiple flows simultaneously
* If using [worker-based deployments](/v3/deploy/infrastructure-concepts/workers)
  + When you define a deployment with `flow.serve` or `flow.deploy`
  + Through the interactive `prefect deploy` command
  + With the `deployments` -> `schedules` section of the `prefect.yaml` file

### [​](#create-schedules-in-the-ui) Create schedules in the UI

You can add schedules in the **Schedules** section of a **Deployment** page in the UI.
To add a schedule select the **+ Schedule** button.
Choose **Interval** or **Cron** to create a schedule.

**What about RRule?**
The UI does not support creating RRule schedules.
However, the UI will display RRule schedules that you’ve created through the command line.

The new schedule appears on the **Deployment** page where you created it.
New scheduled flow runs are visible in the **Upcoming** tab of the **Deployment** page.
To edit an existing schedule, select **Edit** from the three-dot menu next to a schedule on a **Deployment** page.

### [​](#create-schedules-in-python) Create schedules in Python

Specify the schedule when you create a deployment in a Python file with `flow.serve()`, `serve`, `flow.deploy()`, or `deploy`.
Just add the keyword argument `cron`, `interval`, or `rrule`.

| Argument | Description |
| --- | --- |
| `interval` | An interval on which to execute the deployment. Accepts a number or a timedelta object to create a single schedule. If a number is given, it is interpreted as seconds. Also accepts an iterable of numbers or timedelta to create multiple schedules. |
| `cron` | A cron schedule string of when to execute runs of this deployment. Also accepts an iterable of cron schedule strings to create multiple schedules. |
| `rrule` | An rrule schedule string of when to execute runs of this deployment. Also accepts an iterable of rrule schedule strings to create multiple schedules. |
| `schedules` | A list of schedule objects defining when to execute runs of this deployment. Used to define multiple schedules or additional scheduling options such as `timezone`. |
| `schedule` | A schedule object defining when to execute runs of this deployment. Used to define additional scheduling options such as `timezone`. |
| `slug` | An optional unique identifier for the schedule containing only lowercase letters, numbers, and hyphens. If not provided for a given schedule, the schedule will be unnamed. |

The `serve` method below will create a deployment of `my_flow` with a cron schedule that creates runs every minute of every day:

Copy

```
from prefect import flow

from myproject.flows import my_flow

my_flow.serve(name="flowing", cron="* * * * *")
```

If using deployments with [dynamic infrastructure](/v3/deploy/infrastructure-concepts/work-pools), the `deploy` method has the same schedule-based parameters.
When `my_flow` is served with this interval schedule, it will run every 10 minutes beginning at midnight on January, 1, 2026 in the `America/Chicago` timezone:

prefect >= 3.1.16

prefect < 3.1.16

Copy

```
from datetime import timedelta, datetime
from prefect.schedules import Interval

from myproject.flows import my_flow

my_flow.serve(
  name="flowing",
  schedule=Interval(
    timedelta(minutes=10),
    anchor_date=datetime(2026, 1, 1, 0, 0),
    timezone="America/Chicago"
  )
)
```

Keyword arguments for schedules are also accepted by the `to_deployment` method that converts a flow to a deployment.

### [​](#create-schedules-with-the-cli) Create schedules with the CLI

You can create a schedule through the interactive `prefect deploy` command. You will be prompted to choose which type of schedule to create.
You can also create schedules for existing deployments using the `prefect deployment schedule create` command. This command allows you to specify schedule details directly without going through the interactive flow.

By default `prefect deployment schedule create` adds *additional* schedules to your deployment.
Use the `--replace` flag to remove old schedules and update with the new one.

**Examples:**
Create a cron schedule that runs every day at 9 AM:

Copy

```
prefect deployment schedule create my-deployment --cron "0 9 * * *"
```

Create an interval schedule that runs every 30 minutes:

Copy

```
prefect deployment schedule create my-deployment --interval 1800
```

Create a schedule with a specific timezone:

Copy

```
prefect deployment schedule create my-deployment --cron "0 9 * * *" --timezone "America/New_York"
```

Replace all existing schedules with a new one:

Copy

```
prefect deployment schedule create my-deployment --cron "0 9 * * *" --replace
```

### [​](#create-schedules-in-yaml) Create schedules in YAML

If you save the `prefect.yaml` file from the `prefect deploy` command, you will see it has a `schedules` section for your deployment.
Alternatively, you can create a `prefect.yaml` file from a recipe or from scratch and add a `schedules` section to it.

Copy

```
deployments:
  ...
  schedules:
    - cron: "0 0 * * *"
      slug: "chicago-schedule"
      timezone: "America/Chicago"
      active: false
    - cron: "0 12 * * *"
      slug: "new-york-schedule"
      timezone: "America/New_York"
      active: true
    - cron: "0 18 * * *"
      slug: "london-schedule"
      timezone: "Europe/London"
      active: true
```

### [​](#create-schedules-with-terraform) Create schedules with Terraform

You can manage schedules with the [Terraform provider for Prefect](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/deployment).

## [​](#associate-parameters-with-schedules) Associate parameters with schedules

Using any of the above methods to create a schedule, you can bind parameters to your schedules.
For example, say you have a flow that sends an email.
Every day at 8:00 AM you want to send a message to one recipient, and at 8:05 AM you want to send a different message to another recipient.
Instead of creating independent deployments with different default parameters and schedules, you can bind parameters to the schedules themselves:

### [​](#schedule-parameters-in-python) Schedule parameters in Python

Whether using `.serve` or `.deploy`, you can pass `parameters` to your deployment `schedules`:

send\_email\_flow.py

Copy

```
from prefect import flow
from prefect.schedules import Cron

@flow
def send_email(to: str, message: str = "Stop goofing off!"):
    print(f"Sending email to {to} with message: {message}")

send_email.serve(
  name="my-flow",
  schedules=[
    Cron(
      "0 8 * * *",
      slug="jim-email",
      parameters={"to": "jim.halpert@dundermifflin.com"}
    ),
    Cron(
      "5 8 * * *",
      slug="dwight-email",
      parameters={
        "to": "dwight.schrute@dundermifflin.com",
        "message": "Stop goofing off! You're assistant _to_ the regional manager!"
      }
    )
  ]
)
```

Note that our flow has a default `message` parameter, but we’ve overridden it for the second schedule.
This deployment will schedule runs that:

* Send “Stop goofing off!” to Jim at 8:00 AM every day
* Send “Stop goofing off! You’re assistant *to* the regional manager!” to Dwight at 8:05 AM every day

Use the same pattern to bind parameters to any schedule type in `prefect.schedules`.
You can provide one schedule via the `schedule` kwarg or multiple schedules via `schedules`.

### [​](#schedule-parameters-in-prefect-yaml) Schedule parameters in `prefect.yaml`

You can also provide parameters to schedules in your `prefect.yaml` file.

prefect.yaml

Copy

```
deployments:
  name: send-email
  entrypoint: send_email_flow.py:send_email
  schedules:
    - cron: "0 8 * * *"
      slug: "jim-email"
      parameters:
        to: "jim.halpert@dundermifflin.com"
    - cron: "5 8 * * *"
      slug: "dwight-email"
      parameters:
        to: "dwight.schrute@dundermifflin.com"
        message: "Stop goofing off! You're assistant _to_ the regional manager!"
```

## [​](#see-also) See also

* [Manage deployment schedules](/v3/how-to-guides/deployments/manage-schedules) - Learn how to pause and resume deployment schedules
* [Schedules concept](/v3/concepts/schedules) - Deep dive into schedule types and options
* [Deployments](/v3/concepts/deployments) - Learn more about deployments

Was this page helpful?

YesNo

[Trigger ad-hoc deployment runs](/v3/how-to-guides/deployments/run-deployments)[Manage Deployment schedules](/v3/how-to-guides/deployments/manage-schedules)

⌘I