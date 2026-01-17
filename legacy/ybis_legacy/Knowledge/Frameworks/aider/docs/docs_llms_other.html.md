# Other LLMs

Aider uses the [litellm](https://docs.litellm.ai/docs/providers) package
to connect to hundreds of other models.
You can use `aider --model <model-name>` to use any supported model.

To explore the list of supported models you can run `aider --list-models <model-name>`
with a partial model name.
If the supplied name is not an exact match for a known model, aider will
return a list of possible matching models.
For example:

```
$ aider --list-models turbo

Aider v0.29.3-dev
Models which match "turbo":
- gpt-4-turbo-preview (openai/gpt-4-turbo-preview)
- gpt-4-turbo (openai/gpt-4-turbo)
- gpt-4-turbo-2024-04-09 (openai/gpt-4-turbo-2024-04-09)
- gpt-3.5-turbo (openai/gpt-3.5-turbo)
- ...
```

See the [model warnings](warnings.html)
section for information on warnings which will occur
when working with models that aider is not familiar with.

## LiteLLM

Aider uses the LiteLLM package to connect to LLM providers.
The [LiteLLM provider docs](https://docs.litellm.ai/docs/providers)
contain more detail on all the supported providers,
their models and any required environment variables.

## Other API key variables

Here are the API key environment variables that are supported
by litellm. See their docs for more info.

* ALEPH\_ALPHA\_API\_KEY
* ALEPHALPHA\_API\_KEY
* ANTHROPIC\_API\_KEY
* ANYSCALE\_API\_KEY
* ARK\_API\_KEY
* AZURE\_AI\_API\_KEY
* AZURE\_API\_KEY
* AZURE\_OPENAI\_API\_KEY
* BASETEN\_API\_KEY
* BYTEZ\_API\_KEY
* CEREBRAS\_API\_KEY
* CLARIFAI\_API\_KEY
* CLOUDFLARE\_API\_KEY
* CO\_API\_KEY
* CODESTRAL\_API\_KEY
* COHERE\_API\_KEY
* COMPACTIFAI\_API\_KEY
* DASHSCOPE\_API\_KEY
* DATABRICKS\_API\_KEY
* DEEPINFRA\_API\_KEY
* DEEPSEEK\_API\_KEY
* FEATHERLESS\_AI\_API\_KEY
* FIREWORKS\_AI\_API\_KEY
* FIREWORKS\_API\_KEY
* FIREWORKSAI\_API\_KEY
* GEMINI\_API\_KEY
* GOOGLE\_API\_KEY
* GROQ\_API\_KEY
* HUGGINGFACE\_API\_KEY
* INFINITY\_API\_KEY
* MARITALK\_API\_KEY
* MISTRAL\_API\_KEY
* MOONSHOT\_API\_KEY
* NEBIUS\_API\_KEY
* NLP\_CLOUD\_API\_KEY
* NOVITA\_API\_KEY
* NVIDIA\_NIM\_API\_KEY
* OLLAMA\_API\_KEY
* OPENAI\_API\_KEY
* OPENAI\_LIKE\_API\_KEY
* OPENROUTER\_API\_KEY
* OR\_API\_KEY
* OVHCLOUD\_API\_KEY
* PALM\_API\_KEY
* PERPLEXITYAI\_API\_KEY
* PREDIBASE\_API\_KEY
* PROVIDER\_API\_KEY
* REPLICATE\_API\_KEY
* SAMBANOVA\_API\_KEY
* TOGETHERAI\_API\_KEY
* USER\_API\_KEY
* VERCEL\_AI\_GATEWAY\_API\_KEY
* VOLCENGINE\_API\_KEY
* VOYAGE\_API\_KEY
* WANDB\_API\_KEY
* WATSONX\_API\_KEY
* WX\_API\_KEY
* XAI\_API\_KEY
* XINFERENCE\_API\_KEY