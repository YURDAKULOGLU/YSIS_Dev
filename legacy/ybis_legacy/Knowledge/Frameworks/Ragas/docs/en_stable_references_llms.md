LLMs - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.llms)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# LLMs

## BaseRagasLLM `dataclass`

```
BaseRagasLLM(run_config: RunConfig = RunConfig(), multiple_completion_supported: bool = False, cache: Optional[CacheInterface] = None)
```

Bases: `ABC`

### get\_temperature

```
get_temperature(n: int) -> float
```

Return the temperature to use for completion based on n.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 71 72 73 ``` | ``` def get_temperature(self, n: int) -> float:     """Return the temperature to use for completion based on n."""     return 0.3 if n > 1 else 0.01 ``` |

### is\_finished `abstractmethod`

```
is_finished(response: LLMResult) -> bool
```

Check if the LLM response is finished/complete.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 95 96 97 98 ``` | ``` @abstractmethod def is_finished(self, response: LLMResult) -> bool:     """Check if the LLM response is finished/complete."""     ... ``` |

### generate `async`

```
generate(prompt: PromptValue, n: int = 1, temperature: Optional[float] = 0.01, stop: Optional[List[str]] = None, callbacks: Callbacks = None) -> LLMResult
```

Generate text using the given event loop.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 ``` | ``` async def generate(     self,     prompt: PromptValue,     n: int = 1,     temperature: t.Optional[float] = 0.01,     stop: t.Optional[t.List[str]] = None,     callbacks: Callbacks = None, ) -> LLMResult:     """Generate text using the given event loop."""      if temperature is None:         temperature = self.get_temperature(n)      agenerate_text_with_retry = add_async_retry(         self.agenerate_text, self.run_config     )     result = await agenerate_text_with_retry(         prompt=prompt,         n=n,         temperature=temperature,         stop=stop,         callbacks=callbacks,     )      # check there are no max_token issues     if not self.is_finished(result):         raise LLMDidNotFinishException()     return result ``` |

## InstructorBaseRagasLLM

Bases: `ABC`

Base class for LLMs using the Instructor library pattern.

### generate `abstractmethod`

```
generate(prompt: str, response_model: Type[InstructorTypeVar]) -> InstructorTypeVar
```

Generate a response using the configured LLM.

For async clients, this will run the async method in the appropriate event loop.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 732 733 734 735 736 737 738 739 ``` | ``` @abstractmethod def generate(     self, prompt: str, response_model: t.Type[InstructorTypeVar] ) -> InstructorTypeVar:     """Generate a response using the configured LLM.      For async clients, this will run the async method in the appropriate event loop.     """ ``` |

### agenerate `abstractmethod` `async`

```
agenerate(prompt: str, response_model: Type[InstructorTypeVar]) -> InstructorTypeVar
```

Asynchronously generate a response using the configured LLM.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 741 742 743 744 745 746 747 ``` | ``` @abstractmethod async def agenerate(     self,     prompt: str,     response_model: t.Type[InstructorTypeVar], ) -> InstructorTypeVar:     """Asynchronously generate a response using the configured LLM.""" ``` |

## InstructorLLM

```
InstructorLLM(client: Any, model: str, provider: str, model_args: Optional[InstructorModelArgs] = None, cache: Optional[CacheInterface] = None, **kwargs)
```

Bases: `InstructorBaseRagasLLM`

LLM wrapper using the Instructor library for structured outputs.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 ``` | ``` def __init__(     self,     client: t.Any,     model: str,     provider: str,     model_args: t.Optional[InstructorModelArgs] = None,     cache: t.Optional[CacheInterface] = None,     **kwargs, ):     self.client = client     self.model = model     self.provider = provider      # Use deterministic defaults if no model_args provided     if model_args is None:         model_args = InstructorModelArgs()      # Convert to dict and merge with any additional kwargs     self.model_args = {**model_args.model_dump(), **kwargs}      self.cache = cache      # Check if client is async-capable at initialization     self.is_async = self._check_client_async()      if self.cache is not None:         self.generate = cacher(cache_backend=self.cache)(self.generate)  # type: ignore         self.agenerate = cacher(cache_backend=self.cache)(self.agenerate)  # type: ignore ``` |

### generate

```
generate(prompt: str, response_model: Type[InstructorTypeVar]) -> InstructorTypeVar
```

