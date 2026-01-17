Transforms - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.testset.transforms)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Transforms

## BaseGraphTransformation `dataclass`

```
BaseGraphTransformation(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)())
```

Bases: `ABC`

Abstract base class for graph transformations on a KnowledgeGraph.

### transform `abstractmethod` `async`

```
transform(kg: KnowledgeGraph) -> Any
```

Abstract method to transform the KnowledgeGraph. Transformations should be
idempotent, meaning that applying the transformation multiple times should
yield the same result as applying it once.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Any` | The transformed knowledge graph. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 ``` | ``` @abstractmethod async def transform(self, kg: KnowledgeGraph) -> t.Any:     """     Abstract method to transform the KnowledgeGraph. Transformations should be     idempotent, meaning that applying the transformation multiple times should     yield the same result as applying it once.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.Any         The transformed knowledge graph.     """     pass ``` |

### filter

```
filter(kg: KnowledgeGraph) -> KnowledgeGraph
```

Filters the KnowledgeGraph and returns the filtered graph.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be filtered. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `KnowledgeGraph` | The filtered knowledge graph. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 ``` | ``` def filter(self, kg: KnowledgeGraph) -> KnowledgeGraph:     """     Filters the KnowledgeGraph and returns the filtered graph.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be filtered.      Returns     -------     KnowledgeGraph         The filtered knowledge graph.     """     logger.debug("Filtering KnowledgeGraph with %s", self.filter_nodes.__name__)     filtered_nodes = [node for node in kg.nodes if self.filter_nodes(node)]     node_ids = {node.id for node in filtered_nodes}     filtered_relationships = [         rel         for rel in kg.relationships         if (rel.source.id in node_ids) and (rel.target.id in node_ids)     ]     logger.debug(         "Filter reduced KnowledgeGraph by %d/%d nodes and %d/%d relationships",         len(kg.nodes) - len(filtered_nodes),         len(kg.nodes),         len(kg.relationships) - len(filtered_relationships),         len(kg.relationships),     )     return KnowledgeGraph(         nodes=filtered_nodes,         relationships=filtered_relationships,     ) ``` |

### generate\_execution\_plan `abstractmethod`

```
generate_execution_plan(kg: KnowledgeGraph) -> Sequence[Coroutine]
```

Generates a sequence of coroutines to be executed in sequence by the Executor. This
coroutine will, upon execution, write the transformation into the KnowledgeGraph.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Sequence[Coroutine]` | A sequence of coroutines to be executed in parallel. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 ``` | ``` @abstractmethod def generate_execution_plan(self, kg: KnowledgeGraph) -> t.Sequence[t.Coroutine]:     """     Generates a sequence of coroutines to be executed in sequence by the Executor. This     coroutine will, upon execution, write the transformation into the KnowledgeGraph.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.Sequence[t.Coroutine]         A sequence of coroutines to be executed in parallel.     """     pass ``` |

## Extractor `dataclass`

```
Extractor(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)())
```

Bases: `BaseGraphTransformation`

Abstract base class for extractors that transform a KnowledgeGraph by extracting
specific properties from its nodes.

Methods:

| Name | Description |
| --- | --- |
| `transform` | Transforms the KnowledgeGraph by extracting properties from its nodes. |
| `extract` | Abstract method to extract a specific property from a node. |

### transform `async`

```
transform(kg: KnowledgeGraph) -> List[Tuple[Node, Tuple[str, Any]]]
```

Transforms the KnowledgeGraph by extracting properties from its nodes. Uses
the `filter` method to filter the graph and the `extract` method to extract
properties from each node.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `List[Tuple[Node, Tuple[str, Any]]]` | A list of tuples where each tuple contains a node and the extracted property. |

Examples:

```
>>> kg = KnowledgeGraph(nodes=[Node(id=1, properties={"name": "Node1"}), Node(id=2, properties={"name": "Node2"})])
>>> extractor = SomeConcreteExtractor()
>>> extractor.transform(kg)
[(Node(id=1, properties={"name": "Node1"}), ("property_name", "extracted_value")),
 (Node(id=2, properties={"name": "Node2"}), ("property_name", "extracted_value"))]
