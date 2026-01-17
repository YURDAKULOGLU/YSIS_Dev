Generation - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.testset.synthesizers.generate)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Generation

## TestsetGenerator `dataclass`

```
TestsetGenerator(llm: BaseRagasLLM, embedding_model: BaseRagasEmbeddings, knowledge_graph: KnowledgeGraph = KnowledgeGraph(), persona_list: Optional[List[Persona]] = None, llm_context: Optional[str] = None)
```

Generates an evaluation dataset based on given scenarios and parameters.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `llm` | `BaseRagasLLM` | The language model to use for the generation process. |
| `knowledge_graph` | `KnowledgeGraph, default empty` | The knowledge graph to use for the generation process. |
| `llm_context` | `Optional[str], default None` | Additional context to provide to the LLM when generating responses. This context will be used to guide how the LLM generates queries and answers. |

### from\_langchain `classmethod`

```
from_langchain(llm: BaseLanguageModel, embedding_model: Embeddings, knowledge_graph: Optional[KnowledgeGraph] = None, llm_context: Optional[str] = None) -> TestsetGenerator
```

Creates a `TestsetGenerator` from a Langchain LLMs.

Source code in `src/ragas/testset/synthesizers/generate.py`

|  |  |
| --- | --- |
| ``` 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 ``` | ``` @classmethod def from_langchain(     cls,     llm: LangchainLLM,     embedding_model: LangchainEmbeddings,     knowledge_graph: t.Optional[KnowledgeGraph] = None,     llm_context: t.Optional[str] = None, ) -> TestsetGenerator:     """     Creates a `TestsetGenerator` from a Langchain LLMs.     """     knowledge_graph = knowledge_graph or KnowledgeGraph()     return cls(         LangchainLLMWrapper(llm),         LangchainEmbeddingsWrapper(embedding_model),         knowledge_graph,         llm_context=llm_context,     ) ``` |

### from\_llama\_index `classmethod`

```
from_llama_index(llm: BaseLLM, embedding_model: BaseEmbedding, knowledge_graph: Optional[KnowledgeGraph] = None, llm_context: Optional[str] = None) -> TestsetGenerator
```

Creates a `TestsetGenerator` from a LlamaIndex LLM and embedding model.

Source code in `src/ragas/testset/synthesizers/generate.py`

|  |  |
| --- | --- |
| ```  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 ``` | ``` @classmethod def from_llama_index(     cls,     llm: LlamaIndexLLM,     embedding_model: LlamaIndexEmbedding,     knowledge_graph: t.Optional[KnowledgeGraph] = None,     llm_context: t.Optional[str] = None, ) -> TestsetGenerator:     """     Creates a `TestsetGenerator` from a LlamaIndex LLM and embedding model.     """     knowledge_graph = knowledge_graph or KnowledgeGraph()     return cls(         LlamaIndexLLMWrapper(llm),         LlamaIndexEmbeddingsWrapper(embedding_model),         knowledge_graph,         llm_context=llm_context,     ) ``` |

### generate\_with\_langchain\_docs

```
generate_with_langchain_docs(documents: Sequence[Document], testset_size: int, transforms: Optional[Transforms] = None, transforms_llm: Optional[BaseRagasLLM] = None, transforms_embedding_model: Optional[BaseRagasEmbeddings] = None, query_distribution: Optional[QueryDistribution] = None, run_config: Optional[RunConfig] = None, callbacks: Optional[Callbacks] = None, token_usage_parser: Optional[TokenUsageParser] = None, with_debugging_logs=False, raise_exceptions: bool = True, return_executor: bool = False) -> Union[Testset, Executor]
```