Generate a response using the configured LLM.

For async clients, this will run the async method in the appropriate event loop.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 ``` | ``` def generate(     self, prompt: str, response_model: t.Type[InstructorTypeVar] ) -> InstructorTypeVar:     """Generate a response using the configured LLM.      For async clients, this will run the async method in the appropriate event loop.     """     messages = [{"role": "user", "content": prompt}]      # If client is async, use the appropriate method to run it     if self.is_async:         result = self._run_async_in_current_loop(             self.agenerate(prompt, response_model)         )     else:         # Map parameters based on provider requirements         provider_kwargs = self._map_provider_params()          if self.provider.lower() == "google":             result = self.client.create(                 model=self.model,                 messages=messages,                 response_model=response_model,                 **provider_kwargs,             )         else:             # OpenAI, Anthropic, LiteLLM             result = self.client.chat.completions.create(                 model=self.model,                 messages=messages,                 response_model=response_model,                 **provider_kwargs,             )      # Track the usage     track(         LLMUsageEvent(             provider=self.provider,             model=self.model,             llm_type="instructor",             num_requests=1,             is_async=self.is_async,         )     )     return result ``` |

### agenerate `async`

```
agenerate(prompt: str, response_model: Type[InstructorTypeVar]) -> InstructorTypeVar
```

Asynchronously generate a response using the configured LLM.

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 1073 1074 1075 1076 1077 1078 1079 1080 1081 1082 1083 1084 1085 1086 1087 1088 1089 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 ``` | ``` async def agenerate(     self,     prompt: str,     response_model: t.Type[InstructorTypeVar], ) -> InstructorTypeVar:     """Asynchronously generate a response using the configured LLM."""     messages = [{"role": "user", "content": prompt}]      # If client is not async, raise a helpful error     if not self.is_async:         raise TypeError(             "Cannot use agenerate() with a synchronous client. Use generate() instead."         )      # Map parameters based on provider requirements     provider_kwargs = self._map_provider_params()      if self.provider.lower() == "google":         result = await self.client.create(             model=self.model,             messages=messages,             response_model=response_model,             **provider_kwargs,         )     else:         # OpenAI, Anthropic, LiteLLM         result = await self.client.chat.completions.create(             model=self.model,             messages=messages,             response_model=response_model,             **provider_kwargs,         )      # Track the usage     track(         LLMUsageEvent(             provider=self.provider,             model=self.model,             llm_type="instructor",             num_requests=1,             is_async=True,         )     )     return result ``` |

## HaystackLLMWrapper

```
HaystackLLMWrapper(haystack_generator: Any, run_config: Optional[RunConfig] = None, cache: Optional[CacheInterface] = None)
```

Bases: `BaseRagasLLM`

A wrapper class for using Haystack LLM generators within the Ragas framework.

This class integrates Haystack's LLM components (e.g., `OpenAIGenerator`,
`HuggingFaceAPIGenerator`, etc.) into Ragas, enabling both synchronous and
asynchronous text generation.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `haystack_generator` | `AzureOpenAIGenerator | HuggingFaceAPIGenerator | HuggingFaceLocalGenerator | OpenAIGenerator` | An instance of a Haystack generator. | *required* |
| `run_config` | `RunConfig` | Configuration object to manage LLM execution settings, by default None. | `None` |
| `cache` | `CacheInterface` | A cache instance for storing results, by default None. | `None` |

Source code in `src/ragas/llms/haystack_wrapper.py`

|  |  |
| --- | --- |
| ``` 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 ``` | ``` def __init__(     self,     haystack_generator: t.Any,     run_config: t.Optional[RunConfig] = None,     cache: t.Optional[CacheInterface] = None, ):     super().__init__(cache=cache)      # Lazy Import of required Haystack components     try:         from haystack import AsyncPipeline         from haystack.components.generators.azure import AzureOpenAIGenerator         from haystack.components.generators.hugging_face_api import (             HuggingFaceAPIGenerator,         )         from haystack.components.generators.hugging_face_local import (             HuggingFaceLocalGenerator,         )         from haystack.components.generators.openai import OpenAIGenerator     except ImportError as exc:         raise ImportError(             "Haystack is not installed. Please install it using `pip install haystack-ai`."         ) from exc      # Validate haystack_generator type     if not isinstance(         haystack_generator,         (             AzureOpenAIGenerator,             HuggingFaceAPIGenerator,             HuggingFaceLocalGenerator,             OpenAIGenerator,         ),     ):         raise TypeError(             "Expected 'haystack_generator' to be one of: "             "AzureOpenAIGenerator, HuggingFaceAPIGenerator, "             "HuggingFaceLocalGenerator, or OpenAIGenerator, but received "             f"{type(haystack_generator).__name__}."         )      # Set up Haystack pipeline and generator     self.generator = haystack_generator     self.async_pipeline = AsyncPipeline()     self.async_pipeline.add_component("llm", self.generator)      if run_config is None:         run_config = RunConfig()     self.set_run_config(run_config) ``` |