```

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 ``` | ``` async def transform(     self, kg: KnowledgeGraph ) -> t.List[t.Tuple[Node, t.Tuple[str, t.Any]]]:     """     Transforms the KnowledgeGraph by extracting properties from its nodes. Uses     the `filter` method to filter the graph and the `extract` method to extract     properties from each node.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.List[t.Tuple[Node, t.Tuple[str, t.Any]]]         A list of tuples where each tuple contains a node and the extracted         property.      Examples     --------     >>> kg = KnowledgeGraph(nodes=[Node(id=1, properties={"name": "Node1"}), Node(id=2, properties={"name": "Node2"})])     >>> extractor = SomeConcreteExtractor()     >>> extractor.transform(kg)     [(Node(id=1, properties={"name": "Node1"}), ("property_name", "extracted_value")),      (Node(id=2, properties={"name": "Node2"}), ("property_name", "extracted_value"))]     """     filtered = self.filter(kg)     return [(node, await self.extract(node)) for node in filtered.nodes] ``` |

### extract `abstractmethod` `async`

```
extract(node: Node) -> Tuple[str, Any]
```

Abstract method to extract a specific property from a node.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `node` | `Node` | The node from which to extract the property. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Tuple[str, Any]` | A tuple containing the property name and the extracted value. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 ``` | ``` @abstractmethod async def extract(self, node: Node) -> t.Tuple[str, t.Any]:     """     Abstract method to extract a specific property from a node.      Parameters     ----------     node : Node         The node from which to extract the property.      Returns     -------     t.Tuple[str, t.Any]         A tuple containing the property name and the extracted value.     """     pass ``` |

### generate\_execution\_plan

```
generate_execution_plan(kg: KnowledgeGraph) -> Sequence[Coroutine]
```

Generates a sequence of coroutines to be executed in parallel by the Executor.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Sequence[Coroutine]` | A sequence of coroutines to be executed in parallel. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 ``` | ``` def generate_execution_plan(self, kg: KnowledgeGraph) -> t.Sequence[t.Coroutine]:     """     Generates a sequence of coroutines to be executed in parallel by the Executor.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.Sequence[t.Coroutine]         A sequence of coroutines to be executed in parallel.     """      async def apply_extract(node: Node):         property_name, property_value = await self.extract(node)         if node.get_property(property_name) is None:             node.add_property(property_name, property_value)         else:             logger.warning(                 "Property '%s' already exists in node '%.6s'. Skipping!",                 property_name,                 node.id,             )      filtered = self.filter(kg)     plan = [apply_extract(node) for node in filtered.nodes]     logger.debug(         "Created %d coroutines for %s",         len(plan),         self.__class__.__name__,     )     return plan ``` |

## NodeFilter `dataclass`

```
NodeFilter(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)())
```

Bases: `BaseGraphTransformation`

### custom\_filter `abstractmethod` `async`

```
custom_filter(node: Node, kg: KnowledgeGraph) -> bool
```

Abstract method to filter a node based on a prompt.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `node` | `Node` | The node to be filtered. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `bool` | A boolean indicating whether the node should be filtered. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 ``` | ``` @abstractmethod async def custom_filter(self, node: Node, kg: KnowledgeGraph) -> bool:     """     Abstract method to filter a node based on a prompt.      Parameters     ----------     node : Node         The node to be filtered.      Returns     -------     bool         A boolean indicating whether the node should be filtered.     """     pass ``` |

### generate\_execution\_plan

```
generate_execution_plan(kg: KnowledgeGraph) -> Sequence[Coroutine]
```

Generates a sequence of coroutines to be executed

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 ``` | ``` def generate_execution_plan(self, kg: KnowledgeGraph) -> t.Sequence[t.Coroutine]:     """     Generates a sequence of coroutines to be executed     """      async def apply_filter(node: Node):         if await self.custom_filter(node, kg):             kg.remove_node(node)      filtered = self.filter(kg)     plan = [apply_filter(node) for node in filtered.nodes]     logger.debug(         "Created %d coroutines for %s",         len(plan),         self.__class__.__name__,     )     return plan ``` |

