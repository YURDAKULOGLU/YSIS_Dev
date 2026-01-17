celery.backends.elasticsearch — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.redis.html "celery.backends.redis") |
* [previous](celery.backends.mongodb.html "celery.backends.mongodb") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.elasticsearch`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.elasticsearch.html).

# `celery.backends.elasticsearch`[¶](#celery-backends-elasticsearch "Link to this heading")

Elasticsearch result store backend.

*class* celery.backends.elasticsearch.ElasticsearchBackend(*url=None*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend)[¶](#celery.backends.elasticsearch.ElasticsearchBackend "Link to this definition")
:   Elasticsearch Backend.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/elasticsearch/> is not available.

    decode(*payload*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.decode)[¶](#celery.backends.elasticsearch.ElasticsearchBackend.decode "Link to this definition")

    delete(*key*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.delete)[¶](#celery.backends.elasticsearch.ElasticsearchBackend.delete "Link to this definition")

    doc\_type *= None*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.doc_type "Link to this definition")

    encode(*data*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.encode)[¶](#celery.backends.elasticsearch.ElasticsearchBackend.encode "Link to this definition")

    es\_max\_retries *= 3*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.es_max_retries "Link to this definition")

    es\_retry\_on\_timeout *= False*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.es_retry_on_timeout "Link to this definition")

    es\_timeout *= 10*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.es_timeout "Link to this definition")

    exception\_safe\_to\_retry(*exc*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.exception_safe_to_retry)[¶](#celery.backends.elasticsearch.ElasticsearchBackend.exception_safe_to_retry "Link to this definition")
    :   Check if an exception is safe to retry.

        Backends have to overload this method with correct predicates dealing with their exceptions.

        By default no exception is safe to retry, it’s up to backend implementation
        to define which exceptions are safe.

    get(*key*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.get)[¶](#celery.backends.elasticsearch.ElasticsearchBackend.get "Link to this definition")

    host *= 'localhost'*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.host "Link to this definition")

    index *= 'celery'*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.index "Link to this definition")

    mget(*keys*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.mget)[¶](#celery.backends.elasticsearch.ElasticsearchBackend.mget "Link to this definition")

    password *= None*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.password "Link to this definition")

    port *= 9200*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.port "Link to this definition")

    scheme *= 'http'*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.scheme "Link to this definition")

    *property* server[¶](#celery.backends.elasticsearch.ElasticsearchBackend.server "Link to this definition")

    set(*key*, *value*)[[source]](../../_modules/celery/backends/elasticsearch.html#ElasticsearchBackend.set)[¶](#celery.backends.elasticsearch.ElasticsearchBackend.set "Link to this definition")

    username *= None*[¶](#celery.backends.elasticsearch.ElasticsearchBackend.username "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.mongodb`](celery.backends.mongodb.html "previous chapter")

#### Next topic

[`celery.backends.redis`](celery.backends.redis.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.elasticsearch.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.redis.html "celery.backends.redis") |
* [previous](celery.backends.mongodb.html "celery.backends.mongodb") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.elasticsearch`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.