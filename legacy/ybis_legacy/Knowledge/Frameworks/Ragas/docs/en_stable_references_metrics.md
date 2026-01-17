Metrics - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.metrics.base)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Metrics

## MetricType

Bases: `Enum`

Enumeration of metric types in Ragas.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `SINGLE_TURN` | `str` | Represents a single-turn metric type. |
| `MULTI_TURN` | `str` | Represents a multi-turn metric type. |

## Metric `dataclass`

```
Metric(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '')
```

Bases: `ABC`

Abstract base class for metrics in Ragas.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | The name of the metric. |
| `required_columns` | `Dict[str, Set[str]]` | A dictionary mapping metric type names to sets of required column names. This is a property and raises `ValueError` if columns are not in `VALID_COLUMNS`. |

### init `abstractmethod`

```
init(run_config: RunConfig) -> None
```

Initialize the metric with the given run configuration.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `run_config` | `RunConfig` | Configuration for the metric run including timeouts and other settings. | *required* |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 141 142 143 144 145 146 147 148 149 150 151 ``` | ``` @abstractmethod def init(self, run_config: RunConfig) -> None:     """     Initialize the metric with the given run configuration.      Parameters     ----------     run_config : RunConfig         Configuration for the metric run including timeouts and other settings.     """     ... ``` |

## MetricWithLLM `dataclass`

```
MetricWithLLM(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '', llm: Optional[BaseRagasLLM] = None, output_type: Optional[MetricOutputType] = None)
```

Bases: `Metric`, `PromptMixin`

A metric class that uses a language model for evaluation.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `llm` | `Optional[BaseRagasLLM]` | The language model used for the metric. Both BaseRagasLLM and InstructorBaseRagasLLM are accepted at runtime via duck typing (both have compatible methods). |

### init

```
init(run_config: RunConfig) -> None
```

Initialize the metric with run configuration and validate LLM is present.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `run_config` | `RunConfig` | Configuration for the metric run. | *required* |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If no LLM is provided to the metric. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 ``` | ``` def init(self, run_config: RunConfig) -> None:     """     Initialize the metric with run configuration and validate LLM is present.      Parameters     ----------     run_config : RunConfig         Configuration for the metric run.      Raises     ------     ValueError         If no LLM is provided to the metric.     """     if self.llm is None:         raise ValueError(             f"Metric '{self.name}' has no valid LLM provided (self.llm is None). Please instantiate the metric with an LLM to run."         )     # Only BaseRagasLLM has set_run_config method, not InstructorBaseRagasLLM     if isinstance(self.llm, BaseRagasLLM):         self.llm.set_run_config(run_config) ``` |

### train

```
train(path: str, demonstration_config: Optional[DemonstrationConfig] = None, instruction_config: Optional[InstructionConfig] = None, callbacks: Optional[Callbacks] = None, run_config: Optional[RunConfig] = None, batch_size: Optional[int] = None, with_debugging_logs=False, raise_exceptions: bool = True) -> None
```

Train the metric using local JSON data

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `path` | `str` | Path to local JSON training data file | *required* |
| `demonstration_config` | `DemonstrationConfig` | Configuration for demonstration optimization | `None` |
| `instruction_config` | `InstructionConfig` | Configuration for instruction optimization | `None` |
| `callbacks` | `Callbacks` | List of callback functions | `None` |
| `run_config` | `RunConfig` | Run configuration | `None` |
| `batch_size` | `int` | Batch size for training | `None` |
| `with_debugging_logs` | `bool` | Enable debugging logs | `False` |
| `raise_exceptions` | `bool` | Whether to raise exceptions during training | `True` |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If path is not provided or not a JSON file |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 ``` | ``` def train(     self,     path: str,     demonstration_config: t.Optional[DemonstrationConfig] = None,     instruction_config: t.Optional[InstructionConfig] = None,     callbacks: t.Optional[Callbacks] = None,     run_config: t.Optional[RunConfig] = None,     batch_size: t.Optional[int] = None,     with_debugging_logs=False,     raise_exceptions: bool = True, ) -> None:     """     Train the metric using local JSON data      Parameters     ----------     path : str         Path to local JSON training data file     demonstration_config : DemonstrationConfig, optional         Configuration for demonstration optimization     instruction_config : InstructionConfig, optional         Configuration for instruction optimization     callbacks : Callbacks, optional         List of callback functions     run_config : RunConfig, optional         Run configuration     batch_size : int, optional         Batch size for training     with_debugging_logs : bool, default=False         Enable debugging logs     raise_exceptions : bool, default=True         Whether to raise exceptions during training      Raises     ------     ValueError         If path is not provided or not a JSON file     """     # Validate input parameters     if not path:         raise ValueError("Path to training data file must be provided")      if not path.endswith(".json"):         raise ValueError("Train data must be in json format")      run_config = run_config or RunConfig()     callbacks = callbacks or []      # Load the dataset from JSON file     dataset = MetricAnnotation.from_json(path, metric_name=self.name)      # only optimize the instruction if instruction_config is provided     if instruction_config is not None:         self._optimize_instruction(             instruction_config=instruction_config,             dataset=dataset,             callbacks=callbacks,             run_config=run_config,             batch_size=batch_size,             with_debugging_logs=with_debugging_logs,             raise_exceptions=raise_exceptions,         )      # if demonstration_config is provided, optimize the demonstrations     if demonstration_config is not None:         self._optimize_demonstration(             demonstration_config=demonstration_config,             dataset=dataset,         ) ``` |

## SingleTurnMetric `dataclass`

```
SingleTurnMetric(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '')
```

Bases: `Metric`

A metric class for evaluating single-turn interactions.

This class provides methods to score single-turn samples, both synchronously and asynchronously.

### single\_turn\_score

```
single_turn_score(sample: SingleTurnSample, callbacks: Callbacks = None) -> float
```

Synchronously score a single-turn sample.

May raise ImportError if nest\_asyncio is not installed in a Jupyter-like environment.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 ``` | ``` def single_turn_score(     self,     sample: SingleTurnSample,     callbacks: Callbacks = None, ) -> float:     """     Synchronously score a single-turn sample.      May raise ImportError if nest_asyncio is not installed in a Jupyter-like environment.     """     callbacks = callbacks or []     # only get the required columns     sample = self._only_required_columns_single_turn(sample)     rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )      async def _async_wrapper():         try:             result = await self._single_turn_ascore(                 sample=sample, callbacks=group_cm             )         except Exception as e:             if not group_cm.ended:                 rm.on_chain_error(e)             raise e         else:             if not group_cm.ended:                 rm.on_chain_end({"output": result})             return result      apply_nest_asyncio()     score = run(_async_wrapper)      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )     return score ``` |

### single\_turn\_ascore `async`

```
single_turn_ascore(sample: SingleTurnSample, callbacks: Callbacks = None, timeout: Optional[float] = None) -> float
```

Asynchronously score a single-turn sample with an optional timeout.

May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 ``` | ``` async def single_turn_ascore(     self,     sample: SingleTurnSample,     callbacks: Callbacks = None,     timeout: t.Optional[float] = None, ) -> float:     """     Asynchronously score a single-turn sample with an optional timeout.      May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.     """     callbacks = callbacks or []     # only get the required columns     sample = self._only_required_columns_single_turn(sample)     rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )     try:         score = await asyncio.wait_for(             self._single_turn_ascore(sample=sample, callbacks=group_cm),             timeout=timeout,         )     except Exception as e:         if not group_cm.ended:             rm.on_chain_error(e)         raise e     else:         if not group_cm.ended:             rm.on_chain_end({"output": score})      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )     return score ``` |

## MultiTurnMetric `dataclass`

```
MultiTurnMetric(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '')
```

Bases: `Metric`

A metric class for evaluating multi-turn conversations.

This class extends the base Metric class to provide functionality
for scoring multi-turn conversation samples.

### multi\_turn\_score

```
multi_turn_score(sample: MultiTurnSample, callbacks: Callbacks = None) -> float
```

Score a multi-turn conversation sample synchronously.

May raise ImportError if nest\_asyncio is not installed in Jupyter-like environments.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 ``` | ``` def multi_turn_score(     self,     sample: MultiTurnSample,     callbacks: Callbacks = None, ) -> float:     """     Score a multi-turn conversation sample synchronously.      May raise ImportError if nest_asyncio is not installed in Jupyter-like environments.     """     callbacks = callbacks or []     sample = self._only_required_columns_multi_turn(sample)     rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )      async def _async_wrapper():         try:             result = await self._multi_turn_ascore(                 sample=sample, callbacks=group_cm             )         except Exception as e:             if not group_cm.ended:                 rm.on_chain_error(e)             raise e         else:             if not group_cm.ended:                 rm.on_chain_end({"output": result})             return result      apply_nest_asyncio()     score = run(_async_wrapper)      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )     return score ``` |

### multi\_turn\_ascore `async`

```
multi_turn_ascore(sample: MultiTurnSample, callbacks: Callbacks = None, timeout: Optional[float] = None) -> float
```

Score a multi-turn conversation sample asynchronously.

May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 ``` | ``` async def multi_turn_ascore(     self,     sample: MultiTurnSample,     callbacks: Callbacks = None,     timeout: t.Optional[float] = None, ) -> float:     """     Score a multi-turn conversation sample asynchronously.      May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.     """     callbacks = callbacks or []     sample = self._only_required_columns_multi_turn(sample)      rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )     try:         score = await asyncio.wait_for(             self._multi_turn_ascore(sample=sample, callbacks=group_cm),             timeout=timeout,         )     except Exception as e:         if not group_cm.ended:             rm.on_chain_error(e)         raise e     else:         if not group_cm.ended:             rm.on_chain_end({"output": score})      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )      return score ``` |

## Ensember

Combine multiple llm outputs for same input (n>1) to a single output

### from\_discrete

```
from_discrete(inputs: list[list[Dict]], attribute: str) -> List[Dict]
```