## LiteLLMStructuredLLM

```
LiteLLMStructuredLLM(client: Any, model: str, provider: str, cache: Optional[CacheInterface] = None, **kwargs)
```

Bases: `InstructorBaseRagasLLM`

LLM wrapper using LiteLLM for structured outputs.

Works with all 100+ LiteLLM-supported providers including Gemini,
Ollama, vLLM, Groq, and many others.

The LiteLLM client should be initialized with structured output support.

Args:
client: LiteLLM client instance
model: Model name (e.g., "gemini-2.0-flash")
provider: Provider name
cache: Optional cache backend for caching LLM responses
\*\*kwargs: Additional model arguments (temperature, max\_tokens, etc.)

Source code in `src/ragas/llms/litellm_llm.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 ``` | ``` def __init__(     self,     client: t.Any,     model: str,     provider: str,     cache: t.Optional[CacheInterface] = None,     **kwargs, ):     """     Initialize LiteLLM structured LLM.      Args:         client: LiteLLM client instance         model: Model name (e.g., "gemini-2.0-flash")         provider: Provider name         cache: Optional cache backend for caching LLM responses         **kwargs: Additional model arguments (temperature, max_tokens, etc.)     """     self.client = client     self.model = model     self.provider = provider     self.model_args = kwargs     self.cache = cache      # Check if client is async-capable at initialization     self.is_async = self._check_client_async()      if self.cache is not None:         self.generate = cacher(cache_backend=self.cache)(self.generate)  # type: ignore         self.agenerate = cacher(cache_backend=self.cache)(self.agenerate)  # type: ignore ``` |

### generate

```
generate(prompt: str, response_model: Type[InstructorTypeVar]) -> InstructorTypeVar
```

Generate a response using the configured LLM.

For async clients, this will run the async method in the appropriate event loop.

Args:
prompt: Input prompt
response\_model: Pydantic model for structured output

Returns:
Instance of response\_model with generated data

Source code in `src/ragas/llms/litellm_llm.py`

|  |  |
| --- | --- |
| ``` 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 ``` | ``` def generate(     self, prompt: str, response_model: t.Type[InstructorTypeVar] ) -> InstructorTypeVar:     """Generate a response using the configured LLM.      For async clients, this will run the async method in the appropriate event loop.      Args:         prompt: Input prompt         response_model: Pydantic model for structured output      Returns:         Instance of response_model with generated data     """     messages = [{"role": "user", "content": prompt}]      # If client is async, use the appropriate method to run it     if self.is_async:         result = self._run_async_in_current_loop(             self.agenerate(prompt, response_model)         )     else:         # Call LiteLLM with structured output         result = self.client.chat.completions.create(             model=self.model,             messages=messages,             response_model=response_model,             **self.model_args,         )      # Track the usage     track(         LLMUsageEvent(             provider=self.provider,             model=self.model,             llm_type="litellm",             num_requests=1,             is_async=self.is_async,         )     )     return result ``` |

### agenerate `async`

```
agenerate(prompt: str, response_model: Type[InstructorTypeVar]) -> InstructorTypeVar
```

Asynchronously generate a response using the configured LLM.

Args:
prompt: Input prompt
response\_model: Pydantic model for structured output

Returns:
Instance of response\_model with generated data

Source code in `src/ragas/llms/litellm_llm.py`

