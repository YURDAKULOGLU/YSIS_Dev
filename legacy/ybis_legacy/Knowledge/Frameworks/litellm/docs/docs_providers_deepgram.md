Deepgram | liteLLM






[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

LiteLLM supports Deepgram's `/listen` endpoint.

| Property | Details |
| --- | --- |
| Description | Deepgram's voice AI platform provides APIs for speech-to-text, text-to-speech, and language understanding. |
| Provider Route on LiteLLM | `deepgram/` |
| Provider Doc | [Deepgram ↗](https://developers.deepgram.com/docs/introduction) |
| Supported OpenAI Endpoints | `/audio/transcriptions` |

## Quick Start[​](#quick-start "Direct link to Quick Start")

```
from litellm import transcription  
import os   
  
# set api keys   
os.environ["DEEPGRAM_API_KEY"] = ""  
audio_file = open("/path/to/audio.mp3", "rb")  
  
response = transcription(model="deepgram/nova-2", file=audio_file)  
  
print(f"response: {response}")
```

## LiteLLM Proxy Usage[​](#litellm-proxy-usage "Direct link to LiteLLM Proxy Usage")

### Add model to config[​](#add-model-to-config "Direct link to Add model to config")

1. Add model to config.yaml

```
model_list:  
- model_name: nova-2  
  litellm_params:  
    model: deepgram/nova-2  
    api_key: os.environ/DEEPGRAM_API_KEY  
  model_info:  
    mode: audio_transcription  
      
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
* OpenAI

```
curl --location 'http://0.0.0.0:4000/v1/audio/transcriptions' \  
--header 'Authorization: Bearer sk-1234' \  
--form 'file=@"/Users/krrishdholakia/Downloads/gettysburg.wav"' \  
--form 'model="nova-2"'
```

```
from openai import OpenAI  
client = openai.OpenAI(  
    api_key="sk-1234",  
    base_url="http://0.0.0.0:4000"  
)  
  
  
audio_file = open("speech.mp3", "rb")  
transcript = client.audio.transcriptions.create(  
  model="nova-2",  
  file=audio_file  
)
```

* [Quick Start](#quick-start)
* [LiteLLM Proxy Usage](#litellm-proxy-usage)
  + [Add model to config](#add-model-to-config)
  + [Start proxy](#start-proxy)
  + [Test](#test)