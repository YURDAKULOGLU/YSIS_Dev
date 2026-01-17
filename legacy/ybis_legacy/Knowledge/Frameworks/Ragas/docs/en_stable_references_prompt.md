Prompt - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#prompt-api-reference)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Prompt API Reference

The prompt system in Ragas provides a flexible and type-safe way to define prompts for LLM-based metrics and other components. This page documents the core prompt classes and their usage.

## Overview

Ragas uses a modular prompt architecture based on the `BasePrompt` class. Prompts can be:

* **Input/Output Models**: Pydantic BaseModel classes that define the structure of prompt inputs and outputs
* **Prompt Classes**: Inherit from `BasePrompt` to define instructions, examples, and prompt generation logic
* **String Prompts**: Simple text-based prompts for backward compatibility

## Core Classes

## InputModel `module-attribute`

```
InputModel = TypeVar('InputModel', bound=BaseModel)
```

## OutputModel `module-attribute`

```
OutputModel = TypeVar('OutputModel', bound=BaseModel)
```

## BasePrompt

```
BasePrompt(name: Optional[str] = None, language: str = 'english', original_hash: Optional[str] = None)
```

Bases: `ABC`

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` def __init__(     self,     name: t.Optional[str] = None,     language: str = "english",     original_hash: t.Optional[str] = None, ):     if name is None:         self.name = camel_to_snake(self.__class__.__name__)      self.language = language     self.original_hash = original_hash ``` |

### generate `abstractmethod` `async`

```
generate(llm: BaseRagasLLM, data: Any, temperature: Optional[float] = None, stop: Optional[List[str]] = None, callbacks: Callbacks = []) -> Any
```

Generate a single completion from the prompt.

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 39 40 41 42 43 44 45 46 47 48 49 50 51 ``` | ``` @abstractmethod async def generate(     self,     llm: BaseRagasLLM,     data: t.Any,     temperature: t.Optional[float] = None,     stop: t.Optional[t.List[str]] = None,     callbacks: Callbacks = [], ) -> t.Any:     """     Generate a single completion from the prompt.     """     pass ``` |

### generate\_multiple `abstractmethod`

```
generate_multiple(llm: BaseRagasLLM, data: Any, n: int = 1, temperature: Optional[float] = None, stop: Optional[List[str]] = None, callbacks: Callbacks = []) -> Any
```

Generate multiple completions from the prompt.

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 53 54 55 56 57 58 59 60 61 62 63 64 65 66 ``` | ``` @abstractmethod def generate_multiple(     self,     llm: BaseRagasLLM,     data: t.Any,     n: int = 1,     temperature: t.Optional[float] = None,     stop: t.Optional[t.List[str]] = None,     callbacks: Callbacks = [], ) -> t.Any:     """     Generate multiple completions from the prompt.     """     pass ``` |

### save

```
save(file_path: str)
```

