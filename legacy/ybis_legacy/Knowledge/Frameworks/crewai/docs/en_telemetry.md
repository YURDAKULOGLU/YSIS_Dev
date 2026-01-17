Telemetry - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Telemetry

Telemetry

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

## [​](#telemetry) Telemetry

By default, we collect no data that would be considered personal information under GDPR and other privacy regulations.
We do collect Tool’s names and Agent’s roles, so be advised not to include any personal information in the tool’s names or the Agent’s roles.
Because no personal information is collected, it’s not necessary to worry about data residency.
When `share_crew` is enabled, additional data is collected which may contain personal information if included by the user.
Users should exercise caution when enabling this feature to ensure compliance with privacy regulations.

CrewAI utilizes anonymous telemetry to gather usage statistics with the primary goal of enhancing the library.
Our focus is on improving and developing the features, integrations, and tools most utilized by our users.
It’s pivotal to understand that by default, **NO personal data is collected** concerning prompts, task descriptions, agents’ backstories or goals,
usage of tools, API calls, responses, any data processed by the agents, or secrets and environment variables.
When the `share_crew` feature is enabled, detailed data including task descriptions, agents’ backstories or goals, and other specific attributes are collected
to provide deeper insights. This expanded data collection may include personal information if users have incorporated it into their crews or tasks.
Users should carefully consider the content of their crews and tasks before enabling `share_crew`.
Users can disable telemetry by setting the environment variable `CREWAI_DISABLE_TELEMETRY` to `true` or by setting `OTEL_SDK_DISABLED` to `true` (note that the latter disables all OpenTelemetry instrumentation globally).

### [​](#examples:) Examples:

Copy

Ask AI

```
# Disable CrewAI telemetry only
os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'

# Disable all OpenTelemetry (including CrewAI)
os.environ['OTEL_SDK_DISABLED'] = 'true'
```

### [​](#data-explanation:) Data Explanation:

| Defaulted | Data | Reason and Specifics |
| --- | --- | --- |
| Yes | CrewAI and Python Version | Tracks software versions. Example: CrewAI v1.2.3, Python 3.8.10. No personal data. |
| Yes | Crew Metadata | Includes: randomly generated key and ID, process type (e.g., ‘sequential’, ‘parallel’), boolean flag for memory usage (true/false), count of tasks, count of agents. All non-personal. |
| Yes | Agent Data | Includes: randomly generated key and ID, role name (should not include personal info), boolean settings (verbose, delegation enabled, code execution allowed), max iterations, max RPM, max retry limit, LLM info (see LLM Attributes), list of tool names (should not include personal info). No personal data. |
| Yes | Task Metadata | Includes: randomly generated key and ID, boolean execution settings (async\_execution, human\_input), associated agent’s role and key, list of tool names. All non-personal. |
| Yes | Tool Usage Statistics | Includes: tool name (should not include personal info), number of usage attempts (integer), LLM attributes used. No personal data. |
| Yes | Test Execution Data | Includes: crew’s randomly generated key and ID, number of iterations, model name used, quality score (float), execution time (in seconds). All non-personal. |
| Yes | Task Lifecycle Data | Includes: creation and execution start/end times, crew and task identifiers. Stored as spans with timestamps. No personal data. |
| Yes | LLM Attributes | Includes: name, model\_name, model, top\_k, temperature, and class name of the LLM. All technical, non-personal data. |
| Yes | Crew Deployment attempt using crewAI CLI | Includes: The fact a deploy is being made and crew id, and if it’s trying to pull logs, no other data. |
| No | Agent’s Expanded Data | Includes: goal description, backstory text, i18n prompt file identifier. Users should ensure no personal info is included in text fields. |
| No | Detailed Task Information | Includes: task description, expected output description, context references. Users should ensure no personal info is included in these fields. |
| No | Environment Information | Includes: platform, release, system, version, and CPU count. Example: ‘Windows 10’, ‘x86\_64’. No personal data. |
| No | Crew and Task Inputs and Outputs | Includes: input parameters and output results as non-identifiable data. Users should ensure no personal info is included. |
| No | Comprehensive Crew Execution Data | Includes: detailed logs of crew operations, all agents and tasks data, final output. All non-personal and technical in nature. |

“No” in the “Defaulted” column indicates that this data is only collected when `share_crew` is set to `true`.

### [​](#opt-in-further-telemetry-sharing) Opt-In Further Telemetry Sharing

Users can choose to share their complete telemetry data by enabling the `share_crew` attribute to `True` in their crew configurations.
Enabling `share_crew` results in the collection of detailed crew and task execution data, including `goal`, `backstory`, `context`, and `output` of tasks.
This enables a deeper insight into usage patterns.

If you enable `share_crew`, the collected data may include personal information if it has been incorporated into crew configurations, task descriptions, or outputs.
Users should carefully review their data and ensure compliance with GDPR and other applicable privacy regulations before enabling this feature.

Was this page helpful?

YesNo

[Tool Call Hooks

Previous](/en/learn/tool-hooks)

⌘I