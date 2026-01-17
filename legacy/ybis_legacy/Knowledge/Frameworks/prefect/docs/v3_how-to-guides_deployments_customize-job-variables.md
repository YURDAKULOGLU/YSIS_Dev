How to override job configuration for specific deployments - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

How to override job configuration for specific deployments

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

* [Job variables](#job-variables)
* [Override job variables on a deployment](#override-job-variables-on-a-deployment)
* [Use a prefect.yaml file](#use-a-prefect-yaml-file)
* [Hard-coded job variables](#hard-coded-job-variables)
* [Use existing environment variables](#use-existing-environment-variables)
* [Use the .deploy() method](#use-the-deploy-method)
* [Override job variables on a flow run](#override-job-variables-on-a-flow-run)
* [Use the custom run form in the UI](#use-the-custom-run-form-in-the-ui)
* [Use the CLI](#use-the-cli)
* [Use job variables in Terraform](#use-job-variables-in-terraform)
* [Use job variables in automations](#use-job-variables-in-automations)

There are two ways to deploy flows to work pools: with a [`prefect.yaml` file](/v3/deploy/infrastructure-concepts/prefect-yaml) or using the [Python `deploy` method](/v3/deploy/infrastructure-concepts/deploy-via-python).
In both cases, you can add or override job variables to the work pool’s defaults for a given deployment.
You can override both a work pool and a deployment when a flow run is triggered.
This guide explores common patterns for overriding job variables in
both deployment methods.

## [​](#job-variables) Job variables

Job variables are infrastructure-related values that are configurable on a work pool.
You can override job variables on a per-deployment or
per-flow run basis. This allows you to dynamically change infrastructure from the work pool’s defaults.
For example, when you create or edit a work pool, you can specify a set of environment variables to set in the
runtime environment of the flow run.
You could set the following value in the `env` field of any work pool:

Copy

```
{
  "EXECUTION_ENV": "staging",
  "MY_NOT_SO_SECRET_CONFIG": "plumbus",
}
```

Rather than hardcoding these values into your work pool in the UI (and making them available to all
deployments associated with that work pool), you can override these values for a specific deployment.

## [​](#override-job-variables-on-a-deployment) Override job variables on a deployment

Here’s an example repo structure:

Copy

```
» tree
.
|── README.md
|── requirements.txt
|── demo_project
|   |── daily_flow.py
```

With a `demo_flow.py` file like:

Copy

```
import os
from prefect import flow, task


@task
def do_something_important(not_so_secret_value: str) -> None:
    print(f"Doing something important with {not_so_secret_value}!")


@flow(log_prints=True)
def some_work():
    environment = os.environ.get("EXECUTION_ENVIRONMENT", "local")
    
    print(f"Coming to you live from {environment}!")
    
    not_so_secret_value = os.environ.get("MY_NOT_SO_SECRET_CONFIG")
    
    if not_so_secret_value is None:
        raise ValueError("You forgot to set MY_NOT_SO_SECRET_CONFIG!")

    do_something_important(not_so_secret_value)
```

### [​](#use-a-prefect-yaml-file) Use a `prefect.yaml` file

Imagine you have the following deployment definition in a `prefect.yaml` file at the
root of your repository:

Copy

```
deployments:
- name: demo-deployment
  entrypoint: demo_project/demo_flow.py:some_work
  work_pool:
    name: local
  schedule: null
```

While not the focus of this guide, this deployment definition uses a default “global” `pull` step,
because one is not explicitly defined on the deployment. For reference, here’s what that would look like at
the top of the `prefect.yaml` file:

Copy

```
pull:
- prefect.deployments.steps.git_clone: &clone_repo
    repository: https://github.com/some-user/prefect-monorepo
    branch: main
```

#### [​](#hard-coded-job-variables) Hard-coded job variables

To provide the `EXECUTION_ENVIRONMENT` and `MY_NOT_SO_SECRET_CONFIG` environment variables to this deployment,
you can add a `job_variables` section to your deployment definition in the `prefect.yaml` file:

Copy

```
deployments:
- name: demo-deployment
  entrypoint: demo_project/demo_flow.py:some_work
  work_pool:
    name: local
    job_variables:
        env:
            EXECUTION_ENVIRONMENT: staging
            MY_NOT_SO_SECRET_CONFIG: plumbus
  schedule: null
```

Then run `prefect deploy -n demo-deployment` to deploy the flow with these job variables.
You should see the job variables in the `Configuration` tab of the deployment in the UI:
![Job variables in the UI](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/job-variables.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=b3ecc9849ed07d1db9e54180aec304e4)

#### [​](#use-existing-environment-variables) Use existing environment variables

To use environment variables that are already set in your local environment, you can template
these in the `prefect.yaml` file using the `{{ $ENV_VAR_NAME }}` syntax:

Copy

```
deployments:
- name: demo-deployment
  entrypoint: demo_project/demo_flow.py:some_work
  work_pool:
    name: local
    job_variables:
        env:
            EXECUTION_ENVIRONMENT: "{{ $EXECUTION_ENVIRONMENT }}"
            MY_NOT_SO_SECRET_CONFIG: "{{ $MY_NOT_SO_SECRET_CONFIG }}"
  schedule: null
```

This assumes that the machine where `prefect deploy` is run would have these environment variables set.

Copy

```
export EXECUTION_ENVIRONMENT=staging
export MY_NOT_SO_SECRET_CONFIG=plumbus
```

Run `prefect deploy -n demo-deployment` to deploy the flow with these job variables,
and you should see them in the UI under the `Configuration` tab.

### [​](#use-the-deploy-method) Use the `.deploy()` method

If you’re using the `.deploy()` method to deploy your flow, the process is similar. But instead of  
`prefect.yaml` defining the job variables, you can pass them as a dictionary to the `job_variables` argument
of the `.deploy()` method.
Add the following block to your `demo_project/daily_flow.py` file from the setup section:

Copy

```
if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/zzstoatzz/prefect-monorepo.git",
        entrypoint="src/demo_project/demo_flow.py:some_work"
    ).deploy(
        name="demo-deployment",
        work_pool_name="local", 
        job_variables={
            "env": {
                "EXECUTION_ENVIRONMENT": os.environ.get("EXECUTION_ENVIRONMENT", "local"),
                "MY_NOT_SO_SECRET_CONFIG": os.environ.get("MY_NOT_SO_SECRET_CONFIG")
            }
        }
    )
```

The above example works assuming a couple things:

* the machine where this script is run would have these environment variables set.

Copy

```
export EXECUTION_ENVIRONMENT=staging
export MY_NOT_SO_SECRET_CONFIG=plumbus
```

* `demo_project/daily_flow.py` *already exists* in the repository at the specified path

Run the script to deploy the flow with the specified job variables.

Copy

```
python demo_project/daily_flow.py
```

The job variables should be visible in the UI under the `Configuration` tab.
![Job variables in the UI](https://mintcdn.com/prefect-bd373955/rm4-_dTLtkmSX6eG/v3/img/guides/job-variables.png?fit=max&auto=format&n=rm4-_dTLtkmSX6eG&q=85&s=b3ecc9849ed07d1db9e54180aec304e4)

## [​](#override-job-variables-on-a-flow-run) Override job variables on a flow run

When running flows, you can pass in job variables that override any values set on the work pool or deployment.
Any interface that runs deployments can accept job variables.

### [​](#use-the-custom-run-form-in-the-ui) Use the custom run form in the UI

Custom runs allow you to pass in a dictionary of variables into your flow run infrastructure. Using the same
`env` example from above, you could do the following:
![Job variables through custom run](https://mintcdn.com/prefect-bd373955/dwD6EJObIjtIzwSC/v3/img/ui/deployment-job-variables.png?fit=max&auto=format&n=dwD6EJObIjtIzwSC&q=85&s=17edf6009b61e918e00e22f1a7eeee04)

### [​](#use-the-cli) Use the CLI

Similarly, runs kicked off through the CLI accept job variables with the `-jv` or `--job-variable` flag.

Copy

```
prefect deployment run \
  --id "fb8e3073-c449-474b-b993-851fe5e80e53" \
  --job-variable MY_NEW_ENV_VAR=42 \
  --job-variable HELLO=THERE
```

### [​](#use-job-variables-in-terraform) Use job variables in Terraform

You can manage job variables with the [Terraform provider for Prefect](https://registry.terraform.io/providers/PrefectHQ/prefect/latest/docs/resources/deployment).

### [​](#use-job-variables-in-automations) Use job variables in automations

Additionally, runs kicked off through automation actions can use job variables, including ones rendered from Jinja
templates.
![Job variables through automation action](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/ui/automations-action-job-variable.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=9d5df018b5b779875fdb8cba644b2562)

Was this page helpful?

YesNo

[Version Deployments](/v3/how-to-guides/deployments/versioning)[Store secrets](/v3/how-to-guides/configuration/store-secrets)

⌘I