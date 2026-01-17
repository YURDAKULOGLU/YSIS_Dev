CLI - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Core Concepts

CLI

[Home](/)[Documentation](/en/introduction)[AOP](/en/enterprise/introduction)[API Reference](/en/api-reference/introduction)[Examples](/en/examples/example)[Changelog](/en/changelog)

* [Website](https://crewai.com)
* [Forum](https://community.crewai.com)
* [Blog](https://blog.crewai.com)
* [CrewGPT](https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant)

##### Get Started

* [Introduction](/en/introduction)
* [Installation](/en/installation)
* [Quickstart](/en/quickstart)

##### Guides

* Strategy
* Agents
* Crews
* Flows
* Advanced

##### Core Concepts

* [Agents](/en/concepts/agents)
* [Tasks](/en/concepts/tasks)
* [Crews](/en/concepts/crews)
* [Flows](/en/concepts/flows)
* [Production Architecture](/en/concepts/production-architecture)
* [Knowledge](/en/concepts/knowledge)
* [LLMs](/en/concepts/llms)
* [Processes](/en/concepts/processes)
* [Collaboration](/en/concepts/collaboration)
* [Training](/en/concepts/training)
* [Memory](/en/concepts/memory)
* [Reasoning](/en/concepts/reasoning)
* [Planning](/en/concepts/planning)
* [Testing](/en/concepts/testing)
* [CLI](/en/concepts/cli)
* [Tools](/en/concepts/tools)
* [Event Listeners](/en/concepts/event-listener)

##### MCP Integration

* [MCP Servers as Tools in CrewAI](/en/mcp/overview)
* [MCP DSL Integration](/en/mcp/dsl-integration)
* [Stdio Transport](/en/mcp/stdio)
* [SSE Transport](/en/mcp/sse)
* [Streamable HTTP Transport](/en/mcp/streamable-http)
* [Connecting to Multiple MCP Servers](/en/mcp/multiple-servers)
* [MCP Security Considerations](/en/mcp/security)

##### Tools

* [Tools Overview](/en/tools/overview)
* File & Document
* Web Scraping & Browsing
* Search & Research
* Database & Data
* AI & Machine Learning
* Cloud & Storage
* Integrations
* Automation

##### Observability

* [CrewAI Tracing](/en/observability/tracing)
* [Overview](/en/observability/overview)
* [Arize Phoenix](/en/observability/arize-phoenix)
* [Braintrust](/en/observability/braintrust)
* [Datadog Integration](/en/observability/datadog)
* [LangDB Integration](/en/observability/langdb)
* [Langfuse Integration](/en/observability/langfuse)
* [Langtrace Integration](/en/observability/langtrace)
* [Maxim Integration](/en/observability/maxim)
* [MLflow Integration](/en/observability/mlflow)
* [Neatlogs Integration](/en/observability/neatlogs)
* [OpenLIT Integration](/en/observability/openlit)
* [Opik Integration](/en/observability/opik)
* [Patronus AI Evaluation](/en/observability/patronus-evaluation)
* [Portkey Integration](/en/observability/portkey)
* [Weave Integration](/en/observability/weave)
* [TrueFoundry Integration](/en/observability/truefoundry)

##### Learn

* [Overview](/en/learn/overview)
* [Strategic LLM Selection Guide](/en/learn/llm-selection-guide)
* [Conditional Tasks](/en/learn/conditional-tasks)
* [Coding Agents](/en/learn/coding-agents)
* [Create Custom Tools](/en/learn/create-custom-tools)
* [Custom LLM Implementation](/en/learn/custom-llm)
* [Custom Manager Agent](/en/learn/custom-manager-agent)
* [Customize Agents](/en/learn/customizing-agents)
* [Image Generation with DALL-E](/en/learn/dalle-image-generation)
* [Force Tool Output as Result](/en/learn/force-tool-output-as-result)
* [Hierarchical Process](/en/learn/hierarchical-process)
* [Human Input on Execution](/en/learn/human-input-on-execution)
* [Human-in-the-Loop (HITL) Workflows](/en/learn/human-in-the-loop)
* [Human Feedback in Flows](/en/learn/human-feedback-in-flows)
* [Kickoff Crew Asynchronously](/en/learn/kickoff-async)
* [Kickoff Crew for Each](/en/learn/kickoff-for-each)
* [Connect to any LLM](/en/learn/llm-connections)
* [Using Multimodal Agents](/en/learn/multimodal-agents)
* [Replay Tasks from Latest Crew Kickoff](/en/learn/replay-tasks-from-latest-crew-kickoff)
* [Sequential Processes](/en/learn/sequential-process)
* [Using Annotations in crew.py](/en/learn/using-annotations)
* [Execution Hooks Overview](/en/learn/execution-hooks)
* [LLM Call Hooks](/en/learn/llm-hooks)
* [Tool Call Hooks](/en/learn/tool-hooks)

##### Telemetry

* [Telemetry](/en/telemetry)

Since release 0.140.0, CrewAI AOP started a process of migrating their login provider. As such, the authentication flow via CLI was updated. Users that use Google to login, or that created their account after July 3rd, 2025 will be unable to log in with older versions of the `crewai` library.

## [​](#overview) Overview

The CrewAI CLI provides a set of commands to interact with CrewAI, allowing you to create, train, run, and manage crews & flows.

## [​](#installation) Installation

To use the CrewAI CLI, make sure you have CrewAI installed:

Terminal

Copy

Ask AI

```
pip install crewai
```

## [​](#basic-usage) Basic Usage

The basic structure of a CrewAI CLI command is:

Terminal

Copy

Ask AI

```
crewai [COMMAND] [OPTIONS] [ARGUMENTS]
```

## [​](#available-commands) Available Commands

### [​](#1-create) 1. Create

Create a new crew or flow.

Terminal

Copy

Ask AI

```
crewai create [OPTIONS] TYPE NAME
```

* `TYPE`: Choose between “crew” or “flow”
* `NAME`: Name of the crew or flow

Example:

Terminal

Copy

Ask AI

```
crewai create crew my_new_crew
crewai create flow my_new_flow
```

### [​](#2-version) 2. Version

Show the installed version of CrewAI.

Terminal

Copy

Ask AI

```
crewai version [OPTIONS]
```

* `--tools`: (Optional) Show the installed version of CrewAI tools

Example:

Terminal

Copy

Ask AI

```
crewai version
crewai version --tools
```

### [​](#3-train) 3. Train

Train the crew for a specified number of iterations.

Terminal

Copy

Ask AI

```
crewai train [OPTIONS]
```

* `-n, --n_iterations INTEGER`: Number of iterations to train the crew (default: 5)
* `-f, --filename TEXT`: Path to a custom file for training (default: “trained\_agents\_data.pkl”)

Example:

Terminal

Copy

Ask AI

```
crewai train -n 10 -f my_training_data.pkl
```

### [​](#4-replay) 4. Replay

Replay the crew execution from a specific task.

Terminal

Copy

Ask AI

```
crewai replay [OPTIONS]
```

* `-t, --task_id TEXT`: Replay the crew from this task ID, including all subsequent tasks

Example:

Terminal

Copy

Ask AI

```
crewai replay -t task_123456
```

### [​](#5-log-tasks-outputs) 5. Log-tasks-outputs

Retrieve your latest crew.kickoff() task outputs.

Terminal

Copy

Ask AI

```
crewai log-tasks-outputs
```

### [​](#6-reset-memories) 6. Reset-memories

Reset the crew memories (long, short, entity, latest\_crew\_kickoff\_outputs).

Terminal

Copy

Ask AI

```
crewai reset-memories [OPTIONS]
```

* `-l, --long`: Reset LONG TERM memory
* `-s, --short`: Reset SHORT TERM memory
* `-e, --entities`: Reset ENTITIES memory
* `-k, --kickoff-outputs`: Reset LATEST KICKOFF TASK OUTPUTS
* `-kn, --knowledge`: Reset KNOWLEDGE storage
* `-akn, --agent-knowledge`: Reset AGENT KNOWLEDGE storage
* `-a, --all`: Reset ALL memories

Example:

Terminal

Copy

Ask AI

```
crewai reset-memories --long --short
crewai reset-memories --all
```

### [​](#7-test) 7. Test

Test the crew and evaluate the results.

Terminal

Copy

Ask AI

```
crewai test [OPTIONS]
```

* `-n, --n_iterations INTEGER`: Number of iterations to test the crew (default: 3)
* `-m, --model TEXT`: LLM Model to run the tests on the Crew (default: “gpt-4o-mini”)

Example:

Terminal

Copy

Ask AI

```
crewai test -n 5 -m gpt-3.5-turbo
```

### [​](#8-run) 8. Run

Run the crew or flow.

Terminal

Copy

Ask AI

```
crewai run
```

Starting from version 0.103.0, the `crewai run` command can be used to run both standard crews and flows. For flows, it automatically detects the type from pyproject.toml and runs the appropriate command. This is now the recommended way to run both crews and flows.

Make sure to run these commands from the directory where your CrewAI project is set up.
Some commands may require additional configuration or setup within your project structure.

### [​](#9-chat) 9. Chat

Starting in version `0.98.0`, when you run the `crewai chat` command, you start an interactive session with your crew. The AI assistant will guide you by asking for necessary inputs to execute the crew. Once all inputs are provided, the crew will execute its tasks.
After receiving the results, you can continue interacting with the assistant for further instructions or questions.

Terminal

Copy

Ask AI

```
crewai chat
```

Ensure you execute these commands from your CrewAI project’s root directory.

IMPORTANT: Set the `chat_llm` property in your `crew.py` file to enable this command.

Copy

Ask AI

```
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True,
        chat_llm="gpt-4o",  # LLM for chat orchestration
    )
```

### [​](#10-deploy) 10. Deploy

Deploy the crew or flow to [CrewAI AOP](https://app.crewai.com).

* **Authentication**: You need to be authenticated to deploy to CrewAI AOP.
  You can login or create an account with:

  Terminal

  Copy

  Ask AI

  ```
  crewai login
  ```
* **Create a deployment**: Once you are authenticated, you can create a deployment for your crew or flow from the root of your localproject.

  Terminal

  Copy

  Ask AI

  ```
  crewai deploy create
  ```

  + Reads your local project configuration.
  + Prompts you to confirm the environment variables (like `OPENAI_API_KEY`, `SERPER_API_KEY`) found locally. These will be securely stored with the deployment on the Enterprise platform. Ensure your sensitive keys are correctly configured locally (e.g., in a `.env` file) before running this.

### [​](#11-organization-management) 11. Organization Management

Manage your CrewAI AOP organizations.

Terminal

Copy

Ask AI

```
crewai org [COMMAND] [OPTIONS]
```

#### [​](#commands:) Commands:

* `list`: List all organizations you belong to

Terminal

Copy

Ask AI

```
crewai org list
```

* `current`: Display your currently active organization

Terminal

Copy

Ask AI

```
crewai org current
```

* `switch`: Switch to a specific organization

Terminal

Copy

Ask AI

```
crewai org switch <organization_id>
```

You must be authenticated to CrewAI AOP to use these organization management commands.

* **Create a deployment** (continued):
  + Links the deployment to the corresponding remote GitHub repository (it usually detects this automatically).
* **Deploy the Crew**: Once you are authenticated, you can deploy your crew or flow to CrewAI AOP.

  Terminal

  Copy

  Ask AI

  ```
  crewai deploy push
  ```

  + Initiates the deployment process on the CrewAI AOP platform.
  + Upon successful initiation, it will output the Deployment created successfully! message along with the Deployment Name and a unique Deployment ID (UUID).
* **Deployment Status**: You can check the status of your deployment with:

  Terminal

  Copy

  Ask AI

  ```
  crewai deploy status
  ```

  This fetches the latest deployment status of your most recent deployment attempt (e.g., `Building Images for Crew`, `Deploy Enqueued`, `Online`).
* **Deployment Logs**: You can check the logs of your deployment with:

  Terminal

  Copy

  Ask AI

  ```
  crewai deploy logs
  ```

  This streams the deployment logs to your terminal.
* **List deployments**: You can list all your deployments with:

  Terminal

  Copy

  Ask AI

  ```
  crewai deploy list
  ```

  This lists all your deployments.
* **Delete a deployment**: You can delete a deployment with:

  Terminal

  Copy

  Ask AI

  ```
  crewai deploy remove
  ```

  This deletes the deployment from the CrewAI AOP platform.
* **Help Command**: You can get help with the CLI with:

  Terminal

  Copy

  Ask AI

  ```
  crewai deploy --help
  ```

  This shows the help message for the CrewAI Deploy CLI.

Watch this video tutorial for a step-by-step demonstration of deploying your crew to [CrewAI AOP](http://app.crewai.com) using the CLI.

### [​](#11-login) 11. Login

Authenticate with CrewAI AOP using a secure device code flow (no email entry required).

Terminal

Copy

Ask AI

```
crewai login
```

What happens:

* A verification URL and short code are displayed in your terminal
* Your browser opens to the verification URL
* Enter/confirm the code to complete authentication

Notes:

* The OAuth2 provider and domain are configured via `crewai config` (defaults use `login.crewai.com`)
* After successful login, the CLI also attempts to authenticate to the Tool Repository automatically
* If you reset your configuration, run `crewai login` again to re-authenticate

### [​](#12-api-keys) 12. API Keys

When running `crewai create crew` command, the CLI will show you a list of available LLM providers to choose from, followed by model selection for your chosen provider.
Once you’ve selected an LLM provider and model, you will be prompted for API keys.

#### [​](#available-llm-providers) Available LLM Providers

Here’s a list of the most popular LLM providers suggested by the CLI:

* OpenAI
* Groq
* Anthropic
* Google Gemini
* SambaNova

When you select a provider, the CLI will then show you available models for that provider and prompt you to enter your API key.

#### [​](#other-options) Other Options

If you select “other”, you will be able to select from a list of LiteLLM supported providers.
When you select a provider, the CLI will prompt you to enter the Key name and the API key.
See the following link for each provider’s key name:

* [LiteLLM Providers](https://docs.litellm.ai/docs/providers)

### [​](#13-configuration-management) 13. Configuration Management

Manage CLI configuration settings for CrewAI.

Terminal

Copy

Ask AI

```
crewai config [COMMAND] [OPTIONS]
```

#### [​](#commands:-2) Commands:

* `list`: Display all CLI configuration parameters

Terminal

Copy

Ask AI

```
crewai config list
```

* `set`: Set a CLI configuration parameter

Terminal

Copy

Ask AI

```
crewai config set <key> <value>
```

* `reset`: Reset all CLI configuration parameters to default values

Terminal

Copy

Ask AI

```
crewai config reset
```

#### [​](#available-configuration-parameters) Available Configuration Parameters

* `enterprise_base_url`: Base URL of the CrewAI AOP instance
* `oauth2_provider`: OAuth2 provider used for authentication (e.g., workos, okta, auth0)
* `oauth2_audience`: OAuth2 audience value, typically used to identify the target API or resource
* `oauth2_client_id`: OAuth2 client ID issued by the provider, used during authentication requests
* `oauth2_domain`: OAuth2 provider’s domain (e.g., your-org.auth0.com) used for issuing tokens

#### [​](#examples) Examples

Display current configuration:

Terminal

Copy

Ask AI

```
crewai config list
```

Example output:

| Setting | Value | Description |
| --- | --- | --- |
| enterprise\_base\_url | <https://app.crewai.com> | Base URL of the CrewAI AOP instance |
| org\_name | Not set | Name of the currently active organization |
| org\_uuid | Not set | UUID of the currently active organization |
| oauth2\_provider | workos | OAuth2 provider (e.g., workos, okta, auth0) |
| oauth2\_audience | client\_01YYY | Audience identifying the target API/resource |
| oauth2\_client\_id | client\_01XXX | OAuth2 client ID issued by the provider |
| oauth2\_domain | login.crewai.com | Provider domain (e.g., your-org.auth0.com) |

Set the enterprise base URL:

Terminal

Copy

Ask AI

```
crewai config set enterprise_base_url https://my-enterprise.crewai.com
```

Set OAuth2 provider:

Terminal

Copy

Ask AI

```
crewai config set oauth2_provider auth0
```

Set OAuth2 domain:

Terminal

Copy

Ask AI

```
crewai config set oauth2_domain my-company.auth0.com
```

Reset all configuration to defaults:

Terminal

Copy

Ask AI

```
crewai config reset
```

After resetting configuration, re-run `crewai login` to authenticate again.

### [​](#14-trace-management) 14. Trace Management

Manage trace collection preferences for your Crew and Flow executions.

Terminal

Copy

Ask AI

```
crewai traces [COMMAND]
```

#### [​](#commands:-3) Commands:

* `enable`: Enable trace collection for crew/flow executions

Terminal

Copy

Ask AI

```
crewai traces enable
```

* `disable`: Disable trace collection for crew/flow executions

Terminal

Copy

Ask AI

```
crewai traces disable
```

* `status`: Show current trace collection status

Terminal

Copy

Ask AI

```
crewai traces status
```

#### [​](#how-tracing-works) How Tracing Works

Trace collection is controlled by checking three settings in priority order:

1. **Explicit flag in code** (highest priority - can enable OR disable):

   Copy

   Ask AI

   ```
   crew = Crew(agents=[...], tasks=[...], tracing=True)   # Always enable
   crew = Crew(agents=[...], tasks=[...], tracing=False)  # Always disable
   crew = Crew(agents=[...], tasks=[...])                 # Check lower priorities (default)
   ```

   * `tracing=True` will **always enable** tracing (overrides everything)
   * `tracing=False` will **always disable** tracing (overrides everything)
   * `tracing=None` or omitted will check lower priority settings
2. **Environment variable** (second priority):

   Copy

   Ask AI

   ```
   CREWAI_TRACING_ENABLED=true
   ```

   * Checked only if `tracing` is not explicitly set to `True` or `False` in code
   * Set to `true` or `1` to enable tracing
3. **User preference** (lowest priority):

   Terminal

   Copy

   Ask AI

   ```
   crewai traces enable
   ```

   * Checked only if `tracing` is not set in code and `CREWAI_TRACING_ENABLED` is not set to `true`
   * Running `crewai traces enable` is sufficient to enable tracing by itself

**To enable tracing**, use any one of these methods:

* Set `tracing=True` in your Crew/Flow code, OR
* Add `CREWAI_TRACING_ENABLED=true` to your `.env` file, OR
* Run `crewai traces enable`

**To disable tracing**, use any ONE of these methods:

* Set `tracing=False` in your Crew/Flow code (overrides everything), OR
* Remove or set to `false` the `CREWAI_TRACING_ENABLED` env var, OR
* Run `crewai traces disable`

Higher priority settings override lower ones.

For more information about tracing, see the [Tracing documentation](/observability/tracing).

CrewAI CLI handles authentication to the Tool Repository automatically when adding packages to your project. Just append `crewai` before any `uv` command to use it. E.g. `crewai uv add requests`. For more information, see [Tool Repository](https://docs.crewai.com/enterprise/features/tool-repository) docs.

Configuration settings are stored in `~/.config/crewai/settings.json`. Some settings like organization name and UUID are read-only and managed through authentication and organization commands. Tool repository related settings are hidden and cannot be set directly by users.

Was this page helpful?

YesNo

[Testing

Previous](/en/concepts/testing)[Tools

Next](/en/concepts/tools)

⌘I