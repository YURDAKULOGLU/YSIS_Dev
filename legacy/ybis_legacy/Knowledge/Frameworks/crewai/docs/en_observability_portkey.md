Portkey Integration - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Observability

Portkey Integration

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

![Portkey CrewAI Header Image](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/main/Portkey-CrewAI.png)

## [​](#introduction) Introduction

Portkey enhances CrewAI with production-readiness features, turning your experimental agent crews into robust systems by providing:

* **Complete observability** of every agent step, tool use, and interaction
* **Built-in reliability** with fallbacks, retries, and load balancing
* **Cost tracking and optimization** to manage your AI spend
* **Access to 200+ LLMs** through a single integration
* **Guardrails** to keep agent behavior safe and compliant
* **Version-controlled prompts** for consistent agent performance

### [​](#installation-&-setup) Installation & Setup

1

Install the required packages

Copy

Ask AI

```
pip install -U crewai portkey-ai
```

Generate API Key

Create a Portkey API key with optional budget/rate limits from the [Portkey dashboard](https://app.portkey.ai/). You can also attach configurations for reliability, caching, and more to this key. More on this later.

3

Configure CrewAI with Portkey

The integration is simple - you just need to update the LLM configuration in your CrewAI setup:

Copy

Ask AI

```
from crewai import LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Create an LLM instance with Portkey integration
gpt_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",  # We are using a Virtual key, so this is a placeholder
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_LLM_VIRTUAL_KEY",
        trace_id="unique-trace-id",               # Optional, for request tracing
    )
)

#Use them in your Crew Agents like this:

	@agent
	def lead_market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_market_analyst'],
			verbose=True,
			memory=False,
			llm=gpt_llm
		)
```

**What are Virtual Keys?** Virtual keys in Portkey securely store your LLM provider API keys (OpenAI, Anthropic, etc.) in an encrypted vault. They allow for easier key rotation and budget management. [Learn more about virtual keys here](https://portkey.ai/docs/product/ai-gateway/virtual-keys).

## [​](#production-features) Production Features

### [​](#1-enhanced-observability) 1. Enhanced Observability

Portkey provides comprehensive observability for your CrewAI agents, helping you understand exactly what’s happening during each execution.

* Traces
* Logs
* Metrics & Dashboards
* Metadata Filtering

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Product%2011.1.webp)

Traces provide a hierarchical view of your crew’s execution, showing the sequence of LLM calls, tool invocations, and state transitions.

Copy

Ask AI

```
# Add trace_id to enable hierarchical tracing in Portkey
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        trace_id="unique-session-id"  # Add unique trace ID
    )
)
```

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Portkey%20Docs%20Metadata.png)

Portkey logs every interaction with LLMs, including:

* Complete request and response payloads
* Latency and token usage metrics
* Cost calculations
* Tool calls and function executions

All logs can be filtered by metadata, trace IDs, models, and more, making it easy to debug specific crew runs.

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Dashboard.png)

Portkey provides built-in dashboards that help you:

* Track cost and token usage across all crew runs
* Analyze performance metrics like latency and success rates
* Identify bottlenecks in your agent workflows
* Compare different crew configurations and LLMs

You can filter and segment all metrics by custom metadata to analyze specific crew types, user groups, or use cases.

![Analytics with metadata filters](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/Metadata%20Filters%20from%20CrewAI.png)

Add custom metadata to your CrewAI LLM configuration to enable powerful filtering and segmentation:

Copy

Ask AI

```
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        metadata={
            "crew_type": "research_crew",
            "environment": "production",
            "_user": "user_123",   # Special _user field for user analytics
            "request_source": "mobile_app"
        }
    )
)
```

This metadata can be used to filter logs, traces, and metrics on the Portkey dashboard, allowing you to analyze specific crew runs, users, or environments.

### [​](#2-reliability-keep-your-crews-running-smoothly) 2. Reliability - Keep Your Crews Running Smoothly

When running crews in production, things can go wrong - API rate limits, network issues, or provider outages. Portkey’s reliability features ensure your agents keep running smoothly even when problems occur.
It’s simple to enable fallback in your CrewAI setup by using a Portkey Config:

Copy

Ask AI

