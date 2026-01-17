Schemas - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.dataset_schema)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Schemas

## BaseSample

Bases: `BaseModel`

Base class for evaluation samples.

### to\_dict

```
to_dict() -> Dict
```

Get the dictionary representation of the sample without attributes that are None.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 34 35 36 37 38 ``` | ``` def to_dict(self) -> t.Dict:     """     Get the dictionary representation of the sample without attributes that are None.     """     return self.model_dump(exclude_none=True) ``` |

### get\_features

```
get_features() -> List[str]
```

Get the features of the sample that are not None.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 40 41 42 43 44 ``` | ``` def get_features(self) -> t.List[str]:     """     Get the features of the sample that are not None.     """     return list(self.to_dict().keys()) ``` |

### to\_string

```
to_string() -> str
```

Get the string representation of the sample.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 46 47 48 49 50 51 ``` | ``` def to_string(self) -> str:     """     Get the string representation of the sample.     """     sample_dict = self.to_dict()     return "".join(f"\n{key}:\n\t{val}\n" for key, val in sample_dict.items()) ``` |

## SingleTurnSample

Bases: `BaseSample`

Represents evaluation samples for single-turn interactions.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `user_input` | `Optional[str]` | The input query from the user. |
| `retrieved_contexts` | `Optional[List[str]]` | List of contexts retrieved for the query. |
| `reference_contexts` | `Optional[List[str]]` | List of reference contexts for the query. |
| `retrieved_context_ids` | `Optional[List[Union[str, int]]]` | List of IDs for retrieved contexts. |
| `reference_context_ids` | `Optional[List[Union[str, int]]]` | List of IDs for reference contexts. |
| `response` | `Optional[str]` | The generated response for the query. |
| `multi_responses` | `Optional[List[str]]` | List of multiple responses generated for the query. |
| `reference` | `Optional[str]` | The reference answer for the query. |
| `rubric` | `Optional[Dict[str, str]]` | Evaluation rubric for the sample. |
| `persona_name` | `Optional[str]` | Name of the persona used in query generation. |
| `query_style` | `Optional[str]` | Style of the generated query (e.g., formal, casual). |
| `query_length` | `Optional[str]` | Length category of the query (e.g., short, medium, long). |

## MultiTurnSample

Bases: `BaseSample`

Represents evaluation samples for multi-turn interactions.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `user_input` | `List[Union[HumanMessage, AIMessage, ToolMessage]]` | A list of messages representing the conversation turns. |
| `reference` | `(Optional[str], optional)` | The reference answer or expected outcome for the conversation. |
| `reference_tool_calls` | `(Optional[List[ToolCall]], optional)` | A list of expected tool calls for the conversation. |
| `rubrics` | `(Optional[Dict[str, str]], optional)` | Evaluation rubrics for the conversation. |
| `reference_topics` | `(Optional[List[str]], optional)` | A list of reference topics for the conversation. |

### validate\_user\_input `classmethod`

```
validate_user_input(messages: List[Union[HumanMessage, AIMessage, ToolMessage]]) -> List[Union[HumanMessage, AIMessage, ToolMessage]]
```

Validates the user input messages.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 ``` | ``` @field_validator("user_input") @classmethod def validate_user_input(     cls,     messages: t.List[t.Union[HumanMessage, AIMessage, ToolMessage]], ) -> t.List[t.Union[HumanMessage, AIMessage, ToolMessage]]:     """Validates the user input messages."""     if not all(         isinstance(m, (HumanMessage, AIMessage, ToolMessage)) for m in messages     ):         raise ValueError(             "All inputs must be instances of HumanMessage, AIMessage, or ToolMessage."         )      has_seen_ai_message = False      for i, m in enumerate(messages):         if isinstance(m, AIMessage):             has_seen_ai_message = True          elif isinstance(m, ToolMessage):             # Rule 1: ToolMessage must be preceded by an AIMessage somewhere in the conversation             if not has_seen_ai_message:                 raise ValueError(                     "ToolMessage must be preceded by an AIMessage somewhere in the conversation."                 )              # Rule 2: ToolMessage must follow an AIMessage or another ToolMessage             if i > 0:                 prev_message = messages[i - 1]                  if isinstance(prev_message, AIMessage):                     # Rule 3: If following AIMessage, that message must have tool_calls                     if not prev_message.tool_calls:                         raise ValueError(                             "ToolMessage must follow an AIMessage where tools were called."                         )                 elif not isinstance(prev_message, ToolMessage):                     # Not following AIMessage or ToolMessage                     raise ValueError(                         "ToolMessage must follow an AIMessage or another ToolMessage."                     )      return messages ``` |

