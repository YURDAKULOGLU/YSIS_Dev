Events - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Automations

Events

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

* [Event specification](#event-specification)
* [Event grammar](#event-grammar)
* [Resources](#resources)
* [Respond to events](#respond-to-events)
* [Further reading](#further-reading)

Events can represent API calls, state transitions, or changes in your execution environment or infrastructure.
Events power several Prefect features, including flow run logs and [automations](/v3/concepts/automations).
In Prefect Cloud, events power [audit logs](/v3/how-to-guides/cloud/manage-users/audit-logs).
You can manage events with the [Prefect CLI](https://docs.prefect.io/v3/api-ref/cli/event), [Terraform provider](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/automation), or [Prefect API](https://app.prefect.cloud/api/docs#tag/Events).

## [​](#event-specification) Event specification

Events adhere to a structured [specification](https://app.prefect.cloud/api/docs#tag/Events).
![Prefect UI](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/event-spec.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=7b53476f445e37f4f704a19bb5573817)

| Name | Type | Required? | Description |
| --- | --- | --- | --- |
| occurred | String | yes | When the event happened |
| event | String | yes | Name of the event that happened |
| resource | Object | yes | Primary resource this event concerns |
| related | Array | no | List of additional Resources involved in this event |
| payload | Object | no | Open-ended set of data describing what happened |
| id | String | yes | Client-provided identifier of this event |
| follows | String | no | ID of an event that is known to have occurred prior to this one |

## [​](#event-grammar) Event grammar

Events can be named arbitrarily, but are recommended to follow a consistent and informative grammar. An event describes a resource and an action it took—
or that was taken—on that resource.
For example, events emitted automatically by Prefect objects take the following form:

Copy

```
prefect.block.write-method.called
prefect-cloud.automation.action.executed
prefect-cloud.user.logged-in
```

See how to [emit and use custom events](/v3/advanced/use-custom-event-grammar) to trigger automations.

## [​](#resources) Resources

Every event has a primary resource, which describes the object that emitted an event.
Resources are used as quasi-stable identifiers for sources of events, and are represented as dot-delimited strings.
For example:

Copy

```
prefect-cloud.automation.5b9c5c3d-6ca0-48d0-8331-79f4b65385b3.action.0
acme.user.kiki.elt_script_1
prefect.flow-run.e3755d32-cec5-42ca-9bcd-af236e308ba6
```

Resources can have additional arbitrary labels which can be used in event aggregation queries.
For example:

Copy

```
"resource": {
    "prefect.resource.id": "prefect-cloud.automation.5b9c5c3d-6ca0-48d0-8331-79f4b65385b3",
    "prefect-cloud.action.type": "call-webhook"
    }
```

Events may contain related resources, used to associate the event with other resources.
For example, a primary resource can act on or with another resource.
Here is an example of a related resource:

Copy

```
"resource": {
    "prefect.resource.id": "prefect-cloud.automation.5b9c5c3d-6ca0-48d0-8331-79f4b65385b3.action.0",
    "prefect-cloud.action.type": "call-webhook"
  },
"related": [
  {
      "prefect.resource.id": "prefect-cloud.automation.5b9c5c3d-6ca0-48d0-8331-79f4b65385b3",
      "prefect.resource.role": "automation",
      "prefect-cloud.name": "webhook_body_demo",
      "prefect-cloud.posture": "Reactive"
  }
]
```

## [​](#respond-to-events) Respond to events

From any event detail page, you can configure an [automation](/v3/concepts/automations) to trigger on
the observation of matching events—or a lack of matching events—by clicking the automate button in the overflow menu:
![Automation from event](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/ui/automation-from-event.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=968f24fb6ffab269039b09d05b3e58aa)
The default trigger configuration fires every time it sees an event with a matching resource identifier.
Advanced configuration is possible through [custom event triggers](/v3/concepts/event-triggers).

## [​](#further-reading) Further reading

* [How to create automations](/v3/how-to-guides/automations/creating-automations)
* [How to create webhooks](/v3/how-to-guides/cloud/create-a-webhook)

Was this page helpful?

YesNo

[Prefect server](/v3/concepts/server)[Automations](/v3/concepts/automations)

⌘I