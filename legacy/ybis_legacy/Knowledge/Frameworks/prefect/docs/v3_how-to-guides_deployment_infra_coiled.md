How to run flows on Coiled - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows on Coiled

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

* [Install and set up accounts](#install-and-set-up-accounts)
* [Create the Prefect push work pool](#create-the-prefect-push-work-pool)
* [Create flow and create deployment](#create-flow-and-create-deployment)
* [Dockerless execution](#dockerless-execution)
* [Configure hardware](#configure-hardware)
* [Extra: scale out](#extra%3A-scale-out)
* [Architecture: How does this work?](#architecture%3A-how-does-this-work)
* [FAQ](#faq)

This page provides a step-by-step guide to run Prefect flows in your own cloud
account using two technologies:

* [Serverless push work pools](/v3/how-to-guides/deployment_infra/serverless), which remove the need to
  host any always-on Prefect worker
* [Coiled](https://coiled.io?utm_source=prefect-docs), which manages cloud VMs such as
  ECS, Cloud Run, and ACI in your account ergonomically and accessibly.

This combination combines the cost efficiency and security
of a cloud VM with easy setup and zero-maintenance infrastructure.
Coiled is a for-profit service, but its free tier is usually enough for most
Prefect users. Coiled is provided by the makers of Dask. This video
walks through the steps in this article:



## [​](#install-and-set-up-accounts) Install and set up accounts

Copy

```
pip install prefect coiled prefect-coiled
```

If you haven’t used Prefect Cloud before, you’ll need to [create a Prefect account](https://app.prefect.cloud) and log in:

Copy

```
prefect cloud login
```

If you haven’t used Coiled before, you’ll need to [create a Coiled account](https://cloud.coiled.io/signup?utm_source=prefect-docs) and log in:

Copy

```
coiled login
```

and then connect Coiled to your cloud account (AWS, Google Cloud, or Azure) where Coiled will run your flows. You can either use our interactive setup CLI:

Copy

```
coiled setup
```

or via the web app UI at [cloud.coiled.io/settings/setup](https://cloud.coiled.io/settings/setup).

## [​](#create-the-prefect-push-work-pool) Create the Prefect push work pool

To create the push work pool:

Copy

```
prefect work-pool create --type coiled:push --provision-infra 'example-coiled-pool'
```

## [​](#create-flow-and-create-deployment) Create flow and create deployment

We write our flow in Python as normal, using the work pool `"example-coiled-pool"` that we created in the last step.

* example\_flow.py

Copy

```
#example_flow.py
from prefect import flow, task

@task
def f(n):
    return n**2

@task
def do_something(x):
    print(x)

@flow(log_prints=True)
def my_flow():
    print("Hello from your Prefect flow!")
    X = f.map(list(range(10)))
    do_something(X)
    return X


if __name__ == "__main__":
    my_flow.deploy(
        name="example-coiled-deployment",
        work_pool_name="example-coiled-pool",
        image="my-image",
    )
```

Copy

```
python example_flow.py
```

Here we specified the Docker image `”my-image”` that you would replace with your own image location. Alternatively, if you don’t enjoy working with Docker, see the section [Dockerless Execution](#dockerless-execution) below.
Our deployment is now launched and we can execute runs either on the command line using the command printed out:

Copy

```
prefect deployment run 'my-flow/example-coiled-deployment'
```

Or by going to the deployment at the URL that Prefect prints in the CLI.

## [​](#dockerless-execution) Dockerless execution

You don’t have to use Docker if you don’t want to. In our example above we used Docker to build an image locally and push up to our Docker image repository:

Copy

```
if __name__ == "__main__":
    my_flow.deploy(
        name="example-coiled-deployment",
        work_pool_name="example-coiled-pool",
        image="my-image",                       # <--------
    )
```

This works well if you and your team are familiar with Docker. However, if you’re not familiar, then it can cause confusion in a variety of ways:

* You may not have Docker installed
* You may be on a Mac, and be generating ARM-based Docker images for Intel-based cloud machines
* You may need to rebuild your Docker image each time you update libraries
* People on your team may not know how Docker works, limiting who can use Prefect

Because of this, Coiled also provides a Dockerless execution process that called [Package Sync](#how-environment-synchronization). Coiled can automatically inspect your local environment and build a remote cloud environment on the fly. This can be more ergonomic and accessible to everyone on the team.
To invoke this feature today you need to have both a Python file such as `example_flow.py` with your flow defined, and a `prefect.yaml` deployment configuration file .

* example\_flow.py
* prefect.yaml

Copy

```
from prefect import flow, task

@task
def foo(n):
    return n**2

@task
def do_something(x):
    print(x)

@flow(log_prints=True)
def my_flow():
    print("Hello from your Prefect flow!")
    X = foo.map(list(range(10)))
    do_something(X)
    return X
```

Copy

```
push:
- prefect_coiled.deployments.steps.build_package_sync_senv:
    id: coiled_senv

pull:
- prefect.deployments.steps.set_working_directory:
    directory: /scratch/batch

deployments:
- name: example-coiled-deploy
  build: null
  entrypoint: example_flow:my_flow
  work_pool:
    name: example-coiled-pool
    job_variables:
      software: '{{ coiled_senv.name }}'
```

You can deploy this flow to Prefect Cloud with the `prefect deploy` command, which makes it ready to run in the cloud.

Copy

```
prefect deploy --prefect-file prefect.yaml --all
```

You can then run this flow as follows:

Copy

```
prefect deployment run 'my-flow/example-coiled-deployment'
```

If the Docker example above didn’t work for you (for example because you didn’t have Docker installed, or because you have a Mac) then you may find this approach to be more robust.

## [​](#configure-hardware) Configure hardware

One of the great things about the cloud is that you can experiment with different kinds of machines. Need lots of memory? No problem. A big GPU? Of course! Want to try ARM architectures for cost efficiency? Sure!
If you’re using Coiled’s Dockerless framework you can specify the following variables in your `prefect.yaml` file:

Copy

```
job_variables:
  cpu: 16
  memory: 32GB
```

If you’re operating straight from Python you can add these as a keyword in the `.deploy` call.

Copy

```
my_flow.deploy(
    ...,
    job_variables={"cpu": 16, "memory": "32GB"}
)
```

For a full list of possible configuration options see [Coiled API Documentation](https://docs.coiled.io/user_guide/api.html?utm_source=prefect-docs#coiled-batch-run).

## [​](#extra:-scale-out) Extra: scale out

Coiled makes it simple to parallelize individual flows on distributed cloud hardware. The easiest way to do this is to annotate your Prefect tasks with the `@coiled.function` decorator.
Let’s modify our example from above:

Copy

```
from prefect import flow, task
import coiled                               # new!

@task
def f(n):
    return n**2

@task
@coiled.function(memory="64 GiB")           # new!
def do_something(x):
    print(x)

@flow(log_prints=True)
def my_flow():
    print("Hello from your Prefect flow!")
    X = f.map(list(range(10)))
```

If you’re using Docker, then you’ll have to rerun the Python script to rebuild the image. If you’re using the Dockerless approach, then you’ll need to redeploy your flow.

Copy

```
prefect deploy --prefect-file prefect.yaml --all
```

And then you can re-run things to see the new machines show up:

Copy

```
prefect deployment run 'my-flow/example-coiled-deployment'
```

## [​](#architecture:-how-does-this-work) Architecture: How does this work?

It’s important to know where work happens so that you can understand the security and cost implications involved.
Coiled runs flows on VMs spun up in *your* cloud account (this is why you had to setup Coiled with your cloud account earlier). This means that …

* You’ll be charged directly by your cloud provider for any computation used.
* Your data stays within your cloud account. Neither Prefect nor Coiled ever see your data.

Coiled uses raw VM services (like AWS EC2) rather than systems like Kubernetes or Fargate, which has both good and bad tradeoffs:

* **Bad:** there will be a 30-60 second spin-up time on any new flow.
* **Good:** there is no resting infrastructure like a Kubernetes controller or long-standing VM, so there are no standing costs when you aren’t actively running flows.
* **Good:** you can use any VM type available on the cloud, like big memory machines or GPUs.
* **Good:** there is no cloud infrastructure to maintain and keep up-to-date.
* **Good:** Raw VMs are cheap. They cost from 0.02to0.02 to 0.02to0.05 per CPU-hour.

See [Coiled Documentation](https://docs.coiled.io/user_guide/why.html?utm_source=prefect-docs) to learn more about Coiled architecture and design decisions.

## [​](#faq) FAQ

* **Q:** Where do my computations run?  
  **A:** Coiled deploys VMs inside your account.
* **Q:** Can anyone see my data?  
  **A:** Only you and people in your own cloud account.
* **Q:** When I update my software libraries how does that software get on my cloud machines?  
  **A:** If you’re using Docker then you handle this. Otherwise, when you redeploy your flow Coiled scans your local Python environment and ships a specification of all libraries you’re using, along with any local .py files you have lying around. These live in a secure S3 bucket while waiting for your VMs.
* **Q:** How much does this cost?  
  **A:** You’ll have to pay your cloud provider for compute that you use. Additionally, if you use more than 10,000 CPU-hours per month, you’ll have to pay Coiled $0.05 per CPU-hour.  
  The average cost we see of Prefect flows is less than $0.02.
* **Q:** Will this leave expensive things running in my cloud account?  
  **A:** No. We clean everything up very thoroughly (VMs, storage, …) It is safe to try and cheap to run.
* **Q:** What permissions do I need to give Coiled?  
  **A:** In the [cloud setup process above](#install-and-setup-accounts) you give us permissions to do things like turn on and off VMs, set up security groups, and put logs into your cloud logging systems. You do not give us any access to your data.  
  Coiled is happy to talk briefly to your IT group if they’re concerned. Reach out at [support@coiled.io](mailto:support@coiled.io)

Was this page helpful?

YesNo

[Run flows on Modal](/v3/how-to-guides/deployment_infra/modal)[Connect to Prefect Cloud](/v3/how-to-guides/cloud/connect-to-cloud)

⌘I