Save the prompt to a file.

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 68 69 70 71 72 73 74 75 76 77 78 79 80 81 ``` | ``` def save(self, file_path: str):     """     Save the prompt to a file.     """     data = {         "ragas_version": __version__,         "language": self.language,         "original_hash": self.original_hash,     }     if os.path.exists(file_path):         raise FileExistsError(f"The file '{file_path}' already exists.")     with open(file_path, "w", encoding="utf-8") as f:         json.dump(data, f, indent=2, ensure_ascii=False)         print(f"Prompt saved to {file_path}") ``` |

### load `classmethod`

```
load(file_path: str) -> 'BasePrompt'
```

Load the prompt from a file.

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ```  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 ``` | ``` @classmethod def load(cls, file_path: str) -> "BasePrompt":     """     Load the prompt from a file.     """     with open(file_path, "r", encoding="utf-8") as f:         data = json.load(f)      ragas_version = data.get("ragas_version")     if ragas_version != __version__:         logger.warning(             "Prompt was saved with Ragas v%s, but you are loading it with Ragas v%s. "             "There might be incompatibilities.",             ragas_version,             __version__,         )      prompt = cls(         language=data.get("language", "english"),         original_hash=data.get("original_hash"),     )      return prompt ``` |

## StringPrompt

```
StringPrompt(name: Optional[str] = None, language: str = 'english', original_hash: Optional[str] = None)
```

Bases: `BasePrompt`

A simple prompt that can be formatted with additional data using f-string syntax.

This prompt is a simpler alternative to PydanticPrompt for those who prefer a more
flexible approach without the need for a Pydantic model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `instruction` | `str` | The instruction string that can be formatted with additional data. | *required* |

Examples:

```
>>> from ragas.prompt import string_prompt
>>> await prompt.generate(llm=llm, data={"category": "commerce"})
```

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` def __init__(     self,     name: t.Optional[str] = None,     language: str = "english",     original_hash: t.Optional[str] = None, ):     if name is None:         self.name = camel_to_snake(self.__class__.__name__)      self.language = language     self.original_hash = original_hash ``` |

### generate `async`

```
generate(llm: BaseRagasLLM, data: str, temperature: Optional[float] = None, stop: Optional[List[str]] = None, callbacks: Callbacks = []) -> str
```

Generate text based on the instruction and provided data.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `llm` | `BaseRagasLLM` | The language model to use for text generation. | *required* |
| `data` | `Optional[Dict[str, Any]]` | The data to format the instruction with, by default None. | *required* |
| `n` | `int` | The number of completions to generate, by default 1. | *required* |
| `temperature` | `Optional[float]` | The temperature for text generation, by default None. | `None` |
| `stop` | `Optional[List[str]]` | The stop sequences for text generation, by default None. | `None` |
| `callbacks` | `Callbacks` | The callbacks to use during text generation, by default []. | `[]` |

Returns:

| Type | Description |
| --- | --- |
| `str` | The generated text. |

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 ``` | ``` async def generate(     self,     llm: BaseRagasLLM,     data: str,     temperature: t.Optional[float] = None,     stop: t.Optional[t.List[str]] = None,     callbacks: Callbacks = [], ) -> str:     """     Generate text based on the instruction and provided data.      Parameters     ----------     llm : BaseRagasLLM         The language model to use for text generation.     data : Optional[Dict[str, Any]], optional         The data to format the instruction with, by default None.     n : int, optional         The number of completions to generate, by default 1.     temperature : Optional[float], optional         The temperature for text generation, by default None.     stop : Optional[List[str]], optional         The stop sequences for text generation, by default None.     callbacks : Callbacks, optional         The callbacks to use during text generation, by default [].      Returns     -------     str         The generated text.     """     llm_result = await llm.agenerate_text(         StringPromptValue(text=data),         n=1,         temperature=temperature,         stop=stop,         callbacks=callbacks,     )     return llm_result.generations[0][0].text ``` |

### generate\_multiple `async`

```
generate_multiple(llm: BaseRagasLLM, data: str, n: int = 1, temperature: Optional[float] = None, stop: Optional[List[str]] = None, callbacks: Callbacks = []) -> List[str]
```

Generate multiple distinct text outputs based on the instruction and provided data.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `llm` | `BaseRagasLLM` | The language model to use for text generation. | *required* |
| `data` | `str` | The data to format the instruction with. | *required* |
| `n` | `int` | The number of completions to generate, by default 1. | `1` |
| `temperature` | `Optional[float]` | The temperature for text generation, by default None. | `None` |
| `stop` | `Optional[List[str]]` | Stop sequences for text generation, by default None. | `None` |
| `callbacks` | `Callbacks` | Callbacks to use during text generation, by default []. | `[]` |

Returns:

| Type | Description |
| --- | --- |
| `List[str]` | A list containing `n` generated outputs. |

Notes

