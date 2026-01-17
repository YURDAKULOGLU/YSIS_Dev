Connect to any LLM - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Connect to any LLM

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

## [​](#connect-crewai-to-llms) Connect CrewAI to LLMs

CrewAI uses LiteLLM to connect to a wide variety of Language Models (LLMs). This integration provides extensive versatility, allowing you to use models from numerous providers with a simple, unified interface.

By default, CrewAI uses the `gpt-4o-mini` model. This is determined by the `OPENAI_MODEL_NAME` environment variable, which defaults to “gpt-4o-mini” if not set.
You can easily configure your agents to use a different model or provider as described in this guide.

## [​](#supported-providers) Supported Providers

LiteLLM supports a wide range of providers, including but not limited to:

* OpenAI
* Anthropic
* Google (Vertex AI, Gemini)
* Azure OpenAI
* AWS (Bedrock, SageMaker)
* Cohere
* VoyageAI
* Hugging Face
* Ollama
* Mistral AI
* Replicate
* Together AI
* AI21
* Cloudflare Workers AI
* DeepInfra
* Groq
* SambaNova
* Nebius AI Studio
* [NVIDIA NIMs](https://docs.api.nvidia.com/nim/reference/models-1)
* And many more!

For a complete and up-to-date list of supported providers, please refer to the [LiteLLM Providers documentation](https://docs.litellm.ai/docs/providers).

## [​](#changing-the-llm) Changing the LLM

To use a different LLM with your CrewAI agents, you have several options:

* Using a String Identifier
* Using the LLM Class

Pass the model name as a string when initializing the agent:

Code

Copy

Ask AI

```
from crewai import Agent

# Using OpenAI's GPT-4
openai_agent = Agent(
    role='OpenAI Expert',
    goal='Provide insights using GPT-4',
    backstory="An AI assistant powered by OpenAI's latest model.",
    llm='gpt-4'
)

# Using Anthropic's Claude
claude_agent = Agent(
    role='Anthropic Expert',
    goal='Analyze data using Claude',
    backstory="An AI assistant leveraging Anthropic's language model.",
    llm='claude-2'
)
```

For more detailed configuration, use the LLM class:

Code

Copy

Ask AI

```
from crewai import Agent, LLM

llm = LLM(
    model="gpt-4",
    temperature=0.7,
    base_url="https://api.openai.com/v1",
    api_key="your-api-key-here"
)

agent = Agent(
    role='Customized LLM Expert',
    goal='Provide tailored responses',
    backstory="An AI assistant with custom LLM settings.",
    llm=llm
)
```

## [​](#configuration-options) Configuration Options

When configuring an LLM for your agent, you have access to a wide range of parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| **model** | `str` | The name of the model to use (e.g., “gpt-4”, “claude-2”) |
| **temperature** | `float` | Controls randomness in output (0.0 to 1.0) |
| **max\_tokens** | `int` | Maximum number of tokens to generate |
| **top\_p** | `float` | Controls diversity of output (0.0 to 1.0) |
| **frequency\_penalty** | `float` | Penalizes new tokens based on their frequency in the text so far |
| **presence\_penalty** | `float` | Penalizes new tokens based on their presence in the text so far |
| **stop** | `str`, `List[str]` | Sequence(s) to stop generation |
| **base\_url** | `str` | The base URL for the API endpoint |
| **api\_key** | `str` | Your API key for authentication |

For a complete list of parameters and their descriptions, refer to the LLM class documentation.

## [​](#connecting-to-openai-compatible-llms) Connecting to OpenAI-Compatible LLMs

You can connect to OpenAI-compatible LLMs using either environment variables or by setting specific attributes on the LLM class:

* Using Environment Variables
* Using LLM Class Attributes

Generic

Google

Copy

Ask AI

```
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["OPENAI_API_BASE"] = "https://api.your-provider.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "your-model-name"
```

Generic

Google

Copy

Ask AI

```
llm = LLM(
    model="custom-model-name",
    api_key="your-api-key",
    base_url="https://api.your-provider.com/v1"
)
agent = Agent(llm=llm, ...)
```

## [​](#using-local-models-with-ollama) Using Local Models with Ollama

For local models like those provided by Ollama:

1

Download and install Ollama

[Click here to download and install Ollama](https://ollama.com/download)

2

Pull the desired model

For example, run `ollama pull llama3.2` to download the model.

3

Configure your agent

Code

Copy

Ask AI

```
    agent = Agent(
        role='Local AI Expert',
        goal='Process information using a local model',
        backstory="An AI assistant running on local hardware.",
        llm=LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
    )
```

## [​](#changing-the-base-api-url) Changing the Base API URL

You can change the base API URL for any LLM provider by setting the `base_url` parameter:

Code

Copy

Ask AI

```
llm = LLM(
    model="custom-model-name",
    base_url="https://api.your-provider.com/v1",
    api_key="your-api-key"
)
agent = Agent(llm=llm, ...)
```

This is particularly useful when working with OpenAI-compatible APIs or when you need to specify a different endpoint for your chosen provider.

## [​](#conclusion) Conclusion

By leveraging LiteLLM, CrewAI offers seamless integration with a vast array of LLMs. This flexibility allows you to choose the most suitable model for your specific needs, whether you prioritize performance, cost-efficiency, or local deployment. Remember to consult the [LiteLLM documentation](https://docs.litellm.ai/docs/) for the most up-to-date information on supported models and configuration options.

Was this page helpful?

YesNo

[Kickoff Crew for Each

Previous](/en/learn/kickoff-for-each)[Using Multimodal Agents

Next](/en/learn/multimodal-agents)

⌘I