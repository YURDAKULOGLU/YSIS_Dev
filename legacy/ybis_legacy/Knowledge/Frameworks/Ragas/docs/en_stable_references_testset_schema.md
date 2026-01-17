Schemas - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.testset.synthesizers.testset_schema)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Schemas

## TestsetSample

Bases: `BaseSample`

Represents a sample in a test set.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `eval_sample` | `Union[SingleTurnSample, MultiTurnSample]` | The evaluation sample, which can be either a single-turn or multi-turn sample. |
| `synthesizer_name` | `str` | The name of the synthesizer used to generate this sample. |

## TestsetPacket

Bases: `BaseModel`

A packet of testset samples to be uploaded to the server.

## Testset `dataclass`

```
Testset(samples: List[TestsetSample], run_id: str = (lambda: str(uuid4()))(), cost_cb: Optional[CostCallbackHandler] = None)
```

Bases: `RagasDataset[TestsetSample]`

Represents a test set containing multiple test samples.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `samples` | `List[TestsetSample]` | A list of TestsetSample objects representing the samples in the test set. |

### to\_evaluation\_dataset

```
to_evaluation_dataset() -> EvaluationDataset
```

Converts the Testset to an EvaluationDataset.

Source code in `src/ragas/testset/synthesizers/testset_schema.py`

|  |  |
| --- | --- |
| ``` 61 62 63 64 65 66 67 ``` | ``` def to_evaluation_dataset(self) -> EvaluationDataset:     """     Converts the Testset to an EvaluationDataset.     """     return EvaluationDataset(         samples=[sample.eval_sample for sample in self.samples]     ) ``` |

### to\_list

```
to_list() -> List[Dict]
```

Converts the Testset to a list of dictionaries.

Source code in `src/ragas/testset/synthesizers/testset_schema.py`

|  |  |
| --- | --- |
| ``` 69 70 71 72 73 74 75 76 77 78 ``` | ``` def to_list(self) -> t.List[t.Dict]:     """     Converts the Testset to a list of dictionaries.     """     list_dict = []     for sample in self.samples:         sample_dict = sample.eval_sample.model_dump(exclude_none=True)         sample_dict["synthesizer_name"] = sample.synthesizer_name         list_dict.append(sample_dict)     return list_dict ``` |

### from\_list `classmethod`

```
from_list(data: List[Dict]) -> Testset
```

Converts a list of dictionaries to a Testset.

Source code in `src/ragas/testset/synthesizers/testset_schema.py`

|  |  |
| --- | --- |
| ```  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 ``` | ``` @classmethod def from_list(cls, data: t.List[t.Dict]) -> Testset:     """     Converts a list of dictionaries to a Testset.     """     # first create the samples     samples = []     for sample in data:         synthesizer_name = sample["synthesizer_name"]         # remove the synthesizer name from the sample         sample.pop("synthesizer_name")         # the remaining sample is the eval_sample         eval_sample = sample          # if user_input is a list it is MultiTurnSample         if "user_input" in eval_sample and not isinstance(             eval_sample.get("user_input"), list         ):             eval_sample = SingleTurnSample(**eval_sample)         else:             eval_sample = MultiTurnSample(**eval_sample)          samples.append(             TestsetSample(                 eval_sample=eval_sample, synthesizer_name=synthesizer_name             )         )     # then create the testset     return Testset(samples=samples) ``` |

### total\_tokens

```
total_tokens() -> Union[List[TokenUsage], TokenUsage]
```

Compute the total tokens used in the evaluation.

Source code in `src/ragas/testset/synthesizers/testset_schema.py`

|  |  |
| --- | --- |
| ``` 110 111 112 113 114 115 116 117 118 ``` | ``` def total_tokens(self) -> t.Union[t.List[TokenUsage], TokenUsage]:     """     Compute the total tokens used in the evaluation.     """     if self.cost_cb is None:         raise ValueError(             "The Testset was not configured for computing cost. Please provide a token_usage_parser function to TestsetGenerator to compute cost."         )     return self.cost_cb.total_tokens() ``` |

### total\_cost

```
total_cost(cost_per_input_token: Optional[float] = None, cost_per_output_token: Optional[float] = None) -> float
```

Compute the total cost of the evaluation.

