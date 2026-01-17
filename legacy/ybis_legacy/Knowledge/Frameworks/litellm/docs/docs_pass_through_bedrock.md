Bedrock (boto3) SDK | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

Pass-through endpoints for Bedrock - call provider-specific endpoint, in native format (no translation).

| Feature | Supported | Notes |
| --- | --- | --- |
| Cost Tracking | ✅ | For `/invoke` and `/converse` endpoints |
| Load Balancing | ✅ | You can load balance `/invoke`, `/converse` routes across multiple deployments |
| End-user Tracking | ❌ | [Tell us if you need this](https://github.com/BerriAI/litellm/issues/new) |
| Streaming | ✅ |  |

Just replace `https://bedrock-runtime.{aws_region_name}.amazonaws.com` with `LITELLM_PROXY_BASE_URL/bedrock` 🚀

## Overview[​](#overview "Direct link to Overview")

LiteLLM supports two ways to call Bedrock endpoints:

### 1. **Using config.yaml** (Recommended for model endpoints)[​](#1-using-configyaml-recommended-for-model-endpoints "Direct link to 1-using-configyaml-recommended-for-model-endpoints")

Define your Bedrock models in `config.yaml` and reference them by name. The proxy handles authentication and routing.

**Use for**: `/converse`, `/converse-stream`, `/invoke`, `/invoke-with-response-stream`

```
model_list:  
  - model_name: my-bedrock-model  
    litellm_params:  
      model: bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0  
      aws_region_name: us-west-2  
      custom_llm_provider: bedrock
```

```
curl -X POST 'http://0.0.0.0:4000/bedrock/model/my-bedrock-model/converse' \  
-H 'Authorization: Bearer sk-1234' \  
-H 'Content-Type: application/json' \  
-d '{"messages": [{"role": "user", "content": [{"text": "Hello"}]}]}'
```

### 2. **Direct passthrough** (For non-model endpoints)[​](#2-direct-passthrough-for-non-model-endpoints "Direct link to 2-direct-passthrough-for-non-model-endpoints")

Set AWS credentials via environment variables and call Bedrock endpoints directly.

**Use for**: Guardrails, Knowledge Bases, Agents, and other non-model endpoints

```
export AWS_ACCESS_KEY_ID=""  
export AWS_SECRET_ACCESS_KEY=""  
export AWS_REGION_NAME="us-west-2"
```

```
curl "http://0.0.0.0:4000/bedrock/guardrail/my-guardrail-id/version/1/apply" \  
-H 'Authorization: Bearer sk-1234' \  
-H 'Content-Type: application/json' \  
-d '{"contents": [{"text": {"text": "Hello"}}], "source": "INPUT"}'
```

Supports **ALL** Bedrock Endpoints (including streaming).

[**See All Bedrock Endpoints**](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)

## Quick Start[​](#quick-start "Direct link to Quick Start")

Let's call the Bedrock [`/converse` endpoint](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)

1. Create a `config.yaml` file with your Bedrock model

```
model_list:  
  - model_name: my-bedrock-model  
    litellm_params:  
      model: bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0  
      aws_region_name: us-west-2  
      custom_llm_provider: bedrock
```

Set your AWS credentials:

```
export AWS_ACCESS_KEY_ID=""  # Access key  
export AWS_SECRET_ACCESS_KEY="" # Secret access key
```

2. Start LiteLLM Proxy

```
litellm --config config.yaml  
  
# RUNNING on http://0.0.0.0:4000
```

3. Test it!

Let's call the Bedrock converse endpoint using the model name from config:

```
curl -X POST 'http://0.0.0.0:4000/bedrock/model/my-bedrock-model/converse' \  
-H 'Authorization: Bearer sk-1234' \  
-H 'Content-Type: application/json' \  
-d '{  
    "messages": [  
        {  
            "role": "user",  
            "content": [{"text": "Hello, how are you?"}]  
        }  
    ],  
    "inferenceConfig": {  
        "maxTokens": 100  
    }  
}'
```

## Setup with config.yaml[​](#setup-with-configyaml "Direct link to Setup with config.yaml")

Use config.yaml to define Bedrock models and use them via passthrough endpoints.

### 1. Define models in config.yaml[​](#1-define-models-in-configyaml "Direct link to 1. Define models in config.yaml")

```
model_list:  
  - model_name: my-claude-model  
    litellm_params:  
      model: bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0  
      aws_region_name: us-west-2  
      custom_llm_provider: bedrock  
    
  - model_name: my-cohere-model  
    litellm_params:  
      model: bedrock/cohere.command-r-v1:0  
      aws_region_name: us-east-1  
      custom_llm_provider: bedrock
```

### 2. Start proxy with config[​](#2-start-proxy-with-config "Direct link to 2. Start proxy with config")

```
litellm --config config.yaml  
  
# RUNNING on http://0.0.0.0:4000
```

### 3. Call Bedrock Converse endpoint[​](#3-call-bedrock-converse-endpoint "Direct link to 3. Call Bedrock Converse endpoint")

Use the `model_name` from config in the URL path:

```
curl -X POST 'http://0.0.0.0:4000/bedrock/model/my-claude-model/converse' \  
-H 'Authorization: Bearer sk-1234' \  
-H 'Content-Type: application/json' \  
-d '{  
    "messages": [  
        {  
            "role": "user",  
            "content": [{"text": "Hello, how are you?"}]  
        }  
    ],  
    "inferenceConfig": {  
        "temperature": 0.5,  
        "maxTokens": 100  
    }  
}'
```

### 4. Call Bedrock Converse Stream endpoint[​](#4-call-bedrock-converse-stream-endpoint "Direct link to 4. Call Bedrock Converse Stream endpoint")

For streaming responses, use the `/converse-stream` endpoint:

```
curl -X POST 'http://0.0.0.0:4000/bedrock/model/my-claude-model/converse-stream' \  
-H 'Authorization: Bearer sk-1234' \  
-H 'Content-Type: application/json' \  
-d '{  
    "messages": [  
        {  
            "role": "user",  
            "content": [{"text": "Tell me a short story"}]  
        }  
    ],  
    "inferenceConfig": {  
        "temperature": 0.7,  
        "maxTokens": 200  
    }  
}'
```

### Supported Bedrock Endpoints with config.yaml[​](#supported-bedrock-endpoints-with-configyaml "Direct link to Supported Bedrock Endpoints with config.yaml")

When using models from config.yaml, you can call any Bedrock endpoint:

| Endpoint | Description | Example |
| --- | --- | --- |
| `/model/{model_name}/converse` | Converse API | `http://0.0.0.0:4000/bedrock/model/my-claude-model/converse` |
| `/model/{model_name}/converse-stream` | Streaming Converse | `http://0.0.0.0:4000/bedrock/model/my-claude-model/converse-stream` |
| `/model/{model_name}/invoke` | Legacy Invoke API | `http://0.0.0.0:4000/bedrock/model/my-claude-model/invoke` |
| `/model/{model_name}/invoke-with-response-stream` | Legacy Streaming | `http://0.0.0.0:4000/bedrock/model/my-claude-model/invoke-with-response-stream` |

The proxy automatically resolves the `model_name` to the actual Bedrock model ID and region configured in your `config.yaml`.

### Load Balancing Across Multiple Deployments[​](#load-balancing-across-multiple-deployments "Direct link to Load Balancing Across Multiple Deployments")

Define multiple Bedrock deployments with the same `model_name` to enable automatic load balancing.

#### 1. Define multiple deployments in config.yaml[​](#1-define-multiple-deployments-in-configyaml "Direct link to 1. Define multiple deployments in config.yaml")

```
model_list:  
  # First deployment - us-west-2  
  - model_name: my-claude-model  
    litellm_params:  
      model: bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0  
      aws_region_name: us-west-2  
      custom_llm_provider: bedrock  
    
  # Second deployment - us-east-1 (load balanced)  
  - model_name: my-claude-model  
    litellm_params:  
      model: bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0  
      aws_region_name: us-east-1  
      custom_llm_provider: bedrock
```

#### 2. Start proxy with config[​](#2-start-proxy-with-config-1 "Direct link to 2. Start proxy with config")

```
litellm --config config.yaml  
  
# RUNNING on http://0.0.0.0:4000
```

#### 3. Call the endpoint - requests are automatically load balanced[​](#3-call-the-endpoint---requests-are-automatically-load-balanced "Direct link to 3. Call the endpoint - requests are automatically load balanced")

```
curl -X POST 'http://0.0.0.0:4000/bedrock/model/my-claude-model/invoke' \  
-H 'Authorization: Bearer sk-1234' \  
-H 'Content-Type: application/json' \  
-d '{  
    "max_tokens": 100,  
    "messages": [  
        {  
            "role": "user",  
            "content": "Hello, how are you?"  
        }  
    ],  
    "anthropic_version": "bedrock-2023-05-31"  
}'
```

The proxy will automatically distribute requests across both `us-west-2` and `us-east-1` deployments. This works for all Bedrock endpoints: `/invoke`, `/invoke-with-response-stream`, `/converse`, and `/converse-stream`.

#### Using boto3 SDK with load balancing[​](#using-boto3-sdk-with-load-balancing "Direct link to Using boto3 SDK with load balancing")

You can also call the load-balanced endpoint using the boto3 SDK:

```
import boto3  
import json  
import os  
  
# Set dummy AWS credentials (required by boto3, but not used by LiteLLM proxy)  
os.environ['AWS_ACCESS_KEY_ID'] = 'dummy'  
os.environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'  
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "sk-1234"  # your litellm proxy api key  
  
# Point boto3 to the LiteLLM proxy  
bedrock_runtime = boto3.client(  
    service_name='bedrock-runtime',  
    region_name='us-west-2',  
    endpoint_url='http://0.0.0.0:4000/bedrock'  
)  
  
# Call the load-balanced model  
response = bedrock_runtime.invoke_model(  
    modelId='my-claude-model',  # Your model_name from config.yaml  
    contentType='application/json',  
    accept='application/json',  
    body=json.dumps({  
        "max_tokens": 100,  
        "messages": [  
            {  
                "role": "user",  
                "content": "Hello, how are you?"  
            }  
        ],  
        "anthropic_version": "bedrock-2023-05-31"  
    })  
)  
  
# Parse response  
response_body = json.loads(response['body'].read())  
print(response_body['content'][0]['text'])
```

The proxy will automatically load balance your boto3 requests across all configured deployments.

## Examples[​](#examples "Direct link to Examples")

Anything after `http://0.0.0.0:4000/bedrock` is treated as a provider-specific route, and handled accordingly.

Key Changes:

| **Original Endpoint** | **Replace With** |
| --- | --- |
| `https://bedrock-runtime.{aws_region_name}.amazonaws.com` | `http://0.0.0.0:4000/bedrock` (LITELLM\_PROXY\_BASE\_URL="<http://0.0.0.0:4000>") |
| `AWS4-HMAC-SHA256..` | `Bearer anything` (use `Bearer LITELLM_VIRTUAL_KEY` if Virtual Keys are setup on proxy) |

### **Example 1: Converse API**[​](#example-1-converse-api "Direct link to example-1-converse-api")

#### LiteLLM Proxy Call[​](#litellm-proxy-call "Direct link to LiteLLM Proxy Call")

```
curl -X POST 'http://0.0.0.0:4000/bedrock/model/cohere.command-r-v1:0/converse' \  
-H 'Authorization: Bearer sk-anything' \  
-H 'Content-Type: application/json' \  
-d '{  
    "messages": [  
         {"role": "user",  
        "content": [{"text": "Hello"}]  
    }  
    ]  
}'
```

#### Direct Bedrock API Call[​](#direct-bedrock-api-call "Direct link to Direct Bedrock API Call")

```
curl -X POST 'https://bedrock-runtime.us-west-2.amazonaws.com/model/cohere.command-r-v1:0/converse' \  
-H 'Authorization: AWS4-HMAC-SHA256..' \  
-H 'Content-Type: application/json' \  
-d '{  
    "messages": [  
         {"role": "user",  
        "content": [{"text": "Hello"}]  
    }  
    ]  
}'
```

### **Example 2: Apply Guardrail**[​](#example-2-apply-guardrail "Direct link to example-2-apply-guardrail")

**Setup**: Set AWS credentials for direct passthrough

```
export AWS_ACCESS_KEY_ID="your-access-key"  
export AWS_SECRET_ACCESS_KEY="your-secret-key"  
export AWS_REGION_NAME="us-west-2"
```

Start proxy:

```
litellm  
  
# RUNNING on http://0.0.0.0:4000
```

#### LiteLLM Proxy Call[​](#litellm-proxy-call-1 "Direct link to LiteLLM Proxy Call")

```
curl "http://0.0.0.0:4000/bedrock/guardrail/guardrailIdentifier/version/guardrailVersion/apply" \  
    -H 'Authorization: Bearer sk-anything' \  
    -H 'Content-Type: application/json' \  
    -X POST \  
    -d '{  
      "contents": [{"text": {"text": "Hello world"}}],  
      "source": "INPUT"  
       }'
```

#### Direct Bedrock API Call[​](#direct-bedrock-api-call-1 "Direct link to Direct Bedrock API Call")

```
curl "https://bedrock-runtime.us-west-2.amazonaws.com/guardrail/guardrailIdentifier/version/guardrailVersion/apply" \  
    -H 'Authorization: AWS4-HMAC-SHA256..' \  
    -H 'Content-Type: application/json' \  
    -X POST \  
    -d '{  
      "contents": [{"text": {"text": "Hello world"}}],  
      "source": "INPUT"  
       }'
```

### **Example 3: Query Knowledge Base**[​](#example-3-query-knowledge-base "Direct link to example-3-query-knowledge-base")

**Setup**: Set AWS credentials for direct passthrough

```
export AWS_ACCESS_KEY_ID="your-access-key"  
export AWS_SECRET_ACCESS_KEY="your-secret-key"  
export AWS_REGION_NAME="us-west-2"
```

Start proxy:

```
litellm  
  
# RUNNING on http://0.0.0.0:4000
```

#### LiteLLM Proxy Call[​](#litellm-proxy-call-2 "Direct link to LiteLLM Proxy Call")

```
curl -X POST "http://0.0.0.0:4000/bedrock/knowledgebases/{knowledgeBaseId}/retrieve" \  
-H 'Authorization: Bearer sk-anything' \  
-H 'Content-Type: application/json' \  
-d '{  
    "nextToken": "string",  
    "retrievalConfiguration": {   
        "vectorSearchConfiguration": {   
          "filter": { ... },  
          "numberOfResults": number,  
          "overrideSearchType": "string"  
        }  
    },  
    "retrievalQuery": {   
        "text": "string"  
    }  
}'
```

#### Direct Bedrock API Call[​](#direct-bedrock-api-call-2 "Direct link to Direct Bedrock API Call")

```
curl -X POST "https://bedrock-agent-runtime.us-west-2.amazonaws.com/knowledgebases/{knowledgeBaseId}/retrieve" \  
-H 'Authorization: AWS4-HMAC-SHA256..' \  
-H 'Content-Type: application/json' \  
-d '{  
    "nextToken": "string",  
    "retrievalConfiguration": {   
        "vectorSearchConfiguration": {   
          "filter": { ... },  
          "numberOfResults": number,  
          "overrideSearchType": "string"  
        }  
    },  
    "retrievalQuery": {   
        "text": "string"  
    }  
}'
```

## Advanced - Use with Virtual Keys[​](#advanced---use-with-virtual-keys "Direct link to Advanced - Use with Virtual Keys")

Pre-requisites

* [Setup proxy with DB](/docs/proxy/virtual_keys#setup)

Use this, to avoid giving developers the raw AWS Keys, but still letting them use AWS Bedrock endpoints.

### Usage[​](#usage "Direct link to Usage")

1. Setup environment

```
export DATABASE_URL=""  
export LITELLM_MASTER_KEY=""  
export AWS_ACCESS_KEY_ID=""  # Access key  
export AWS_SECRET_ACCESS_KEY="" # Secret access key  
export AWS_REGION_NAME="" # us-east-1, us-east-2, us-west-1, us-west-2
```

```
litellm  
  
# RUNNING on http://0.0.0.0:4000
```

2. Generate virtual key

```
curl -X POST 'http://0.0.0.0:4000/key/generate' \  
-H 'Authorization: Bearer sk-1234' \  
-H 'Content-Type: application/json' \  
-d '{}'
```

Expected Response

```
{  
    ...  
    "key": "sk-1234ewknldferwedojwojw"  
}
```

3. Test it!

```
curl -X POST 'http://0.0.0.0:4000/bedrock/model/cohere.command-r-v1:0/converse' \  
-H 'Authorization: Bearer sk-1234ewknldferwedojwojw' \  
-H 'Content-Type: application/json' \  
-d '{  
    "messages": [  
         {"role": "user",  
        "content": [{"text": "Hello"}]  
    }  
    ]  
}'
```

## Advanced - Bedrock Agents[​](#advanced---bedrock-agents "Direct link to Advanced - Bedrock Agents")

Call Bedrock Agents via LiteLLM proxy

**Setup**: Set AWS credentials on your LiteLLM proxy server

```
export AWS_ACCESS_KEY_ID="your-access-key"  
export AWS_SECRET_ACCESS_KEY="your-secret-key"  
export AWS_REGION_NAME="us-west-2"
```

Start proxy:

```
litellm  
  
# RUNNING on http://0.0.0.0:4000
```

**Usage from Python**:

```
import os   
import boto3  
  
# Set dummy AWS credentials (required by boto3, but not used by LiteLLM proxy)  
os.environ["AWS_ACCESS_KEY_ID"] = "dummy"  
os.environ["AWS_SECRET_ACCESS_KEY"] = "dummy"  
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = "sk-1234"  # your litellm proxy api key  
  
# Create the client  
runtime_client = boto3.client(  
    service_name="bedrock-agent-runtime",   
    region_name="us-west-2",   
    endpoint_url="http://0.0.0.0:4000/bedrock"  
)  
  
response = runtime_client.invoke_agent(  
    agentId="L1RT58GYRW",  
    agentAliasId="MFPSBCXYTW",  
    sessionId="12345",  
    inputText="Who do you know?"  
)  
  
completion = ""  
  
for event in response.get("completion"):  
    chunk = event["chunk"]  
    completion += chunk["bytes"].decode()  
  
print(completion)
```

* [Overview](#overview)
  + [1. **Using config.yaml** (Recommended for model endpoints)](#1-using-configyaml-recommended-for-model-endpoints)
  + [2. **Direct passthrough** (For non-model endpoints)](#2-direct-passthrough-for-non-model-endpoints)
* [Quick Start](#quick-start)
* [Setup with config.yaml](#setup-with-configyaml)
  + [1. Define models in config.yaml](#1-define-models-in-configyaml)
  + [2. Start proxy with config](#2-start-proxy-with-config)
  + [3. Call Bedrock Converse endpoint](#3-call-bedrock-converse-endpoint)
  + [4. Call Bedrock Converse Stream endpoint](#4-call-bedrock-converse-stream-endpoint)
  + [Supported Bedrock Endpoints with config.yaml](#supported-bedrock-endpoints-with-configyaml)
  + [Load Balancing Across Multiple Deployments](#load-balancing-across-multiple-deployments)
* [Examples](#examples)
  + [**Example 1: Converse API**](#example-1-converse-api)
  + [**Example 2: Apply Guardrail**](#example-2-apply-guardrail)
  + [**Example 3: Query Knowledge Base**](#example-3-query-knowledge-base)
* [Advanced - Use with Virtual Keys](#advanced---use-with-virtual-keys)
  + [Usage](#usage)
* [Advanced - Bedrock Agents](#advanced---bedrock-agents)