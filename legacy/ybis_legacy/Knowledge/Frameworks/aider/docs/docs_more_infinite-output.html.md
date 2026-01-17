# Infinite output

LLM providers limit how much output a model can generate from a single request.
This is usually called the output token limit.

Aider is able to work around this limit with models that support
“prefilling” the assistant response.
When you use aider with a model that supports prefill, you will see
“infinite output” noted in the announcement lines displayed at launch:

```
Aider v0.58.0
Main model: claude-3-5-sonnet-20240620 with diff edit format, prompt cache, infinite output
```

Models that support prefill can be primed to think they started their response
with a specific piece of text.
You can put words in their mouth, and they will continue generating
text from that point forward.

When aider is collecting code edits from a model and
it hits the output token limit,
aider simply initiates another LLM request with the partial
response prefilled.
This prompts the model to continue where it left off,
generating more of the desired response.
This prefilling of the partially completed response can be repeated,
allowing for very long outputs.
Joining the text across these output limit boundaries
requires some heuristics, but is typically fairly reliable.

Aider supports “infinite output” for models that support “prefill”,
such as:

* anthropic.claude-3-5-haiku-20241022-v1:0
* anthropic.claude-3-5-sonnet-20241022-v2:0
* anthropic.claude-3-7-sonnet-20240620-v1:0
* anthropic.claude-3-7-sonnet-20250219-v1:0
* anthropic.claude-haiku-4-5-20251001-v1:0
* anthropic.claude-haiku-4-5@20251001
* anthropic.claude-opus-4-1-20250805-v1:0
* anthropic.claude-opus-4-20250514-v1:0
* anthropic.claude-opus-4-5-20251101-v1:0
* anthropic.claude-sonnet-4-20250514-v1:0
* anthropic.claude-sonnet-4-5-20250929-v1:0
* apac.anthropic.claude-3-5-sonnet-20241022-v2:0
* apac.anthropic.claude-haiku-4-5-20251001-v1:0
* apac.anthropic.claude-sonnet-4-20250514-v1:0
* au.anthropic.claude-haiku-4-5-20251001-v1:0
* au.anthropic.claude-sonnet-4-5-20250929-v1:0
* azure\_ai/claude-haiku-4-5
* azure\_ai/claude-opus-4-1
* azure\_ai/claude-sonnet-4-5
* azure\_ai/deepseek-v3.2
* azure\_ai/deepseek-v3.2-speciale
* azure\_ai/mistral-medium-2505
* bedrock/us-gov-east-1/claude-sonnet-4-5-20250929-v1:0
* bedrock/us-gov-west-1/anthropic.claude-3-7-sonnet-20250219-v1:0
* bedrock/us-gov-west-1/claude-sonnet-4-5-20250929-v1:0
* bedrock/us.anthropic.claude-3-5-haiku-20241022-v1:0
* claude-3-5-haiku-20241022
* claude-3-5-haiku-latest
* claude-3-5-sonnet-20240620
* claude-3-5-sonnet-20241022
* claude-3-5-sonnet-latest
* claude-3-7-sonnet-20250219
* claude-3-7-sonnet-latest
* claude-3-haiku-20240307
* claude-3-opus-20240229
* claude-3-opus-latest
* claude-4-opus-20250514
* claude-4-sonnet-20250514
* claude-haiku-4-5
* claude-haiku-4-5-20251001
* claude-opus-4-1
* claude-opus-4-1-20250805
* claude-opus-4-20250514
* claude-opus-4-5
* claude-opus-4-5-20251101
* claude-sonnet-4-20250514
* claude-sonnet-4-5
* claude-sonnet-4-5-20250929
* claude-sonnet-4-5-20250929-v1:0
* codestral/codestral-2405
* codestral/codestral-latest
* databricks/databricks-claude-3-7-sonnet
* databricks/databricks-claude-haiku-4-5
* databricks/databricks-claude-opus-4
* databricks/databricks-claude-opus-4-1
* databricks/databricks-claude-opus-4-5
* databricks/databricks-claude-sonnet-4
* databricks/databricks-claude-sonnet-4-1
* databricks/databricks-claude-sonnet-4-5
* deepseek/deepseek-chat
* deepseek/deepseek-coder
* deepseek/deepseek-r1
* deepseek/deepseek-reasoner
* deepseek/deepseek-v3
* deepseek/deepseek-v3.2
* eu.anthropic.claude-3-5-haiku-20241022-v1:0
* eu.anthropic.claude-3-5-sonnet-20241022-v2:0
* eu.anthropic.claude-3-7-sonnet-20250219-v1:0
* eu.anthropic.claude-haiku-4-5-20251001-v1:0
* eu.anthropic.claude-opus-4-1-20250805-v1:0
* eu.anthropic.claude-opus-4-20250514-v1:0
* eu.anthropic.claude-opus-4-5-20251101-v1:0
* eu.anthropic.claude-sonnet-4-20250514-v1:0
* eu.anthropic.claude-sonnet-4-5-20250929-v1:0
* global.anthropic.claude-haiku-4-5-20251001-v1:0
* global.anthropic.claude-opus-4-5-20251101-v1:0
* global.anthropic.claude-sonnet-4-20250514-v1:0
* global.anthropic.claude-sonnet-4-5-20250929-v1:0
* jp.anthropic.claude-haiku-4-5-20251001-v1:0
* jp.anthropic.claude-sonnet-4-5-20250929-v1:0
* mistral/codestral-2405
* mistral/codestral-2508
* mistral/codestral-latest
* mistral/codestral-mamba-latest
* mistral/devstral-2512
* mistral/devstral-medium-2507
* mistral/devstral-small-2505
* mistral/devstral-small-2507
* mistral/labs-devstral-small-2512
* mistral/magistral-medium-2506
* mistral/magistral-medium-2509
* mistral/magistral-medium-latest
* mistral/magistral-small-2506
* mistral/magistral-small-latest
* mistral/mistral-large-2402
* mistral/mistral-large-2407
* mistral/mistral-large-2411
* mistral/mistral-large-3
* mistral/mistral-large-latest
* mistral/mistral-medium
* mistral/mistral-medium-2312
* mistral/mistral-medium-2505
* mistral/mistral-medium-latest
* mistral/mistral-small
* mistral/mistral-small-latest
* mistral/mistral-tiny
* mistral/open-codestral-mamba
* mistral/open-mistral-7b
* mistral/open-mistral-nemo
* mistral/open-mistral-nemo-2407
* mistral/open-mixtral-8x22b
* mistral/open-mixtral-8x7b
* mistral/pixtral-12b-2409
* mistral/pixtral-large-2411
* mistral/pixtral-large-latest
* openrouter/anthropic/claude-3.5-sonnet
* openrouter/anthropic/claude-3.7-sonnet
* openrouter/anthropic/claude-haiku-4.5
* openrouter/anthropic/claude-opus-4
* openrouter/anthropic/claude-opus-4.1
* openrouter/anthropic/claude-opus-4.5
* openrouter/anthropic/claude-sonnet-4
* openrouter/anthropic/claude-sonnet-4.5
* openrouter/deepseek/deepseek-chat-v3.1
* openrouter/deepseek/deepseek-r1
* openrouter/deepseek/deepseek-r1-0528
* openrouter/deepseek/deepseek-v3.2
* openrouter/deepseek/deepseek-v3.2-exp
* us.anthropic.claude-3-5-haiku-20241022-v1:0
* us.anthropic.claude-3-5-sonnet-20241022-v2:0
* us.anthropic.claude-3-7-sonnet-20250219-v1:0
* us.anthropic.claude-haiku-4-5-20251001-v1:0
* us.anthropic.claude-opus-4-1-20250805-v1:0
* us.anthropic.claude-opus-4-20250514-v1:0
* us.anthropic.claude-opus-4-5-20251101-v1:0
* us.anthropic.claude-sonnet-4-20250514-v1:0
* us.anthropic.claude-sonnet-4-5-20250929-v1:0
* vertex\_ai/claude-3-5-haiku
* vertex\_ai/claude-3-5-haiku@20241022
* vertex\_ai/claude-3-5-sonnet
* vertex\_ai/claude-3-5-sonnet-v2
* vertex\_ai/claude-3-5-sonnet-v2@20241022
* vertex\_ai/claude-3-5-sonnet@20240620
* vertex\_ai/claude-3-7-sonnet@20250219
* vertex\_ai/claude-3-haiku
* vertex\_ai/claude-3-haiku@20240307
* vertex\_ai/claude-3-opus
* vertex\_ai/claude-3-opus@20240229
* vertex\_ai/claude-3-sonnet
* vertex\_ai/claude-3-sonnet@20240229
* vertex\_ai/claude-haiku-4-5@20251001
* vertex\_ai/claude-opus-4
* vertex\_ai/claude-opus-4-1
* vertex\_ai/claude-opus-4-1@20250805
* vertex\_ai/claude-opus-4-5
* vertex\_ai/claude-opus-4-5@20251101
* vertex\_ai/claude-opus-4@20250514
* vertex\_ai/claude-sonnet-4
* vertex\_ai/claude-sonnet-4-5
* vertex\_ai/claude-sonnet-4-5@20250929
* vertex\_ai/claude-sonnet-4@20250514
* vertex\_ai/deepseek-ai/deepseek-r1-0528-maas
* vertex\_ai/deepseek-ai/deepseek-v3.1-maas
* vertex\_ai/deepseek-ai/deepseek-v3.2-maas