### to\_messages

```
to_messages()
```

Converts the user input messages to a list of dictionaries.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 169 170 171 ``` | ``` def to_messages(self):     """Converts the user input messages to a list of dictionaries."""     return [m.model_dump() for m in self.user_input] ``` |

### pretty\_repr

```
pretty_repr()
```

Returns a pretty string representation of the conversation.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 173 174 175 176 177 178 179 ``` | ``` def pretty_repr(self):     """Returns a pretty string representation of the conversation."""     lines = []     for m in self.user_input:         lines.append(m.pretty_repr())      return "\n".join(lines) ``` |

## RagasDataset `dataclass`

```
RagasDataset(samples: List[Sample])
```

Bases: `ABC`, `Generic[Sample]`

### to\_list `abstractmethod`

```
to_list() -> List[Dict]
```

Converts the samples to a list of dictionaries.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 193 194 195 196 ``` | ``` @abstractmethod def to_list(self) -> t.List[t.Dict]:     """Converts the samples to a list of dictionaries."""     pass ``` |

### from\_list `abstractmethod` `classmethod`

```
from_list(data: List[Dict]) -> T
```

Creates an RagasDataset from a list of dictionaries.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 198 199 200 201 202 ``` | ``` @classmethod @abstractmethod def from_list(cls: t.Type[T], data: t.List[t.Dict]) -> T:     """Creates an RagasDataset from a list of dictionaries."""     pass ``` |

### validate\_samples

```
validate_samples(samples: List[Sample]) -> List[Sample]
```

Validates that all samples are of the same type.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 204 205 206 207 208 209 210 211 212 213 214 215 216 ``` | ``` def validate_samples(self, samples: t.List[Sample]) -> t.List[Sample]:     """Validates that all samples are of the same type."""     if len(samples) == 0:         return samples      first_sample_type = type(samples[0])     for i, sample in enumerate(samples):         if not isinstance(sample, first_sample_type):             raise ValueError(                 f"Sample at index {i} is of type {type(sample)}, expected {first_sample_type}"             )      return samples ``` |

### get\_sample\_type

```
get_sample_type() -> Type[Sample]
```

Returns the type of the samples in the dataset.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 218 219 220 ``` | ``` def get_sample_type(self) -> t.Type[Sample]:     """Returns the type of the samples in the dataset."""     return type(self.samples[0]) ``` |

### to\_hf\_dataset

```
to_hf_dataset() -> Dataset
```

Converts the dataset to a Hugging Face Dataset.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 222 223 224 225 226 227 228 229 230 231 ``` | ``` def to_hf_dataset(self) -> HFDataset:     """Converts the dataset to a Hugging Face Dataset."""     try:         from datasets import Dataset as HFDataset     except ImportError:         raise ImportError(             "datasets is not installed. Please install it to use this function."         )      return HFDataset.from_list(self.to_list()) ``` |

### from\_hf\_dataset `classmethod`

```
from_hf_dataset(dataset: Dataset) -> T
```

Creates an EvaluationDataset from a Hugging Face Dataset.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 233 234 235 236 ``` | ``` @classmethod def from_hf_dataset(cls: t.Type[T], dataset: HFDataset) -> T:     """Creates an EvaluationDataset from a Hugging Face Dataset."""     return cls.from_list(dataset.to_list()) ``` |

### to\_pandas

```
to_pandas() -> DataFrame
```

