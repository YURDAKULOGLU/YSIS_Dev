evaluate() - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#evaluation)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Evaluation

## evaluate()

Perform the evaluation on the dataset with different metrics

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `dataset` | `(Dataset, EvaluationDataset)` | The dataset used by the metrics to evaluate the RAG pipeline. | *required* |
| `metrics` | `list[Metric]` | List of metrics to use for evaluation. If not provided, ragas will run the evaluation on the best set of metrics to give a complete view. | `None` |
| `llm` | `BaseRagasLLM` | The language model (LLM) to use to generate the score for calculating the metrics. If not provided, ragas will use the default language model for metrics that require an LLM. This can be overridden by the LLM specified in the metric level with `metric.llm`. | `None` |
| `embeddings` | `BaseRagasEmbeddings` | The embeddings model to use for the metrics. If not provided, ragas will use the default embeddings for metrics that require embeddings. This can be overridden by the embeddings specified in the metric level with `metric.embeddings`. | `None` |
| `experiment_name` | `str` | The name of the experiment to track. This is used to track the evaluation in the tracing tool. | `None` |
| `callbacks` | `Callbacks` | Lifecycle Langchain Callbacks to run during evaluation. Check the [Langchain documentation](https://python.langchain.com/docs/modules/callbacks/) for more information. | `None` |
| `run_config` | `RunConfig` | Configuration for runtime settings like timeout and retries. If not provided, default values are used. | `None` |
| `token_usage_parser` | `TokenUsageParser` | Parser to get the token usage from the LLM result. If not provided, the cost and total token count will not be calculated. Default is None. | `None` |
| `raise_exceptions` | `False` | Whether to raise exceptions or not. If set to True, the evaluation will raise an exception if any of the metrics fail. If set to False, the evaluation will return `np.nan` for the row that failed. Default is False. | `False` |
| `column_map` | `dict[str, str]` | The column names of the dataset to use for evaluation. If the column names of the dataset are different from the default ones, it is possible to provide the mapping as a dictionary here. Example: If the dataset column name is `contexts_v1`, it is possible to pass column\_map as `{"contexts": "contexts_v1"}`. | `None` |
| `show_progress` | `bool` | Whether to show the progress bar during evaluation. If set to False, the progress bar will be disabled. The default is True. | `True` |
| `batch_size` | `int` | How large the batches should be. If set to None (default), no batching is done. | `None` |
| `return_executor` | `bool` | If True, returns the Executor instance instead of running evaluation. The returned executor can be used to cancel execution by calling executor.cancel(). To get results, call executor.results(). Default is False. | `False` |
| `allow_nest_asyncio` | `bool` | Whether to allow nest\_asyncio patching for Jupyter compatibility. Set to False in production async applications to avoid event loop conflicts. Default is True. | `True` |

Returns:

| Type | Description |
| --- | --- |
| `EvaluationResult or Executor` | If return\_executor is False, returns EvaluationResult object containing the scores of each metric. If return\_executor is True, returns the Executor instance for cancellable execution. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | if validation fails because the columns required for the metrics are missing or if the columns are of the wrong format. |

Examples:

the basic usage is as follows:

```
from ragas import evaluate

>>> dataset
Dataset({
    features: ['question', 'ground_truth', 'answer', 'contexts'],
    num_rows: 30
})

>>> result = evaluate(dataset)
>>> print(result)
{'context_precision': 0.817,
'faithfulness': 0.892,
'answer_relevancy': 0.874}
```

Source code in `src/ragas/evaluation.py`

|  |  |
| --- | --- |
| ``` 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 ``` | ``` @track_was_completed def evaluate(     dataset: t.Union[Dataset, EvaluationDataset],     metrics: t.Optional[t.Sequence[Metric]] = None,     llm: t.Optional[BaseRagasLLM | LangchainLLM] = None,     embeddings: t.Optional[         BaseRagasEmbeddings | BaseRagasEmbedding | LangchainEmbeddings     ] = None,     experiment_name: t.Optional[str] = None,     callbacks: Callbacks = None,     run_config: t.Optional[RunConfig] = None,     token_usage_parser: t.Optional[TokenUsageParser] = None,     raise_exceptions: bool = False,     column_map: t.Optional[t.Dict[str, str]] = None,     show_progress: bool = True,     batch_size: t.Optional[int] = None,     _run_id: t.Optional[UUID] = None,     _pbar: t.Optional[tqdm] = None,     return_executor: bool = False,     allow_nest_asyncio: bool = True, ) -> t.Union[EvaluationResult, Executor]:     """     Perform the evaluation on the dataset with different metrics      Parameters     ----------     dataset : Dataset, EvaluationDataset         The dataset used by the metrics to evaluate the RAG pipeline.     metrics : list[Metric], optional         List of metrics to use for evaluation. If not provided, ragas will run         the evaluation on the best set of metrics to give a complete view.     llm : BaseRagasLLM, optional         The language model (LLM) to use to generate the score for calculating the metrics.         If not provided, ragas will use the default         language model for metrics that require an LLM. This can be overridden by the LLM         specified in the metric level with `metric.llm`.     embeddings : BaseRagasEmbeddings, optional         The embeddings model to use for the metrics.         If not provided, ragas will use the default embeddings for metrics that require embeddings.         This can be overridden by the embeddings specified in the metric level with `metric.embeddings`.     experiment_name : str, optional         The name of the experiment to track. This is used to track the evaluation in the tracing tool.     callbacks : Callbacks, optional         Lifecycle Langchain Callbacks to run during evaluation.         Check the [Langchain documentation](https://python.langchain.com/docs/modules/callbacks/) for more information.     run_config : RunConfig, optional         Configuration for runtime settings like timeout and retries. If not provided, default values are used.     token_usage_parser : TokenUsageParser, optional         Parser to get the token usage from the LLM result.         If not provided, the cost and total token count will not be calculated. Default is None.     raise_exceptions : False         Whether to raise exceptions or not. If set to True, the evaluation will raise an exception         if any of the metrics fail. If set to False, the evaluation will return `np.nan` for the row that failed. Default is False.     column_map : dict[str, str], optional         The column names of the dataset to use for evaluation. If the column names of the dataset are different from the default ones,         it is possible to provide the mapping as a dictionary here. Example: If the dataset column name is `contexts_v1`, it is possible to pass column_map as `{"contexts": "contexts_v1"}`.     show_progress : bool, optional         Whether to show the progress bar during evaluation. If set to False, the progress bar will be disabled. The default is True.     batch_size : int, optional         How large the batches should be. If set to None (default), no batching is done.     return_executor : bool, optional         If True, returns the Executor instance instead of running evaluation.         The returned executor can be used to cancel execution by calling executor.cancel().         To get results, call executor.results(). Default is False.     allow_nest_asyncio : bool, optional         Whether to allow nest_asyncio patching for Jupyter compatibility.         Set to False in production async applications to avoid event loop conflicts. Default is True.      Returns     -------     EvaluationResult or Executor         If return_executor is False, returns EvaluationResult object containing the scores of each metric.         If return_executor is True, returns the Executor instance for cancellable execution.      Raises     ------     ValueError         if validation fails because the columns required for the metrics are missing or         if the columns are of the wrong format.      Examples     --------     the basic usage is as follows:     ```     from ragas import evaluate      >>> dataset     Dataset({         features: ['question', 'ground_truth', 'answer', 'contexts'],         num_rows: 30     })      >>> result = evaluate(dataset)     >>> print(result)     {'context_precision': 0.817,     'faithfulness': 0.892,     'answer_relevancy': 0.874}     ```     """     warnings.warn(         "evaluate() is deprecated and will be removed in a future version. "         "Use the @experiment decorator instead. "         "See https://docs.ragas.io/en/latest/concepts/experiment/ for more information.",         DeprecationWarning,         stacklevel=2,     )      # Create async wrapper for aevaluate     async def _async_wrapper():         return await aevaluate(             dataset=dataset,             metrics=metrics,             llm=llm,             embeddings=embeddings,             experiment_name=experiment_name,             callbacks=callbacks,             run_config=run_config,             token_usage_parser=token_usage_parser,             raise_exceptions=raise_exceptions,             column_map=column_map,             show_progress=show_progress,             batch_size=batch_size,             _run_id=_run_id,             _pbar=_pbar,             return_executor=return_executor,         )      if not allow_nest_asyncio:         # Run without nest_asyncio - creates a new event loop         import asyncio          return asyncio.run(_async_wrapper())     else:         # Default behavior: use nest_asyncio for backward compatibility (Jupyter notebooks)         from ragas.async_utils import run          return run(_async_wrapper()) ``` |

November 28, 2025




November 28, 2025

Back to top