## RelationshipBuilder `dataclass`

```
RelationshipBuilder(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)())
```

Bases: `BaseGraphTransformation`

Abstract base class for building relationships in a KnowledgeGraph.

Methods:

| Name | Description |
| --- | --- |
| `transform` | Transforms the KnowledgeGraph by building relationships. |

### transform `abstractmethod` `async`

```
transform(kg: KnowledgeGraph) -> List[Relationship]
```

Transforms the KnowledgeGraph by building relationships.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `List[Relationship]` | A list of new relationships. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 ``` | ``` @abstractmethod async def transform(self, kg: KnowledgeGraph) -> t.List[Relationship]:     """     Transforms the KnowledgeGraph by building relationships.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.List[Relationship]         A list of new relationships.     """     pass ``` |

### generate\_execution\_plan

```
generate_execution_plan(kg: KnowledgeGraph) -> Sequence[Coroutine]
```

Generates a sequence of coroutines to be executed in parallel by the Executor.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Sequence[Coroutine]` | A sequence of coroutines to be executed in parallel. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 ``` | ``` def generate_execution_plan(self, kg: KnowledgeGraph) -> t.Sequence[t.Coroutine]:     """     Generates a sequence of coroutines to be executed in parallel by the Executor.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.Sequence[t.Coroutine]         A sequence of coroutines to be executed in parallel.     """      async def apply_build_relationships(         filtered_kg: KnowledgeGraph, original_kg: KnowledgeGraph     ):         relationships = await self.transform(filtered_kg)         original_kg.relationships.extend(relationships)      filtered_kg = self.filter(kg)     plan = [apply_build_relationships(filtered_kg=filtered_kg, original_kg=kg)]     logger.debug(         "Created %d coroutines for %s",         len(plan),         self.__class__.__name__,     )     return plan ``` |

## Splitter `dataclass`

```
Splitter(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)())
```

Bases: `BaseGraphTransformation`

Abstract base class for splitters that transform a KnowledgeGraph by splitting
its nodes into smaller chunks.

Methods:

| Name | Description |
| --- | --- |
| `transform` | Transforms the KnowledgeGraph by splitting its nodes into smaller chunks. |
| `split` | Abstract method to split a node into smaller chunks. |

### transform `async`

```
transform(kg: KnowledgeGraph) -> Tuple[List[Node], List[Relationship]]
```

Transforms the KnowledgeGraph by splitting its nodes into smaller chunks.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Tuple[List[Node], List[Relationship]]` | A tuple containing a list of new nodes and a list of new relationships. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 ``` | ``` async def transform(     self, kg: KnowledgeGraph ) -> t.Tuple[t.List[Node], t.List[Relationship]]:     """     Transforms the KnowledgeGraph by splitting its nodes into smaller chunks.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.Tuple[t.List[Node], t.List[Relationship]]         A tuple containing a list of new nodes and a list of new relationships.     """     filtered = self.filter(kg)      all_nodes = []     all_relationships = []     for node in filtered.nodes:         nodes, relationships = await self.split(node)         all_nodes.extend(nodes)         all_relationships.extend(relationships)      return all_nodes, all_relationships ``` |

### split `abstractmethod` `async`

```
split(node: Node) -> Tuple[List[Node], List[Relationship]]
```

Abstract method to split a node into smaller chunks.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `node` | `Node` | The node to be split. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Tuple[List[Node], List[Relationship]]` | A tuple containing a list of new nodes and a list of new relationships. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 ``` | ``` @abstractmethod async def split(self, node: Node) -> t.Tuple[t.List[Node], t.List[Relationship]]:     """     Abstract method to split a node into smaller chunks.      Parameters     ----------     node : Node         The node to be split.      Returns     -------     t.Tuple[t.List[Node], t.List[Relationship]]         A tuple containing a list of new nodes and a list of new relationships.     """     pass ``` |

### generate\_execution\_plan

```
generate_execution_plan(kg: KnowledgeGraph) -> Sequence[Coroutine]
```

Generates a sequence of coroutines to be executed in parallel by the Executor.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `kg` | `KnowledgeGraph` | The knowledge graph to be transformed. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Sequence[Coroutine]` | A sequence of coroutines to be executed in parallel. |