Converts the dataset to a pandas DataFrame.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 238 239 240 241 242 243 244 245 246 247 248 ``` | ``` def to_pandas(self) -> PandasDataframe:     """Converts the dataset to a pandas DataFrame."""     try:         import pandas as pd     except ImportError:         raise ImportError(             "pandas is not installed. Please install it to use this function."         )      data = self.to_list()     return pd.DataFrame(data) ``` |

### from\_pandas `classmethod`

```
from_pandas(dataframe: DataFrame)
```

Creates an EvaluationDataset from a pandas DataFrame.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 250 251 252 253 ``` | ``` @classmethod def from_pandas(cls, dataframe: PandasDataframe):     """Creates an EvaluationDataset from a pandas DataFrame."""     return cls.from_list(dataframe.to_dict(orient="records")) ``` |

### features

```
features()
```

Returns the features of the samples.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 255 256 257 ``` | ``` def features(self):     """Returns the features of the samples."""     return self.samples[0].get_features() ``` |

### from\_dict `classmethod`

```
from_dict(mapping: Dict) -> T
```

Creates an EvaluationDataset from a dictionary.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 259 260 261 262 263 264 265 266 267 268 269 270 ``` | ``` @classmethod def from_dict(cls: t.Type[T], mapping: t.Dict) -> T:     """Creates an EvaluationDataset from a dictionary."""     samples = []     if all(         "user_input" in item and isinstance(mapping[0]["user_input"], list)         for item in mapping     ):         samples.extend(MultiTurnSample(**sample) for sample in mapping)     else:         samples.extend(SingleTurnSample(**sample) for sample in mapping)     return cls(samples=samples) ``` |

### to\_csv

```
to_csv(path: Union[str, Path])
```

Converts the dataset to a CSV file.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 ``` | ``` def to_csv(self, path: t.Union[str, Path]):     """Converts the dataset to a CSV file."""     import csv      data = self.to_list()     if not data:         return      fieldnames = data[0].keys()      with open(path, "w", newline="") as csvfile:         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)         writer.writeheader()         for row in data:             writer.writerow(row) ``` |

### to\_jsonl

```
to_jsonl(path: Union[str, Path])
```

Converts the dataset to a JSONL file.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 288 289 290 291 292 ``` | ``` def to_jsonl(self, path: t.Union[str, Path]):     """Converts the dataset to a JSONL file."""     with open(path, "w") as jsonlfile:         for sample in self.to_list():             jsonlfile.write(json.dumps(sample, ensure_ascii=False) + "\n") ``` |

### from\_jsonl `classmethod`

```
from_jsonl(path: Union[str, Path]) -> T
```