Simple majority voting for binary values, ie [0,0,1] -> 0
inputs: list of list of dicts each containing verdict for a single input

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 ``` | ``` def from_discrete(     self, inputs: list[list[t.Dict]], attribute: str ) -> t.List[t.Dict]:     """     Simple majority voting for binary values, ie [0,0,1] -> 0     inputs: list of list of dicts each containing verdict for a single input     """      if not isinstance(inputs, list):         inputs = [inputs]      if not all(len(item) == len(inputs[0]) for item in inputs):         logger.warning("All inputs must have the same length")         return inputs[0]      if not all(attribute in item for input in inputs for item in input):         logger.warning(f"All inputs must have {attribute} attribute")         return inputs[0]      if len(inputs) == 1:         return inputs[0]      verdict_agg = []     for i in range(len(inputs[0])):         item = inputs[0][i]         verdicts = [inputs[k][i][attribute] for k in range(len(inputs))]         verdict_counts = dict(Counter(verdicts).most_common())         item[attribute] = list(verdict_counts.keys())[0]         verdict_agg.append(item)      return verdict_agg ``` |

## SimpleBaseMetric `dataclass`

```
SimpleBaseMetric(name: str, allowed_values: AllowedValuesType = (lambda: ['pass', 'fail'])())
```

Bases: `ABC`

Base class for simple metrics that return MetricResult objects.

This class provides the foundation for metrics that evaluate inputs
and return structured MetricResult objects containing scores and reasoning.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | The name of the metric. |
| `allowed_values` | `AllowedValuesType` | Allowed values for the metric output. Can be a list of strings for discrete metrics, a tuple of floats for numeric metrics, or an integer for ranking metrics. |

Examples:

```
>>> from ragas.metrics import discrete_metric
>>>
>>> @discrete_metric(name="sentiment", allowed_values=["positive", "negative"])
>>> def sentiment_metric(user_input: str, response: str) -> str:
...     return "positive" if "good" in response else "negative"
>>>
>>> result = sentiment_metric(user_input="How are you?", response="I'm good!")
>>> print(result.value)  # "positive"
```

### score `abstractmethod`

```
score(**kwargs) -> 'MetricResult'
```

Synchronously calculate the metric score.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `**kwargs` | `dict` | Input parameters required by the specific metric implementation. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `MetricResult` | The evaluation result containing the score and reasoning. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 ``` | ``` @abstractmethod def score(self, **kwargs) -> "MetricResult":     """     Synchronously calculate the metric score.      Parameters     ----------     **kwargs : dict         Input parameters required by the specific metric implementation.      Returns     -------     MetricResult         The evaluation result containing the score and reasoning.     """     pass ``` |

### ascore `abstractmethod` `async`

```
ascore(**kwargs) -> 'MetricResult'
```

Asynchronously calculate the metric score.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `**kwargs` | `dict` | Input parameters required by the specific metric implementation. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `MetricResult` | The evaluation result containing the score and reasoning. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 ``` | ``` @abstractmethod async def ascore(self, **kwargs) -> "MetricResult":     """     Asynchronously calculate the metric score.      Parameters     ----------     **kwargs : dict         Input parameters required by the specific metric implementation.      Returns     -------     MetricResult         The evaluation result containing the score and reasoning.     """     pass ``` |

### batch\_score

```
batch_score(inputs: List[Dict[str, Any]]) -> List['MetricResult']
```

Synchronously calculate scores for a batch of inputs.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `inputs` | `List[Dict[str, Any]]` | List of input dictionaries, each containing parameters for the metric. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `List[MetricResult]` | List of evaluation results, one for each input. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 ``` | ``` def batch_score(     self,     inputs: t.List[t.Dict[str, t.Any]], ) -> t.List["MetricResult"]:     """     Synchronously calculate scores for a batch of inputs.      Parameters     ----------     inputs : List[Dict[str, Any]]         List of input dictionaries, each containing parameters for the metric.      Returns     -------     List[MetricResult]         List of evaluation results, one for each input.     """     return [self.score(**input_dict) for input_dict in inputs] ``` |

### abatch\_score `async`

```
abatch_score(inputs: List[Dict[str, Any]]) -> List['MetricResult']
```

Asynchronously calculate scores for a batch of inputs in parallel.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `inputs` | `List[Dict[str, Any]]` | List of input dictionaries, each containing parameters for the metric. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `List[MetricResult]` | List of evaluation results, one for each input. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 ``` | ``` async def abatch_score(     self,     inputs: t.List[t.Dict[str, t.Any]], ) -> t.List["MetricResult"]:     """     Asynchronously calculate scores for a batch of inputs in parallel.      Parameters     ----------     inputs : List[Dict[str, Any]]         List of input dictionaries, each containing parameters for the metric.      Returns     -------     List[MetricResult]         List of evaluation results, one for each input.     """     async_tasks = []     for input_dict in inputs:         # Process input asynchronously         async_tasks.append(self.ascore(**input_dict))      # Run all tasks concurrently and return results     return await asyncio.gather(*async_tasks) ``` |

## SimpleLLMMetric `dataclass`

```
SimpleLLMMetric(name: str, allowed_values: AllowedValuesType = (lambda: ['pass', 'fail'])(), prompt: Optional[Union[str, 'Prompt']] = None)
```

Bases: `SimpleBaseMetric`

LLM-based metric that uses prompts to generate structured responses.

### save

```
save(path: Optional[str] = None) -> None
```

Save the metric configuration to a JSON file.

Parameters:

path : str, optional
File path to save to. If not provided, saves to "./{metric.name}.json"
Use .gz extension for compression.


Note:

If the metric has a response\_model, its schema will be saved for reference
but the model itself cannot be serialized. You'll need to provide it when loading.


Examples:

All these work:

> > > metric.save() # → ./response\_quality.json
> > > metric.save("custom.json") # → ./custom.json
> > > metric.save("/path/to/metrics/") # → /path/to/metrics/response\_quality.json
> > > metric.save("no\_extension") # → ./no\_extension.json
> > > metric.save("compressed.json.gz") # → ./compressed.json.gz (compressed)


Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ```  935  936  937  938  939  940  941  942  943  944  945  946  947  948  949  950  951  952  953  954  955  956  957  958  959  960  961  962  963  964  965  966  967  968  969  970  971  972  973  974  975  976  977  978  979  980  981  982  983  984  985  986  987  988  989  990  991  992  993  994  995  996  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 ``` | ``` def save(self, path: t.Optional[str] = None) -> None:     """     Save the metric configuration to a JSON file.      Parameters:     -----------     path : str, optional         File path to save to. If not provided, saves to "./{metric.name}.json"         Use .gz extension for compression.      Note:     -----     If the metric has a response_model, its schema will be saved for reference     but the model itself cannot be serialized. You'll need to provide it when loading.      Examples:     ---------     All these work:     >>> metric.save()                      # → ./response_quality.json     >>> metric.save("custom.json")         # → ./custom.json     >>> metric.save("/path/to/metrics/")   # → /path/to/metrics/response_quality.json     >>> metric.save("no_extension")        # → ./no_extension.json     >>> metric.save("compressed.json.gz")  # → ./compressed.json.gz (compressed)     """     import gzip     import json     import warnings     from pathlib import Path      # Handle default path     if path is None:         # Default to current directory with metric name as filename         file_path = Path(f"./{self.name}.json")     else:         file_path = Path(path)          # If path is a directory, append the metric name as filename         if file_path.is_dir():             file_path = file_path / f"{self.name}.json"         # If path has no extension, add .json         elif not file_path.suffix:             file_path = file_path.with_suffix(".json")      # Collect warning messages for data loss     warning_messages = []      if hasattr(self, "_response_model") and self._response_model:         # Only warn for custom response models, not auto-generated ones         if not getattr(self._response_model, "__ragas_auto_generated__", False):             warning_messages.append(                 "- Custom response_model will be lost (set it manually after loading)"             )      # Serialize the prompt (may add embedding_model warning)     prompt_data = self._serialize_prompt(warning_messages)      # Determine the metric type     metric_type = self.__class__.__name__      # Get metric-specific config     config = self._get_metric_config()      # Emit consolidated warning if there's data loss     if warning_messages:         warnings.warn(             "Some metric components cannot be saved and will be lost:\n"             + "\n".join(warning_messages)             + "\n\nYou'll need to provide these when loading the metric."         )      data = {         "format_version": "1.0",         "metric_type": metric_type,         "name": self.name,         "prompt": prompt_data,         "config": config,         "response_model_info": self._serialize_response_model_info(),     }     try:         if file_path.suffix == ".gz":             with gzip.open(file_path, "wt", encoding="utf-8") as f:                 json.dump(data, f, indent=2)         else:             with open(file_path, "w", encoding="utf-8") as f:                 json.dump(data, f, indent=2)     except (OSError, IOError) as e:         raise ValueError(f"Cannot save metric to {file_path}: {e}") ``` |

### load `classmethod`

```
load(path: str, response_model: Optional[Type['BaseModel']] = None, embedding_model: Optional['EmbeddingModelType'] = None) -> 'SimpleLLMMetric'
```

Load a metric from a JSON file.

Parameters:

path : str
File path to load from. Supports .gz compressed files.
response\_model : Optional[Type[BaseModel]]
Pydantic model to use for response validation. Required for custom SimpleLLMMetrics.
embedding\_model : Optional[Any]
Embedding model for DynamicFewShotPrompt. Required if the original used one.


Returns:

SimpleLLMMetric
Loaded metric instance


Raises:

ValueError
If file cannot be loaded, is invalid, or missing required models


Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 1194 1195 1196 1197 1198 1199 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 ``` | ``` @classmethod def load(     cls,     path: str,     response_model: t.Optional[t.Type["BaseModel"]] = None,     embedding_model: t.Optional["EmbeddingModelType"] = None, ) -> "SimpleLLMMetric":     """     Load a metric from a JSON file.      Parameters:     -----------     path : str         File path to load from. Supports .gz compressed files.     response_model : Optional[Type[BaseModel]]         Pydantic model to use for response validation. Required for custom SimpleLLMMetrics.     embedding_model : Optional[Any]         Embedding model for DynamicFewShotPrompt. Required if the original used one.      Returns:     --------     SimpleLLMMetric         Loaded metric instance      Raises:     -------     ValueError         If file cannot be loaded, is invalid, or missing required models     """     import gzip     import json     from pathlib import Path      file_path = Path(path)      # Load JSON data     try:         if file_path.suffix == ".gz":             with gzip.open(file_path, "rt", encoding="utf-8") as f:                 data = json.load(f)         else:             with open(file_path, "r", encoding="utf-8") as f:                 data = json.load(f)     except (FileNotFoundError, json.JSONDecodeError, OSError) as e:         raise ValueError(f"Cannot load metric from {path}: {e}")      # Validate format     if data.get("format_version") != "1.0":         import warnings          warnings.warn(             f"Loading metric with format version {data.get('format_version')}, expected 1.0"         )      # Reconstruct the prompt     prompt = cls._deserialize_prompt(data["prompt"], embedding_model)      # Get config     config = data.get("config", {})      # Create the metric instance     metric = cls(name=data["name"], prompt=prompt, **config)      # Set response model if provided     if response_model:         metric._response_model = response_model      return metric ``` |

