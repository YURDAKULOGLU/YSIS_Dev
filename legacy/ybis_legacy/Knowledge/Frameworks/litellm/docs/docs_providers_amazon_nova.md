Amazon Nova | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

| Property | Details |
| --- | --- |
| Description | Amazon Nova is a family of foundation models built by Amazon that deliver frontier intelligence and industry-leading price performance. |
| Provider Route on LiteLLM | `amazon_nova/` |
| Provider Doc | [Amazon Nova ↗](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html) |
| Supported OpenAI Endpoints | `/chat/completions`, `v1/responses` |
| Other Supported Endpoints | `v1/messages`, `/generateContent` |

## Authentication[​](#authentication "Direct link to Authentication")

Amazon Nova uses API key authentication. You can obtain your API key from the [Amazon Nova developer console ↗](https://nova.amazon.com/dev/documentation).

```
export AMAZON_NOVA_API_KEY="your-api-key"
```

## Usage[​](#usage "Direct link to Usage")

* SDK
* PROXY

```
import os  
from litellm import completion  
  
# Set your API key  
os.environ["AMAZON_NOVA_API_KEY"] = "your-api-key"  
  
response = completion(  
    model="amazon_nova/nova-micro-v1",  
    messages=[  
        {"role": "system", "content": "You are a helpful assistant"},  
        {"role": "user", "content": "Hello, how are you?"}  
    ]  
)  
  
print(response)
```

### 1. Setup config.yaml[​](#1-setup-configyaml "Direct link to 1. Setup config.yaml")

```
model_list:  
  - model_name: amazon-nova-micro  
    litellm_params:  
      model: amazon_nova/nova-micro-v1  
      api_key: os.environ/AMAZON_NOVA_API_KEY
```

### 2. Start the proxy[​](#2-start-the-proxy "Direct link to 2. Start the proxy")

```
litellm --config /path/to/config.yaml
```

### 3. Test it[​](#3-test-it "Direct link to 3. Test it")

```
curl --location 'http://0.0.0.0:4000/chat/completions' \  
--header 'Content-Type: application/json' \  
--data '{  
    "model": "amazon-nova-micro",  
    "messages": [  
        {  
            "role": "user",  
            "content": "Hello, how are you?"  
        }  
    ]  
}'
```

## Supported Models[​](#supported-models "Direct link to Supported Models")

| Model Name | Usage | Context Window |
| --- | --- | --- |
| Nova Micro | `completion(model="amazon_nova/nova-micro-v1", messages=messages)` | 128K tokens |
| Nova Lite | `completion(model="amazon_nova/nova-lite-v1", messages=messages)` | 300K tokens |
| Nova Pro | `completion(model="amazon_nova/nova-pro-v1", messages=messages)` | 300K tokens |
| Nova Premier | `completion(model="amazon_nova/nova-premier-v1", messages=messages)` | 1M tokens |

## Usage - Streaming[​](#usage---streaming "Direct link to Usage - Streaming")

* SDK
* PROXY

```
import os  
from litellm import completion  
  
os.environ["AMAZON_NOVA_API_KEY"] = "your-api-key"  
  
response = completion(  
    model="amazon_nova/nova-micro-v1",  
    messages=[  
        {"role": "system", "content": "You are a helpful assistant"},  
        {"role": "user", "content": "Tell me about machine learning"}  
    ],  
    stream=True  
)  
  
for chunk in response:  
    print(chunk.choices[0].delta.content or "", end="")
```

```
curl --location 'http://0.0.0.0:4000/chat/completions' \  
--header 'Content-Type: application/json' \  
--data '{  
    "model": "amazon-nova-micro",  
    "messages": [  
        {  
            "role": "user",  
            "content": "Tell me about machine learning"  
        }  
    ],  
    "stream": true  
}'
```

## Usage - Function Calling / Tool Usage[​](#usage---function-calling--tool-usage "Direct link to Usage - Function Calling / Tool Usage")

* SDK
* PROXY

```
import os  
from litellm import completion  
  
os.environ["AMAZON_NOVA_API_KEY"] = "your-api-key"  
  
tools = [  
    {  
        "type": "function",  
        "function": {  
            "name": "getCurrentWeather",  
            "description": "Get the current weather in a given city",  
            "parameters": {  
                "type": "object",  
                "properties": {  
                    "location": {  
                        "type": "string",  
                        "description": "City and country e.g. San Francisco, CA"  
                    }  
                },  
                "required": ["location"]  
            }  
        }  
    }  
]  
  
response = completion(  
    model="amazon_nova/nova-micro-v1",  
    messages=[  
        {"role": "user", "content": "What's the weather like in San Francisco?"}  
    ],  
    tools=tools  
)  
  
print(response)
```

```
curl --location 'http://0.0.0.0:4000/chat/completions' \  
--header 'Content-Type: application/json' \  
--data '{  
    "model": "amazon-nova-micro",  
    "messages": [  
        {  
            "role": "user",  
            "content": "What'\''s the weather like in San Francisco?"  
        }  
    ],  
    "tools": [  
        {  
            "type": "function",  
            "function": {  
                "name": "getCurrentWeather",  
                "description": "Get the current weather in a given city",  
                "parameters": {  
                    "type": "object",  
                    "properties": {  
                        "location": {  
                            "type": "string",  
                            "description": "City and country e.g. San Francisco, CA"  
                        }  
                    },  
                    "required": ["location"]  
                }  
            }  
        }  
    ]  
}'
```

## Set temperature, top\_p, etc.[​](#set-temperature-top_p-etc "Direct link to Set temperature, top_p, etc.")

* SDK
* PROXY

```
import os  
from litellm import completion  
  
os.environ["AMAZON_NOVA_API_KEY"] = "your-api-key"  
  
response = completion(  
    model="amazon_nova/nova-pro-v1",  
    messages=[  
        {"role": "user", "content": "Write a creative story"}  
    ],  
    temperature=0.8,  
    max_tokens=500,  
    top_p=0.9  
)  
  
print(response)
```

**Set on yaml**

```
model_list:  
  - model_name: amazon-nova-pro  
    litellm_params:  
      model: amazon_nova/nova-pro-v1  
      temperature: 0.8  
      max_tokens: 500  
      top_p: 0.9
```

**Set on request**

```
curl --location 'http://0.0.0.0:4000/chat/completions' \  
--header 'Content-Type: application/json' \  
--data '{  
    "model": "amazon-nova-pro",  
    "messages": [  
        {  
            "role": "user",  
            "content": "Write a creative story"  
        }  
    ],  
    "temperature": 0.8,  
    "max_tokens": 500,  
    "top_p": 0.9  
}'
```

## Model Comparison[​](#model-comparison "Direct link to Model Comparison")

| Model | Best For | Speed | Cost | Context |
| --- | --- | --- | --- | --- |
| **Nova Micro** | Simple tasks, high throughput | Fastest | Lowest | 128K |
| **Nova Lite** | Balanced performance | Fast | Low | 300K |
| **Nova Pro** | Complex reasoning | Medium | Medium | 300K |
| **Nova Premier** | Most advanced tasks | Slower | Higher | 1M |

## Error Handling[​](#error-handling "Direct link to Error Handling")

Common error codes and their meanings:

* `401 Unauthorized`: Invalid API key
* `429 Too Many Requests`: Rate limit exceeded
* `400 Bad Request`: Invalid request format
* `500 Internal Server Error`: Service temporarily unavailable

* [Authentication](#authentication)
* [Usage](#usage)
  + [1. Setup config.yaml](#1-setup-configyaml)
  + [2. Start the proxy](#2-start-the-proxy)
  + [3. Test it](#3-test-it)
* [Supported Models](#supported-models)
* [Usage - Streaming](#usage---streaming)
* [Usage - Function Calling / Tool Usage](#usage---function-calling--tool-usage)
* [Set temperature, top\_p, etc.](#set-temperature-top_p-etc)
* [Model Comparison](#model-comparison)
* [Error Handling](#error-handling)