Creates an EvaluationDataset from a JSONL file.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 294 295 296 297 298 299 ``` | ``` @classmethod def from_jsonl(cls: t.Type[T], path: t.Union[str, Path]) -> T:     """Creates an EvaluationDataset from a JSONL file."""     with open(path, "r") as jsonlfile:         data = [json.loads(line) for line in jsonlfile]     return cls.from_list(data) ``` |

## EvaluationDataset `dataclass`

```
EvaluationDataset(samples: List[Sample], backend: Optional[str] = None, name: Optional[str] = None)
```

Bases: `RagasDataset[SingleTurnSampleOrMultiTurnSample]`

Represents a dataset of evaluation samples.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `samples` | `List[BaseSample]` | A list of evaluation samples. |
| `backend` | `Optional[str]` | The backend to use for storing the dataset (e.g., "local/csv"). Default is None. |
| `name` | `Optional[str]` | The name of the dataset. Default is None. |

Methods:

| Name | Description |
| --- | --- |
| `validate_samples` | Validates that all samples are of the same type. |
| `get_sample_type` | Returns the type of the samples in the dataset. |
| `to_hf_dataset` | Converts the dataset to a Hugging Face Dataset. |
| `to_pandas` | Converts the dataset to a pandas DataFrame. |
| `features` | Returns the features of the samples. |
| `from_list` | Creates an EvaluationDataset from a list of dictionaries. |
| `from_dict` | Creates an EvaluationDataset from a dictionary. |
| `to_csv` | Converts the dataset to a CSV file. |
| `to_jsonl` | Converts the dataset to a JSONL file. |
| `from_jsonl` | Creates an EvaluationDataset from a JSONL file. |

## EvaluationResult `dataclass`

```
EvaluationResult(scores: List[Dict[str, Any]], dataset: EvaluationDataset, binary_columns: List[str] = list(), cost_cb: Optional[CostCallbackHandler] = None, traces: List[Dict[str, Any]] = list(), ragas_traces: Dict[str, ChainRun] = dict(), run_id: Optional[UUID] = None)
```

A class to store and process the results of the evaluation.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `scores` | `Dataset` | The dataset containing the scores of the evaluation. |
| `dataset` | `(Dataset, optional)` | The original dataset used for the evaluation. Default is None. |
| `binary_columns` | `list of str, optional` | List of columns that are binary metrics. Default is an empty list. |
| `cost_cb` | `(CostCallbackHandler, optional)` | The callback handler for cost computation. Default is None. |

### to\_pandas

```
to_pandas(batch_size: int | None = None, batched: bool = False)
```

Convert the result to a pandas DataFrame.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `batch_size` | `int` | The batch size for conversion. Default is None. | `None` |
| `batched` | `bool` | Whether to convert in batches. Default is False. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `DataFrame` | The result as a pandas DataFrame. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the dataset is not provided. |

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 ``` | ``` def to_pandas(self, batch_size: int | None = None, batched: bool = False):     """     Convert the result to a pandas DataFrame.      Parameters     ----------     batch_size : int, optional         The batch size for conversion. Default is None.     batched : bool, optional         Whether to convert in batches. Default is False.      Returns     -------     pandas.DataFrame         The result as a pandas DataFrame.      Raises     ------     ValueError         If the dataset is not provided.     """     try:         import pandas as pd     except ImportError:         raise ImportError(             "pandas is not installed. Please install it to use this function."         )      if self.dataset is None:         raise ValueError("dataset is not provided for the results class")     assert len(self.scores) == len(self.dataset)     # convert both to pandas dataframes and concatenate     scores_df = pd.DataFrame(self.scores)     dataset_df = self.dataset.to_pandas()     return pd.concat([dataset_df, scores_df], axis=1) ``` |

### total\_tokens

```
total_tokens() -> Union[List[TokenUsage], TokenUsage]
```

Compute the total tokens used in the evaluation.

Returns:

| Type | Description |
| --- | --- |
| `list of TokenUsage or TokenUsage` | The total tokens used. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the cost callback handler is not provided. |

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 ``` | ``` def total_tokens(self) -> t.Union[t.List[TokenUsage], TokenUsage]:     """     Compute the total tokens used in the evaluation.      Returns     -------     list of TokenUsage or TokenUsage         The total tokens used.      Raises     ------     ValueError         If the cost callback handler is not provided.     """     if self.cost_cb is None:         raise ValueError(             "The evaluate() run was not configured for computing cost. Please provide a token_usage_parser function to evaluate() to compute cost."         )     return self.cost_cb.total_tokens() ``` |

### total\_cost

```
total_cost(cost_per_input_token: Optional[float] = None, cost_per_output_token: Optional[float] = None, per_model_costs: Dict[str, Tuple[float, float]] = {}) -> float
```

Compute the total cost of the evaluation.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `cost_per_input_token` | `float` | The cost per input token. Default is None. | `None` |
| `cost_per_output_token` | `float` | The cost per output token. Default is None. | `None` |
| `per_model_costs` | `dict of str to tuple of float` | The per model costs. Default is an empty dictionary. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `float` | The total cost of the evaluation. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the cost callback handler is not provided. |

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 ``` | ``` def total_cost(     self,     cost_per_input_token: t.Optional[float] = None,     cost_per_output_token: t.Optional[float] = None,     per_model_costs: t.Dict[str, t.Tuple[float, float]] = {}, ) -> float:     """     Compute the total cost of the evaluation.      Parameters     ----------     cost_per_input_token : float, optional         The cost per input token. Default is None.     cost_per_output_token : float, optional         The cost per output token. Default is None.     per_model_costs : dict of str to tuple of float, optional         The per model costs. Default is an empty dictionary.      Returns     -------     float         The total cost of the evaluation.      Raises     ------     ValueError         If the cost callback handler is not provided.     """     if self.cost_cb is None:         raise ValueError(             "The evaluate() run was not configured for computing cost. Please provide a token_usage_parser function to evaluate() to compute cost."         )     return self.cost_cb.total_cost(         cost_per_input_token, cost_per_output_token, per_model_costs     ) ``` |

