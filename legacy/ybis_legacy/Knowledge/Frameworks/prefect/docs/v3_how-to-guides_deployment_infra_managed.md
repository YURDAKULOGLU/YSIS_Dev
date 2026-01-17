How to run flows on Prefect Managed infrastructure - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows on Prefect Managed infrastructure

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

* [Create a managed deployment](#create-a-managed-deployment)
* [Add dependencies](#add-dependencies)
* [Networking](#networking)
* [Static Outbound IP addresses](#static-outbound-ip-addresses)
* [Images](#images)
* [Code storage](#code-storage)
* [Resources & Limitations](#resources-%26-limitations)
* [Next steps](#next-steps)

Prefect Cloud can run your flows on your behalf with Prefect Managed work pools.
Flows that run with this work pool do not require a worker or cloud provider
account—Prefect handles the infrastructure and code execution for you.
Managed execution is a great option for users who want to get started quickly, with no infrastructure setup.

## [​](#create-a-managed-deployment) Create a managed deployment

1. Create a new work pool of type Prefect Managed in the UI or the CLI.
   Use this command to create a new work pool using the CLI:

   Copy

   ```
   prefect work-pool create my-managed-pool --type prefect:managed
   ```
2. Create a deployment using the flow `deploy` method or `prefect.yaml`.
   Specify the name of your managed work pool, as shown in this example that uses the `deploy` method:

   managed-execution.py

   Copy

   ```
   from prefect import flow

   if __name__ == "__main__":
       flow.from_source(
           source="https://github.com/prefecthq/demo.git",
           entrypoint="flow.py:my_flow",
       ).deploy(
           name="test-managed-flow",
           work_pool_name="my-managed-pool",
       )
   ```
3. With your [CLI authenticated to your Prefect Cloud workspace](/v3/how-to-guides/cloud/manage-users/api-keys), run the script to create your deployment:

   Copy

   ```
   python managed-execution.py
   ```
4. Run the deployment from the UI or from the CLI.
   This process runs a flow on remote infrastructure without any infrastructure setup, starting a worker, or requiring a cloud provider account.

## [​](#add-dependencies) Add dependencies

Prefect can install Python packages in the container that runs your flow at runtime.
Specify these dependencies in the **Pip Packages** field in the UI, or by configuring
`job_variables={"pip_packages": ["pandas", "prefect-aws"]}` in your deployment creation like this:

Copy

```
from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/prefecthq/demo.git",
        entrypoint="flow.py:my_flow",
    ).deploy(
        name="test-managed-flow",
        work_pool_name="my-managed-pool",
        job_variables={"pip_packages": ["pandas", "prefect-aws"]}
    )
```

Alternatively, you can create a `requirements.txt` file and reference it in your [prefect.yaml pull step](/v3/deploy/infrastructure-concepts/prefect-yaml#utility-steps).

## [​](#networking) Networking

### [​](#static-outbound-ip-addresses) Static Outbound IP addresses

Flows running on Prefect Managed infrastructure can be assigned static IP addresses on outbound traffic, which will pose as the `source` address for requests interacting with your system or database.
Include these `source` addresses in your firewall rules to explicitly allow flows to communicate with your environment.

* `184.73.85.134`
* `52.4.218.198`
* `44.217.117.74`

### [​](#images) Images

Managed execution requires that you run an official Prefect Docker image, such as `prefecthq/prefect:3-latest`.
However, as noted above, you can install Python package dependencies at runtime.
If you need to use your own image, we recommend using another type of work pool.

### [​](#code-storage) Code storage

You must store flow code in an accessible remote location.
Prefect supports git-based cloud providers such as GitHub, Bitbucket, or GitLab.
Remote block-based storage is also supported, so S3, GCS, and Azure Blob are additional code storage options.

### [​](#resources-&-limitations) Resources & Limitations

All flow runs receive:

* 4vCPUs
* 16GB of RAM
* 128GB of ephemeral storage

Maximum flow run time is limited to 24 hours.
Every account has a compute usage limit per workspace that resets monthly. Compute used is defined as the duration
between compute startup and teardown, rounded up to the nearest minute. This is approximately, although not exactly,
the duration of a flow run going from `PENDING` to `COMPLETED`.

## [​](#next-steps) Next steps

Read more about creating deployments in [Run flows in Docker containers](/v3/how-to-guides/deployment_infra/docker).
For more control over your infrastructure, such as the ability to run
custom Docker images, [serverless push work pools](/v3/how-to-guides/deployment_infra/serverless)
are a good option.

Was this page helpful?

YesNo

[Run Flows in Local Processes](/v3/how-to-guides/deployment_infra/run-flows-in-local-processes)[Run flows on serverless compute](/v3/how-to-guides/deployment_infra/serverless)

⌘I