Source code in `src/ragas/testset/transforms/base.py`

|  |  |
| --- | --- |
| ``` 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 ``` | ``` def generate_execution_plan(self, kg: KnowledgeGraph) -> t.Sequence[t.Coroutine]:     """     Generates a sequence of coroutines to be executed in parallel by the Executor.      Parameters     ----------     kg : KnowledgeGraph         The knowledge graph to be transformed.      Returns     -------     t.Sequence[t.Coroutine]         A sequence of coroutines to be executed in parallel.     """      async def apply_split(node: Node):         nodes, relationships = await self.split(node)         kg.nodes.extend(nodes)         kg.relationships.extend(relationships)      filtered = self.filter(kg)     plan = [apply_split(node) for node in filtered.nodes]     logger.debug(         "Created %d coroutines for %s",         len(plan),         self.__class__.__name__,     )     return plan ``` |

## Parallel

```
Parallel(*transformations: Union[BaseGraphTransformation, 'Parallel'])
```

Collection of transformations to be applied in parallel.

Examples:

```
>>> Parallel(HeadlinesExtractor(), SummaryExtractor())
```

Source code in `src/ragas/testset/transforms/engine.py`

|  |  |
| --- | --- |
| ``` 32 33 ``` | ``` def __init__(self, *transformations: t.Union[BaseGraphTransformation, "Parallel"]):     self.transformations = list(transformations) ``` |

## EmbeddingExtractor `dataclass`

```
EmbeddingExtractor(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), property_name: str = 'embedding', embed_property_name: str = 'page_content', embedding_model: Union[BaseRagasEmbeddings, BaseRagasEmbedding] = embedding_factory())
```

Bases: `Extractor`

A class for extracting embeddings from nodes in a knowledge graph.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `property_name` | `str` | The name of the property to store the embedding |
| `embed_property_name` | `str` | The name of the property containing the text to embed |
| `embedding_model` | `BaseRagasEmbeddings or BaseRagasEmbedding` | The embedding model used for generating embeddings |

### extract `async`

```
extract(node: Node) -> Tuple[str, Any]
```

Extracts the embedding for a given node.

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the property to be embedded is not a string. |

Source code in `src/ragas/testset/transforms/extractors/embeddings.py`

|  |  |
| --- | --- |
| ``` 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 ``` | ``` async def extract(self, node: Node) -> t.Tuple[str, t.Any]:     """     Extracts the embedding for a given node.      Raises     ------     ValueError         If the property to be embedded is not a string.     """     text = node.get_property(self.embed_property_name)     if not isinstance(text, str):         raise ValueError(             f"node.property('{self.embed_property_name}') must be a string, found '{type(text)}'"         )      # Handle both modern (BaseRagasEmbedding) and legacy (BaseRagasEmbeddings) interfaces     if hasattr(self.embedding_model, "aembed_text"):         # Modern interface (BaseRagasEmbedding)         # Check if the client supports async operations by checking if is_async exists and is True         if hasattr(self.embedding_model, "is_async") and getattr(             self.embedding_model, "is_async", False         ):             embedding = await self.embedding_model.aembed_text(text)  # type: ignore[attr-defined]         else:             # For sync clients, use the sync method wrapped in thread executor to avoid blocking             warnings.warn(                 f"Using sync embedding model {self.embedding_model.__class__.__name__} "                 f"in async context. This may impact performance. "                 f"Consider using an async-compatible embedding model for better performance.",                 UserWarning,                 stacklevel=2,             )             embedding = await run_sync_in_async(                 self.embedding_model.embed_text, text             )  # type: ignore[attr-defined]     else:         # Legacy interface (BaseRagasEmbeddings)         embedding = await self.embedding_model.embed_text(text)  # type: ignore[misc]      return self.property_name, embedding ``` |