### get\_correlation `abstractmethod`

```
get_correlation(gold_labels: List[str], predictions: List[str]) -> float
```

Calculate the correlation between gold scores and predicted scores.
This is a placeholder method and should be implemented based on the specific metric.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1275 1276 1277 1278 1279 1280 1281 1282 1283 ``` | ``` @abstractmethod def get_correlation(     self, gold_labels: t.List[str], predictions: t.List[str] ) -> float:     """     Calculate the correlation between gold scores and predicted scores.     This is a placeholder method and should be implemented based on the specific metric.     """     pass ``` |

### align\_and\_validate

```
align_and_validate(dataset: 'Dataset', embedding_model: 'EmbeddingModelType', llm: 'BaseRagasLLM', test_size: float = 0.2, random_state: int = 42, **kwargs: Dict[str, Any])
```

Args:
dataset: experiment to align the metric with.
embedding\_model: The embedding model used for dynamic few-shot prompting.
llm: The LLM instance to use for scoring.

Align the metric with the specified experiments and validate it against a gold standard experiment.
This method combines alignment and validation into a single step.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 ``` | ``` def align_and_validate(     self,     dataset: "Dataset",     embedding_model: "EmbeddingModelType",     llm: "BaseRagasLLM",     test_size: float = 0.2,     random_state: int = 42,     **kwargs: t.Dict[str, t.Any], ):     """     Args:         dataset: experiment to align the metric with.         embedding_model: The embedding model used for dynamic few-shot prompting.         llm: The LLM instance to use for scoring.      Align the metric with the specified experiments and validate it against a gold standard experiment.     This method combines alignment and validation into a single step.     """     train_dataset, test_dataset = dataset.train_test_split(         test_size=test_size, random_state=random_state     )      self.align(train_dataset, embedding_model, **kwargs)  # type: ignore     return self.validate_alignment(llm, test_dataset)  # type: ignore ``` |

### align

```
align(train_dataset: 'Dataset', embedding_model: 'EmbeddingModelType', **kwargs: Dict[str, Any])
```

Args:
train\_dataset: train\_dataset to align the metric with.
embedding\_model: The embedding model used for dynamic few-shot prompting.

Align the metric with the specified experiments by different optimization methods.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1310 1311 1312 1313 1314 1315 1316 1317 1318 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 1331 1332 1333 1334 1335 1336 1337 1338 1339 1340 1341 1342 1343 1344 1345 1346 1347 1348 1349 1350 1351 1352 1353 1354 1355 1356 1357 1358 1359 1360 1361 1362 1363 1364 1365 1366 1367 1368 1369 1370 1371 1372 1373 1374 1375 1376 1377 1378 1379 1380 1381 1382 1383 1384 1385 1386 1387 1388 1389 1390 1391 1392 1393 ``` | ``` def align(     self,     train_dataset: "Dataset",     embedding_model: "EmbeddingModelType",     **kwargs: t.Dict[str, t.Any], ):     """     Args:         train_dataset: train_dataset to align the metric with.         embedding_model: The embedding model used for dynamic few-shot prompting.      Align the metric with the specified experiments by different optimization methods.     """      # get prompt     if not self.prompt:         raise Exception("prompt not passed")     from ragas.prompt.simple_prompt import Prompt      self.prompt = (         self.prompt if isinstance(self.prompt, Prompt) else Prompt(self.prompt)     )     # Extract specific parameters for from_prompt method     max_similar_examples_val = kwargs.get("max_similar_examples", 3)     similarity_threshold_val = kwargs.get("similarity_threshold", 0.7)     max_similar_examples = (         int(max_similar_examples_val)         if isinstance(max_similar_examples_val, (int, str))         else 3     )     similarity_threshold = (         float(similarity_threshold_val)         if isinstance(similarity_threshold_val, (int, float, str))         else 0.7     )     # Convert BaseRagasEmbeddings to BaseRagasEmbedding if needed     if hasattr(embedding_model, "embed_query"):         # For legacy BaseRagasEmbeddings, we need to wrap it         # Create a wrapper that implements BaseRagasEmbedding interface         class EmbeddingWrapper:             def __init__(self, legacy_embedding):                 self.legacy_embedding = legacy_embedding              def embed_text(self, text: str, **kwargs) -> t.List[float]:                 return self.legacy_embedding.embed_query(text)              async def aembed_text(self, text: str, **kwargs) -> t.List[float]:                 return await self.legacy_embedding.aembed_query(text)          actual_embedding_model = EmbeddingWrapper(embedding_model)     else:         # Already BaseRagasEmbedding         actual_embedding_model = embedding_model      from ragas.prompt.dynamic_few_shot import DynamicFewShotPrompt      self.prompt = DynamicFewShotPrompt.from_prompt(         self.prompt,         actual_embedding_model,  # type: ignore[arg-type]         max_similar_examples,         similarity_threshold,     )     train_dataset.reload()     total_items = len(train_dataset)     input_vars = self.get_variables()     output_vars = [self.name, f"{self.name}_reason"]      from rich.progress import Progress      with Progress() as progress:         task = progress.add_task("Processing examples", total=total_items)         for row in train_dataset:             inputs = {                 var: train_dataset.get_row_value(row, var) for var in input_vars             }             inputs = {k: v for k, v in inputs.items() if v is not None}             output = {                 var: train_dataset.get_row_value(row, var) for var in output_vars             }             output = {k: v for k, v in output.items() if v is not None}              if output:                 self.prompt.add_example(inputs, output)             progress.update(task, advance=1) ``` |

### validate\_alignment

```
validate_alignment(llm: 'BaseRagasLLM', test_dataset: 'Dataset', mapping: Dict[str, str] = {})
```

Args:
llm: The LLM instance to use for scoring.
test\_dataset: An Dataset instance containing the gold standard scores.
mapping: A dictionary mapping variable names expected by metrics to their corresponding names in the gold experiment.

Validate the alignment of the metric by comparing the scores against a gold standard experiment.
This method computes the Cohen's Kappa score and agreement rate between the gold standard scores and
the predicted scores from the metric.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1395 1396 1397 1398 1399 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1415 1416 1417 1418 1419 1420 1421 1422 1423 1424 1425 1426 1427 1428 1429 1430 1431 1432 1433 1434 1435 1436 1437 1438 1439 1440 1441 1442 1443 ``` | ``` def validate_alignment(     self,     llm: "BaseRagasLLM",     test_dataset: "Dataset",     mapping: t.Dict[str, str] = {}, ):     """     Args:         llm: The LLM instance to use for scoring.         test_dataset: An Dataset instance containing the gold standard scores.         mapping: A dictionary mapping variable names expected by metrics to their corresponding names in the gold experiment.      Validate the alignment of the metric by comparing the scores against a gold standard experiment.     This method computes the Cohen's Kappa score and agreement rate between the gold standard scores and     the predicted scores from the metric.     """      test_dataset.reload()     gold_scores_raw = [         test_dataset.get_row_value(row, self.name) for row in test_dataset     ]     pred_scores = []     for row in test_dataset:         values = {             v: (                 test_dataset.get_row_value(row, v)                 if v not in mapping                 else test_dataset.get_row_value(row, mapping.get(v, v))             )             for v in self.get_variables()         }         score = self.score(llm=llm, **values)         pred_scores.append(score.value)      # Convert to strings for correlation calculation, filtering out None values     gold_scores = [str(score) for score in gold_scores_raw if score is not None]     pred_scores_str = [str(score) for score in pred_scores if score is not None]      df = test_dataset.to_pandas()     df[f"{self.name}_pred"] = pred_scores     correlation = self.get_correlation(gold_scores, pred_scores_str)     agreement_rate = sum(         x == y for x, y in zip(gold_scores, pred_scores_str)     ) / len(gold_scores)     return {         "correlation": correlation,         "agreement_rate": agreement_rate,         "df": df,     } ``` |

## create\_auto\_response\_model

```
create_auto_response_model(name: str, **fields) -> Type['BaseModel']
```

Create a response model and mark it as auto-generated by Ragas.

This function creates a Pydantic model using create\_model and marks it
with a special attribute to indicate it was auto-generated. This allows
the save() method to distinguish between auto-generated models (which
are recreated on load) and custom user models.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name for the model class | *required* |
| `**fields` |  | Field definitions in create\_model format. Each field is specified as: field\_name=(type, default\_or\_field\_info) | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `Type[BaseModel]` | Pydantic model class marked as auto-generated |

Examples:

```
>>> from pydantic import Field
>>> # Simple model with required fields
>>> ResponseModel = create_auto_response_model(
...     "ResponseModel",
...     value=(str, ...),
...     reason=(str, ...)
... )
>>>
>>> # Model with Field validators and descriptions
>>> ResponseModel = create_auto_response_model(
...     "ResponseModel",
...     value=(str, Field(..., description="The predicted value")),
...     reason=(str, Field(..., description="Reasoning for the prediction"))
... )
```

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 835 836 837 838 839 840 841 842 ``` | ``` def create_auto_response_model(name: str, **fields) -> t.Type["BaseModel"]:     """     Create a response model and mark it as auto-generated by Ragas.      This function creates a Pydantic model using create_model and marks it     with a special attribute to indicate it was auto-generated. This allows     the save() method to distinguish between auto-generated models (which     are recreated on load) and custom user models.      Parameters     ----------     name : str         Name for the model class     **fields         Field definitions in create_model format.         Each field is specified as: field_name=(type, default_or_field_info)      Returns     -------     Type[BaseModel]         Pydantic model class marked as auto-generated      Examples     --------     >>> from pydantic import Field     >>> # Simple model with required fields     >>> ResponseModel = create_auto_response_model(     ...     "ResponseModel",     ...     value=(str, ...),     ...     reason=(str, ...)     ... )     >>>     >>> # Model with Field validators and descriptions     >>> ResponseModel = create_auto_response_model(     ...     "ResponseModel",     ...     value=(str, Field(..., description="The predicted value")),     ...     reason=(str, Field(..., description="Reasoning for the prediction"))     ... )     """     from pydantic import create_model      model = create_model(name, **fields)     setattr(model, "__ragas_auto_generated__", True)  # type: ignore[attr-defined]     return model ``` |

## Metric `dataclass`

```
Metric(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '')
```

Bases: `ABC`

