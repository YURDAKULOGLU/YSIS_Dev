OpenMeter - Usage-Based Billing | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

[OpenMeter](https://openmeter.io/) is an Open Source Usage-Based Billing solution for AI/Cloud applications. It integrates with Stripe for easy billing.

![](/assets/ideal-img/openmeter.b328729.640.png)

info

We want to learn how we can make the callbacks better! Meet the LiteLLM [founders](https://calendly.com/d/4mp-gd3-k5k/berriai-1-1-onboarding-litellm-hosted-version) or
join our [discord](https://discord.gg/wuPM9dRgDw)

## Quick Start[​](#quick-start "Direct link to Quick Start")

Use just 2 lines of code, to instantly log your responses **across all providers** with OpenMeter

Get your OpenMeter API Key from <https://openmeter.cloud/meters>

```
litellm.callbacks = ["openmeter"] # logs cost + usage of successful calls to openmeter
```

* SDK
* PROXY

```
# pip install openmeter   
import litellm  
import os  
  
# from https://openmeter.cloud  
os.environ["OPENMETER_API_ENDPOINT"] = ""  
os.environ["OPENMETER_API_KEY"] = ""  
  
# LLM API Keys  
os.environ['OPENAI_API_KEY']=""  
  
# set openmeter as a callback, litellm will send the data to openmeter  
litellm.callbacks = ["openmeter"]   
   
# openai call  
response = litellm.completion(  
  model="gpt-3.5-turbo",  
  messages=[  
    {"role": "user", "content": "Hi 👋 - i'm openai"}  
  ]  
)
```

1. Add to Config.yaml

```
model_list:  
- litellm_params:  
    api_base: https://openai-function-calling-workers.tasslexyz.workers.dev/  
    api_key: my-fake-key  
    model: openai/my-fake-model  
  model_name: fake-openai-endpoint  
  
litellm_settings:  
  callbacks: ["openmeter"] # 👈 KEY CHANGE
```

2. Start Proxy

```
litellm --config /path/to/config.yaml
```

3. Test it!

```
curl --location 'http://0.0.0.0:4000/chat/completions' \  
--header 'Content-Type: application/json' \  
--data ' {  
      "model": "fake-openai-endpoint",  
      "messages": [  
        {  
          "role": "user",  
          "content": "what llm are you"  
        }  
      ],  
    }  
'
```

![](/assets/ideal-img/openmeter_img_2.67961c2.640.png)

* [Quick Start](#quick-start)