How Model Access Works | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

## Concept[​](#concept "Direct link to Concept")

Each model onboarded is a "model deployment" in LiteLLM.

These model deployments are assigned to a "model group", via the "model\_name" field in the config.yaml.

## Example[​](#example "Direct link to Example")

```
model_list:  
  - model_name: my-custom-model  
    litellm_params:  
      model: openai/gpt-4o  
      api_key: os.environ/OPENAI_API_KEY
```

In here, we onboard a model deployment for the model `gpt-4o` and assign it to the model group `my-custom-model`.

## Client-side request[​](#client-side-request "Direct link to Client-side request")

Here's what a client-side request looks like:

```
curl --location 'http://localhost:4000/chat/completions' \  
-H 'Authorization: Bearer <your-api-key>' \  
-H 'Content-Type: application/json' \  
-d '{"model": "my-custom-model", "messages": [{"role": "user", "content": "Hello, how are you?"}]}'
```

## Access Control[​](#access-control "Direct link to Access Control")

When you give access to a key/user/team, you are giving them access to a "model group".

Example:

```
curl --location 'http://localhost:4000/key/generate' \  
--header 'Authorization: Bearer <your-master-key>' \  
--header 'Content-Type: application/json' \  
--data-raw '{"models": ["my-custom-model"]}'
```

## Loadbalancing[​](#loadbalancing "Direct link to Loadbalancing")

You can add multiple model deployments to a single "model group". LiteLLM will automatically load balance requests across the model deployments in the group.

Example:

```
model_list:  
  - model_name: my-custom-model  
    litellm_params:  
      model: openai/gpt-4o  
      api_key: os.environ/OPENAI_API_KEY  
  - model_name: my-custom-model  
    litellm_params:  
      model: azure/gpt-4o  
      api_key: os.environ/AZURE_API_KEY  
      api_base: os.environ/AZURE_API_BASE  
      api_version: os.environ/AZURE_API_VERSION
```

This way, you can maximize your rate limits across multiple model deployments.

## Fallbacks[​](#fallbacks "Direct link to Fallbacks")

You can fallback across model groups. This is useful, if all "model deployments" in a "model group" are down (e.g. raising 429 errors).

Example:

```
model_list:  
  - model_name: my-custom-model  
    litellm_params:  
      model: openai/gpt-4o-mini  
      api_key: os.environ/OPENAI_API_KEY  
  - model_name: my-other-model  
    litellm_params:  
      model: openai/gpt-4o  
      api_key: os.environ/OPENAI_API_KEY  
  
litellm_settings:  
  fallbacks: [{"my-custom-model": ["my-other-model"]}]
```

Fallbacks are done sequentially, so the first model group in the list will be tried first. If it fails, the next model group will be tried.

## Advanced: Model Access Groups[​](#advanced-model-access-groups "Direct link to Advanced: Model Access Groups")

For advanced use cases, use [Model Access Groups](/docs/proxy/model_access_groups) to dynamically group multiple models and manage access without restarting the proxy.

* [Concept](#concept)
* [Example](#example)
* [Client-side request](#client-side-request)
* [Access Control](#access-control)
* [Loadbalancing](#loadbalancing)
* [Fallbacks](#fallbacks)
* [Advanced: Model Access Groups](#advanced-model-access-groups)