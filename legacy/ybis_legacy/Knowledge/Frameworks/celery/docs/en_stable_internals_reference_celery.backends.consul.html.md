celery.backends.consul — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.couchdb.html "celery.backends.couchdb") |
* [previous](celery.backends.cache.html "celery.backends.cache") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* celery.backends.consul

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.consul.html).

# celery.backends.consul[¶](#celery-backends-consul "Link to this heading")

Consul result store backend.

* [`ConsulBackend`](#celery.backends.consul.ConsulBackend "celery.backends.consul.ConsulBackend") implements KeyValueStoreBackend to store results
  :   in the key-value store of Consul.

*class* celery.backends.consul.ConsulBackend(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend)[¶](#celery.backends.consul.ConsulBackend "Link to this definition")
:   Consul.io K/V store backend for Celery.

    client()[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.client)[¶](#celery.backends.consul.ConsulBackend.client "Link to this definition")

    consistency *= 'consistent'*[¶](#celery.backends.consul.ConsulBackend.consistency "Link to this definition")

    consul *= None*[¶](#celery.backends.consul.ConsulBackend.consul "Link to this definition")

    delete(*key*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.delete)[¶](#celery.backends.consul.ConsulBackend.delete "Link to this definition")

    get(*key*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.get)[¶](#celery.backends.consul.ConsulBackend.get "Link to this definition")

    mget(*keys*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.mget)[¶](#celery.backends.consul.ConsulBackend.mget "Link to this definition")

    path *= None*[¶](#celery.backends.consul.ConsulBackend.path "Link to this definition")

    set(*key*, *value*)[[source]](../../_modules/celery/backends/consul.html#ConsulBackend.set)[¶](#celery.backends.consul.ConsulBackend.set "Link to this definition")
    :   Set a key in Consul.

        Before creating the key it will create a session inside Consul
        where it creates a session with a TTL

        The key created afterwards will reference to the session’s ID.

        If the session expires it will remove the key so that results
        can auto expire from the K/V store

    supports\_autoexpire *= True*[¶](#celery.backends.consul.ConsulBackend.supports_autoexpire "Link to this definition")
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.cache`](celery.backends.cache.html "previous chapter")

#### Next topic

[`celery.backends.couchdb`](celery.backends.couchdb.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.consul.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.couchdb.html "celery.backends.couchdb") |
* [previous](celery.backends.cache.html "celery.backends.cache") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* celery.backends.consul

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.