Welcome to Outlines! - Outlines






[Skip to content](#_1)

# 

![](assets/images/logo-light-mode.svg#only-light)
![](assets/images/logo-dark-mode.svg#only-dark)

LLMs are powerful but their outputs are unpredictable. Most solutions attempt to fix bad outputs after generation using parsing, regex, or fragile code that breaks easily.

Outlines guarantees structured outputs during generation — directly from any LLM.

* **Works with any model** - Same code runs across OpenAI, Ollama, vLLM, and more
* **Simple integration** - Just pass your desired output type: `model(prompt, output_type)`
* **Guaranteed valid structure** - No more parsing headaches or broken JSON
* **Provider independence** - Switch models without changing code
* **Rich structure definition** - Use Json Schema, regular expressions or context-free grammars

[Get Started](guide/getting_started)
[View Examples](examples/)
[API Reference](api_reference/)
[GitHub](https://github.com/dottxt-ai/outlines)

## 🚀 Building the future of structured generation

We're working with select partners to develop new interfaces to structured generation.

Need XML, FHIR, custom schemas or grammars? Let's talk.

[Become a design partner](mailto:contact@dottxt.ai)

## See it in action

```
from pydantic import BaseModel
from typing import Literal
import outlines
import openai

class Customer(BaseModel):
    name: str
    urgency: Literal["high", "medium", "low"]
    issue: str

client = openai.OpenAI()
model = outlines.from_openai(client, "gpt-4o")

customer = model(
    "Alice needs help with login issues ASAP",
    Customer
)
# ✓ Always returns valid Customer object
# ✓ No parsing, no errors, no retries
```

## Quick install

```
pip install outlines
```

## Features

* **Reliable** - Guaranteed schema compliance -- always valid JSON.
* **Feature-rich** - Supports a large proportion of the JSON Schema spec, along with regex and context-free grammars.
* **Fast** - Microseconds of overhead vs seconds of retries. Compilation happens once, not every request.
* **Simple** - Outlines is a low-abstraction library. Write code the way you normally do with LLMs. No agent frameworks needed.

## Supported inference APIs, libraries & servers

* [vLLM](features/models/vllm/)
* [vLLM offline](features/models/vllm_offline/)
* [Transformers](features/models/transformers/)
* [llama.cpp](features/models/llamacpp/)
* [Ollama](features/models/ollama/)
* [MLX-LM](features/models/mlxlm/)
* [SgLang](features/models/sglang/)
* [TGI](features/models/tgi/)
* [OpenAI](features/models/openai/)
* [Anthropic](features/models/anthropic/)
* [Gemini](features/models/gemini/)
* [Dottxt](features/models/dottxt/)

## Who is using Outlines?

Hundreds of organisations and the main LLM serving frameworks ([vLLM](https://github.com/vllm-project/vllm), [TGI](https://github.com/huggingface/text-generation-inference), [LoRAX](https://github.com/predibase/lorax), [xinference](https://github.com/xorbitsai/inference), [SGLang](https://github.com/sgl-project/sglang/)) use Outlines. Prominent companies and organizations that use Outlines include:

![](../logos/amazon.png)

![](../logos/apple.png)

![](../logos/best_buy.png)

![](../logos/canoe.png)

![](../logos/cisco.png)

![](../logos/dassault_systems.png)

![](../logos/databricks.png)

![](../logos/datadog.png)

![](../logos/dbt_labs.png)

![](../assets/images/dottxt.png)

![](../logos/gladia.jpg)

![](../logos/harvard.png)

![](../logos/hf.png)

![](../logos/johns_hopkins.png)

![](../logos/meta.png)

![](../logos/mit.png)

![](../logos/mount_sinai.png)

![](../logos/nvidia.png)

![](../logos/nyu.png)

![](../logos/safran.png)

![](../logos/salesforce.png)

![](../logos/shopify.png)

![](../logos/smithsonian.png)

![](../logos/tinder.png)

![](../logos/upenn.png)

Organizations are included either because they use Outlines as a dependency in a public repository, or because of direct communication between members of the Outlines team and employees at these organizations.

Still not convinced, read [what people say about us](community/feedback/). And make sure to take a look at what the [community is building](community/examples/)!

## Outlines people

Outlines would not be what it is today without a community of dedicated developers:

[![](https://contrib.rocks/image?repo=dottxt-ai/outlines)](https://github.com/dottxt-ai/outlines/graphs/contributors)

## About .txt

Outlines is built with ❤️ by [.txt](https://dottxt.co).

.txt solves the critical problem of reliable structured output generation for large language models. Our [commercially-licensed libraries](https://docs.dottxt.co) ensure 100% compliance with JSON Schema, regular expressions and context-free grammars while adding only microseconds of latency. Unlike open-source alternatives, we offer superior reliability, performance, and enterprise support.

## Acknowledgements

[![Normal Computing logo](assets/images/normal_computing.jpg)](https://www.normalcomputing.ai)

Outlines was originally developed at [@NormalComputing](https://twitter.com/NormalComputing) by [@remilouf](https://twitter.com/remilouf) and [@BrandonTWillard](https://twitter.com/BrandonTWillard). It is now maintained by [.txt](https://dottxt.co).

2025-10-06




2023-11-12




GitHub