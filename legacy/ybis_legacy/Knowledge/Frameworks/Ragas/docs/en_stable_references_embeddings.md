Embeddings - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.embeddings)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Embeddings

## BaseRagasEmbedding

```
BaseRagasEmbedding(cache: Optional[CacheInterface] = None)
```

Bases: `ABC`

Modern abstract base class for Ragas embedding implementations.

This class provides a consistent interface for embedding text using various
providers. Implementations should provide both sync and async methods for
embedding single texts, with batch methods automatically provided.

Args:
cache: Optional cache backend for caching embeddings.
Use DiskCacheBackend() for persistent caching.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 37 38 39 40 41 42 43 44 45 46 47 48 ``` | ``` def __init__(self, cache: t.Optional[CacheInterface] = None):     """Initialize embedding with optional caching.      Args:         cache: Optional cache backend for caching embeddings.             Use DiskCacheBackend() for persistent caching.     """     self.cache = cache      if self.cache is not None:         self.embed_text = cacher(cache_backend=self.cache)(self.embed_text)         self.aembed_text = cacher(cache_backend=self.cache)(self.aembed_text) ``` |

### embed\_text `abstractmethod`

```
embed_text(text: str, **kwargs: Any) -> List[float]
```

Embed a single text.

Args:
text: The text to embed
\*\*kwargs: Additional arguments for the embedding call

Returns:
List of floats representing the embedding

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 50 51 52 53 54 55 56 57 58 59 60 61 ``` | ``` @abstractmethod def embed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Embed a single text.      Args:         text: The text to embed         **kwargs: Additional arguments for the embedding call      Returns:         List of floats representing the embedding     """     pass ``` |

### aembed\_text `abstractmethod` `async`

```
aembed_text(text: str, **kwargs: Any) -> List[float]
```

Asynchronously embed a single text.

Args:
text: The text to embed
\*\*kwargs: Additional arguments for the embedding call