* When caching is enabled, each output is uniquely cached to prevent duplicates.
* This ensures that multiple outputs for the same input are distinct.
* Previous issues where caching returned duplicate outputs have been fixed.

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 ``` | ``` async def generate_multiple(     self,     llm: BaseRagasLLM,     data: str,     n: int = 1,     temperature: t.Optional[float] = None,     stop: t.Optional[t.List[str]] = None,     callbacks: Callbacks = [], ) -> t.List[str]:     """     Generate multiple distinct text outputs based on the instruction and provided data.      Parameters     ----------     llm : BaseRagasLLM         The language model to use for text generation.     data : str         The data to format the instruction with.     n : int, optional         The number of completions to generate, by default 1.     temperature : Optional[float], optional         The temperature for text generation, by default None.     stop : Optional[List[str]], optional         Stop sequences for text generation, by default None.     callbacks : Callbacks, optional         Callbacks to use during text generation, by default [].      Returns     -------     List[str]         A list containing `n` generated outputs.      Notes     -----     - When caching is enabled, each output is uniquely cached to prevent duplicates.     - This ensures that multiple outputs for the same input are distinct.     - Previous issues where caching returned duplicate outputs have been fixed.     """     llm_result = await llm.agenerate_text(         StringPromptValue(text=data),         n=n,         temperature=temperature,         stop=stop,         callbacks=callbacks,     )      # flatten the generations     return [gen.text for gen in llm_result.generations[0]] ``` |

## PydanticPrompt

```
PydanticPrompt(name: Optional[str] = None, language: str = 'english', original_hash: Optional[str] = None)
```

Bases: `BasePrompt`, `Generic[InputModel, OutputModel]`

Source code in `src/ragas/prompt/base.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` def __init__(     self,     name: t.Optional[str] = None,     language: str = "english",     original_hash: t.Optional[str] = None, ):     if name is None:         self.name = camel_to_snake(self.__class__.__name__)      self.language = language     self.original_hash = original_hash ``` |

### generate `async`

```
generate(llm: Union[BaseRagasLLM, InstructorBaseRagasLLM, BaseLanguageModel], data: InputModel, temperature: Optional[float] = None, stop: Optional[List[str]] = None, callbacks: Optional[Callbacks] = None, retries_left: int = 3) -> OutputModel
```

Generate a single output using the provided language model and input data.

This method is a special case of `generate_multiple` where only one output is generated.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `llm` | `BaseRagasLLM` | The language model to use for generation. | *required* |
| `data` | `InputModel` | The input data for generation. | *required* |
| `temperature` | `float` | The temperature parameter for controlling randomness in generation. | `None` |
| `stop` | `List[str]` | A list of stop sequences to end generation. | `None` |
| `callbacks` | `Callbacks` | Callback functions to be called during the generation process. | `None` |
| `retries_left` | `int` | Number of retry attempts for an invalid LLM response | `3` |

Returns:

| Type | Description |
| --- | --- |
| `OutputModel` | The generated output. |

Notes

This method internally calls `generate_multiple` with `n=1` and returns the first (and only) result.


Source code in `src/ragas/prompt/pydantic_prompt.py`

|  |  |
| --- | --- |
| ``` 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 ``` | ``` async def generate(     self,     llm: t.Union[BaseRagasLLM, InstructorBaseRagasLLM, BaseLanguageModel],     data: InputModel,     temperature: t.Optional[float] = None,     stop: t.Optional[t.List[str]] = None,     callbacks: t.Optional[Callbacks] = None,     retries_left: int = 3, ) -> OutputModel:     """     Generate a single output using the provided language model and input data.      This method is a special case of `generate_multiple` where only one output is generated.      Parameters     ----------     llm : BaseRagasLLM         The language model to use for generation.     data : InputModel         The input data for generation.     temperature : float, optional         The temperature parameter for controlling randomness in generation.     stop : List[str], optional         A list of stop sequences to end generation.     callbacks : Callbacks, optional         Callback functions to be called during the generation process.     retries_left : int, optional         Number of retry attempts for an invalid LLM response      Returns     -------     OutputModel         The generated output.      Notes     -----     This method internally calls `generate_multiple` with `n=1` and returns the first (and only) result.     """     callbacks = callbacks or []      # this is just a special case of generate_multiple     output_single = await self.generate_multiple(         llm=llm,         data=data,         n=1,         temperature=temperature,         stop=stop,         callbacks=callbacks,         retries_left=retries_left,     )     return output_single[0] ``` |

