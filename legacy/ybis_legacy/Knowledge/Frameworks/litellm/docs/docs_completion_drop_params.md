Drop Unsupported Params | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

Drop unsupported OpenAI params by your LLM Provider.

## Default Behavior[​](#default-behavior "Direct link to Default Behavior")

**By default, LiteLLM raises an exception** if you send a parameter to a model that doesn't support it.

For example, if you send `temperature=0.2` to a model that doesn't support the `temperature` parameter, LiteLLM will raise an exception.

**When `drop_params=True` is set**, LiteLLM will drop the unsupported parameter instead of raising an exception. This allows your code to work seamlessly across different providers without having to customize parameters for each one.

## Quick Start[​](#quick-start "Direct link to Quick Start")

```
import litellm   
import os   
  
# set keys   
os.environ["COHERE_API_KEY"] = "co-.."  
  
litellm.drop_params = True # 👈 KEY CHANGE  
  
response = litellm.completion(  
                model="command-r",  
                messages=[{"role": "user", "content": "Hey, how's it going?"}],  
                response_format={"key": "value"},  
            )
```

LiteLLM maps all supported openai params by provider + model (e.g. function calling is supported by anthropic on bedrock but not titan).

See `litellm.get_supported_openai_params("command-r")` [**Code**](https://github.com/BerriAI/litellm/blob/main/litellm/utils.py#L3584)

If a provider/model doesn't support a particular param, you can drop it.

## OpenAI Proxy Usage[​](#openai-proxy-usage "Direct link to OpenAI Proxy Usage")

```
litellm_settings:  
    drop_params: true
```

## Pass drop\_params in `completion(..)`[​](#pass-drop_params-in-completion "Direct link to pass-drop_params-in-completion")

Just drop\_params when calling specific models

* SDK
* PROXY

```
import litellm   
import os   
  
# set keys   
os.environ["COHERE_API_KEY"] = "co-.."  
  
response = litellm.completion(  
                model="command-r",  
                messages=[{"role": "user", "content": "Hey, how's it going?"}],  
                response_format={"key": "value"},  
                drop_params=True  
            )
```

```
- litellm_params:  
    api_base: my-base  
    model: openai/my-model  
    drop_params: true # 👈 KEY CHANGE  
  model_name: my-model
```

## Specify params to drop[​](#specify-params-to-drop "Direct link to Specify params to drop")

To drop specific params when calling a provider (E.g. 'logit\_bias' for vllm)

Use `additional_drop_params`

* SDK
* PROXY

```
import litellm   
import os   
  
# set keys   
os.environ["COHERE_API_KEY"] = "co-.."  
  
response = litellm.completion(  
                model="command-r",  
                messages=[{"role": "user", "content": "Hey, how's it going?"}],  
                response_format={"key": "value"},  
                additional_drop_params=["response_format"]  
            )
```

```
- litellm_params:  
    api_base: my-base  
    model: openai/my-model  
    additional_drop_params: ["response_format"] # 👈 KEY CHANGE  
  model_name: my-model
```

**additional\_drop\_params**: List or null - Is a list of openai params you want to drop when making a call to the model.

### Nested Field Removal[​](#nested-field-removal "Direct link to Nested Field Removal")

Drop nested fields within complex objects using JSONPath-like notation:

* SDK
* PROXY

```
import litellm  
  
response = litellm.completion(  
    model="bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0",  
    messages=[{"role": "user", "content": "Hello"}],  
    tools=[{  
        "name": "search",  
        "description": "Search files",  
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},  
        "input_examples": [{"query": "test"}]  # Will be removed  
    }],  
    additional_drop_params=["tools[*].input_examples"]  # Remove from all tools  
)
```

```
model_list:  
  - model_name: my-bedrock-model  
    litellm_params:  
      model: bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0  
      additional_drop_params: ["tools[*].input_examples"]  # Remove from all tools
```

**Supported syntax:**

* `field` - Top-level field
* `parent.child` - Nested object field
* `array[*]` - All array elements
* `array[0]` - Specific array index
* `tools[*].input_examples` - Field in all array elements
* `tools[0].metadata.field` - Specific index + nested field

**Example use cases:**

* Remove `input_examples` from tool definitions (Claude Code + AWS Bedrock)
* Drop provider-specific fields from nested structures
* Clean up nested parameters before sending to LLM

## Specify allowed openai params in a request[​](#specify-allowed-openai-params-in-a-request "Direct link to Specify allowed openai params in a request")

Tell litellm to allow specific openai params in a request. Use this if you get a `litellm.UnsupportedParamsError` and want to allow a param. LiteLLM will pass the param as is to the model.

* LiteLLM Python SDK
* LiteLLM Proxy

In this example we pass `allowed_openai_params=["tools"]` to allow the `tools` param.

Pass allowed\_openai\_params to LiteLLM Python SDK

```
await litellm.acompletion(  
    model="azure/o_series/<my-deployment-name>",  
    api_key="xxxxx",  
    api_base=api_base,  
    messages=[{"role": "user", "content": "Hello! return a json object"}],  
    tools=[{"type": "function", "function": {"name": "get_current_time", "description": "Get the current time in a given location.", "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "The city name, e.g. San Francisco"}}, "required": ["location"]}}}]  
    allowed_openai_params=["tools"],  
)
```

When using litellm proxy you can pass `allowed_openai_params` in two ways:

1. Dynamically pass `allowed_openai_params` in a request
2. Set `allowed_openai_params` on the config.yaml file for a specific model

#### Dynamically pass allowed\_openai\_params in a request[​](#dynamically-pass-allowed_openai_params-in-a-request "Direct link to Dynamically pass allowed_openai_params in a request")

In this example we pass `allowed_openai_params=["tools"]` to allow the `tools` param for a request sent to the model set on the proxy.

Dynamically pass allowed\_openai\_params in a request

```
import openai  
from openai import AsyncAzureOpenAI  
  
import openai  
client = openai.OpenAI(  
    api_key="anything",  
    base_url="http://0.0.0.0:4000"  
)  
  
response = client.chat.completions.create(  
    model="gpt-3.5-turbo",  
    messages = [  
        {  
            "role": "user",  
            "content": "this is a test request, write a short poem"  
        }  
    ],  
    extra_body={   
        "allowed_openai_params": ["tools"]  
    }  
)
```

#### Set allowed\_openai\_params on config.yaml[​](#set-allowed_openai_params-on-configyaml "Direct link to Set allowed_openai_params on config.yaml")

You can also set `allowed_openai_params` on the config.yaml file for a specific model. This means that all requests to this deployment are allowed to pass in the `tools` param.

Set allowed\_openai\_params on config.yaml

```
model_list:  
  - model_name: azure-o1-preview  
    litellm_params:  
      model: azure/o_series/<my-deployment-name>  
      api_key: xxxxx  
      api_base: https://openai-prod-test.openai.azure.com/openai/deployments/o1/chat/completions?api-version=2025-01-01-preview  
      allowed_openai_params: ["tools"]
```

* [Default Behavior](#default-behavior)
* [Quick Start](#quick-start)
* [OpenAI Proxy Usage](#openai-proxy-usage)
* [Pass drop\_params in `completion(..)`](#pass-drop_params-in-completion)
* [Specify params to drop](#specify-params-to-drop)
  + [Nested Field Removal](#nested-field-removal)
* [Specify allowed openai params in a request](#specify-allowed-openai-params-in-a-request)