## HeadlinesExtractor `dataclass`

```
HeadlinesExtractor(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), llm: Union[BaseRagasLLM, InstructorBaseRagasLLM] = _default_llm_factory(), merge_if_possible: bool = True, max_token_limit: int = 32000, tokenizer: BaseTokenizer = (lambda: DEFAULT_TOKENIZER)(), property_name: str = 'headlines', prompt: HeadlinesExtractorPrompt = HeadlinesExtractorPrompt(), max_num: int = 5)
```

Bases: `LLMBasedExtractor`

Extracts the headlines from the given text.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `property_name` | `str` | The name of the property to extract. |
| `prompt` | `HeadlinesExtractorPrompt` | The prompt used for extraction. |

## KeyphrasesExtractor `dataclass`

```
KeyphrasesExtractor(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), llm: Union[BaseRagasLLM, InstructorBaseRagasLLM] = _default_llm_factory(), merge_if_possible: bool = True, max_token_limit: int = 32000, tokenizer: BaseTokenizer = (lambda: DEFAULT_TOKENIZER)(), property_name: str = 'keyphrases', prompt: KeyphrasesExtractorPrompt = KeyphrasesExtractorPrompt(), max_num: int = 5)
```

Bases: `LLMBasedExtractor`

Extracts top keyphrases from the given text.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `property_name` | `str` | The name of the property to extract. |
| `prompt` | `KeyphrasesExtractorPrompt` | The prompt used for extraction. |

## SummaryExtractor `dataclass`

```
SummaryExtractor(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), llm: Union[BaseRagasLLM, InstructorBaseRagasLLM] = _default_llm_factory(), merge_if_possible: bool = True, max_token_limit: int = 32000, tokenizer: BaseTokenizer = (lambda: DEFAULT_TOKENIZER)(), property_name: str = 'summary', prompt: SummaryExtractorPrompt = SummaryExtractorPrompt())
```

Bases: `LLMBasedExtractor`

Extracts a summary from the given text.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `property_name` | `str` | The name of the property to extract. |
| `prompt` | `SummaryExtractorPrompt` | The prompt used for extraction. |

## TitleExtractor `dataclass`

```
TitleExtractor(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), llm: Union[BaseRagasLLM, InstructorBaseRagasLLM] = _default_llm_factory(), merge_if_possible: bool = True, max_token_limit: int = 32000, tokenizer: BaseTokenizer = (lambda: DEFAULT_TOKENIZER)(), property_name: str = 'title', prompt: TitleExtractorPrompt = TitleExtractorPrompt())
```

Bases: `LLMBasedExtractor`

Extracts the title from the given text.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `property_name` | `str` | The name of the property to extract. |
| `prompt` | `TitleExtractorPrompt` | The prompt used for extraction. |

## CustomNodeFilter `dataclass`

```
CustomNodeFilter(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), llm: Union[BaseRagasLLM, InstructorBaseRagasLLM] = _default_llm_factory(), scoring_prompt: PydanticPrompt = QuestionPotentialPrompt(), min_score: int = 2, rubrics: Dict[str, str] = (lambda: DEFAULT_RUBRICS)())
```

Bases: `LLMBasedNodeFilter`

returns True if the score is less than min\_score

## CosineSimilarityBuilder `dataclass`

```
CosineSimilarityBuilder(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), property_name: str = 'embedding', new_property_name: str = 'cosine_similarity', threshold: float = 0.9, block_size: int = 1024)
```

Bases: `RelationshipBuilder`

### generate\_execution\_plan

```
generate_execution_plan(kg: KnowledgeGraph) -> List[Coroutine]
```

Generates a coroutine task for finding similar embedding pairs, which can be scheduled/executed by an Executor.

Source code in `src/ragas/testset/transforms/relationship_builders/cosine.py`