### generate\_multiple `async`

```
generate_multiple(llm: Union[BaseRagasLLM, InstructorBaseRagasLLM, BaseLanguageModel], data: InputModel, n: int = 1, temperature: Optional[float] = None, stop: Optional[List[str]] = None, callbacks: Optional[Callbacks] = None, retries_left: int = 3) -> List[OutputModel]
```

Generate multiple outputs using the provided language model and input data.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `llm` | `BaseRagasLLM` | The language model to use for generation. | *required* |
| `data` | `InputModel` | The input data for generation. | *required* |
| `n` | `int` | The number of outputs to generate. Default is 1. | `1` |
| `temperature` | `float` | The temperature parameter for controlling randomness in generation. | `None` |
| `stop` | `List[str]` | A list of stop sequences to end generation. | `None` |
| `callbacks` | `Callbacks` | Callback functions to be called during the generation process. | `None` |
| `retries_left` | `int` | Number of retry attempts for an invalid LLM response | `3` |

Returns:

| Type | Description |
| --- | --- |
| `List[OutputModel]` | A list of generated outputs. |

Raises:

| Type | Description |
| --- | --- |
| `RagasOutputParserException` | If there's an error parsing the output. |

Source code in `src/ragas/prompt/pydantic_prompt.py`

|  |  |
| --- | --- |
| ``` 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 ``` | ``` async def generate_multiple(     self,     llm: t.Union[BaseRagasLLM, InstructorBaseRagasLLM, BaseLanguageModel],     data: InputModel,     n: int = 1,     temperature: t.Optional[float] = None,     stop: t.Optional[t.List[str]] = None,     callbacks: t.Optional[Callbacks] = None,     retries_left: int = 3, ) -> t.List[OutputModel]:     """     Generate multiple outputs using the provided language model and input data.      Parameters     ----------     llm : BaseRagasLLM         The language model to use for generation.     data : InputModel         The input data for generation.     n : int, optional         The number of outputs to generate. Default is 1.     temperature : float, optional         The temperature parameter for controlling randomness in generation.     stop : List[str], optional         A list of stop sequences to end generation.     callbacks : Callbacks, optional         Callback functions to be called during the generation process.     retries_left : int, optional         Number of retry attempts for an invalid LLM response      Returns     -------     List[OutputModel]         A list of generated outputs.      Raises     ------     RagasOutputParserException         If there's an error parsing the output.     """     callbacks = callbacks or []      processed_data = self.process_input(data)     prompt_rm, prompt_cb = new_group(         name=self.name,         inputs={"data": processed_data},         callbacks=callbacks,         metadata={"type": ChainType.RAGAS_PROMPT},     )     prompt_value = PromptValue(text=self.to_string(processed_data))      # Handle different LLM types with different interfaces     # 1. LangChain LLMs have agenerate_prompt() for async with specific signature     # 2. BaseRagasLLM have generate() with n, temperature, stop, callbacks     # 3. InstructorLLM has generate()/agenerate() with only prompt and response_model     if is_langchain_llm(llm):         # This is a LangChain LLM - use agenerate_prompt() with batch for multiple generations         langchain_llm = t.cast(BaseLanguageModel, llm)         # LangChain doesn't support n parameter directly, so we batch multiple prompts         prompts = t.cast(t.List[t.Any], [prompt_value for _ in range(n)])         resp = await langchain_llm.agenerate_prompt(             prompts,             stop=stop,             callbacks=prompt_cb,         )     elif isinstance(llm, InstructorBaseRagasLLM):         # This is an InstructorLLM - use its generate()/agenerate() method         # InstructorLLM.generate()/agenerate() only takes prompt and response_model parameters         from ragas.llms.base import InstructorLLM          instructor_llm = t.cast(InstructorLLM, llm)         if instructor_llm.is_async:             result = await llm.agenerate(                 prompt=prompt_value.text,                 response_model=self.output_model,             )         else:             result = llm.generate(                 prompt=prompt_value.text,                 response_model=self.output_model,             )         # Wrap the single response in an LLMResult-like structure for consistency         from langchain_core.outputs import Generation, LLMResult          generation = Generation(text=result.model_dump_json())         resp = LLMResult(generations=[[generation]])     else:         # This is a standard BaseRagasLLM - use generate()         ragas_llm = t.cast(BaseRagasLLM, llm)         resp = await ragas_llm.generate(             prompt_value,             n=n,             temperature=temperature,             stop=stop,             callbacks=prompt_cb,         )      output_models = []     parser = RagasOutputParser(pydantic_object=self.output_model)      # Handle cases where LLM returns fewer generations than requested     if is_langchain_llm(llm) or isinstance(llm, InstructorBaseRagasLLM):         available_generations = len(resp.generations)     else:         available_generations = len(resp.generations[0]) if resp.generations else 0      actual_n = min(n, available_generations)      if actual_n == 0:         logger.error(             f"LLM returned no generations when {n} were requested. Cannot proceed."         )         raise ValueError(f"LLM returned no generations when {n} were requested")      if actual_n < n:         logger.warning(             f"LLM returned {actual_n} generations instead of requested {n}. "             f"Proceeding with {actual_n} generations."         )      for i in range(actual_n):         if is_langchain_llm(llm) or isinstance(llm, InstructorBaseRagasLLM):             # For LangChain LLMs and InstructorLLM, each generation is in a separate batch result             output_string = resp.generations[i][0].text         else:             # For Ragas LLMs, all generations are in the first batch             output_string = resp.generations[0][i].text         try:             # For the parser, we need a BaseRagasLLM, so if it's a LangChain LLM, we need to handle this             if is_langchain_llm(llm) or isinstance(llm, InstructorBaseRagasLLM):                 # Skip parsing retry for LangChain LLMs since parser expects BaseRagasLLM                 answer = self.output_model.model_validate_json(output_string)             else:                 ragas_llm = t.cast(BaseRagasLLM, llm)                 answer = await parser.parse_output_string(                     output_string=output_string,                     prompt_value=prompt_value,                     llm=ragas_llm,                     callbacks=prompt_cb,                     retries_left=retries_left,                 )             processed_output = self.process_output(answer, data)  # type: ignore             output_models.append(processed_output)         except RagasOutputParserException as e:             prompt_rm.on_chain_error(error=e)             logger.error("Prompt %s failed to parse output: %s", self.name, e)             raise e      prompt_rm.on_chain_end({"output": output_models})      # Track prompt usage     track(         PromptUsageEvent(             prompt_type="pydantic",             has_examples=len(self.examples) > 0,             num_examples=len(self.examples),             has_response_model=True,  # PydanticPrompt always has response model             language=self.language,         )     )      return output_models ``` |