Generates an evaluation dataset based on given Langchain documents and parameters.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `documents` | `Sequence[Document]` | A sequence of Langchain documents to use as source material | *required* |
| `testset_size` | `int` | The number of test samples to generate | *required* |
| `transforms` | `Optional[Transforms]` | Custom transforms to apply to the documents, by default None | `None` |
| `transforms_llm` | `Optional[BaseRagasLLM]` | LLM to use for transforms if different from instance LLM, by default None | `None` |
| `transforms_embedding_model` | `Optional[BaseRagasEmbeddings]` | Embedding model to use for transforms if different from instance model, by default None | `None` |
| `query_distribution` | `Optional[QueryDistribution]` | Distribution of query types to generate, by default None | `None` |
| `run_config` | `Optional[RunConfig]` | Configuration for the generation run, by default None | `None` |
| `callbacks` | `Optional[Callbacks]` | Callbacks to use during generation, by default None | `None` |
| `token_usage_parser` | `Optional[TokenUsageParser]` | Parse the LLMResult object and return a TokenUsage object. This is used to calculate the cost of the generation process. | `None` |
| `with_debugging_logs` | `bool` | Whether to include debug logs, by default False | `False` |
| `raise_exceptions` | `bool` | Whether to raise exceptions during generation, by default True | `True` |
| `return_executor` | `bool` | If True, returns the Executor instance instead of running generation. The returned executor can be used to cancel execution by calling executor.cancel(). To get results, call executor.results(). Default is False. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Testset or Executor` | If return\_executor is False, returns the generated evaluation dataset. If return\_executor is True, returns the Executor instance for cancellable execution. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If no LLM or embedding model is provided either during initialization or as arguments |

Source code in `src/ragas/testset/synthesizers/generate.py`

|  |  |
| --- | --- |
| ``` 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 ``` | ``` def generate_with_langchain_docs(     self,     documents: t.Sequence[LCDocument],     testset_size: int,     transforms: t.Optional[Transforms] = None,     transforms_llm: t.Optional[BaseRagasLLM] = None,     transforms_embedding_model: t.Optional[BaseRagasEmbeddings] = None,     query_distribution: t.Optional[QueryDistribution] = None,     run_config: t.Optional[RunConfig] = None,     callbacks: t.Optional[Callbacks] = None,     token_usage_parser: t.Optional[TokenUsageParser] = None,     with_debugging_logs=False,     raise_exceptions: bool = True,     return_executor: bool = False, ) -> t.Union[Testset, Executor]:     """     Generates an evaluation dataset based on given Langchain documents and parameters.      Parameters     ----------     documents : Sequence[LCDocument]         A sequence of Langchain documents to use as source material     testset_size : int         The number of test samples to generate     transforms : Optional[Transforms], optional         Custom transforms to apply to the documents, by default None     transforms_llm : Optional[BaseRagasLLM], optional         LLM to use for transforms if different from instance LLM, by default None     transforms_embedding_model : Optional[BaseRagasEmbeddings], optional         Embedding model to use for transforms if different from instance model, by default None     query_distribution : Optional[QueryDistribution], optional         Distribution of query types to generate, by default None     run_config : Optional[RunConfig], optional         Configuration for the generation run, by default None     callbacks : Optional[Callbacks], optional         Callbacks to use during generation, by default None     token_usage_parser : Optional[TokenUsageParser], optional         Parse the LLMResult object and return a TokenUsage object. This is used to         calculate the cost of the generation process.     with_debugging_logs : bool, optional         Whether to include debug logs, by default False     raise_exceptions : bool, optional         Whether to raise exceptions during generation, by default True     return_executor : bool, optional         If True, returns the Executor instance instead of running generation.         The returned executor can be used to cancel execution by calling executor.cancel().         To get results, call executor.results(). Default is False.      Returns     -------     Testset or Executor         If return_executor is False, returns the generated evaluation dataset.         If return_executor is True, returns the Executor instance for cancellable execution.      Raises     ------     ValueError         If no LLM or embedding model is provided either during initialization or as arguments     """      # force the user to provide an llm and embedding client to prevent use of default LLMs     if not self.llm and not transforms_llm:         raise ValueError(             """An llm client was not provided.                    Provide an LLM on TestsetGenerator instantiation or as an argument for transforms_llm parameter.                    Alternatively you can provide your own transforms through the `transforms` parameter."""         )     if not self.embedding_model and not transforms_embedding_model:         raise ValueError(             """An embedding client was not provided. Provide an embedding through the transforms_embedding_model parameter. Alternatively you can provide your own transforms through the `transforms` parameter."""         )      if not transforms:         transforms = default_transforms(             documents=list(documents),             llm=transforms_llm or self.llm,             embedding_model=transforms_embedding_model or self.embedding_model,         )      # convert the documents to Ragas nodes     nodes = []     for doc in documents:         node = Node(             type=NodeType.DOCUMENT,             properties={                 "page_content": doc.page_content,                 "document_metadata": doc.metadata,             },         )         nodes.append(node)      kg = KnowledgeGraph(nodes=nodes)      # apply transforms and update the knowledge graph     apply_transforms(kg, transforms, run_config=run_config or RunConfig())     self.knowledge_graph = kg      return self.generate(         testset_size=testset_size,         query_distribution=query_distribution,         run_config=run_config,         callbacks=callbacks,         token_usage_parser=token_usage_parser,         with_debugging_logs=with_debugging_logs,         raise_exceptions=raise_exceptions,         return_executor=return_executor,     ) ``` |

