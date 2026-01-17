Welcome to Weaviate Python Client’s documentation! — Weaviate Python Client 4.19.2 documentation



* Welcome to Weaviate Python Client’s documentation!
* [View page source](_sources/index.rst.txt)

---

# Welcome to Weaviate Python Client’s documentation![](#welcome-to-weaviate-python-client-s-documentation "Link to this heading")

![Weaviate logo](https://raw.githubusercontent.com/semi-technologies/weaviate/19de0956c69b66c5552447e84d016f4fe29d12c9/docs/assets/weaviate-logo.png)

[![Build Status](https://github.com/weaviate/weaviate-python-client/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/weaviate/weaviate-python-client/actions/workflows/main.yaml) [![PyPI version](https://badge.fury.io/py/weaviate-client.svg)](https://badge.fury.io/py/weaviate-client)

The Weaviate Python client makes it easy to work with [Weaviate](https://weaviate.io/), an AI Native vector database. The client is tested for Python 3.8 and higher.

The current major version is **v4** while the older **v3** client is deprecated and should be avoided. You can find further documentation for both versions:

* [Python Client v4](https://weaviate.io/developers/weaviate/client-libraries/python)
* [Python Client v3](https://weaviate.io/developers/weaviate/client-libraries/python_v3) (deprecated)

Note

Follow the [Weaviate Quickstart guide](https://weaviate.io/developers/weaviate/quickstart) to get up and running quickly.

## Installation[](#installation "Link to this heading")

You can install the Weaviate Python client using pip:

```
pip install -U weaviate-client
```

See the [installation section](https://weaviate.io/developers/weaviate/client-libraries/python#installation) in the main Weaviate documentation for more details.

## Optional: Weaviate Agents[](#optional-weaviate-agents "Link to this heading")

This client supports optional integration with [Weaviate Agents](https://weaviate.io/developers/agents/), which are agentic pre-built services designed to simplify common LLM-related tasks like querying, transformation, and personalization using your Weaviate data.

To install the client with agent support, use the `[agents]` extra:

```
pip install -U "weaviate-client[agents]"
```

For detailed guides and usage examples for the different agents, please refer to the main [Weaviate Agents documentation](https://weaviate.io/developers/agents/).

Note

Weaviate Agents require a connection to a [Weaviate Cloud (WCD)](https://weaviate.io/developers/wcs/) instance, local instances are not supported.

## Client API reference[](#client-api-reference "Link to this heading")

Explore the detailed API documentation:

* [Weaviate Library](modules.html)
  :   + [`WeaviateClient`](weaviate.html#weaviate.WeaviateClient "weaviate.WeaviateClient")
      + [`WeaviateAsyncClient`](weaviate.html#weaviate.WeaviateAsyncClient "weaviate.WeaviateAsyncClient")
* [Weaviate Exceptions](weaviate.exceptions.html)
* [Weaviate Agents](weaviate-agents-python-client/docs/modules.html)
  :   + [QueryAgent](weaviate-agents-python-client/docs/weaviate_agents.query.html)
      + [TransformationAgent](weaviate-agents-python-client/docs/weaviate_agents.transformation.html)
      + [PersonalizationAgent](weaviate-agents-python-client/docs/weaviate_agents.personalization.html)

## Support[](#support "Link to this heading")

* [Community Forum](https://forum.weaviate.io)
* [Community Slack Channel](https://weaviate.io/slack)
* Use the `weaviate` tag on [StackOverflow](https://stackoverflow.com/questions/tagged/weaviate) for questions.
* For bugs or problems, submit a GitHub [issue](https://github.com/weaviate/weaviate-python-client/issues).