### adapt `async`

```
adapt(target_language: str, llm: Union[BaseRagasLLM, InstructorBaseRagasLLM], adapt_instruction: bool = False) -> 'PydanticPrompt[InputModel, OutputModel]'
```

Adapt the prompt to a new language.

Source code in `src/ragas/prompt/pydantic_prompt.py`

|  |  |
| --- | --- |
| ``` 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 ``` | ``` async def adapt(     self,     target_language: str,     llm: t.Union[BaseRagasLLM, InstructorBaseRagasLLM],     adapt_instruction: bool = False, ) -> "PydanticPrompt[InputModel, OutputModel]":     """     Adapt the prompt to a new language.     """      strings = get_all_strings(self.examples)     translated_strings = await translate_statements_prompt.generate(         llm=llm,         data=ToTranslate(target_language=target_language, statements=strings),     )      translated_examples = update_strings(         obj=self.examples,         old_strings=strings,         new_strings=translated_strings.statements,     )      new_prompt = copy.deepcopy(self)     new_prompt.examples = translated_examples     new_prompt.language = target_language      if adapt_instruction:         translated_instruction = await translate_statements_prompt.generate(             llm=llm,             data=ToTranslate(                 target_language=target_language, statements=[self.instruction]             ),         )         new_prompt.instruction = translated_instruction.statements[0]      new_prompt.original_hash = hash(new_prompt)      return new_prompt ``` |

