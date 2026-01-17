Synthesizers - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.testset.synthesizers)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Synthesizers

## BaseSynthesizer `dataclass`

```
BaseSynthesizer(name: str = '', llm: Union[BaseRagasLLM, 'InstructorBaseRagasLLM'] = _default_llm_factory(), llm_context: Optional[str] = None)
```

Bases: `ABC`, `Generic[Scenario]`, `PromptMixin`

Base class for synthesizing scenarios and samples.

## default\_query\_distribution

```
default_query_distribution(llm: Union[BaseRagasLLM, InstructorBaseRagasLLM], kg: Optional[KnowledgeGraph] = None, llm_context: Optional[str] = None) -> QueryDistribution
```

Source code in `src/ragas/testset/synthesizers/__init__.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 ``` | ``` def default_query_distribution(     llm: t.Union[BaseRagasLLM, "InstructorBaseRagasLLM"],     kg: t.Optional[KnowledgeGraph] = None,     llm_context: t.Optional[str] = None, ) -> QueryDistribution:     """ """     default_queries = [         SingleHopSpecificQuerySynthesizer(llm=llm, llm_context=llm_context),         MultiHopAbstractQuerySynthesizer(llm=llm, llm_context=llm_context),         MultiHopSpecificQuerySynthesizer(llm=llm, llm_context=llm_context),     ]     if kg is not None:         available_queries = []         for query in default_queries:             try:                 if query.get_node_clusters(kg):                     available_queries.append(query)             except Exception as e:                 # Keep broad catch minimal for resilience; log and skip.                 logger.warning(                     "Skipping %s due to unexpected error: %s",                     getattr(query, "name", type(query).__name__),                     e,                 )                 continue         if not available_queries:             raise ValueError(                 "No compatible query synthesizers for the provided KnowledgeGraph."             )     else:         available_queries = default_queries      return [(query, 1 / len(available_queries)) for query in available_queries] ``` |

November 28, 2025




November 28, 2025

Back to top