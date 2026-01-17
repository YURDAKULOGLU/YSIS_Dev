Webhooks - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Cloud

Webhooks

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

* [Webhook Endpoints](#webhook-endpoints)
* [Webhook Authentication and Validation](#webhook-authentication-and-validation)
* [API key authentication](#api-key-authentication)
* [Account-level security enforcement](#account-level-security-enforcement)
* [Azure Event Grid subscriptions](#azure-event-grid-subscriptions)
* [Webhook Templates](#webhook-templates)
* [Static Webhook Events](#static-webhook-events)
* [Event fields that Prefect Cloud populates for you](#event-fields-that-prefect-cloud-populates-for-you)
* [Dynamic Webhook Events](#dynamic-webhook-events)
* [How HTTP request components are handled](#how-http-request-components-are-handled)
* [Accept Prefect events directly](#accept-prefect-events-directly)
* [Accepting CloudEvents](#accepting-cloudevents)
* [Managing Webhooks Programmatically](#managing-webhooks-programmatically)
* [Troubleshooting Webhook Configuration](#troubleshooting-webhook-configuration)

Prefect Cloud webhooks can receive, observe, and respond to events from other systems. Each webhook exposes a unique URL endpoint to receive events from other systems and transform them into Prefect [events](/v3/concepts/events) for use in [automations](/v3/automate/events/automations-triggers).
Webhooks are defined by two essential components: a unique URL and a template that translates incoming web requests to a Prefect event.

## [​](#webhook-endpoints) Webhook Endpoints

The webhook endpoints have randomly generated opaque URLs that do not divulge any information about your Prefect Cloud workspace. They are rooted at `https://api.prefect.cloud/hooks/`. For example: `https://api.prefect.cloud/hooks/AERylZ_uewzpDx-8fcweHQ`.
Prefect Cloud assigns this URL when you create a webhook; it cannot be set through the API. You may rotate your webhook URL at any time without losing the associated configuration.
All webhooks may accept requests with the most common HTTP methods:

* Use `GET`, `HEAD`, and `DELETE` for webhooks that define a static event template, or a template that does not depend on the *body* of the HTTP request. The headers of the request will be available for templates.
* Use `POST`, `PUT`, and `PATCH` when the webhook request includes a body. See [How HTTP request components are handled](#how-http-request-components-are-handled) for more details on how the body is parsed.

Prefect Cloud webhooks are deliberately quiet to the outside world, and only return a `204 No Content` response when they are successful (except in certain scenarios, [see below](#webhook-authentication-and-validation)) or a `400 Bad Request` error when there is any error interpreting the request. For more visibility when your webhooks fail, see the [Troubleshooting Webhook Configuration](#troubleshooting-webhook-configuration) section below.

## [​](#webhook-authentication-and-validation) Webhook Authentication and Validation

To enhance security, within a Prefect Cloud Pro or Enterprise tier account, you can assign a service account to a webhook. This feature provides an additional layer of security and is highly recommended, especially for enterprise environments.

### [​](#api-key-authentication) API key authentication

Webhooks can be associated with a service account, and the webhook endpoint will be authenticated using the service account’s API key.
To use API key authentication:

1. Create a service account or use an existing one.
2. Associate the service account with your webhook from the UI.
3. Include the API key in the `Authorization` header of your webhook requests:

   Copy

   ```
   Authorization: Bearer <your-api-key>
   ```

### [​](#account-level-security-enforcement) Account-level security enforcement

An account-level setting is available to enforce authentication on all webhooks. When enabled:

* All existing webhooks without an associated service account will be automatically disabled.
* New webhooks must be created with an associated service account.
* Existing webhooks must be updated to include a service account before they can be re-enabled.

### [​](#azure-event-grid-subscriptions) Azure Event Grid subscriptions

Prefect Cloud webhooks support [Azure Event Grid webhook event handlers](https://learn.microsoft.com/en-us/azure/event-grid/handler-webhooks), including handling the [endpoint validation steps](https://learn.microsoft.com/en-us/azure/event-grid/receive-events?source=recommendations#endpoint-validation). When Event Grid sends a validation request to Prefect Cloud, the webhook automatically responds with the necessary validation code, confirming endpoint ownership and validity.

## [​](#webhook-templates) Webhook Templates

The purpose of a webhook is to accept an HTTP request from another system and produce a Prefect event from it. You often have little control over the format of those requests, so Prefect’s webhook system gives you full configuration on how you turn those notifications from other systems into meaningful events in your Prefect Cloud workspace. The template you define for each webhook determines how individual components of the incoming HTTP request become the event name and resource labels of the resulting Prefect event.
When creating a webhook, you write this template in [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/templates/). All of the built-in Jinja2 blocks and filters are available, as well as the filters from the [`jinja2-humanize-extensions` package](https://pypi.org/project/jinja2-humanize-extension/).
Your goal when defining an event template is to produce a valid JSON object that defines (at minimum) the `event` name and the `resource["prefect.resource.id"]`, which are required of all events. The simplest template is one in which these are statically defined.

**Make sure to produce valid JSON**The output of your template, when rendered, should be a valid string that can be parsed, for example, with `json.loads`.

### [​](#static-webhook-events) Static Webhook Events

Here’s a static webhook template example that notifies Prefect when your `recommendations` machine learning model has been updated. Those models are produced on a daily schedule by another team that is using `cron` for scheduling. They aren’t able to use Prefect for their flows yet, but they are happy to add a `curl` to the end of their daily script to notify you. Because this webhook is only used for a single event from a single resource, your template can be entirely static:

Copy

```
{
    "event": "model.refreshed",
    "resource": {
        "prefect.resource.id": "product.models.recommendations",
        "prefect.resource.name": "Recommendations [Products]",
        "producing-team": "Data Science"
    }
}
```

A webhook with this template may be invoked through *any* of the HTTP methods, including a `GET` request with no body, so the team you are integrating with can include this line at the end of their daily script:

Copy

```
curl https://api.prefect.cloud/hooks/AERylZ_uewzpDx-8fcweHQ
```

Each time the script hits the webhook, the webhook produces a single Prefect event with that name and resource in your workspace.

### [​](#event-fields-that-prefect-cloud-populates-for-you) Event fields that Prefect Cloud populates for you

You only had to provide the `event` and `resource` definition, which is not a completely fleshed out event. Prefect Cloud sets default values for any missing fields, such as `occurred` and `id`, so you don’t need to set them in your template. Additionally, Prefect Cloud adds the webhook itself as a related resource on all of the events it produces.
If your template does not produce a `payload` field, the `payload` defaults to a standard set of debugging information, including the HTTP method, headers, and body.

### [​](#dynamic-webhook-events) Dynamic Webhook Events

Let’s say that after a few days you and the Data Science team are getting a lot of value from the automations you have set up with the static webhook. You’ve agreed to upgrade this webhook to handle all of the various models that the team produces. It’s time to add some dynamic information to your webhook template.
Your colleagues on the team have adjusted their daily `cron` scripts to `POST` a small body that includes the ID and name of the model that was updated:

Copy

```
curl \
    -d "model=recommendations" \
    -d "friendly_name=Recommendations%20[Products]" \
    -X POST https://api.prefect.cloud/hooks/AERylZ_uewzpDx-8fcweHQ
```

This script sends a `POST` request and the body will include a traditional URL-encoded form with two fields describing the model that was updated: `model` and `friendly_name`. Here’s the webhook code that uses Jinja to receive these values in your template and produce different events for the different models:

Copy

```
{
    "event": "model.refreshed",
    "resource": {
        "prefect.resource.id": "product.models.{{ body.model }}",
        "prefect.resource.name": "{{ body.friendly_name }}",
        "producing-team": "Data Science"
    }
}
```

All subsequent `POST` requests will produce events with those variable resource IDs and names. The other statically defined parts, such as `event` or the `producing-team` label you included earlier, will still be used.

**Use Jinja2’s `default` filter to handle missing values**Jinja2 has a helpful [`default`](https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.default) filter that can compensate for missing values in the request. In this example, you may want to use the model’s ID in place of the friendly name when the friendly name is not provided: `{{ body.friendly_name|default(body.model) }}`.

### [​](#how-http-request-components-are-handled) How HTTP request components are handled

The Jinja2 template context includes the three parts of the incoming HTTP request:

* `method` is the uppercased string of the HTTP method, like `GET` or `POST`.
* `headers` is a case-insensitive dictionary of the HTTP headers included with the request. To prevent accidental disclosures, the `Authorization` header is removed.
* `body` represents the body that was posted to the webhook, with a best-effort approach to parse it into an object you can access.

HTTP headers are available without any alteration as a `dict`-like object, but you may access them with header names in any case. For example, these template expressions all return the value of the `Content-Length` header:

Copy

```
{{ headers['Content-Length'] }}

{{ headers['content-length'] }}

{{ headers['CoNtEnt-LeNgTh'] }}
```

The HTTP request body goes through some light preprocessing to make it more useful in templates. If the `Content-Type` of the request is `application/json`, the body will be parsed as a JSON object and made available to the webhook templates. If the `Content-Type` is `application/x-www-form-urlencoded` (as in our example above), the body is parsed into a flat `dict`-like object of key-value pairs. Jinja2 supports both index and attribute access to the fields of these objects, so the following two expressions are equivalent:

Copy

```
{{ body['friendly_name'] }}

{{ body.friendly_name }}
```

**Only for Python identifiers**Jinja2’s syntax only allows attribute-like access if the key is a valid Python identifier, so `body.friendly-name` will not work. Use `body['friendly-name']` in those cases.

Prefect Cloud will attempt to parse any other content type (such as `text/plain`) as if it were JSON first. In any case where the body cannot be transformed into JSON, it is made available to your templates as a Python `str`.

### [​](#accept-prefect-events-directly) Accept Prefect events directly

In cases where you have more control over the client, your webhook can accept Prefect events directly with a simple pass-through template:

Copy

```
{{ body|tojson }}
```

This template accepts the incoming body (assuming it was in JSON format) and passes it through unmodified. This allows a `POST` of a partial Prefect event as in this example:

Copy

```
POST /hooks/AERylZ_uewzpDx-8fcweHQ HTTP/1.1
Host: api.prefect.cloud
Content-Type: application/json
Content-Length: 228

{
    "event": "model.refreshed",
    "resource": {
        "prefect.resource.id": "product.models.recommendations",
        "prefect.resource.name": "Recommendations [Products]",
        "producing-team": "Data Science"
    }
}
```

The resulting event is filled out with the default values for `occurred`, `id`, and other fields as described [above](#event-fields-that-prefect-cloud-populates-for-you).

### [​](#accepting-cloudevents) Accepting CloudEvents

The [Cloud Native Computing Foundation](https://cncf.io) has standardized [CloudEvents](https://cloudevents.io) for use by systems to exchange event information in a common format. These events are supported by major cloud providers and a growing number of cloud-native systems. Prefect Cloud can interpret a webhook containing a CloudEvent natively with the following template:

Copy

```
{{ body|from_cloud_event(headers) }}
```

The resulting event uses the CloudEvent’s `subject` as the resource (or the `source` if no `subject` is available). The CloudEvent’s `data` attribute becomes the Prefect event’s `payload['data']`, and the other CloudEvent metadata will be at `payload['cloudevents']`. To handle CloudEvents in a more specific way tailored to your use case, use a dynamic template to interpret the incoming `body`.

## [​](#managing-webhooks-programmatically) Managing Webhooks Programmatically

In addition to [creating webhooks in the Prefect Cloud UI](/v3/how-to-guides/cloud/create-a-webhook), you can also manage them programmatically via the Prefect CLI, the Prefect Cloud API, or Terraform.

* **Prefect CLI**: Use the `prefect cloud webhook` command group. For example, to create a webhook:

  Copy

  ```
  prefect cloud webhook create your-webhook-name \
      --description "Receives webhooks from your system" \
      --template '{ "event": "your.event.name", "resource": { "prefect.resource.id": "your.resource.id" } }'
  ```

  Use `prefect cloud webhook --help` for more commands like `ls`, `get`, `toggle`, and `rotate`. For detailed template guidance, see [Webhook Templates](#webhook-templates).
* **Prefect Cloud API**: You can interact with webhook endpoints programmatically. Refer to the [API documentation](/v3/api-ref/rest-api/cloud) for available operations.
* **Terraform**: Use the [Prefect Terraform Provider](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/webhook) to manage webhooks as part of your infrastructure-as-code setup. This is particularly useful for versioning webhook configurations alongside other Prefect resources.

## [​](#troubleshooting-webhook-configuration) Troubleshooting Webhook Configuration

The initial configuration of your webhook may require some trial and error as you get the sender and your receiving webhook speaking a compatible language.
When Prefect Cloud encounters an error during receipt of a webhook, it produces a `prefect-cloud.webhook.failed` event in your workspace. This event includes critical information about the HTTP method, headers, and body it received, as well as what the template rendered. Keep an eye out for these events when something goes wrong with webhook processing or template rendering. You can inspect these events in the [event feed](/v3/concepts/events) in the UI to understand what might have gone wrong.

Was this page helpful?

YesNo

[SLAs](/v3/concepts/slas)

⌘I