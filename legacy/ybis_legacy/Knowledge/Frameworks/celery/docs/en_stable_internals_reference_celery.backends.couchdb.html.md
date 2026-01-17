celery.backends.couchdb — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.mongodb.html "celery.backends.mongodb") |
* [previous](celery.backends.consul.html "celery.backends.consul") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.couchdb`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.couchdb.html).

# `celery.backends.couchdb`[¶](#celery-backends-couchdb "Link to this heading")

CouchDB result store backend.

*class* celery.backends.couchdb.CouchBackend(*url=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend)[¶](#celery.backends.couchdb.CouchBackend "Link to this definition")
:   CouchDB backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/pycouchdb/> is not available.

    *property* connection[¶](#celery.backends.couchdb.CouchBackend.connection "Link to this definition")

    container *= 'default'*[¶](#celery.backends.couchdb.CouchBackend.container "Link to this definition")

    delete(*key*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.delete)[¶](#celery.backends.couchdb.CouchBackend.delete "Link to this definition")

    get(*key*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.get)[¶](#celery.backends.couchdb.CouchBackend.get "Link to this definition")

    host *= 'localhost'*[¶](#celery.backends.couchdb.CouchBackend.host "Link to this definition")

    mget(*keys*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.mget)[¶](#celery.backends.couchdb.CouchBackend.mget "Link to this definition")

    password *= None*[¶](#celery.backends.couchdb.CouchBackend.password "Link to this definition")

    port *= 5984*[¶](#celery.backends.couchdb.CouchBackend.port "Link to this definition")

    scheme *= 'http'*[¶](#celery.backends.couchdb.CouchBackend.scheme "Link to this definition")

    set(*key*, *value*)[[source]](../../_modules/celery/backends/couchdb.html#CouchBackend.set)[¶](#celery.backends.couchdb.CouchBackend.set "Link to this definition")

    username *= None*[¶](#celery.backends.couchdb.CouchBackend.username "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[celery.backends.consul](celery.backends.consul.html "previous chapter")

#### Next topic

[`celery.backends.mongodb`](celery.backends.mongodb.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.couchdb.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.mongodb.html "celery.backends.mongodb") |
* [previous](celery.backends.consul.html "celery.backends.consul") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.couchdb`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.