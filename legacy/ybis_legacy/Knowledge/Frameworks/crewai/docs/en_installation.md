Installation - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘K

Search...

Navigation

Get Started

Installation

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

## [​](#video-tutorial) Video Tutorial

Watch this video tutorial for a step-by-step demonstration of the installation process:

## [​](#text-tutorial) Text Tutorial

**Python Version Requirements**CrewAI requires `Python >=3.10 and <3.14`. Here’s how to check your version:

Copy

Ask AI

```
python3 --version
```

If you need to update Python, visit [python.org/downloads](https://python.org/downloads)

**OpenAI SDK Requirement**CrewAI 0.175.0 requires `openai >= 1.13.3`. If you manage dependencies yourself, ensure your environment satisfies this constraint to avoid import/runtime issues.

CrewAI uses the `uv` as its dependency management and package handling tool. It simplifies project setup and execution, offering a seamless experience.
If you haven’t installed `uv` yet, follow **step 1** to quickly get it set up on your system, else you can skip to **step 2**.

1

Install uv

* **On macOS/Linux:**
  Use `curl` to download the script and execute it with `sh`:

  Copy

  Ask AI

  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

  If your system doesn’t have `curl`, you can use `wget`:

  Copy

  Ask AI

  ```
  wget -qO- https://astral.sh/uv/install.sh | sh
  ```
* **On Windows:**
  Use `irm` to download the script and `iex` to execute it:

  Copy

  Ask AI

  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

  If you run into any issues, refer to [UV’s installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more information.

2

Install CrewAI 🚀

* Run the following command to install `crewai` CLI:

  Copy

  Ask AI

  ```
  uv tool install crewai
  ```

  If you encounter a `PATH` warning, run this command to update your shell:

  Copy

  Ask AI

  ```
  uv tool update-shell
  ```

  If you encounter the `chroma-hnswlib==0.7.6` build error (`fatal error C1083: Cannot open include file: 'float.h'`) on Windows, install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with *Desktop development with C++*.
* To verify that `crewai` is installed, run:

  Copy

  Ask AI

  ```
  uv tool list
  ```
* You should see something like:

  Copy

  Ask AI

  ```
  crewai v0.102.0
  - crewai
  ```
* If you need to update `crewai`, run:

  Copy

  Ask AI

  ```
  uv tool install crewai --upgrade
  ```

Installation successful! You’re ready to create your first crew! 🎉

# [​](#creating-a-crewai-project) Creating a CrewAI Project

We recommend using the `YAML` template scaffolding for a structured approach to defining agents and tasks. Here’s how to get started:

1

Generate Project Scaffolding

* Run the `crewai` CLI command:

  Copy

  Ask AI

  ```
  crewai create crew <your_project_name>
  ```
* This creates a new project with the following structure:

  Copy

  Ask AI

  ```
  my_project/
  ├── .gitignore
  ├── knowledge/
  ├── pyproject.toml
  ├── README.md
  ├── .env
  └── src/
      └── my_project/
          ├── __init__.py
          ├── main.py
          ├── crew.py
          ├── tools/
          │   ├── custom_tool.py
          │   └── __init__.py
          └── config/
              ├── agents.yaml
              └── tasks.yaml
  ```

2

Customize Your Project

* Your project will contain these essential files:

  | File | Purpose |
  | --- | --- |
  | `agents.yaml` | Define your AI agents and their roles |
  | `tasks.yaml` | Set up agent tasks and workflows |
  | `.env` | Store API keys and environment variables |
  | `main.py` | Project entry point and execution flow |
  | `crew.py` | Crew orchestration and coordination |
  | `tools/` | Directory for custom agent tools |
  | `knowledge/` | Directory for knowledge base |
* Start by editing `agents.yaml` and `tasks.yaml` to define your crew’s behavior.
* Keep sensitive information like API keys in `.env`.

3

Run your Crew

* Before you run your crew, make sure to run:

  Copy

  Ask AI

  ```
  crewai install
  ```
* If you need to install additional packages, use:

  Copy

  Ask AI

  ```
  uv add <package-name>
  ```
* To run your crew, execute the following command in the root of your project:

  Copy

  Ask AI

  ```
  crewai run
  ```

## [​](#enterprise-installation-options) Enterprise Installation Options

For teams and organizations, CrewAI offers enterprise deployment options that eliminate setup complexity:

### [​](#crewai-aop-saas) CrewAI AOP (SaaS)

* Zero installation required - just sign up for free at [app.crewai.com](https://app.crewai.com)
* Automatic updates and maintenance
* Managed infrastructure and scaling
* Build Crews with no Code

### [​](#crewai-factory-self-hosted) CrewAI Factory (Self-hosted)

* Containerized deployment for your infrastructure
* Supports any hyperscaler including on prem deployments
* Integration with your existing security systems

[## Explore Enterprise Options

Learn about CrewAI’s enterprise offerings and schedule a demo](https://crewai.com/enterprise)

## [​](#next-steps) Next Steps

[## Build Your First Agent

Follow our quickstart guide to create your first CrewAI agent and get hands-on experience.](/en/quickstart)[## Join the Community

Connect with other developers, get help, and share your CrewAI experiences.](https://community.crewai.com)

Was this page helpful?

YesNo

[Introduction

Previous](/en/introduction)[Quickstart

Next](/en/quickstart)

⌘I