## MetricAnnotation

Bases: `BaseModel`

### from\_json `classmethod`

```
from_json(path: str, metric_name: Optional[str]) -> 'MetricAnnotation'
```

Load annotations from a JSON file

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 611 612 613 614 615 ``` | ``` @classmethod def from_json(cls, path: str, metric_name: t.Optional[str]) -> "MetricAnnotation":     """Load annotations from a JSON file"""     dataset = json.load(open(path))     return cls._process_dataset(dataset, metric_name) ``` |

## SingleMetricAnnotation

Bases: `BaseModel`

### train\_test\_split

```
train_test_split(test_size: float = 0.2, seed: int = 42, stratify: Optional[List[Any]] = None) -> Tuple['SingleMetricAnnotation', 'SingleMetricAnnotation']
```

Split the dataset into training and testing sets.

Parameters:
test\_size (float): The proportion of the dataset to include in the test split.
seed (int): Random seed for reproducibility.
stratify (list): The column values to stratify the split on.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 ``` | ``` def train_test_split(     self,     test_size: float = 0.2,     seed: int = 42,     stratify: t.Optional[t.List[t.Any]] = None, ) -> t.Tuple["SingleMetricAnnotation", "SingleMetricAnnotation"]:     """     Split the dataset into training and testing sets.      Parameters:         test_size (float): The proportion of the dataset to include in the test split.         seed (int): Random seed for reproducibility.         stratify (list): The column values to stratify the split on.     """     raise NotImplementedError ``` |

### sample

```
sample(n: int, stratify_key: Optional[str] = None) -> 'SingleMetricAnnotation'
```

Create a subset of the dataset.

Parameters:
n (int): The number of samples to include in the subset.
stratify\_key (str): The column to stratify the subset on.

Returns:
SingleMetricAnnotation: A subset of the dataset with `n` samples.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 ``` | ``` def sample(     self, n: int, stratify_key: t.Optional[str] = None ) -> "SingleMetricAnnotation":     """     Create a subset of the dataset.      Parameters:         n (int): The number of samples to include in the subset.         stratify_key (str): The column to stratify the subset on.      Returns:         SingleMetricAnnotation: A subset of the dataset with `n` samples.     """     if n > len(self.samples):         raise ValueError(             "Requested sample size exceeds the number of available samples."         )      if stratify_key is None:         # Simple random sampling         sampled_indices = random.sample(range(len(self.samples)), n)         sampled_samples = [self.samples[i] for i in sampled_indices]     else:         # Stratified sampling         class_groups = defaultdict(list)         for idx, sample in enumerate(self.samples):             key = sample[stratify_key]             class_groups[key].append(idx)          # Determine the proportion of samples to take from each class         total_samples = sum(len(indices) for indices in class_groups.values())         proportions = {             cls: len(indices) / total_samples             for cls, indices in class_groups.items()         }          sampled_indices = []         for cls, indices in class_groups.items():             cls_sample_count = int(np.round(proportions[cls] * n))             cls_sample_count = min(                 cls_sample_count, len(indices)             )  # Don't oversample             sampled_indices.extend(random.sample(indices, cls_sample_count))          # Handle any rounding discrepancies to ensure exactly `n` samples         while len(sampled_indices) < n:             remaining_indices = set(range(len(self.samples))) - set(sampled_indices)             if not remaining_indices:                 break             sampled_indices.append(random.choice(list(remaining_indices)))          sampled_samples = [self.samples[i] for i in sampled_indices]      return SingleMetricAnnotation(name=self.name, samples=sampled_samples) ``` |

### batch

```
batch(batch_size: int, drop_last_batch: bool = False)
```

Create a batch iterator.