|  |  |
| --- | --- |
| ```  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 ``` | ``` def generate_execution_plan(self, kg: KnowledgeGraph) -> t.List[t.Coroutine]:     """     Generates a coroutine task for finding similar embedding pairs, which can be scheduled/executed by an Executor.     """     filtered_kg = self.filter(kg)      embeddings = []     for node in filtered_kg.nodes:         embedding = node.get_property(self.property_name)         if embedding is None:             raise ValueError(f"Node {node.id} has no {self.property_name}")         embeddings.append(embedding)     self._validate_embedding_shapes(embeddings)      async def find_and_add_relationships():         similar_pairs = self._find_similar_embedding_pairs(             np.array(embeddings), self.threshold         )         for i, j, similarity_float in similar_pairs:             rel = Relationship(                 source=filtered_kg.nodes[i],                 target=filtered_kg.nodes[j],                 type=self.new_property_name,                 properties={self.new_property_name: similarity_float},                 bidirectional=True,             )             kg.relationships.append(rel)      return [find_and_add_relationships()] ``` |

## SummaryCosineSimilarityBuilder `dataclass`

```
SummaryCosineSimilarityBuilder(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), property_name: str = 'summary_embedding', new_property_name: str = 'summary_cosine_similarity', threshold: float = 0.1, block_size: int = 1024)
```

Bases: `CosineSimilarityBuilder`

## JaccardSimilarityBuilder `dataclass`

```
JaccardSimilarityBuilder(name: str = '', filter_nodes: Callable[[Node], bool] = (lambda: default_filter)(), property_name: str = 'entities', key_name: Optional[str] = None, new_property_name: str = 'jaccard_similarity', threshold: float = 0.5)
```

Bases: `RelationshipBuilder`

### generate\_execution\_plan

```
generate_execution_plan(kg: KnowledgeGraph) -> List[Coroutine]
```

Generates a coroutine task for finding similar pairs, which can be scheduled/executed by an Executor.

Source code in `src/ragas/testset/transforms/relationship_builders/traditional.py`

|  |  |
| --- | --- |
| ``` 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 ``` | ``` def generate_execution_plan(self, kg: KnowledgeGraph) -> t.List[t.Coroutine]:     """     Generates a coroutine task for finding similar pairs, which can be scheduled/executed by an Executor.     """      async def find_and_add_relationships():         similar_pairs = self._find_similar_embedding_pairs(kg)         for i, j, similarity_float in similar_pairs:             rel = Relationship(                 source=kg.nodes[i],                 target=kg.nodes[j],                 type=self.new_property_name,                 properties={self.new_property_name: similarity_float},                 bidirectional=True,             )             kg.relationships.append(rel)      return [find_and_add_relationships()] ``` |

## default\_transforms

```
default_transforms(documents: List[Document], llm: Union[BaseRagasLLM, 'InstructorBaseRagasLLM'], embedding_model: BaseRagasEmbeddings) -> 'Transforms'
```

Creates and returns a default set of transforms for processing a knowledge graph.

This function defines a series of transformation steps to be applied to a
knowledge graph, including extracting summaries, keyphrases, titles,
headlines, and embeddings, as well as building similarity relationships
between nodes.

Returns:

| Type | Description |
| --- | --- |
| `Transforms` | A list of transformation steps to be applied to the knowledge graph. |

Source code in `src/ragas/testset/transforms/default.py`