Returns:
List of floats representing the embedding

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 63 64 65 66 67 68 69 70 71 72 73 74 ``` | ``` @abstractmethod async def aembed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Asynchronously embed a single text.      Args:         text: The text to embed         **kwargs: Additional arguments for the embedding call      Returns:         List of floats representing the embedding     """     pass ``` |

### embed\_texts

```
embed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Embed multiple texts.

Default implementation processes texts individually. Override for
batch optimization.

Args:
texts: List of texts to embed
\*\*kwargs: Additional arguments for the embedding calls

Returns:
List of embeddings, one for each input text

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 ``` | ``` def embed_texts(self, texts: t.List[str], **kwargs: t.Any) -> t.List[t.List[float]]:     """Embed multiple texts.      Default implementation processes texts individually. Override for     batch optimization.      Args:         texts: List of texts to embed         **kwargs: Additional arguments for the embedding calls      Returns:         List of embeddings, one for each input text     """     texts = validate_texts(texts)     return [self.embed_text(text, **kwargs) for text in texts] ``` |

### aembed\_texts `async`

```
aembed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Asynchronously embed multiple texts.

Default implementation processes texts concurrently. Override for
batch optimization.

Args:
texts: List of texts to embed
\*\*kwargs: Additional arguments for the embedding calls

Returns:
List of embeddings, one for each input text

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ```  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 ``` | ``` async def aembed_texts(     self, texts: t.List[str], **kwargs: t.Any ) -> t.List[t.List[float]]:     """Asynchronously embed multiple texts.      Default implementation processes texts concurrently. Override for     batch optimization.      Args:         texts: List of texts to embed         **kwargs: Additional arguments for the embedding calls      Returns:         List of embeddings, one for each input text     """     texts = validate_texts(texts)     tasks = [self.aembed_text(text, **kwargs) for text in texts]     return await asyncio.gather(*tasks) ``` |

## BaseRagasEmbeddings

```
BaseRagasEmbeddings(cache: Optional[CacheInterface] = None)
```

Bases: `Embeddings`, `ABC`

Abstract base class for Ragas embeddings.

This class extends the Embeddings class and provides methods for embedding
text and managing run configurations.

Attributes:
run\_config (RunConfig): Configuration for running the embedding operations.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 197 198 199 200 201 202 203 204 205 206 207 208 ``` | ``` def __init__(self, cache: t.Optional[CacheInterface] = None):     super().__init__()     self.cache = cache     if self.cache is not None:         self.embed_query = cacher(cache_backend=self.cache)(self.embed_query)         self.embed_documents = cacher(cache_backend=self.cache)(             self.embed_documents         )         self.aembed_query = cacher(cache_backend=self.cache)(self.aembed_query)         self.aembed_documents = cacher(cache_backend=self.cache)(             self.aembed_documents         ) ``` |

### embed\_text `async`

```
embed_text(text: str, is_async=True) -> List[float]
```

Embed a single text string.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 210 211 212 213 214 215 ``` | ``` async def embed_text(self, text: str, is_async=True) -> t.List[float]:     """     Embed a single text string.     """     embs = await self.embed_texts([text], is_async=is_async)     return embs[0] ``` |

### embed\_texts `async`

```
embed_texts(texts: List[str], is_async: bool = True) -> List[List[float]]
```

Embed multiple texts.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 ``` | ``` async def embed_texts(     self, texts: t.List[str], is_async: bool = True ) -> t.List[t.List[float]]:     """     Embed multiple texts.     """     if is_async:         aembed_documents_with_retry = add_async_retry(             self.aembed_documents, self.run_config         )         return await aembed_documents_with_retry(texts)     else:         loop = asyncio.get_event_loop()         embed_documents_with_retry = add_retry(             self.embed_documents, self.run_config         )         return await loop.run_in_executor(None, embed_documents_with_retry, texts) ``` |

### set\_run\_config

```
set_run_config(run_config: RunConfig)
```

Set the run configuration for the embedding operations.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 241 242 243 244 245 ``` | ``` def set_run_config(self, run_config: RunConfig):     """     Set the run configuration for the embedding operations.     """     self.run_config = run_config ``` |

## HuggingfaceEmbeddings

```
HuggingfaceEmbeddings(cache: Optional[CacheInterface] = None)
```

Bases: `BaseRagasEmbeddings`

Hugging Face embeddings class for generating embeddings using pre-trained models.

This class provides functionality to load and use Hugging Face models for
generating embeddings of text inputs.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model_name` | `str` | Name of the pre-trained model to use, by default DEFAULT\_MODEL\_NAME. | *required* |
| `cache_folder` | `str` | Path to store downloaded models. Can also be set by SENTENCE\_TRANSFORMERS\_HOME environment variable. | *required* |
| `model_kwargs` | `dict` | Additional keyword arguments to pass to the model. | *required* |
| `encode_kwargs` | `dict` | Additional keyword arguments to pass to the encoding method. | *required* |

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `model` | `Union[SentenceTransformer, CrossEncoder]` | The loaded Hugging Face model. |
| `is_cross_encoder` | `bool` | Flag indicating whether the model is a cross-encoder. |

Methods:

| Name | Description |
| --- | --- |
| `embed_query` | Embed a single query text. |
| `embed_documents` | Embed multiple documents. |
| `predict` | Make predictions using a cross-encoder model. |

Notes

This class requires the `sentence_transformers` and `transformers` packages
to be installed.

Examples:

```
>>> embeddings = HuggingfaceEmbeddings(model_name="bert-base-uncased")
>>> query_embedding = embeddings.embed_query("What is the capital of France?")
>>> doc_embeddings = embeddings.embed_documents(["Paris is the capital of France.", "London is the capital of the UK."])
```

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 197 198 199 200 201 202 203 204 205 206 207 208 ``` | ``` def __init__(self, cache: t.Optional[CacheInterface] = None):     super().__init__()     self.cache = cache     if self.cache is not None:         self.embed_query = cacher(cache_backend=self.cache)(self.embed_query)         self.embed_documents = cacher(cache_backend=self.cache)(             self.embed_documents         )         self.aembed_query = cacher(cache_backend=self.cache)(self.aembed_query)         self.aembed_documents = cacher(cache_backend=self.cache)(             self.aembed_documents         ) ``` |

### embed\_query

```
embed_query(text: str) -> List[float]
```

Embed a single query text.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 485 486 487 488 489 ``` | ``` def embed_query(self, text: str) -> t.List[float]:     """     Embed a single query text.     """     return self.embed_documents([text])[0] ``` |

### embed\_documents

```
embed_documents(texts: List[str]) -> List[List[float]]
```

Embed multiple documents.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 ``` | ``` def embed_documents(self, texts: t.List[str]) -> t.List[t.List[float]]:     """     Embed multiple documents.     """     from sentence_transformers.SentenceTransformer import SentenceTransformer     from torch import Tensor      assert isinstance(self.model, SentenceTransformer), (         "Model is not of the type Bi-encoder"     )     embeddings = self.model.encode(         texts, normalize_embeddings=True, **self.encode_kwargs     )      assert isinstance(embeddings, Tensor)     return embeddings.tolist() ``` |

### predict

```
predict(texts: List[List[str]]) -> List[List[float]]
```

Make predictions using a cross-encoder model.

Source code in `src/ragas/embeddings/base.py`

|  |  |
| --- | --- |
| ``` 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 ``` | ``` def predict(self, texts: t.List[t.List[str]]) -> t.List[t.List[float]]:     """     Make predictions using a cross-encoder model.     """     from sentence_transformers.cross_encoder import CrossEncoder     from torch import Tensor      assert isinstance(self.model, CrossEncoder), (         "Model is not of the type CrossEncoder"     )      predictions = self.model.predict(texts, **self.encode_kwargs)      assert isinstance(predictions, Tensor)     return predictions.tolist() ``` |

## GoogleEmbeddings

```
GoogleEmbeddings(client: Optional[Any] = None, model: str = 'gemini-embedding-001', use_vertex: bool = False, project_id: Optional[str] = None, location: Optional[str] = 'us-central1', cache: Optional[CacheInterface] = None, **kwargs: Any)
```

Bases: `BaseRagasEmbedding`

Google embeddings using Vertex AI or Google AI (Gemini).

Supports both Vertex AI and Google AI (Gemini) embedding models.
For Vertex AI, requires google-cloud-aiplatform package.
For Google AI, supports both:
- New SDK (google-genai): Recommended, uses genai.Client()
- Old SDK (google-generativeai): Deprecated (support ends Aug 2025)

The client parameter is flexible:
- For new SDK: genai.Client(api\_key="...") instance
- For old SDK: None (auto-imports), the genai module, or a GenerativeModel instance
- For Vertex: Should be the configured vertex client

Note: Unlike LLM generation, embeddings work correctly with both SDKs.
The known instructor safety settings issue (github.com/567-labs/instructor/issues/1658)
only affects LLM generation, not embeddings.

Examples:
# New SDK (google-genai) - recommended
from google import genai
client = genai.Client(api\_key="...")
embeddings = GoogleEmbeddings(client=client, model="gemini-embedding-001")

```
# Old SDK (google-generativeai) - deprecated
import google.generativeai as genai
genai.configure(api_key="...")
embeddings = GoogleEmbeddings(client=genai, model="text-embedding-004")

# Auto-import (tries new SDK first, falls back to old)
embeddings = GoogleEmbeddings(model="text-embedding-004")
```

Source code in `src/ragas/embeddings/google_provider.py`

|  |  |
| --- | --- |
| ``` 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 ``` | ``` def __init__(     self,     client: t.Optional[t.Any] = None,     model: str = "gemini-embedding-001",     use_vertex: bool = False,     project_id: t.Optional[str] = None,     location: t.Optional[str] = "us-central1",     cache: t.Optional[CacheInterface] = None,     **kwargs: t.Any, ):     super().__init__(cache=cache)     self._original_client = client     self.model = model     self.use_vertex = use_vertex     self.project_id = project_id     self.location = location     self.kwargs = kwargs      # Track which SDK is being used (new google-genai vs old google-generativeai)     self._use_new_sdk = False      # Resolve the actual client to use     self.client = self._resolve_client(client, use_vertex) ``` |

### embed\_text

```
embed_text(text: str, **kwargs: Any) -> List[float]
```

Embed a single text using Google's embedding service.

Source code in `src/ragas/embeddings/google_provider.py`

|  |  |
| --- | --- |
| ``` 206 207 208 209 210 211 ``` | ``` def embed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Embed a single text using Google's embedding service."""     if self.use_vertex:         return self._embed_text_vertex(text, **kwargs)     else:         return self._embed_text_genai(text, **kwargs) ``` |

### aembed\_text `async`

```
aembed_text(text: str, **kwargs: Any) -> List[float]
```

Asynchronously embed a single text using Google's embedding service.

Google's SDK doesn't provide native async support, so we use ThreadPoolExecutor.

Source code in `src/ragas/embeddings/google_provider.py`

|  |  |
| --- | --- |
| ``` 249 250 251 252 253 254 ``` | ``` async def aembed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Asynchronously embed a single text using Google's embedding service.      Google's SDK doesn't provide native async support, so we use ThreadPoolExecutor.     """     return await run_sync_in_async(self.embed_text, text, **kwargs) ``` |

