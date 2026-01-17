How to run flows on Modal - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows on Modal

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

* [Prerequisites](#prerequisites)
* [Create a GitHub repository](#create-a-github-repository)
* [Give Prefect access to your GitHub repository](#give-prefect-access-to-your-github-repository)
* [Connect Prefect and Modal](#connect-prefect-and-modal)
* [Configure CI/CD](#configure-ci%2Fcd)

Prefect is the world’s best orchestrator.
Modal is the world’s best serverless compute framework.
It only makes sense that they would fit together perfectly.
In this tutorial, you’ll build your first Prefect deployment that runs on Modal every hour, and create a scalable framework to grow your project.
Here’s an architecture diagram which shows what you’ll build.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/0.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=4a4e18e1bc8d72a7e70443c7c52dba23)
You’ll build a full serverless infrastructure framework for scheduling and provisioning workflows.
GitHub will act as the source of truth, Prefect will be the orchestrator, and Modal will be the serverless infrastructure.
You’ll only pay for the Modal CPU time you use.
First, here’s a recap of some important terms:

| Term | Definition |
| --- | --- |
| *Flow* | A Python function in a file, decorated with `@flow`, that is an entrypoint to perform a task in Prefect. |
| *Run* | An instance of a flow, executed at a specific time with a specific payload. |
| *Deployment* | A manifest around a flow, including where it should run, when it should run, and any variables it needs to run. A deployment can schedule your flows, creating runs when needed. |
| *Work Pool* | An interface to the hardware used to run a given flow. |

## [​](#prerequisites) Prerequisites

* A free [Prefect Cloud](https://app.prefect.cloud/auth/sign-in) account.
* A free [Modal](https://modal.com/signup?next=%2Fapps) account.

## [​](#create-a-github-repository) Create a GitHub repository

Create a GitHub repository containing your Prefect flows.
You can reference the [Ben-Epstein/prefect-modal](https://github.com/Ben-Epstein/prefect-modal) repository for a complete example.
Your repository should have a `prefect.yaml` deployment configuration file, standard Python tooling, and CI/CD.

1. Start by creating the following `Makefile` to keep things easy:

   Makefile

   Copy

   ```
   export PYTHONPATH = .venv

   .PHONY: uv
   uv:
     pip install --upgrade 'uv>=0.5.6,<0.6'
     uv venv

   setup:
     @if [ ! -d ".venv" ] || ! command -v uv > /dev/null; then \
       echo "UV not installed or .venv does not exist, running uv"; \
       make uv; \
     fi
     @if [ ! -f "uv.lock" ]; then \
       echo "Can't find lockfile. Locking"; \
       uv lock; \
     fi
     uv sync --all-extras --all-groups
     uv pip install --no-deps -e .
   ```
2. Set up and manage your environment with `uv`.

   Copy

   ```
   make setup
   ```
3. Create your Python project.

   Copy

   ```
   uv init --lib --name prefect_modal --python 3.12
   ```

   If `uv` creates a `python-version` that is pinned to a micro version (for example, 3.12.6), remove the micro version (for example, 3.12) to avoid downstream issues.
4. Add your dependencies:

   Copy

   ```
   uv add modal 'prefect[github]'
   ```
5. Add the following to the end of the `pyproject.toml` file created by `uv`:

   Copy

   ```
   [tool.hatch.build.targets.wheel]
   packages = ["src/prefect_modal"]
   ```
6. Initialize the Prefect environment:

   Copy

   ```
   uv run prefect init
   ```

   You will be prompted to choose your code storage; select `git` to store code within a git repository.
   ![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/1.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=3998fff07e902af8b6bc8539593bce2e)
7. Because this is meant to be a scalable repository, create a submodule just for your workflows.

   Copy

   ```
   mkdir src/prefect_modal/flows
   touch src/prefect_modal/flows/__init__.py
   ```

Now that your repository is set up, take a look at the `prefect.yaml` file that you generated.

prefect.yaml

Copy

```
# Welcome to your prefect.yaml file! You can use this file for storing and managing
# configuration for deploying your flows. We recommend committing this file to source
# control along with your flow code.

# Generic metadata about this project
name: prefect-modal
prefect-version: 3.1.15

# build section allows you to manage and build docker images
build: null

# push section allows you to manage if and how this project is uploaded to remote locations
push: null

# pull section allows you to provide instructions for cloning this project in remote locations
pull:
- prefect.deployments.steps.git_clone:
    repository: https://github.com/Ben-Epstein/prefect-modal
    branch: main
    access_token: null

# the deployments section allows you to provide configuration for deploying flows
deployments:
- name: null
  version: null
  tags: []
  description: null
  schedule: {}
  flow_name: null
  entrypoint: null
  parameters: {}
  work_pool:
    name: null
    work_queue_name: null
    job_variables: {}
```

The important sections here are `pull`, which defines the repository and branch to pull from, as well as `deployments`, which define the `flows` that will be `run` at some `schedule` on a `work_pool`.
The work pool will be set to modal later in this tutorial.
Finally, create your flow.

Copy

```
touch src/prefect_modal/flows/flow1.py
```

You can do anything in your flow, but use the following code to keep it simple.

src/prefect\_modal/flows/flow1.py

Copy

```
from prefect import flow, task

@task()
def do_print(param: str) -> None:
    print("Doing the task")
    print(param)

@flow(log_prints=True)
def run_my_flow(param: str) -> None:
    print("flow 2")
    do_print(param)

@flow(log_prints=True)
def main(name: str = "world", goodbye: bool = False):
    print(f"Hello {name} from Prefect! 🤗")
    run_my_flow(name)
    if goodbye:
        print(f"Goodbye {name}!")
```

## [​](#give-prefect-access-to-your-github-repository) Give Prefect access to your GitHub repository

First, authenticate to Prefect Cloud.

Copy

```
uv run prefect cloud login
```

You’ll need a Personal Access Token (PAT) for authentication.
For simplicity, use a classic token, but you can configure a fine-grained token if you want.
In GitHub, go to [Personal access tokens](https://github.com/settings/tokens) and click **Generate new token (classic)**.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/2.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=7c14394650d398bd359d940cea743757)
Give the token a name, an expiration date, and repository access.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/3.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=d5961a522ab8264b6cd2268731364fae)
Once you’ve created the token, copy it and give it to Prefect.
First, run:

Copy

```
# Register the block
uv run prefect block register -m prefect_github

# Create the block
uv run prefect block create prefect_github
```

The second command returns a URL.
Click that URL to give your block a name and paste in the token you got from GitHub.
Name the block `prefect-modal`.
In `prefect.yaml`, edit the `pull:` section as follows:

Copy

```
pull:
- prefect.deployments.steps.git_clone:
    id: clone-step
    repository: https://github.com/Ben-Epstein/prefect-modal
    branch: main
    credentials: '{{ prefect.blocks.github-credentials.prefect-modal }}'
```

* Replace the `access_token` key name with `credentials`.
* Change the repository name to the name of your repository.

Now, add the following section to configure how you install your package and what your working directory is:

Copy

```
- prefect.deployments.steps.run_shell_script:
    directory: '{{ clone-step.directory }}'
    script: pip install --upgrade 'uv>=0.5.6,<0.6'
- prefect.deployments.steps.run_shell_script:
    directory: '{{ clone-step.directory }}'
    script: uv sync --no-editable --no-dev
```

Typically, `uv sync` creates a new virtual environment.
The following steps show how to tell `uv` to use the root Python version.

This configuration tells Prefect how to download the code from GitHub into the Modal pod before running the flow.
This is important: you are telling Modal to load the code from `main`.
This means that if you push new code to main, the next run of a flow in Modal will change to whatever is in main.
To keep this stable, you can set that to a release branch, for example, to only update that release branch when you’re stable and ready.
Now, configure a few more options on the `deployment` to get it ready: `entrypoint`, `schedule`, and `description`.

Copy

```
  name: prefect-modal-example
  description: "Your first deployment which runs daily at 12:00 on Modal"
  entrypoint: prefect_modal.flows.flow1:main
  schedules:
  - cron: '0 12 * * *'
    timezone: America/New_York
    active: true
```

This schedule runs once a day at 12PM EST.
You can add another schedule by adding another list element.

Because you referenced the entrypoint as a module and not a path, you can call it from anywhere (as long as it’s installed).
This is much more flexible.

## [​](#connect-prefect-and-modal) Connect Prefect and Modal

You need to give Prefect access to your Modal account to provision a serverless instance to run your flows and tasks.
Modal will be the *Work Pool* in Prefect terms, remaining off when unused, and spinning up the infrastructure you need when a new flow run is scheduled.
Prefect makes this incredibly easy.
First, authenticate with Modal:

Copy

```
uv run modal setup
```

Next, create a token:

Copy

```
uv run modal token new
```

Finally, create a work pool:

Copy

```
uv run prefect work-pool create --type modal:push --provision-infra pref-modal-pool
```

The name `pref-modal-pool` in the last command is custom, you can name it whatever you want.
Take the work pool name and update your `prefect.yaml` file with it.

prefect.yaml

Copy

```
...
work_pool:
    name: "pref-modal-pool"
    work_queue_name: "default"
    job_variables: {
        "env": {"UV_PROJECT_ENVIRONMENT": "/usr/local"}
    }
```

This `UV_PROJECT_ENVIRONMENT` is how you tell uv to use the root python.
You could `pip install` without `uv` but it would be significantly slower (minutes instead of seconds) and you can’t leverage your lockfile, resulting in unexpected behavior!

You can create multiple work queues across the same pool (for example, if you have another job using this pool).
Multiple work queues let you handle concurrency and swim-lane priorities.
To keep things simple, this tutorial will use the the default queue name that comes with every new pool.
When you deploy to Prefect, it will know to schedule all of the flow runs for this particular deployment on your modal work pool!
At this point, you could `git add . && git commit -m "prefect modal" && git push` to get your code into GitHub, and then `uv run prefect deploy --all` to get your deployment live.
But first, learn how to automate Prefect deployments.

## [​](#configure-ci/cd) Configure CI/CD

Since the code must exist in GitHub in order for Modal to download, install, and run it, GitHub should also be the source of truth for telling Prefect what to do with the code.
First, create two secrets to add to the GitHub repository: `PREFECT_API_KEY` and `PREFECT_API_URL`.

1. For `PREFECT_API_URL`, the format is as follows: `https://api.prefect.cloud/api/accounts/{account_id}/workspaces/{workspace_id}`.
   Go to the Prefect Cloud Dashboard, and then extract the account ID and workspace ID from the URL.

   The Prefect console URL uses `/account` and `/workspace` but the API uses `/accounts` and `/workspaces`, respectively.
2. For `PREFECT_API_KEY`, go to the [API keys](https://app.prefect.cloud/my/api-keys) page and create a new API key.
   ![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/4.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=22db8bb67f9faa3f051f6a22994685ed)

Go to your repository, and then **Settings** / **Secrets and variables** / **Actions**.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/5.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=67f61f7362368a8fd4b163590e227bf3)
Click **New repository secret** to add these secrets to your GitHub repository.
Now, add a simple GitHub workflow.
Create a new folder in the root of your GitHub repository:

Copy

```
mkdir -p .github/workflows
```

Create a workflow file.

Copy

```
touch .github/workflows/prefect_cd.yaml
```

Add the following code to this workflow.

.github/workflows/prefect\_cd.yaml

Copy

```
name: Deploy Prefect flow

on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Prefect Deploy
        env:
          PREFECT_API_KEY: ${{ secrets.PREFECT_API_KEY }}
          PREFECT_API_URL: ${{ secrets.PREFECT_API_URL }}
        run: |
          make prefect-deploy
```

The `make prefect-deploy` command is used to deploy the flows in your deployment.

You can run `make prefect-deploy` locally at any time to keep your deployment up to date.

Add the following command to your `Makefile`.

Makefile

Copy

```
prefect-deploy: setup
    uv run prefect deploy --prefect-file prefect.yaml --all
```

Before pushing your code, run `make prefect-deploy` once to make sure everything works.
Prefect will suggest changes to `prefect.yaml`, which you should accept.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/6.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=e64a05a860e344c8c79a102b819569fe)
You let Prefect override your deployment spec, which allowed your CD to run without any interruptions or prompts.
If you go to the **Deployment** page in Prefect Cloud, you’ll see your deployment!
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/7.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=aeb05225ab1e4ec603edc49806adc51b)
There are no runs yet.
The output from `make prefect-deploy` shows the command to run your deployed flow.
However, since the code isn’t in GitHub yet, this will fail.
To fix this, push your code:

Copy

```
git push
```

Go to the repository in **GitHub**, and then open **Actions** to verify that your CI/CD is running successfully.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/8.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=7fa4a81f7489dd7e405a1d59c0af1c27)
You can see the flow run in Prefect Cloud as well.
The flow will run automatically at 12 PM, but you can also run it manually.
In a new browser tab, open your [Modal dashboard](https://modal.com/apps/) alongside your Prefect Cloud dashboard.
In your terminal, run the following command:

Copy

```
uv run prefect deployment run main/prefect-modal-example
```

You should see the run start in your Prefect dashboard.
In 30-60 seconds, you should see it run in Modal.
You can click on the run to see the logs.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/9.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=8db98eb8807965b3333dd36122bce457)
Click into the app and then click **App Logs** on the left to show everything that’s happening inside the flow run!
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/10.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=0ed44b69a5f58f0547d129ae1180e0c1)
Click on a specific log line to get more details.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/11.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=7f10980722d9f62f824307ccedd7eee9)
If you open the URL in that log, you’ll see the corresponding logs in Prefect Cloud.
![image.png](https://mintcdn.com/prefect-bd373955/ZU4EjeonScNdwFxn/v3/img/tutorials/modal/12.png?fit=max&auto=format&n=ZU4EjeonScNdwFxn&q=85&s=361cfb3d4a4a66310c6e187fae01dc23)
As you make changes to either the code or deployment file, Prefect will redeploy and Modal will automatically pick up changes.
You’ve successfully built your first Prefect deployment that runs on Modal every hour!

For more information about CI/CD in Prefect, see [Build deployments via CI/CD](/v3/advanced/deploy-ci-cd).

Was this page helpful?

YesNo

[Run flows on Kubernetes](/v3/how-to-guides/deployment_infra/kubernetes)[Run flows on Coiled](/v3/how-to-guides/deployment_infra/coiled)

⌘I