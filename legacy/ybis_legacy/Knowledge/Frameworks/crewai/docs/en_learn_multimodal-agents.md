Using Multimodal Agents - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Using Multimodal Agents

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

## [​](#using-multimodal-agents) Using Multimodal Agents

CrewAI supports multimodal agents that can process both text and non-text content like images. This guide will show you how to enable and use multimodal capabilities in your agents.

### [​](#enabling-multimodal-capabilities) Enabling Multimodal Capabilities

To create a multimodal agent, simply set the `multimodal` parameter to `True` when initializing your agent:

Copy

Ask AI

```
from crewai import Agent

agent = Agent(
    role="Image Analyst",
    goal="Analyze and extract insights from images",
    backstory="An expert in visual content interpretation with years of experience in image analysis",
    multimodal=True  # This enables multimodal capabilities
)
```

When you set `multimodal=True`, the agent is automatically configured with the necessary tools for handling non-text content, including the `AddImageTool`.

### [​](#working-with-images) Working with Images

The multimodal agent comes pre-configured with the `AddImageTool`, which allows it to process images. You don’t need to manually add this tool - it’s automatically included when you enable multimodal capabilities.
Here’s a complete example showing how to use a multimodal agent to analyze an image:

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create a multimodal agent
image_analyst = Agent(
    role="Product Analyst",
    goal="Analyze product images and provide detailed descriptions",
    backstory="Expert in visual product analysis with deep knowledge of design and features",
    multimodal=True
)

# Create a task for image analysis
task = Task(
    description="Analyze the product image at https://example.com/product.jpg and provide a detailed description",
    expected_output="A detailed description of the product image",
    agent=image_analyst
)

# Create and run the crew
crew = Crew(
    agents=[image_analyst],
    tasks=[task]
)

result = crew.kickoff()
```

### [​](#advanced-usage-with-context) Advanced Usage with Context

You can provide additional context or specific questions about the image when creating tasks for multimodal agents. The task description can include specific aspects you want the agent to focus on:

Copy

Ask AI

```
from crewai import Agent, Task, Crew

# Create a multimodal agent for detailed analysis
expert_analyst = Agent(
    role="Visual Quality Inspector",
    goal="Perform detailed quality analysis of product images",
    backstory="Senior quality control expert with expertise in visual inspection",
    multimodal=True  # AddImageTool is automatically included
)

# Create a task with specific analysis requirements
inspection_task = Task(
    description="""
    Analyze the product image at https://example.com/product.jpg with focus on:
    1. Quality of materials
    2. Manufacturing defects
    3. Compliance with standards
    Provide a detailed report highlighting any issues found.
    """,
    expected_output="A detailed report highlighting any issues found",
    agent=expert_analyst
)

# Create and run the crew
crew = Crew(
    agents=[expert_analyst],
    tasks=[inspection_task]
)

result = crew.kickoff()
```

### [​](#tool-details) Tool Details

When working with multimodal agents, the `AddImageTool` is automatically configured with the following schema:

Copy

Ask AI

```
class AddImageToolSchema:
    image_url: str  # Required: The URL or path of the image to process
    action: Optional[str] = None  # Optional: Additional context or specific questions about the image
```

The multimodal agent will automatically handle the image processing through its built-in tools, allowing it to:

* Access images via URLs or local file paths
* Process image content with optional context or specific questions
* Provide analysis and insights based on the visual information and task requirements

### [​](#best-practices) Best Practices

When working with multimodal agents, keep these best practices in mind:

1. **Image Access**
   * Ensure your images are accessible via URLs that the agent can reach
   * For local images, consider hosting them temporarily or using absolute file paths
   * Verify that image URLs are valid and accessible before running tasks
2. **Task Description**
   * Be specific about what aspects of the image you want the agent to analyze
   * Include clear questions or requirements in the task description
   * Consider using the optional `action` parameter for focused analysis
3. **Resource Management**
   * Image processing may require more computational resources than text-only tasks
   * Some language models may require base64 encoding for image data
   * Consider batch processing for multiple images to optimize performance
4. **Environment Setup**
   * Verify that your environment has the necessary dependencies for image processing
   * Ensure your language model supports multimodal capabilities
   * Test with small images first to validate your setup
5. **Error Handling**
   * Implement proper error handling for image loading failures
   * Have fallback strategies for when image processing fails
   * Monitor and log image processing operations for debugging

Was this page helpful?

YesNo

[Connect to any LLM

Previous](/en/learn/llm-connections)[Replay Tasks from Latest Crew Kickoff

Next](/en/learn/replay-tasks-from-latest-crew-kickoff)

⌘I