### embed\_texts

```
embed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Embed multiple texts using Google's embedding service.

Source code in `src/ragas/embeddings/google_provider.py`

|  |  |
| --- | --- |
| ``` 256 257 258 259 260 261 262 263 264 265 ``` | ``` def embed_texts(self, texts: t.List[str], **kwargs: t.Any) -> t.List[t.List[float]]:     """Embed multiple texts using Google's embedding service."""     texts = validate_texts(texts)     if not texts:         return []      if self.use_vertex:         return self._embed_texts_vertex(texts, **kwargs)     else:         return self._embed_texts_genai(texts, **kwargs) ``` |

### aembed\_texts `async`

```
aembed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Asynchronously embed multiple texts using Google's embedding service.

Source code in `src/ragas/embeddings/google_provider.py`

|  |  |
| --- | --- |
| ``` 303 304 305 306 307 308 309 310 311 ``` | ``` async def aembed_texts(     self, texts: t.List[str], **kwargs: t.Any ) -> t.List[t.List[float]]:     """Asynchronously embed multiple texts using Google's embedding service."""     texts = validate_texts(texts)     if not texts:         return []      return await run_sync_in_async(self.embed_texts, texts, **kwargs) ``` |

## HaystackEmbeddingsWrapper

```
HaystackEmbeddingsWrapper(embedder: Any, run_config: Optional[RunConfig] = None, cache: Optional[CacheInterface] = None)
```

