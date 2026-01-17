Integrations - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.integrations.langchain)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Integrations

## ragas.integrations.langchain

### EvaluatorChain

```
EvaluatorChain(metric: Metric, **kwargs: Any)
```

Bases: `Chain`, `RunEvaluator`

Wrapper around ragas Metrics to use them with langsmith.

Source code in `src/ragas/integrations/langchain.py`

|  |  |
| --- | --- |
| ``` 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 ``` | ``` def __init__(self, metric: Metric, **kwargs: t.Any):     kwargs["metric"] = metric     super().__init__(**kwargs)     if "run_config" in kwargs:         run_config = kwargs["run_config"]     else:         run_config = RunConfig()     if isinstance(self.metric, MetricWithLLM):         llm = get_or_init(kwargs, "llm", ChatOpenAI)         t.cast(MetricWithLLM, self.metric).llm = LangchainLLMWrapper(llm)     if isinstance(self.metric, MetricWithEmbeddings):         embeddings = get_or_init(kwargs, "embeddings", OpenAIEmbeddings)         t.cast(             MetricWithEmbeddings, self.metric         ).embeddings = LangchainEmbeddingsWrapper(embeddings)     self.metric.init(run_config)      assert isinstance(self.metric, SingleTurnMetric), (         "Metric must be SingleTurnMetric"     ) ``` |

#### evaluate\_run

```
evaluate_run(run: Run, example: Optional[Example] = None) -> EvaluationResult
```

Evaluate a langsmith run

Source code in `src/ragas/integrations/langchain.py`

|  |  |
| --- | --- |
| ``` 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 ``` | ``` @t.no_type_check def evaluate_run(     self, run: Run, example: t.Optional[Example] = None ) -> EvaluationResult:     """     Evaluate a langsmith run     """     # Moved away from this implementation in LangChain evaluations;     # we can safely ignore type checking for this legacy function.     self._validate_langsmith_eval(run, example)      # this is just to suppress the type checker error     # actual check and error message is in the _validate_langsmith_eval     assert run.outputs is not None     assert example is not None     assert example.inputs is not None     assert example.outputs is not None      chain_eval = run.outputs     chain_eval["question"] = example.inputs["question"]     if "ground_truth" in get_required_columns_v1(self.metric):         if example.outputs is None or "ground_truth" not in example.outputs:             raise ValueError("expected `ground_truth` in example outputs.")         chain_eval["ground_truth"] = example.outputs["ground_truth"]     eval_output = self.invoke(chain_eval, include_run_info=True)      evaluation_result = EvaluationResult(         key=self.metric.name, score=eval_output[self.metric.name]     )     if RUN_KEY in eval_output:         evaluation_result.evaluator_info[RUN_KEY] = eval_output[RUN_KEY]     return evaluation_result ``` |

## ragas.integrations.langsmith

### upload\_dataset

```
upload_dataset(dataset: Testset, dataset_name: str, dataset_desc: str = '') -> Dataset
```

Uploads a new dataset to LangSmith, converting it from a TestDataset object to a
pandas DataFrame before upload. If a dataset with the specified name already
exists, the function raises an error.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `dataset` | `TestDataset` | The dataset to be uploaded. | *required* |
| `dataset_name` | `str` | The name for the new dataset in LangSmith. | *required* |
| `dataset_desc` | `str` | A description for the new dataset. The default is an empty string. | `''` |

Returns:

| Type | Description |
| --- | --- |
| `Dataset` | The dataset object as stored in LangSmith after upload. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If a dataset with the specified name already exists in LangSmith. |

Notes

The function attempts to read a dataset by the given name to check its existence.
If not found, it proceeds to upload the dataset after converting it to a pandas
DataFrame. This involves specifying input and output keys for the dataset being
uploaded.


Source code in `src/ragas/integrations/langsmith.py`