Abstract base class for metrics in Ragas.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | The name of the metric. |
| `required_columns` | `Dict[str, Set[str]]` | A dictionary mapping metric type names to sets of required column names. This is a property and raises `ValueError` if columns are not in `VALID_COLUMNS`. |

### init `abstractmethod`

```
init(run_config: RunConfig) -> None
```

Initialize the metric with the given run configuration.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `run_config` | `RunConfig` | Configuration for the metric run including timeouts and other settings. | *required* |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 141 142 143 144 145 146 147 148 149 150 151 ``` | ``` @abstractmethod def init(self, run_config: RunConfig) -> None:     """     Initialize the metric with the given run configuration.      Parameters     ----------     run_config : RunConfig         Configuration for the metric run including timeouts and other settings.     """     ... ``` |

## MetricType

Bases: `Enum`

Enumeration of metric types in Ragas.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `SINGLE_TURN` | `str` | Represents a single-turn metric type. |
| `MULTI_TURN` | `str` | Represents a multi-turn metric type. |

## MetricWithLLM `dataclass`

```
MetricWithLLM(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '', llm: Optional[BaseRagasLLM] = None, output_type: Optional[MetricOutputType] = None)
```

Bases: `Metric`, `PromptMixin`

A metric class that uses a language model for evaluation.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `llm` | `Optional[BaseRagasLLM]` | The language model used for the metric. Both BaseRagasLLM and InstructorBaseRagasLLM are accepted at runtime via duck typing (both have compatible methods). |

### init

```
init(run_config: RunConfig) -> None
```

Initialize the metric with run configuration and validate LLM is present.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `run_config` | `RunConfig` | Configuration for the metric run. | *required* |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If no LLM is provided to the metric. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 ``` | ``` def init(self, run_config: RunConfig) -> None:     """     Initialize the metric with run configuration and validate LLM is present.      Parameters     ----------     run_config : RunConfig         Configuration for the metric run.      Raises     ------     ValueError         If no LLM is provided to the metric.     """     if self.llm is None:         raise ValueError(             f"Metric '{self.name}' has no valid LLM provided (self.llm is None). Please instantiate the metric with an LLM to run."         )     # Only BaseRagasLLM has set_run_config method, not InstructorBaseRagasLLM     if isinstance(self.llm, BaseRagasLLM):         self.llm.set_run_config(run_config) ``` |

### train

```
train(path: str, demonstration_config: Optional[DemonstrationConfig] = None, instruction_config: Optional[InstructionConfig] = None, callbacks: Optional[Callbacks] = None, run_config: Optional[RunConfig] = None, batch_size: Optional[int] = None, with_debugging_logs=False, raise_exceptions: bool = True) -> None
```

Train the metric using local JSON data

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `path` | `str` | Path to local JSON training data file | *required* |
| `demonstration_config` | `DemonstrationConfig` | Configuration for demonstration optimization | `None` |
| `instruction_config` | `InstructionConfig` | Configuration for instruction optimization | `None` |
| `callbacks` | `Callbacks` | List of callback functions | `None` |
| `run_config` | `RunConfig` | Run configuration | `None` |
| `batch_size` | `int` | Batch size for training | `None` |
| `with_debugging_logs` | `bool` | Enable debugging logs | `False` |
| `raise_exceptions` | `bool` | Whether to raise exceptions during training | `True` |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If path is not provided or not a JSON file |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 ``` | ``` def train(     self,     path: str,     demonstration_config: t.Optional[DemonstrationConfig] = None,     instruction_config: t.Optional[InstructionConfig] = None,     callbacks: t.Optional[Callbacks] = None,     run_config: t.Optional[RunConfig] = None,     batch_size: t.Optional[int] = None,     with_debugging_logs=False,     raise_exceptions: bool = True, ) -> None:     """     Train the metric using local JSON data      Parameters     ----------     path : str         Path to local JSON training data file     demonstration_config : DemonstrationConfig, optional         Configuration for demonstration optimization     instruction_config : InstructionConfig, optional         Configuration for instruction optimization     callbacks : Callbacks, optional         List of callback functions     run_config : RunConfig, optional         Run configuration     batch_size : int, optional         Batch size for training     with_debugging_logs : bool, default=False         Enable debugging logs     raise_exceptions : bool, default=True         Whether to raise exceptions during training      Raises     ------     ValueError         If path is not provided or not a JSON file     """     # Validate input parameters     if not path:         raise ValueError("Path to training data file must be provided")      if not path.endswith(".json"):         raise ValueError("Train data must be in json format")      run_config = run_config or RunConfig()     callbacks = callbacks or []      # Load the dataset from JSON file     dataset = MetricAnnotation.from_json(path, metric_name=self.name)      # only optimize the instruction if instruction_config is provided     if instruction_config is not None:         self._optimize_instruction(             instruction_config=instruction_config,             dataset=dataset,             callbacks=callbacks,             run_config=run_config,             batch_size=batch_size,             with_debugging_logs=with_debugging_logs,             raise_exceptions=raise_exceptions,         )      # if demonstration_config is provided, optimize the demonstrations     if demonstration_config is not None:         self._optimize_demonstration(             demonstration_config=demonstration_config,             dataset=dataset,         ) ``` |

## MultiTurnMetric `dataclass`

```
MultiTurnMetric(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '')
```

Bases: `Metric`

A metric class for evaluating multi-turn conversations.

This class extends the base Metric class to provide functionality
for scoring multi-turn conversation samples.

### multi\_turn\_score

```
multi_turn_score(sample: MultiTurnSample, callbacks: Callbacks = None) -> float
```

Score a multi-turn conversation sample synchronously.

May raise ImportError if nest\_asyncio is not installed in Jupyter-like environments.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 ``` | ``` def multi_turn_score(     self,     sample: MultiTurnSample,     callbacks: Callbacks = None, ) -> float:     """     Score a multi-turn conversation sample synchronously.      May raise ImportError if nest_asyncio is not installed in Jupyter-like environments.     """     callbacks = callbacks or []     sample = self._only_required_columns_multi_turn(sample)     rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )      async def _async_wrapper():         try:             result = await self._multi_turn_ascore(                 sample=sample, callbacks=group_cm             )         except Exception as e:             if not group_cm.ended:                 rm.on_chain_error(e)             raise e         else:             if not group_cm.ended:                 rm.on_chain_end({"output": result})             return result      apply_nest_asyncio()     score = run(_async_wrapper)      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )     return score ``` |

### multi\_turn\_ascore `async`

```
multi_turn_ascore(sample: MultiTurnSample, callbacks: Callbacks = None, timeout: Optional[float] = None) -> float
```

Score a multi-turn conversation sample asynchronously.

May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 ``` | ``` async def multi_turn_ascore(     self,     sample: MultiTurnSample,     callbacks: Callbacks = None,     timeout: t.Optional[float] = None, ) -> float:     """     Score a multi-turn conversation sample asynchronously.      May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.     """     callbacks = callbacks or []     sample = self._only_required_columns_multi_turn(sample)      rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )     try:         score = await asyncio.wait_for(             self._multi_turn_ascore(sample=sample, callbacks=group_cm),             timeout=timeout,         )     except Exception as e:         if not group_cm.ended:             rm.on_chain_error(e)         raise e     else:         if not group_cm.ended:             rm.on_chain_end({"output": score})      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )      return score ``` |

## BaseMetric `dataclass`

```
BaseMetric(name: str, allowed_values: AllowedValuesType = (lambda: ['pass', 'fail'])())
```

Bases: `ABC`

Base class for simple metrics that return MetricResult objects.

This class provides the foundation for metrics that evaluate inputs
and return structured MetricResult objects containing scores and reasoning.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | The name of the metric. |
| `allowed_values` | `AllowedValuesType` | Allowed values for the metric output. Can be a list of strings for discrete metrics, a tuple of floats for numeric metrics, or an integer for ranking metrics. |

Examples:

```
>>> from ragas.metrics import discrete_metric
>>>
>>> @discrete_metric(name="sentiment", allowed_values=["positive", "negative"])
>>> def sentiment_metric(user_input: str, response: str) -> str:
...     return "positive" if "good" in response else "negative"
>>>
>>> result = sentiment_metric(user_input="How are you?", response="I'm good!")
>>> print(result.value)  # "positive"
```

### score `abstractmethod`

```
score(**kwargs) -> 'MetricResult'
```

Synchronously calculate the metric score.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `**kwargs` | `dict` | Input parameters required by the specific metric implementation. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `MetricResult` | The evaluation result containing the score and reasoning. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 ``` | ``` @abstractmethod def score(self, **kwargs) -> "MetricResult":     """     Synchronously calculate the metric score.      Parameters     ----------     **kwargs : dict         Input parameters required by the specific metric implementation.      Returns     -------     MetricResult         The evaluation result containing the score and reasoning.     """     pass ``` |

### ascore `abstractmethod` `async`

```
ascore(**kwargs) -> 'MetricResult'
```

Asynchronously calculate the metric score.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `**kwargs` | `dict` | Input parameters required by the specific metric implementation. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `MetricResult` | The evaluation result containing the score and reasoning. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 ``` | ``` @abstractmethod async def ascore(self, **kwargs) -> "MetricResult":     """     Asynchronously calculate the metric score.      Parameters     ----------     **kwargs : dict         Input parameters required by the specific metric implementation.      Returns     -------     MetricResult         The evaluation result containing the score and reasoning.     """     pass ``` |

### batch\_score

```
batch_score(inputs: List[Dict[str, Any]]) -> List['MetricResult']
```

Synchronously calculate scores for a batch of inputs.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `inputs` | `List[Dict[str, Any]]` | List of input dictionaries, each containing parameters for the metric. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `List[MetricResult]` | List of evaluation results, one for each input. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 ``` | ``` def batch_score(     self,     inputs: t.List[t.Dict[str, t.Any]], ) -> t.List["MetricResult"]:     """     Synchronously calculate scores for a batch of inputs.      Parameters     ----------     inputs : List[Dict[str, Any]]         List of input dictionaries, each containing parameters for the metric.      Returns     -------     List[MetricResult]         List of evaluation results, one for each input.     """     return [self.score(**input_dict) for input_dict in inputs] ``` |

### abatch\_score `async`

```
abatch_score(inputs: List[Dict[str, Any]]) -> List['MetricResult']
```

Asynchronously calculate scores for a batch of inputs in parallel.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `inputs` | `List[Dict[str, Any]]` | List of input dictionaries, each containing parameters for the metric. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `List[MetricResult]` | List of evaluation results, one for each input. |

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 ``` | ``` async def abatch_score(     self,     inputs: t.List[t.Dict[str, t.Any]], ) -> t.List["MetricResult"]:     """     Asynchronously calculate scores for a batch of inputs in parallel.      Parameters     ----------     inputs : List[Dict[str, Any]]         List of input dictionaries, each containing parameters for the metric.      Returns     -------     List[MetricResult]         List of evaluation results, one for each input.     """     async_tasks = []     for input_dict in inputs:         # Process input asynchronously         async_tasks.append(self.ascore(**input_dict))      # Run all tasks concurrently and return results     return await asyncio.gather(*async_tasks) ``` |

