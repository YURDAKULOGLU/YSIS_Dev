/embeddings | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

## Quick Start[​](#quick-start "Direct link to Quick Start")

```
from litellm import embedding  
import os  
os.environ['OPENAI_API_KEY'] = ""  
response = embedding(model='text-embedding-ada-002', input=["good morning from litellm"])
```

## Async Usage - `aembedding()`[​](#async-usage---aembedding "Direct link to async-usage---aembedding")

LiteLLM provides an asynchronous version of the `embedding` function called `aembedding`:

```
from litellm import aembedding  
import asyncio  
  
async def get_embedding():  
    response = await aembedding(  
        model='text-embedding-ada-002',  
        input=["good morning from litellm"]  
    )  
    return response  
  
response = asyncio.run(get_embedding())  
print(response)
```

## Proxy Usage[​](#proxy-usage "Direct link to Proxy Usage")

**NOTE**
For `vertex_ai`,

```
export GOOGLE_APPLICATION_CREDENTIALS="absolute/path/to/service_account.json"
```

### Add model to config[​](#add-model-to-config "Direct link to Add model to config")

```
model_list:  
- model_name: textembedding-gecko  
  litellm_params:  
    model: vertex_ai/textembedding-gecko  
  
general_settings:  
  master_key: sk-1234
```

### Start proxy[​](#start-proxy "Direct link to Start proxy")

```
litellm --config /path/to/config.yaml   
  
# RUNNING on http://0.0.0.0:4000
```

### Test[​](#test "Direct link to Test")

* Curl
* OpenAI (python)
* Langchain Embeddings

```
curl --location 'http://0.0.0.0:4000/embeddings' \  
--header 'Authorization: Bearer sk-1234' \  
--header 'Content-Type: application/json' \  
--data '{"input": ["Academia.edu uses"], "model": "textembedding-gecko", "encoding_format": "base64"}'
```

```
from openai import OpenAI  
client = OpenAI(  
  api_key="sk-1234",  
  base_url="http://0.0.0.0:4000"  
)  
  
client.embeddings.create(  
  model="textembedding-gecko",  
  input="The food was delicious and the waiter...",  
  encoding_format="float"  
)
```

```
from langchain_openai import OpenAIEmbeddings  
  
embeddings = OpenAIEmbeddings(model="textembedding-gecko", openai_api_base="http://0.0.0.0:4000", openai_api_key="sk-1234")  
  
text = "This is a test document."  
  
query_result = embeddings.embed_query(text)  
  
print(f"VERTEX AI EMBEDDINGS")  
print(query_result[:5])
```

## Image Embeddings[​](#image-embeddings "Direct link to Image Embeddings")

For models that support image embeddings, you can pass in a base64 encoded image string to the `input` param.

* SDK
* PROXY

```
from litellm import embedding  
import os  
  
# set your api key  
os.environ["COHERE_API_KEY"] = ""  
  
response = embedding(model="cohere/embed-english-v3.0", input=["<base64 encoded image>"])
```

1. Setup config.yaml

```
model_list:  
  - model_name: cohere-embed  
    litellm_params:  
      model: cohere/embed-english-v3.0  
      api_key: os.environ/COHERE_API_KEY
```

2. Start proxy

```
litellm --config /path/to/config.yaml   
  
# RUNNING on http://0.0.0.0:4000
```

3. Test it!

```
curl -X POST 'http://0.0.0.0:4000/v1/embeddings' \  
-H 'Authorization: Bearer sk-54d77cd67b9febbb' \  
-H 'Content-Type: application/json' \  
-d '{  
  "model": "cohere/embed-english-v3.0",  
  "input": ["<base64 encoded image>"]  
}'
```

## Input Params for `litellm.embedding()`[​](#input-params-for-litellmembedding "Direct link to input-params-for-litellmembedding")

info

Any non-openai params, will be treated as provider-specific params, and sent in the request body as kwargs to the provider.

