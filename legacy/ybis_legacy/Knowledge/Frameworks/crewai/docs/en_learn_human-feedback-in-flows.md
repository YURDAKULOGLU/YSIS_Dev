Human Feedback in Flows - CrewAI

[Skip to main content](#content-area)

[CrewAI home page![light logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)![dark logo](https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/crew_only_logo.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=439ca5dc63a1768cad7196005ff5636f)](/)

![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)

English

Search...

⌘KAsk AI

Search...

Navigation

Learn

Human Feedback in Flows

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

The `@human_feedback` decorator enables human-in-the-loop (HITL) workflows directly within CrewAI Flows. It allows you to pause flow execution, present output to a human for review, collect their feedback, and optionally route to different listeners based on the feedback outcome.
This is particularly valuable for:

* **Quality assurance**: Review AI-generated content before it’s used downstream
* **Decision gates**: Let humans make critical decisions in automated workflows
* **Approval workflows**: Implement approve/reject/revise patterns
* **Interactive refinement**: Collect feedback to improve outputs iteratively

## [​](#quick-start) Quick Start

Here’s the simplest way to add human feedback to a flow:

Code

Copy

Ask AI

```
from crewai.flow.flow import Flow, start, listen
from crewai.flow.human_feedback import human_feedback

class SimpleReviewFlow(Flow):
    @start()
    @human_feedback(message="Please review this content:")
    def generate_content(self):
        return "This is AI-generated content that needs review."

    @listen(generate_content)
    def process_feedback(self, result):
        print(f"Content: {result.output}")
        print(f"Human said: {result.feedback}")

flow = SimpleReviewFlow()
flow.kickoff()
```

When this flow runs, it will:

1. Execute `generate_content` and return the string
2. Display the output to the user with the request message
3. Wait for the user to type feedback (or press Enter to skip)
4. Pass a `HumanFeedbackResult` object to `process_feedback`

## [​](#the-@human_feedback-decorator) The @human\_feedback Decorator

### [​](#parameters) Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `message` | `str` | Yes | The message shown to the human alongside the method output |
| `emit` | `Sequence[str]` | No | List of possible outcomes. Feedback is collapsed to one of these, which triggers `@listen` decorators |
| `llm` | `str | BaseLLM` | When `emit` specified | LLM used to interpret feedback and map to an outcome |
| `default_outcome` | `str` | No | Outcome to use if no feedback provided. Must be in `emit` |
| `metadata` | `dict` | No | Additional data for enterprise integrations |
| `provider` | `HumanFeedbackProvider` | No | Custom provider for async/non-blocking feedback. See [Async Human Feedback](#async-human-feedback-non-blocking) |

### [​](#basic-usage-no-routing) Basic Usage (No Routing)

When you don’t specify `emit`, the decorator simply collects feedback and passes a `HumanFeedbackResult` to the next listener:

Code

Copy

Ask AI

```
@start()
@human_feedback(message="What do you think of this analysis?")
def analyze_data(self):
    return "Analysis results: Revenue up 15%, costs down 8%"

@listen(analyze_data)
def handle_feedback(self, result):
    # result is a HumanFeedbackResult
    print(f"Analysis: {result.output}")
    print(f"Feedback: {result.feedback}")
```

### [​](#routing-with-emit) Routing with emit

When you specify `emit`, the decorator becomes a router. The human’s free-form feedback is interpreted by an LLM and collapsed into one of the specified outcomes:

Code

Copy

Ask AI

```
@start()
@human_feedback(
    message="Do you approve this content for publication?",
    emit=["approved", "rejected", "needs_revision"],
    llm="gpt-4o-mini",
    default_outcome="needs_revision",
)
def review_content(self):
    return "Draft blog post content here..."

@listen("approved")
def publish(self, result):
    print(f"Publishing! User said: {result.feedback}")

@listen("rejected")
def discard(self, result):
    print(f"Discarding. Reason: {result.feedback}")

@listen("needs_revision")
def revise(self, result):
    print(f"Revising based on: {result.feedback}")
```

The LLM uses structured outputs (function calling) when available to guarantee the response is one of your specified outcomes. This makes routing reliable and predictable.

## [​](#humanfeedbackresult) HumanFeedbackResult

The `HumanFeedbackResult` dataclass contains all information about a human feedback interaction:

Code

Copy

Ask AI

```
from crewai.flow.human_feedback import HumanFeedbackResult

@dataclass
class HumanFeedbackResult:
    output: Any              # The original method output shown to the human
    feedback: str            # The raw feedback text from the human
    outcome: str | None      # The collapsed outcome (if emit was specified)
    timestamp: datetime      # When the feedback was received
    method_name: str         # Name of the decorated method
    metadata: dict           # Any metadata passed to the decorator
```

### [​](#accessing-in-listeners) Accessing in Listeners

When a listener is triggered by a `@human_feedback` method with `emit`, it receives the `HumanFeedbackResult`:

Code

Copy

Ask AI

```
@listen("approved")
def on_approval(self, result: HumanFeedbackResult):
    print(f"Original output: {result.output}")
    print(f"User feedback: {result.feedback}")
    print(f"Outcome: {result.outcome}")  # "approved"
    print(f"Received at: {result.timestamp}")
```

## [​](#accessing-feedback-history) Accessing Feedback History

The `Flow` class provides two attributes for accessing human feedback:

### [​](#last_human_feedback) last\_human\_feedback

Returns the most recent `HumanFeedbackResult`:

Code

Copy

Ask AI

```
@listen(some_method)
def check_feedback(self):
    if self.last_human_feedback:
        print(f"Last feedback: {self.last_human_feedback.feedback}")
```

### [​](#human_feedback_history) human\_feedback\_history

A list of all `HumanFeedbackResult` objects collected during the flow:

Code

Copy

Ask AI

```
@listen(final_step)
def summarize(self):
    print(f"Total feedback collected: {len(self.human_feedback_history)}")
    for i, fb in enumerate(self.human_feedback_history):
        print(f"{i+1}. {fb.method_name}: {fb.outcome or 'no routing'}")
```

Each `HumanFeedbackResult` is appended to `human_feedback_history`, so multiple feedback steps won’t overwrite each other. Use this list to access all feedback collected during the flow.

## [​](#complete-example:-content-approval-workflow) Complete Example: Content Approval Workflow

Here’s a full example implementing a content review and approval workflow:

Code

Output

Copy

Ask AI

```
from crewai.flow.flow import Flow, start, listen
from crewai.flow.human_feedback import human_feedback, HumanFeedbackResult
from pydantic import BaseModel


class ContentState(BaseModel):
    topic: str = ""
    draft: str = ""
    final_content: str = ""
    revision_count: int = 0


class ContentApprovalFlow(Flow[ContentState]):
    """A flow that generates content and gets human approval."""

    @start()
    def get_topic(self):
        self.state.topic = input("What topic should I write about? ")
        return self.state.topic

    @listen(get_topic)
    def generate_draft(self, topic):
        # In real use, this would call an LLM
        self.state.draft = f"# {topic}\n\nThis is a draft about {topic}..."
        return self.state.draft

    @listen(generate_draft)
    @human_feedback(
        message="Please review this draft. Reply 'approved', 'rejected', or provide revision feedback:",
        emit=["approved", "rejected", "needs_revision"],
        llm="gpt-4o-mini",
        default_outcome="needs_revision",
    )
    def review_draft(self, draft):
        return draft

    @listen("approved")
    def publish_content(self, result: HumanFeedbackResult):
        self.state.final_content = result.output
        print("\n✅ Content approved and published!")
        print(f"Reviewer comment: {result.feedback}")
        return "published"

    @listen("rejected")
    def handle_rejection(self, result: HumanFeedbackResult):
        print("\n❌ Content rejected")
        print(f"Reason: {result.feedback}")
        return "rejected"

    @listen("needs_revision")
    def revise_content(self, result: HumanFeedbackResult):
        self.state.revision_count += 1
        print(f"\n📝 Revision #{self.state.revision_count} requested")
        print(f"Feedback: {result.feedback}")

        # In a real flow, you might loop back to generate_draft
        # For this example, we just acknowledge
        return "revision_requested"


# Run the flow
flow = ContentApprovalFlow()
result = flow.kickoff()
print(f"\nFlow completed. Revisions requested: {flow.state.revision_count}")
```

## [​](#combining-with-other-decorators) Combining with Other Decorators

The `@human_feedback` decorator works with other flow decorators. Place it as the innermost decorator (closest to the function):

Code

Copy

Ask AI

```
# Correct: @human_feedback is innermost (closest to the function)
@start()
@human_feedback(message="Review this:")
def my_start_method(self):
    return "content"

@listen(other_method)
@human_feedback(message="Review this too:")
def my_listener(self, data):
    return f"processed: {data}"
```

Place `@human_feedback` as the innermost decorator (last/closest to the function) so it wraps the method directly and can capture the return value before passing to the flow system.

## [​](#best-practices) Best Practices

### [​](#1-write-clear-request-messages) 1. Write Clear Request Messages

The `request` parameter is what the human sees. Make it actionable:

Code

Copy

Ask AI

```
# ✅ Good - clear and actionable
@human_feedback(message="Does this summary accurately capture the key points? Reply 'yes' or explain what's missing:")

# ❌ Bad - vague
@human_feedback(message="Review this:")
```

### [​](#2-choose-meaningful-outcomes) 2. Choose Meaningful Outcomes

When using `emit`, pick outcomes that map naturally to human responses:

Code

Copy

Ask AI

```
# ✅ Good - natural language outcomes
emit=["approved", "rejected", "needs_more_detail"]

# ❌ Bad - technical or unclear
emit=["state_1", "state_2", "state_3"]
```

### [​](#3-always-provide-a-default-outcome) 3. Always Provide a Default Outcome

Use `default_outcome` to handle cases where users press Enter without typing:

Code

Copy

Ask AI

```
@human_feedback(
    message="Approve? (press Enter to request revision)",
    emit=["approved", "needs_revision"],
    llm="gpt-4o-mini",
    default_outcome="needs_revision",  # Safe default
)
```

### [​](#4-use-feedback-history-for-audit-trails) 4. Use Feedback History for Audit Trails

Access `human_feedback_history` to create audit logs:

Code

Copy

Ask AI

```
@listen(final_step)
def create_audit_log(self):
    log = []
    for fb in self.human_feedback_history:
        log.append({
            "step": fb.method_name,
            "outcome": fb.outcome,
            "feedback": fb.feedback,
            "timestamp": fb.timestamp.isoformat(),
        })
    return log
```

### [​](#5-handle-both-routed-and-non-routed-feedback) 5. Handle Both Routed and Non-Routed Feedback

When designing flows, consider whether you need routing:

| Scenario | Use |
| --- | --- |
| Simple review, just need the feedback text | No `emit` |
| Need to branch to different paths based on response | Use `emit` |
| Approval gates with approve/reject/revise | Use `emit` |
| Collecting comments for logging only | No `emit` |

## [​](#async-human-feedback-non-blocking) Async Human Feedback (Non-Blocking)

By default, `@human_feedback` blocks execution waiting for console input. For production applications, you may need **async/non-blocking** feedback that integrates with external systems like Slack, email, webhooks, or APIs.

### [​](#the-provider-abstraction) The Provider Abstraction

Use the `provider` parameter to specify a custom feedback collection strategy:

Code

Copy

Ask AI

```
from crewai.flow import Flow, start, human_feedback, HumanFeedbackProvider, HumanFeedbackPending, PendingFeedbackContext

class WebhookProvider(HumanFeedbackProvider):
    """Provider that pauses flow and waits for webhook callback."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def request_feedback(self, context: PendingFeedbackContext, flow: Flow) -> str:
        # Notify external system (e.g., send Slack message, create ticket)
        self.send_notification(context)

        # Pause execution - framework handles persistence automatically
        raise HumanFeedbackPending(
            context=context,
            callback_info={"webhook_url": f"{self.webhook_url}/{context.flow_id}"}
        )

class ReviewFlow(Flow):
    @start()
    @human_feedback(
        message="Review this content:",
        emit=["approved", "rejected"],
        llm="gpt-4o-mini",
        provider=WebhookProvider("https://myapp.com/api"),
    )
    def generate_content(self):
        return "AI-generated content..."

    @listen("approved")
    def publish(self, result):
        return "Published!"
```

The flow framework **automatically persists state** when `HumanFeedbackPending` is raised. Your provider only needs to notify the external system and raise the exception—no manual persistence calls required.

### [​](#handling-paused-flows) Handling Paused Flows

When using an async provider, `kickoff()` returns a `HumanFeedbackPending` object instead of raising an exception:

Code

Copy

Ask AI

```
flow = ReviewFlow()
result = flow.kickoff()

if isinstance(result, HumanFeedbackPending):
    # Flow is paused, state is automatically persisted
    print(f"Waiting for feedback at: {result.callback_info['webhook_url']}")
    print(f"Flow ID: {result.context.flow_id}")
else:
    # Normal completion
    print(f"Flow completed: {result}")
```

### [​](#resuming-a-paused-flow) Resuming a Paused Flow

When feedback arrives (e.g., via webhook), resume the flow:

Code

Copy

Ask AI

```
# Sync handler:
def handle_feedback_webhook(flow_id: str, feedback: str):
    flow = ReviewFlow.from_pending(flow_id)
    result = flow.resume(feedback)
    return result

# Async handler (FastAPI, aiohttp, etc.):
async def handle_feedback_webhook(flow_id: str, feedback: str):
    flow = ReviewFlow.from_pending(flow_id)
    result = await flow.resume_async(feedback)
    return result
```

### [​](#key-types) Key Types

| Type | Description |
| --- | --- |
| `HumanFeedbackProvider` | Protocol for custom feedback providers |
| `PendingFeedbackContext` | Contains all info needed to resume a paused flow |
| `HumanFeedbackPending` | Returned by `kickoff()` when flow is paused for feedback |
| `ConsoleProvider` | Default blocking console input provider |

### [​](#pendingfeedbackcontext) PendingFeedbackContext

The context contains everything needed to resume:

Code

Copy

Ask AI

```
@dataclass
class PendingFeedbackContext:
    flow_id: str           # Unique identifier for this flow execution
    flow_class: str        # Fully qualified class name
    method_name: str       # Method that triggered feedback
    method_output: Any     # Output shown to the human
    message: str           # The request message
    emit: list[str] | None # Possible outcomes for routing
    default_outcome: str | None
    metadata: dict         # Custom metadata
    llm: str | None        # LLM for outcome collapsing
    requested_at: datetime
```

### [​](#complete-async-flow-example) Complete Async Flow Example

Code

Copy

Ask AI

```
from crewai.flow import (
    Flow, start, listen, human_feedback,
    HumanFeedbackProvider, HumanFeedbackPending, PendingFeedbackContext
)

class SlackNotificationProvider(HumanFeedbackProvider):
    """Provider that sends Slack notifications and pauses for async feedback."""

    def __init__(self, channel: str):
        self.channel = channel

    def request_feedback(self, context: PendingFeedbackContext, flow: Flow) -> str:
        # Send Slack notification (implement your own)
        slack_thread_id = self.post_to_slack(
            channel=self.channel,
            message=f"Review needed:\n\n{context.method_output}\n\n{context.message}",
        )

        # Pause execution - framework handles persistence automatically
        raise HumanFeedbackPending(
            context=context,
            callback_info={
                "slack_channel": self.channel,
                "thread_id": slack_thread_id,
            }
        )

class ContentPipeline(Flow):
    @start()
    @human_feedback(
        message="Approve this content for publication?",
        emit=["approved", "rejected", "needs_revision"],
        llm="gpt-4o-mini",
        default_outcome="needs_revision",
        provider=SlackNotificationProvider("#content-reviews"),
    )
    def generate_content(self):
        return "AI-generated blog post content..."

    @listen("approved")
    def publish(self, result):
        print(f"Publishing! Reviewer said: {result.feedback}")
        return {"status": "published"}

    @listen("rejected")
    def archive(self, result):
        print(f"Archived. Reason: {result.feedback}")
        return {"status": "archived"}

    @listen("needs_revision")
    def queue_revision(self, result):
        print(f"Queued for revision: {result.feedback}")
        return {"status": "revision_needed"}


# Starting the flow (will pause and wait for Slack response)
def start_content_pipeline():
    flow = ContentPipeline()
    result = flow.kickoff()

    if isinstance(result, HumanFeedbackPending):
        return {"status": "pending", "flow_id": result.context.flow_id}

    return result


# Resuming when Slack webhook fires (sync handler)
def on_slack_feedback(flow_id: str, slack_message: str):
    flow = ContentPipeline.from_pending(flow_id)
    result = flow.resume(slack_message)
    return result


# If your handler is async (FastAPI, aiohttp, Slack Bolt async, etc.)
async def on_slack_feedback_async(flow_id: str, slack_message: str):
    flow = ContentPipeline.from_pending(flow_id)
    result = await flow.resume_async(slack_message)
    return result
```

If you’re using an async web framework (FastAPI, aiohttp, Slack Bolt async mode), use `await flow.resume_async()` instead of `flow.resume()`. Calling `resume()` from within a running event loop will raise a `RuntimeError`.

### [​](#best-practices-for-async-feedback) Best Practices for Async Feedback

1. **Check the return type**: `kickoff()` returns `HumanFeedbackPending` when paused—no try/except needed
2. **Use the right resume method**: Use `resume()` in sync code, `await resume_async()` in async code
3. **Store callback info**: Use `callback_info` to store webhook URLs, ticket IDs, etc.
4. **Implement idempotency**: Your resume handler should be idempotent for safety
5. **Automatic persistence**: State is automatically saved when `HumanFeedbackPending` is raised and uses `SQLiteFlowPersistence` by default
6. **Custom persistence**: Pass a custom persistence instance to `from_pending()` if needed

## [​](#related-documentation) Related Documentation

* [Flows Overview](/en/concepts/flows) - Learn about CrewAI Flows
* [Flow State Management](/en/guides/flows/mastering-flow-state) - Managing state in flows
* [Flow Persistence](/en/concepts/flows#persistence) - Persisting flow state
* [Routing with @router](/en/concepts/flows#router) - More about conditional routing
* [Human Input on Execution](/en/learn/human-input-on-execution) - Task-level human input

Was this page helpful?

YesNo

[Human-in-the-Loop (HITL) Workflows

Previous](/en/learn/human-in-the-loop)[Kickoff Crew Asynchronously

Next](/en/learn/kickoff-async)

⌘I