|  |  |
| --- | --- |
| ```  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 ``` | ``` def default_transforms(     documents: t.List[LCDocument],     llm: t.Union[BaseRagasLLM, "InstructorBaseRagasLLM"],     embedding_model: BaseRagasEmbeddings, ) -> "Transforms":     """     Creates and returns a default set of transforms for processing a knowledge graph.      This function defines a series of transformation steps to be applied to a     knowledge graph, including extracting summaries, keyphrases, titles,     headlines, and embeddings, as well as building similarity relationships     between nodes.        Returns     -------     Transforms         A list of transformation steps to be applied to the knowledge graph.      """      def count_doc_length_bins(documents, bin_ranges):         data = [num_tokens_from_string(doc.page_content) for doc in documents]         bins = {f"{start}-{end}": 0 for start, end in bin_ranges}          for num in data:             for start, end in bin_ranges:                 if start <= num <= end:                     bins[f"{start}-{end}"] += 1                     break  # Move to the next number once it’s placed in a bin          return bins      def filter_doc_with_num_tokens(node, min_num_tokens=500):         return (             node.type == NodeType.DOCUMENT             and num_tokens_from_string(node.properties["page_content"]) > min_num_tokens         )      def filter_docs(node):         return node.type == NodeType.DOCUMENT      def filter_chunks(node):         return node.type == NodeType.CHUNK      bin_ranges = [(0, 100), (101, 500), (501, float("inf"))]     result = count_doc_length_bins(documents, bin_ranges)     result = {k: v / len(documents) for k, v in result.items()}      transforms = []      if result["501-inf"] >= 0.25:         headline_extractor = HeadlinesExtractor(             llm=llm, filter_nodes=lambda node: filter_doc_with_num_tokens(node)         )         splitter = HeadlineSplitter(min_tokens=500)         summary_extractor = SummaryExtractor(             llm=llm, filter_nodes=lambda node: filter_doc_with_num_tokens(node)         )          theme_extractor = ThemesExtractor(             llm=llm, filter_nodes=lambda node: filter_chunks(node)         )         ner_extractor = NERExtractor(             llm=llm, filter_nodes=lambda node: filter_chunks(node)         )          summary_emb_extractor = EmbeddingExtractor(             embedding_model=embedding_model,             property_name="summary_embedding",             embed_property_name="summary",             filter_nodes=lambda node: filter_doc_with_num_tokens(node),         )          cosine_sim_builder = CosineSimilarityBuilder(             property_name="summary_embedding",             new_property_name="summary_similarity",             threshold=0.7,             filter_nodes=lambda node: filter_doc_with_num_tokens(node),         )          ner_overlap_sim = OverlapScoreBuilder(             threshold=0.01, filter_nodes=lambda node: filter_chunks(node)         )          node_filter = CustomNodeFilter(             llm=llm, filter_nodes=lambda node: filter_chunks(node)         )         transforms = [             headline_extractor,             splitter,             summary_extractor,             node_filter,             Parallel(summary_emb_extractor, theme_extractor, ner_extractor),             Parallel(cosine_sim_builder, ner_overlap_sim),         ]     elif result["101-500"] >= 0.25:         summary_extractor = SummaryExtractor(             llm=llm, filter_nodes=lambda node: filter_doc_with_num_tokens(node, 100)         )         summary_emb_extractor = EmbeddingExtractor(             embedding_model=embedding_model,             property_name="summary_embedding",             embed_property_name="summary",             filter_nodes=lambda node: filter_doc_with_num_tokens(node, 100),         )          cosine_sim_builder = CosineSimilarityBuilder(             property_name="summary_embedding",             new_property_name="summary_similarity",             threshold=0.5,             filter_nodes=lambda node: filter_doc_with_num_tokens(node, 100),         )          ner_extractor = NERExtractor(llm=llm)         ner_overlap_sim = OverlapScoreBuilder(threshold=0.01)         theme_extractor = ThemesExtractor(             llm=llm, filter_nodes=lambda node: filter_docs(node)         )         node_filter = CustomNodeFilter(llm=llm)          transforms = [             summary_extractor,             node_filter,             Parallel(summary_emb_extractor, theme_extractor, ner_extractor),             Parallel(cosine_sim_builder, ner_overlap_sim),         ]     else:         raise ValueError(             "Documents appears to be too short (ie 100 tokens or less). Please provide longer documents."         )      return transforms ``` |

## default\_transforms\_for\_prechunked

```
default_transforms_for_prechunked(llm: Union[BaseRagasLLM, 'InstructorBaseRagasLLM'], embedding_model: BaseRagasEmbeddings) -> 'Transforms'
```

Creates and returns a default set of transforms for processing a knowledge graph
containing pre-chunked documents.

This ignores the splitting step and directly applies extractors and relationship builders
to the chunks.

