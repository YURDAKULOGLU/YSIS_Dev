AWS Bedrock - Image Generation | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

Use Bedrock for image generation with Stable Diffusion, Amazon Titan Image Generator, and Amazon Nova Canvas models.

## Supported Models[​](#supported-models "Direct link to Supported Models")

| Model Name | Function Call | Cost Tracking |
| --- | --- | --- |
| Stable Diffusion 3 - v0 | `image_generation(model="bedrock/stability.stability.sd3-large-v1:0", prompt=prompt)` | ✅ |
| Stable Diffusion - v0 | `image_generation(model="bedrock/stability.stable-diffusion-xl-v0", prompt=prompt)` | ✅ |
| Stable Diffusion - v1 | `image_generation(model="bedrock/stability.stable-diffusion-xl-v1", prompt=prompt)` | ✅ |
| Amazon Titan Image Generator - v1 | `image_generation(model="bedrock/amazon.titan-image-generator-v1", prompt=prompt)` | ✅ |
| Amazon Titan Image Generator - v2 | `image_generation(model="bedrock/amazon.titan-image-generator-v2:0", prompt=prompt)` | ✅ |
| Amazon Nova Canvas - v1 | `image_generation(model="bedrock/amazon.nova-canvas-v1:0", prompt=prompt)` | ✅ |

## Usage[​](#usage "Direct link to Usage")

* SDK
* PROXY

### Basic Usage[​](#basic-usage "Direct link to Basic Usage")

```
import os  
from litellm import image_generation  
  
os.environ["AWS_ACCESS_KEY_ID"] = ""  
os.environ["AWS_SECRET_ACCESS_KEY"] = ""  
os.environ["AWS_REGION_NAME"] = ""  
  
response = image_generation(  
    prompt="A cute baby sea otter",  
    model="bedrock/stability.stable-diffusion-xl-v0",  
)  
print(f"response: {response}")
```

### Set Optional Parameters[​](#set-optional-parameters "Direct link to Set Optional Parameters")

```
import os  
from litellm import image_generation  
  
os.environ["AWS_ACCESS_KEY_ID"] = ""  
os.environ["AWS_SECRET_ACCESS_KEY"] = ""  
os.environ["AWS_REGION_NAME"] = ""  
  
response = image_generation(  
    prompt="A cute baby sea otter",  
    model="bedrock/stability.stable-diffusion-xl-v0",  
    ### OPENAI-COMPATIBLE ###  
    size="128x512", # width=128, height=512  
    ### PROVIDER-SPECIFIC ### see `AmazonStabilityConfig` in bedrock.py for all params  
    seed=30  
)  
print(f"response: {response}")
```

### 1. Setup config.yaml[​](#1-setup-configyaml "Direct link to 1. Setup config.yaml")

```
model_list:  
  - model_name: amazon.nova-canvas-v1:0  
    litellm_params:  
      model: bedrock/amazon.nova-canvas-v1:0  
      aws_region_name: "us-east-1"  
      aws_secret_access_key: my-key # OPTIONAL - all boto3 auth params supported  
      aws_secret_access_id: my-id # OPTIONAL - all boto3 auth params supported
```

### 2. Start proxy[​](#2-start-proxy "Direct link to 2. Start proxy")

```
litellm --config /path/to/config.yaml
```

### 3. Test it![​](#3-test-it "Direct link to 3. Test it!")

**Text to Image:**

```
curl -L -X POST 'http://0.0.0.0:4000/v1/images/generations' \  
-H 'Content-Type: application/json' \  
-H 'Authorization: Bearer $LITELLM_VIRTUAL_KEY' \  
-d '{  
    "model": "amazon.nova-canvas-v1:0",  
    "prompt": "A cute baby sea otter"  
}'
```

**Color Guided Generation:**

```
curl -L -X POST 'http://0.0.0.0:4000/v1/images/generations' \  
-H 'Content-Type: application/json' \  
-H 'Authorization: Bearer $LITELLM_VIRTUAL_KEY' \  
-d '{  
    "model": "amazon.nova-canvas-v1:0",  
    "prompt": "A cute baby sea otter",  
    "taskType": "COLOR_GUIDED_GENERATION",  
    "colorGuidedGenerationParams":{"colors":["#FFFFFF"]}  
}'
```

## Using Inference Profiles with Image Generation[​](#using-inference-profiles-with-image-generation "Direct link to Using Inference Profiles with Image Generation")

For AWS Bedrock Application Inference Profiles with image generation, use the `model_id` parameter to specify the inference profile ARN:

* SDK
* PROXY

```
from litellm import image_generation  
  
response = image_generation(  
    model="bedrock/amazon.nova-canvas-v1:0",  
    model_id="arn:aws:bedrock:eu-west-1:000000000000:application-inference-profile/a0a0a0a0a0a0",  
    prompt="A cute baby sea otter"  
)  
print(f"response: {response}")
```

```
model_list:  
  - model_name: nova-canvas-inference-profile  
    litellm_params:  
      model: bedrock/amazon.nova-canvas-v1:0  
      model_id: arn:aws:bedrock:eu-west-1:000000000000:application-inference-profile/a0a0a0a0a0a0  
      aws_region_name: "eu-west-1"
```

## Authentication[​](#authentication "Direct link to Authentication")

All standard Bedrock authentication methods are supported for image generation. See [Bedrock Authentication](/docs/providers/bedrock#boto3---authentication) for details.

* [Supported Models](#supported-models)
* [Usage](#usage)
  + [Basic Usage](#basic-usage)
  + [Set Optional Parameters](#set-optional-parameters)
  + [1. Setup config.yaml](#1-setup-configyaml)
  + [2. Start proxy](#2-start-proxy)
  + [3. Test it!](#3-test-it)
* [Using Inference Profiles with Image Generation](#using-inference-profiles-with-image-generation)
* [Authentication](#authentication)