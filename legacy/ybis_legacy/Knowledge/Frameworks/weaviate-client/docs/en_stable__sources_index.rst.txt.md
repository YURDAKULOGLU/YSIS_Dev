==================================================
Welcome to Weaviate Python Client's documentation!
==================================================
.. raw:: html
![Weaviate logo](https://raw.githubusercontent.com/semi-technologies/weaviate/19de0956c69b66c5552447e84d016f4fe29d12c9/docs/assets/weaviate-logo.png)
.. |build-status| image:: https://github.com/weaviate/weaviate-python-client/actions/workflows/main.yaml/badge.svg?branch=main
:target: https://github.com/weaviate/weaviate-python-client/actions/workflows/main.yaml
:alt: Build Status
.. |pypi-version| image:: https://badge.fury.io/py/weaviate-client.svg
:target: https://badge.fury.io/py/weaviate-client
:alt: PyPI version
|build-status| |pypi-version|
The Weaviate Python client makes it easy to work with `Weaviate `\_, an AI Native vector database. The client is tested for Python 3.8 and higher.
The current major version is \*\*v4\*\* while the older \*\*v3\*\* client is deprecated and should be avoided. You can find further documentation for both versions:
\* `Python Client v4 `\_
\* `Python Client v3 `\_ (deprecated)
.. note::
Follow the `Weaviate Quickstart guide `\_ to get up and running quickly.
Installation
------------
You can install the Weaviate Python client using pip:
.. code-block:: bash
pip install -U weaviate-client
See the `installation section `\_ in the main Weaviate documentation for more details.
Optional: Weaviate Agents
-------------------------
This client supports optional integration with `Weaviate Agents `\_, which are agentic pre-built services designed to simplify common LLM-related tasks like querying, transformation, and personalization using your Weaviate data.
To install the client with agent support, use the ``[agents]`` extra:
.. code-block:: bash
pip install -U "weaviate-client[agents]"
For detailed guides and usage examples for the different agents, please refer to the main `Weaviate Agents documentation `\_.
.. note::
Weaviate Agents require a connection to a `Weaviate Cloud (WCD) `\_ instance, local instances are not supported.
Client API reference
-------------
Explore the detailed API documentation:
\* :doc:`Weaviate Library `
\* :class:`~weaviate.WeaviateClient`
\* :class:`~weaviate.WeaviateAsyncClient`
\* :doc:`Weaviate Exceptions `
\* :doc:`Weaviate Agents `
\* :doc:`QueryAgent `
\* :doc:`TransformationAgent `
\* :doc:`PersonalizationAgent `
Support
-------
\* `Community Forum `\_
\* `Community Slack Channel `\_
\* Use the ``weaviate`` tag on `StackOverflow `\_ for questions.
\* For bugs or problems, submit a GitHub `issue `\_.
.. toctree::
:maxdepth: 2
:hidden:
:caption: Contents:
modules
weaviate.exceptions
weaviate-agents-python-client/docs/modules
changelog
genindex