 Prompting | LlamaIndex Python Documentation
  [Skip to content](#_top)

# Prompting

Prompting LLMs is a fundamental unit of any LLM application. You can build an entire application entirely around prompting, or orchestrate with other modules (e.g. retrieval) to build RAG, agents, and more.

LlamaIndex supports LLM abstractions and simple-to-advanced prompt abstractions to make complex prompt workflows possible.

## LLM Integrations

[Section titled “LLM Integrations”](#llm-integrations)

LlamaIndex supports 40+ LLM integrations, from proprietary model providers like OpenAI, Anthropic to open-source models/model providers like Mistral, Ollama, Replicate. It provides all the tools to standardize interface around common LLM usage patterns, including but not limited to async, streaming, function calling.

Here’s the [full module guide for LLMs](/python/framework/module_guides/models/llms).

## Prompts

[Section titled “Prompts”](#prompts)

LlamaIndex has robust prompt abstractions that capture all the common interaction patterns with LLMs.

Here’s the [full module guide for prompts](/python/framework/module_guides/models/prompts).

### Table Stakes

[Section titled “Table Stakes”](#table-stakes)

* [Text Completion Prompts](/python/examples/customization/prompts/completion_prompts)
* [Chat Prompts](/python/examples/customization/prompts/chat_prompts)

### Advanced

[Section titled “Advanced”](#advanced)

* [Variable Mappings, Functions, Partials](/python/examples/prompts/advanced_prompts)
* [RichPromptTemplate Features](/python/examples/prompts/rich_prompt_template_features)

## Prompt Chains and Pipelines

[Section titled “Prompt Chains and Pipelines”](#prompt-chains-and-pipelines)

LlamaIndex has robust abstractions for creating sequential prompt chains, as well as general DAGs to orchestrate prompts with any other component. This allows you to build complex workflows, including RAG with multi-hop query understanding layers, as well as agents.

These pipelines are integrated with [observability partners](/python/framework/module_guides/observability) out of the box.