[**See Reserved Params**](https://github.com/BerriAI/litellm/blob/2f5f85cb52f36448d1f8bbfbd3b8af8167d0c4c8/litellm/main.py#L3130)

[**See Example**](#example)

### Required Fields[​](#required-fields "Direct link to Required Fields")

* `model`: *string* - ID of the model to use. `model='text-embedding-ada-002'`
* `input`: *string or array* - Input text to embed, encoded as a string or array of tokens. To embed multiple inputs in a single request, pass an array of strings or array of token arrays. The input must not exceed the max input tokens for the model (8192 tokens for text-embedding-ada-002), cannot be an empty string, and any array must be 2048 dimensions or less.

```
input=["good morning from litellm"]
```

### Optional LiteLLM Fields[​](#optional-litellm-fields "Direct link to Optional LiteLLM Fields")

* `user`: *string (optional)* A unique identifier representing your end-user,
* `dimensions`: *integer (Optional)* The number of dimensions the resulting output embeddings should have. Only supported in OpenAI/Azure text-embedding-3 and later models.
* `encoding_format`: *string (Optional)* The format to return the embeddings in. Can be either `"float"` or `"base64"`. Defaults to `encoding_format="float"`
* `timeout`: *integer (Optional)* - The maximum time, in seconds, to wait for the API to respond. Defaults to 600 seconds (10 minutes).
* `api_base`: *string (optional)* - The api endpoint you want to call the model with
* `api_version`: *string (optional)* - (Azure-specific) the api version for the call
* `api_key`: *string (optional)* - The API key to authenticate and authorize requests. If not provided, the default API key is used.
* `api_type`: *string (optional)* - The type of API to use.

### Output from `litellm.embedding()`[​](#output-from-litellmembedding "Direct link to output-from-litellmembedding")

```
{  
  "object": "list",  
  "data": [  
    {  
      "object": "embedding",  
      "index": 0,  
      "embedding": [  
        -0.0022326677571982145,  
        0.010749882087111473,  
        ...  
        ...  
        ...  
     
      ]  
    }  
  ],  
  "model": "text-embedding-ada-002-v2",  
  "usage": {  
    "prompt_tokens": 10,  
    "total_tokens": 10  
  }  
}
```

## OpenAI Embedding Models[​](#openai-embedding-models "Direct link to OpenAI Embedding Models")

### Usage[​](#usage "Direct link to Usage")

```
from litellm import embedding  
import os  
os.environ['OPENAI_API_KEY'] = ""  
response = embedding(  
    model="text-embedding-3-small",  
    input=["good morning from litellm", "this is another item"],  
    metadata={"anything": "good day"},  
    dimensions=5 # Only supported in text-embedding-3 and later models.  
)
```

| Model Name | Function Call | Required OS Variables |
| --- | --- | --- |
| text-embedding-3-small | `embedding('text-embedding-3-small', input)` | `os.environ['OPENAI_API_KEY']` |
| text-embedding-3-large | `embedding('text-embedding-3-large', input)` | `os.environ['OPENAI_API_KEY']` |
| text-embedding-ada-002 | `embedding('text-embedding-ada-002', input)` | `os.environ['OPENAI_API_KEY']` |

## OpenAI Compatible Embedding Models[​](#openai-compatible-embedding-models "Direct link to OpenAI Compatible Embedding Models")

Use this for calling `/embedding` endpoints on OpenAI Compatible Servers, example <https://github.com/xorbitsai/inference>

**Note add `openai/` prefix to model so litellm knows to route to OpenAI**

### Usage[​](#usage-1 "Direct link to Usage")

```
from litellm import embedding  
response = embedding(  
  model = "openai/<your-llm-name>",     # add `openai/` prefix to model so litellm knows to route to OpenAI  
  api_base="http://0.0.0.0:4000/"       # set API Base of your Custom OpenAI Endpoint  
  input=["good morning from litellm"]  
)
```

## Bedrock Embedding[​](#bedrock-embedding "Direct link to Bedrock Embedding")

### API keys[​](#api-keys "Direct link to API keys")

This can be set as env variables or passed as **params to litellm.embedding()**

```
import os  
os.environ["AWS_ACCESS_KEY_ID"] = ""  # Access key  
os.environ["AWS_SECRET_ACCESS_KEY"] = "" # Secret access key  
os.environ["AWS_REGION_NAME"] = "" # us-east-1, us-east-2, us-west-1, us-west-2
```

### Usage[​](#usage-2 "Direct link to Usage")

```
from litellm import embedding  
response = embedding(  
    model="amazon.titan-embed-text-v1",  
    input=["good morning from litellm"],  
)  
print(response)
```

| Model Name | Function Call |
| --- | --- |
| Amazon Nova Multimodal Embeddings | `embedding(model="bedrock/amazon.nova-2-multimodal-embeddings-v1:0", input=input)` |
| Amazon Nova (Async) | `embedding(model="bedrock/async_invoke/amazon.nova-2-multimodal-embeddings-v1:0", input=input, input_type="text", output_s3_uri="s3://bucket/")` |
| Titan Embeddings - G1 | `embedding(model="amazon.titan-embed-text-v1", input=input)` |
| Cohere Embeddings - English | `embedding(model="cohere.embed-english-v3", input=input)` |
| Cohere Embeddings - Multilingual | `embedding(model="cohere.embed-multilingual-v3", input=input)` |
| TwelveLabs Marengo (Async) | `embedding(model="bedrock/async_invoke/us.twelvelabs.marengo-embed-2-7-v1:0", input=input, input_type="text")` |

## TwelveLabs Bedrock Embedding Models[​](#twelvelabs-bedrock-embedding-models "Direct link to TwelveLabs Bedrock Embedding Models")

TwelveLabs Marengo models support multimodal embeddings (text, image, video, audio) and require the `input_type` parameter to specify the input format.

### Usage[​](#usage-3 "Direct link to Usage")

```
from litellm import embedding  
import os  
  
# Set AWS credentials  
os.environ["AWS_ACCESS_KEY_ID"] = ""  
os.environ["AWS_SECRET_ACCESS_KEY"] = ""  
os.environ["AWS_REGION_NAME"] = "us-east-1"  
  
# Text embedding  
response = embedding(  
    model="bedrock/us.twelvelabs.marengo-embed-2-7-v1:0",  
    input=["Hello world from LiteLLM!"],  
    input_type="text"  # Required parameter  
)  
  
# Image embedding (base64)  
response = embedding(  
    model="bedrock/async_invoke/us.twelvelabs.marengo-embed-2-7-v1:0",  
    input=["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."],  
    input_type="image",  # Required parameter  
    output_s3_uri="s3://your-bucket/async-invoke-output/"  
)  
  
# Video embedding (S3 URL)  
response = embedding(  
    model="bedrock/async_invoke/us.twelvelabs.marengo-embed-2-7-v1:0",  
    input=["s3://your-bucket/video.mp4"],  
    input_type="video",  # Required parameter  
    output_s3_uri="s3://your-bucket/async-invoke-output/"  
)
```

### Required Parameters[​](#required-parameters "Direct link to Required Parameters")

| Parameter | Description | Values |
| --- | --- | --- |
| `input_type` | Type of input content | `"text"`, `"image"`, `"video"`, `"audio"` |

### Supported Models[​](#supported-models "Direct link to Supported Models")

| Model Name | Function Call | Notes |
| --- | --- | --- |
| TwelveLabs Marengo 2.7 (Sync) | `embedding(model="bedrock/us.twelvelabs.marengo-embed-2-7-v1:0", input=input, input_type="text")` | Text embeddings only |
| TwelveLabs Marengo 2.7 (Async) | `embedding(model="bedrock/async_invoke/us.twelvelabs.marengo-embed-2-7-v1:0", input=input, input_type="text/image/video/audio")` | All input types, requires `output_s3_uri` |

## Cohere Embedding Models[​](#cohere-embedding-models "Direct link to Cohere Embedding Models")

<https://docs.cohere.com/reference/embed>

### Usage[​](#usage-4 "Direct link to Usage")

```
from litellm import embedding  
os.environ["COHERE_API_KEY"] = "cohere key"  
  
# cohere call  
response = embedding(  
    model="embed-english-v3.0",   
    input=["good morning from litellm", "this is another item"],   
    input_type="search_document" # optional param for v3 llms  
)
```

| Model Name | Function Call |
| --- | --- |
| embed-english-v3.0 | `embedding(model="embed-english-v3.0", input=["good morning from litellm", "this is another item"])` |
| embed-english-light-v3.0 | `embedding(model="embed-english-light-v3.0", input=["good morning from litellm", "this is another item"])` |
| embed-multilingual-v3.0 | `embedding(model="embed-multilingual-v3.0", input=["good morning from litellm", "this is another item"])` |
| embed-multilingual-light-v3.0 | `embedding(model="embed-multilingual-light-v3.0", input=["good morning from litellm", "this is another item"])` |
| embed-english-v2.0 | `embedding(model="embed-english-v2.0", input=["good morning from litellm", "this is another item"])` |
| embed-english-light-v2.0 | `embedding(model="embed-english-light-v2.0", input=["good morning from litellm", "this is another item"])` |
| embed-multilingual-v2.0 | `embedding(model="embed-multilingual-v2.0", input=["good morning from litellm", "this is another item"])` |

## NVIDIA NIM Embedding Models[​](#nvidia-nim-embedding-models "Direct link to NVIDIA NIM Embedding Models")

### API keys[​](#api-keys-1 "Direct link to API keys")

This can be set as env variables or passed as **params to litellm.embedding()**

```
import os  
os.environ["NVIDIA_NIM_API_KEY"] = ""  # api key  
os.environ["NVIDIA_NIM_API_BASE"] = "" # nim endpoint url
```

### Usage[​](#usage-5 "Direct link to Usage")

```
from litellm import embedding  
import os  
os.environ['NVIDIA_NIM_API_KEY'] = ""  
response = embedding(  
    model='nvidia_nim/<model_name>',   
    input=["good morning from litellm"],  
    input_type="query"  
)
```

## `input_type` Parameter for Embedding Models[​](#input_type-parameter-for-embedding-models "Direct link to input_type-parameter-for-embedding-models")

Certain embedding models, such as `nvidia/embed-qa-4` and the E5 family, operate in **dual modes**—one for **indexing documents (passages)** and another for **querying**. To maintain high retrieval accuracy, it's essential to specify how the input text is being used by setting the `input_type` parameter correctly.

### Usage[​](#usage-6 "Direct link to Usage")

Set the `input_type` parameter to one of the following values:

* `"passage"` – for embedding content during **indexing** (e.g., documents).
* `"query"` – for embedding content during **retrieval** (e.g., user queries).

> **Warning:** Incorrect usage of `input_type` can lead to a significant drop in retrieval performance.

All models listed [here](https://build.nvidia.com/explore/retrieval) are supported:

| Model Name | Function Call |
| --- | --- |
| NV-Embed-QA | `embedding(model="nvidia_nim/NV-Embed-QA", input)` |
| nvidia/nv-embed-v1 | `embedding(model="nvidia_nim/nvidia/nv-embed-v1", input)` |
| nvidia/nv-embedqa-mistral-7b-v2 | `embedding(model="nvidia_nim/nvidia/nv-embedqa-mistral-7b-v2", input)` |
| nvidia/nv-embedqa-e5-v5 | `embedding(model="nvidia_nim/nvidia/nv-embedqa-e5-v5", input)` |
| nvidia/embed-qa-4 | `embedding(model="nvidia_nim/nvidia/embed-qa-4", input)` |
| nvidia/llama-3.2-nv-embedqa-1b-v1 | `embedding(model="nvidia_nim/nvidia/llama-3.2-nv-embedqa-1b-v1", input)` |
| nvidia/llama-3.2-nv-embedqa-1b-v2 | `embedding(model="nvidia_nim/nvidia/llama-3.2-nv-embedqa-1b-v2", input)` |
| snowflake/arctic-embed-l | `embedding(model="nvidia_nim/snowflake/arctic-embed-l", input)` |
| baai/bge-m3 | `embedding(model="nvidia_nim/baai/bge-m3", input)` |

## HuggingFace Embedding Models[​](#huggingface-embedding-models "Direct link to HuggingFace Embedding Models")

LiteLLM supports all Feature-Extraction + Sentence Similarity Embedding models: <https://huggingface.co/models?pipeline_tag=feature-extraction>

### Usage[​](#usage-7 "Direct link to Usage")

```
from litellm import embedding  
import os  
os.environ['HUGGINGFACE_API_KEY'] = ""  
response = embedding(  
    model='huggingface/microsoft/codebert-base',   
    input=["good morning from litellm"]  
)
```

### Usage - Set input\_type[​](#usage---set-input_type "Direct link to Usage - Set input_type")

LiteLLM infers input type (feature-extraction or sentence-similarity) by making a GET request to the api base.

Override this, by setting the `input_type` yourself.

```
from litellm import embedding  
import os  
os.environ['HUGGINGFACE_API_KEY'] = ""  
response = embedding(  
    model='huggingface/microsoft/codebert-base',   
    input=["good morning from litellm", "you are a good bot"],  
    api_base = "https://p69xlsj6rpno5drq.us-east-1.aws.endpoints.huggingface.cloud",   
    input_type="sentence-similarity"  
)
```

### Usage - Custom API Base[​](#usage---custom-api-base "Direct link to Usage - Custom API Base")

```
from litellm import embedding  
import os  
os.environ['HUGGINGFACE_API_KEY'] = ""  
response = embedding(  
    model='huggingface/microsoft/codebert-base',   
    input=["good morning from litellm"],  
    api_base = "https://p69xlsj6rpno5drq.us-east-1.aws.endpoints.huggingface.cloud"  
)
```

| Model Name | Function Call | Required OS Variables |
| --- | --- | --- |
| microsoft/codebert-base | `embedding('huggingface/microsoft/codebert-base', input=input)` | `os.environ['HUGGINGFACE_API_KEY']` |
| BAAI/bge-large-zh | `embedding('huggingface/BAAI/bge-large-zh', input=input)` | `os.environ['HUGGINGFACE_API_KEY']` |
| any-hf-embedding-model | `embedding('huggingface/hf-embedding-model', input=input)` | `os.environ['HUGGINGFACE_API_KEY']` |

## Mistral AI Embedding Models[​](#mistral-ai-embedding-models "Direct link to Mistral AI Embedding Models")

All models listed here <https://docs.mistral.ai/platform/endpoints> are supported

### Usage[​](#usage-8 "Direct link to Usage")

```
from litellm import embedding  
import os  
  
os.environ['MISTRAL_API_KEY'] = ""  
response = embedding(  
    model="mistral/mistral-embed",  
    input=["good morning from litellm"],  
)  
print(response)
```

| Model Name | Function Call |
| --- | --- |
| mistral-embed | `embedding(model="mistral/mistral-embed", input)` |

## Gemini AI Embedding Models[​](#gemini-ai-embedding-models "Direct link to Gemini AI Embedding Models")

### API keys[​](#api-keys-2 "Direct link to API keys")

This can be set as env variables or passed as **params to litellm.embedding()**

```
import os  
os.environ["GEMINI_API_KEY"] = ""
```

### Usage - Embedding[​](#usage---embedding "Direct link to Usage - Embedding")

```
from litellm import embedding  
response = embedding(  
  model="gemini/text-embedding-004",  
  input=["good morning from litellm"],  
)  
print(response)
```

All models listed [here](https://ai.google.dev/gemini-api/docs/models/gemini) are supported:

| Model Name | Function Call |
| --- | --- |
| text-embedding-004 | `embedding(model="gemini/text-embedding-004", input)` |

## Vertex AI Embedding Models[​](#vertex-ai-embedding-models "Direct link to Vertex AI Embedding Models")

### Usage - Embedding[​](#usage---embedding-1 "Direct link to Usage - Embedding")

```
import litellm  
from litellm import embedding  
litellm.vertex_project = "hardy-device-38811" # Your Project ID  
litellm.vertex_location = "us-central1"  # proj location  
  
response = embedding(  
    model="vertex_ai/textembedding-gecko",  
    input=["good morning from litellm"],  
)  
print(response)
```

### Supported Models[​](#supported-models-1 "Direct link to Supported Models")

All models listed [here](https://github.com/BerriAI/litellm/blob/57f37f743886a0249f630a6792d49dffc2c5d9b7/model_prices_and_context_window.json#L835) are supported

| Model Name | Function Call |
| --- | --- |
| textembedding-gecko | `embedding(model="vertex_ai/textembedding-gecko", input)` |
| textembedding-gecko-multilingual | `embedding(model="vertex_ai/textembedding-gecko-multilingual", input)` |
| textembedding-gecko-multilingual@001 | `embedding(model="vertex_ai/textembedding-gecko-multilingual@001", input)` |
| textembedding-gecko@001 | `embedding(model="vertex_ai/textembedding-gecko@001", input)` |
| textembedding-gecko@003 | `embedding(model="vertex_ai/textembedding-gecko@003", input)` |
| text-embedding-preview-0409 | `embedding(model="vertex_ai/text-embedding-preview-0409", input)` |
| text-multilingual-embedding-preview-0409 | `embedding(model="vertex_ai/text-multilingual-embedding-preview-0409", input)` |

## Voyage AI Embedding Models[​](#voyage-ai-embedding-models "Direct link to Voyage AI Embedding Models")

### Usage - Embedding[​](#usage---embedding-2 "Direct link to Usage - Embedding")

```
from litellm import embedding  
import os  
  
os.environ['VOYAGE_API_KEY'] = ""  
response = embedding(  
    model="voyage/voyage-01",  
    input=["good morning from litellm"],  
)  
print(response)
```

### Supported Models[​](#supported-models-2 "Direct link to Supported Models")

All models listed here <https://docs.voyageai.com/embeddings/#models-and-specifics> are supported

| Model Name | Function Call |
| --- | --- |
| voyage-01 | `embedding(model="voyage/voyage-01", input)` |
| voyage-lite-01 | `embedding(model="voyage/voyage-lite-01", input)` |
| voyage-lite-01-instruct | `embedding(model="voyage/voyage-lite-01-instruct", input)` |

### Provider-specific Params[​](#provider-specific-params "Direct link to Provider-specific Params")

info

Any non-openai params, will be treated as provider-specific params, and sent in the request body as kwargs to the provider.

[**See Reserved Params**](https://github.com/BerriAI/litellm/blob/2f5f85cb52f36448d1f8bbfbd3b8af8167d0c4c8/litellm/main.py#L3130)

### **Example**[​](#example "Direct link to example")

Cohere v3 Models have a required parameter: `input_type`, it can be one of the following four values:

* `input_type="search_document"`: (default) Use this for texts (documents) you want to store in your vector database
* `input_type="search_query"`: Use this for search queries to find the most relevant documents in your vector database
* `input_type="classification"`: Use this if you use the embeddings as an input for a classification system
* `input_type="clustering"`: Use this if you use the embeddings for text clustering

<https://txt.cohere.com/introducing-embed-v3/>

* SDK
* PROXY

```
from litellm import embedding  
os.environ["COHERE_API_KEY"] = "cohere key"  
  
# cohere call  
response = embedding(  
    model="embed-english-v3.0",   
    input=["good morning from litellm", "this is another item"],   
    input_type="search_document" # 👈 PROVIDER-SPECIFIC PARAM  
)
```

**via config**

```
model_list:  
  - model_name: "cohere-embed"  
    litellm_params:  
      model: embed-english-v3.0  
      input_type: search_document # 👈 PROVIDER-SPECIFIC PARAM
```

**via request**

```
curl -X POST 'http://0.0.0.0:4000/v1/embeddings' \  
-H 'Authorization: Bearer sk-54d77cd67b9febbb' \  
-H 'Content-Type: application/json' \  
-d '{  
  "model": "cohere-embed",  
  "input": ["Are you authorized to work in United States of America?"],  
  "input_type": "search_document" # 👈 PROVIDER-SPECIFIC PARAM  
}'
```

## Nebius AI Studio Embedding Models[​](#nebius-ai-studio-embedding-models "Direct link to Nebius AI Studio Embedding Models")

### Usage - Embedding[​](#usage---embedding-3 "Direct link to Usage - Embedding")

```
from litellm import embedding  
import os  
  
os.environ['NEBIUS_API_KEY'] = ""  
response = embedding(  
    model="nebius/BAAI/bge-en-icl",  
    input=["Good morning from litellm!"],  
)  
print(response)
```

### Supported Models[​](#supported-models-3 "Direct link to Supported Models")

All supported models can be found here: <https://studio.nebius.ai/models/embedding>

| Model Name | Function Call |
| --- | --- |
| BAAI/bge-en-icl | `embedding(model="nebius/BAAI/bge-en-icl", input)` |
| BAAI/bge-multilingual-gemma2 | `embedding(model="nebius/BAAI/bge-multilingual-gemma2", input)` |
| intfloat/e5-mistral-7b-instruct | `embedding(model="nebius/intfloat/e5-mistral-7b-instruct", input)` |

* [Quick Start](#quick-start)
* [Async Usage - `aembedding()`](#async-usage---aembedding)
* [Proxy Usage](#proxy-usage)
  + [Add model to config](#add-model-to-config)
  + [Start proxy](#start-proxy)
  + [Test](#test)
* [Image Embeddings](#image-embeddings)
* [Input Params for `litellm.embedding()`](#input-params-for-litellmembedding)
  + [Required Fields](#required-fields)
  + [Optional LiteLLM Fields](#optional-litellm-fields)
  + [Output from `litellm.embedding()`](#output-from-litellmembedding)
* [OpenAI Embedding Models](#openai-embedding-models)
  + [Usage](#usage)
* [OpenAI Compatible Embedding Models](#openai-compatible-embedding-models)
  + [Usage](#usage-1)
* [Bedrock Embedding](#bedrock-embedding)
  + [API keys](#api-keys)
  + [Usage](#usage-2)
* [TwelveLabs Bedrock Embedding Models](#twelvelabs-bedrock-embedding-models)
  + [Usage](#usage-3)
  + [Required Parameters](#required-parameters)
  + [Supported Models](#supported-models)
* [Cohere Embedding Models](#cohere-embedding-models)
  + [Usage](#usage-4)
* [NVIDIA NIM Embedding Models](#nvidia-nim-embedding-models)
  + [API keys](#api-keys-1)
  + [Usage](#usage-5)
* [`input_type` Parameter for Embedding Models](#input_type-parameter-for-embedding-models)
  + [Usage](#usage-6)
* [HuggingFace Embedding Models](#huggingface-embedding-models)
  + [Usage](#usage-7)
  + [Usage - Set input\_type](#usage---set-input_type)
  + [Usage - Custom API Base](#usage---custom-api-base)
* [Mistral AI Embedding Models](#mistral-ai-embedding-models)
  + [Usage](#usage-8)
* [Gemini AI Embedding Models](#gemini-ai-embedding-models)
  + [API keys](#api-keys-2)
  + [Usage - Embedding](#usage---embedding)
* [Vertex AI Embedding Models](#vertex-ai-embedding-models)
  + [Usage - Embedding](#usage---embedding-1)
  + [Supported Models](#supported-models-1)
* [Voyage AI Embedding Models](#voyage-ai-embedding-models)
  + [Usage - Embedding](#usage---embedding-2)
  + [Supported Models](#supported-models-2)
  + [Provider-specific Params](#provider-specific-params)
  + [**Example**](#example)
* [Nebius AI Studio Embedding Models](#nebius-ai-studio-embedding-models)
  + [Usage - Embedding](#usage---embedding-3)
  + [Supported Models](#supported-models-3)