Bases: `BaseRagasEmbeddings`

A wrapper for using Haystack embedders within the Ragas framework.

This class allows you to use both synchronous and asynchronous methods
(`embed_query`/`embed_documents` and `aembed_query`/`aembed_documents`)
for generating embeddings through a Haystack embedder.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `embedder` | `AzureOpenAITextEmbedder | HuggingFaceAPITextEmbedder | OpenAITextEmbedder | SentenceTransformersTextEmbedder` | An instance of a supported Haystack embedder class. | *required* |
| `run_config` | `RunConfig` | A configuration object to manage embedding execution settings, by default None. | `None` |
| `cache` | `CacheInterface` | A cache instance for storing and retrieving embedding results, by default None. | `None` |

Source code in `src/ragas/embeddings/haystack_wrapper.py`

|  |  |
| --- | --- |
| ``` 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 ``` | ``` def __init__(     self,     embedder: t.Any,     run_config: t.Optional[RunConfig] = None,     cache: t.Optional[CacheInterface] = None, ):     super().__init__(cache=cache)      # Lazy Import of required Haystack components     try:         from haystack import AsyncPipeline         from haystack.components.embedders.azure_text_embedder import (             AzureOpenAITextEmbedder,         )         from haystack.components.embedders.hugging_face_api_text_embedder import (             HuggingFaceAPITextEmbedder,         )         from haystack.components.embedders.openai_text_embedder import (             OpenAITextEmbedder,         )         from haystack.components.embedders.sentence_transformers_text_embedder import (             SentenceTransformersTextEmbedder,         )     except ImportError as exc:         raise ImportError(             "Haystack is not installed. Please install it with `pip install haystack-ai`."         ) from exc      # Validate embedder type     if not isinstance(         embedder,         (             AzureOpenAITextEmbedder,             HuggingFaceAPITextEmbedder,             OpenAITextEmbedder,             SentenceTransformersTextEmbedder,         ),     ):         raise TypeError(             "Expected 'embedder' to be one of: AzureOpenAITextEmbedder, "             "HuggingFaceAPITextEmbedder, OpenAITextEmbedder, or "             f"SentenceTransformersTextEmbedder, but got {type(embedder).__name__}."         )      self.embedder = embedder      # Initialize an asynchronous pipeline and add the embedder component     self.async_pipeline = AsyncPipeline()     self.async_pipeline.add_component("embedder", self.embedder)      # Set or create the run configuration     if run_config is None:         run_config = RunConfig()     self.set_run_config(run_config) ``` |

