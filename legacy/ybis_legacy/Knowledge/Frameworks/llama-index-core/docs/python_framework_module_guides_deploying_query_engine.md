 Query Engine | LlamaIndex Python Documentation
  [Skip to content](#_top)

# Query Engine

## Concept

[Section titled “Concept”](#concept)

Query engine is a generic interface that allows you to ask question over your data.

A query engine takes in a natural language query, and returns a rich response.
It is most often (but not always) built on one or many [indexes](/python/framework/module_guides/indexing) via [retrievers](/python/framework/module_guides/querying/retriever).
You can compose multiple query engines to achieve more advanced capability.

Tip

If you want to have a conversation with your data (multiple back-and-forth
instead of a single question & answer), take a look at [Chat
Engine](/python/framework/module_guides/deploying/chat_engines)

## Usage Pattern

[Section titled “Usage Pattern”](#usage-pattern)

Get started with:

```
query_engine = index.as_query_engine()



response = query_engine.query("Who is Paul Graham.")
```

To stream response:

```
query_engine = index.as_query_engine(streaming=True)



streaming_response = query_engine.query("Who is Paul Graham.")



streaming_response.print_response_stream()
```

See the full [usage pattern](/python/framework/module_guides/deploying/query_engine/usage_pattern) for more details.

## Modules

[Section titled “Modules”](#modules)

Find all the modules in the [modules guide](/python/framework/module_guides/deploying/query_engine/modules).

## Supporting Modules

[Section titled “Supporting Modules”](#supporting-modules)

There are also [supporting modules](/python/framework/module_guides/deploying/query_engine/supporting_modules).