|  |  |
| --- | --- |
| ``` 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 ``` | ``` def upload_dataset(     dataset: Testset, dataset_name: str, dataset_desc: str = "" ) -> LangsmithDataset:     """     Uploads a new dataset to LangSmith, converting it from a TestDataset object to a     pandas DataFrame before upload. If a dataset with the specified name already     exists, the function raises an error.      Parameters     ----------     dataset : TestDataset         The dataset to be uploaded.     dataset_name : str         The name for the new dataset in LangSmith.     dataset_desc : str, optional         A description for the new dataset. The default is an empty string.      Returns     -------     LangsmithDataset         The dataset object as stored in LangSmith after upload.      Raises     ------     ValueError         If a dataset with the specified name already exists in LangSmith.      Notes     -----     The function attempts to read a dataset by the given name to check its existence.     If not found, it proceeds to upload the dataset after converting it to a pandas     DataFrame. This involves specifying input and output keys for the dataset being     uploaded.     """     client = Client()     try:         # check if dataset exists         langsmith_dataset: LangsmithDataset = client.read_dataset(             dataset_name=dataset_name         )         raise ValueError(             f"Dataset {dataset_name} already exists in langsmith. [{langsmith_dataset}]"         )     except LangSmithNotFoundError:         # if not create a new one with the generated query examples         langsmith_dataset: LangsmithDataset = client.upload_dataframe(             df=dataset.to_pandas(),             name=dataset_name,             input_keys=["question"],             output_keys=["ground_truth"],             description=dataset_desc,         )          print(             f"Created a new dataset '{langsmith_dataset.name}'. Dataset is accessible at {langsmith_dataset.url}"         )         return langsmith_dataset ``` |

### evaluate

```
evaluate(dataset_name: str, llm_or_chain_factory: Any, experiment_name: Optional[str] = None, metrics: Optional[list] = None, verbose: bool = False) -> Dict[str, Any]
```

Evaluates a language model or a chain factory on a specified dataset using
LangSmith, with the option to customize metrics and verbosity.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `dataset_name` | `str` | The name of the dataset to use for evaluation. This dataset must exist in LangSmith. | *required* |
| `llm_or_chain_factory` | `Any` | The language model or chain factory to be evaluated. This parameter is flexible and can accept a variety of objects depending on the implementation. | *required* |
| `experiment_name` | `Optional[str]` | The name of the experiment. This can be used to categorize or identify the evaluation run within LangSmith. The default is None. | `None` |
| `metrics` | `Optional[list]` | A list of custom metrics (functions or evaluators) to be used for the evaluation. If None, a default set of metrics (answer relevancy, context precision, context recall, and faithfulness) are used. The default is None. | `None` |
| `verbose` | `bool` | If True, detailed progress and results will be printed during the evaluation process. The default is False. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Dict[str, Any]` | A dictionary containing the results of the evaluation. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the specified dataset does not exist in LangSmith. |

See Also

Client.read\_dataset : Method to read an existing dataset.
Client.run\_on\_dataset : Method to run the evaluation on the specified dataset.

Examples:

```
>>> results = evaluate(
...     dataset_name="MyDataset",
...     llm_or_chain_factory=my_llm,
...     experiment_name="experiment_1_with_vanila_rag",
...     verbose=True
... )
>>> print(results)
{'evaluation_result': ...}
```

Notes

The function initializes a client to interact with LangSmith, validates the existence
of the specified dataset, prepares evaluation metrics, and runs the evaluation,
returning the results. Custom evaluation metrics can be specified, or a default set
will be used if none are provided.


Source code in `src/ragas/integrations/langsmith.py`

|  |  |
| --- | --- |
| ```  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 ``` | ``` def evaluate(     dataset_name: str,     llm_or_chain_factory: t.Any,     experiment_name: t.Optional[str] = None,     metrics: t.Optional[list] = None,     verbose: bool = False, ) -> t.Dict[str, t.Any]:     """     Evaluates a language model or a chain factory on a specified dataset using     LangSmith, with the option to customize metrics and verbosity.      Parameters     ----------     dataset_name : str         The name of the dataset to use for evaluation. This dataset must exist in         LangSmith.     llm_or_chain_factory : Any         The language model or chain factory to be evaluated. This parameter is         flexible and can accept a variety of objects depending on the implementation.     experiment_name : Optional[str], optional         The name of the experiment. This can be used to categorize or identify the         evaluation run within LangSmith. The default is None.     metrics : Optional[list], optional         A list of custom metrics (functions or evaluators) to be used for the         evaluation. If None, a default set of metrics (answer relevancy, context         precision, context recall, and faithfulness) are used.         The default is None.     verbose : bool, optional         If True, detailed progress and results will be printed during the evaluation         process.         The default is False.      Returns     -------     Dict[str, Any]         A dictionary containing the results of the evaluation.      Raises     ------     ValueError         If the specified dataset does not exist in LangSmith.      See Also     --------     Client.read_dataset : Method to read an existing dataset.     Client.run_on_dataset : Method to run the evaluation on the specified dataset.      Examples     --------     >>> results = evaluate(     ...     dataset_name="MyDataset",     ...     llm_or_chain_factory=my_llm,     ...     experiment_name="experiment_1_with_vanila_rag",     ...     verbose=True     ... )     >>> print(results)     {'evaluation_result': ...}      Notes     -----     The function initializes a client to interact with LangSmith, validates the existence     of the specified dataset, prepares evaluation metrics, and runs the evaluation,     returning the results. Custom evaluation metrics can be specified, or a default set     will be used if none are provided.     """     # init client and validate dataset     client = Client()     try:         _ = client.read_dataset(dataset_name=dataset_name)     except LangSmithNotFoundError:         raise ValueError(             f"Dataset {dataset_name} not found in langsmith, make sure it exists in langsmith"         )      # make config     if metrics is None:         from ragas.metrics._answer_relevance import answer_relevancy         from ragas.metrics._context_precision import context_precision         from ragas.metrics._context_recall import context_recall         from ragas.metrics._faithfulness import faithfulness          metrics = [answer_relevancy, context_precision, faithfulness, context_recall]      metrics = [EvaluatorChain(m) for m in metrics]     eval_config = RunEvalConfig(         custom_evaluators=metrics,     )      # run evaluation with langsmith     run = client.run_on_dataset(  # type: ignore[attr-defined]         dataset_name=dataset_name,         llm_or_chain_factory=llm_or_chain_factory,         evaluation=eval_config,         verbose=verbose,         # Any experiment metadata can be specified here         project_name=experiment_name,     )      return run ``` |