## LLMMetric `dataclass`

```
LLMMetric(name: str, allowed_values: AllowedValuesType = (lambda: ['pass', 'fail'])(), prompt: Optional[Union[str, 'Prompt']] = None)
```

Bases: `SimpleBaseMetric`

LLM-based metric that uses prompts to generate structured responses.

### save

```
save(path: Optional[str] = None) -> None
```

Save the metric configuration to a JSON file.

Parameters:

path : str, optional
File path to save to. If not provided, saves to "./{metric.name}.json"
Use .gz extension for compression.


Note:

If the metric has a response\_model, its schema will be saved for reference
but the model itself cannot be serialized. You'll need to provide it when loading.


Examples:

All these work:

> > > metric.save() # → ./response\_quality.json
> > > metric.save("custom.json") # → ./custom.json
> > > metric.save("/path/to/metrics/") # → /path/to/metrics/response\_quality.json
> > > metric.save("no\_extension") # → ./no\_extension.json
> > > metric.save("compressed.json.gz") # → ./compressed.json.gz (compressed)


Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ```  935  936  937  938  939  940  941  942  943  944  945  946  947  948  949  950  951  952  953  954  955  956  957  958  959  960  961  962  963  964  965  966  967  968  969  970  971  972  973  974  975  976  977  978  979  980  981  982  983  984  985  986  987  988  989  990  991  992  993  994  995  996  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 ``` | ``` def save(self, path: t.Optional[str] = None) -> None:     """     Save the metric configuration to a JSON file.      Parameters:     -----------     path : str, optional         File path to save to. If not provided, saves to "./{metric.name}.json"         Use .gz extension for compression.      Note:     -----     If the metric has a response_model, its schema will be saved for reference     but the model itself cannot be serialized. You'll need to provide it when loading.      Examples:     ---------     All these work:     >>> metric.save()                      # → ./response_quality.json     >>> metric.save("custom.json")         # → ./custom.json     >>> metric.save("/path/to/metrics/")   # → /path/to/metrics/response_quality.json     >>> metric.save("no_extension")        # → ./no_extension.json     >>> metric.save("compressed.json.gz")  # → ./compressed.json.gz (compressed)     """     import gzip     import json     import warnings     from pathlib import Path      # Handle default path     if path is None:         # Default to current directory with metric name as filename         file_path = Path(f"./{self.name}.json")     else:         file_path = Path(path)          # If path is a directory, append the metric name as filename         if file_path.is_dir():             file_path = file_path / f"{self.name}.json"         # If path has no extension, add .json         elif not file_path.suffix:             file_path = file_path.with_suffix(".json")      # Collect warning messages for data loss     warning_messages = []      if hasattr(self, "_response_model") and self._response_model:         # Only warn for custom response models, not auto-generated ones         if not getattr(self._response_model, "__ragas_auto_generated__", False):             warning_messages.append(                 "- Custom response_model will be lost (set it manually after loading)"             )      # Serialize the prompt (may add embedding_model warning)     prompt_data = self._serialize_prompt(warning_messages)      # Determine the metric type     metric_type = self.__class__.__name__      # Get metric-specific config     config = self._get_metric_config()      # Emit consolidated warning if there's data loss     if warning_messages:         warnings.warn(             "Some metric components cannot be saved and will be lost:\n"             + "\n".join(warning_messages)             + "\n\nYou'll need to provide these when loading the metric."         )      data = {         "format_version": "1.0",         "metric_type": metric_type,         "name": self.name,         "prompt": prompt_data,         "config": config,         "response_model_info": self._serialize_response_model_info(),     }     try:         if file_path.suffix == ".gz":             with gzip.open(file_path, "wt", encoding="utf-8") as f:                 json.dump(data, f, indent=2)         else:             with open(file_path, "w", encoding="utf-8") as f:                 json.dump(data, f, indent=2)     except (OSError, IOError) as e:         raise ValueError(f"Cannot save metric to {file_path}: {e}") ``` |

### load `classmethod`

```
load(path: str, response_model: Optional[Type['BaseModel']] = None, embedding_model: Optional['EmbeddingModelType'] = None) -> 'SimpleLLMMetric'
```

Load a metric from a JSON file.

Parameters:

path : str
File path to load from. Supports .gz compressed files.
response\_model : Optional[Type[BaseModel]]
Pydantic model to use for response validation. Required for custom SimpleLLMMetrics.
embedding\_model : Optional[Any]
Embedding model for DynamicFewShotPrompt. Required if the original used one.


Returns:

SimpleLLMMetric
Loaded metric instance


Raises:

ValueError
If file cannot be loaded, is invalid, or missing required models


Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 1194 1195 1196 1197 1198 1199 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 ``` | ``` @classmethod def load(     cls,     path: str,     response_model: t.Optional[t.Type["BaseModel"]] = None,     embedding_model: t.Optional["EmbeddingModelType"] = None, ) -> "SimpleLLMMetric":     """     Load a metric from a JSON file.      Parameters:     -----------     path : str         File path to load from. Supports .gz compressed files.     response_model : Optional[Type[BaseModel]]         Pydantic model to use for response validation. Required for custom SimpleLLMMetrics.     embedding_model : Optional[Any]         Embedding model for DynamicFewShotPrompt. Required if the original used one.      Returns:     --------     SimpleLLMMetric         Loaded metric instance      Raises:     -------     ValueError         If file cannot be loaded, is invalid, or missing required models     """     import gzip     import json     from pathlib import Path      file_path = Path(path)      # Load JSON data     try:         if file_path.suffix == ".gz":             with gzip.open(file_path, "rt", encoding="utf-8") as f:                 data = json.load(f)         else:             with open(file_path, "r", encoding="utf-8") as f:                 data = json.load(f)     except (FileNotFoundError, json.JSONDecodeError, OSError) as e:         raise ValueError(f"Cannot load metric from {path}: {e}")      # Validate format     if data.get("format_version") != "1.0":         import warnings          warnings.warn(             f"Loading metric with format version {data.get('format_version')}, expected 1.0"         )      # Reconstruct the prompt     prompt = cls._deserialize_prompt(data["prompt"], embedding_model)      # Get config     config = data.get("config", {})      # Create the metric instance     metric = cls(name=data["name"], prompt=prompt, **config)      # Set response model if provided     if response_model:         metric._response_model = response_model      return metric ``` |

### get\_correlation `abstractmethod`

```
get_correlation(gold_labels: List[str], predictions: List[str]) -> float
```

Calculate the correlation between gold scores and predicted scores.
This is a placeholder method and should be implemented based on the specific metric.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1275 1276 1277 1278 1279 1280 1281 1282 1283 ``` | ``` @abstractmethod def get_correlation(     self, gold_labels: t.List[str], predictions: t.List[str] ) -> float:     """     Calculate the correlation between gold scores and predicted scores.     This is a placeholder method and should be implemented based on the specific metric.     """     pass ``` |

### align\_and\_validate

```
align_and_validate(dataset: 'Dataset', embedding_model: 'EmbeddingModelType', llm: 'BaseRagasLLM', test_size: float = 0.2, random_state: int = 42, **kwargs: Dict[str, Any])
```

Args:
dataset: experiment to align the metric with.
embedding\_model: The embedding model used for dynamic few-shot prompting.
llm: The LLM instance to use for scoring.

Align the metric with the specified experiments and validate it against a gold standard experiment.
This method combines alignment and validation into a single step.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 ``` | ``` def align_and_validate(     self,     dataset: "Dataset",     embedding_model: "EmbeddingModelType",     llm: "BaseRagasLLM",     test_size: float = 0.2,     random_state: int = 42,     **kwargs: t.Dict[str, t.Any], ):     """     Args:         dataset: experiment to align the metric with.         embedding_model: The embedding model used for dynamic few-shot prompting.         llm: The LLM instance to use for scoring.      Align the metric with the specified experiments and validate it against a gold standard experiment.     This method combines alignment and validation into a single step.     """     train_dataset, test_dataset = dataset.train_test_split(         test_size=test_size, random_state=random_state     )      self.align(train_dataset, embedding_model, **kwargs)  # type: ignore     return self.validate_alignment(llm, test_dataset)  # type: ignore ``` |

### align

```
align(train_dataset: 'Dataset', embedding_model: 'EmbeddingModelType', **kwargs: Dict[str, Any])
```

Args:
train\_dataset: train\_dataset to align the metric with.
embedding\_model: The embedding model used for dynamic few-shot prompting.

