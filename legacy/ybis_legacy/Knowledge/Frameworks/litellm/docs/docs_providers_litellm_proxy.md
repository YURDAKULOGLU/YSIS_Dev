LiteLLM Proxy (LLM Gateway) | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

| Property | Details |
| --- | --- |
| Description | LiteLLM Proxy is an OpenAI-compatible gateway that allows you to interact with multiple LLM providers through a unified API. Simply use the `litellm_proxy/` prefix before the model name to route your requests through the proxy. |
| Provider Route on LiteLLM | `litellm_proxy/` (add this prefix to the model name, to route any requests to litellm\_proxy - e.g. `litellm_proxy/your-model-name`) |
| Setup LiteLLM Gateway | [LiteLLM Gateway ↗](/docs/simple_proxy) |
| Supported Endpoints | `/chat/completions`, `/completions`, `/embeddings`, `/audio/speech`, `/audio/transcriptions`, `/images`, `/images/edits`, `/rerank` |

## Required Variables[​](#required-variables "Direct link to Required Variables")

```
os.environ["LITELLM_PROXY_API_KEY"] = "" # "sk-1234" your litellm proxy api key   
os.environ["LITELLM_PROXY_API_BASE"] = "" # "http://localhost:4000" your litellm proxy api base
```

## Usage (Non Streaming)[​](#usage-non-streaming "Direct link to Usage (Non Streaming)")

```
import os   
import litellm  
from litellm import completion  
  
os.environ["LITELLM_PROXY_API_KEY"] = ""  
  
# set custom api base to your proxy  
# either set .env or litellm.api_base  
# os.environ["LITELLM_PROXY_API_BASE"] = ""  
litellm.api_base = "your-openai-proxy-url"  
  
  
messages = [{ "content": "Hello, how are you?","role": "user"}]  
  
# litellm proxy call  
response = completion(model="litellm_proxy/your-model-name", messages)
```

## Usage - passing `api_base`, `api_key` per request[​](#usage---passing-api_base-api_key-per-request "Direct link to usage---passing-api_base-api_key-per-request")

If you need to set api\_base dynamically, just pass it in completions instead - completions(...,api\_base="your-proxy-api-base")

```
import os   
import litellm  
from litellm import completion  
  
os.environ["LITELLM_PROXY_API_KEY"] = ""  
  
messages = [{ "content": "Hello, how are you?","role": "user"}]  
  
# litellm proxy call  
response = completion(  
    model="litellm_proxy/your-model-name",   
    messages=messages,   
    api_base = "your-litellm-proxy-url",  
    api_key = "your-litellm-proxy-api-key"  
)
```

## Usage - Streaming[​](#usage---streaming "Direct link to Usage - Streaming")

```
import os   
import litellm  
from litellm import completion  
  
os.environ["LITELLM_PROXY_API_KEY"] = ""  
  
messages = [{ "content": "Hello, how are you?","role": "user"}]  
  
# openai call  
response = completion(  
    model="litellm_proxy/your-model-name",   
    messages=messages,  
    api_base = "your-litellm-proxy-url",   
    stream=True  
)  
  
for chunk in response:  
    print(chunk)
```

## Embeddings[​](#embeddings "Direct link to Embeddings")

```
import litellm  
  
response = litellm.embedding(  
    model="litellm_proxy/your-embedding-model",  
    input="Hello world",  
    api_base="your-litellm-proxy-url",  
    api_key="your-litellm-proxy-api-key"  
)
```

## Image Generation[​](#image-generation "Direct link to Image Generation")

```
import litellm  
  
response = litellm.image_generation(  
    model="litellm_proxy/dall-e-3",  
    prompt="A beautiful sunset over mountains",  
    api_base="your-litellm-proxy-url",  
    api_key="your-litellm-proxy-api-key"  
)
```

## Image Edit[​](#image-edit "Direct link to Image Edit")

```
import litellm  
  
with open("your-image.png", "rb") as f:  
    response = litellm.image_edit(  
        model="litellm_proxy/gpt-image-1",  
        prompt="Make this image a watercolor painting",  
        image=[f],  
        api_base="your-litellm-proxy-url",  
        api_key="your-litellm-proxy-api-key",  
    )
```

## Audio Transcription[​](#audio-transcription "Direct link to Audio Transcription")

```
import litellm  
  
response = litellm.transcription(  
    model="litellm_proxy/whisper-1",  
    file="your-audio-file",  
    api_base="your-litellm-proxy-url",  
    api_key="your-litellm-proxy-api-key"  
)
```

## Text to Speech[​](#text-to-speech "Direct link to Text to Speech")

```
import litellm  
  
response = litellm.speech(  
    model="litellm_proxy/tts-1",  
    input="Hello world",  
    api_base="your-litellm-proxy-url",  
    api_key="your-litellm-proxy-api-key"  
)
```

