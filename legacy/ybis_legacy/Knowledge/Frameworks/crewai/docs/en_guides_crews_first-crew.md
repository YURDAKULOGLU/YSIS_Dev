Build Your First Crew - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Crews

Build Your First Crew

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

  + [Build Your First Crew](/en/guides/crews/first-crew)
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

## [​](#unleashing-the-power-of-collaborative-ai) Unleashing the Power of Collaborative AI

Imagine having a team of specialized AI agents working together seamlessly to solve complex problems, each contributing their unique skills to achieve a common goal. This is the power of CrewAI - a framework that enables you to create collaborative AI systems that can accomplish tasks far beyond what a single AI could achieve alone.
In this guide, we’ll walk through creating a research crew that will help us research and analyze a topic, then create a comprehensive report. This practical example demonstrates how AI agents can collaborate to accomplish complex tasks, but it’s just the beginning of what’s possible with CrewAI.

### [​](#what-you’ll-build-and-learn) What You’ll Build and Learn

By the end of this guide, you’ll have:

1. **Created a specialized AI research team** with distinct roles and responsibilities
2. **Orchestrated collaboration** between multiple AI agents
3. **Automated a complex workflow** that involves gathering information, analysis, and report generation
4. **Built foundational skills** that you can apply to more ambitious projects

While we’re building a simple research crew in this guide, the same patterns and techniques can be applied to create much more sophisticated teams for tasks like:

* Multi-stage content creation with specialized writers, editors, and fact-checkers
* Complex customer service systems with tiered support agents
* Autonomous business analysts that gather data, create visualizations, and generate insights
* Product development teams that ideate, design, and plan implementation

Let’s get started building your first crew!

### [​](#prerequisites) Prerequisites

Before starting, make sure you have:

1. Installed CrewAI following the [installation guide](/en/installation)
2. Set up your LLM API key in your environment, following the [LLM setup
   guide](/en/concepts/llms#setting-up-your-llm)
3. Basic understanding of Python

## [​](#step-1:-create-a-new-crewai-project) Step 1: Create a New CrewAI Project

First, let’s create a new CrewAI project using the CLI. This command will set up a complete project structure with all the necessary files, allowing you to focus on defining your agents and their tasks rather than setting up boilerplate code.

Copy

Ask AI

```
crewai create crew research_crew
cd research_crew
```

This will generate a project with the basic structure needed for your crew. The CLI automatically creates:

* A project directory with the necessary files
* Configuration files for agents and tasks
* A basic crew implementation
* A main script to run the crew

![CrewAI Framework Overview](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crews.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=514fd0b06e4128e62f10728d44601975)

CrewAI Framework Overview

## [​](#step-2:-explore-the-project-structure) Step 2: Explore the Project Structure

Let’s take a moment to understand the project structure created by the CLI. CrewAI follows best practices for Python projects, making it easy to maintain and extend your code as your crews become more complex.

Copy

Ask AI

```
research_crew/
├── .gitignore
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── research_crew/
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

This structure follows best practices for Python projects and makes it easy to organize your code. The separation of configuration files (in YAML) from implementation code (in Python) makes it easy to modify your crew’s behavior without changing the underlying code.

## [​](#step-3:-configure-your-agents) Step 3: Configure Your Agents

Now comes the fun part - defining your AI agents! In CrewAI, agents are specialized entities with specific roles, goals, and backstories that shape their behavior. Think of them as characters in a play, each with their own personality and purpose.
For our research crew, we’ll create two agents:

1. A **researcher** who excels at finding and organizing information
2. An **analyst** who can interpret research findings and create insightful reports

Let’s modify the `agents.yaml` file to define these specialized agents. Be sure
to set `llm` to the provider you are using.

Copy

Ask AI

```
# src/research_crew/config/agents.yaml
researcher:
  role: >
    Senior Research Specialist for {topic}
  goal: >
    Find comprehensive and accurate information about {topic}
    with a focus on recent developments and key insights
  backstory: >
    You are an experienced research specialist with a talent for
    finding relevant information from various sources. You excel at
    organizing information in a clear and structured manner, making
    complex topics accessible to others.
  llm: provider/model-id  # e.g. openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...

analyst:
  role: >
    Data Analyst and Report Writer for {topic}
  goal: >
    Analyze research findings and create a comprehensive, well-structured
    report that presents insights in a clear and engaging way
  backstory: >
    You are a skilled analyst with a background in data interpretation
    and technical writing. You have a talent for identifying patterns
    and extracting meaningful insights from research data, then
    communicating those insights effectively through well-crafted reports.
  llm: provider/model-id  # e.g. openai/gpt-4o, google/gemini-2.0-flash, anthropic/claude...
```

Notice how each agent has a distinct role, goal, and backstory. These elements aren’t just descriptive - they actively shape how the agent approaches its tasks. By crafting these carefully, you can create agents with specialized skills and perspectives that complement each other.

## [​](#step-4:-define-your-tasks) Step 4: Define Your Tasks

With our agents defined, we now need to give them specific tasks to perform. Tasks in CrewAI represent the concrete work that agents will perform, with detailed instructions and expected outputs.
For our research crew, we’ll define two main tasks:

1. A **research task** for gathering comprehensive information
2. An **analysis task** for creating an insightful report

Let’s modify the `tasks.yaml` file:

Copy

Ask AI

```
# src/research_crew/config/tasks.yaml
research_task:
  description: >
    Conduct thorough research on {topic}. Focus on:
    1. Key concepts and definitions
    2. Historical development and recent trends
    3. Major challenges and opportunities
    4. Notable applications or case studies
    5. Future outlook and potential developments

    Make sure to organize your findings in a structured format with clear sections.
  expected_output: >
    A comprehensive research document with well-organized sections covering
    all the requested aspects of {topic}. Include specific facts, figures,
    and examples where relevant.
  agent: researcher

analysis_task:
  description: >
    Analyze the research findings and create a comprehensive report on {topic}.
    Your report should:
    1. Begin with an executive summary
    2. Include all key information from the research
    3. Provide insightful analysis of trends and patterns
    4. Offer recommendations or future considerations
    5. Be formatted in a professional, easy-to-read style with clear headings
  expected_output: >
    A polished, professional report on {topic} that presents the research
    findings with added analysis and insights. The report should be well-structured
    with an executive summary, main sections, and conclusion.
  agent: analyst
  context:
    - research_task
  output_file: output/report.md
```

Note the `context` field in the analysis task - this is a powerful feature that allows the analyst to access the output of the research task. This creates a workflow where information flows naturally between agents, just as it would in a human team.

## [​](#step-5:-configure-your-crew) Step 5: Configure Your Crew

Now it’s time to bring everything together by configuring our crew. The crew is the container that orchestrates how agents work together to complete tasks.
Let’s modify the `crew.py` file:

Copy

Ask AI

```
# src/research_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class ResearchCrew():
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'] # type: ignore[index]
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

In this code, we’re:

1. Creating the researcher agent and equipping it with the SerperDevTool to search the web
2. Creating the analyst agent
3. Setting up the research and analysis tasks
4. Configuring the crew to run tasks sequentially (the analyst will wait for the researcher to finish)

This is where the magic happens - with just a few lines of code, we’ve defined a collaborative AI system where specialized agents work together in a coordinated process.

## [​](#step-6:-set-up-your-main-script) Step 6: Set Up Your Main Script

Now, let’s set up the main script that will run our crew. This is where we provide the specific topic we want our crew to research.

Copy

Ask AI

```
#!/usr/bin/env python
# src/research_crew/main.py
import os
from research_crew.crew import ResearchCrew

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the research crew.
    """
    inputs = {
        'topic': 'Artificial Intelligence in Healthcare'
    }

    # Create and run the crew
    result = ResearchCrew().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()
```

This script prepares the environment, specifies our research topic, and kicks off the crew’s work. The power of CrewAI is evident in how simple this code is - all the complexity of managing multiple AI agents is handled by the framework.

## [​](#step-7:-set-up-your-environment-variables) Step 7: Set Up Your Environment Variables

Create a `.env` file in your project root with your API keys:

Copy

Ask AI

```
SERPER_API_KEY=your_serper_api_key
# Add your provider's API key here too.
```

See the [LLM Setup guide](/en/concepts/llms#setting-up-your-llm) for details on configuring your provider of choice. You can get a Serper API key from [Serper.dev](https://serper.dev/).

## [​](#step-8:-install-dependencies) Step 8: Install Dependencies

Install the required dependencies using the CrewAI CLI:

Copy

Ask AI

```
crewai install
```

This command will:

1. Read the dependencies from your project configuration
2. Create a virtual environment if needed
3. Install all required packages

## [​](#step-9:-run-your-crew) Step 9: Run Your Crew

Now for the exciting moment - it’s time to run your crew and see AI collaboration in action!

Copy

Ask AI

```
crewai run
```

When you run this command, you’ll see your crew spring to life. The researcher will gather information about the specified topic, and the analyst will then create a comprehensive report based on that research. You’ll see the agents’ thought processes, actions, and outputs in real-time as they work together to complete their tasks.

## [​](#step-10:-review-the-output) Step 10: Review the Output

Once the crew completes its work, you’ll find the final report in the `output/report.md` file. The report will include:

1. An executive summary
2. Detailed information about the topic
3. Analysis and insights
4. Recommendations or future considerations

Take a moment to appreciate what you’ve accomplished - you’ve created a system where multiple AI agents collaborated on a complex task, each contributing their specialized skills to produce a result that’s greater than what any single agent could achieve alone.

## [​](#exploring-other-cli-commands) Exploring Other CLI Commands

CrewAI offers several other useful CLI commands for working with crews:

Copy

Ask AI

```
# View all available commands
crewai --help

# Run the crew
crewai run

# Test the crew
crewai test

# Reset crew memories
crewai reset-memories

# Replay from a specific task
crewai replay -t <task_id>
```

## [​](#the-art-of-the-possible:-beyond-your-first-crew) The Art of the Possible: Beyond Your First Crew

What you’ve built in this guide is just the beginning. The skills and patterns you’ve learned can be applied to create increasingly sophisticated AI systems. Here are some ways you could extend this basic research crew:

### [​](#expanding-your-crew) Expanding Your Crew

You could add more specialized agents to your crew:

* A **fact-checker** to verify research findings
* A **data visualizer** to create charts and graphs
* A **domain expert** with specialized knowledge in a particular area
* A **critic** to identify weaknesses in the analysis

### [​](#adding-tools-and-capabilities) Adding Tools and Capabilities

You could enhance your agents with additional tools:

* Web browsing tools for real-time research
* CSV/database tools for data analysis
* Code execution tools for data processing
* API connections to external services

### [​](#creating-more-complex-workflows) Creating More Complex Workflows

You could implement more sophisticated processes:

* Hierarchical processes where manager agents delegate to worker agents
* Iterative processes with feedback loops for refinement
* Parallel processes where multiple agents work simultaneously
* Dynamic processes that adapt based on intermediate results

### [​](#applying-to-different-domains) Applying to Different Domains

The same patterns can be applied to create crews for:

* **Content creation**: Writers, editors, fact-checkers, and designers working together
* **Customer service**: Triage agents, specialists, and quality control working together
* **Product development**: Researchers, designers, and planners collaborating
* **Data analysis**: Data collectors, analysts, and visualization specialists

## [​](#next-steps) Next Steps

Now that you’ve built your first crew, you can:

1. Experiment with different agent configurations and personalities
2. Try more complex task structures and workflows
3. Implement custom tools to give your agents new capabilities
4. Apply your crew to different topics or problem domains
5. Explore [CrewAI Flows](/en/guides/flows/first-flow) for more advanced workflows with procedural programming

Congratulations! You’ve successfully built your first CrewAI crew that can research and analyze any topic you provide. This foundational experience has equipped you with the skills to create increasingly sophisticated AI systems that can tackle complex, multi-stage problems through collaborative intelligence.

Was this page helpful?

YesNo

[Crafting Effective Agents

Previous](/en/guides/agents/crafting-effective-agents)[Build Your First Flow

Next](/en/guides/flows/first-flow)

⌘I