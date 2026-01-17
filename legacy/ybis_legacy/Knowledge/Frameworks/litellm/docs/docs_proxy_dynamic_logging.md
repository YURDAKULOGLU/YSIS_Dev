Dynamic Callback Management | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

info

✨ This is an enterprise feature.

[Get started with LiteLLM Enterprise](https://www.litellm.ai/enterprise)

LiteLLM's dynamic callback management enables teams to control logging behavior on a per-request basis without requiring central infrastructure changes. This is essential for organizations managing large-scale service ecosystems where:

* **Teams manage their own compliance** - Services can handle sensitive data appropriately without central oversight
* **Decentralized responsibility** - Each team controls their data handling while using shared infrastructure

You can disable callbacks by passing the `x-litellm-disable-callbacks` header with your requests, giving teams granular control over where their data is logged.

## Getting Started: List and Disable Callbacks[​](#getting-started-list-and-disable-callbacks "Direct link to Getting Started: List and Disable Callbacks")

Managing callbacks is a two-step process:

1. **First, list your active callbacks** to see what's currently enabled
2. **Then, disable specific callbacks** as needed for your requests

## 1. List Active Callbacks[​](#1-list-active-callbacks "Direct link to 1. List Active Callbacks")

Start by viewing all currently enabled callbacks on your proxy to see what's available to disable.

#### Request[​](#request "Direct link to Request")

```
curl -X 'GET' \  
  'http://localhost:4000/callbacks/list' \  
  -H 'accept: application/json' \  
  -H 'x-litellm-api-key: sk-1234'
```

#### Response[​](#response "Direct link to Response")

```
{  
  "success": [  
    "deployment_callback_on_success",  
    "sync_deployment_callback_on_success"  
  ],  
  "failure": [  
    "async_deployment_callback_on_failure",  
    "deployment_callback_on_failure"  
  ],  
  "success_and_failure": [  
    "langfuse",  
    "datadog"  
  ]  
}
```

#### Response Fields[​](#response-fields "Direct link to Response Fields")

The response contains three arrays that categorize your active callbacks:

* **`success`** - Callbacks that only execute when requests complete successfully. These callbacks receive data from successful LLM responses.
* **`failure`** - Callbacks that only execute when requests fail or encounter errors. These callbacks receive error information and failed request data.
* **`success_and_failure`** - Callbacks that execute for both successful and failed requests. These are typically logging/observability tools that need to capture all request data regardless of outcome.

---

## 2. Disable Callbacks[​](#2-disable-callbacks "Direct link to 2. Disable Callbacks")

Now that you know which callbacks are active, you can selectively disable them using the `x-litellm-disable-callbacks` header. You can reference any callback name from the list response above.

### Disable a Single Callback[​](#disable-a-single-callback "Direct link to Disable a Single Callback")

Use the `x-litellm-disable-callbacks` header to disable specific callbacks for individual requests.

* Curl Request
* OpenAI Python SDK

```
curl --location 'http://0.0.0.0:4000/chat/completions' \  
    --header 'Content-Type: application/json' \  
    --header 'Authorization: Bearer sk-1234' \  
    --header 'x-litellm-disable-callbacks: langfuse' \  
    --data '{  
    "model": "claude-sonnet-4-20250514",  
    "messages": [  
        {  
        "role": "user",  
        "content": "what llm are you"  
        }  
    ]  
}'
```

```
import openai  
  
client = openai.OpenAI(  
    api_key="sk-1234",  
    base_url="http://0.0.0.0:4000"  
)  
  
response = client.chat.completions.create(  
    model="claude-sonnet-4-20250514",  
    messages=[  
        {  
            "role": "user",  
            "content": "what llm are you"  
        }  
    ],  
    extra_headers={  
        "x-litellm-disable-callbacks": "langfuse"  
    }  
)  
  
print(response)
```

### Disable Multiple Callbacks[​](#disable-multiple-callbacks "Direct link to Disable Multiple Callbacks")

You can disable multiple callbacks by providing a comma-separated list in the header. Use any combination of callback names from your `/callbacks/list` response.

* Curl Request
* OpenAI Python SDK

```
curl --location 'http://0.0.0.0:4000/chat/completions' \  
    --header 'Content-Type: application/json' \  
    --header 'Authorization: Bearer sk-1234' \  
    --header 'x-litellm-disable-callbacks: langfuse,datadog,prometheus' \  
    --data '{  
    "model": "claude-sonnet-4-20250514",  
    "messages": [  
        {  
        "role": "user",  
        "content": "what llm are you"  
        }  
    ]  
}'
```

```
import openai  
  
client = openai.OpenAI(  
    api_key="sk-1234",  
    base_url="http://0.0.0.0:4000"  
)  
  
response = client.chat.completions.create(  
    model="claude-sonnet-4-20250514",  
    messages=[  
        {  
            "role": "user",  
            "content": "what llm are you"  
        }  
    ],  
    extra_headers={  
        "x-litellm-disable-callbacks": "langfuse,datadog,prometheus"  
    }  
)  
  
print(response)
```

## Header Format and Case Sensitivity[​](#header-format-and-case-sensitivity "Direct link to Header Format and Case Sensitivity")

### Expected Header Format[​](#expected-header-format "Direct link to Expected Header Format")

The `x-litellm-disable-callbacks` header accepts callback names in the following formats (use the exact names returned by `/callbacks/list`):

* **Single callback**: `x-litellm-disable-callbacks: langfuse`
* **Multiple callbacks**: `x-litellm-disable-callbacks: langfuse,datadog,prometheus`

When specifying multiple callbacks, use comma-separated values without spaces around the commas.

### Case Sensitivity[​](#case-sensitivity "Direct link to Case Sensitivity")

**Callback name checks are case insensitive.** This means all of the following are equivalent:

```
# These are all equivalent  
x-litellm-disable-callbacks: langfuse  
x-litellm-disable-callbacks: LANGFUSE    
x-litellm-disable-callbacks: LangFuse  
x-litellm-disable-callbacks: langFUSE
```

This applies to both single and multiple callback specifications:

```
# Case insensitive for multiple callbacks  
x-litellm-disable-callbacks: LANGFUSE,datadog,PROMETHEUS  
x-litellm-disable-callbacks: langfuse,DATADOG,prometheus
```

---

## Disabling Dynamic Callback Management (Enterprise)[​](#disabling-dynamic-callback-management-enterprise "Direct link to Disabling Dynamic Callback Management (Enterprise)")

Some organizations have compliance requirements where **all requests must be logged under all circumstances**. For these cases, you can disable dynamic callback management entirely to ensure users cannot disable any logging callbacks.

### Use Case[​](#use-case "Direct link to Use Case")

This is designed for enterprise scenarios where:

* **Compliance requirements** mandate that all API requests must be logged
* **Audit trails** must be complete with no gaps
* **Security policies** require all traffic to be monitored
* **No exceptions** can be made for callback disabling

### How to Disable[​](#how-to-disable "Direct link to How to Disable")

Set `allow_dynamic_callback_disabling` to `false` in your config.yaml:

config.yaml

```
litellm_settings:  
  allow_dynamic_callback_disabling: false
```

### Effect[​](#effect "Direct link to Effect")

When disabled:

* The `x-litellm-disable-callbacks` header will be **ignored**
* All configured callbacks will **always execute** for every request
* Users cannot bypass logging through headers or request metadata
* All requests are guaranteed to be logged per your proxy configuration

### Example: Compliance Logging Setup[​](#example-compliance-logging-setup "Direct link to Example: Compliance Logging Setup")

Here's a complete example for an organization requiring guaranteed logging:

config.yaml

```
# config.yaml  
model_list:  
  - model_name: gpt-4  
    litellm_params:  
      model: openai/gpt-4  
      api_key: os.environ/OPENAI_API_KEY  
  
litellm_settings:  
  callbacks: ["langfuse", "datadog", "s3"]  
  # Disable dynamic callback disabling for compliance  
  allow_dynamic_callback_disabling: false
```

With this configuration:

* All requests will be logged to Langfuse, Datadog, and S3
* Users cannot disable any of these callbacks via headers
* Complete audit trail is guaranteed for compliance requirements

info

**Default Behavior**: Dynamic callback disabling is **enabled by default** (`allow_dynamic_callback_disabling: true`). You must explicitly set it to `false` to enforce guaranteed logging.

* [Getting Started: List and Disable Callbacks](#getting-started-list-and-disable-callbacks)
* [1. List Active Callbacks](#1-list-active-callbacks)
* [2. Disable Callbacks](#2-disable-callbacks)
  + [Disable a Single Callback](#disable-a-single-callback)
  + [Disable Multiple Callbacks](#disable-multiple-callbacks)
* [Header Format and Case Sensitivity](#header-format-and-case-sensitivity)
  + [Expected Header Format](#expected-header-format)
  + [Case Sensitivity](#case-sensitivity)
* [Disabling Dynamic Callback Management (Enterprise)](#disabling-dynamic-callback-management-enterprise)
  + [Use Case](#use-case)
  + [How to Disable](#how-to-disable)
  + [Effect](#effect)
  + [Example: Compliance Logging Setup](#example-compliance-logging-setup)