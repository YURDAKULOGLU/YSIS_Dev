Settings and profiles - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Configuration

Settings and profiles

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

* [Why use settings?](#why-use-settings)
* [Get started with settings](#get-started-with-settings)
* [Settings sources](#settings-sources)
* [Environment variables](#environment-variables)
* [.env file](#env-file)
* [prefect.toml file](#prefect-toml-file)
* [pyproject.toml file](#pyproject-toml-file)
* [Profiles](#profiles)
* [Configure settings for the active profile](#configure-settings-for-the-active-profile)
* [Common client settings](#common-client-settings)
* [Common server settings](#common-server-settings)

## [​](#why-use-settings) Why use settings?

Settings in Prefect help you control how your workflows behave. They let you easily customize Prefect to work the way you need it to, whether you’re testing locally or running in production.
Specifically, settings enable:

* **Environment-Specific Configuration**: Use different settings for development (like detailed logging), testing (like test databases), and production (like your production server) without changing your workflow code.
* **Runtime Flexibility**: Quickly adjust things like retry attempts or logging levels without having to modify and redeploy your workflows.

## [​](#get-started-with-settings) Get started with settings

The simplest way declare settings is by creating a `prefect.toml` file in your project directory. For example:

prefect.toml

Copy

```
# Set more detailed logging while developing
[logging]
level = "DEBUG"
```

To use `prefect.toml` or `pyproject.toml` for configuration, `prefect>=3.1` must be installed.To use a `.env` file for configuration, `prefect>=3.0.5` must be installed.

Most editors have plugins for TOML that provide syntax highlighting, linting, and autocomplete for `prefect.toml` files. If you use VSCode, we recommend the [Even Better TOML extension](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml).

**Writing TOML**TOML is a simple configuration language. If you’re new to TOML, learn more about the syntax in the [official documentation](https://toml.io/en/).In particular, note that TOML uses square brackets to denote [tables](https://toml.io/en/v1.0.0#table), which are analogous to dictionaries in Python.

## [​](#settings-sources) Settings sources

You can configure settings via the following sources (highest to lowest precedence):

* **Environment variables**: Environment variables are useful for temporarily overriding settings or configuring the runtime environment of a single workflow run.
* **`.env` file**: `.env` files are useful for declaring local settings that you want to apply across multiple runs.
* **`prefect.toml` file**: A `prefect.toml` file is useful when you want to declare settings for an entire project. You can keep this file in your project directory and it will be automatically applied regardless of where you run your project.
* **`pyproject.toml` file**: If you already have a `pyproject.toml` file in your project or like to consolidate settings for all your tools in one place, you can declare settings in the `[tool.prefect]` table of your `pyproject.toml` file.
* **Profiles**: Prefect profiles are useful for switching between different environments. For example, you might use one profile for a local Prefect server and another for your production environment.

When multiple settings sources define the same setting, Prefect follows this precedence order (highest to lowest):

1

Environment variables

2

.env file in the current working directory

3

prefect.toml file in the current working directory

4

pyproject.toml file in the current working directory

5

Active profile settings

6

Default values

For example, if you set `PREFECT_API_URL` in both your environment and your active profile, the environment variable value will take precedence.

### [​](#environment-variables) Environment variables

Environment variables are useful for temporarily overriding settings or configuring the runtime environment of a workflow.
All Prefect settings can be set using environment variables prefixed with `PREFECT_`. They take precedence over all other sources, making them ideal for adjustments that should only apply to a single session or process.
For example, you can run the following command to temporarily set the logging level for a single flow run:

Copy

```
PREFECT_LOGGING_LEVEL="DEBUG" python my_flow.py
```

You can also export an environment variable in your shell to apply it to all flow runs in that shell session:

Copy

```
export PREFECT_LOGGING_LEVEL="DEBUG"
prefect run my_flow.py
```

You can see supported environment variables for each setting in the [settings reference documentation](/v3/develop/settings-ref).

**Environment variables *always* take precedence**Environment variables always take precedence over values declared in other sources.
This allows you to configure certain runtime behavior for your workflows by setting the appropriate
environment variable on the job or process executing the workflow.

### [​](#env-file) `.env` file

`.env` files are useful for declaring local settings that you want to apply across multiple runs.
When running `prefect` in a directory that contains a `.env` file, Prefect will automatically apply the settings in the file. We recommend keeping your `.env` files local and not committing them to your code repositories.
For example, the following `.env` file declares a local setting for the logging level:

.env

Copy

```
PREFECT_LOGGING_LEVEL="DEBUG"
```

Any flows run in the same directory as this `.env` file will use the `DEBUG` logging level, even if they are run in different shell sessions.
View supported environment variables for each setting in the [settings reference documentation](/v3/develop/settings-ref).

### [​](#prefect-toml-file) `prefect.toml` file

A `prefect.toml` file is useful when you want to declare settings for an entire project.
You can keep a `prefect.toml` file in your project directory and the declared settings will be automatically applied when running `prefect` in that directory. We recommend committing this file to your code repositories to ensure consistency across environments.
For example, the following `prefect.toml` file declares a setting for the logging level:

prefect.toml

Copy

```
[logging]
level = "DEBUG"
```

If you commit your `prefect.toml` file to a code repository, creating deployments from flows in that repository will use the settings declared in the `prefect.toml` file.
You can see the `prefect.toml` path for each setting in the [settings reference documentation](/v3/develop/settings-ref).

### [​](#pyproject-toml-file) `pyproject.toml` file

Declaring settings in a `pyproject.toml` file is very similar to declaring settings in a `prefect.toml` file. The main difference is that settings are declared in the `[tool.prefect]` table instead of at the root of the file.
For example, the following `pyproject.toml` file declares a setting for the logging level:

pyproject.toml

Copy

```
[tool.prefect]
logging.level = "DEBUG"
```

The advantage of declaring settings in a `pyproject.toml` file is that it allows you to keep all your dependencies and settings for all your tools in one place. You can learn more about `pyproject.toml` files in the [Python Packaging User Guide](https://packaging.python.org/en/latest/specifications/pyproject-toml/#arbitrary-tool-configuration-the-tool-table).

### [​](#profiles) Profiles

Prefect profiles are useful for switching between different environments. By creating different profiles with different API URLs, you can easily switch between a local Prefect server and your production environment.
Profiles are stored in a [TOML](https://toml.io/en/) file located at `~/.prefect/profiles.toml` by default. This location can be configured by setting `PREFECT_PROFILES_PATH`.
One and only one profile can be active at any time.
Immediately after installation, the `ephemeral` profile will be used, which only has `PREFECT_SERVER_ALLOW_EPHEMERAL_MODE` configured:

**What is `PREFECT_SERVER_ALLOW_EPHEMERAL_MODE`?**This setting allows a Prefect server to be run ephemerally as needed without explicitly starting a server process.

The `prefect profile` CLI commands enable you to create, review, and manage profiles:

| Command | Description |
| --- | --- |
| `create` | Create a new profile; use the `--from` flag to copy settings from another profile. |
| `delete` | Delete the given profile. |
| `inspect` | Display settings from a given profile; defaults to active. |
| `ls` | List all profile names. |
| `rename` | Change the name of a profile. |
| `use` | Switch the active profile. |
| `populate-defaults` | Populate your `profiles.toml` file with opinionated stock profiles. |

… or you may edit your `profiles.toml` file directly:

Copy

```
vim ~/.prefect/profiles.toml
```

#### [​](#configure-settings-for-the-active-profile) Configure settings for the active profile

The `prefect config` CLI commands enable you to manage the settings within the currently active profile.

| Command | Description |
| --- | --- |
| set | Change the value for a setting. |
| unset | Restore the default value for a setting. |
| view | Display the current settings. |

For example, the following CLI commands set configuration in the `ephemeral` profile and then create a new
profile with new settings:

Copy

```
prefect profile use ephemeral
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

prefect profile create new-profile --from ephemeral
prefect profile use new-profile
prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true PREFECT_LOGGING_LEVEL="ERROR"

prefect profile inspect
prefect config unset PREFECT_LOGGING_LEVEL -y
```

## [​](#common-client-settings) Common client settings

* [`api.url`](/v3/develop/settings-ref#url): this setting specifies the API endpoint of your
  Prefect Cloud workspace or a self-hosted Prefect server instance.
* [`api.key`](/v3/develop/settings-ref#key): this setting specifies the
  [API key](/v3/how-to-guides/cloud/manage-users/api-keys) used to authenticate with Prefect Cloud.
* [`home`](/v3/develop/settings-ref#home): the `home` value specifies the local Prefect directory for configuration files,
  profiles, and the location of the default Prefect SQLite database.

**Use `prefect cloud login` to set these values for Prefect Cloud**To set `PREFECT_API_URL` and `PREFECT_API_KEY` for your active profile, run `prefect cloud login`.
Read more about [managing API keys](/v3/how-to-guides/cloud/manage-users/api-keys).

## [​](#common-server-settings) Common server settings

* [`server.database.connection_url`](/v3/develop/settings-ref#connection-url): the database connection URL for a self-hosted Prefect server instance.
  Must be provided in a SQLAlchemy-compatible format. Prefect currently supports SQLite and Postgres.

Was this page helpful?

YesNo

[Blocks](/v3/concepts/blocks)[Prefect server](/v3/concepts/server)

⌘I