## HuggingFaceEmbeddings

```
HuggingFaceEmbeddings(model: str, use_api: bool = False, api_key: Optional[str] = None, device: Optional[str] = None, normalize_embeddings: bool = True, batch_size: int = 32, cache: Optional[CacheInterface] = None, **model_kwargs: Any)
```

Bases: `BaseRagasEmbedding`

HuggingFace embeddings supporting both local and API-based models.

Supports sentence-transformers for local models and HuggingFace API for
hosted models. Provides efficient batch processing and caching.

Source code in `src/ragas/embeddings/huggingface_provider.py`

|  |  |
| --- | --- |
| ``` 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 ``` | ``` def __init__(     self,     model: str,     use_api: bool = False,     api_key: t.Optional[str] = None,     device: t.Optional[str] = None,     normalize_embeddings: bool = True,     batch_size: int = 32,     cache: t.Optional[CacheInterface] = None,     **model_kwargs: t.Any, ):     super().__init__(cache=cache)     self.model = model     self.use_api = use_api     self.api_key = api_key     self.device = device     self.normalize_embeddings = normalize_embeddings     self.batch_size = batch_size     self.model_kwargs = model_kwargs      if use_api:         self._setup_api_client()     else:         self._setup_local_model() ``` |

### embed\_text

```
embed_text(text: str, **kwargs: Any) -> List[float]
```

Embed a single text using HuggingFace.

Source code in `src/ragas/embeddings/huggingface_provider.py`

|  |  |
| --- | --- |
| ``` 75 76 77 78 79 80 ``` | ``` def embed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Embed a single text using HuggingFace."""     if self.use_api:         return self._embed_text_api(text, **kwargs)     else:         return self._embed_text_local(text, **kwargs) ``` |

### aembed\_text `async`

```
aembed_text(text: str, **kwargs: Any) -> List[float]
```

Asynchronously embed a single text using HuggingFace.

Source code in `src/ragas/embeddings/huggingface_provider.py`

|  |  |
| --- | --- |
| ```  97  98  99 100 101 102 ``` | ``` async def aembed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Asynchronously embed a single text using HuggingFace."""     if self.use_api:         return await self._aembed_text_api(text, **kwargs)     else:         return await run_sync_in_async(self._embed_text_local, text, **kwargs) ``` |

### embed\_texts

```
embed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Embed multiple texts using HuggingFace with batching.

Source code in `src/ragas/embeddings/huggingface_provider.py`

|  |  |
| --- | --- |
| ``` 109 110 111 112 113 114 115 116 117 118 ``` | ``` def embed_texts(self, texts: t.List[str], **kwargs: t.Any) -> t.List[t.List[float]]:     """Embed multiple texts using HuggingFace with batching."""     texts = validate_texts(texts)     if not texts:         return []      if self.use_api:         return self._embed_texts_api(texts, **kwargs)     else:         return self._embed_texts_local(texts, **kwargs) ``` |

### aembed\_texts `async`

```
aembed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Asynchronously embed multiple texts using HuggingFace.

Source code in `src/ragas/embeddings/huggingface_provider.py`

|  |  |
| --- | --- |
| ``` 152 153 154 155 156 157 158 159 160 161 162 163 ``` | ``` async def aembed_texts(     self, texts: t.List[str], **kwargs: t.Any ) -> t.List[t.List[float]]:     """Asynchronously embed multiple texts using HuggingFace."""     texts = validate_texts(texts)     if not texts:         return []      if self.use_api:         return await run_sync_in_async(self._embed_texts_api, texts, **kwargs)     else:         return await run_sync_in_async(self._embed_texts_local, texts, **kwargs) ``` |