### generate\_with\_llamaindex\_docs

```
generate_with_llamaindex_docs(documents: Sequence[Document], testset_size: int, transforms: Optional[Transforms] = None, transforms_llm: Optional[BaseLLM] = None, transforms_embedding_model: Optional[BaseEmbedding] = None, query_distribution: Optional[QueryDistribution] = None, run_config: Optional[RunConfig] = None, callbacks: Optional[Callbacks] = None, token_usage_parser: Optional[TokenUsageParser] = None, with_debugging_logs=False, raise_exceptions: bool = True)
```

Generates an evaluation dataset based on given scenarios and parameters.

Source code in `src/ragas/testset/synthesizers/generate.py`

|  |  |
| --- | --- |
| ``` 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 ``` | ``` def generate_with_llamaindex_docs(     self,     documents: t.Sequence[LlamaIndexDocument],     testset_size: int,     transforms: t.Optional[Transforms] = None,     transforms_llm: t.Optional[LlamaIndexLLM] = None,     transforms_embedding_model: t.Optional[LlamaIndexEmbedding] = None,     query_distribution: t.Optional[QueryDistribution] = None,     run_config: t.Optional[RunConfig] = None,     callbacks: t.Optional[Callbacks] = None,     token_usage_parser: t.Optional[TokenUsageParser] = None,     with_debugging_logs=False,     raise_exceptions: bool = True, ):     """     Generates an evaluation dataset based on given scenarios and parameters.     """      run_config = run_config or RunConfig()      # force the user to provide an llm and embedding client to prevent use of default LLMs     if not self.llm and not transforms_llm:         raise ValueError(             "An llm client was not provided. Provide an LLM on TestsetGenerator instantiation or as an argument for transforms_llm parameter. Alternatively you can provide your own transforms through the `transforms` parameter."         )     if not self.embedding_model and not transforms_embedding_model:         raise ValueError(             "An embedding client was not provided. Provide an embedding through the transforms_embedding_model parameter. Alternatively you can provide your own transforms through the `transforms` parameter."         )      if not transforms:         # use TestsetGenerator's LLM and embedding model if no transforms_llm or transforms_embedding_model is provided         if transforms_llm is None:             llm_for_transforms = self.llm         else:             llm_for_transforms = LlamaIndexLLMWrapper(transforms_llm)         if transforms_embedding_model is None:             embedding_model_for_transforms = self.embedding_model         else:             embedding_model_for_transforms = LlamaIndexEmbeddingsWrapper(                 transforms_embedding_model             )          # create the transforms         transforms = default_transforms(             documents=[LCDocument(page_content=doc.text) for doc in documents],             llm=llm_for_transforms,             embedding_model=embedding_model_for_transforms,         )      # convert the documents to Ragas nodes     nodes = []     for doc in documents:         if doc.text is not None and doc.text.strip() != "":             node = Node(                 type=NodeType.DOCUMENT,                 properties={                     "page_content": doc.text,                     "document_metadata": doc.metadata,                 },             )             nodes.append(node)      kg = KnowledgeGraph(nodes=nodes)      # apply transforms and update the knowledge graph     apply_transforms(kg, transforms, run_config)     self.knowledge_graph = kg      return self.generate(         testset_size=testset_size,         query_distribution=query_distribution,         run_config=run_config,         callbacks=callbacks,         token_usage_parser=token_usage_parser,         with_debugging_logs=with_debugging_logs,         raise_exceptions=raise_exceptions,         return_executor=False,  # Default value for llamaindex_docs method     ) ``` |