Source code in `src/ragas/testset/synthesizers/testset_schema.py`

|  |  |
| --- | --- |
| ``` 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 ``` | ``` def total_cost(     self,     cost_per_input_token: t.Optional[float] = None,     cost_per_output_token: t.Optional[float] = None, ) -> float:     """     Compute the total cost of the evaluation.     """     if self.cost_cb is None:         raise ValueError(             "The Testset was not configured for computing cost. Please provide a token_usage_parser function to TestsetGenerator to compute cost."         )     return self.cost_cb.total_cost(         cost_per_input_token=cost_per_input_token,         cost_per_output_token=cost_per_output_token,     ) ``` |

### from\_annotated `classmethod`

```
from_annotated(path: str) -> Testset
```

Loads a testset from an annotated JSON file.

Source code in `src/ragas/testset/synthesizers/testset_schema.py`

|  |  |
| --- | --- |
| ``` 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 ``` | ``` @classmethod def from_annotated(cls, path: str) -> Testset:     """     Loads a testset from an annotated JSON file.     """     import json      with open(path, "r") as f:         annotated_testset = json.load(f)      samples = []     for sample in annotated_testset:         if sample["approval_status"] == "approved":             samples.append(TestsetSample(**sample))     return cls(samples=samples) ``` |

## QueryLength

Bases: `str`, `Enum`

Enumeration of query lengths. Available options are: LONG, MEDIUM, SHORT

## QueryStyle

Bases: `str`, `Enum`

Enumeration of query styles. Available options are: MISSPELLED, PERFECT\_GRAMMAR, POOR\_GRAMMAR, WEB\_SEARCH\_LIKE

## BaseScenario

Bases: `BaseModel`

Base class for representing a scenario for generating test samples.

Attributes:

| Name | Type | Description |
| --- | --- | --- |
| `nodes` | `List[Node]` | List of nodes involved in the scenario. |
| `style` | `QueryStyle` | The style of the query. |
| `length` | `QueryLength` | The length of the query. |
| `persona` | `Persona` | A persona associated with the scenario. |

## SingleHopSpecificQuerySynthesizer `dataclass`

```
SingleHopSpecificQuerySynthesizer(name: str = 'single_hop_specific_query_synthesizer', llm: Union[BaseRagasLLM, 'InstructorBaseRagasLLM'] = _default_llm_factory(), llm_context: Optional[str] = None, generate_query_reference_prompt: PydanticPrompt = QueryAnswerGenerationPrompt(), theme_persona_matching_prompt: PydanticPrompt = ThemesPersonasMatchingPrompt(), property_name: str = 'entities')
```

Bases: `SingleHopQuerySynthesizer`

## MultiHopSpecificQuerySynthesizer `dataclass`

```
MultiHopSpecificQuerySynthesizer(name: str = 'multi_hop_specific_query_synthesizer', llm: Union[BaseRagasLLM, 'InstructorBaseRagasLLM'] = _default_llm_factory(), llm_context: Optional[str] = None, generate_query_reference_prompt: PydanticPrompt = QueryAnswerGenerationPrompt(), property_name: str = 'entities', relation_type: str = 'entities_overlap', relation_overlap_property: str = 'overlapped_items', theme_persona_matching_prompt: PydanticPrompt = ThemesPersonasMatchingPrompt())
```

Bases: `MultiHopQuerySynthesizer`

Synthesize multi-hop queries based on a chunk cluster defined by entity overlap.

### get\_node\_clusters

```
get_node_clusters(knowledge_graph: KnowledgeGraph) -> List[Tuple]
```

Identify clusters of nodes based on the specified relationship condition.

Source code in `src/ragas/testset/synthesizers/multi_hop/specific.py`

|  |  |
| --- | --- |
| ``` 40 41 42 43 44 45 46 ``` | ``` def get_node_clusters(self, knowledge_graph: KnowledgeGraph) -> t.List[t.Tuple]:     """Identify clusters of nodes based on the specified relationship condition."""     node_clusters = knowledge_graph.find_two_nodes_single_rel(         relationship_condition=lambda rel: rel.type == self.relation_type     )     logger.info("found %d clusters", len(node_clusters))     return node_clusters ``` |

November 28, 2025




November 28, 2025

Back to top