Source code in `src/ragas/testset/transforms/default.py`

|  |  |
| --- | --- |
| ``` 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 ``` | ``` def default_transforms_for_prechunked(     llm: t.Union[BaseRagasLLM, "InstructorBaseRagasLLM"],     embedding_model: BaseRagasEmbeddings, ) -> "Transforms":     """     Creates and returns a default set of transforms for processing a knowledge graph     containing pre-chunked documents.      This ignores the splitting step and directly applies extractors and relationship builders     to the chunks.     """      def filter_chunks(node):         return node.type == NodeType.CHUNK      summary_extractor = SummaryExtractor(llm=llm, filter_nodes=filter_chunks)     summary_emb_extractor = EmbeddingExtractor(         embedding_model=embedding_model,         property_name="summary_embedding",         embed_property_name="summary",         filter_nodes=filter_chunks,     )      theme_extractor = ThemesExtractor(llm=llm, filter_nodes=filter_chunks)     ner_extractor = NERExtractor(llm=llm, filter_nodes=filter_chunks)      cosine_sim_builder = CosineSimilarityBuilder(         property_name="summary_embedding",         new_property_name="summary_similarity",         threshold=0.7,         filter_nodes=filter_chunks,     )      ner_overlap_sim = OverlapScoreBuilder(threshold=0.01, filter_nodes=filter_chunks)      node_filter = CustomNodeFilter(llm=llm, filter_nodes=filter_chunks)      return [         summary_extractor,         node_filter,         Parallel(summary_emb_extractor, theme_extractor, ner_extractor),         Parallel(cosine_sim_builder, ner_overlap_sim),     ] ``` |

## apply\_transforms

```
apply_transforms(kg: KnowledgeGraph, transforms: Transforms, run_config: RunConfig = RunConfig(), callbacks: Optional[Callbacks] = None)
```

Recursively apply transformations to a knowledge graph in place.

Source code in `src/ragas/testset/transforms/engine.py`

|  |  |
| --- | --- |
| ``` 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 ``` | ``` def apply_transforms(     kg: KnowledgeGraph,     transforms: Transforms,     run_config: RunConfig = RunConfig(),     callbacks: t.Optional[Callbacks] = None, ):     """     Recursively apply transformations to a knowledge graph in place.     """     # apply nest_asyncio to fix the event loop issue in jupyter     apply_nest_asyncio()      max_workers = getattr(run_config, "max_workers", -1)      if isinstance(transforms, t.Sequence):         for transform in transforms:             apply_transforms(kg, transform, run_config, callbacks)     elif isinstance(transforms, Parallel):         apply_transforms(kg, transforms.transformations, run_config, callbacks)     elif isinstance(transforms, BaseGraphTransformation):         logger.debug(             f"Generating execution plan for transformation {transforms.__class__.__name__}"         )         coros = transforms.generate_execution_plan(kg)         desc = get_desc(transforms)         run_async_tasks(             coros,             batch_size=None,             show_progress=True,             progress_bar_desc=desc,             max_workers=max_workers,         )     else:         raise ValueError(             f"Invalid transforms type: {type(transforms)}. Expects a sequence of BaseGraphTransformations or a Parallel instance."         )     logger.debug("All transformations applied successfully.") ``` |

## rollback\_transforms

```
rollback_transforms(kg: KnowledgeGraph, transforms: Transforms)
```

Rollback a sequence of transformations from a knowledge graph.

Note

This is not yet implemented. Please open an issue if you need this feature.


Source code in `src/ragas/testset/transforms/engine.py`

|  |  |
| --- | --- |
| ```  93  94  95  96  97  98  99 100 101 102 ``` | ``` def rollback_transforms(kg: KnowledgeGraph, transforms: Transforms):     """     Rollback a sequence of transformations from a knowledge graph.      Note     ----     This is not yet implemented. Please open an issue if you need this feature.     """     # this will allow you to roll back the transformations     raise NotImplementedError ``` |

November 28, 2025




November 28, 2025

Back to top