## ragas.integrations.llama\_index

### convert\_to\_ragas\_messages

```
convert_to_ragas_messages(events: List[Event]) -> List[Message]
```

Convert a sequence of LlamIndex agent events into Ragas message objects.

This function processes a list of `Event` objects (e.g., `AgentInput`, `AgentOutput`,
and `ToolCallResult`) and converts them into a list of `Message` objects (`HumanMessage`,
`AIMessage`, and `ToolMessage`) that can be used for evaluation with the Ragas framework.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `events` | `List[Event]` | A list of agent events that represent a conversation trace. These can include user inputs (`AgentInput`), model outputs (`AgentOutput`), and tool responses (`ToolCallResult`). | *required* |

Returns:

| Type | Description |
| --- | --- |
| `List[Message]` | A list of Ragas `Message` objects corresponding to the structured conversation. Tool calls are de-duplicated using their tool ID to avoid repeated entries. |

Source code in `src/ragas/integrations/llama_index.py`

|  |  |
| --- | --- |
| ``` 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 ``` | ``` def convert_to_ragas_messages(events: t.List[Event]) -> t.List[Message]:     """     Convert a sequence of LlamIndex agent events into Ragas message objects.      This function processes a list of `Event` objects (e.g., `AgentInput`, `AgentOutput`,     and `ToolCallResult`) and converts them into a list of `Message` objects (`HumanMessage`,     `AIMessage`, and `ToolMessage`) that can be used for evaluation with the Ragas framework.      Parameters     ----------     events : List[Event]         A list of agent events that represent a conversation trace. These can include         user inputs (`AgentInput`), model outputs (`AgentOutput`), and tool responses         (`ToolCallResult`).      Returns     -------     List[Message]         A list of Ragas `Message` objects corresponding to the structured conversation.         Tool calls are de-duplicated using their tool ID to avoid repeated entries.     """     try:         from llama_index.core.agent.workflow import (             AgentInput,             AgentOutput,             ToolCallResult,         )         from llama_index.core.base.llms.types import MessageRole, TextBlock     except ImportError:         raise ImportError(             "Please install the llama_index package to use this function."         )     ragas_messages = []     tool_call_ids = set()      for event in events:         if isinstance(event, AgentInput):             last_chat_message = event.input[-1]              content = ""             if last_chat_message.blocks:                 content = "\n".join(                     str(block.text)                     for block in last_chat_message.blocks                     if isinstance(block, TextBlock)                 )              if last_chat_message.role == MessageRole.USER:                 if ragas_messages and isinstance(ragas_messages[-1], ToolMessage):                     continue                 ragas_messages.append(HumanMessage(content=content))          elif isinstance(event, AgentOutput):             content = "\n".join(                 str(block.text)                 for block in event.response.blocks                 if isinstance(block, TextBlock)             )             ragas_tool_calls = None              if hasattr(event, "tool_calls"):                 raw_tool_calls = event.tool_calls                 ragas_tool_calls = []                 for tc in raw_tool_calls:                     if tc.tool_id not in tool_call_ids:                         tool_call_ids.add(tc.tool_id)                         ragas_tool_calls.append(                             ToolCall(                                 name=tc.tool_name,                                 args=tc.tool_kwargs,                             )                         )             ragas_messages.append(                 AIMessage(                     content=content,                     tool_calls=ragas_tool_calls if ragas_tool_calls else None,                 )             )         elif isinstance(event, ToolCallResult):             if event.return_direct:                 ragas_messages.append(AIMessage(content=event.tool_output.content))             else:                 ragas_messages.append(ToolMessage(content=event.tool_output.content))      return ragas_messages ``` |

