Adding OpenAI-Compatible Providers | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

For simple OpenAI-compatible providers (like Hyperbolic, Nscale, etc.), you can add support by editing a single JSON file.

## Quick Start[​](#quick-start "Direct link to Quick Start")

1. Edit `litellm/llms/openai_like/providers.json`
2. Add your provider configuration
3. Test with: `litellm.completion(model="your_provider/model-name", ...)`

## Basic Configuration[​](#basic-configuration "Direct link to Basic Configuration")

For a fully OpenAI-compatible provider:

```
{  
  "your_provider": {  
    "base_url": "https://api.yourprovider.com/v1",  
    "api_key_env": "YOUR_PROVIDER_API_KEY"  
  }  
}
```

That's it! The provider is now available.

## Configuration Options[​](#configuration-options "Direct link to Configuration Options")

### Required Fields[​](#required-fields "Direct link to Required Fields")

* `base_url` - API endpoint (e.g., `https://api.provider.com/v1`)
* `api_key_env` - Environment variable name for API key (e.g., `PROVIDER_API_KEY`)

### Optional Fields[​](#optional-fields "Direct link to Optional Fields")

* `api_base_env` - Environment variable to override `base_url`
* `base_class` - Use `"openai_gpt"` (default) or `"openai_like"`
* `param_mappings` - Map OpenAI parameter names to provider-specific names
* `constraints` - Parameter value constraints (min/max)
* `special_handling` - Special behaviors like content format conversion

## Examples[​](#examples "Direct link to Examples")

### Simple Provider (Fully Compatible)[​](#simple-provider-fully-compatible "Direct link to Simple Provider (Fully Compatible)")

```
{  
  "hyperbolic": {  
    "base_url": "https://api.hyperbolic.xyz/v1",  
    "api_key_env": "HYPERBOLIC_API_KEY"  
  }  
}
```

### Provider with Parameter Mapping[​](#provider-with-parameter-mapping "Direct link to Provider with Parameter Mapping")

```
{  
  "publicai": {  
    "base_url": "https://api.publicai.co/v1",  
    "api_key_env": "PUBLICAI_API_KEY",  
    "param_mappings": {  
      "max_completion_tokens": "max_tokens"  
    }  
  }  
}
```

### Provider with Constraints[​](#provider-with-constraints "Direct link to Provider with Constraints")

```
{  
  "custom_provider": {  
    "base_url": "https://api.custom.com/v1",  
    "api_key_env": "CUSTOM_API_KEY",  
    "constraints": {  
      "temperature_max": 1.0,  
      "temperature_min": 0.0  
    }  
  }  
}
```

## Usage[​](#usage "Direct link to Usage")

```
import litellm  
import os  
  
# Set your API key  
os.environ["YOUR_PROVIDER_API_KEY"] = "your-key-here"  
  
# Use the provider  
response = litellm.completion(  
    model="your_provider/model-name",  
    messages=[{"role": "user", "content": "Hello"}],  
)
```

## When to Use Python Instead[​](#when-to-use-python-instead "Direct link to When to Use Python Instead")

Use a Python config class if you need:

* Custom authentication flows (OAuth, JWT, etc.)
* Complex request/response transformations
* Provider-specific streaming logic
* Advanced tool calling modifications

For these cases, create a config class in `litellm/llms/your_provider/chat/transformation.py` that inherits from `OpenAIGPTConfig` or `OpenAILikeChatConfig`.

## Testing[​](#testing "Direct link to Testing")

Test your provider:

```
# Quick test  
python -c "  
import litellm  
import os  
os.environ['PROVIDER_API_KEY'] = 'your-key'  
response = litellm.completion(  
    model='provider/model-name',  
    messages=[{'role': 'user', 'content': 'test'}]  
)  
print(response.choices[0].message.content)  
"
```

## Reference[​](#reference "Direct link to Reference")

See existing providers in `litellm/llms/openai_like/providers.json` for examples.

* [Quick Start](#quick-start)
* [Basic Configuration](#basic-configuration)
* [Configuration Options](#configuration-options)
  + [Required Fields](#required-fields)
  + [Optional Fields](#optional-fields)
* [Examples](#examples)
  + [Simple Provider (Fully Compatible)](#simple-provider-fully-compatible)
  + [Provider with Parameter Mapping](#provider-with-parameter-mapping)
  + [Provider with Constraints](#provider-with-constraints)
* [Usage](#usage)
* [When to Use Python Instead](#when-to-use-python-instead)
* [Testing](#testing)
* [Reference](#reference)