Parameters:
batch\_size (int): The number of samples in each batch.
stratify (str): The column to stratify the batches on.
drop\_last\_batch (bool): Whether to drop the last batch if it is smaller than the specified batch size.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 ``` | ``` def batch(     self,     batch_size: int,     drop_last_batch: bool = False, ):     """     Create a batch iterator.      Parameters:         batch_size (int): The number of samples in each batch.         stratify (str): The column to stratify the batches on.         drop_last_batch (bool): Whether to drop the last batch if it is smaller than the specified batch size.     """      samples = self.samples[:]     random.shuffle(samples)      all_batches = [         samples[i : i + batch_size]         for i in range(0, len(samples), batch_size)         if len(samples[i : i + batch_size]) == batch_size or not drop_last_batch     ]      return all_batches ``` |

### stratified\_batches

```
stratified_batches(batch_size: int, stratify_key: str, drop_last_batch: bool = False, replace: bool = False) -> List[List[SampleAnnotation]]
```

Create stratified batches based on a specified key, ensuring proportional representation.

Parameters:
batch\_size (int): Number of samples per batch.
stratify\_key (str): Key in `metric_input` used for stratification (e.g., class labels).
drop\_last\_batch (bool): If True, drops the last batch if it has fewer samples than `batch_size`.
replace (bool): If True, allows reusing samples from the same class to fill a batch if necessary.

Returns:
List[List[SampleAnnotation]]: A list of stratified batches, each batch being a list of SampleAnnotation objects.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 ``` | ``` def stratified_batches(     self,     batch_size: int,     stratify_key: str,     drop_last_batch: bool = False,     replace: bool = False, ) -> t.List[t.List[SampleAnnotation]]:     """     Create stratified batches based on a specified key, ensuring proportional representation.      Parameters:         batch_size (int): Number of samples per batch.         stratify_key (str): Key in `metric_input` used for stratification (e.g., class labels).         drop_last_batch (bool): If True, drops the last batch if it has fewer samples than `batch_size`.         replace (bool): If True, allows reusing samples from the same class to fill a batch if necessary.      Returns:         List[List[SampleAnnotation]]: A list of stratified batches, each batch being a list of SampleAnnotation objects.     """     # Group samples based on the stratification key     class_groups = defaultdict(list)     for sample in self.samples:         key = sample[stratify_key]         class_groups[key].append(sample)      # Shuffle each class group for randomness     for group in class_groups.values():         random.shuffle(group)      # Determine the number of batches required     total_samples = len(self.samples)     num_batches = (         np.ceil(total_samples / batch_size).astype(int)         if drop_last_batch         else np.floor(total_samples / batch_size).astype(int)     )     samples_per_class_per_batch = {         cls: max(1, len(samples) // num_batches)         for cls, samples in class_groups.items()     }      # Create stratified batches     all_batches = []     while len(all_batches) < num_batches:         batch = []         for cls, samples in list(class_groups.items()):             # Determine the number of samples to take from this class             count = min(                 samples_per_class_per_batch[cls],                 len(samples),                 batch_size - len(batch),             )             if count > 0:                 # Add samples from the current class                 batch.extend(samples[:count])                 class_groups[cls] = samples[count:]  # Remove used samples             elif replace and len(batch) < batch_size:                 # Reuse samples if `replace` is True                 batch.extend(random.choices(samples, k=batch_size - len(batch)))          # Shuffle the batch to mix classes         random.shuffle(batch)         if len(batch) == batch_size or not drop_last_batch:             all_batches.append(batch)      return all_batches ``` |

### get\_prompt\_annotations

```
get_prompt_annotations() -> Dict[str, List[PromptAnnotation]]
```

