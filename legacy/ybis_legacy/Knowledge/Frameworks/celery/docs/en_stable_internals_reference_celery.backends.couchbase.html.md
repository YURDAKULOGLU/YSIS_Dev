celery.backends.couchbase — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.arangodb.html "celery.backends.arangodb") |
* [previous](celery.backends.cassandra.html "celery.backends.cassandra") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.couchbase`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.couchbase.html).

# `celery.backends.couchbase`[¶](#celery-backends-couchbase "Link to this heading")

Couchbase result store backend.

*class* celery.backends.couchbase.CouchbaseBackend(*url=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend)[¶](#celery.backends.couchbase.CouchbaseBackend "Link to this definition")
:   Couchbase backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/couchbase/> is not available.

    bucket *= 'default'*[¶](#celery.backends.couchbase.CouchbaseBackend.bucket "Link to this definition")

    *property* connection[¶](#celery.backends.couchbase.CouchbaseBackend.connection "Link to this definition")

    delete(*key*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.delete)[¶](#celery.backends.couchbase.CouchbaseBackend.delete "Link to this definition")

    get(*key*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.get)[¶](#celery.backends.couchbase.CouchbaseBackend.get "Link to this definition")

    host *= 'localhost'*[¶](#celery.backends.couchbase.CouchbaseBackend.host "Link to this definition")

    key\_t[¶](#celery.backends.couchbase.CouchbaseBackend.key_t "Link to this definition")
    :   alias of [`str`](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")

    mget(*keys*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.mget)[¶](#celery.backends.couchbase.CouchbaseBackend.mget "Link to this definition")

    password *= None*[¶](#celery.backends.couchbase.CouchbaseBackend.password "Link to this definition")

    port *= 8091*[¶](#celery.backends.couchbase.CouchbaseBackend.port "Link to this definition")

    quiet *= False*[¶](#celery.backends.couchbase.CouchbaseBackend.quiet "Link to this definition")

    set(*key*, *value*)[[source]](../../_modules/celery/backends/couchbase.html#CouchbaseBackend.set)[¶](#celery.backends.couchbase.CouchbaseBackend.set "Link to this definition")

    supports\_autoexpire *= True*[¶](#celery.backends.couchbase.CouchbaseBackend.supports_autoexpire "Link to this definition")
    :   If true the backend must automatically expire results.
        The daily backend\_cleanup periodic task won’t be triggered
        in this case.

    timeout *= 2.5*[¶](#celery.backends.couchbase.CouchbaseBackend.timeout "Link to this definition")

    username *= None*[¶](#celery.backends.couchbase.CouchbaseBackend.username "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.cassandra`](celery.backends.cassandra.html "previous chapter")

#### Next topic

[`celery.backends.arangodb`](celery.backends.arangodb.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.couchbase.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.arangodb.html "celery.backends.arangodb") |
* [previous](celery.backends.cassandra.html "celery.backends.cassandra") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.couchbase`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.