## LiteLLMEmbeddings

```
LiteLLMEmbeddings(model: str, api_key: Optional[str] = None, api_base: Optional[str] = None, api_version: Optional[str] = None, timeout: int = 600, max_retries: int = 3, batch_size: Optional[int] = None, cache: Optional[CacheInterface] = None, **litellm_params: Any)
```

Bases: `BaseRagasEmbedding`

Universal embedding interface using LiteLLM.

Supports 100+ models across OpenAI, Azure, Google, Cohere, Anthropic, and more.
Provides intelligent batching and provider-specific optimizations.

Source code in `src/ragas/embeddings/litellm_provider.py`

|  |  |
| --- | --- |
| ``` 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 ``` | ``` def __init__(     self,     model: str,     api_key: t.Optional[str] = None,     api_base: t.Optional[str] = None,     api_version: t.Optional[str] = None,     timeout: int = 600,     max_retries: int = 3,     batch_size: t.Optional[int] = None,     cache: t.Optional[CacheInterface] = None,     **litellm_params: t.Any, ):     super().__init__(cache=cache)     self.litellm = safe_import("litellm", "litellm")     self.model = model     self.api_key = api_key     self.api_base = api_base     self.api_version = api_version     self.timeout = timeout     self.max_retries = max_retries     self.batch_size = batch_size or get_optimal_batch_size("litellm", model)     self.litellm_params = litellm_params ``` |

### embed\_text

```
embed_text(text: str, **kwargs: Any) -> List[float]
```

Embed a single text using LiteLLM.

Source code in `src/ragas/embeddings/litellm_provider.py`

|  |  |
| --- | --- |
| ``` 63 64 65 66 67 ``` | ``` def embed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Embed a single text using LiteLLM."""     call_kwargs = self._prepare_kwargs(**kwargs)     response = self.litellm.embedding(input=[text], **call_kwargs)     return response.data[0]["embedding"] ``` |

### aembed\_text `async`

```
aembed_text(text: str, **kwargs: Any) -> List[float]
```

Asynchronously embed a single text using LiteLLM.

Source code in `src/ragas/embeddings/litellm_provider.py`

|  |  |
| --- | --- |
| ``` 69 70 71 72 73 ``` | ``` async def aembed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Asynchronously embed a single text using LiteLLM."""     call_kwargs = self._prepare_kwargs(**kwargs)     response = await self.litellm.aembedding(input=[text], **call_kwargs)     return response.data[0]["embedding"] ``` |

### embed\_texts

```
embed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Embed multiple texts using LiteLLM with intelligent batching.

Source code in `src/ragas/embeddings/litellm_provider.py`

|  |  |
| --- | --- |
| ``` 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 ``` | ``` def embed_texts(self, texts: t.List[str], **kwargs: t.Any) -> t.List[t.List[float]]:     """Embed multiple texts using LiteLLM with intelligent batching."""     texts = validate_texts(texts)     if not texts:         return []      embeddings = []     batches = batch_texts(texts, self.batch_size)      for batch in batches:         call_kwargs = self._prepare_kwargs(**kwargs)         response = self.litellm.embedding(input=batch, **call_kwargs)         embeddings.extend([item["embedding"] for item in response.data])      return embeddings ``` |

### aembed\_texts `async`

```
aembed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Asynchronously embed multiple texts using LiteLLM with intelligent batching.

Source code in `src/ragas/embeddings/litellm_provider.py`

|  |  |
| --- | --- |
| ```  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 ``` | ``` async def aembed_texts(     self, texts: t.List[str], **kwargs: t.Any ) -> t.List[t.List[float]]:     """Asynchronously embed multiple texts using LiteLLM with intelligent batching."""     texts = validate_texts(texts)     if not texts:         return []      embeddings = []     batches = batch_texts(texts, self.batch_size)      for batch in batches:         call_kwargs = self._prepare_kwargs(**kwargs)         response = await self.litellm.aembedding(input=batch, **call_kwargs)         embeddings.extend([item["embedding"] for item in response.data])      return embeddings ``` |

