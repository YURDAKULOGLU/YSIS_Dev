Google Gemini - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#google-gemini-integration-guide)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Google Gemini Integration Guide

This guide covers setting up and using Google's Gemini models with Ragas for evaluation.

## Overview

Ragas supports Google Gemini models with automatic adapter selection. The framework works with both the new `google-genai` SDK (recommended) and the legacy `google-generativeai` SDK.

## Setup

### Prerequisites

* Google API Key with Gemini API access
* Python 3.8+
* Ragas installed

### Installation

Install required dependencies:

```
# Recommended: New Google GenAI SDK
pip install ragas google-genai

# Legacy (deprecated, support ends Aug 2025)
pip install ragas google-generativeai
```

## Configuration

### Option 1: Using New Google GenAI SDK (Recommended)

The new `google-genai` SDK is the recommended approach:

```
import os
from google import genai
from ragas.llms import llm_factory

# Create client with API key
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# Create LLM - adapter is auto-detected for google provider
llm = llm_factory(
    "gemini-2.0-flash",
    provider="google",
    client=client
)
```

### Option 2: Using Legacy SDK (Deprecated)

The old `google-generativeai` SDK still works but is deprecated (support ends Aug 2025):

```
import os
import google.generativeai as genai
from ragas.llms import llm_factory

# Configure with your API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Create client
client = genai.GenerativeModel("gemini-2.0-flash")

# Create LLM
llm = llm_factory(
    "gemini-2.0-flash",
    provider="google",
    client=client
)
```

### Option 3: Using LiteLLM Proxy (Advanced)

For advanced use cases where you need LiteLLM's proxy capabilities, set up the LiteLLM proxy server first, then use:

```
import os
from openai import OpenAI
from ragas.llms import llm_factory

# Requires running: litellm --model gemini-2.0-flash
client = OpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"  # LiteLLM proxy endpoint
)

# Create LLM with explicit adapter selection
llm = llm_factory("gemini-2.0-flash", client=client, adapter="litellm")
```

## Supported Models

Ragas works with all Gemini models:

* **Latest**: `gemini-2.0-flash` (recommended)
* **1.5 Series**: `gemini-1.5-pro`, `gemini-1.5-flash`
* **1.0 Series**: `gemini-1.0-pro`

