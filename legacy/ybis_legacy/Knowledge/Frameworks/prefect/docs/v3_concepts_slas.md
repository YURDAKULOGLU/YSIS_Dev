Measure reliability with Service Level Agreements - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Cloud

Measure reliability with Service Level Agreements

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

* [Overview](/v3/concepts)

##### Workflows

* [Flows](/v3/concepts/flows)
* [Tasks](/v3/concepts/tasks)
* [Assets](/v3/concepts/assets)
* [Caching](/v3/concepts/caching)
* [States](/v3/concepts/states)
* [Runtime context](/v3/concepts/runtime-context)
* [Artifacts](/v3/concepts/artifacts)
* [Task runners](/v3/concepts/task-runners)
* [Global concurrency limits](/v3/concepts/global-concurrency-limits)
* [Tag-based concurrency limits](/v3/concepts/tag-based-concurrency-limits)

##### Deployments

* [Deployments](/v3/concepts/deployments)
* [Schedules](/v3/concepts/schedules)
* [Work pools](/v3/concepts/work-pools)
* [Workers](/v3/concepts/workers)

##### Configuration

* [Variables](/v3/concepts/variables)
* [Blocks](/v3/concepts/blocks)
* [Settings and profiles](/v3/concepts/settings-and-profiles)
* [Prefect server](/v3/concepts/server)

##### Automations

* [Events](/v3/concepts/events)
* [Automations](/v3/concepts/automations)
* [Event triggers](/v3/concepts/event-triggers)

##### Prefect Cloud

* [Rate limits and data retention](/v3/concepts/rate-limits)
* [SLAs](/v3/concepts/slas)
* [Webhooks](/v3/concepts/webhooks)

On this page

