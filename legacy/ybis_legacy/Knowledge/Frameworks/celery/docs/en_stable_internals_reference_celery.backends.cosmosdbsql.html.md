celery.backends.cosmosdbsql — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.s3.html "celery.backends.s3") |
* [previous](celery.backends.filesystem.html "celery.backends.filesystem") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.cosmosdbsql`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.cosmosdbsql.html).

# `celery.backends.cosmosdbsql`[¶](#celery-backends-cosmosdbsql "Link to this heading")

The CosmosDB/SQL backend for Celery (experimental).

*class* celery.backends.cosmosdbsql.CosmosDBSQLBackend(*url=None*, *database\_name=None*, *collection\_name=None*, *consistency\_level=None*, *max\_retry\_attempts=None*, *max\_retry\_wait\_time=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend)[¶](#celery.backends.cosmosdbsql.CosmosDBSQLBackend "Link to this definition")
:   CosmosDB/SQL backend for Celery.

    delete(*key*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.delete)[¶](#celery.backends.cosmosdbsql.CosmosDBSQLBackend.delete "Link to this definition")
    :   Delete the value at a given key.

        Parameters:
        :   **key** – The key of the value to delete.

    get(*key*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.get)[¶](#celery.backends.cosmosdbsql.CosmosDBSQLBackend.get "Link to this definition")
    :   Read the value stored at the given key.

        Parameters:
        :   **key** – The key for which to read the value.

    mget(*keys*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.mget)[¶](#celery.backends.cosmosdbsql.CosmosDBSQLBackend.mget "Link to this definition")
    :   Read all the values for the provided keys.

        Parameters:
        :   **keys** – The list of keys to read.

    set(*key*, *value*)[[source]](../../_modules/celery/backends/cosmosdbsql.html#CosmosDBSQLBackend.set)[¶](#celery.backends.cosmosdbsql.CosmosDBSQLBackend.set "Link to this definition")
    :   Store a value for a given key.

        Parameters:
        :   * **key** – The key at which to store the value.
            * **value** – The value to store.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.filesystem`](celery.backends.filesystem.html "previous chapter")

#### Next topic

[`celery.backends.s3`](celery.backends.s3.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.cosmosdbsql.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.s3.html "celery.backends.s3") |
* [previous](celery.backends.filesystem.html "celery.backends.filesystem") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.cosmosdbsql`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.