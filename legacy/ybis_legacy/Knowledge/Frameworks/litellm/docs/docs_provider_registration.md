Integrate as a Model Provider | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

## Quick Start for OpenAI-Compatible Providers[​](#quick-start-for-openai-compatible-providers "Direct link to Quick Start for OpenAI-Compatible Providers")

If your API is OpenAI-compatible, you can add support by editing a single JSON file. See [Adding OpenAI-Compatible Providers](/docs/contributing/adding_openai_compatible_providers) for the simple approach.

---

This guide focuses on how to setup the classes and configuration necessary to act as a chat provider.

Please see this guide first and look at the existing code in the codebase to understand how to act as a different provider, e.g. handling embeddings or image-generation.

---

### Overview[​](#overview "Direct link to Overview")

The way liteLLM works from a provider's perspective is simple.

liteLLM acts as a wrapper, it takes openai requests and routes them to your api. It then adapts your output into a standard output.

To integrate as a provider, you need to write a module that slots in the api and acts as an adapter between the liteLLM API and your API.

The module you will be writing acts as both a config and a means to adapt requests and responses.

Your objective is to effectively write this module so that it adapts inputs to your api, and adapts outputs to the calling liteLLM code.

It includes methods that:

* Validate the request
* Transform (adapt) the requests into requests sent to your api
* Transform (adapt) responses from your api into responses given back to the calling liteLLM code
* + a few others

---

### 1. Create Your Config Class[​](#1-create-your-config-class "Direct link to 1. Create Your Config Class")

Create a new directory with your provider name

#### `litellm/llms/your_provider_name_here`[​](#litellmllmsyour_provider_name_here "Direct link to litellmllmsyour_provider_name_here")

Inside of there, you will want to add a file for your chat configuration

#### `litellm/llms/your_provider_name_here/chat/transformation.py`[​](#litellmllmsyour_provider_name_herechattransformationpy "Direct link to litellmllmsyour_provider_name_herechattransformationpy")

The `transformation.py` file will contain a configuration class that dictates how your api will slot into the liteLLM api.

Define your config class extending `BaseConfig`:

```
from litellm.llms.base_llm.chat.transformation import BaseConfig  
  
class MyProviderChatConfig(BaseConfig):  
    def __init__(self):  
        ...
```

We will fill in the abstract methods at a later point.

---

### 2. Add Yourself To Various Places In The Code Base[​](#2-add-yourself-to-various-places-in-the-code-base "Direct link to 2. Add Yourself To Various Places In The Code Base")

liteLLM is working to enhance this process, but currently, what you need to do is the following:

#### `litellm/__init__.py`[​](#litellm__init__py "Direct link to litellm__init__py")

At the top part of the file, add your key to the list of keys as an option

```
azure_key: Optional[str] = None  
anthropic_key: Optional[str] = None  
replicate_key: Optional[str] = None  
bytez_key: Optional[str] = None  
cohere_key: Optional[str] = None  
infinity_key: Optional[str] = None  
clarifai_key: Optional[str] = None
```

Import your config

```
from .llms.bytez.chat.transformation import BytezChatConfig  
from .llms.custom_llm import CustomLLM  
from .llms.bedrock.chat.converse_transformation import AmazonConverseConfig  
from .llms.openai_like.chat.handler import OpenAILikeChatConfig
```

#### `litellm/main.py`[​](#litellmmainpy "Direct link to litellmmainpy")

Add yourself to `main.py` so requests can be routed to your config class

```
from .llms.bedrock.chat import BedrockConverseLLM, BedrockLLM  
from .llms.bedrock.embed.embedding import BedrockEmbedding  
from .llms.bedrock.image.image_handler import BedrockImageGeneration  
from .llms.bytez.chat.transformation import BytezChatConfig  
from .llms.codestral.completion.handler import CodestralTextCompletion  
from .llms.cohere.embed import handler as cohere_embed  
from .llms.custom_httpx.aiohttp_handler import BaseLLMAIOHTTPHandler  
  
base_llm_http_handler = BaseLLMHTTPHandler()  
base_llm_aiohttp_handler = BaseLLMAIOHTTPHandler()  
sagemaker_chat_completion = SagemakerChatHandler()  
bytez_transformation = BytezChatConfig()
```

Then much lower in the code

```
elif custom_llm_provider == "bytez":  
    api_key = (  
        api_key  
        or litellm.bytez_key  
        or get_secret_str("BYTEZ_API_KEY")  
        or litellm.api_key  
    )  
  
    response = base_llm_http_handler.completion(  
        model=model,  
        messages=messages,  
        headers=headers,  
        model_response=model_response,  
        api_key=api_key,  
        api_base=api_base,  
        acompletion=acompletion,  
        logging_obj=logging,  
        optional_params=optional_params,  
        litellm_params=litellm_params,  
        timeout=timeout,  # type: ignore  
        client=client,  
        custom_llm_provider=custom_llm_provider,  
        encoding=encoding,  
        stream=stream,  
    )  
  
    pass
```

NOTE you can rely on liteLLM passing each of the args/kwargs to your config via the .completion() call

#### `litellm/constants.py`[​](#litellmconstantspy "Direct link to litellmconstantspy")

Add yourself to the list of `LITELLM_CHAT_PROVIDERS`

```
LITELLM_CHAT_PROVIDERS = [  
    "openai",  
    "openai_like",  
    "bytez",  
    "xai",  
    "custom_openai",  
    "text-completion-openai",
```

Add yourself to the if statement chain of providers here

#### `litellm/litellm_core_utils/get_llm_provider_logic.py`[​](#litellmlitellm_core_utilsget_llm_provider_logicpy "Direct link to litellmlitellm_core_utilsget_llm_provider_logicpy")