## OpenAIEmbeddings

```
OpenAIEmbeddings(client: Any, model: str = 'text-embedding-3-small', cache: Optional[CacheInterface] = None)
```

Bases: `BaseRagasEmbedding`

OpenAI embeddings implementation with batch optimization.

Supports both sync and async OpenAI clients with automatic detection.
Provides optimized batch processing for better performance.

Source code in `src/ragas/embeddings/openai_provider.py`

|  |  |
| --- | --- |
| ``` 21 22 23 24 25 26 27 28 29 30 ``` | ``` def __init__(     self,     client: t.Any,     model: str = "text-embedding-3-small",     cache: t.Optional[CacheInterface] = None, ):     super().__init__(cache=cache)     self.client = client     self.model = model     self.is_async = self._check_client_async(client) ``` |

### embed\_text

```
embed_text(text: str, **kwargs: Any) -> List[float]
```

Embed a single text using OpenAI.

For async clients, this will run the async method in the appropriate event loop.

Source code in `src/ragas/embeddings/openai_provider.py`

|  |  |
| --- | --- |
| ``` 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 ``` | ``` def embed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Embed a single text using OpenAI.      For async clients, this will run the async method in the appropriate event loop.     """     if self.is_async:         result = self._run_async_in_current_loop(self.aembed_text(text, **kwargs))     else:         response = self.client.embeddings.create(             input=text, model=self.model, **kwargs         )         result = response.data[0].embedding      # Track usage     track(         EmbeddingUsageEvent(             provider="openai",             model=self.model,             embedding_type="modern",             num_requests=1,             is_async=self.is_async,         )     )     return result ``` |

### aembed\_text `async`

```
aembed_text(text: str, **kwargs: Any) -> List[float]
```

Asynchronously embed a single text using OpenAI.

Source code in `src/ragas/embeddings/openai_provider.py`

|  |  |
| --- | --- |
| ``` 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 ``` | ``` async def aembed_text(self, text: str, **kwargs: t.Any) -> t.List[float]:     """Asynchronously embed a single text using OpenAI."""     if not self.is_async:         raise TypeError(             "Cannot use aembed_text() with a synchronous client. Use embed_text() instead."         )      response = await self.client.embeddings.create(         input=text, model=self.model, **kwargs     )     result = response.data[0].embedding      # Track usage     track(         EmbeddingUsageEvent(             provider="openai",             model=self.model,             embedding_type="modern",             num_requests=1,             is_async=True,         )     )     return result ``` |

### embed\_texts

```
embed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Embed multiple texts using OpenAI's batch API for optimization.

Source code in `src/ragas/embeddings/openai_provider.py`

|  |  |
| --- | --- |
| ```  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 ``` | ``` def embed_texts(self, texts: t.List[str], **kwargs: t.Any) -> t.List[t.List[float]]:     """Embed multiple texts using OpenAI's batch API for optimization."""     texts = validate_texts(texts)     if not texts:         return []      if self.is_async:         result = self._run_async_in_current_loop(self.aembed_texts(texts, **kwargs))     else:         # OpenAI supports batch embedding natively         response = self.client.embeddings.create(             input=texts, model=self.model, **kwargs         )         result = [item.embedding for item in response.data]      # Track usage     track(         EmbeddingUsageEvent(             provider="openai",             model=self.model,             embedding_type="modern",             num_requests=len(texts),             is_async=self.is_async,         )     )     return result ``` |

### aembed\_texts `async`

```
aembed_texts(texts: List[str], **kwargs: Any) -> List[List[float]]
```

Asynchronously embed multiple texts using OpenAI's batch API.

Source code in `src/ragas/embeddings/openai_provider.py`

|  |  |
| --- | --- |
| ``` 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 ``` | ``` async def aembed_texts(     self, texts: t.List[str], **kwargs: t.Any ) -> t.List[t.List[float]]:     """Asynchronously embed multiple texts using OpenAI's batch API."""     texts = validate_texts(texts)     if not texts:         return []      if not self.is_async:         raise TypeError(             "Cannot use aembed_texts() with a synchronous client. Use embed_texts() instead."         )      response = await self.client.embeddings.create(         input=texts, model=self.model, **kwargs     )     result = [item.embedding for item in response.data]      # Track usage     track(         EmbeddingUsageEvent(             provider="openai",             model=self.model,             embedding_type="modern",             num_requests=len(texts),             is_async=True,         )     )     return result ``` |

