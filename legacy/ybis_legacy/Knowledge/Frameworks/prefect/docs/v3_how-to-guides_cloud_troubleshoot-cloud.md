How to troubleshoot Prefect Cloud - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Prefect Cloud

How to troubleshoot Prefect Cloud

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

* [Prefect Cloud and proxies](#prefect-cloud-and-proxies)
* [Prefect Cloud access through the API](#prefect-cloud-access-through-the-api)
* [Prefect Cloud login errors](#prefect-cloud-login-errors)
* [General troubleshooting](#general-troubleshooting)
* [Upgrade](#upgrade)
* [Logs](#logs)
* [Cloud](#cloud)
* [Execution](#execution)
* [API tests return an unexpected 307 Redirected](#api-tests-return-an-unexpected-307-redirected)
* [pytest.PytestUnraisableExceptionWarning or ResourceWarning](#pytest-pytestunraisableexceptionwarning-or-resourcewarning)

## [​](#prefect-cloud-and-proxies) Prefect Cloud and proxies

Proxies handle network requests between a server and a client.
To communicate with Prefect Cloud, the Prefect client library makes HTTPS requests.
These requests are made with the [`httpx`](https://www.python-httpx.org/) Python library.
`httpx` respects accepted proxy environment variables, so the Prefect client can communicate through proxies.
To enable communication through proxies, set the `HTTPS_PROXY` and `SSL_CERT_FILE` environment
variables in your execution environment.
See the [Using Prefect Cloud with proxies](https://github.com/PrefectHQ/prefect/discussions/16175)
GitHub Discussion for more information.
You should whitelist the URLs for the UI, API, Authentication,
and the current OCSP server for outbound-communication in a secure environment:

* app.prefect.cloud
* api.prefect.cloud
* auth.workos.com
* api.github.com
* github.com
* ocsp.pki.goog/s/gts1d4/OxYEb8XcYmo

## [​](#prefect-cloud-access-through-the-api) Prefect Cloud access through the API

If the Prefect Cloud API key, environment variable settings, or account login for your execution environment
are not configured correctly, you may experience errors or unexpected flow run results when using Prefect CLI commands,
running flows, or observing flow run results in Prefect Cloud.
Use the `prefect config view` CLI command to make sure your execution environment is correctly configured
to access Prefect Cloud:

Copy

```
$ prefect config view
PREFECT_PROFILE='cloud'
PREFECT_API_KEY='pnu_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' (from profile)
PREFECT_API_URL='https://api.prefect.cloud/api/accounts/...' (from profile)
```

Make sure `PREFECT_API_URL` is configured to use `https://api.prefect.cloud/api/...`.
Make sure `PREFECT_API_KEY` is configured to use a valid API key.
You can use the `prefect cloud workspace ls` CLI command to view or set the active workspace.

Copy

```
prefect cloud workspace ls
```

Copy

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   Available Workspaces: ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   g-gadflow/g-workspace │
│    * prefect/workinonit │
━━━━━━━━━━━━━━━━━━━━━━━━━━━
    * active workspace
```

You can also check that the account and workspace IDs specified in the URL for `PREFECT_API_URL`
match those shown in the URL for your Prefect Cloud workspace.

## [​](#prefect-cloud-login-errors) Prefect Cloud login errors

If you’re having difficulty logging in to Prefect Cloud, the following troubleshooting steps may resolve the issue,
or will provide more information when sharing your case to the support channel.

* Are you logging into Prefect Cloud 3? Prefect Cloud 1, Prefect Cloud 2, and Prefect Cloud 3 use separate accounts.
  Make sure to use the right Prefect Cloud 3 URL: <[https://app.prefect.cloud/>](https://app.prefect.cloud/%3E)
* Do you already have a Prefect Cloud account? If you’re having difficulty accepting an invitation,
  try creating an account first using the email associated with the invitation, then accept the invitation.
* Are you using a single sign-on (SSO) provider, social authentication (Google, Microsoft, or GitHub) or just using an emailed link?

Other tips to help with login difficulties:

* Hard refresh your browser with Cmd+Shift+R.
* Try in a different browser. We actively test against the following browsers:
  + Chrome
  + Edge
  + Firefox
  + Safari
* Clear recent browser history/cookies

None of this worked?
Email us at <[help@prefect.io](mailto:help@prefect.io)> and provide answers to the questions above in your email to make it faster to troubleshoot
and unblock you. Make sure you add the email address you used to attempt to log in, your Prefect Cloud account name, and, if applicable,
the organization it belongs to.

# [​](#general-troubleshooting) General troubleshooting

The first troubleshooting step is to confirm that you are running the latest version of Prefect.
If you are not, upgrade (see below) to the latest version, since the issue may have already been fixed.
Beyond that, there are several categories of errors:

* The issue may be in your flow code, in which case you should carefully read the [logs](#logs).
* The issue could be with how you are authenticated, and whether or not you are connected to [Cloud](#cloud).
* The issue might have to do with how your code is [executed](#execution).

## [​](#upgrade) Upgrade

Prefect is constantly evolving by adding new features and fixing bugs. A patch may have already been
identified and released. Search existing [issues](https://github.com/PrefectHQ/prefect/issues) for similar reports
and check out the [Release Notes](https://github.com/PrefectHQ/prefect/releases).
Upgrade to the newest version with the following command:

Copy

```
pip install --upgrade prefect
```

Different components may use different versions of Prefect:

* **Cloud** is generally the newest version. Cloud is continuously deployed by the Prefect team.
  When using a self-hosted server, you can control this version.
* **Workers** change versions infrequently, and are usually the latest version at the time of creation.
  Workers provision infrastructure for flow runs, so upgrading them may help with infrastructure problems.
* **Flows** could use a different version than the worker that created them, especially when running in different environments.
  Suppose your worker and flow both use the latest official Docker image, but your worker was created a month ago.
  Your worker is often an older version than your flow.

**Integration Versions**[Integrations](/integrations) are versioned and released independently of the core Prefect library.
They should be upgraded simultaneously with the core library, using the same method.

## [​](#logs) Logs

In many cases, there is an informative stack trace in Prefect’s [logs](/v3/develop/logging).
**Read it carefully**, locate the source of the error, and try to identify the cause.
There are two types of logs:

* **Flow and task logs** are always scoped to a flow. They are sent to Prefect and are viewable in the UI.
* **Worker logs** are not scoped to a flow and may have more information on what happened before the flow started.
  These logs are generally only available where the worker is running.

If your flow and task logs are empty, there may have been an infrastructure issue that prevented your flow from starting.
Check your worker logs for more details.
If there is no clear indication of what went wrong, try updating the logging level from the default `INFO` level
to the `DEBUG` level. [Settings](https://reference.prefect.io/prefect/settings/) such as the logging level are propagated
from the worker environment to the flow run environment. Set them with environment variables or the `prefect config set` CLI:

Copy

```
# Using the CLI
prefect config set PREFECT_LOGGING_LEVEL=DEBUG

# Using environment variables
export PREFECT_LOGGING_LEVEL=DEBUG
```

The `DEBUG` logging level produces a high volume of logs, so consider setting it back to `INFO` once any issues are resolved.

## [​](#cloud) Cloud

When using Prefect Cloud, there are the additional concerns of authentication and authorization.
The Prefect API authenticates users and service accounts, collectively known as actors, with API keys.
Missing, incorrect, or expired API keys result in a 401 response with detail `Invalid authentication credentials`.
Use the following command to check your authentication, replacing `$PREFECT_API_KEY` with your API key:

Copy

```
curl -s -H "Authorization: Bearer $PREFECT_API_KEY" "https://api.prefect.cloud/api/me/"
```

**Users vs Service Accounts**[Service accounts](/v3/how-to-guides/cloud/manage-users/service-accounts) (sometimes referred to as bots),
represent non-human actors that interact with Prefect such as workers and CI/CD systems.
Each human that interacts with Prefect should be represented as a user.
User API keys start with `pnu_` and service account API keys start with `pnb_`.

Actors can be members of [workspaces](/v3/manage/cloud/workspaces). An actor attempting an action in a
workspace they are not a member of results in a 404 response. Use the following command to check your actor’s workspace memberships:

Copy

```
curl -s -H "Authorization: Bearer $PREFECT_API_KEY" "https://api.prefect.cloud/api/me/workspaces"
```

**Formatting JSON**Python comes with a helpful [tool](https://docs.python.org/3/library/json.html#module-json.tool) for formatting JSON.
Append the following to the end of the command above to make the output more readable: `| python -m json.tool`

Make sure your actor is a member of the workspace you are working in. Within a workspace,
an actor has a [role](/v3/how-to-guides/cloud/manage-users/manage-roles) which grants them certain permissions.
Insufficient permissions result in an error. For example, starting a worker with the **Viewer** role results in errors.

## [​](#execution) Execution

The user can execute flows locally, or remotely by a worker. Local execution generally means that you, the user,
run your flow directly with a command like `python flow.py`. Remote execution generally means that a worker runs your flow
through a [deployment](/v3/how-to-guides/deployment_infra/docker) (optionally on different infrastructure).
With remote execution, the creation of your flow run happens separately from its execution.
Flow runs are assigned to a work pool and a work queue. For flow runs to execute, a worker must be subscribed
to the work pool and work queue, or the flow runs will go from `Scheduled` to `Late`.
Ensure that your work pool and work queue have a subscribed worker.
Local and remote execution can also differ in their treatment of relative imports.
If switching from local to remote execution results in local import errors, try replicating the
behavior by executing the flow locally with the `-m` flag (For example, `python -m flow` instead of `python flow.py`).
Read more about `-m` in this [Stack Overflow post](https://stackoverflow.com/a/62923810).

## [​](#api-tests-return-an-unexpected-307-redirected) API tests return an unexpected 307 Redirected

**Summary:** requests require a trailing `/` in the request URL.
If you write a test that does not include a trailing `/` when making a request to a specific endpoint:

Copy

```
async def test_example(client):
    response = await client.post("/my_route")
    assert response.status_code == 201
```

You’ll see a failure like:

Copy

```
E       assert 307 == 201
E        +  where 307 = <Response [307 Temporary Redirect]>.status_code
```

To resolve this, include the trailing `/`:

Copy

```
async def test_example(client):
    response = await client.post("/my_route/")
    assert response.status_code == 201
```

Note: requests to nested URLs may exhibit the *opposite* behavior and require no trailing slash:

Copy

```
async def test_nested_example(client):
    response = await client.post("/my_route/filter/")
    assert response.status_code == 307

    response = await client.post("/my_route/filter")
    assert response.status_code == 200
```

**Reference:** “HTTPX disabled redirect following by default” in
[`0.22.0`](https://github.com/encode/httpx/blob/master/CHANGELOG.md#0200-13th-october-2021).

## [​](#pytest-pytestunraisableexceptionwarning-or-resourcewarning) `pytest.PytestUnraisableExceptionWarning` or `ResourceWarning`

As you’re working with one of the `FlowRunner` implementations, you may get an
error like this:

Copy

```
E               pytest.PytestUnraisableExceptionWarning: Exception ignored in: <ssl.SSLSocket fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
E
E               Traceback (most recent call last):
E                 File ".../pytest_asyncio/plugin.py", line 306, in setup
E                   res = await func(**_add_kwargs(func, kwargs, event_loop, request))
E               ResourceWarning: unclosed <ssl.SSLSocket fd=10, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 60605), raddr=('127.0.0.1', 6443)>

.../_pytest/unraisableexception.py:78: PytestUnraisableExceptionWarning
```

This error states that your test suite (or the `prefect` library code) opened a
connection to something (like a Docker daemon or a Kubernetes cluster) and didn’t close
it.
It may help to re-run the specific test with `PYTHONTRACEMALLOC=25 pytest ...` so that
Python can display more of the stack trace where the connection was opened.

Was this page helpful?

YesNo

[Create a Webhook](/v3/how-to-guides/cloud/create-a-webhook)[Run a local Prefect server](/v3/how-to-guides/self-hosted/server-cli)

⌘I