### generate\_with\_chunks

```
generate_with_chunks(chunks: Sequence[Union[Document, str]], testset_size: int, transforms: Optional[Transforms] = None, transforms_llm: Optional[BaseRagasLLM] = None, transforms_embedding_model: Optional[BaseRagasEmbeddings] = None, query_distribution: Optional[QueryDistribution] = None, run_config: Optional[RunConfig] = None, callbacks: Optional[Callbacks] = None, token_usage_parser: Optional[TokenUsageParser] = None, with_debugging_logs=False, raise_exceptions: bool = True, return_executor: bool = False) -> Union[Testset, Executor]
```

Generates an evaluation dataset based on provided pre-chunked documents.

This method allows users to skip the internal chunking process by providing
documents that are already chunked. The input documents are treated as
`NodeType.CHUNK` directly.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `chunks` | `Sequence[Union[Document, str]]` | A sequence of Langchain documents or strings to use as chunks. Strings will be automatically converted to Documents. | *required* |
| `testset_size` | `int` | The number of test samples to generate | *required* |
| `transforms` | `Optional[Transforms]` | Custom transforms to apply to the chunks, by default None | `None` |
| `transforms_llm` | `Optional[BaseRagasLLM]` | LLM to use for transforms if different from instance LLM, by default None | `None` |
| `transforms_embedding_model` | `Optional[BaseRagasEmbeddings]` | Embedding model to use for transforms if different from instance model, by default None | `None` |
| `query_distribution` | `Optional[QueryDistribution]` | Distribution of query types to generate, by default None | `None` |
| `run_config` | `Optional[RunConfig]` | Configuration for the generation run, by default None | `None` |
| `callbacks` | `Optional[Callbacks]` | Callbacks to use during generation, by default None | `None` |
| `token_usage_parser` | `Optional[TokenUsageParser]` | Parse the LLMResult object and return a TokenUsage object. | `None` |
| `with_debugging_logs` | `bool` | Whether to include debug logs, by default False | `False` |
| `raise_exceptions` | `bool` | Whether to raise exceptions during generation, by default True | `True` |
| `return_executor` | `bool` | If True, returns the Executor instance instead of running generation. | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Testset or Executor` | If return\_executor is False, returns the generated evaluation dataset. If return\_executor is True, returns the Executor instance. |

Source code in `src/ragas/testset/synthesizers/generate.py`

|  |  |
| --- | --- |
| ``` 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 ``` | ``` def generate_with_chunks(     self,     chunks: t.Sequence[t.Union[LCDocument, str]],     testset_size: int,     transforms: t.Optional[Transforms] = None,     transforms_llm: t.Optional[BaseRagasLLM] = None,     transforms_embedding_model: t.Optional[BaseRagasEmbeddings] = None,     query_distribution: t.Optional[QueryDistribution] = None,     run_config: t.Optional[RunConfig] = None,     callbacks: t.Optional[Callbacks] = None,     token_usage_parser: t.Optional[TokenUsageParser] = None,     with_debugging_logs=False,     raise_exceptions: bool = True,     return_executor: bool = False, ) -> t.Union[Testset, Executor]:     """     Generates an evaluation dataset based on provided pre-chunked documents.      This method allows users to skip the internal chunking process by providing     documents that are already chunked. The input documents are treated as     `NodeType.CHUNK` directly.      Parameters     ----------     chunks : Sequence[Union[LCDocument, str]]         A sequence of Langchain documents or strings to use as chunks.         Strings will be automatically converted to Documents.     testset_size : int         The number of test samples to generate     transforms : Optional[Transforms], optional         Custom transforms to apply to the chunks, by default None     transforms_llm : Optional[BaseRagasLLM], optional         LLM to use for transforms if different from instance LLM, by default None     transforms_embedding_model : Optional[BaseRagasEmbeddings], optional         Embedding model to use for transforms if different from instance model, by default None     query_distribution : Optional[QueryDistribution], optional         Distribution of query types to generate, by default None     run_config : Optional[RunConfig], optional         Configuration for the generation run, by default None     callbacks : Optional[Callbacks], optional         Callbacks to use during generation, by default None     token_usage_parser : Optional[TokenUsageParser], optional         Parse the LLMResult object and return a TokenUsage object.     with_debugging_logs : bool, optional         Whether to include debug logs, by default False     raise_exceptions : bool, optional         Whether to raise exceptions during generation, by default True     return_executor : bool, optional         If True, returns the Executor instance instead of running generation.      Returns     -------     Testset or Executor         If return_executor is False, returns the generated evaluation dataset.         If return_executor is True, returns the Executor instance.     """      # force the user to provide an llm and embedding client     if not self.llm and not transforms_llm:         raise ValueError(             """An llm client was not provided.                    Provide an LLM on TestsetGenerator instantiation or as an argument for transforms_llm parameter.                    Alternatively you can provide your own transforms through the `transforms` parameter."""         )     if not self.embedding_model and not transforms_embedding_model:         raise ValueError(             """An embedding client was not provided. Provide an embedding through the transforms_embedding_model parameter. Alternatively you can provide your own transforms through the `transforms` parameter."""         )      if transforms is None:         transforms = default_transforms_for_prechunked(             llm=transforms_llm or self.llm,             embedding_model=transforms_embedding_model or self.embedding_model,         )      # convert the chunks to Ragas nodes     nodes = []     for chunk in chunks:         if isinstance(chunk, str):             page_content = chunk             metadata = {}         else:             page_content = chunk.page_content             metadata = chunk.metadata          if page_content is not None and page_content.strip() != "":             node = Node(                 type=NodeType.CHUNK,                 properties={                     "page_content": page_content,                     "document_metadata": metadata,                 },             )             nodes.append(node)      kg = KnowledgeGraph(nodes=nodes)      # apply transforms and update the knowledge graph     apply_transforms(kg, transforms, run_config=run_config or RunConfig())     self.knowledge_graph = kg      return self.generate(         testset_size=testset_size,         query_distribution=query_distribution,         run_config=run_config,         callbacks=callbacks,         token_usage_parser=token_usage_parser,         with_debugging_logs=with_debugging_logs,         raise_exceptions=raise_exceptions,         return_executor=return_executor,     ) ``` |