Align the metric with the specified experiments by different optimization methods.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1310 1311 1312 1313 1314 1315 1316 1317 1318 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 1331 1332 1333 1334 1335 1336 1337 1338 1339 1340 1341 1342 1343 1344 1345 1346 1347 1348 1349 1350 1351 1352 1353 1354 1355 1356 1357 1358 1359 1360 1361 1362 1363 1364 1365 1366 1367 1368 1369 1370 1371 1372 1373 1374 1375 1376 1377 1378 1379 1380 1381 1382 1383 1384 1385 1386 1387 1388 1389 1390 1391 1392 1393 ``` | ``` def align(     self,     train_dataset: "Dataset",     embedding_model: "EmbeddingModelType",     **kwargs: t.Dict[str, t.Any], ):     """     Args:         train_dataset: train_dataset to align the metric with.         embedding_model: The embedding model used for dynamic few-shot prompting.      Align the metric with the specified experiments by different optimization methods.     """      # get prompt     if not self.prompt:         raise Exception("prompt not passed")     from ragas.prompt.simple_prompt import Prompt      self.prompt = (         self.prompt if isinstance(self.prompt, Prompt) else Prompt(self.prompt)     )     # Extract specific parameters for from_prompt method     max_similar_examples_val = kwargs.get("max_similar_examples", 3)     similarity_threshold_val = kwargs.get("similarity_threshold", 0.7)     max_similar_examples = (         int(max_similar_examples_val)         if isinstance(max_similar_examples_val, (int, str))         else 3     )     similarity_threshold = (         float(similarity_threshold_val)         if isinstance(similarity_threshold_val, (int, float, str))         else 0.7     )     # Convert BaseRagasEmbeddings to BaseRagasEmbedding if needed     if hasattr(embedding_model, "embed_query"):         # For legacy BaseRagasEmbeddings, we need to wrap it         # Create a wrapper that implements BaseRagasEmbedding interface         class EmbeddingWrapper:             def __init__(self, legacy_embedding):                 self.legacy_embedding = legacy_embedding              def embed_text(self, text: str, **kwargs) -> t.List[float]:                 return self.legacy_embedding.embed_query(text)              async def aembed_text(self, text: str, **kwargs) -> t.List[float]:                 return await self.legacy_embedding.aembed_query(text)          actual_embedding_model = EmbeddingWrapper(embedding_model)     else:         # Already BaseRagasEmbedding         actual_embedding_model = embedding_model      from ragas.prompt.dynamic_few_shot import DynamicFewShotPrompt      self.prompt = DynamicFewShotPrompt.from_prompt(         self.prompt,         actual_embedding_model,  # type: ignore[arg-type]         max_similar_examples,         similarity_threshold,     )     train_dataset.reload()     total_items = len(train_dataset)     input_vars = self.get_variables()     output_vars = [self.name, f"{self.name}_reason"]      from rich.progress import Progress      with Progress() as progress:         task = progress.add_task("Processing examples", total=total_items)         for row in train_dataset:             inputs = {                 var: train_dataset.get_row_value(row, var) for var in input_vars             }             inputs = {k: v for k, v in inputs.items() if v is not None}             output = {                 var: train_dataset.get_row_value(row, var) for var in output_vars             }             output = {k: v for k, v in output.items() if v is not None}              if output:                 self.prompt.add_example(inputs, output)             progress.update(task, advance=1) ``` |

### validate\_alignment

```
validate_alignment(llm: 'BaseRagasLLM', test_dataset: 'Dataset', mapping: Dict[str, str] = {})
```

Args:
llm: The LLM instance to use for scoring.
test\_dataset: An Dataset instance containing the gold standard scores.
mapping: A dictionary mapping variable names expected by metrics to their corresponding names in the gold experiment.

Validate the alignment of the metric by comparing the scores against a gold standard experiment.
This method computes the Cohen's Kappa score and agreement rate between the gold standard scores and
the predicted scores from the metric.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 1395 1396 1397 1398 1399 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1415 1416 1417 1418 1419 1420 1421 1422 1423 1424 1425 1426 1427 1428 1429 1430 1431 1432 1433 1434 1435 1436 1437 1438 1439 1440 1441 1442 1443 ``` | ``` def validate_alignment(     self,     llm: "BaseRagasLLM",     test_dataset: "Dataset",     mapping: t.Dict[str, str] = {}, ):     """     Args:         llm: The LLM instance to use for scoring.         test_dataset: An Dataset instance containing the gold standard scores.         mapping: A dictionary mapping variable names expected by metrics to their corresponding names in the gold experiment.      Validate the alignment of the metric by comparing the scores against a gold standard experiment.     This method computes the Cohen's Kappa score and agreement rate between the gold standard scores and     the predicted scores from the metric.     """      test_dataset.reload()     gold_scores_raw = [         test_dataset.get_row_value(row, self.name) for row in test_dataset     ]     pred_scores = []     for row in test_dataset:         values = {             v: (                 test_dataset.get_row_value(row, v)                 if v not in mapping                 else test_dataset.get_row_value(row, mapping.get(v, v))             )             for v in self.get_variables()         }         score = self.score(llm=llm, **values)         pred_scores.append(score.value)      # Convert to strings for correlation calculation, filtering out None values     gold_scores = [str(score) for score in gold_scores_raw if score is not None]     pred_scores_str = [str(score) for score in pred_scores if score is not None]      df = test_dataset.to_pandas()     df[f"{self.name}_pred"] = pred_scores     correlation = self.get_correlation(gold_scores, pred_scores_str)     agreement_rate = sum(         x == y for x, y in zip(gold_scores, pred_scores_str)     ) / len(gold_scores)     return {         "correlation": correlation,         "agreement_rate": agreement_rate,         "df": df,     } ``` |

## SingleTurnMetric `dataclass`

```
SingleTurnMetric(_required_columns: Dict[MetricType, Set[str]] = dict(), name: str = '')
```

Bases: `Metric`

A metric class for evaluating single-turn interactions.

This class provides methods to score single-turn samples, both synchronously and asynchronously.

### single\_turn\_score

```
single_turn_score(sample: SingleTurnSample, callbacks: Callbacks = None) -> float
```

Synchronously score a single-turn sample.

May raise ImportError if nest\_asyncio is not installed in a Jupyter-like environment.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 ``` | ``` def single_turn_score(     self,     sample: SingleTurnSample,     callbacks: Callbacks = None, ) -> float:     """     Synchronously score a single-turn sample.      May raise ImportError if nest_asyncio is not installed in a Jupyter-like environment.     """     callbacks = callbacks or []     # only get the required columns     sample = self._only_required_columns_single_turn(sample)     rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )      async def _async_wrapper():         try:             result = await self._single_turn_ascore(                 sample=sample, callbacks=group_cm             )         except Exception as e:             if not group_cm.ended:                 rm.on_chain_error(e)             raise e         else:             if not group_cm.ended:                 rm.on_chain_end({"output": result})             return result      apply_nest_asyncio()     score = run(_async_wrapper)      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )     return score ``` |

### single\_turn\_ascore `async`

```
single_turn_ascore(sample: SingleTurnSample, callbacks: Callbacks = None, timeout: Optional[float] = None) -> float
```

Asynchronously score a single-turn sample with an optional timeout.

May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.

Source code in `src/ragas/metrics/base.py`

|  |  |
| --- | --- |
| ``` 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 ``` | ``` async def single_turn_ascore(     self,     sample: SingleTurnSample,     callbacks: Callbacks = None,     timeout: t.Optional[float] = None, ) -> float:     """     Asynchronously score a single-turn sample with an optional timeout.      May raise asyncio.TimeoutError if the scoring process exceeds the specified timeout.     """     callbacks = callbacks or []     # only get the required columns     sample = self._only_required_columns_single_turn(sample)     rm, group_cm = new_group(         self.name,         inputs=sample.to_dict(),         callbacks=callbacks,         metadata={"type": ChainType.METRIC},     )     try:         score = await asyncio.wait_for(             self._single_turn_ascore(sample=sample, callbacks=group_cm),             timeout=timeout,         )     except Exception as e:         if not group_cm.ended:             rm.on_chain_error(e)         raise e     else:         if not group_cm.ended:             rm.on_chain_end({"output": score})      # track the evaluation event     _analytics_batcher.add_evaluation(         EvaluationEvent(             metrics=[self.name],             num_rows=1,             evaluation_type=MetricType.SINGLE_TURN.name,             language=get_metric_language(self),         )     )     return score ``` |

## DiscreteMetric `dataclass`

```
DiscreteMetric(name: str, allowed_values: List[str] = (lambda: ['pass', 'fail'])(), prompt: Optional[Union[str, 'Prompt']] = None)
```

Bases: `SimpleLLMMetric`, `DiscreteValidator`

Metric for categorical/discrete evaluations with predefined allowed values.

This class is used for metrics that output categorical values like
"pass/fail", "good/bad/excellent", or custom discrete categories.
Uses the instructor library for structured LLM outputs.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `allowed_values` | `List[str]` | List of allowed categorical values the metric can output. Default is ["pass", "fail"]. |
| `llm` | `Optional[BaseRagasLLM]` | The language model instance for evaluation. Can be created using llm\_factory(). |
| `prompt` | `Optional[Union[str, Prompt]]` | The prompt template for the metric. Should contain placeholders for evaluation inputs that will be formatted at runtime. |

Examples:

```
>>> from ragas.metrics import DiscreteMetric
>>> from ragas.llms import llm_factory
>>> from openai import OpenAI
>>>
>>> # Create an LLM instance
>>> client = OpenAI(api_key="your-api-key")
>>> llm = llm_factory("gpt-4o-mini", client=client)
>>>
>>> # Create a custom discrete metric
>>> metric = DiscreteMetric(
...     name="quality_check",
...     llm=llm,
...     prompt="Check the quality of the response: {response}. Return 'excellent', 'good', or 'poor'.",
...     allowed_values=["excellent", "good", "poor"]
... )
>>>
>>> # Score with the metric
>>> result = metric.score(
...     llm=llm,
...     response="This is a great response!"
... )
>>> print(result.value)  # Output: "excellent" or similar
```

### get\_correlation

```
get_correlation(gold_labels: List[str], predictions: List[str]) -> float
```

Calculate the correlation between gold labels and predictions.
This is a placeholder method and should be implemented based on the specific metric.

Source code in `src/ragas/metrics/discrete.py`

|  |  |
| --- | --- |
| ``` 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 ``` | ``` def get_correlation(     self, gold_labels: t.List[str], predictions: t.List[str] ) -> float:     """     Calculate the correlation between gold labels and predictions.     This is a placeholder method and should be implemented based on the specific metric.     """     try:         from sklearn.metrics import cohen_kappa_score     except ImportError:         raise ImportError(             "scikit-learn is required for correlation calculation. "             "Please install it with `pip install scikit-learn`."         )     return cohen_kappa_score(gold_labels, predictions) ``` |

### load `classmethod`

```
load(path: str, embedding_model: Optional[EmbeddingModelType] = None) -> DiscreteMetric
```

Load a DiscreteMetric from a JSON file.

Parameters:

path : str
File path to load from. Supports .gz compressed files.
embedding\_model : Optional[Any]
Embedding model for DynamicFewShotPrompt. Required if the original used one.


Returns:

DiscreteMetric
Loaded metric instance


Raises:

ValueError
If file cannot be loaded or is not a DiscreteMetric


Source code in `src/ragas/metrics/discrete.py`