* [Prerequisites](#prerequisites)
* [Service Level Agreements](#service-level-agreements)
* [Defining SLAs](#defining-slas)
* [Types of SLAs](#types-of-slas)
* [Time to Completion SLA](#time-to-completion-sla)
* [Frequency SLA](#frequency-sla)
* [Lateness SLA](#lateness-sla)
* [Monitoring SLAs](#monitoring-slas)
* [Setting up an automation](#setting-up-an-automation)

**Experimental:** This feature is experimental and may change in the future.

## [​](#prerequisites) Prerequisites

* Prefect Client Version 3.1.12 or later
* Prefect Cloud account (SLAs are only available in Prefect Cloud)
* (If using Terraform) [Prefect Terraform Provider](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs) version 2.22.0 or later

## [​](#service-level-agreements) Service Level Agreements

 Service Level Agreements (SLAs) help you set and monitor performance standards for your data stack. By establishing specific thresholds for flow runs on your Deployments, you can automatically detect when your system isn’t meeting expectations.
When you set up an SLA, you define specific performance criteria - such as a maximum runtime of 10 minutes for a flow. If a flow run exceeds this threshold, the system generates an alert event. You can then use these events to trigger automated responses, whether that’s sending notifications to your team or initiating other corrective actions through automations.

## [​](#defining-slas) Defining SLAs

To define an SLA you can add it to the deployment through a `prefect.yaml` file, a `.deploy` method, or the CLI:

Defining SLAs in your prefect.yaml file

prefect.yaml SLA

Copy

```
deployments:
  my-deployment:
    sla:
        - name: "time-to-completion"
          duration: 10
          severity: "high"
        - name: "lateness"
          within: 600
          severity: "high"
```

Defining SLAs using a .deploy method

.deploy SLA

Copy

```
    from prefect import flow
    from prefect._experimental.sla.objects import TimeToCompletionSla, LatenessSla, FrequencySla

    @flow
    def my_flow():
        pass

    flow.from_source(
        source=source,
        entrypoint="my_file.py:my_flow",
    ).deploy(
        name="my-deployment",
        work_pool_name="my_pool",
        _sla=[
            TimeToCompletionSla(name="my-time-to-completion-sla", duration=30, severity="high"),
            LatenessSla(name="my-lateness-sla", within=timedelta(minutes=10), severity="high"),
            FrequencySla(name="my-frequency-sla", stale_after=timedelta(hours=1), severity="high"),
        ]
    )
```

Defining SLAs with the Prefect CLI

CLI SLA

Copy

```
prefect deploy --sla '{"name": "my-time-to-completion-sla", "duration": 10, "severity": "high"}'
```

Defining SLAs with the Terraform Provider

Terraform Provider

Copy

```
provider "prefect" {}

resource "prefect_flow" "my_flow" {
  name = "my-flow"
}

resource "prefect_deployment" "my_deployment" {
  name    = "my-deployment"
  flow_id = prefect_flow.my_flow.id
}

resource "prefect_resource_sla" "slas" {
  resource_id = "prefect.deployment.${prefect_deployment.my_deployment.id}"
  slas = [
    {
      name     = "my-time-to-completion-sla"
      severity = "high"
      duration = 30
    },
    {
      name     = "my-lateness-sla"
      severity = "high"
      within   = 600
    },
    {
      name        = "my-frequency-sla"
      severity    = "high"
      stale_after = 3600
    }
  ]
}
```

## [​](#types-of-slas) Types of SLAs

### [​](#time-to-completion-sla) Time to Completion SLA

A Time to Completion SLA describes how long flow runs should take and the severity of going over that duration.
The SLA is triggered when a flow run takes longer than the specified duration to complete.
The Time to Completion SLA requires one unique parameter:

* `duration`: The maximum allowed duration in seconds before the SLA is violated

This SLA is useful for monitoring long-running flows and ensuring they complete within an expected timeframe.
For example, if you set a Time to Completion SLA on your deployment with a `duration` of 600 seconds (10 minutes) the backend will emit an `prefect.sla.violation` event if a flow run does not complete within that timeframe.

### [​](#frequency-sla) Frequency SLA

A Frequency SLA describes the interval a deployment should run at and the severity of missing that interval.
The Frequency SLA requires one unique parameter:

* `stale_after`: The maximum allowed time between flow runs (e.g. `1 hour` for hourly jobs)

For example, if you have a deployment that should run every hour, you can set up a Frequency SLA with a `stale_after` of 1 hour.
This SLA triggers when more than an hour passes between `Completed` flow runs.

### [​](#lateness-sla) Lateness SLA

A Lateness SLA describes the severity of a flow run failing to start at its scheduled time.
The Lateness SLA requires one unique parameter:

* `within`: The amount of startup time allotted to a flow run before the SLA is violated.

For example, if a deployment is scheduled to run every day at 10am, and has a Lateness SLA of 5 minutes, the backend will emit an SLA violation event if a flow run does not start by 10:05am.

## [​](#monitoring-slas) Monitoring SLAs

You can monitor SLAs in the Prefect Cloud UI. On the runs page you can see the SLA status in the top level metrics:
![SLA status](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/sla-overview.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=1e48e62b8e670119d56a333ca3561e16)

## [​](#setting-up-an-automation) Setting up an automation

To set up an automation to notify a team or to take other actions when an SLA is triggered, you can use the [automations](/v3/automate/events/automations-triggers) feature. To create the automation first you’ll need to create a trigger.

1. Choose trigger type ‘Custom’.
2. Choose any event matching: `prefect.sla.violation`
3. For “From the Following Resources” choose: `prefect.flow-run.*`

![Create an automation](https://mintcdn.com/prefect-bd373955/rT_XiX8cZI7Bzt5c/v3/img/ui/sla-trigger-automation.png?fit=max&auto=format&n=rT_XiX8cZI7Bzt5c&q=85&s=9dca987a16c4d0c5501c7e87b9d33c04)
After creating the trigger, you can create an automation to notify a team or to take other actions when an SLA is triggered using [automations](/v3/automate/events/automations-triggers).

Was this page helpful?

YesNo

[Rate limits and data retention](/v3/concepts/rate-limits)[Webhooks](/v3/concepts/webhooks)

⌘I