For the latest models and pricing, see [Google AI Studio](https://aistudio.google.com/apikey).

## Embeddings Configuration

Ragas metrics fall into two categories:

1. **LLM-only metrics** (don't require embeddings):
2. ContextPrecision
3. ContextRecall
4. Faithfulness
5. AspectCritic
6. **Embedding-dependent metrics** (require embeddings):
7. AnswerCorrectness
8. AnswerRelevancy
9. AnswerSimilarity
10. SemanticSimilarity
11. ContextEntityRecall

### Automatic Provider Matching

When using Ragas with Gemini, the embedding provider is **automatically matched** to your LLM provider. If you provide a Gemini LLM, Ragas will default to using Google embeddings. **No OpenAI API key is needed.**

### Option 1: Default Embeddings (Recommended)

Let Ragas automatically select the right embeddings based on your LLM:

```
import os
from datasets import Dataset
from google import genai
from ragas import evaluate
from ragas.llms import llm_factory
from ragas.metrics import (
    AnswerCorrectness,
    ContextPrecision,
    ContextRecall,
    Faithfulness
)

# Initialize Gemini client (new SDK)
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)

# Create sample evaluation data
data = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is the capital of France."],
    "contexts": [["France is a country in Western Europe. Paris is its capital."]],
    "ground_truth": ["Paris"]
}

dataset = Dataset.from_dict(data)

# Define metrics - embeddings are auto-configured for Google
metrics = [
    ContextPrecision(llm=llm),
    ContextRecall(llm=llm),
    Faithfulness(llm=llm),
    AnswerCorrectness(llm=llm)  # Uses Google embeddings automatically
]

# Run evaluation
results = evaluate(dataset, metrics=metrics)
print(results)
```

### Option 2: Explicit Embeddings

For explicit control over embeddings, you can create them separately. Google embeddings work with multiple configuration options:

```
import os
from google import genai
from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings
from ragas.embeddings.base import embedding_factory
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import AnswerCorrectness, ContextPrecision, ContextRecall, Faithfulness

# Initialize Gemini client (new SDK)
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)

# Initialize Google embeddings (multiple options):

# Option A: Using the same client (recommended for new SDK)
embeddings = GoogleEmbeddings(client=client, model="gemini-embedding-001")

# Option B: Using embedding factory
embeddings = embedding_factory("google", model="gemini-embedding-001")

# Option C: Auto-import (creates client automatically)
embeddings = GoogleEmbeddings(model="gemini-embedding-001")

# Create sample evaluation data
data = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is the capital of France."],
    "contexts": [["France is a country in Western Europe. Paris is its capital."]],
    "ground_truth": ["Paris"]
}

dataset = Dataset.from_dict(data)

# Define metrics with explicit embeddings
metrics = [
    ContextPrecision(llm=llm),
    ContextRecall(llm=llm),
    Faithfulness(llm=llm),
    AnswerCorrectness(llm=llm, embeddings=embeddings)
]

# Run evaluation
results = evaluate(dataset, metrics=metrics)
print(results)
```

## Example: Complete Evaluation

Here's a complete example evaluating a RAG application with Gemini (using automatic embedding provider matching):

```
import os
from datasets import Dataset
from google import genai
from ragas import evaluate
from ragas.llms import llm_factory
from ragas.metrics import (
    AnswerCorrectness,
    ContextPrecision,
    ContextRecall,
    Faithfulness
)

# Initialize Gemini client (new SDK)
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)

# Create sample evaluation data
data = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is the capital of France."],
    "contexts": [["France is a country in Western Europe. Paris is its capital."]],
    "ground_truth": ["Paris"]
}

dataset = Dataset.from_dict(data)

# Define metrics - embeddings automatically use Google provider
metrics = [
    ContextPrecision(llm=llm),
    ContextRecall(llm=llm),
    Faithfulness(llm=llm),
    AnswerCorrectness(llm=llm)
]

# Run evaluation
results = evaluate(dataset, metrics=metrics)
print(results)
```

## Performance Considerations

### Model Selection

* **gemini-2.0-flash**: Best for speed and efficiency
* **gemini-1.5-pro**: Better reasoning for complex evaluations
* **gemini-1.5-flash**: Good balance of speed and cost

### Cost Optimization

Gemini models are cost-effective. For large-scale evaluations:

1. Use `gemini-2.0-flash` for most metrics
2. Consider batch processing for multiple evaluations
3. Cache prompts when possible (Gemini supports prompt caching)

### Async Support

For high-throughput evaluations, use async operations:

```
import os
from google import genai
from ragas.llms import llm_factory

# Create client (new SDK)
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)

# Use in async evaluation
# response = await llm.agenerate(prompt, ResponseModel)
```

## Adapter Selection

Ragas automatically selects the appropriate adapter based on your setup:

```
# Auto-detection happens automatically
# For Gemini: uses LiteLLM adapter
# For other providers: uses Instructor adapter

# Explicit selection (if needed)
llm = llm_factory(
    "gemini-2.0-flash",
    client=client,
    adapter="litellm"  # Explicit adapter selection
)

# Check auto-detected adapter
from ragas.llms.adapters import auto_detect_adapter
adapter_name = auto_detect_adapter(client, "google")
print(f"Using adapter: {adapter_name}")  # Output: Using adapter: litellm
```

## Troubleshooting

### API Key Issues

```
# Make sure your API key is set
import os
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY environment variable not set")
```

### Known Issue: Instructor Safety Settings (New SDK)

There is a known upstream issue with the instructor library where it sends invalid safety settings to the Gemini API when using the new `google-genai` SDK. This may cause errors like:

```
Invalid value at 'safety_settings[5].category'... "HARM_CATEGORY_JAILBREAK"
```

**Workarounds:**

1. Use the OpenAI-compatible endpoint (recommended for now):

   ```
   from openai import OpenAI
   client = OpenAI(
       api_key=os.environ.get("GOOGLE_API_KEY"),
       base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
   )
   llm = llm_factory("gemini-2.0-flash", provider="openai", client=client)
   ```
2. Track the upstream issue: [instructor#1658](https://github.com/567-labs/instructor/issues/1658)

Note: Embeddings work correctly with the new SDK - this issue only affects LLM generation.

### Rate Limits

Gemini has rate limits. For production use, the LLM adapter handles retries and timeouts automatically. If you need fine-grained control, ensure your client is properly configured with appropriate timeouts at the HTTP client level.

### Model Availability

If a model isn't available:

1. Check your region/quota in [Google Cloud Console](https://console.cloud.google.com)
2. Try a different model from the supported list
3. Verify your API key has access to the Generative AI API

## Migration from Other Providers

### From OpenAI

```
# Before: OpenAI-only
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
llm = llm_factory("gpt-4o", client=client)

# After: Gemini with new SDK
from google import genai
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)
```

### From Anthropic

```
# Before: Anthropic
from anthropic import Anthropic
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
llm = llm_factory("claude-3-sonnet", provider="anthropic", client=client)

# After: Gemini with new SDK
from google import genai
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)
```

### From Legacy google-generativeai SDK

```
# Before: Legacy SDK (deprecated)
import google.generativeai as genai
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
client = genai.GenerativeModel("gemini-2.0-flash")
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)

# After: New SDK (recommended)
from google import genai
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)
```

## Using with Metrics Collections (Modern Approach)

For the modern metrics collections API, you need to explicitly create both LLM and embeddings:

```
import os
from google import genai
from ragas.llms import llm_factory
from ragas.embeddings import GoogleEmbeddings
from ragas.metrics.collections import AnswerCorrectness, ContextPrecision

# Create client (new SDK)
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# Create LLM
llm = llm_factory("gemini-2.0-flash", provider="google", client=client)

# Create embeddings using the same client
embeddings = GoogleEmbeddings(client=client, model="gemini-embedding-001")

# Create metrics with explicit LLM and embeddings
metrics = [
    ContextPrecision(llm=llm),  # LLM-only metric
    AnswerCorrectness(llm=llm, embeddings=embeddings),  # Needs both
]

# Use metrics with your evaluation workflow
result = await metrics[1].ascore(
    user_input="What is the capital of France?",
    response="Paris",
    reference="Paris is the capital of France."
)
```

**Key difference from legacy approach:**
- Legacy `evaluate()`: Auto-creates embeddings from LLM provider
- Modern collections: You explicitly pass embeddings to each metric

This gives you more control and works seamlessly with Gemini!

## Supported Metrics

All Ragas metrics work with Gemini:

* Answer Correctness
* Answer Relevancy
* Answer Similarity
* Aspect Critique
* Context Precision
* Context Recall
* Context Entities Recall
* Faithfulness
* NLI Eval
* Response Relevancy

See [Metrics Reference](../../../concepts/metrics/) for details.

## Advanced: Custom Model Parameters

Pass custom parameters to Gemini:

```
llm = llm_factory(
    "gemini-2.0-flash",
    client=client,
    temperature=0.5,
    max_tokens=2048,
    top_p=0.9,
    top_k=40,
)
```

## Resources

* [Google GenAI SDK Documentation](https://googleapis.github.io/python-genai/)
* [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
* [Ragas Metrics Documentation](../../../concepts/metrics/)
* [Ragas LLM Factory Guide](../llm-factory.md)

December 16, 2025




November 28, 2025

Back to top