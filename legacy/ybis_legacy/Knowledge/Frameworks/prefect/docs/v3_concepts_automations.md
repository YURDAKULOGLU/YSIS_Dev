Automations - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Automations

Automations

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

* [Triggers](#triggers)
* [Actions](#actions)
* [Selected and inferred action targets](#selected-and-inferred-action-targets)
* [Sending notifications with automations](#sending-notifications-with-automations)
* [Templating with Jinja](#templating-with-jinja)
* [Further reading](#further-reading)

Automations enable you to configure [actions](#actions) that execute automatically based on [trigger](#triggers) conditions.
Potential triggers include the occurrence of events from changes in a flow run’s state—or the absence of such events.
You can define your own custom trigger to fire based on a custom [event](/v3/concepts/event-triggers) defined in Python code.
With Prefect Cloud you can even create [webhooks](/v3/automate/events/webhook-triggers) that can receive data for use in actions.
Actions you can take upon a trigger include:

* creating flow runs from existing deployments
* pausing and resuming schedules or work pools
* sending custom notifications

### [​](#triggers) Triggers

Triggers specify the conditions under which your action should be performed. The Prefect UI includes templates for many
common conditions, such as:

* Flow run state change (Flow Run Tags are only evaluated with `OR` criteria)
* Work pool status
* Work queue status
* Deployment status
* Metric thresholds, such as average duration, lateness, or completion percentage
* Custom event triggers

Importantly, you can configure the triggers not only in reaction to events, but also proactively: in the absence of
an expected event.
![Configuring a trigger for an automation in Prefect Cloud.](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/automations-trigger.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=266fbeea3114360696a4adbc82eeac85)
For example, in the case of flow run state change triggers, you might expect production flows to finish in no longer
than thirty minutes. But transient infrastructure or network issues could cause your flow to get “stuck” in a running state.
A trigger could kick off an action if the flow stays in a running state for more than 30 minutes.
This action could be taken on the flow itself, such as cancelling or restarting it. Or the action could take the form of a
notification for someone to take manual remediation steps. Or you could set both actions to take place when the trigger occurs.

### [​](#actions) Actions

Actions specify what your automation does when its trigger criteria are met. Current action types include:

| Action | Type |
| --- | --- |
| Cancel a flow run | `cancel-flow-run` |
| Change the state of a flow run | `change-flow-run-state` |
| Suspend a flow run | `suspend-flow-run` |
| Resume a flow run | `resume-flow-run` |
| Run a deployment | `run-deployment` |
| Pause a deployment schedule | `pause-deployment` |
| Resume a deployment schedule | `resume-deployment` |
| Pause a work pool | `pause-work-pool` |
| Resume a work pool | `resume-work-pool` |
| Pause a work queue | `pause-work-queue` |
| Resume a work queue | `resume-work-queue` |
| Pause an automation | `pause-automation` |
| Resume an automation | `resume-automation` |
| Send a [notification](#sending-notifications-with-automations) | `send-notification` |
| Call a webhook | `call-webhook` |

![Configuring an action for an automation in Prefect Cloud.](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/ui/automations-action.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=16439f3f9b1614ab84454c79ccfda359)

### [​](#selected-and-inferred-action-targets) Selected and inferred action targets

Some actions require you to either select the target of the action, or specify that the target of the action should be
inferred. Selected targets are simple and useful for when you know exactly what object your action should act on. For
example, the case of a cleanup flow you want to run or a specific notification you want to send.
Inferred targets are deduced from the trigger itself.
For example, if a trigger fires on a flow run that is stuck in a running state, and the action is to cancel an inferred
flow run—the flow run that caused the trigger to fire.
Similarly, if a trigger fires on a work queue event and the corresponding action is to pause an inferred work queue, the
inferred work queue is the one that emitted the event.
Prefect infers the relevant event whenever possible, but sometimes one does not exist.
Specify a name and, optionally, a description for the automation.

## [​](#sending-notifications-with-automations) Sending notifications with automations

Automations support sending notifications through any predefined block that is capable of and configured
to send a message, including:

* Slack message to a channel
* Microsoft Teams message to a channel
* Email to an email address

![Configuring notifications for an automation in Prefect Cloud.](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/automations-notifications.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=43a44548667b7a594fff369d8040f54a)

## [​](#templating-with-jinja) Templating with Jinja

You can access templated variables with automation actions through [Jinja](https://palletsprojects.com/p/jinja/) syntax.
Templated variables enable you to dynamically include details from an automation trigger, such as a flow or pool name.
Jinja templated variable syntax wraps the variable name in double curly brackets, like this: `{{ variable }}`.
You can access properties of the underlying flow run objects including:

* [flow\_run](https://reference.prefect.io/prefect/server/schemas/core/#prefect.server.schemas.core.FlowRun)
* [flow](https://reference.prefect.io/prefect/server/schemas/core/#prefect.server.schemas.core.Flow)
* [deployment](https://reference.prefect.io/prefect/server/schemas/core/#prefect.server.schemas.core.Deployment)
* [work\_queue](https://reference.prefect.io/prefect/server/schemas/core/#prefect.server.schemas.core.WorkQueue)
* [work\_pool](https://reference.prefect.io/prefect/server/schemas/core/#prefect.server.schemas.core.WorkPool)

In addition to its native properties, each object includes an `id` along with `created` and `updated` timestamps.
The `flow_run|ui_url` token returns the URL to view the flow run in the UI.
Here’s an example relevant to a flow run state-based notification:

Copy

```
Flow run {{ flow_run.name }} entered state {{ flow_run.state.name }}.

    Timestamp: {{ flow_run.state.timestamp }}
    Flow ID: {{ flow_run.flow_id }}
    Flow Run ID: {{ flow_run.id }}
    State message: {{ flow_run.state.message }}
```

The resulting Slack webhook notification looks something like this:
![Configuring notifications for an automation in Prefect Cloud.](https://mintcdn.com/prefect-bd373955/rT_XiX8cZI7Bzt5c/v3/img/ui/templated-notification.png?fit=max&auto=format&n=rT_XiX8cZI7Bzt5c&q=85&s=d2072752b2ef7111879fd64ffd46c841)
You could include `flow` and `deployment` properties:

Copy

```
Flow run {{ flow_run.name }} for flow {{ flow.name }}
entered state {{ flow_run.state.name }}
with message {{ flow_run.state.message }}

Flow tags: {{ flow_run.tags }}
Deployment name: {{ deployment.name }}
Deployment version: {{ deployment.version }}
Deployment parameters: {{ deployment.parameters }}
```

An automation that reports on work pool status might include notifications using `work_pool` properties:

Copy

```
Work pool status alert!

Name: {{ work_pool.name }}
Last polled: {{ work_pool.last_polled }}
```

In addition to those shortcuts for flows, deployments, and work pools, you have access to the automation and the
event that triggered the automation. See the [Automations API](https://app.prefect.cloud/api/docs#tag/Automations)
for additional details.

Copy

```
Automation: {{ automation.name }}
Description: {{ automation.description }}

Event: {{ event.id }}
Resource:
{% for label, value in event.resource %}
{{ label }}: {{ value }}
{% endfor %}
Related Resources:
{% for related in event.related %}
    Role: {{ related.role }}
    {% for label, value in related %}
    {{ label }}: {{ value }}
    {% endfor %}
{% endfor %}
```

Note that this example also illustrates the ability to use Jinja features such as iterator and for loop
[control structures](https://jinja.palletsprojects.com/en/3.1.x/templates/#list-of-control-structures) when
templating notifications.
For more on the common use case of passing an upstream flow run’s parameters to the flow run invoked by the automation, see the [Passing parameters to a flow run](/v3/how-to-guides/automations/access-parameters-in-templates) guide.

## [​](#further-reading) Further reading

* To learn more about Prefect events, which can trigger automations, see the [events docs](/v3/concepts/events).
* See the [webhooks guide](/v3/how-to-guides/cloud/create-a-webhook)
  to learn how to create webhooks and receive external events.

Was this page helpful?

YesNo

[Events](/v3/concepts/events)[Event triggers](/v3/concepts/event-triggers)

⌘I