|  |  |
| --- | --- |
| ``` 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 ``` | ``` async def agenerate(     self,     prompt: str,     response_model: t.Type[InstructorTypeVar], ) -> InstructorTypeVar:     """Asynchronously generate a response using the configured LLM.      Args:         prompt: Input prompt         response_model: Pydantic model for structured output      Returns:         Instance of response_model with generated data     """     messages = [{"role": "user", "content": prompt}]      # If client is not async, raise a helpful error     if not self.is_async:         raise TypeError(             "Cannot use agenerate() with a synchronous client. Use generate() instead."         )      # Call LiteLLM async with structured output     result = await self.client.chat.completions.create(         model=self.model,         messages=messages,         response_model=response_model,         **self.model_args,     )      # Track the usage     track(         LLMUsageEvent(             provider=self.provider,             model=self.model,             llm_type="litellm",             num_requests=1,             is_async=True,         )     )     return result ``` |

## OCIGenAIWrapper

```
OCIGenAIWrapper(model_id: str, compartment_id: str, config: Optional[Dict[str, Any]] = None, endpoint_id: Optional[str] = None, run_config: Optional[RunConfig] = None, cache: Optional[Any] = None, default_system_prompt: Optional[str] = None, client: Optional[Any] = None)
```

Bases: `BaseRagasLLM`

OCI Gen AI LLM wrapper for Ragas.

This wrapper provides direct integration with Oracle Cloud Infrastructure
Generative AI services without requiring LangChain or LlamaIndex.

Args:
model\_id: The OCI model ID to use for generation
compartment\_id: The OCI compartment ID
config: OCI configuration dictionary (optional, uses default if not provided)
endpoint\_id: Optional endpoint ID for the model
run\_config: Ragas run configuration
cache: Optional cache backend

Source code in `src/ragas/llms/oci_genai_wrapper.py`

|  |  |
| --- | --- |
| ``` 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 ``` | ``` def __init__(     self,     model_id: str,     compartment_id: str,     config: t.Optional[t.Dict[str, t.Any]] = None,     endpoint_id: t.Optional[str] = None,     run_config: t.Optional[RunConfig] = None,     cache: t.Optional[t.Any] = None,     default_system_prompt: t.Optional[str] = None,     client: t.Optional[t.Any] = None, ):     """     Initialize OCI Gen AI wrapper.      Args:         model_id: The OCI model ID to use for generation         compartment_id: The OCI compartment ID         config: OCI configuration dictionary (optional, uses default if not provided)         endpoint_id: Optional endpoint ID for the model         run_config: Ragas run configuration         cache: Optional cache backend     """     super().__init__(cache=cache)      self.model_id = model_id     self.compartment_id = compartment_id     self.endpoint_id = endpoint_id     self.default_system_prompt = default_system_prompt      # Store client/config; perform lazy initialization to keep import-optional     self.client = client     self._oci_config = config     # If no client and SDK not available and no endpoint fallback, raise early     if (         self.client is None         and GenerativeAiClient is None         and self.endpoint_id is None     ):  # type: ignore         raise ImportError(             "OCI SDK not found. Please install it with: pip install oci"         )      # Set run config     if run_config is None:         run_config = RunConfig()     self.set_run_config(run_config)      # Track initialization     track(         LLMUsageEvent(             provider="oci_genai",             model=model_id,             llm_type="oci_wrapper",             num_requests=1,             is_async=False,         )     ) ``` |

### generate\_text

```
generate_text(prompt: PromptValue, n: int = 1, temperature: Optional[float] = 0.01, stop: Optional[List[str]] = None, callbacks: Optional[Any] = None) -> LLMResult
```

Generate text using OCI Gen AI.

Source code in `src/ragas/llms/oci_genai_wrapper.py`

|  |  |
| --- | --- |
| ``` 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 ``` | ``` def generate_text(     self,     prompt: PromptValue,     n: int = 1,     temperature: t.Optional[float] = 0.01,     stop: t.Optional[t.List[str]] = None,     callbacks: t.Optional[t.Any] = None, ) -> LLMResult:     """Generate text using OCI Gen AI."""     if temperature is None:         temperature = self.get_temperature(n)      messages = self._convert_prompt_to_messages(prompt)     generations = []      try:         for _ in range(n):             request = self._create_generation_request(                 messages, temperature, stop=stop             )              response = self._get_client().generate_text(**request)              # Extract text from response             if hasattr(response.data, "choices") and response.data.choices:                 text = response.data.choices[0].message.content             elif hasattr(response.data, "text"):                 text = response.data.text             else:                 text = str(response.data)              generation = Generation(text=text)             generations.append([generation])          # Track usage         track(             LLMUsageEvent(                 provider="oci_genai",                 model=self.model_id,                 llm_type="oci_wrapper",                 num_requests=n,                 is_async=False,             )         )          return LLMResult(generations=generations)      except Exception as e:         logger.error(f"Error generating text with OCI Gen AI: {e}")         raise ``` |