Get all the prompt annotations for each prompt as a list.

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 828 829 830 831 832 833 834 835 836 837 ``` | ``` def get_prompt_annotations(self) -> t.Dict[str, t.List[PromptAnnotation]]:     """     Get all the prompt annotations for each prompt as a list.     """     prompt_annotations = defaultdict(list)     for sample in self.samples:         if sample.is_accepted:             for prompt_name, prompt_annotation in sample.prompts.items():                 prompt_annotations[prompt_name].append(prompt_annotation)     return prompt_annotations ``` |

## Message

Bases: `BaseModel`

Represents a generic message.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `content` | `str` | The content of the message. |
| `metadata` | `(Optional[Dict[str, Any]], optional)` | Additional metadata associated with the message. |

## ToolCall

Bases: `BaseModel`

Represents a tool call with a name and arguments.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `name` | `str` | The name of the tool being called. | *required* |
| `args` | `Dict[str, Any]` | A dictionary of arguments for the tool call, where keys are argument names and values can be strings, integers, or floats. | *required* |

## HumanMessage

Bases: `Message`

Represents a message from a human user.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `type` | `Literal[human]` | The type of the message, always set to "human". |

Methods:

| Name | Description |
| --- | --- |
| `pretty_repr` | Returns a formatted string representation of the human message. |

### pretty\_repr

```
pretty_repr()
```

Returns a formatted string representation of the human message.

Source code in `src/ragas/messages.py`

|  |  |
| --- | --- |
| ``` 56 57 58 ``` | ``` def pretty_repr(self):     """Returns a formatted string representation of the human message."""     return f"Human: {self.content}" ``` |

## ToolMessage

Bases: `Message`

Represents a message from a tool.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `type` | `Literal[tool]` | The type of the message, always set to "tool". |

Methods:

| Name | Description |
| --- | --- |
| `pretty_repr` | Returns a formatted string representation of the tool message. |

### pretty\_repr

```
pretty_repr()
```

Returns a formatted string representation of the tool message.

Source code in `src/ragas/messages.py`

|  |  |
| --- | --- |
| ``` 78 79 80 ``` | ``` def pretty_repr(self):     """Returns a formatted string representation of the tool message."""     return f"ToolOutput: {self.content}" ``` |

## AIMessage

Bases: `Message`

Represents a message from an AI.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `type` | `Literal[ai]` | The type of the message, always set to "ai". |
| `tool_calls` | `Optional[List[ToolCall]]` | A list of tool calls made by the AI, if any. |
| `metadata` | `Optional[Dict[str, Any]]` | Additional metadata associated with the AI message. |

Methods:

| Name | Description |
| --- | --- |
| `dict` | Returns a dictionary representation of the AI message. |
| `pretty_repr` | Returns a formatted string representation of the AI message. |

### to\_dict

```
to_dict(**kwargs)
```

Returns a dictionary representation of the AI message.

Source code in `src/ragas/messages.py`

|  |  |
| --- | --- |
| ``` 108 109 110 111 112 113 114 115 116 117 118 119 120 ``` | ``` def to_dict(self, **kwargs):     """     Returns a dictionary representation of the AI message.     """     content = (         self.content         if self.tool_calls is None         else {             "text": self.content,             "tool_calls": [tc.dict() for tc in self.tool_calls],         }     )     return {"content": content, "type": self.type} ``` |

### pretty\_repr

```
pretty_repr()
```

Returns a formatted string representation of the AI message.

Source code in `src/ragas/messages.py`

|  |  |
| --- | --- |
| ``` 122 123 124 125 126 127 128 129 130 131 132 133 134 ``` | ``` def pretty_repr(self):     """     Returns a formatted string representation of the AI message.     """     lines = []     if self.content != "":         lines.append(f"AI: {self.content}")     if self.tool_calls is not None:         lines.append("Tools:")         for tc in self.tool_calls:             lines.append(f"  {tc.name}: {tc.args}")      return "\n".join(lines) ``` |

## ragas.evaluation.EvaluationResult `dataclass`

```
EvaluationResult(scores: List[Dict[str, Any]], dataset: EvaluationDataset, binary_columns: List[str] = list(), cost_cb: Optional[CostCallbackHandler] = None, traces: List[Dict[str, Any]] = list(), ragas_traces: Dict[str, ChainRun] = dict(), run_id: Optional[UUID] = None)
```

A class to store and process the results of the evaluation.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `scores` | `Dataset` | The dataset containing the scores of the evaluation. |
| `dataset` | `(Dataset, optional)` | The original dataset used for the evaluation. Default is None. |
| `binary_columns` | `list of str, optional` | List of columns that are binary metrics. Default is an empty list. |
| `cost_cb` | `(CostCallbackHandler, optional)` | The callback handler for cost computation. Default is None. |

### to\_pandas

```
to_pandas(batch_size: int | None = None, batched: bool = False)
```

Convert the result to a pandas DataFrame.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `batch_size` | `int` | The batch size for conversion. Default is None. | `None` |
| `batched` | `bool` | Whether to convert in batches. Default is False. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `DataFrame` | The result as a pandas DataFrame. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the dataset is not provided. |

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 ``` | ``` def to_pandas(self, batch_size: int | None = None, batched: bool = False):     """     Convert the result to a pandas DataFrame.      Parameters     ----------     batch_size : int, optional         The batch size for conversion. Default is None.     batched : bool, optional         Whether to convert in batches. Default is False.      Returns     -------     pandas.DataFrame         The result as a pandas DataFrame.      Raises     ------     ValueError         If the dataset is not provided.     """     try:         import pandas as pd     except ImportError:         raise ImportError(             "pandas is not installed. Please install it to use this function."         )      if self.dataset is None:         raise ValueError("dataset is not provided for the results class")     assert len(self.scores) == len(self.dataset)     # convert both to pandas dataframes and concatenate     scores_df = pd.DataFrame(self.scores)     dataset_df = self.dataset.to_pandas()     return pd.concat([dataset_df, scores_df], axis=1) ``` |

