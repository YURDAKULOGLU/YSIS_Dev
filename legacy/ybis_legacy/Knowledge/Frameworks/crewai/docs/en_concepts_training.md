Training - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Core Concepts

Training

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

## [​](#overview) Overview

The training feature in CrewAI allows you to train your AI agents using the command-line interface (CLI).
By running the command `crewai train -n <n_iterations>`, you can specify the number of iterations for the training process.
During training, CrewAI utilizes techniques to optimize the performance of your agents along with human feedback.
This helps the agents improve their understanding, decision-making, and problem-solving abilities.

### [​](#training-your-crew-using-the-cli) Training Your Crew Using the CLI

To use the training feature, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the directory where your CrewAI project is located.
3. Run the following command:

Copy

Ask AI

```
crewai train -n <n_iterations> -f <filename.pkl>
```

Replace `<n_iterations>` with the desired number of training iterations and `<filename>` with the appropriate filename ending with `.pkl`.

If you omit `-f`, the output defaults to `trained_agents_data.pkl` in the current working directory. You can pass an absolute path to control where the file is written.

### [​](#training-your-crew-programmatically) Training your Crew programmatically

To train your crew programmatically, use the following steps:

1. Define the number of iterations for training.
2. Specify the input parameters for the training process.
3. Execute the training command within a try-except block to handle potential errors.

Code

Copy

Ask AI

```
n_iterations = 2
inputs = {"topic": "CrewAI Training"}
filename = "your_model.pkl"

try:
    YourCrewName_Crew().crew().train(
      n_iterations=n_iterations,
      inputs=inputs,
      filename=filename
    )

except Exception as e:
    raise Exception(f"An error occurred while training the crew: {e}")
```

## [​](#how-trained-data-is-used-by-agents) How trained data is used by agents

CrewAI uses the training artifacts in two ways: during training to incorporate your human feedback, and after training to guide agents with consolidated suggestions.

### [​](#training-data-flow) Training data flow

### [​](#during-training-runs) During training runs

* On each iteration, the system records for every agent:
  + `initial_output`: the agent’s first answer
  + `human_feedback`: your inline feedback when prompted
  + `improved_output`: the agent’s follow-up answer after feedback
* This data is stored in a working file named `training_data.pkl` keyed by the agent’s internal ID and iteration.
* While training is active, the agent automatically appends your prior human feedback to its prompt to enforce those instructions on subsequent attempts within the training session.
  Training is interactive: tasks set `human_input = true`, so running in a non-interactive environment will block on user input.

### [​](#after-training-completes) After training completes

* When `train(...)` finishes, CrewAI evaluates the collected training data per agent and produces a consolidated result containing:
  + `suggestions`: clear, actionable instructions distilled from your feedback and the difference between initial/improved outputs
  + `quality`: a 0–10 score capturing improvement
  + `final_summary`: a step-by-step set of action items for future tasks
* These consolidated results are saved to the filename you pass to `train(...)` (default via CLI is `trained_agents_data.pkl`). Entries are keyed by the agent’s `role` so they can be applied across sessions.
* During normal (non-training) execution, each agent automatically loads its consolidated `suggestions` and appends them to the task prompt as mandatory instructions. This gives you consistent improvements without changing your agent definitions.

### [​](#file-summary) File summary

* `training_data.pkl` (ephemeral, per-session):
  + Structure: `agent_id -> { iteration_number: { initial_output, human_feedback, improved_output } }`
  + Purpose: capture raw data and human feedback during training
  + Location: saved in the current working directory (CWD)
* `trained_agents_data.pkl` (or your custom filename):
  + Structure: `agent_role -> { suggestions: string[], quality: number, final_summary: string }`
  + Purpose: persist consolidated guidance for future runs
  + Location: written to the CWD by default; use `-f` to set a custom (including absolute) path

## [​](#small-language-model-considerations) Small Language Model Considerations

When using smaller language models (≤7B parameters) for training data evaluation, be aware that they may face challenges with generating structured outputs and following complex instructions.

### [​](#limitations-of-small-models-in-training-evaluation) Limitations of Small Models in Training Evaluation

## JSON Output Accuracy

Smaller models often struggle with producing valid JSON responses needed for structured training evaluations, leading to parsing errors and incomplete data.

## Evaluation Quality

Models under 7B parameters may provide less nuanced evaluations with limited reasoning depth compared to larger models.

## Instruction Following

Complex training evaluation criteria may not be fully followed or considered by smaller models.

## Consistency

Evaluations across multiple training iterations may lack consistency with smaller models.

### [​](#recommendations-for-training) Recommendations for Training

* Best Practice
* Small Model Usage

For optimal training quality and reliable evaluations, we strongly recommend using models with at least 7B parameters or larger:

Copy

Ask AI

```
from crewai import Agent, Crew, Task, LLM

# Recommended minimum for training evaluation
llm = LLM(model="mistral/open-mistral-7b")

# Better options for reliable training evaluation
llm = LLM(model="anthropic/claude-3-sonnet-20240229-v1:0")
llm = LLM(model="gpt-4o")

# Use this LLM with your agents
agent = Agent(
    role="Training Evaluator",
    goal="Provide accurate training feedback",
    llm=llm
)
```

More powerful models provide higher quality feedback with better reasoning, leading to more effective training iterations.

If you must use smaller models for training evaluation, be aware of these constraints:

Copy

Ask AI

```
# Using a smaller model (expect some limitations)
llm = LLM(model="huggingface/microsoft/Phi-3-mini-4k-instruct")
```

While CrewAI includes optimizations for small models, expect less reliable and less nuanced evaluation results that may require more human intervention during training.

### [​](#key-points-to-note) Key Points to Note

* **Positive Integer Requirement:** Ensure that the number of iterations (`n_iterations`) is a positive integer. The code will raise a `ValueError` if this condition is not met.
* **Filename Requirement:** Ensure that the filename ends with `.pkl`. The code will raise a `ValueError` if this condition is not met.
* **Error Handling:** The code handles subprocess errors and unexpected exceptions, providing error messages to the user.
* Trained guidance is applied at prompt time; it does not modify your Python/YAML agent configuration.
* Agents automatically load trained suggestions from a file named `trained_agents_data.pkl` located in the current working directory. If you trained to a different filename, either rename it to `trained_agents_data.pkl` before running, or adjust the loader in code.
* You can change the output filename when calling `crewai train` with `-f/--filename`. Absolute paths are supported if you want to save outside the CWD.

It is important to note that the training process may take some time, depending on the complexity of your agents and will also require your feedback on each iteration.
Once the training is complete, your agents will be equipped with enhanced capabilities and knowledge, ready to tackle complex tasks and provide more consistent and valuable insights.
Remember to regularly update and retrain your agents to ensure they stay up-to-date with the latest information and advancements in the field.

Was this page helpful?

YesNo

[Collaboration

Previous](/en/concepts/collaboration)[Memory

Next](/en/concepts/memory)

⌘I