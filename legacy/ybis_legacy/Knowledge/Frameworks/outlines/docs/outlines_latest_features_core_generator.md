Generator API - Outlines






[Skip to content](#generator)

# Generator

The `Generator` class is the core component of Outlines v1. `Generator` accepts a [model](../../models/) and an optional [output type](../output_types/). If no output type is provided, the `Generator` will return unstructured text.

Note

`Generator` is new as of Outlines v1, and replaces previous generator constructors:

* `generate.cfg`
* `generate.choice`
* `generate.format`
* `generate.fsm`
* `generate.json`
* `generate.regex`
* `generate.text`

## Methods

Generators implement the same methods as models:

* `__call__`
* `batch`
* `stream`

All of them take a single positional argument: the [model input](../inputs/) from which text is generated. Contrarily to the equivalent methods of models, you do not need to provide an output type as it has already been defined when initializing the generator.

## Basic Usage

```
from outlines import Generator, from_transformers
import transformers

# Initialize a model
model_name = "HuggingFaceTB/SmolLM2-135M-Instruct"
model = from_transformers(
    transformers.AutoModelForCausalLM.from_pretrained(model_name),
    transformers.AutoTokenizer.from_pretrained(model_name),
)

# Create a generator for plain text
generator = Generator(model)
result = generator("Write a short poem about AI.")

# Print the result
print(result)
```

## Structured Generation

```
from pydantic import BaseModel
from outlines import Generator, from_transformers
import transformers

# Define a Pydantic model for structured output
class BookRecommendation(BaseModel):
    title: str
    author: str
    year: int

# Initialize a model
model_name = "HuggingFaceTB/SmolLM2-135M-Instruct"
model = from_transformers(
    transformers.AutoModelForCausalLM.from_pretrained(model_name),
    transformers.AutoTokenizer.from_pretrained(model_name),
)

# Create a generator for JSON output
generator = Generator(model, BookRecommendation)

# Generate a book recommendation
result = generator("Recommend a science fiction book.")

# Parse the JSON result into a Pydantic model
book = BookRecommendation.model_validate_json(result)
print(f"{book.title} by {book.author} ({book.year})")
```

## Parameters

* `model`: The language model to use for generation
* `output_type`: Optional. The type of output to generate

## Generation Parameters

When calling the generator, you can pass additional parameters to control the generation process. These parameters are passed through to the underlying model, so they depend on the specific model being used.

Common parameters for most models include:
- `max_new_tokens`: Maximum number of tokens to generate
- `temperature`: Controls randomness (higher values = more random)
- `top_p`: Controls diversity via nucleus sampling
- `stop_strings`: String or list of strings at which to stop generation

Example:

```
result = generator(
    "Write a short story.",
    max_new_tokens=200,
    temperature=0.7,
    top_p=0.9,
    stop_strings=["THE END", "###"]
)
```

## Return Value

The generator always returns a raw string containing the generated text. When generating structured outputs, you need to parse this string into the desired format.

Unlike in Outlines v0, where the return type could be a parsed object, in v1 you are responsible for parsing the output when needed:

```
# Outlines v1 approach
from pydantic import BaseModel
from outlines import Generator

class Person(BaseModel):
    name: str
    age: int

generator = Generator(model, Person)
result = generator("Generate a person:")

# Parse the result yourself
person = Person.model_validate_json(result)
```

Create a generator for the given model and output parameters.

The 2 parameters output\_type and processor are mutually exclusive. The
parameters processor is only supported for SteerableModel instances
(typically local models) and is intended to be only used by advanced users.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model` | `Union[Model, AsyncModel]` | An instance of an Outlines model. | *required* |
| `output_type` | `Optional[Any]` | The output type expressed as a Python type or a type defined in the outlines.types.dsl module. | `None` |
| `backend` | `Optional[str]` | The name of the backend to use to create the logits processor. Only used for steerable models if there is an output type and `processor` is not provided. | `None` |
| `processor` | `Optional[LogitsProcessorType]` | An instance of a logits processor. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `Union[SteerableGenerator, BlackBoxGenerator, AsyncBlackBoxGenerator]` | A generator instance. |

Source code in `outlines/generator.py`

|  |  |
| --- | --- |
| ``` 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 ``` | ``` def Generator(     model: Union[Model, AsyncModel],     output_type: Optional[Any] = None,     backend: Optional[str] = None,     *,     processor: Optional[LogitsProcessorType] = None, ) -> Union[SteerableGenerator, BlackBoxGenerator, AsyncBlackBoxGenerator]:     """Create a generator for the given model and output parameters.      The 2 parameters output_type and processor are mutually exclusive. The     parameters processor is only supported for SteerableModel instances     (typically local models) and is intended to be only used by advanced users.      Parameters     ----------     model         An instance of an Outlines model.     output_type         The output type expressed as a Python type or a type defined in the         outlines.types.dsl module.     backend         The name of the backend to use to create the logits processor. Only         used for steerable models if there is an output type and `processor` is         not provided.     processor         An instance of a logits processor.      Returns     -------     Union[SteerableGenerator, BlackBoxGenerator, AsyncBlackBoxGenerator]         A generator instance.      """     provided_output_params = sum(         param is not None         for param in [output_type, processor]     )     if provided_output_params > 1:         raise ValueError(             "At most one of output_type or processor can be provided"         )      if isinstance(model, SteerableModel): # type: ignore         if processor is not None:             return SteerableGenerator.from_processor(model, processor) # type: ignore         else:             return SteerableGenerator(model, output_type, backend) # type: ignore     else:         if processor is not None:             raise NotImplementedError(                 "This model does not support logits processors"             )         if isinstance(model, AsyncBlackBoxModel): # type: ignore             return AsyncBlackBoxGenerator(model, output_type) # type: ignore         elif isinstance(model, BlackBoxModel): # type: ignore             return BlackBoxGenerator(model, output_type) # type: ignore         else:             raise ValueError(                 "The model argument must be an instance of "                 "SteerableModel, BlackBoxModel or AsyncBlackBoxModel"             ) ``` |

2025-07-10




2025-05-08




GitHub