### save

```
save(file_path: str)
```

Save the prompt to a file.

Source code in `src/ragas/prompt/pydantic_prompt.py`

|  |  |
| --- | --- |
| ``` 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 ``` | ``` def save(self, file_path: str):     """     Save the prompt to a file.     """     data = {         "ragas_version": __version__,         "original_hash": (             hash(self) if self.original_hash is None else self.original_hash         ),         "language": self.language,         "instruction": self.instruction,         "examples": [             {"input": example[0].model_dump(), "output": example[1].model_dump()}             for example in self.examples         ],     }     if os.path.exists(file_path):         raise FileExistsError(f"The file '{file_path}' already exists.")     with open(file_path, "w", encoding="utf-8") as f:         json.dump(data, f, indent=2, ensure_ascii=False)         print(f"Prompt saved to {file_path}") ``` |

## BoolIO

Bases: `BaseModel`

## StringIO

Bases: `BaseModel`

## PromptMixin

Mixin class for classes that have prompts.
eg: [BaseSynthesizer](../synthesizers/#ragas.testset.synthesizers.BaseSynthesizer), [MetricWithLLM](../metrics/#ragas.metrics.base.MetricWithLLM)

### get\_prompts

```
get_prompts() -> Dict[str, PydanticPrompt]
```

Returns a dictionary of prompts for the class.

Source code in `src/ragas/prompt/mixin.py`

|  |  |
| --- | --- |
| ``` 32 33 34 35 36 37 38 39 ``` | ``` def get_prompts(self) -> t.Dict[str, PydanticPrompt]:     """     Returns a dictionary of prompts for the class.     """     prompts = {}     for _, value in self._get_prompts().items():         prompts.update({value.name: value})     return prompts ``` |

### set\_prompts

```
set_prompts(**prompts)
```

Sets the prompts for the class.

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the prompt is not an instance of `PydanticPrompt`. |

Source code in `src/ragas/prompt/mixin.py`

|  |  |
| --- | --- |
| ``` 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 ``` | ``` def set_prompts(self, **prompts):     """     Sets the prompts for the class.      Raises     ------     ValueError         If the prompt is not an instance of `PydanticPrompt`.     """     available_prompts = self.get_prompts()     name_to_var = {v.name: k for k, v in self._get_prompts().items()}     for key, value in prompts.items():         if key not in available_prompts:             raise ValueError(                 f"Prompt with name '{key}' does not exist. Use get_prompts() to see available prompts."             )         if not isinstance(value, PydanticPrompt):             raise ValueError(                 f"Prompt with name '{key}' must be an instance of 'ragas.prompt.PydanticPrompt'"             )         setattr(self, name_to_var[key], value) ``` |

### adapt\_prompts `async`

```
adapt_prompts(language: str, llm: Union[BaseRagasLLM, InstructorBaseRagasLLM], adapt_instruction: bool = False) -> Dict[str, PydanticPrompt]
```

Adapts the prompts in the class to the given language and using the given LLM.

Notes

Make sure you use the best available LLM for adapting the prompts and then save and load the prompts using
[save\_prompts](#ragas.prompt.PromptMixin.save_prompts) and [load\_prompts](#ragas.prompt.PromptMixin.load_prompts)
methods.


Source code in `src/ragas/prompt/mixin.py`

|  |  |
| --- | --- |
| ``` 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 ``` | ``` async def adapt_prompts(     self,     language: str,     llm: t.Union[BaseRagasLLM, InstructorBaseRagasLLM],     adapt_instruction: bool = False, ) -> t.Dict[str, PydanticPrompt]:     """     Adapts the prompts in the class to the given language and using the given LLM.      Notes     -----     Make sure you use the best available LLM for adapting the prompts and then save and load the prompts using     [save_prompts][ragas.prompt.mixin.PromptMixin.save_prompts] and [load_prompts][ragas.prompt.mixin.PromptMixin.load_prompts]     methods.     """     prompts = self.get_prompts()     adapted_prompts = {}     for name, prompt in prompts.items():         adapted_prompt = await prompt.adapt(language, llm, adapt_instruction)         adapted_prompts[name] = adapted_prompt      return adapted_prompts ``` |

### save\_prompts

```
save_prompts(path: str)
```

Saves the prompts to a directory in the format of {name}\_{language}.json

Source code in `src/ragas/prompt/mixin.py`

|  |  |
| --- | --- |
| ```  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 ``` | ``` def save_prompts(self, path: str):     """     Saves the prompts to a directory in the format of {name}_{language}.json     """     # check if path is valid     if not os.path.exists(path):         raise ValueError(f"Path {path} does not exist")      prompts = self.get_prompts()     for prompt_name, prompt in prompts.items():         # hash_hex = f"0x{hash(prompt) & 0xFFFFFFFFFFFFFFFF:016x}"         if self.name == "":             file_name = os.path.join(path, f"{prompt_name}_{prompt.language}.json")         else:             file_name = os.path.join(                 path, f"{self.name}_{prompt_name}_{prompt.language}.json"             )         prompt.save(file_name) ``` |

### load\_prompts

```
load_prompts(path: str, language: Optional[str] = None)
```

Loads the prompts from a path. File should be in the format of {name}\_{language}.json

Source code in `src/ragas/prompt/mixin.py`

|  |  |
| --- | --- |
| ``` 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 ``` | ``` def load_prompts(self, path: str, language: t.Optional[str] = None):     """     Loads the prompts from a path. File should be in the format of {name}_{language}.json     """     # check if path is valid     if not os.path.exists(path):         raise ValueError(f"Path {path} does not exist")      # check if language is supported, defaults to english     if language is None:         language = "english"         logger.info(             "Language not specified, loading prompts for default language: %s",             language,         )      loaded_prompts = {}     for prompt_name, prompt in self.get_prompts().items():         if self.name == "":             file_name = os.path.join(path, f"{prompt_name}_{language}.json")         else:             file_name = os.path.join(                 path, f"{self.name}_{prompt_name}_{language}.json"             )         loaded_prompt = prompt.__class__.load(file_name)         loaded_prompts[prompt_name] = loaded_prompt     return loaded_prompts ``` |

## Metrics Collections Prompts

Modern metrics in Ragas use specialized prompt classes. Each metric module contains:

* **Input Model**: Defines what data the prompt needs (e.g., `FaithfulnessInput`)
* **Output Model**: Defines the expected LLM response structure (e.g., `FaithfulnessOutput`)
* **Prompt Class**: Inherits from `BasePrompt` to generate the prompt string with examples and instructions

### Example: Faithfulness Metric Prompts

```
from ragas.metrics.collections.faithfulness.util import (
    FaithfulnessPrompt,
    FaithfulnessInput,
    FaithfulnessOutput,
)

# The prompt class combines input/output models with instructions and examples
prompt = FaithfulnessPrompt()

# Create input data
input_data = FaithfulnessInput(
    response="The capital of France is Paris.",
    context="Paris is the capital and most populous city of France."
)

# Generate the prompt string for the LLM
prompt_string = prompt.to_string(input_data)

# The output will be structured according to FaithfulnessOutput model
```

### Available Metric Prompts

See the individual metric documentation for details on their prompts:

* [Faithfulness](../../concepts/metrics/available_metrics/faithfulness/)
* [Context Recall](../../concepts/metrics/available_metrics/context_recall/)
* [Context Precision](../../concepts/metrics/available_metrics/context_precision/)
* [Answer Correctness](../../concepts/metrics/available_metrics/answer_correctness/)
* [Factual Correctness](../../concepts/metrics/available_metrics/factual_correctness/)
* [Noise Sensitivity](../../concepts/metrics/available_metrics/noise_sensitivity/)

## Customization

For detailed guidance on customizing prompts for metrics, see [Modifying prompts in metrics](../../howtos/customizations/metrics/modifying-prompts-metrics/).

December 14, 2025




November 28, 2025

Back to top