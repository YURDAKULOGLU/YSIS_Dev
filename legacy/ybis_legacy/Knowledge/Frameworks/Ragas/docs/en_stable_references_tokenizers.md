Tokenizers - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#tokenizers)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Tokenizers

Ragas supports multiple tokenizer implementations for text splitting during knowledge graph operations and test data generation.

## Overview

When extracting properties from knowledge graph nodes, text is split into chunks based on token limits. By default, Ragas uses tiktoken (OpenAI's tokenizer), but you can also use HuggingFace tokenizers for better compatibility with open-source models.

## Available Tokenizers

### TiktokenWrapper

Wrapper for OpenAI's tiktoken tokenizers. This is the default tokenizer.

```
from ragas import TiktokenWrapper

# Using default encoding (o200k_base)
tokenizer = TiktokenWrapper()

# Using a specific encoding
tokenizer = TiktokenWrapper(encoding_name="cl100k_base")

# Using encoding for a specific model
tokenizer = TiktokenWrapper(model_name="gpt-4")
```

### HuggingFaceTokenizer

Wrapper for HuggingFace transformers tokenizers. Use this when working with open-source models.

```
from ragas import HuggingFaceTokenizer

# Load tokenizer for a specific model
tokenizer = HuggingFaceTokenizer(model_name="meta-llama/Llama-2-7b-hf")

# Use a pre-initialized tokenizer
from transformers import AutoTokenizer
hf_tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
tokenizer = HuggingFaceTokenizer(tokenizer=hf_tokenizer)
```

**Note:** HuggingFace tokenizers require the `transformers` package. Install it with:

```
pip install transformers
# or
uv add transformers
```

### Factory Function

Use `get_tokenizer()` for a simple way to create tokenizers:

```
from ragas import get_tokenizer

# Default tiktoken tokenizer
tokenizer = get_tokenizer()

# Tiktoken for a specific model
tokenizer = get_tokenizer("tiktoken", model_name="gpt-4")

# HuggingFace tokenizer
tokenizer = get_tokenizer("huggingface", model_name="meta-llama/Llama-2-7b-hf")
```

## Using Custom Tokenizers

### With LLM-based Extractors

All LLM-based extractors accept a `tokenizer` parameter:

```
from ragas import HuggingFaceTokenizer
from ragas.testset.transforms import (
    SummaryExtractor,
    KeyphrasesExtractor,
    HeadlinesExtractor,
)

# Create a HuggingFace tokenizer for your model
tokenizer = HuggingFaceTokenizer(model_name="meta-llama/Llama-2-7b-hf")

# Use it with extractors
summary_extractor = SummaryExtractor(llm=your_llm, tokenizer=tokenizer)
keyphrase_extractor = KeyphrasesExtractor(llm=your_llm, tokenizer=tokenizer)
headlines_extractor = HeadlinesExtractor(llm=your_llm, tokenizer=tokenizer)
```

### Custom Tokenizer Implementation

You can create your own tokenizer by extending `BaseTokenizer`:

```
from ragas.tokenizers import BaseTokenizer

class MyCustomTokenizer(BaseTokenizer):
    def __init__(self, ...):
        # Initialize your tokenizer
        pass

    def encode(self, text: str) -> list[int]:
        # Return token IDs
        pass

    def decode(self, tokens: list[int]) -> str:
        # Return decoded text
        pass
```

## API Reference

Tokenizer abstractions for Ragas.

This module provides a unified interface for different tokenizer implementations,
supporting both tiktoken (OpenAI) and HuggingFace tokenizers.

## BaseTokenizer

Bases: `ABC`

Abstract base class for tokenizers.

### encode `abstractmethod`

```
encode(text: str) -> List[int]
```

Encode text into token IDs.

Source code in `src/ragas/tokenizers.py`

|  |  |
| --- | --- |
| ``` 19 20 21 22 ``` | ``` @abstractmethod def encode(self, text: str) -> t.List[int]:     """Encode text into token IDs."""     pass ``` |

### decode `abstractmethod`

```
decode(tokens: List[int]) -> str
```

Decode token IDs back into text.

Source code in `src/ragas/tokenizers.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 ``` | ``` @abstractmethod def decode(self, tokens: t.List[int]) -> str:     """Decode token IDs back into text."""     pass ``` |

### count\_tokens

```
count_tokens(text: str) -> int
```

Count the number of tokens in text.

Source code in `src/ragas/tokenizers.py`

|  |  |
| --- | --- |
| ``` 29 30 31 ``` | ``` def count_tokens(self, text: str) -> int:     """Count the number of tokens in text."""     return len(self.encode(text)) ``` |

## TiktokenWrapper

```
TiktokenWrapper(encoding: Optional[Encoding] = None, model_name: Optional[str] = None, encoding_name: Optional[str] = None)
```

Bases: `BaseTokenizer`

Wrapper for tiktoken encodings (OpenAI tokenizers).

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `encoding` | `Encoding` | A pre-initialized tiktoken encoding. | `None` |
| `model_name` | `str` | Model name to get encoding for (e.g., "gpt-4", "gpt-3.5-turbo"). | `None` |
| `encoding_name` | `str` | Encoding name (e.g., "cl100k\_base", "o200k\_base"). | `None` |
| `If` |  |  | *required* |

Source code in `src/ragas/tokenizers.py`

|  |  |
| --- | --- |
| ``` 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 ``` | ``` def __init__(     self,     encoding: t.Optional[tiktoken.Encoding] = None,     model_name: t.Optional[str] = None,     encoding_name: t.Optional[str] = None, ):     """     Initialize TiktokenWrapper.      Parameters     ----------     encoding : tiktoken.Encoding, optional         A pre-initialized tiktoken encoding.     model_name : str, optional         Model name to get encoding for (e.g., "gpt-4", "gpt-3.5-turbo").     encoding_name : str, optional         Encoding name (e.g., "cl100k_base", "o200k_base").      If none provided, defaults to "o200k_base" encoding.     """     if encoding is not None:         self._encoding = encoding     elif model_name is not None:         self._encoding = tiktoken.encoding_for_model(model_name)     elif encoding_name is not None:         self._encoding = tiktoken.get_encoding(encoding_name)     else:         self._encoding = tiktoken.get_encoding("o200k_base") ``` |

### encoding `property`

```
encoding: Encoding
```

Access the underlying tiktoken encoding.

## HuggingFaceTokenizer

```
HuggingFaceTokenizer(tokenizer: Optional[Any] = None, model_name: Optional[str] = None)
```

Bases: `BaseTokenizer`

Wrapper for HuggingFace tokenizers.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `tokenizer` | `PreTrainedTokenizer or PreTrainedTokenizerFast` | A pre-initialized HuggingFace tokenizer. | `None` |
| `model_name` | `str` | Model name or path to load tokenizer from (e.g., "meta-llama/Llama-2-7b"). | `None` |
| `One` |  |  | *required* |

Source code in `src/ragas/tokenizers.py`

|  |  |
| --- | --- |
| ```  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 ``` | ``` def __init__(     self,     tokenizer: t.Optional[t.Any] = None,     model_name: t.Optional[str] = None, ):     """     Initialize HuggingFaceTokenizer.      Parameters     ----------     tokenizer : PreTrainedTokenizer or PreTrainedTokenizerFast, optional         A pre-initialized HuggingFace tokenizer.     model_name : str, optional         Model name or path to load tokenizer from (e.g., "meta-llama/Llama-2-7b").      One of tokenizer or model_name must be provided.     """     if tokenizer is not None:         self._tokenizer = tokenizer     elif model_name is not None:         try:             from transformers import AutoTokenizer         except ImportError:             raise ImportError(                 "transformers package is required for HuggingFace tokenizers. "                 "Install it with: pip install transformers"             )         self._tokenizer = AutoTokenizer.from_pretrained(model_name)     else:         raise ValueError("Either tokenizer or model_name must be provided") ``` |

### tokenizer `property`

```
tokenizer: Any
```

Access the underlying HuggingFace tokenizer.

## get\_tokenizer

```
get_tokenizer(tokenizer_type: str = 'tiktoken', model_name: Optional[str] = None, encoding_name: Optional[str] = None) -> BaseTokenizer
```

Factory function to get a tokenizer instance.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `tokenizer_type` | `str` | Type of tokenizer: "tiktoken" or "huggingface". | `'tiktoken'` |
| `model_name` | `str` | Model name for the tokenizer. | `None` |
| `encoding_name` | `str` | Encoding name (only for tiktoken). | `None` |

Returns:

| Type | Description |
| --- | --- |
| `BaseTokenizer` | A tokenizer instance. |

Examples:

```
>>> # Get default tiktoken tokenizer
>>> tokenizer = get_tokenizer()
```

```
>>> # Get tiktoken for a specific model
>>> tokenizer = get_tokenizer("tiktoken", model_name="gpt-4")
```

```
>>> # Get HuggingFace tokenizer
>>> tokenizer = get_tokenizer("huggingface", model_name="meta-llama/Llama-2-7b")
```

Source code in `src/ragas/tokenizers.py`

|  |  |
| --- | --- |
| ``` 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 ``` | ``` def get_tokenizer(     tokenizer_type: str = "tiktoken",     model_name: t.Optional[str] = None,     encoding_name: t.Optional[str] = None, ) -> BaseTokenizer:     """     Factory function to get a tokenizer instance.      Parameters     ----------     tokenizer_type : str         Type of tokenizer: "tiktoken" or "huggingface".     model_name : str, optional         Model name for the tokenizer.     encoding_name : str, optional         Encoding name (only for tiktoken).      Returns     -------     BaseTokenizer         A tokenizer instance.      Examples     --------     >>> # Get default tiktoken tokenizer     >>> tokenizer = get_tokenizer()      >>> # Get tiktoken for a specific model     >>> tokenizer = get_tokenizer("tiktoken", model_name="gpt-4")      >>> # Get HuggingFace tokenizer     >>> tokenizer = get_tokenizer("huggingface", model_name="meta-llama/Llama-2-7b")     """     if tokenizer_type == "tiktoken":         return TiktokenWrapper(model_name=model_name, encoding_name=encoding_name)     elif tokenizer_type == "huggingface":         if model_name is None:             raise ValueError("model_name is required for HuggingFace tokenizers")         return HuggingFaceTokenizer(model_name=model_name)     else:         raise ValueError(f"Unknown tokenizer type: {tokenizer_type}") ``` |

December 19, 2025




December 19, 2025

Back to top