## batch\_texts

```
batch_texts(texts: List[str], batch_size: int) -> List[List[str]]
```

Batch a list of texts into smaller chunks.

Args:
texts: List of texts to batch
batch\_size: Size of each batch

Returns:
List of batches, where each batch is a list of texts

Source code in `src/ragas/embeddings/utils.py`

|  |  |
| --- | --- |
| ```  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 ``` | ``` def batch_texts(texts: t.List[str], batch_size: int) -> t.List[t.List[str]]:     """Batch a list of texts into smaller chunks.      Args:         texts: List of texts to batch         batch_size: Size of each batch      Returns:         List of batches, where each batch is a list of texts     """     if batch_size <= 0:         raise ValueError("Batch size must be positive")      batches = []     for i in range(0, len(texts), batch_size):         batches.append(texts[i : i + batch_size])     return batches ``` |

## get\_optimal\_batch\_size

```
get_optimal_batch_size(provider: str, model: str) -> int
```

Get optimal batch size for a provider/model combination.

Args:
provider: The embedding provider
model: The model name

Returns:
Optimal batch size for the provider/model

Source code in `src/ragas/embeddings/utils.py`

|  |  |
| --- | --- |
| ``` 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 ``` | ``` def get_optimal_batch_size(provider: str, model: str) -> int:     """Get optimal batch size for a provider/model combination.      Args:         provider: The embedding provider         model: The model name      Returns:         Optimal batch size for the provider/model     """     provider_lower = provider.lower()      # Provider-specific batch sizes     if "openai" in provider_lower:         return 100  # OpenAI supports large batches     elif "cohere" in provider_lower:         return 96  # Cohere's documented limit     elif "google" in provider_lower or "vertex" in provider_lower:         return 5  # Google/Vertex AI is more conservative     elif "huggingface" in provider_lower:         return 32  # HuggingFace default     else:         return 10  # Conservative default for unknown providers ``` |

## validate\_texts

```
validate_texts(texts: Union[str, List[str]]) -> List[str]
```

Validate and normalize text inputs.

Args:
texts: Single text or list of texts

Returns:
List of validated texts

Raises:
ValueError: If texts are invalid

Source code in `src/ragas/embeddings/utils.py`

|  |  |
| --- | --- |
| ``` 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 ``` | ``` def validate_texts(texts: t.Union[str, t.List[str]]) -> t.List[str]:     """Validate and normalize text inputs.      Args:         texts: Single text or list of texts      Returns:         List of validated texts      Raises:         ValueError: If texts are invalid     """     if isinstance(texts, str):         texts = [texts]      if not isinstance(texts, list):         raise ValueError("Texts must be a string or list of strings")      if not texts:         raise ValueError("Texts list cannot be empty")      for i, text in enumerate(texts):         if not isinstance(text, str):             raise ValueError(f"Text at index {i} must be a string, got {type(text)}")         if not text.strip():             raise ValueError(f"Text at index {i} cannot be empty or whitespace only")      return texts ``` |

## embedding\_factory

```
embedding_factory(*args, **kwargs)
```

Deprecated: Use embedding\_factory from base module directly.

Source code in `src/ragas/embeddings/__init__.py`

|  |  |
| --- | --- |
| ``` 39 40 41 42 43 44 45 46 47 48 49 50 ``` | ``` def embedding_factory(*args, **kwargs):     """Deprecated: Use embedding_factory from base module directly."""     import warnings      warnings.warn(         "Importing embedding_factory from ragas.embeddings is deprecated. "         "Import directly from ragas.embeddings.base or use modern providers: "         "from ragas.embeddings import OpenAIEmbeddings, GoogleEmbeddings, HuggingFaceEmbeddings",         DeprecationWarning,         stacklevel=2,     )     return _embedding_factory(*args, **kwargs) ``` |

November 28, 2025




November 28, 2025

Back to top