```
from crewai import LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Create LLM with fallback configuration
portkey_llm = LLM(
    model="gpt-4o",
    max_tokens=1000,
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        config={
            "strategy": {
                "mode": "fallback"
            },
            "targets": [
                {
                    "provider": "openai",
                    "api_key": "YOUR_OPENAI_API_KEY",
                    "override_params": {"model": "gpt-4o"}
                },
                {
                    "provider": "anthropic",
                    "api_key": "YOUR_ANTHROPIC_API_KEY",
                    "override_params": {"model": "claude-3-opus-20240229"}
                }
            ]
        }
    )
)

# Use this LLM configuration with your agents
```

This configuration will automatically try Claude if the GPT-4o request fails, ensuring your crew can continue operating.

[## Automatic Retries

Handles temporary failures automatically. If an LLM call fails, Portkey will retry the same request for the specified number of times - perfect for rate limits or network blips.](https://portkey.ai/docs/product/ai-gateway/automatic-retries)[## Request Timeouts

Prevent your agents from hanging. Set timeouts to ensure you get responses (or can fail gracefully) within your required timeframes.](https://portkey.ai/docs/product/ai-gateway/request-timeouts)[## Conditional Routing

Send different requests to different providers. Route complex reasoning to GPT-4, creative tasks to Claude, and quick responses to Gemini based on your needs.](https://portkey.ai/docs/product/ai-gateway/conditional-routing)[## Fallbacks

Keep running even if your primary provider fails. Automatically switch to backup providers to maintain availability.](https://portkey.ai/docs/product/ai-gateway/fallbacks)[## Load Balancing

Spread requests across multiple API keys or providers. Great for high-volume crew operations and staying within rate limits.](https://portkey.ai/docs/product/ai-gateway/load-balancing)

### [​](#3-prompting-in-crewai) 3. Prompting in CrewAI

Portkey’s Prompt Engineering Studio helps you create, manage, and optimize the prompts used in your CrewAI agents. Instead of hardcoding prompts or instructions, use Portkey’s prompt rendering API to dynamically fetch and apply your versioned prompts.

![Prompt Playground Interface](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Portkey%20Docs.webp)

Manage prompts in Portkey's Prompt Library

* Prompt Playground
* Using Prompt Templates
* Prompt Versioning
* Mustache Templating for variables

Prompt Playground is a place to compare, test and deploy perfect prompts for your AI application. It’s where you experiment with different models, test variables, compare outputs, and refine your prompt engineering strategy before deploying to production. It allows you to:

1. Iteratively develop prompts before using them in your agents
2. Test prompts with different variables and models
3. Compare outputs between different prompt versions
4. Collaborate with team members on prompt development

This visual environment makes it easier to craft effective prompts for each step in your CrewAI agents’ workflow.

The Prompt Render API retrieves your prompt templates with all parameters configured:

Copy

Ask AI

```
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL, Portkey

# Initialize Portkey admin client
portkey_admin = Portkey(api_key="YOUR_PORTKEY_API_KEY")

# Retrieve prompt using the render API
prompt_data = portkey_client.prompts.render(
    prompt_id="YOUR_PROMPT_ID",
    variables={
        "agent_role": "Senior Research Scientist",
    }
)

backstory_agent_prompt=prompt_data.data.messages[0]["content"]


# Set up LLM with Portkey integration
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY"
    )
)

# Create agent using the rendered prompt
researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory=backstory_agent,  # Use the rendered prompt
    verbose=True,
    llm=portkey_llm
)
```

You can:

* Create multiple versions of the same prompt
* Compare performance between versions
* Roll back to previous versions if needed
* Specify which version to use in your code:

Copy

Ask AI

```
# Use a specific prompt version
prompt_data = portkey_admin.prompts.render(
    prompt_id="YOUR_PROMPT_ID@version_number",
    variables={
        "agent_role": "Senior Research Scientist",
        "agent_goal": "Discover groundbreaking insights"
    }
)
```

Portkey prompts use Mustache-style templating for easy variable substitution:

Copy

Ask AI

```
You are a {{agent_role}} with expertise in {{domain}}.

Your mission is to {{agent_goal}} by leveraging your knowledge
and experience in the field.

Always maintain a {{tone}} tone and focus on providing {{focus_area}}.
```

When rendering, simply pass the variables:

Copy

Ask AI

```
prompt_data = portkey_admin.prompts.render(
    prompt_id="YOUR_PROMPT_ID",
    variables={
        "agent_role": "Senior Research Scientist",
        "domain": "artificial intelligence",
        "agent_goal": "discover groundbreaking insights",
        "tone": "professional",
        "focus_area": "practical applications"
    }
)
```

[## Prompt Engineering Studio

Learn more about Portkey’s prompt management features](https://portkey.ai/docs/product/prompt-library)

### [​](#4-guardrails-for-safe-crews) 4. Guardrails for Safe Crews

Guardrails ensure your CrewAI agents operate safely and respond appropriately in all situations.
**Why Use Guardrails?**
CrewAI agents can experience various failure modes:

* Generating harmful or inappropriate content
* Leaking sensitive information like PII
* Hallucinating incorrect information
* Generating outputs in incorrect formats

Portkey’s guardrails add protections for both inputs and outputs.
**Implementing Guardrails**

Copy

Ask AI

```
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Create LLM with guardrails
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        config={
            "input_guardrails": ["guardrails-id-xxx", "guardrails-id-yyy"],
            "output_guardrails": ["guardrails-id-zzz"]
        }
    )
)

# Create agent with guardrailed LLM
researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

Portkey’s guardrails can:

* Detect and redact PII in both inputs and outputs
* Filter harmful or inappropriate content
* Validate response formats against schemas
* Check for hallucinations against ground truth
* Apply custom business logic and rules

[## Learn More About Guardrails

Explore Portkey’s guardrail features to enhance agent safety](https://portkey.ai/docs/product/guardrails)

### [​](#5-user-tracking-with-metadata) 5. User Tracking with Metadata

Track individual users through your CrewAI agents using Portkey’s metadata system.
**What is Metadata in Portkey?**
Metadata allows you to associate custom data with each request, enabling filtering, segmentation, and analytics. The special `_user` field is specifically designed for user tracking.

Copy

Ask AI

```
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Configure LLM with user tracking
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        metadata={
            "_user": "user_123",  # Special _user field for user analytics
            "user_tier": "premium",
            "user_company": "Acme Corp",
            "session_id": "abc-123"
        }
    )
)