## Rerank[​](#rerank "Direct link to Rerank")

```
import litellm  
  
import litellm  
  
response = litellm.rerank(  
    model="litellm_proxy/rerank-english-v2.0",  
    query="What is machine learning?",  
    documents=[  
        "Machine learning is a field of study in artificial intelligence",  
        "Biology is the study of living organisms"  
    ],  
    api_base="your-litellm-proxy-url",  
    api_key="your-litellm-proxy-api-key"  
)
```

## Integration with Other Libraries[​](#integration-with-other-libraries "Direct link to Integration with Other Libraries")

LiteLLM Proxy works seamlessly with Langchain, LlamaIndex, OpenAI JS, Anthropic SDK, Instructor, and more.

[Learn how to use LiteLLM proxy with these libraries →](/docs/proxy/user_keys)

## Send all SDK requests to LiteLLM Proxy[​](#send-all-sdk-requests-to-litellm-proxy "Direct link to Send all SDK requests to LiteLLM Proxy")

info

Requires v1.72.1 or higher.

Use this when calling LiteLLM Proxy from any library / codebase already using the LiteLLM SDK.

These flags will route all requests through your LiteLLM proxy, regardless of the model specified.

When enabled, requests will use `LITELLM_PROXY_API_BASE` with `LITELLM_PROXY_API_KEY` as the authentication.

### Option 1: Set Globally in Code[​](#option-1-set-globally-in-code "Direct link to Option 1: Set Globally in Code")

```
# Set the flag globally for all requests  
litellm.use_litellm_proxy = True  
  
response = litellm.completion(  
    model="vertex_ai/gemini-2.0-flash-001",  
    messages=[{"role": "user", "content": "Hello, how are you?"}]  
)
```

### Option 2: Control via Environment Variable[​](#option-2-control-via-environment-variable "Direct link to Option 2: Control via Environment Variable")

```
# Control proxy usage through environment variable  
os.environ["USE_LITELLM_PROXY"] = "True"  
  
response = litellm.completion(  
    model="vertex_ai/gemini-2.0-flash-001",  
    messages=[{"role": "user", "content": "Hello, how are you?"}]  
)
```

### Option 3: Set Per Request[​](#option-3-set-per-request "Direct link to Option 3: Set Per Request")

```
# Enable proxy for specific requests only  
response = litellm.completion(  
    model="vertex_ai/gemini-2.0-flash-001",  
    messages=[{"role": "user", "content": "Hello, how are you?"}],  
    use_litellm_proxy=True  
)
```

## Sending `tags` to LiteLLM Proxy[​](#sending-tags-to-litellm-proxy "Direct link to sending-tags-to-litellm-proxy")

Tags allow you to categorize and track your API requests for monitoring, debugging, and analytics purposes. You can send tags as a list of strings to the LiteLLM Proxy using the `extra_body` parameter.

### Usage[​](#usage "Direct link to Usage")

Send tags by including them in the `extra_body` parameter of your completion request:

Usage

```
import litellm  
  
response = litellm.completion(  
    model="gpt-4",  
    messages=[{"role": "user", "content": "What is the capital of France?"}],  
    api_base="http://localhost:4000",  
    api_key="sk-1234",  
    extra_body={"tags": ["user:ishaan", "department:engineering", "priority:high"]}  
)
```

### Async Usage[​](#async-usage "Direct link to Async Usage")

Async Usage

```
import litellm  
  
response = await litellm.acompletion(  
    model="gpt-4",  
    messages=[{"role": "user", "content": "What is the capital of France?"}],  
    api_base="http://localhost:4000",   
    api_key="sk-1234",  
    extra_body={"tags": ["user:ishaan", "department:engineering"]}  
)
```

* [Required Variables](#required-variables)
* [Usage (Non Streaming)](#usage-non-streaming)
* [Usage - passing `api_base`, `api_key` per request](#usage---passing-api_base-api_key-per-request)
* [Usage - Streaming](#usage---streaming)
* [Embeddings](#embeddings)
* [Image Generation](#image-generation)
* [Image Edit](#image-edit)
* [Audio Transcription](#audio-transcription)
* [Text to Speech](#text-to-speech)
* [Rerank](#rerank)
* [Integration with Other Libraries](#integration-with-other-libraries)
* [Send all SDK requests to LiteLLM Proxy](#send-all-sdk-requests-to-litellm-proxy)
  + [Option 1: Set Globally in Code](#option-1-set-globally-in-code)
  + [Option 2: Control via Environment Variable](#option-2-control-via-environment-variable)
  + [Option 3: Set Per Request](#option-3-set-per-request)
* [Sending `tags` to LiteLLM Proxy](#sending-tags-to-litellm-proxy)
  + [Usage](#usage)
  + [Async Usage](#async-usage)