|  |  |
| --- | --- |
| ```  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 ``` | ``` @classmethod def load(     cls, path: str, embedding_model: t.Optional["EmbeddingModelType"] = None ) -> "DiscreteMetric":     """     Load a DiscreteMetric from a JSON file.      Parameters:     -----------     path : str         File path to load from. Supports .gz compressed files.     embedding_model : Optional[Any]         Embedding model for DynamicFewShotPrompt. Required if the original used one.      Returns:     --------     DiscreteMetric         Loaded metric instance      Raises:     -------     ValueError         If file cannot be loaded or is not a DiscreteMetric     """     # Validate metric type before loading     cls._validate_metric_type(path)      # Load using parent class method     metric = super().load(path, embedding_model=embedding_model)      # Additional type check for safety     if not isinstance(metric, cls):         raise ValueError(f"Loaded metric is not a {cls.__name__}")      return metric ``` |

## NumericMetric `dataclass`

```
NumericMetric(name: str, allowed_values: Union[Tuple[float, float], range] = (0.0, 1.0), prompt: Optional[Union[str, 'Prompt']] = None)
```

Bases: `SimpleLLMMetric`, `NumericValidator`

Metric for continuous numeric evaluations within a specified range.

This class is used for metrics that output numeric scores within a
defined range, such as 0.0 to 1.0 for similarity scores or 1-10 ratings.
Uses the instructor library for structured LLM outputs.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `allowed_values` | `Union[Tuple[float, float], range]` | The valid range for metric outputs. Can be a tuple of (min, max) floats or a range object. Default is (0.0, 1.0). |
| `llm` | `Optional[BaseRagasLLM]` | The language model instance for evaluation. Can be created using llm\_factory(). |
| `prompt` | `Optional[Union[str, Prompt]]` | The prompt template for the metric. Should contain placeholders for evaluation inputs that will be formatted at runtime. |

Examples:

```
>>> from ragas.metrics import NumericMetric
>>> from ragas.llms import llm_factory
>>> from openai import OpenAI
>>>
>>> # Create an LLM instance
>>> client = OpenAI(api_key="your-api-key")
>>> llm = llm_factory("gpt-4o-mini", client=client)
>>>
>>> # Create a custom numeric metric with 0-10 range
>>> metric = NumericMetric(
...     name="quality_score",
...     llm=llm,
...     prompt="Rate the quality of this response on a scale of 0-10: {response}",
...     allowed_values=(0.0, 10.0)
... )
>>>
>>> # Score with the metric
>>> result = metric.score(
...     llm=llm,
...     response="This is a great response!"
... )
>>> print(result.value)  # Output: a float between 0.0 and 10.0
```

### get\_correlation

```
get_correlation(gold_labels: List[str], predictions: List[str]) -> float
```

Calculate the correlation between gold labels and predictions.
This is a placeholder method and should be implemented based on the specific metric.

Source code in `src/ragas/metrics/numeric.py`

|  |  |
| --- | --- |
| ``` 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 ``` | ``` def get_correlation(     self, gold_labels: t.List[str], predictions: t.List[str] ) -> float:     """     Calculate the correlation between gold labels and predictions.     This is a placeholder method and should be implemented based on the specific metric.     """     try:         from scipy.stats import pearsonr     except ImportError:         raise ImportError(             "scipy is required for correlation calculation. "             "Please install it with `pip install scipy`."         )     # Convert strings to floats for correlation calculation     gold_floats = [float(x) for x in gold_labels]     pred_floats = [float(x) for x in predictions]     result = pearsonr(gold_floats, pred_floats)     # pearsonr returns (correlation, p-value) tuple     correlation = t.cast(float, result[0])     return correlation ``` |

### load `classmethod`

```
load(path: str, embedding_model: Optional[EmbeddingModelType] = None) -> NumericMetric
```

Load a NumericMetric from a JSON file.

Parameters:

path : str
File path to load from. Supports .gz compressed files.
embedding\_model : Optional[Any]
Embedding model for DynamicFewShotPrompt. Required if the original used one.


Returns:

NumericMetric
Loaded metric instance


Raises:

ValueError
If file cannot be loaded or is not a NumericMetric


Source code in `src/ragas/metrics/numeric.py`

|  |  |
| --- | --- |
| ```  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 ``` | ``` @classmethod def load(     cls, path: str, embedding_model: t.Optional["EmbeddingModelType"] = None ) -> "NumericMetric":     """     Load a NumericMetric from a JSON file.      Parameters:     -----------     path : str         File path to load from. Supports .gz compressed files.     embedding_model : Optional[Any]         Embedding model for DynamicFewShotPrompt. Required if the original used one.      Returns:     --------     NumericMetric         Loaded metric instance      Raises:     -------     ValueError         If file cannot be loaded or is not a NumericMetric     """     # Validate metric type before loading     cls._validate_metric_type(path)      # Load using parent class method     metric = super().load(path, embedding_model=embedding_model)      # Additional type check for safety     if not isinstance(metric, cls):         raise ValueError(f"Loaded metric is not a {cls.__name__}")      # Convert allowed_values back to tuple if it's a list (due to JSON serialization)     if hasattr(metric, "allowed_values") and isinstance(         metric.allowed_values, list     ):         # Ensure it's a 2-element tuple for NumericMetric         if len(metric.allowed_values) == 2:             metric.allowed_values = (                 metric.allowed_values[0],                 metric.allowed_values[1],             )         else:             metric.allowed_values = tuple(metric.allowed_values)  # type: ignore      return metric ``` |

## RankingMetric `dataclass`

```
RankingMetric(name: str, allowed_values: int = 2, prompt: Optional[Union[str, 'Prompt']] = None)
```

Bases: `SimpleLLMMetric`, `RankingValidator`

Metric for evaluations that produce ranked lists of items.

This class is used for metrics that output ordered lists, such as
ranking search results, prioritizing features, or ordering responses
by relevance. Uses the instructor library for structured LLM outputs.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `allowed_values` | `int` | Expected number of items in the ranking list. Default is 2. |
| `llm` | `Optional[BaseRagasLLM]` | The language model instance for evaluation. Can be created using llm\_factory(). |
| `prompt` | `Optional[Union[str, Prompt]]` | The prompt template for the metric. Should contain placeholders for evaluation inputs that will be formatted at runtime. |

Examples:

```
>>> from ragas.metrics import RankingMetric
>>> from ragas.llms import llm_factory
>>> from openai import OpenAI
>>>
>>> # Create an LLM instance
>>> client = OpenAI(api_key="your-api-key")
>>> llm = llm_factory("gpt-4o-mini", client=client)
>>>
>>> # Create a ranking metric that returns top 3 items
>>> metric = RankingMetric(
...     name="relevance_ranking",
...     llm=llm,
...     prompt="Rank these results by relevance: {results}",
...     allowed_values=3
... )
>>>
>>> # Score with the metric
>>> result = metric.score(
...     llm=llm,
...     results="result1, result2, result3"
... )
>>> print(result.value)  # Output: a list of 3 ranked items
```

### get\_correlation

```
get_correlation(gold_labels: List[str], predictions: List[str]) -> float
```

Calculate the correlation between gold labels and predictions.
This is a placeholder method and should be implemented based on the specific metric.

Source code in `src/ragas/metrics/ranking.py`

|  |  |
| --- | --- |
| ``` 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 ``` | ``` def get_correlation(     self, gold_labels: t.List[str], predictions: t.List[str] ) -> float:     """     Calculate the correlation between gold labels and predictions.     This is a placeholder method and should be implemented based on the specific metric.     """     try:         from sklearn.metrics import cohen_kappa_score     except ImportError:         raise ImportError(             "scikit-learn is required for correlation calculation. "             "Please install it with `pip install scikit-learn`."         )      kappa_scores = []     for gold_item, prediction in zip(gold_labels, predictions):         kappa = cohen_kappa_score(gold_item, prediction, weights="quadratic")         kappa_scores.append(kappa)      return sum(kappa_scores) / len(kappa_scores) if kappa_scores else 0.0 ``` |

### load `classmethod`

```
load(path: str, embedding_model: Optional[EmbeddingModelType] = None) -> RankingMetric
```

Load a RankingMetric from a JSON file.

Parameters:

path : str
File path to load from. Supports .gz compressed files.
embedding\_model : Optional[Any]
Embedding model for DynamicFewShotPrompt. Required if the original used one.


Returns:

RankingMetric
Loaded metric instance


Raises:

ValueError
If file cannot be loaded or is not a RankingMetric


Source code in `src/ragas/metrics/ranking.py`

|  |  |
| --- | --- |
| ```  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 ``` | ``` @classmethod def load(     cls, path: str, embedding_model: t.Optional["EmbeddingModelType"] = None ) -> "RankingMetric":     """     Load a RankingMetric from a JSON file.      Parameters:     -----------     path : str         File path to load from. Supports .gz compressed files.     embedding_model : Optional[Any]         Embedding model for DynamicFewShotPrompt. Required if the original used one.      Returns:     --------     RankingMetric         Loaded metric instance      Raises:     -------     ValueError         If file cannot be loaded or is not a RankingMetric     """     # Validate metric type before loading     cls._validate_metric_type(path)      # Load using parent class method     metric = super().load(path, embedding_model=embedding_model)      # Additional type check for safety     if not isinstance(metric, cls):         raise ValueError(f"Loaded metric is not a {cls.__name__}")      return metric ``` |

## MetricResult

```
MetricResult(value: Any, reason: Optional[str] = None, traces: Optional[Dict[str, Any]] = None)
```

Class to hold the result of a metric evaluation.

This class behaves like its underlying result value but still provides access
to additional metadata like reasoning.

Works with:
- DiscreteMetrics (string results)
- NumericMetrics (float/int results)
- RankingMetrics (list results)

Source code in `src/ragas/metrics/result.py`

|  |  |
| --- | --- |
| ``` 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 ``` | ``` def __init__(     self,     value: t.Any,     reason: t.Optional[str] = None,     traces: t.Optional[t.Dict[str, t.Any]] = None, ):     if traces is not None:         invalid_keys = [             key for key in traces.keys() if key not in {"input", "output"}         ]         if invalid_keys:             raise ValueError(                 f"Invalid keys in traces: {invalid_keys}. Allowed keys are 'input' and 'output'."             )     self._value = value     self.reason = reason     self.traces = traces ``` |

### value `property`

```
value
```

Get the raw result value.

### to\_dict

```
to_dict()
```

Convert the result to a dictionary.

Source code in `src/ragas/metrics/result.py`

|  |  |
| --- | --- |
| ``` 178 179 180 ``` | ``` def to_dict(self):     """Convert the result to a dictionary."""     return {"result": self._value, "reason": self.reason} ``` |

### validate `classmethod`

```
validate(value: Any, info: ValidationInfo)
```

Provide compatibility with older Pydantic versions.

Source code in `src/ragas/metrics/result.py`