### total\_tokens

```
total_tokens() -> Union[List[TokenUsage], TokenUsage]
```

Compute the total tokens used in the evaluation.

Returns:

| Type | Description |
| --- | --- |
| `list of TokenUsage or TokenUsage` | The total tokens used. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the cost callback handler is not provided. |

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 ``` | ``` def total_tokens(self) -> t.Union[t.List[TokenUsage], TokenUsage]:     """     Compute the total tokens used in the evaluation.      Returns     -------     list of TokenUsage or TokenUsage         The total tokens used.      Raises     ------     ValueError         If the cost callback handler is not provided.     """     if self.cost_cb is None:         raise ValueError(             "The evaluate() run was not configured for computing cost. Please provide a token_usage_parser function to evaluate() to compute cost."         )     return self.cost_cb.total_tokens() ``` |

### total\_cost

```
total_cost(cost_per_input_token: Optional[float] = None, cost_per_output_token: Optional[float] = None, per_model_costs: Dict[str, Tuple[float, float]] = {}) -> float
```

Compute the total cost of the evaluation.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `cost_per_input_token` | `float` | The cost per input token. Default is None. | `None` |
| `cost_per_output_token` | `float` | The cost per output token. Default is None. | `None` |
| `per_model_costs` | `dict of str to tuple of float` | The per model costs. Default is an empty dictionary. | `{}` |

Returns:

| Type | Description |
| --- | --- |
| `float` | The total cost of the evaluation. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the cost callback handler is not provided. |

Source code in `src/ragas/dataset_schema.py`

|  |  |
| --- | --- |
| ``` 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 ``` | ``` def total_cost(     self,     cost_per_input_token: t.Optional[float] = None,     cost_per_output_token: t.Optional[float] = None,     per_model_costs: t.Dict[str, t.Tuple[float, float]] = {}, ) -> float:     """     Compute the total cost of the evaluation.      Parameters     ----------     cost_per_input_token : float, optional         The cost per input token. Default is None.     cost_per_output_token : float, optional         The cost per output token. Default is None.     per_model_costs : dict of str to tuple of float, optional         The per model costs. Default is an empty dictionary.      Returns     -------     float         The total cost of the evaluation.      Raises     ------     ValueError         If the cost callback handler is not provided.     """     if self.cost_cb is None:         raise ValueError(             "The evaluate() run was not configured for computing cost. Please provide a token_usage_parser function to evaluate() to compute cost."         )     return self.cost_cb.total_cost(         cost_per_input_token, cost_per_output_token, per_model_costs     ) ``` |

November 28, 2025




November 28, 2025

Back to top