## ragas.integrations.opik

### OpikTracer

Bases: `OpikTracer`

Callback for Opik that can be used to log traces and evaluation scores to the Opik platform.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `tags` | `list[string]` | The tags to set on each trace. |
| `metadata` | `dict` | Additional metadata to log for each trace. |

## ragas.integrations.helicone

## ragas.integrations.langgraph

### convert\_to\_ragas\_messages

```
convert_to_ragas_messages(messages: List[Union[HumanMessage, SystemMessage, AIMessage, ToolMessage]], metadata: bool = False) -> List[Union[HumanMessage, AIMessage, ToolMessage]]
```

Convert LangChain messages into Ragas messages with metadata for agent evaluation.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `messages` | `List[Union[HumanMessage, SystemMessage, AIMessage, ToolMessage]]` | List of LangChain message objects to be converted. | *required* |
| `metadata` | `(bool, optional(default=False))` | Whether to include metadata in the converted messages. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `List[Union[HumanMessage, AIMessage, ToolMessage]]` | List of corresponding Ragas message objects with metadata. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If an unsupported message type is encountered. |
| `TypeError` | If message content is not a string. |

Notes

SystemMessages are skipped in the conversion process.


Source code in `src/ragas/integrations/langgraph.py`

|  |  |
| --- | --- |
| ```   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 ``` | ``` def convert_to_ragas_messages(     messages: List[Union[HumanMessage, SystemMessage, AIMessage, ToolMessage]],     metadata: bool = False, ) -> List[Union[r.HumanMessage, r.AIMessage, r.ToolMessage]]:     """     Convert LangChain messages into Ragas messages with metadata for agent evaluation.      Parameters     ----------     messages : List[Union[HumanMessage, SystemMessage, AIMessage, ToolMessage]]         List of LangChain message objects to be converted.     metadata : bool, optional (default=False)         Whether to include metadata in the converted messages.      Returns     -------     List[Union[r.HumanMessage, r.AIMessage, r.ToolMessage]]         List of corresponding Ragas message objects with metadata.      Raises     ------     ValueError         If an unsupported message type is encountered.     TypeError         If message content is not a string.      Notes     -----     SystemMessages are skipped in the conversion process.     """      def _validate_string_content(message, message_type: str) -> str:         if not isinstance(message.content, str):             raise TypeError(                 f"{message_type} content must be a string, got {type(message.content).__name__}. "                 f"Content: {message.content}"             )         return message.content      def _extract_metadata(message) -> dict:         return {k: v for k, v in message.__dict__.items() if k != "content"}      if metadata:         MESSAGE_TYPE_MAP = {             HumanMessage: lambda m: r.HumanMessage(                 content=_validate_string_content(m, "HumanMessage"),                 metadata=_extract_metadata(m),             ),             ToolMessage: lambda m: r.ToolMessage(                 content=_validate_string_content(m, "ToolMessage"),                 metadata=_extract_metadata(m),             ),         }     else:         MESSAGE_TYPE_MAP = {             HumanMessage: lambda m: r.HumanMessage(                 content=_validate_string_content(m, "HumanMessage")             ),             ToolMessage: lambda m: r.ToolMessage(                 content=_validate_string_content(m, "ToolMessage")             ),         }      def _extract_tool_calls(message: AIMessage) -> List[r.ToolCall]:         tool_calls = message.additional_kwargs.get("tool_calls", [])         return [             r.ToolCall(                 name=tool_call["function"]["name"],                 args=json.loads(tool_call["function"]["arguments"]),             )             for tool_call in tool_calls         ]      def _convert_ai_message(message: AIMessage, metadata: bool) -> r.AIMessage:         tool_calls = _extract_tool_calls(message) if message.additional_kwargs else None         if metadata:             return r.AIMessage(                 content=_validate_string_content(message, "AIMessage"),                 tool_calls=tool_calls,                 metadata=_extract_metadata(message),             )         else:             return r.AIMessage(                 content=_validate_string_content(message, "AIMessage"),                 tool_calls=tool_calls,             )      def _convert_message(message, metadata: bool = False):         if isinstance(message, SystemMessage):             return None  # Skip SystemMessages         if isinstance(message, AIMessage):             return _convert_ai_message(message, metadata)         converter = MESSAGE_TYPE_MAP.get(type(message))         if converter is None:             raise ValueError(f"Unsupported message type: {type(message).__name__}")         return converter(message)      return [         converted         for message in messages         if (converted := _convert_message(message)) is not None     ] ``` |

November 28, 2025




November 28, 2025

Back to top