### generate

```
generate(testset_size: int, query_distribution: Optional[QueryDistribution] = None, num_personas: int = 3, run_config: Optional[RunConfig] = None, batch_size: Optional[int] = None, callbacks: Optional[Callbacks] = None, token_usage_parser: Optional[TokenUsageParser] = None, with_debugging_logs=False, raise_exceptions: bool = True, return_executor: bool = False) -> Union[Testset, Executor]
```

Generate an evaluation dataset based on given scenarios and parameters.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `testset_size` | `int` | The number of samples to generate. | *required* |
| `query_distribution` | `Optional[QueryDistribution]` | A list of tuples containing scenario simulators and their probabilities. If None, default simulators will be used. | `None` |
| `num_personas` | `int` | The number of personas to generate or use from the persona\_list. | `3` |
| `run_config` | `Optional[RunConfig]` | Configuration for running the generation process. | `None` |
| `batch_size` | `Optional[int]` | How large should batches be. If set to None (default), no batching is done. | `None` |
| `callbacks` | `Optional[Callbacks]` | Langchain style callbacks to use for the generation process. You can use this to log the generation process or add other metadata. | `None` |
| `token_usage_parser` | `Optional[TokenUsageParser]` | Parse the LLMResult object and return a TokenUsage object. This is used to calculate the cost of the generation process. | `None` |
| `with_debugging_logs` | `bool` | If True, enable debug logging for various components. | `False` |
| `raise_exceptions` | `bool` | If True, raise exceptions during the generation process. | `True` |
| `return_executor` | `bool` | If True, returns the Executor instance instead of running generation. The returned executor can be used to cancel execution by calling executor.cancel(). To get results, call executor.results(). | `False` |

