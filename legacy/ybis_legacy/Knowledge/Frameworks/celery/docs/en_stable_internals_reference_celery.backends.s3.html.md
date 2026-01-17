celery.backends.s3 — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.gcs.html "celery.backends.gcs") |
* [previous](celery.backends.cosmosdbsql.html "celery.backends.cosmosdbsql") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.s3`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.s3.html).

# `celery.backends.s3`[¶](#celery-backends-s3 "Link to this heading")

s3 result store backend.

*class* celery.backends.s3.S3Backend(*\*\*kwargs*)[[source]](../../_modules/celery/backends/s3.html#S3Backend)[¶](#celery.backends.s3.S3Backend "Link to this definition")
:   An S3 task result store.

    Raises:
    :   [**celery.exceptions.ImproperlyConfigured**](../../reference/celery.exceptions.html#celery.exceptions.ImproperlyConfigured "celery.exceptions.ImproperlyConfigured") – if module <https://pypi.org/project/boto3/> is not available,
        if the `aws_access_key_id` or
        setting:aws\_secret\_access\_key are not set,
        or it the `bucket` is not set.

    delete(*key*)[[source]](../../_modules/celery/backends/s3.html#S3Backend.delete)[¶](#celery.backends.s3.S3Backend.delete "Link to this definition")

    get(*key*)[[source]](../../_modules/celery/backends/s3.html#S3Backend.get)[¶](#celery.backends.s3.S3Backend.get "Link to this definition")

    set(*key*, *value*)[[source]](../../_modules/celery/backends/s3.html#S3Backend.set)[¶](#celery.backends.s3.S3Backend.set "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.cosmosdbsql`](celery.backends.cosmosdbsql.html "previous chapter")

#### Next topic

[`celery.backends.gcs`](celery.backends.gcs.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.s3.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.gcs.html "celery.backends.gcs") |
* [previous](celery.backends.cosmosdbsql.html "celery.backends.cosmosdbsql") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.s3`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.