### agenerate\_text `async`

```
agenerate_text(prompt: PromptValue, n: int = 1, temperature: Optional[float] = 0.01, stop: Optional[List[str]] = None, callbacks: Optional[Any] = None) -> LLMResult
```

Generate text asynchronously using OCI Gen AI.

Source code in `src/ragas/llms/oci_genai_wrapper.py`

|  |  |
| --- | --- |
| ``` 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 ``` | ``` async def agenerate_text(     self,     prompt: PromptValue,     n: int = 1,     temperature: t.Optional[float] = 0.01,     stop: t.Optional[t.List[str]] = None,     callbacks: t.Optional[t.Any] = None, ) -> LLMResult:     """Generate text asynchronously using OCI Gen AI."""     if temperature is None:         temperature = self.get_temperature(n)      messages = self._convert_prompt_to_messages(prompt)     generations = []      try:         # Run synchronous calls in thread pool for async compatibility         loop = asyncio.get_event_loop()          for _ in range(n):             request = self._create_generation_request(                 messages, temperature, stop=stop             )              response = await loop.run_in_executor(                 None, lambda: self._get_client().generate_text(**request)             )              # Extract text from response             if hasattr(response.data, "choices") and response.data.choices:                 text = response.data.choices[0].message.content             elif hasattr(response.data, "text"):                 text = response.data.text             else:                 text = str(response.data)              generation = Generation(text=text)             generations.append([generation])          # Track usage         track(             LLMUsageEvent(                 provider="oci_genai",                 model=self.model_id,                 llm_type="oci_wrapper",                 num_requests=n,                 is_async=True,             )         )          return LLMResult(generations=generations)      except Exception as e:         logger.error(f"Error generating text with OCI Gen AI: {e}")         raise ``` |

### is\_finished

```
is_finished(response: LLMResult) -> bool
```

Check if the LLM response is finished/complete.

Source code in `src/ragas/llms/oci_genai_wrapper.py`

|  |  |
| --- | --- |
| ``` 295 296 297 298 299 300 301 302 303 304 305 306 ``` | ``` def is_finished(self, response: LLMResult) -> bool:     """Check if the LLM response is finished/complete."""     # For OCI Gen AI, we assume the response is always finished     # unless there's an explicit error or truncation     try:         for generation_list in response.generations:             for generation in generation_list:                 if not generation.text or generation.text.strip() == "":                     return False         return True     except Exception:         return False ``` |

## llm\_factory

```
llm_factory(model: str, provider: str = 'openai', client: Optional[Any] = None, adapter: str = 'auto', cache: Optional[CacheInterface] = None, **kwargs: Any) -> InstructorBaseRagasLLM
```

Create an LLM instance for structured output generation with automatic adapter selection.

Supports multiple LLM providers and structured output backends with unified interface
for both sync and async operations. Returns instances with .generate() and .agenerate()
methods that accept Pydantic models for structured outputs.

Auto-detects the best adapter for your provider:
- Google Gemini → uses LiteLLM adapter
- Other providers → uses Instructor adapter (default)
- Explicit control available via adapter parameter

Args:
model: Model name (e.g., "gpt-4o", "claude-3-sonnet", "gemini-2.0-flash").
provider: LLM provider (default: "openai").
Examples: openai, anthropic, google, groq, mistral, etc.
client: Pre-initialized client instance (required). For OpenAI, can be
OpenAI(...) or AsyncOpenAI(...).
adapter: Structured output adapter to use (default: "auto").
- "auto": Auto-detect based on provider/client (recommended)
- "instructor": Use Instructor library
- "litellm": Use LiteLLM (supports 100+ providers)
cache: Optional cache backend for caching LLM responses.
Pass DiskCacheBackend() for persistent caching across runs.
Saves costs and speeds up repeated evaluations by 60x.
\*\*kwargs: Additional model arguments (temperature, max\_tokens, top\_p, etc).

Returns:
InstructorBaseRagasLLM: Instance with generate() and agenerate() methods.