Returns:

| Type | Description |
| --- | --- |
| `Testset or Executor` | If return\_executor is False, returns a dataset containing the generated TestsetSamples. If return\_executor is True, returns the Executor instance for cancellable execution. |

Notes

This function performs the following steps:
1. Set up scenarios and debug logging if required.
2. Generate scenarios using an Executor.
3. Calculate split values for different scenario types.
4. Generate samples for each scenario.
5. Compile the results into an EvaluationDataset.


Source code in `src/ragas/testset/synthesizers/generate.py`

|  |  |
| --- | --- |
| ``` 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 ``` | ``` def generate(     self,     testset_size: int,     query_distribution: t.Optional[QueryDistribution] = None,     num_personas: int = 3,     run_config: t.Optional[RunConfig] = None,     batch_size: t.Optional[int] = None,     callbacks: t.Optional[Callbacks] = None,     token_usage_parser: t.Optional[TokenUsageParser] = None,     with_debugging_logs=False,     raise_exceptions: bool = True,     return_executor: bool = False, ) -> t.Union[Testset, Executor]:     """     Generate an evaluation dataset based on given scenarios and parameters.      Parameters     ----------     testset_size : int         The number of samples to generate.     query_distribution : Optional[QueryDistribution], optional         A list of tuples containing scenario simulators and their probabilities.         If None, default simulators will be used.     num_personas : int, default 3         The number of personas to generate or use from the persona_list.     run_config : Optional[RunConfig], optional         Configuration for running the generation process.     batch_size: int, optional         How large should batches be.  If set to None (default), no batching is done.     callbacks : Optional[Callbacks], optional         Langchain style callbacks to use for the generation process. You can use         this to log the generation process or add other metadata.     token_usage_parser : Optional[TokenUsageParser], optional         Parse the LLMResult object and return a TokenUsage object. This is used to         calculate the cost of the generation process.     with_debugging_logs : bool, default False         If True, enable debug logging for various components.     raise_exceptions : bool, default True         If True, raise exceptions during the generation process.     return_executor : bool, default False         If True, returns the Executor instance instead of running generation.         The returned executor can be used to cancel execution by calling executor.cancel().         To get results, call executor.results().      Returns     -------     Testset or Executor         If return_executor is False, returns a dataset containing the generated TestsetSamples.         If return_executor is True, returns the Executor instance for cancellable execution.      Notes     -----     This function performs the following steps:     1. Set up scenarios and debug logging if required.     2. Generate scenarios using an Executor.     3. Calculate split values for different scenario types.     4. Generate samples for each scenario.     5. Compile the results into an EvaluationDataset.     """     if run_config is not None:         # Only BaseRagasLLM has set_run_config method, not InstructorBaseRagasLLM         if isinstance(self.llm, BaseRagasLLM):             self.llm.set_run_config(run_config)      query_distribution = query_distribution or default_query_distribution(         self.llm, self.knowledge_graph, self.llm_context     )     callbacks = callbacks or []      # dict to store any callbacks we define     ragas_callbacks = {}     # set the token usage parser     if token_usage_parser is not None:         from ragas.cost import CostCallbackHandler          cost_cb = CostCallbackHandler(token_usage_parser=token_usage_parser)         ragas_callbacks["cost_cb"] = cost_cb     else:         cost_cb = None      # append all the ragas_callbacks to the callbacks     for cb in ragas_callbacks.values():         if isinstance(callbacks, BaseCallbackManager):             callbacks.add_handler(cb)         else:             callbacks.append(cb)      # new group for Testset Generation     testset_generation_rm, testset_generation_grp = new_group(         name=RAGAS_TESTSET_GENERATION_GROUP_NAME,         inputs={"testset_size": testset_size},         callbacks=callbacks,     )      if with_debugging_logs:         # TODO: Edit this before pre-release         from ragas.utils import patch_logger          patch_logger("ragas.experimental.testset.synthesizers", logging.DEBUG)         patch_logger("ragas.experimental.testset.graph", logging.DEBUG)         patch_logger("ragas.experimental.testset.transforms", logging.DEBUG)      if self.persona_list is None:         self.persona_list = generate_personas_from_kg(             llm=self.llm,             kg=self.knowledge_graph,             num_personas=num_personas,             callbacks=callbacks,         )     else:         random.shuffle(self.persona_list)      splits, _ = calculate_split_values(         [prob for _, prob in query_distribution], testset_size     )     # new group for Generation of Scenarios     scenario_generation_rm, scenario_generation_grp = new_group(         name="Scenario Generation",         inputs={"splits": splits},         callbacks=testset_generation_grp,     )      # generate scenarios     exec = Executor(         desc="Generating Scenarios",         raise_exceptions=raise_exceptions,         run_config=run_config,         keep_progress_bar=False,         batch_size=batch_size,     )     # generate samples     splits, _ = calculate_split_values(         [prob for _, prob in query_distribution], testset_size     )     for i, (scenario, _) in enumerate(query_distribution):         exec.submit(             scenario.generate_scenarios,             n=splits[i],             knowledge_graph=self.knowledge_graph,             persona_list=self.persona_list[:num_personas],             callbacks=scenario_generation_grp,         )      try:         scenario_sample_list: t.List[t.List[BaseScenario]] = exec.results()     except Exception as e:         scenario_generation_rm.on_chain_error(e)         raise e     else:         scenario_generation_rm.on_chain_end(             outputs={"scenario_sample_list": scenario_sample_list}         )      # new group for Generation of Samples     sample_generation_rm, sample_generation_grp = new_group(         name="Sample Generation",         inputs={"scenario_sample_list": scenario_sample_list},         callbacks=testset_generation_grp,     )     exec = Executor(         "Generating Samples",         raise_exceptions=raise_exceptions,         run_config=run_config,         keep_progress_bar=True,         batch_size=batch_size,     )     additional_testset_info: t.List[t.Dict] = []     for i, (synthesizer, _) in enumerate(query_distribution):         for sample in scenario_sample_list[i]:             exec.submit(                 synthesizer.generate_sample,                 scenario=sample,                 callbacks=sample_generation_grp,             )             # fill out the additional info for the TestsetSample             additional_testset_info.append(                 {                     "synthesizer_name": synthesizer.name,                 }             )      # Return executor for cancellable execution if requested     if return_executor:         return exec      try:         eval_samples = exec.results()     except Exception as e:         sample_generation_rm.on_chain_error(e)         raise e     else:         sample_generation_rm.on_chain_end(outputs={"eval_samples": eval_samples})      # build the testset     testsets = []     for sample, additional_info in zip(eval_samples, additional_testset_info):         testsets.append(TestsetSample(eval_sample=sample, **additional_info))     testset = Testset(samples=testsets, cost_cb=cost_cb)     testset_generation_rm.on_chain_end({"testset": testset})      # tracking how many samples were generated     track(         TestsetGenerationEvent(             event_type="testset_generation",             evolution_names=[                 e.__class__.__name__.lower() for e, _ in query_distribution             ],             evolution_percentages=[p for _, p in query_distribution],             num_rows=testset_size,             language="english",         )     )     return testset ``` |

November 28, 2025




November 28, 2025

Back to top