# Create agent with tracked LLM
researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

**Filter Analytics by User**
With metadata in place, you can filter analytics by user and analyze performance metrics on a per-user basis:

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/Metadata%20Filters%20from%20CrewAI.png)

Filter analytics by user

This enables:

* Per-user cost tracking and budgeting
* Personalized user analytics
* Team or organization-level metrics
* Environment-specific monitoring (staging vs. production)

[## Learn More About Metadata

Explore how to use custom metadata to enhance your analytics](https://portkey.ai/docs/product/observability/metadata)

### [​](#6-caching-for-efficient-crews) 6. Caching for Efficient Crews

Implement caching to make your CrewAI agents more efficient and cost-effective:

* Simple Caching
* Semantic Caching

Copy

Ask AI

```
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Configure LLM with simple caching
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        config={
            "cache": {
                "mode": "simple"
            }
        }
    )
)

# Create agent with cached LLM
researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

Simple caching performs exact matches on input prompts, caching identical requests to avoid redundant model executions.

Copy

Ask AI

```
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Configure LLM with semantic caching
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY",
        config={
            "cache": {
                "mode": "semantic"
            }
        }
    )
)

# Create agent with semantically cached LLM
researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

Semantic caching considers the contextual similarity between input requests, caching responses for semantically similar inputs.

### [​](#7-model-interoperability) 7. Model Interoperability

CrewAI supports multiple LLM providers, and Portkey extends this capability by providing access to over 200 LLMs through a unified interface. You can easily switch between different models without changing your core agent logic:

Copy

Ask AI

```
from crewai import Agent, LLM
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

# Set up LLMs with different providers
openai_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_OPENAI_VIRTUAL_KEY"
    )
)

anthropic_llm = LLM(
    model="claude-3-5-sonnet-latest",
    max_tokens=1000,
    base_url=PORTKEY_GATEWAY_URL,
    api_key="dummy",
    extra_headers=createHeaders(
        api_key="YOUR_PORTKEY_API_KEY",
        virtual_key="YOUR_ANTHROPIC_VIRTUAL_KEY"
    )
)

# Choose which LLM to use for each agent based on your needs
researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=openai_llm  # Use anthropic_llm for Anthropic
)
```

Portkey provides access to LLMs from providers including:

* OpenAI (GPT-4o, GPT-4 Turbo, etc.)
* Anthropic (Claude 3.5 Sonnet, Claude 3 Opus, etc.)
* Mistral AI (Mistral Large, Mistral Medium, etc.)
* Google Vertex AI (Gemini 1.5 Pro, etc.)
* Cohere (Command, Command-R, etc.)
* AWS Bedrock (Claude, Titan, etc.)
* Local/Private Models

[## Supported Providers

See the full list of LLM providers supported by Portkey](https://portkey.ai/docs/integrations/llms)

## [​](#set-up-enterprise-governance-for-crewai) Set Up Enterprise Governance for CrewAI

**Why Enterprise Governance?**
If you are using CrewAI inside your organization, you need to consider several governance aspects:

* **Cost Management**: Controlling and tracking AI spending across teams
* **Access Control**: Managing which teams can use specific models
* **Usage Analytics**: Understanding how AI is being used across the organization
* **Security & Compliance**: Maintaining enterprise security standards
* **Reliability**: Ensuring consistent service across all users

Portkey adds a comprehensive governance layer to address these enterprise needs. Let’s implement these controls step by step.

1

Create Virtual Key

Virtual Keys are Portkey’s secure way to manage your LLM provider API keys. They provide essential controls like:

* Budget limits for API usage
* Rate limiting capabilities
* Secure API key storage

To create a virtual key:
Go to [Virtual Keys](https://app.portkey.ai/virtual-keys) in the Portkey App. Save and copy the virtual key ID

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/Virtual%20Key%20from%20Portkey%20Docs.png)

Save your virtual key ID - you’ll need it for the next step.

2

Create Default Config

Configs in Portkey define how your requests are routed, with features like advanced routing, fallbacks, and retries.To create your config:

1. Go to [Configs](https://app.portkey.ai/configs) in Portkey dashboard
2. Create new config with:

   Copy

   Ask AI

   ```
   {
       "virtual_key": "YOUR_VIRTUAL_KEY_FROM_STEP1",
      	"override_params": {
         "model": "gpt-4o" // Your preferred model name
       }
   }
   ```
3. Save and note the Config name for the next step

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20Portkey%20Docs%20Config.png)

3

Configure Portkey API Key

Now create a Portkey API key and attach the config you created in Step 2:

1. Go to [API Keys](https://app.portkey.ai/api-keys) in Portkey and Create new API key
2. Select your config from `Step 2`
3. Generate and save your API key

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/CrewAI%20API%20Key.png)

4

Connect to CrewAI

After setting up your Portkey API key with the attached config, connect it to your CrewAI agents:

Copy

Ask AI

```
from crewai import Agent, LLM
from portkey_ai import PORTKEY_GATEWAY_URL

# Configure LLM with your API key
portkey_llm = LLM(
    model="gpt-4o",
    base_url=PORTKEY_GATEWAY_URL,
    api_key="YOUR_PORTKEY_API_KEY"
)

# Create agent with Portkey-enabled LLM
researcher = Agent(
    role="Senior Research Scientist",
    goal="Discover groundbreaking insights about the assigned topic",
    backstory="You are an expert researcher with deep domain knowledge.",
    verbose=True,
    llm=portkey_llm
)
```

Step 1: Implement Budget Controls & Rate Limits

### [​](#step-1:-implement-budget-controls-&-rate-limits) Step 1: Implement Budget Controls & Rate Limits

Virtual Keys enable granular control over LLM access at the team/department level. This helps you:

* Set up [budget limits](https://portkey.ai/docs/product/ai-gateway/virtual-keys/budget-limits)
* Prevent unexpected usage spikes using Rate limits
* Track departmental spending

#### [​](#setting-up-department-specific-controls:) Setting Up Department-Specific Controls:

1. Navigate to [Virtual Keys](https://app.portkey.ai/virtual-keys) in Portkey dashboard
2. Create new Virtual Key for each department with budget limits and rate limits
3. Configure department-specific limits

![](https://raw.githubusercontent.com/siddharthsambharia-portkey/Portkey-Product-Images/refs/heads/main/Virtual%20Key%20from%20Portkey%20Docs.png)

Step 2: Define Model Access Rules

### [​](#step-2:-define-model-access-rules) Step 2: Define Model Access Rules

As your AI usage scales, controlling which teams can access specific models becomes crucial. Portkey Configs provide this control layer with features like:

#### [​](#access-control-features:) Access Control Features:

* **Model Restrictions**: Limit access to specific models
* **Data Protection**: Implement guardrails for sensitive data
* **Reliability Controls**: Add fallbacks and retry logic

#### [​](#example-configuration:) Example Configuration:

Here’s a basic configuration to route requests to OpenAI, specifically using GPT-4o:

Copy

Ask AI

```
{
	"strategy": {
		"mode": "single"
	},
	"targets": [
		{
			"virtual_key": "YOUR_OPENAI_VIRTUAL_KEY",
			"override_params": {
				"model": "gpt-4o"
			}
		}
	]
}
```

Create your config on the [Configs page](https://app.portkey.ai/configs) in your Portkey dashboard.

Configs can be updated anytime to adjust controls without affecting running applications.

Step 3: Implement Access Controls

### [​](#step-3:-implement-access-controls) Step 3: Implement Access Controls

Create User-specific API keys that automatically:

* Track usage per user/team with the help of virtual keys
* Apply appropriate configs to route requests
* Collect relevant metadata to filter logs
* Enforce access permissions

Create API keys through the [Portkey App](https://app.portkey.ai/)Example using Python SDK:

Copy

Ask AI

```
from portkey_ai import Portkey

portkey = Portkey(api_key="YOUR_ADMIN_API_KEY")

api_key = portkey.api_keys.create(
    name="engineering-team",
    type="organisation",
    workspace_id="YOUR_WORKSPACE_ID",
    defaults={
        "config_id": "your-config-id",
        "metadata": {
            "environment": "production",
            "department": "engineering"
        }
    },
    scopes=["logs.view", "configs.read"]
)
```

For detailed key management instructions, see the [Portkey documentation](https://portkey.ai/docs).

Step 4: Deploy & Monitor

### [​](#step-4:-deploy-&-monitor) Step 4: Deploy & Monitor

After distributing API keys to your team members, your enterprise-ready CrewAI setup is ready to go. Each team member can now use their designated API keys with appropriate access levels and budget controls.Monitor usage in Portkey dashboard:

* Cost tracking by department
* Model usage patterns
* Request volumes
* Error rates

### [​](#enterprise-features-now-available) Enterprise Features Now Available

**Your CrewAI integration now has:**

* Departmental budget controls
* Model access governance
* Usage tracking & attribution
* Security guardrails
* Reliability features

## [​](#frequently-asked-questions) Frequently Asked Questions

How does Portkey enhance CrewAI?

Portkey adds production-readiness to CrewAI through comprehensive observability (traces, logs, metrics), reliability features (fallbacks, retries, caching), and access to 200+ LLMs through a unified interface. This makes it easier to debug, optimize, and scale your agent applications.

Can I use Portkey with existing CrewAI applications?

Yes! Portkey integrates seamlessly with existing CrewAI applications. You just need to update your LLM configuration code with the Portkey-enabled version. The rest of your agent and crew code remains unchanged.

Does Portkey work with all CrewAI features?

Portkey supports all CrewAI features, including agents, tools, human-in-the-loop workflows, and all task process types (sequential, hierarchical, etc.). It adds observability and reliability without limiting any of the framework’s functionality.

Can I track usage across multiple agents in a crew?

Yes, Portkey allows you to use a consistent `trace_id` across multiple agents in a crew to track the entire workflow. This is especially useful for complex crews where you want to understand the full execution path across multiple agents.

How do I filter logs and traces for specific crew runs?

Portkey allows you to add custom metadata to your LLM configuration, which you can then use for filtering. Add fields like `crew_name`, `crew_type`, or `session_id` to easily find and analyze specific crew executions.

Can I use my own API keys with Portkey?

Yes! Portkey uses your own API keys for the various LLM providers. It securely stores them as virtual keys, allowing you to easily manage and rotate keys without changing your code.

## [​](#resources) Resources

[## CrewAI Docs

Official CrewAI documentation](https://docs.crewai.com/)[## Book a Demo

Get personalized guidance on implementing this integration](https://calendly.com/portkey-ai)

Was this page helpful?

YesNo

[Patronus AI Evaluation

Previous](/en/observability/patronus-evaluation)[Weave Integration

Next](/en/observability/weave)

⌘I