How to create a webhook - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Cloud

How to create a webhook

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

* [Trigger an Automation from an External Event](#trigger-an-automation-from-an-external-event)
* [1. Create a Webhook in the UI](#1-create-a-webhook-in-the-ui)
* [2. Invoke the Webhook Endpoint](#2-invoke-the-webhook-endpoint)
* [3. Observe the Event in Prefect Cloud](#3-observe-the-event-in-prefect-cloud)
* [4. Create an Automation from the Event](#4-create-an-automation-from-the-event)
* [Troubleshooting Event Reception](#troubleshooting-event-reception)
* [Further reading](#further-reading)

This page shows you how to quickly set up a webhook using the Prefect Cloud UI, invoke it, and create an automation based on the received event.

## [​](#trigger-an-automation-from-an-external-event) Trigger an Automation from an External Event

Here’s how to set up a webhook and trigger an automation using the Prefect Cloud UI.

### [​](#1-create-a-webhook-in-the-ui) 1. Create a Webhook in the UI

Navigate to the **Webhooks** page in Prefect Cloud and click **Create Webhook**.
You will need to provide a name for your webhook and a Jinja2 template. The template defines how the incoming HTTP request data is transformed into a Prefect event. For example, to capture a model ID and a friendly name from the request body:

Copy

```
{
    "event": "model-update",
    "resource": {
        "prefect.resource.id": "product.models.{{ body.model_id}}",
        "prefect.resource.name": "{{ body.friendly_name }}",
        "run_count": "{{body.run_count}}"
    }
}
```

This template will look for `model_id`, `friendly_name`, and `run_count` in the body of the incoming request.
![Create a webhook in the Prefect Cloud UI, showing the template editor.](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/webhook-simple.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=40ad34d41e5e706a624c91ed79312ff9)
After saving, Prefect Cloud will provide you with a unique URL for your webhook.

### [​](#2-invoke-the-webhook-endpoint) 2. Invoke the Webhook Endpoint

Use any HTTP client to send a `POST` request to the unique URL provided for your webhook. Include the data you want to pass in the request body. For the example template above:

Copy

```
curl -X POST https://api.prefect.cloud/hooks/YOUR_UNIQUE_WEBHOOK_ID \
  -d "model_id=my_model_123" \
  -d "friendly_name=My Awesome Model" \
  -d "run_count=15"
```

Replace `YOUR_UNIQUE_WEBHOOK_ID` with your actual webhook ID.

### [​](#3-observe-the-event-in-prefect-cloud) 3. Observe the Event in Prefect Cloud

After invoking the webhook, navigate to the **Event Feed** in Prefect Cloud. You should see a new event corresponding to your webhook invocation.
![Event feed in Prefect Cloud showing a newly created event from a webhook.](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/webhook-created.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=1a348eaf056244f5fe2d36a4bfc55417)

### [​](#4-create-an-automation-from-the-event) 4. Create an Automation from the Event

From the event details page (click on the event in the feed), you can click the **Automate** button.
![Event details page with the Automate button highlighted.](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/webhook-automate.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=2ff4522c881fa28f9ebcbb944e552b12)
This will pre-fill an automation trigger based on the event you just created.
![Automation trigger definition pre-filled from a webhook event.](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/automation-custom.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=b89876f934154273d59cf6778fb55d45)
Click **Next** to define the action(s) this automation should perform, such as running a deployment or sending a notification.

## [​](#troubleshooting-event-reception) Troubleshooting Event Reception

If you’ve invoked your webhook but don’t see the expected event in Prefect Cloud, or the event data isn’t what you anticipated:

* **Check the Event Feed**: Look for any events related to your webhook, even if they don’t match your exact expectations.
* **Look for `prefect-cloud.webhook.failed` events**: If Prefect Cloud encountered an error processing the webhook (e.g., an invalid template or malformed request), it will generate a `prefect-cloud.webhook.failed` event. This event contains details about the received request and any template rendering errors.
* **Verify your request**: Double-check the URL, HTTP method, headers, and body of the request you sent to the webhook.
* **Review your template**: Ensure your Jinja2 template correctly accesses the parts of the HTTP request you intend to use (e.g., `body.field_name`, `headers['Header-Name']`).

For more in-depth troubleshooting of webhook configuration and template rendering, see [Troubleshooting Webhook Configuration in the Concepts documentation](/v3/concepts/webhooks#troubleshooting-webhook-configuration).

## [​](#further-reading) Further reading

For more on webhooks, see the [Webhooks Concepts](/v3/concepts/webhooks) page.

Was this page helpful?

YesNo

[Manage Workspaces](/v3/how-to-guides/cloud/workspaces)[Troubleshoot Prefect Cloud](/v3/how-to-guides/cloud/troubleshoot-cloud)

⌘I