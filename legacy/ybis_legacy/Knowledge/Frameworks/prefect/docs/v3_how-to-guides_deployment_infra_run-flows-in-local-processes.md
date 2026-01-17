How to run flows in local processes - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Workflow Infrastructure

How to run flows in local processes

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

* [Serve a flow](#serve-a-flow)
* [Additional serve options](#additional-serve-options)
* [Serve multiple flows at once](#serve-multiple-flows-at-once)
* [Serve instance methods](#serve-instance-methods)
* [Retrieve a flow from remote storage](#retrieve-a-flow-from-remote-storage)
* [from\_source](#from-source)
* [source](#source)
* [entrypoint](#entrypoint)
* [Remote storage polling](#remote-storage-polling)
* [Further reading](#further-reading)

The simplest way to create a [deployment](/v3/deploy) for your flow is by calling its `serve` method.

## [​](#serve-a-flow) Serve a flow

The serve method creates a deployment for the flow and starts a long-running process
that monitors for work from the Prefect server.
When work is found, it is executed within its own isolated subprocess.

hello\_world.py

Copy

```
from prefect import flow


@flow(log_prints=True)
def hello_world(name: str = "world", goodbye: bool = False):
    print(f"Hello {name} from Prefect! 🤗")

    if goodbye:
        print(f"Goodbye {name}!")


if __name__ == "__main__":
    # creates a deployment and starts a long-running
    # process that listens for scheduled work
    hello_world.serve(name="my-first-deployment",
        tags=["onboarding"],
        parameters={"goodbye": True},
        interval=60
    )
```

This interface provides the configuration for a deployment (with no
strong infrastructure requirements), such as:

* schedules
* event triggers
* metadata such as tags and description
* default parameter values

**Schedules are auto-paused on shutdown**By default, stopping the process running `flow.serve` will pause the schedule
for the deployment (if it has one).When running this in environments where restarts are expected use the`pause_on_shutdown=False` flag to prevent this behavior:

Copy

```
if __name__ == "__main__":
    hello_world.serve(
        name="my-first-deployment",
        tags=["onboarding"],
        parameters={"goodbye": True},
        pause_on_shutdown=False,
        interval=60
    )
```

## [​](#additional-serve-options) Additional serve options

The `serve` method on flows exposes many options for the deployment.
Here’s how to use some of those options:

* `cron`: a keyword that allows you to set a cron string schedule for the deployment; see
  [schedules](/v3/automate/add-schedules) for more advanced scheduling options
* `tags`: a keyword that allows you to tag this deployment and its runs for bookkeeping and filtering purposes
* `description`: a keyword that allows you to document what this deployment does; by default the
  description is set from the docstring of the flow function (if documented)
* `version`: a keyword that allows you to track changes to your deployment; uses a hash of the
  file containing the flow by default; popular options include semver tags or git commit hashes
* `triggers`: a keyword that allows you to define a set of conditions for when the deployment should run; see
  [triggers](/v3/concepts/event-triggers) for more on Prefect Events concepts

Next, add these options to your deployment:

Copy

```
if __name__ == "__main__":
    get_repo_info.serve(
        name="my-first-deployment",
        cron="* * * * *",
        tags=["testing", "tutorial"],
        description="Given a GitHub repository, logs repository statistics for that repo.",
        version="tutorial/deployments",
    )
```

**Triggers with `.serve`**See this [example](/v3/how-to-guides/automations/chaining-deployments-with-events) that triggers downstream work on upstream events.

**`serve()` is a long-running process**To execute remotely triggered or scheduled runs, your script with `flow.serve` must be actively running.
Stop the script with `CTRL+C` and your schedule will automatically pause.

## [​](#serve-multiple-flows-at-once) Serve multiple flows at once

Serve multiple flows with the same process using the `serve` utility along with the `to_deployment` method of flows:

serve\_two\_flows.py

Copy

```
import time
from prefect import flow, serve


@flow
def slow_flow(sleep: int = 60):
    "Sleepy flow - sleeps the provided amount of time (in seconds)."
    time.sleep(sleep)


@flow
def fast_flow():
    "Fastest flow this side of the Mississippi."
    return


if __name__ == "__main__":
    slow_deploy = slow_flow.to_deployment(name="sleeper", interval=45)
    fast_deploy = fast_flow.to_deployment(name="fast")
    serve(slow_deploy, fast_deploy)
```

The behavior and interfaces are identical to the single flow case.
A few things to note:

* the `flow.to_deployment` interface exposes the *exact same* options as `flow.serve`; this method
  produces a deployment object
* the deployments are only registered with the API once `serve(...)` is called
* when serving multiple deployments, the only requirement is that they share a Python environment;
  they can be executed and scheduled independently of each other

A few optional steps for exploration include:

* pause and unpause the schedule for the `"sleeper"` deployment
* use the UI to submit ad-hoc runs for the `"sleeper"` deployment with different values for `sleep`
* cancel an active run for the `"sleeper"` deployment from the UI

**Hybrid execution option**Prefect’s deployment interface allows you to choose a hybrid execution model.
Whether you use Prefect Cloud or self-host Prefect server, you can run workflows in the
environments best suited to their execution.
This model enables efficient use of your infrastructure resources while maintaining the privacy
of your code and data.
There is no ingress required.
Read more about our [hybrid model](https://www.prefect.io/security/overview/#hybrid-model).

## [​](#serve-instance-methods) Serve instance methods

You can serve flow methods that are part of a class instance. This is useful when you want to configure a flow once at initialization time and reuse that configuration across all runs.

data\_processor.py

Copy

```
from prefect import flow


class DataProcessor:
    """Processor configured at initialization time."""

    def __init__(self, environment: str):
        # Configuration is set once when the instance is created
        if environment == "prod":
            self.api_url = "https://api.example.com"
            self.batch_size = 1000
        else:
            self.api_url = "https://staging.example.com"
            self.batch_size = 100

    @flow(log_prints=True)
    def process_batch(self, batch_id: str):
        """Process a batch using the configured settings."""
        print(f"Processing batch {batch_id}")
        print(f"API URL: {self.api_url}")
        print(f"Batch size: {self.batch_size}")
        # processing logic here using self.api_url and self.batch_size


if __name__ == "__main__":
    # Create processor configured for staging environment
    processor = DataProcessor(environment="staging")
    # All flow runs will use the staging configuration
    processor.process_batch.serve(name="batch-processor")
```

The instance configuration (set during `__init__`) is available to all flow runs. This is useful for environment-specific settings, connection parameters, or any configuration that should be consistent across all runs of the deployment.

## [​](#retrieve-a-flow-from-remote-storage) Retrieve a flow from remote storage

Just like the `.deploy` method, the `flow.from_source` method is used to define how to retrieve the flow that you want to serve.

### [​](#from-source) `from_source`

The `flow.from_source` method on `Flow` objects requires a `source` and an `entrypoint`.

#### [​](#source) `source`

The `source` of your deployment can be:

* a path to a local directory such as `path/to/a/local/directory`
* a repository URL such as `https://github.com/org/repo.git`
* a `GitRepository` object that accepts
  + a repository URL
  + a reference to a branch, tag, or commit hash
  + `GitCredentials` for private repositories

#### [​](#entrypoint) `entrypoint`

A flow `entrypoint` is the path to the file where the flow is located within that `source`, in the form

Copy

```
{path}:{flow_name}
```

For example, the following code will load the `hello` flow from the `flows/hello_world.py` file in the `PrefectHQ/examples` repository:

load\_from\_url.py

Copy

```
from prefect import flow


my_flow = flow.from_source(
    source="https://github.com/PrefectHQ/examples.git",
    entrypoint="flows/hello_world.py:hello"
)


if __name__ == "__main__":
    my_flow()
```

Copy

```
16:40:33.818 | INFO    | prefect.engine - Created flow run 'muscular-perch' for flow 'hello'
16:40:34.048 | INFO    | Flow run 'muscular-perch' - Hello world!
16:40:34.706 | INFO    | Flow run 'muscular-perch' - Finished in state Completed()
```

For more ways to store and access flow code, see the [Retrieve code from storage page](/v3/deploy/infrastructure-concepts/store-flow-code).

**You can serve loaded flows**You can serve a flow loaded from remote storage with the same [`serve`](#serve-a-flow) method as a local flow:

serve\_loaded\_flow.py

Copy

```
from prefect import flow


if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/org/repo.git",
        entrypoint="flows.py:my_flow"
    ).serve(name="my-deployment")
```

### [​](#remote-storage-polling) Remote storage polling

When you serve a flow loaded from remote storage, the serving process periodically polls your remote storage for updates to the flow’s code.
This pattern allows you to update your flow code without restarting the serving process.
Note that if you change metadata associated with your flow’s deployment such as parameters, you *will* need to restart the serve process.

## [​](#further-reading) Further reading

* [Serve flows in a long-lived Docker container](/v3/deploy/static-infrastructure-examples/docker)
* [Work pools and deployments with dynamic infrastructure](/v3/deploy/infrastructure-concepts/work-pools)

Was this page helpful?

YesNo

[Manage Work Pools](/v3/how-to-guides/deployment_infra/manage-work-pools)[Run flows on Prefect Managed infrastructure](/v3/how-to-guides/deployment_infra/managed)

⌘I