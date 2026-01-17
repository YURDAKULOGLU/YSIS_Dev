Baseten | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

LiteLLM supports both Baseten Model APIs and dedicated deployments with automatic routing.

## API Types[​](#api-types "Direct link to API Types")

### Model API (Default)[​](#model-api-default "Direct link to Model API (Default)")

* **URL**: `https://inference.baseten.co/v1`
* **Format**: `baseten/<model-name>` (e.g., `baseten/openai/gpt-oss-120b`)
* **Best for**: Quick access to popular models

### Dedicated Deployments[​](#dedicated-deployments "Direct link to Dedicated Deployments")

* **URL**: `https://model-{id}.api.baseten.co/environments/production/sync/v1`
* **Format**: `baseten/{8-digit-alphanumeric-code}` (e.g., `baseten/abcd1234`)
* **Best for**: Custom models, latency SLAs

tip

**Automatic Routing**: LiteLLM detects the type based on model format:

* 8-digit alphanumeric codes → Dedicated deployment
* All other formats → Model API

## Quick Start[​](#quick-start "Direct link to Quick Start")

```
import os  
from litellm import completion  
  
os.environ['BASETEN_API_KEY'] = "your-api-key"  
  
# Model API (default)  
response = completion(  
    model="baseten/openai/gpt-oss-120b",  
    messages=[{"role": "user", "content": "Hello!"}]  
)  
  
# Dedicated deployment (8-digit ID)  
response = completion(  
    model="baseten/abcd1234",  
    messages=[{"role": "user", "content": "Hello!"}]  
)
```

## Examples[​](#examples "Direct link to Examples")

### Basic Usage[​](#basic-usage "Direct link to Basic Usage")

```
# Model API  
response = completion(  
    model="baseten/openai/gpt-oss-120b",  
    messages=[{"role": "user", "content": "Explain quantum computing"}],  
    max_tokens=500,  
    temperature=0.7  
)  
  
# Dedicated deployment  
response = completion(  
    model="baseten/abcd1234",  
    messages=[{"role": "user", "content": "Explain quantum computing"}],  
    max_tokens=500,  
    temperature=0.7  
)
```

### Streaming (Model API only)[​](#streaming-model-api-only "Direct link to Streaming (Model API only)")

```
response = completion(  
    model="baseten/openai/gpt-oss-120b",  
    messages=[{"role": "user", "content": "Write a poem"}],  
    stream=True,  
    stream_options={"include_usage": True}  
)  
  
for chunk in response:  
    if chunk.choices and chunk.choices[0].delta.content:  
        print(chunk.choices[0].delta.content, end="")
```

## Usage with LiteLLM Proxy[​](#usage-with-litellm-proxy "Direct link to Usage with LiteLLM Proxy")

1. **Config**:

```
model_list:  
  - model_name: baseten-model  
    litellm_params:  
      model: baseten/openai/gpt-oss-120b  
      api_key: your-baseten-api-key
```

2. **Request**:

```
import openai  
client = openai.OpenAI(  
    api_key="sk-1234",  
    base_url="http://0.0.0.0:4000"  
)  
  
response = client.chat.completions.create(  
    model="baseten-model",  
    messages=[{"role": "user", "content": "Hello!"}]  
)
```

* [API Types](#api-types)
  + [Model API (Default)](#model-api-default)
  + [Dedicated Deployments](#dedicated-deployments)
* [Quick Start](#quick-start)
* [Examples](#examples)
  + [Basic Usage](#basic-usage)
  + [Streaming (Model API only)](#streaming-model-api-only)
* [Usage with LiteLLM Proxy](#usage-with-litellm-proxy)