How to version deployments - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

How to version deployments

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

* [What’s included in a deployment version](#what%E2%80%99s-included-in-a-deployment-version)
* [How to create and manage versions](#how-to-create-and-manage-versions)
* [Supported source code management platforms](#supported-source-code-management-platforms)
* [Using the version deployment property](#using-the-version-deployment-property)
* [Executing specific code versions](#executing-specific-code-versions)
* [Pulling from Git](#pulling-from-git)
* [Pulling Docker images](#pulling-docker-images)

In Prefect Cloud, deployments have a version history.
The **live** deployment version is the runnable version of a deployment.
A previous deployment version can be made live by **rolling back** to it.
When a previous deployment version is live, a newer deployment version can be made live by **promoting** it.

When a new version of a deployment is created, it is automatically set as the live version.

## [​](#what’s-included-in-a-deployment-version) What’s included in a deployment version

Deployment versions are a history of changes to a deployment’s configuration.
While the majority of deployment properties are included in a deployment’s version, some properties cannot be versioned.
Persisting these properties across all versions helps prevent unexpected execution behavior when rolling back or promoting versions.

Versioned deployment properties

These properties are pinned to each deployment version.

| Deployment Property | Versioned |
| --- | --- |
| `description` |  |
| `tags` |  |
| `labels` |  |
| `entrypoint` |  |
| `pull_steps` |  |
| `parameters` |  |
| `parameter_openapi_schema` |  |
| `enforce_parameter_schema` |  |
| `work_queue_id` |  |
| `work_pool_name` |  |
| `job_variables` |  |
| `created_by` |  |
| `updated_by` |  |
| `version_info` |  |

Unversioned deployment properties

These properties persist across version rollbacks and promotions.

| Deployment Property | Versioned |
| --- | --- |
| `name` | (immutable) |
| `schedules` |  |
| `is_schedule_active` |  |
| `paused` |  |
| `disabled` |  |
| `concurrency_limit` |  |
| `concurrency_options` |  |

## [​](#how-to-create-and-manage-versions) How to create and manage versions

A new deployment version is created every time a deployment is updated, whether from the CLI, from Python, or from the UI.
If you’re deploying from a supported source code management platform or from inside a Git repository, Prefect automatically collects the **repository name**, **repository URL**, the currently checked out **branch**, the **commit SHA**, and the **first line of your commit message** from your environment.
This information is used to help create a record of which code versions produced which deployment versions, and does not affect deployment execution.

### [​](#supported-source-code-management-platforms) Supported source code management platforms

Prefect searches for environment variables in each supported platform’s CI environment in order to collect information about the current state of the repository from which deployment versions are created.
It may be useful to access these environment variables in other stages of your deployment process for constructing version identifiers.

Prefect’s automatic version information collection currently supports GitHub Actions, GitLab CI, Bitbucket Pipelines, and Azure Pipelines.
If deploying from a Git repository not on one of these platforms, Prefect will use `git` CLI commands as a best effort to discover these values.

* GitHub Actions
* GitLab CI
* Bitbucket Pipelines
* Azure Pipelines

| Environment Variable | Value |
| --- | --- |
| `GITHUB_SHA` | Commit SHA |
| `GITHUB_REF_NAME` | Branch name |
| `GITHUB_REPOSITORY` | Repository name |
| `GITHUB_SERVER_URL` | Github account or organization URL |

| Environment Variable | Value |
| --- | --- |
| `CI_COMMIT_SHA` | Commit SHA |
| `CI_COMMIT_REF_NAME` | Branch name |
| `CI_PROJECT_NAME` | Repository name |
| `CI_PROJECT_URL` | Repository URL |

| Environment Variable | Value |
| --- | --- |
| `BITBUCKET_COMMIT` | Commit SHA |
| `BITBUCKET_BRANCH` | Branch name |
| `BITBUCKET_REPO_SLUG` | Repository name |
| `BITBUCKET_GIT_HTTP_ORIGIN` | Bitbucket account or organization URL |

| Environment Variable | Value |
| --- | --- |
| `BUILD_SOURCEVERSION` | Commit SHA |
| `BUILD_SOURCEBRANCHNAME` | Branch name |
| `BUILD_REPOSITORY_NAME` | Repository name |
| `BUILD_REPOSITORY_URI` | Repository URL |

### [​](#using-the-version-deployment-property) Using the `version` deployment property

Supplying a `version` to your deployment is not required, but using human-readable version names helps give meaning to each change you make.
It’s also valuable for quickly finding or communicating the version you want to roll back to or promote.
For additional details on how Prefect handles the value of `version`, see [deployment metadata for bookkeeping](/v3/deploy#metadata-for-bookkeeping).

### [​](#executing-specific-code-versions) Executing specific code versions

It’s possible to synchronize code changes to deployment versions so each deployment version executes the exact commit that was checked out when it was created.
Since `pull_steps` and `job_variables` define what repository or image to pull when a flow runs, updating their contents with each code change keeps deployment versions in step with your codebase.
Which of these configurations to use depends on whether you are pulling code from Git or storing code in Docker images.
The examples in this section use GitHub as their source control management and CI platform, so be sure to replace URLs, environment variables, and CI workflows with the ones relevant to your platform.
You can check out complete example repositories on GitHub for executing specific code versions when [pulling from Git](https://github.com/kevingrismore/version-testing) and [pulling Docker images](https://github.com/kevingrismore/version-testing-docker/tree/main).

#### [​](#pulling-from-git) Pulling from Git

The `git_clone` deployment pull step and `GitRepository` deployment storage class offer a `commit_sha` field.
When deploying from a Git repository, provide the commit SHA from your environment to your deployment.
Both approaches below will result in a deployment pull step that clones your repository and checks out a specific commit.

With prefect.yaml

With .deploy()

Copy

```
pull:
- prefect.deployments.steps.git_clone:
    repository: https://github.com/my-org/my-repo.git
    commit_sha: "{{ $GITHUB_SHA }}"

deployments:
- name: my-deployment
  version: 0.0.1
  entrypoint: example.py:my_flow
  work_pool:
    name: my-work-pool
```

#### [​](#pulling-docker-images) Pulling Docker images

When baking code into Docker images, use the image digest to pin exact code versions to deployment versions.
An image digest uniquely and immutably identifies a container image.
First, build your image in your CI job and pass the image digest as an environment variable to the Prefect deploy step.

Github Actions

Copy

```
      ...

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        id: build-docker-image
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: my-registry/my-example-image:my-tag
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Deploy a Prefect flow
        env:
          IMAGE_DIGEST: ${{ steps.build-docker-image.outputs.digest }}
          PREFECT_API_KEY: ${{ secrets.PREFECT_API_KEY }}
          PREFECT_API_URL: ${{ secrets.PREFECT_API_URL }}
        ... # your deployment action here
```

Then, refer to that digest in the image name you provide to this deployment version’s job variables.

With prefect.yaml

With .deploy()

Copy

```
deployments:
- name: my-deployment
  version: 0.0.1
  entrypoint: example.py:my_flow
  work_pool:
    name: my-work-pool
    job_variables:
      image: "my-registry/my-image@{{ $IMAGE_DIGEST }}"
```

Was this page helpful?

YesNo

[Retrieve code from storage](/v3/how-to-guides/deployments/store-flow-code)[Override Job Configuration](/v3/how-to-guides/deployments/customize-job-variables)

⌘I