```
elif model == "*":  
    custom_llm_provider = "openai"  
# bytez models  
elif model.startswith("bytez/"):  
    custom_llm_provider = "bytez"  
if not custom_llm_provider:  
    if litellm.suppress_debug_info is False:  
        print()  # noqa
```

#### `litellm/litellm_core_utils/streaming_handler.py`[​](#litellmlitellm_core_utilsstreaming_handlerpy "Direct link to litellmlitellm_core_utilsstreaming_handlerpy")

#### If you are doing something custom with streaming, this needs to be updated, e.g.[​](#if-you-are-doing-something-custom-with-streaming-this-needs-to-be-updated-eg "Direct link to If you are doing something custom with streaming, this needs to be updated, e.g.")

```
    def handle_bytez_chunk(self, chunk):  
        try:  
            is_finished = False  
            finish_reason = ""  
  
            return {  
                "text": chunk,  
                "is_finished": is_finished,  
                "finish_reason": finish_reason,  
            }  
        except Exception as e:  
            raise e
```

Then lower in the file

```
elif self.custom_llm_provider and self.custom_llm_provider == "bytez":  
    response_obj = self.handle_bytez_chunk(chunk)  
    completion_obj["content"] = response_obj["text"]  
    if response_obj["is_finished"]:  
        self.received_finish_reason = response_obj["finish_reason"]  
    pass
```

---

### 3. Write a test file to iterate your code[​](#3-write-a-test-file-to-iterate-your-code "Direct link to 3. Write a test file to iterate your code")

Add a test file somewhere in the project, `tests/test_litellm/llms/my_provider/chat/test.py`

Write to it the following:

```
import os  
from litellm import completion  
  
os.environ["MY_PROVIDER_KEY"] = "KEY_GOES_HERE"  
  
completion(model="my_provider/your-model", messages=[...], api_key="...")
```

If you want to run it with the vscode debugger you can do so with this config file (recommended)

`.vscode/launch.json`

```
{  
  // Use IntelliSense to learn about possible attributes.  
  // Hover to view descriptions of existing attributes.  
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387  
  "version": "0.2.0",  
  "configurations": [  
    {  
      "name": "Python Debugger: Current File",  
      "type": "debugpy",  
      "request": "launch",  
      "program": "${file}",  
      "console": "integratedTerminal",  
      "env": {  
        "PYTHONPATH": "${workspaceFolder}",  
        "MY_PROVIDER_API_KEY": "YOUR_API_KEY"  
      }  
    }  
  ]  
}
```

If you run with the debugger, after you update `"MY_PROVIDER_API_KEY": "YOUR_API_KEY"` you can remove this from the test script:

`os.environ["MY_PROVIDER_KEY"] = "KEY_GOES_HERE"`

---

### 4. Implement Required Methods[​](#4-implement-required-methods "Direct link to 4. Implement Required Methods")

It's wise to follow `completion()` in `litellm/llms/custom_httpx/llm_http_handler.py`

You will see it calls each of the methods defined in the base class.

The debugger is your friend.

###### `validate_environment`[​](#validate_environment "Direct link to validate_environment")

Setup headers, validate key/model:

```
def validate_environment(...):  
    headers.update({  
        "Authorization": f"Bearer {api_key}",  
        "Content-Type": "application/json"  
    })  
    return headers
```

###### `get_complete_url`[​](#get_complete_url "Direct link to get_complete_url")

Return the final request URL:

```
def get_complete_url(...):  
    return f"{api_base}/{model}"
```

###### `transform_request`[​](#transform_request "Direct link to transform_request")

Adapt OpenAI-style input into provider-specific format:

```
def transform_request(...):  
    data = {"messages": messages, "params": optional_params}  
    return data
```

###### `transform_response`[​](#transform_response "Direct link to transform_response")

Process and map the raw provider response:

```
def transform_response(...):  
    json = raw_response.json()  
    model_response.model = model  
    model_response.choices[0].message.content = json.get("output")  
    return model_response
```

###### `get_sync_custom_stream_wrapper` / `get_async_custom_stream_wrapper`[​](#get_sync_custom_stream_wrapper--get_async_custom_stream_wrapper "Direct link to get_sync_custom_stream_wrapper--get_async_custom_stream_wrapper")

If you need to do something these are here for you. See the `litellm/llms/sagemaker/chat/transformation.py` or the `litellm/llms/bytez/chat/transformation.py` implementation to better understand how to use these.

Use `CustomStreamWrapper` + `httpx` streaming client to yield content.

---

### 🧪 Tests[​](#-tests "Direct link to 🧪 Tests")

Create tests in `tests/test_litellm/llms/my_provider/chat/test.py`. Iterate until you are satisfied with the quality!

---

### Spare thoughts[​](#spare-thoughts "Direct link to Spare thoughts")

If you get stuck, see the other provider implementations, `ctrl + shift + f` and `ctrl + p` are your friends!

You can also visit the [discord feedback channel](https://discord.gg/wuPM9dRgDw)

* [Quick Start for OpenAI-Compatible Providers](#quick-start-for-openai-compatible-providers)
  + [Overview](#overview)
  + [1. Create Your Config Class](#1-create-your-config-class)
  + [2. Add Yourself To Various Places In The Code Base](#2-add-yourself-to-various-places-in-the-code-base)
  + [3. Write a test file to iterate your code](#3-write-a-test-file-to-iterate-your-code)
  + [4. Implement Required Methods](#4-implement-required-methods)
  + [🧪 Tests](#-tests)
  + [Spare thoughts](#spare-thoughts)