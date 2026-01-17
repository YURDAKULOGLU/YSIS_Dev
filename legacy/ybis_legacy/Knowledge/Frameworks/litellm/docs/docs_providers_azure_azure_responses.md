Azure Responses API | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

| Property | Details |
| --- | --- |
| Description | Azure OpenAI Responses API |
| `custom_llm_provider` on LiteLLM | `azure/` |
| Supported Operations | `/v1/responses` |
| Azure OpenAI Responses API | [Azure OpenAI Responses API ↗](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/responses?tabs=python-secure) |
| Cost Tracking, Logging Support | ✅ LiteLLM will log, track cost for Responses API Requests |
| Supported OpenAI Params | ✅ All OpenAI params are supported, [See here](https://github.com/BerriAI/litellm/blob/0717369ae6969882d149933da48eeb8ab0e691bd/litellm/llms/openai/responses/transformation.py#L23) |

## Usage[​](#usage "Direct link to Usage")

## Create a model response[​](#create-a-model-response "Direct link to Create a model response")

* LiteLLM SDK
* OpenAI SDK with LiteLLM Proxy

#### Non-streaming[​](#non-streaming "Direct link to Non-streaming")

Azure Responses API

```
import litellm  
  
# Non-streaming response  
response = litellm.responses(  
    model="azure/o1-pro",  
    input="Tell me a three sentence bedtime story about a unicorn.",  
    max_output_tokens=100,  
    api_key=os.getenv("AZURE_RESPONSES_OPENAI_API_KEY"),  
    api_base="https://litellm8397336933.openai.azure.com/",  
    api_version="2023-03-15-preview",  
)  
  
print(response)
```

#### Streaming[​](#streaming "Direct link to Streaming")

Azure Responses API

```
import litellm  
  
# Streaming response  
response = litellm.responses(  
    model="azure/o1-pro",  
    input="Tell me a three sentence bedtime story about a unicorn.",  
    stream=True,  
    api_key=os.getenv("AZURE_RESPONSES_OPENAI_API_KEY"),  
    api_base="https://litellm8397336933.openai.azure.com/",  
    api_version="2023-03-15-preview",  
)  
  
for event in response:  
    print(event)
```

First, add this to your litellm proxy config.yaml:

Azure Responses API

```
model_list:  
  - model_name: o1-pro  
    litellm_params:  
      model: azure/o1-pro  
      api_key: os.environ/AZURE_RESPONSES_OPENAI_API_KEY  
      api_base: https://litellm8397336933.openai.azure.com/  
      api_version: 2023-03-15-preview
```

Start your LiteLLM proxy:

```
litellm --config /path/to/config.yaml  
  
# RUNNING on http://0.0.0.0:4000
```

Then use the OpenAI SDK pointed to your proxy:

#### Non-streaming[​](#non-streaming-1 "Direct link to Non-streaming")

```
from openai import OpenAI  
  
# Initialize client with your proxy URL  
client = OpenAI(  
    base_url="http://localhost:4000",  # Your proxy URL  
    api_key="your-api-key"             # Your proxy API key  
)  
  
# Non-streaming response  
response = client.responses.create(  
    model="o1-pro",  
    input="Tell me a three sentence bedtime story about a unicorn."  
)  
  
print(response)
```

#### Streaming[​](#streaming-1 "Direct link to Streaming")

```
from openai import OpenAI  
  
# Initialize client with your proxy URL  
client = OpenAI(  
    base_url="http://localhost:4000",  # Your proxy URL  
    api_key="your-api-key"             # Your proxy API key  
)  
  
# Streaming response  
response = client.responses.create(  
    model="o1-pro",  
    input="Tell me a three sentence bedtime story about a unicorn.",  
    stream=True  
)  
  
for event in response:  
    print(event)
```

## Azure Codex Models[​](#azure-codex-models "Direct link to Azure Codex Models")

Codex models use Azure's new [/v1/preview API](https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-lifecycle?tabs=key#next-generation-api) which provides ongoing access to the latest features with no need to update `api-version` each month.

**LiteLLM will send your requests to the `/v1/preview` endpoint when you set `api_version="preview"`.**

* LiteLLM SDK
* OpenAI SDK with LiteLLM Proxy

#### Non-streaming[​](#non-streaming-2 "Direct link to Non-streaming")

Azure Codex Models

```
import litellm  
  
# Non-streaming response with Codex models  
response = litellm.responses(  
    model="azure/codex-mini",  
    input="Tell me a three sentence bedtime story about a unicorn.",  
    max_output_tokens=100,  
    api_key=os.getenv("AZURE_RESPONSES_OPENAI_API_KEY"),  
    api_base="https://litellm8397336933.openai.azure.com",  
    api_version="preview", # 👈 key difference  
)  
  
print(response)
```

#### Streaming[​](#streaming-2 "Direct link to Streaming")

Azure Codex Models

```
import litellm  
  
# Streaming response with Codex models  
response = litellm.responses(  
    model="azure/codex-mini",  
    input="Tell me a three sentence bedtime story about a unicorn.",  
    stream=True,  
    api_key=os.getenv("AZURE_RESPONSES_OPENAI_API_KEY"),  
    api_base="https://litellm8397336933.openai.azure.com",  
    api_version="preview", # 👈 key difference  
)  
  
for event in response:  
    print(event)
```

First, add this to your litellm proxy config.yaml:

Azure Codex Models

```
model_list:  
  - model_name: codex-mini  
    litellm_params:  
      model: azure/codex-mini  
      api_key: os.environ/AZURE_RESPONSES_OPENAI_API_KEY  
      api_base: https://litellm8397336933.openai.azure.com  
      api_version: preview # 👈 key difference
```

Start your LiteLLM proxy:

```
litellm --config /path/to/config.yaml  
  
# RUNNING on http://0.0.0.0:4000
```

Then use the OpenAI SDK pointed to your proxy:

#### Non-streaming[​](#non-streaming-3 "Direct link to Non-streaming")

```
from openai import OpenAI  
  
# Initialize client with your proxy URL  
client = OpenAI(  
    base_url="http://localhost:4000",  # Your proxy URL  
    api_key="your-api-key"             # Your proxy API key  
)  
  
# Non-streaming response  
response = client.responses.create(  
    model="codex-mini",  
    input="Tell me a three sentence bedtime story about a unicorn."  
)  
  
print(response)
```

#### Streaming[​](#streaming-3 "Direct link to Streaming")

```
from openai import OpenAI  
  
# Initialize client with your proxy URL  
client = OpenAI(  
    base_url="http://localhost:4000",  # Your proxy URL  
    api_key="your-api-key"             # Your proxy API key  
)  
  
# Streaming response  
response = client.responses.create(  
    model="codex-mini",  
    input="Tell me a three sentence bedtime story about a unicorn.",  
    stream=True  
)  
  
for event in response:  
    print(event)
```

## Calling via `/chat/completions`[​](#calling-via-chatcompletions "Direct link to calling-via-chatcompletions")

You can also call the Azure Responses API via the `/chat/completions` endpoint.

* LiteLLM SDK
* OpenAI SDK with LiteLLM Proxy

```
from litellm import completion  
import os   
  
os.environ["AZURE_API_BASE"] = "https://my-endpoint-sweden-berri992.openai.azure.com/"  
os.environ["AZURE_API_VERSION"] = "2023-03-15-preview"  
os.environ["AZURE_API_KEY"] = "my-api-key"  
  
response = completion(  
    model="azure/responses/my-custom-o1-pro",  
    messages=[{"role": "user", "content": "Hello world"}],  
)  
  
print(response)
```

1. Setup config.yaml

```
model_list:  
  - model_name: my-custom-o1-pro  
    litellm_params:  
      model: azure/responses/my-custom-o1-pro  
      api_key: os.environ/AZURE_API_KEY  
      api_base: https://my-endpoint-sweden-berri992.openai.azure.com/  
      api_version: 2023-03-15-preview
```

2. Start LiteLLM proxy

```
litellm --config /path/to/config.yaml  
  
# RUNNING on http://0.0.0.0:4000
```

3. Test it!

```
curl http://localhost:4000/v1/chat/completions \  
  -X POST \  
  -H "Content-Type: application/json" \  
  -H "Authorization: Bearer $LITELLM_API_KEY" \  
  -d '{  
    "model": "my-custom-o1-pro",  
    "messages": [{"role": "user", "content": "Hello world"}]  
  }'
```

* [Usage](#usage)
* [Create a model response](#create-a-model-response)
* [Azure Codex Models](#azure-codex-models)
* [Calling via `/chat/completions`](#calling-via-chatcompletions)