Raises:
ValueError: If client is missing, provider is unsupported, model is invalid,
or adapter initialization fails.

Examples:
from openai import OpenAI

```
# Basic usage
client = OpenAI(api_key="...")
llm = llm_factory("gpt-4o-mini", client=client)
response = llm.generate(prompt, ResponseModel)

# With caching (recommended for experiments)
from ragas.cache import DiskCacheBackend
cache = DiskCacheBackend()
llm = llm_factory("gpt-4o-mini", client=client, cache=cache)

# Anthropic
from anthropic import Anthropic
client = Anthropic(api_key="...")
llm = llm_factory("claude-3-sonnet", provider="anthropic", client=client)

# Google Gemini (auto-detects litellm adapter)
from litellm import OpenAI as LiteLLMClient
client = LiteLLMClient(api_key="...", model="gemini-2.0-flash")
llm = llm_factory("gemini-2.0-flash", client=client)

# Explicit adapter selection
llm = llm_factory("gemini-2.0-flash", client=client, adapter="litellm")

# Async
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key="...")
llm = llm_factory("gpt-4o-mini", client=client)
response = await llm.agenerate(prompt, ResponseModel)
```

Source code in `src/ragas/llms/base.py`

|  |  |
| --- | --- |
| ``` 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 ``` | ``` def llm_factory(     model: str,     provider: str = "openai",     client: t.Optional[t.Any] = None,     adapter: str = "auto",     cache: t.Optional[CacheInterface] = None,     **kwargs: t.Any, ) -> InstructorBaseRagasLLM:     """     Create an LLM instance for structured output generation with automatic adapter selection.      Supports multiple LLM providers and structured output backends with unified interface     for both sync and async operations. Returns instances with .generate() and .agenerate()     methods that accept Pydantic models for structured outputs.      Auto-detects the best adapter for your provider:     - Google Gemini → uses LiteLLM adapter     - Other providers → uses Instructor adapter (default)     - Explicit control available via adapter parameter      Args:         model: Model name (e.g., "gpt-4o", "claude-3-sonnet", "gemini-2.0-flash").         provider: LLM provider (default: "openai").                  Examples: openai, anthropic, google, groq, mistral, etc.         client: Pre-initialized client instance (required). For OpenAI, can be                OpenAI(...) or AsyncOpenAI(...).         adapter: Structured output adapter to use (default: "auto").                 - "auto": Auto-detect based on provider/client (recommended)                 - "instructor": Use Instructor library                 - "litellm": Use LiteLLM (supports 100+ providers)         cache: Optional cache backend for caching LLM responses.                Pass DiskCacheBackend() for persistent caching across runs.                Saves costs and speeds up repeated evaluations by 60x.         **kwargs: Additional model arguments (temperature, max_tokens, top_p, etc).      Returns:         InstructorBaseRagasLLM: Instance with generate() and agenerate() methods.      Raises:         ValueError: If client is missing, provider is unsupported, model is invalid,                    or adapter initialization fails.      Examples:         from openai import OpenAI          # Basic usage         client = OpenAI(api_key="...")         llm = llm_factory("gpt-4o-mini", client=client)         response = llm.generate(prompt, ResponseModel)          # With caching (recommended for experiments)         from ragas.cache import DiskCacheBackend         cache = DiskCacheBackend()         llm = llm_factory("gpt-4o-mini", client=client, cache=cache)          # Anthropic         from anthropic import Anthropic         client = Anthropic(api_key="...")         llm = llm_factory("claude-3-sonnet", provider="anthropic", client=client)          # Google Gemini (auto-detects litellm adapter)         from litellm import OpenAI as LiteLLMClient         client = LiteLLMClient(api_key="...", model="gemini-2.0-flash")         llm = llm_factory("gemini-2.0-flash", client=client)          # Explicit adapter selection         llm = llm_factory("gemini-2.0-flash", client=client, adapter="litellm")          # Async         from openai import AsyncOpenAI         client = AsyncOpenAI(api_key="...")         llm = llm_factory("gpt-4o-mini", client=client)         response = await llm.agenerate(prompt, ResponseModel)     """     if client is None:         raise ValueError(             "llm_factory() requires a client instance. "             "Text-only mode has been removed.\n\n"             "To migrate:\n"             "  from openai import OpenAI\n"             "  client = OpenAI(api_key='...')\n"             "  llm = llm_factory('gpt-4o-mini', client=client)\n\n"             "For more details: https://docs.ragas.io/en/latest/llm-factory"         )      if not model:         raise ValueError("model parameter is required")      provider_lower = provider.lower()      # Auto-detect adapter if needed     if adapter == "auto":         from ragas.llms.adapters import auto_detect_adapter          adapter = auto_detect_adapter(client, provider_lower)      # Create LLM using selected adapter     from ragas.llms.adapters import get_adapter      try:         adapter_instance = get_adapter(adapter)         llm = adapter_instance.create_llm(             client, model, provider_lower, cache=cache, **kwargs         )     except ValueError as e:         # Re-raise ValueError from get_adapter for unknown adapter names         # Also handle adapter initialization failures         if "Unknown adapter" in str(e):             raise         # Adapter-specific failures get wrapped         raise ValueError(             f"Failed to initialize {provider} client with {adapter} adapter. "             f"Ensure you've created a valid {provider} client.\n"             f"Error: {str(e)}"         )     except Exception as e:         raise ValueError(             f"Failed to initialize {provider} client with {adapter} adapter. "             f"Ensure you've created a valid {provider} client.\n"             f"Error: {str(e)}"         )      track(         LLMUsageEvent(             provider=provider,             model=model,             llm_type="llm_factory",             num_requests=1,             is_async=False,         )     )      return llm ``` |