|  |  |
| --- | --- |
| ``` 182 183 184 185 186 187 ``` | ``` @classmethod def validate(cls, value: t.Any, info: ValidationInfo):     """Provide compatibility with older Pydantic versions."""     if isinstance(value, MetricResult):         return value     return cls(value=value) ``` |

## discrete\_metric

```
discrete_metric(*, name: Optional[str] = None, allowed_values: Optional[List[str]] = None, **metric_params: Any) -> Callable[[Callable[..., Any]], DiscreteMetricProtocol]
```

Decorator for creating discrete/categorical metrics.

This decorator transforms a regular function into a DiscreteMetric instance
that can be used for evaluation with predefined categorical outputs.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name for the metric. If not provided, uses the function name. | `None` |
| `allowed_values` | `List[str]` | List of allowed categorical values for the metric output. Default is ["pass", "fail"]. | `None` |
| `**metric_params` | `Any` | Additional parameters to pass to the metric initialization. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], DiscreteMetricProtocol]` | A decorator that transforms a function into a DiscreteMetric instance. |

Examples:

```
>>> from ragas.metrics import discrete_metric
>>>
>>> @discrete_metric(name="sentiment", allowed_values=["positive", "neutral", "negative"])
>>> def sentiment_analysis(user_input: str, response: str) -> str:
...     '''Analyze sentiment of the response.'''
...     if "great" in response.lower() or "good" in response.lower():
...         return "positive"
...     elif "bad" in response.lower() or "poor" in response.lower():
...         return "negative"
...     return "neutral"
>>>
>>> result = sentiment_analysis(
...     user_input="How was your day?",
...     response="It was great!"
... )
>>> print(result.value)  # "positive"
```

Source code in `src/ragas/metrics/discrete.py`

|  |  |
| --- | --- |
| ``` 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 ``` | ``` def discrete_metric(     *,     name: t.Optional[str] = None,     allowed_values: t.Optional[t.List[str]] = None,     **metric_params: t.Any, ) -> t.Callable[[t.Callable[..., t.Any]], DiscreteMetricProtocol]:     """     Decorator for creating discrete/categorical metrics.      This decorator transforms a regular function into a DiscreteMetric instance     that can be used for evaluation with predefined categorical outputs.      Parameters     ----------     name : str, optional         Name for the metric. If not provided, uses the function name.     allowed_values : List[str], optional         List of allowed categorical values for the metric output.         Default is ["pass", "fail"].     **metric_params : Any         Additional parameters to pass to the metric initialization.      Returns     -------     Callable[[Callable[..., Any]], DiscreteMetricProtocol]         A decorator that transforms a function into a DiscreteMetric instance.      Examples     --------     >>> from ragas.metrics import discrete_metric     >>>     >>> @discrete_metric(name="sentiment", allowed_values=["positive", "neutral", "negative"])     >>> def sentiment_analysis(user_input: str, response: str) -> str:     ...     '''Analyze sentiment of the response.'''     ...     if "great" in response.lower() or "good" in response.lower():     ...         return "positive"     ...     elif "bad" in response.lower() or "poor" in response.lower():     ...         return "negative"     ...     return "neutral"     >>>     >>> result = sentiment_analysis(     ...     user_input="How was your day?",     ...     response="It was great!"     ... )     >>> print(result.value)  # "positive"     """     if allowed_values is None:         allowed_values = ["pass", "fail"]      decorator_factory = create_metric_decorator()     return decorator_factory(name=name, allowed_values=allowed_values, **metric_params)  # type: ignore[return-value] ``` |

## numeric\_metric

```
numeric_metric(*, name: Optional[str] = None, allowed_values: Optional[Union[Tuple[float, float], range]] = None, **metric_params: Any) -> Callable[[Callable[..., Any]], NumericMetricProtocol]
```

Decorator for creating numeric/continuous metrics.

This decorator transforms a regular function into a NumericMetric instance
that outputs continuous values within a specified range.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name for the metric. If not provided, uses the function name. | `None` |
| `allowed_values` | `Union[Tuple[float, float], range]` | The valid range for metric outputs as (min, max) tuple or range object. Default is (0.0, 1.0). | `None` |
| `**metric_params` | `Any` | Additional parameters to pass to the metric initialization. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], NumericMetricProtocol]` | A decorator that transforms a function into a NumericMetric instance. |

Examples:

```
>>> from ragas.metrics import numeric_metric
>>>
>>> @numeric_metric(name="relevance_score", allowed_values=(0.0, 1.0))
>>> def calculate_relevance(user_input: str, response: str) -> float:
...     '''Calculate relevance score between 0 and 1.'''
...     # Simple word overlap example
...     user_words = set(user_input.lower().split())
...     response_words = set(response.lower().split())
...     if not user_words:
...         return 0.0
...     overlap = len(user_words & response_words)
...     return overlap / len(user_words)
>>>
>>> result = calculate_relevance(
...     user_input="What is Python?",
...     response="Python is a programming language"
... )
>>> print(result.value)  # Numeric score between 0.0 and 1.0
```

Source code in `src/ragas/metrics/numeric.py`

|  |  |
| --- | --- |
| ``` 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 ``` | ``` def numeric_metric(     *,     name: t.Optional[str] = None,     allowed_values: t.Optional[t.Union[t.Tuple[float, float], range]] = None,     **metric_params: t.Any, ) -> t.Callable[[t.Callable[..., t.Any]], NumericMetricProtocol]:     """     Decorator for creating numeric/continuous metrics.      This decorator transforms a regular function into a NumericMetric instance     that outputs continuous values within a specified range.      Parameters     ----------     name : str, optional         Name for the metric. If not provided, uses the function name.     allowed_values : Union[Tuple[float, float], range], optional         The valid range for metric outputs as (min, max) tuple or range object.         Default is (0.0, 1.0).     **metric_params : Any         Additional parameters to pass to the metric initialization.      Returns     -------     Callable[[Callable[..., Any]], NumericMetricProtocol]         A decorator that transforms a function into a NumericMetric instance.      Examples     --------     >>> from ragas.metrics import numeric_metric     >>>     >>> @numeric_metric(name="relevance_score", allowed_values=(0.0, 1.0))     >>> def calculate_relevance(user_input: str, response: str) -> float:     ...     '''Calculate relevance score between 0 and 1.'''     ...     # Simple word overlap example     ...     user_words = set(user_input.lower().split())     ...     response_words = set(response.lower().split())     ...     if not user_words:     ...         return 0.0     ...     overlap = len(user_words & response_words)     ...     return overlap / len(user_words)     >>>     >>> result = calculate_relevance(     ...     user_input="What is Python?",     ...     response="Python is a programming language"     ... )     >>> print(result.value)  # Numeric score between 0.0 and 1.0     """     if allowed_values is None:         allowed_values = (0.0, 1.0)      decorator_factory = create_metric_decorator()     return decorator_factory(name=name, allowed_values=allowed_values, **metric_params)  # type: ignore[return-value] ``` |

## ranking\_metric

```
ranking_metric(*, name: Optional[str] = None, allowed_values: Optional[int] = None, **metric_params: Any) -> Callable[[Callable[..., Any]], RankingMetricProtocol]
```

Decorator for creating ranking/ordering metrics.

This decorator transforms a regular function into a RankingMetric instance
that outputs ordered lists of items.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | Name for the metric. If not provided, uses the function name. | `None` |
| `allowed_values` | `int` | Expected number of items in the ranking list. Default is 2. | `None` |
| `**metric_params` | `Any` | Additional parameters to pass to the metric initialization. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `Callable[[Callable[..., Any]], RankingMetricProtocol]` | A decorator that transforms a function into a RankingMetric instance. |

Examples:

```
>>> from ragas.metrics import ranking_metric
>>>
>>> @ranking_metric(name="priority_ranker", allowed_values=3)
>>> def rank_by_urgency(user_input: str, responses: list) -> list:
...     '''Rank responses by urgency keywords.'''
...     urgency_keywords = ["urgent", "asap", "critical"]
...     scored = []
...     for resp in responses:
...         score = sum(kw in resp.lower() for kw in urgency_keywords)
...         scored.append((score, resp))
...     # Sort by score descending and return top items
...     ranked = sorted(scored, key=lambda x: x[0], reverse=True)
...     return [item[1] for item in ranked[:3]]
>>>
>>> result = rank_by_urgency(
...     user_input="What should I do first?",
...     responses=["This is urgent", "Take your time", "Critical issue!"]
... )
>>> print(result.value)  # Ranked list of responses
```

Source code in `src/ragas/metrics/ranking.py`

|  |  |
| --- | --- |
| ``` 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 ``` | ``` def ranking_metric(     *,     name: t.Optional[str] = None,     allowed_values: t.Optional[int] = None,     **metric_params: t.Any, ) -> t.Callable[[t.Callable[..., t.Any]], RankingMetricProtocol]:     """     Decorator for creating ranking/ordering metrics.      This decorator transforms a regular function into a RankingMetric instance     that outputs ordered lists of items.      Parameters     ----------     name : str, optional         Name for the metric. If not provided, uses the function name.     allowed_values : int, optional         Expected number of items in the ranking list. Default is 2.     **metric_params : Any         Additional parameters to pass to the metric initialization.      Returns     -------     Callable[[Callable[..., Any]], RankingMetricProtocol]         A decorator that transforms a function into a RankingMetric instance.      Examples     --------     >>> from ragas.metrics import ranking_metric     >>>     >>> @ranking_metric(name="priority_ranker", allowed_values=3)     >>> def rank_by_urgency(user_input: str, responses: list) -> list:     ...     '''Rank responses by urgency keywords.'''     ...     urgency_keywords = ["urgent", "asap", "critical"]     ...     scored = []     ...     for resp in responses:     ...         score = sum(kw in resp.lower() for kw in urgency_keywords)     ...         scored.append((score, resp))     ...     # Sort by score descending and return top items     ...     ranked = sorted(scored, key=lambda x: x[0], reverse=True)     ...     return [item[1] for item in ranked[:3]]     >>>     >>> result = rank_by_urgency(     ...     user_input="What should I do first?",     ...     responses=["This is urgent", "Take your time", "Critical issue!"]     ... )     >>> print(result.value)  # Ranked list of responses     """     if allowed_values is None:         allowed_values = 2      decorator_factory = create_metric_decorator()     return decorator_factory(name=name, allowed_values=allowed_values, **metric_params)  # type: ignore[return-value] ``` |

November 28, 2025




November 28, 2025

Back to top