## oci\_genai\_factory

```
oci_genai_factory(model_id: str, compartment_id: str, config: Optional[Dict[str, Any]] = None, endpoint_id: Optional[str] = None, run_config: Optional[RunConfig] = None, cache: Optional[Any] = None, default_system_prompt: Optional[str] = None, client: Optional[Any] = None) -> OCIGenAIWrapper
```

Factory function to create an OCI Gen AI LLM instance.

Args:
model\_id: The OCI model ID to use for generation
compartment\_id: The OCI compartment ID
config: OCI configuration dictionary (optional)
endpoint\_id: Optional endpoint ID for the model
run\_config: Ragas run configuration
\*\*kwargs: Additional arguments passed to OCIGenAIWrapper

Returns:
OCIGenAIWrapper: An instance of the OCI Gen AI LLM wrapper

Examples:
# Basic usage with default config
llm = oci\_genai\_factory(
model\_id="cohere.command",
compartment\_id="ocid1.compartment.oc1..example"
)

```
# With custom config
llm = oci_genai_factory(
    model_id="cohere.command",
    compartment_id="ocid1.compartment.oc1..example",
    config={"user": "user_ocid", "key_file": "~/.oci/private_key.pem"}
)
```

Source code in `src/ragas/llms/oci_genai_wrapper.py`

|  |  |
| --- | --- |
| ``` 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 ``` | ``` def oci_genai_factory(     model_id: str,     compartment_id: str,     config: t.Optional[t.Dict[str, t.Any]] = None,     endpoint_id: t.Optional[str] = None,     run_config: t.Optional[RunConfig] = None,     cache: t.Optional[t.Any] = None,     default_system_prompt: t.Optional[str] = None,     client: t.Optional[t.Any] = None, ) -> OCIGenAIWrapper:     """     Factory function to create an OCI Gen AI LLM instance.      Args:         model_id: The OCI model ID to use for generation         compartment_id: The OCI compartment ID         config: OCI configuration dictionary (optional)         endpoint_id: Optional endpoint ID for the model         run_config: Ragas run configuration         **kwargs: Additional arguments passed to OCIGenAIWrapper      Returns:         OCIGenAIWrapper: An instance of the OCI Gen AI LLM wrapper      Examples:         # Basic usage with default config         llm = oci_genai_factory(             model_id="cohere.command",             compartment_id="ocid1.compartment.oc1..example"         )          # With custom config         llm = oci_genai_factory(             model_id="cohere.command",             compartment_id="ocid1.compartment.oc1..example",             config={"user": "user_ocid", "key_file": "~/.oci/private_key.pem"}         )     """     return OCIGenAIWrapper(         model_id=model_id,         compartment_id=compartment_id,         config=config,         endpoint_id=endpoint_id,         run_config=run_config,         cache=cache,         default_system_prompt=default_system_prompt,         client=client,     ) ``` |

November 28, 2025




November 28, 2025

Back to top